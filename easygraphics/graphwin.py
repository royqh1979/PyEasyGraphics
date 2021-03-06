import os
import threading
import time
import queue
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from easygraphics.image import Image
from easygraphics.consts import Color, MouseMessageType

__all__ = ['GraphWin']


class GraphWin(QtWidgets.QWidget):
    """
    Main Window for painting graphics

    we use an Image object (self._canvas) to save the painted contents

    how to process repaint event:

    if we are in immediate mode (RENDER_AUTO, self._immediate=True) , \
    we directly paint the saved contents to the window

    if we are in manual refresh mode (RENDER_MANUAL, self._immediate=False), \
    we use another image object( self._device_image) as an intermediary .\
    The contents on this object is painted to the window  and this object is synced with self._canvas manually
    """

    def __init__(self, width: int, height: int):
        super().__init__(flags=QtCore.Qt.Window | QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self._width = width
        self._height = height
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self._wait_event = threading.Event()
        self._key_msg_queue = queue.Queue(10)
        self._key_char_msg_queue = queue.Queue(10)
        self._mouse_msg_queue = queue.Queue(10)
        self.setGeometry(100, 100, width, height)
        self._init_screen(width, height)
        self._is_run = True
        self._immediate = True
        self.set_immediate(True)
        self._skip_count = 0
        self._frames_to_skip_count = 0
        self._last_fps_time = 0
        self._frames_skipped = 0
        self._capture_dir = "."
        self._capture_count = 0

    def resize(self,width:int,height:int):
        self._width = width
        self._height = height
        self.setGeometry(100, 100, width, height)
        _old_canvas = self._canvas
        _old_canvas.close()
        self._init_screen(width, height)

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def _init_screen(self, width, height):
        screen_image = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32_Premultiplied)
        screen_image.fill(Color.WHITE)
        self._canvas = Image(screen_image)
        self._device_image = screen_image.copy()
        self.real_update()

    def get_canvas(self):
        return self._canvas

    def paintEvent(self, e):
        if self._immediate:
            self._canvas.draw_to_device(self)
        else:
            p = QtGui.QPainter()
            p.begin(self)
            p.drawImage(0, 0, self._device_image)
            p.end()

    def set_immediate(self, immediate: bool):
        """
        set if the graphics window will be updated immediately after things are drawn

        possible values:

        * **True** (default, auto mode) update the window immediately after every drawing
        * **False** (manual mode) only update the window after pause()/delay()/delay_fps()/delay_jfps() is called.

        manual mode is used for animations

        :param immediate:  if the graphics window will be updated immediately
        """
        self._immediate = immediate
        if immediate:
            self._canvas.add_updated_listener(self.update)
        else:
            self._canvas.remove_updated_listener(self.update)

    def close(self):
        self._key_msg_queue.queue.clear()
        self._key_char_msg_queue.queue.clear()
        self._mouse_msg_queue.queue.clear()
        if self._immediate:
            self._canvas.remove_updated_listener(self.update)
        self._is_run = False
        self._wait_event.set()

    def is_immediate(self) -> bool:
        """
        get if the graphics window will be updated immediately after things are drawn

        :return:
        """
        return self._immediate

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        self._wait_event.set()
        mouse_msg=MouseMessage(e, MouseMessageType.PRESS_MESSAGE)
        try:
            self._mouse_msg_queue.put_nowait(mouse_msg)
        except queue.Full as err:
            pass

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent) -> None:
        mouse_msg=MouseMessage(e, MouseMessageType.DOUBLE_CLICK_MESSAGE)
        try:
            self._mouse_msg_queue.put_nowait(mouse_msg)
        except queue.Full as err:
            pass

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        mouse_msg=MouseMessage(e, MouseMessageType.RELEASE_MESSAGE)
        try:
            self._mouse_msg_queue.put_nowait(mouse_msg)
        except queue.Full as err:
            pass

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        self._wait_event.set()
        if e.key() == QtCore.Qt.Key_F10:
            modifiers = e.modifiers()
            if modifiers & (QtCore.Qt.ControlModifier |
                            QtCore.Qt.ShiftModifier |
                            QtCore.Qt.AltModifier):
                self._capture_count += 1
                self._canvas.save(self._capture_dir + os.sep + "save{0}.png".format(self._capture_count))
        if e.key() < 127 or e.key() == QtCore.Qt.Key_Return:
            # ascii char key pressed
            key_char_msg = _KeyCharMsg(e)
            try:
                self._key_char_msg_queue.put_nowait(key_char_msg)
            except queue.Full as err:
                pass
        key_msg = KeyMessage(e)
        try:
            self._key_msg_queue.put_nowait(key_msg)
        except queue.Full as err:
            pass

    def pause(self):
        """
        pause and wait for mouse click or keyboard hit
        """
        if not self._is_run:
            return
        self.real_update()
        self._wait_event.clear()
        self._wait_event.wait()

    def closeEvent(self, e: QtGui.QCloseEvent):
        self.close()

    def is_run(self) -> bool:
        return self._is_run

    def real_update(self):
        """
        really update and repaint the window

        the intermediary image (self._device_image) is synced with the canvas
        """
        self._canvas.draw_to_device(self._device_image)
        self.update()

    def delay(self, milliseconds: float):
        """
        Delay the program for specified milliseconds.

        :param milliseconds: time to delay
        """
        if self._immediate:
            raise RuntimeError("Must set render mode to MANUAL to use delay()!")
        if not self._is_run:
            return
        self.real_update()
        nanotime = milliseconds * 1000000
        start_wait_time = time.perf_counter_ns()
        if time.perf_counter_ns() - start_wait_time < nanotime:
            QtCore.QThread.usleep((start_wait_time + nanotime - time.perf_counter_ns()) // 1000)

    def delay_fps(self, fps: int) -> bool:
        """
        Delay to control fps without frame skipping. Never skip frames.

        :param fps: the desire fps
        :return: False the graphics window is closed. True otherwise.
        """
        if self._immediate:
            raise RuntimeError("Must set render mode to MANUAL to use delay()!")
        if not self._is_run:
            return False
        nanotime = 1000000000 // fps
        if self._last_fps_time == 0:
            self._last_fps_time = time.perf_counter_ns()
        self.real_update()
        tt = time.perf_counter_ns()
        # print(tt)
        if tt - self._last_fps_time < nanotime:
            QtCore.QThread.usleep((self._last_fps_time + nanotime - tt) // 1000)
        self._last_fps_time = time.perf_counter_ns()
        return True

    def delay_jfps(self, fps: int, max_skip_count: int = 10) -> bool:
        """
        Delay to control fps with frame skipping.

        If we don't have enough time to delay, we'll skip some frames.

        :param fps: frames per second (max is 1000)
        :param max_skip_count: max num of  frames to skip
        :return: True if this frame should not be skipped
        """
        if self._immediate:
            raise RuntimeError("Must set render mode to MANUAL to use delay()!")
        if not self._is_run:
            return False
        nanotime = 1000000000 // fps
        if self._frames_to_skip_count > 0:
            self._frames_to_skip_count -= 1
            self._frames_skipped += 1
            return False
        if self._last_fps_time == 0:
            self._last_fps_time = time.perf_counter_ns()

        nowtime = time.perf_counter_ns()
        if self._last_fps_time + nanotime < nowtime:
            if self._frames_skipped <= max_skip_count:
                # we don't have to draw this frame, so let's skip it
                self._frames_to_skip_count = round((nowtime - self._last_fps_time) // nanotime)
                if max_skip_count <= 0:
                    self._frames_to_skip_count -= 1
                    self._last_fps_time = time.perf_counter_ns()
                    return False
                elif self._frames_to_skip_count > max_skip_count - self._frames_skipped:
                    self._frames_to_skip_count = (max_skip_count - self._frames_skipped) - 1
                    self._frames_skipped += 1
                    self._last_fps_time = time.perf_counter_ns()
                    return False
            else:
                self._frames_skipped = 0
        self.real_update()
        tt = time.perf_counter_ns()
        sleep_time = (self._last_fps_time + nanotime - tt) // 1000
        if sleep_time > 0:
            QtCore.QThread.usleep(sleep_time)
        self._last_fps_time = time.perf_counter_ns()
        return True

    def get_char(self) -> str:
        """
        Get the ascii char inputted by keyboard.

        If not any char key is pressed in last 100 ms, the program will stop and wait for the next key hitting.

        :return: the character inputted by keyboard
        """
        if not self._is_run:
            return ' '
        nt = time.perf_counter_ns()
        self.real_update()
        while True:
            try:
                key_char_msg = self._key_char_msg_queue.get(True,0.1)
                return key_char_msg.char
            except queue.Empty as err:
                if not self._is_run:
                    return ''
                pass



    def get_key(self) -> "KeyMessage":
        """
        Get the key inputted by keyboard.

        If not any  key is pressed in last 100 ms, the program will stop and wait for the next key hitting.

        :return: key message
        """
        if not self._is_run:
            return QtCore.Qt.Key_Escape, QtCore.Qt.NoModifier
        nt = time.perf_counter_ns()
        self.real_update()
        while True:
            try:
                key_msg = self._key_msg_queue.get(True,0.1)
                return key_msg
            except queue.Empty as err:
                if not self._is_run:
                    return KeyMessage(None)
                pass



    def get_mouse_msg(self) -> "MouseMessage":
        """
        Get the mouse message.

        If there is not any  mouse message, the program will stop and wait for it.

        :return: mouse message
        """
        if not self._is_run:
            return 0, 0, 0, QtCore.Qt.NoButton
        nt = time.perf_counter_ns()
        self.real_update()
        while True:
            try:
                mouse_msg = self._mouse_msg_queue.get(True,0.1)
                return mouse_msg
            except queue.Empty as err:
                if not self._is_run:
                    return MouseMessage(None,None)
                pass

    def get_click(self) -> "MouseMessage":
        """
        Get the mouse click message.

        If there isn't any clicked event, the program will stop and wait for it.

        :return: mouse message
        """
        while self._is_run:
            msg = self.get_mouse_msg()
            if msg == MouseMessageType.NO_MESSAGE or\
                    msg.type == MouseMessageType.RELEASE_MESSAGE and (msg.button & QtCore.Qt.LeftButton) > 0:
                return msg
        return MouseMessage(None,None)

    def has_kb_hit(self) -> bool:
        """
        See if any ascii char key hit message in the message queue.

        Use it with get_char().

        :return:  True if hit, False otherwise
        """
        return not self._key_char_msg_queue.empty()

    def has_kb_msg(self) -> bool:
        """
        See if any key hit message in the message queue.

        Use it with get_key().

        :return:  True if hit, False otherwise
        """
        return not self._key_msg_queue.empty()

    def has_mouse_msg(self) -> bool:
        """
        See if there is any mouse message(event) in the message queue.

        Use it with get_mouse_msg().

        :return:  True if any mouse message, False otherwise
        """
        return not self._mouse_msg_queue.empty()

    def get_cursor_pos(self) -> (int, int):
        """
        Get position of the mouse cursor

        :return: position's coordinate values (x,y)
        """
        p = self.mapFromGlobal(QtGui.QCursor.pos())
        return p.x(), p.y()

    def clear_key_msg(self):
        """
        Clear all keyboard hit messages.
        """
        self._key_msg_queue.queue.clear()

    def clear_char_msg(self):
        """
        Clear all char key hit messages.
        """
        self._key_char_msg_queue.queue.clear()

    def clear_mouse_msg(self):
        """
        Clear all mouse messages.
        """
        self._mouse_msg_queue.queue.clear()

class KeyMessage:
    """
    class for saving keyboard message
    """

    def __init__(self,key_event: QtGui.QKeyEvent):
        if key_event is None:
            self.key = None
            self.char = ''
            self.count = 0
            self.modifiers = QtCore.Qt.NoModifier
        else:
            self.key = key_event.key()
            self.char = key_event.text()
            self.count = key_event.count()
            self.modifiers = key_event.modifiers()


class _KeyCharMsg:
    """
    class for saving keyboard hit char
    """

    def __init__(self, key_event: QtGui.QKeyEvent):
        self.char = key_event.text()

class MouseMessage:
    def __init__(self, e: QtGui.QMouseEvent, _type: MouseMessageType):
        if e is None:
            self.x = 0
            self.y = 0
            self.modifiers = QtCore.Qt.NoModifier
            self.global_x = 0
            self.global_y = 0
            self.type = MouseMessageType.NO_MESSAGE
            self.button = QtCore.Qt.NoButton
        else:
            self.x = e.x()
            self.y = e.y()
            self.modifiers = e.modifiers()
            self.global_x = e.globalX()
            self.global_y = e.globalY()
            self.type = _type
            self.button = e.button()
