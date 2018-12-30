import threading
import time
import math
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

    def __init__(self, width: int, height: int, app: QtWidgets.QApplication):
        super().__init__(flags=QtCore.Qt.Window | QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self._width = width
        self._height = height
        self._wait_event = threading.Event()
        self._mouse_event = threading.Event()
        self._key_event = threading.Event()
        self._char_key_event = threading.Event()
        self._key_msg = _KeyMsg()
        self._key_char_msg = _KeyCharMsg()
        self._mouse_msg = _MouseMsg()
        self.setGeometry(100, 100, width, height)
        self._init_screen(width, height)
        self._is_run = True
        self._immediate = True
        self._skip_count = 0
        self._app = app
        self._frames_to_skip_count = 0
        self._last_fps_time = 0
        self._frames_skipped = 0

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

    def invalid(self):
        """
        try to invalidate window

        if is in immediate mode (MODE_AUTO), the window is updated and repaint;
        otherwise, the window is not updated
        """
        if self._immediate:
            self.update()

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

    def is_immediate(self) -> bool:
        """
        get if the graphics window will be updated immediately after things are drawn

        :return:
        """
        return self._immediate

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        self._wait_event.set()
        self._mouse_msg.set_event(e, MouseMessageType.PRESS_MESSAGE)
        self._mouse_event.set()

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        self._mouse_msg.set_event(e, MouseMessageType.RELEASE_MESSAGE)
        self._mouse_event.set()

    def keyPressEvent(self, e: QtGui.QKeyEvent):
        self._wait_event.set()
        if e.key() < 127 or e.key() == QtCore.Qt.Key_Return:
            # ascii char key pressed
            self._key_char_msg.set_char(e)
            self._char_key_event.set()
        self._key_msg.set_event(e)
        self._key_event.set()

    def pause(self):
        """
        pause and wait for mouse click or keyboard hit
        """
        self.real_update()
        self._wait_event.clear()
        self._wait_event.wait()

    def closeEvent(self, e: QtGui.QCloseEvent):
        self._is_run = False
        self._canvas.close()
        self._wait_event.set()
        self._mouse_event.set()
        self._key_event.set()
        self._char_key_event.set()
        self._app.quit()

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
        delay for milliseconds
        :param milliseconds: time to delay
        """
        nanotime = milliseconds * 1000000
        start_wait_time = time.time_ns()
        self.real_update()
        while time.time_ns() - start_wait_time < nanotime:
            time.time_ns()

    def delay_fps(self, fps: int):
        """
        delay to control fps without frame skiping

        never skip frames

        :param fps: the desire fps
        """
        nanotime = 1000000000 // fps
        if self._last_fps_time == 0:
            self._last_fps_time = time.time_ns()
        self.real_update()
        tt = time.time_ns()
        while tt - self._last_fps_time < nanotime:
            tt = time.time_ns()
        self._last_fps_time = tt

    def delay_jfps(self, fps: int, max_skip_count: int = 10) -> bool:
        """
        delay to control fps with frame skiping

        if we don't have enough time to delay, we'll skip some frames

        :param fps: frames per second (max is 1000)
        :param max_skip_count: max num of  frames to skip
        :return: True if this frame should not be skipped
        """
        nanotime = 1000000000 // fps
        if self._frames_to_skip_count > 0:
            self._frames_to_skip_count -= 1
            self._frames_skipped += 1
            return False
        if self._last_fps_time == 0:
            self._last_fps_time = time.time_ns()

        nowtime = time.time_ns()
        if self._last_fps_time + nanotime < nowtime:
            if self._frames_skipped <= max_skip_count:
                # we don't have to draw this frame, so let's skip it
                self._frames_to_skip_count = round((nowtime - self._last_fps_time) // nanotime)
                if self._frames_to_skip_count > max_skip_count - self._frames_skipped:
                    self._frames_to_skip_count = (max_skip_count - self._frames_skipped) - 1
                    self._frames_skipped += 1
                    return False
            else:
                self._frames_skipped = 0
        self.real_update()
        tt = time.time_ns()
        while tt - self._last_fps_time < nanotime:
            tt = time.time_ns()
        self._last_fps_time = tt
        return True

    def get_char(self) -> str:
        """
        get the ascii char inputted by keybord
        if not any char key is pressed in last 100 ms, the program will stop and wait for the next key hitting

        :return: the character inputted by keybord
        """
        nt = time.time_ns()
        self.real_update()
        if nt - self._key_char_msg.get_time() > 100000000:
            # if the last char msg is 100ms ago, we wait for a new msg
            self._char_key_event.clear()
            self._char_key_event.wait()
        if not self._is_run:
            return ' '
        ch = self._key_char_msg.get_char()
        self._key_char_msg.reset()
        return ch

    def get_key(self) -> (int, int):
        """
        get the key inputted by keyboard
        if not any  key is pressed in last 100 ms, the program will stop and wait for the next key hitting

        :return: `keyboard code <http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#Key-enum/>`_ ,
            `keyboard modifier codes <http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#KeyboardModifier-enum)/>`_
        """
        nt = time.time_ns()
        self.real_update()
        if nt - self._key_msg.get_time() > 100000000:
            # if the last key msg is 100ms ago, we wait for a new msg
            self._key_event.clear()
            self._key_event.wait()
        if not self._is_run:
            return QtCore.Qt.Key_Escape, QtCore.Qt.NoModifier
        e = self._key_msg.get_event()
        self._key_msg.reset()
        return e.key(), e.modifiers()

    def get_mouse_msg(self) -> (int, int, int, int):
        """
        Get the mouse message.

        If there is not any  mouse button is pressed or released in last 100 ms, the program will stop and wait
        for the next key hitting.


        :return: x of the cursor, y of the cursor , type, mouse buttons down
            ( QtCore.Qt.LeftButton or QtCore.Qt.RightButton or QtCore.Qt.MidButton or QtCore.Qt.NoButton)
        """
        nt = time.time_ns()
        self.real_update()
        if nt - self._mouse_msg.get_time() > 100000000:
            # if the last key msg is 100ms ago, we wait for a new msg
            self._mouse_event.clear()
            self._mouse_event.wait()
        if not self._is_run:
            return 0, 0, 0, QtCore.Qt.NoButton
        e = self._mouse_msg.get_event()
        type = self._mouse_msg.get_type()
        self._mouse_msg.reset()
        return e.x(), e.y(), type, e.button()

    def has_kb_hit(self) -> bool:
        """
        see if any ascii char key is hitted in the last 100 ms
        use it with get_char()

        :return:  True if hitted, False or not
        """
        nt = time.time_ns()
        return nt - self._key_char_msg.get_time() <= 100000000

    def has_kb_msg(self) -> bool:
        """
        see if any key is hitted in the last 100 ms
        use it with get_key()

        :return:  True if hitted, False or not
        """
        nt = time.time_ns()
        return nt - self._key_char_msg.get_time() <= 100000000

    def has_mouse_msg(self) -> bool:
        """
        see if there's any mouse message(event) in the last 100 ms
        use it with get_mouse_msg()

        :return:  True if any mouse message, False or not
        """
        nt = time.time_ns()
        return nt - self._mouse_msg.get_time() <= 100000000

    def get_cursor_pos(self) -> (int, int):
        """
        Get position of the mouse cursor

        :return: position's coordinate values (x,y)
        """
        p = self.mapFromGlobal(QtGui.QCursor.pos())
        return p.x(), p.y()


class _KeyMsg:
    """
    class for saving keyboard message
    """

    def __init__(self):
        self._time = 0
        self._key_event = None

    def set_event(self, key_event: QtGui.QKeyEvent):
        self._key_event = key_event
        self._time = time.time_ns()

    def get_event(self) -> QtGui.QKeyEvent:
        return self._key_event

    def get_time(self) -> int:
        return self._time

    def reset(self):
        self._time = 0
        self._key_event = None


class _KeyCharMsg:
    """
    class for saving keyboard hit char
    """

    def __init__(self):
        self._time = 0
        self._key = None

    def set_char(self, key_event: QtGui.QKeyEvent):
        key_event.key()
        self._key = key_event.text()
        self._time = time.time_ns()

    def get_char(self) -> str:
        return self._key

    def get_time(self):
        return self._time

    def reset(self):
        self._time = 0
        self._key = None


class _MouseMsg:
    def __init__(self):
        self._time = 0
        self._mouse_event = None
        self._type = MouseMessageType.NO_MESSAGE

    def set_event(self, e: QtGui.QMouseEvent, type: int):
        self._mouse_event = e
        self._time = time.time_ns()
        self._type = type

    def get_event(self) -> QtGui.QMouseEvent:
        return self._mouse_event

    def get_time(self):
        return self._time

    def get_type(self):
        return self._type

    def reset(self):
        self._time = 0
        self._mouse_event = None
        self._type = MouseMessageType.NO_MESSAGE
