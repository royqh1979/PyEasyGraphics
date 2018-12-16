import threading
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from easygraphics.image import Image


class GraphWin(QWidget):
    """
    Main Window for painting graphics


    we use an Image object (self._canvas) to save the painted contents

    how to process repaint event:
    if we are in immediate mode (RENDER_AUTO, self._immediate=True) ,
        we directly paint the saved contents to the window
    if we are in manual refresh mode (RENDER_MANUAL, self._immediate=False),
        we use another image object( self._device_image) as an intermediary
        the contents on this object is painted to the window
        and this object is synced with self._screen manually
    """

    def __init__(self, width, height, app: QApplication):
        super().__init__();
        self._width = width;
        self._height = height;
        self._waitEvent = threading.Event()
        self._mouseEvent = threading.Event()
        self._keyEvent = threading.Event()
        self.setGeometry(100, 100, width, height)
        self._init_screen(width, height)
        self._is_run = True
        self._immediate = True
        self._last_update_time = time.time_ns()
        self._skip_count = 0
        self._app = app

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def _init_screen(self, width, height):
        screen_image = QImage(width, height, QImage.Format_ARGB32_Premultiplied)
        p = QPainter()
        p.begin(screen_image)
        p.fillRect(0, 0, width, height, Qt.white)
        p.end()
        self._canvas = Image(screen_image)
        self._device_image = screen_image.copy()
        self.real_update()

    def get_canvas(self):
        return self._canvas;

    def paintEvent(self, e):
        p = QPainter()
        p.begin(self)
        if self._immediate:
            p.drawImage(0, 0, self._canvas.get_image())
        else:
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
        self._immediate = immediate

    def is_immediate(self) -> bool:
        return self._immediate

    def mousePressEvent(self, QMouseEvent):
        self._waitEvent.set()
        self._mouseEvent.set()

    def keyPressEvent(self, QKeyEvent):
        self._waitEvent.set()
        self._keyEvent.set()

    def pause(self):
        self._waitEvent.clear()
        self._waitEvent.wait()

    def closeEvent(self, QCloseEvent):
        self._is_run = False
        self._waitEvent.set()
        self._app.quit()

    def is_run(self) -> bool:
        return self._is_run

    def real_update(self):
        """
        really update and repaint the window

        the intermediary image (self._device_image) is synced with the canvas
        """
        painter = QPainter()
        painter.begin(self._device_image)
        painter.drawImage(0, 0, self._canvas.get_image().copy())
        painter.end()
        self.update()
        self._last_update_time = time.time_ns()

    def delay(self, milliseconds):
        nanotime = milliseconds * 1000000
        start_wait_time = time.time_ns()
        self.real_update()
        while time.time_ns() - start_wait_time < nanotime:
            time.time_ns()

    def delay_fps(self, fps):
        nanotime = 1000000000 // fps
        if self._last_update_time == 0:
            self._last_update_time = time.time_ns()
        while time.time_ns() - self._last_update_time < nanotime:
            time.time_ns()
        self.real_update()

    def delay_jfps(self, fps, max_skip_count=10):
        nanotime = 1000000000 // fps
        if self._last_update_time == 0:
            self._last_update_time = time.time_ns()
        nowtime = time.time_ns()
        if self._last_update_time + nanotime < nowtime:
            # we don't have to draw this frame, so let's skip it
            self._skip_count += 1
            if self._skip_count < max_skip_count:
                self._last_update_time = time.time_ns()
                return
            else:
                # we have skipped too many frames, draw this frame
                self._skip_count = 0
        while time.time_ns() - self._last_update_time < nanotime:
            time.time_ns()
        self.real_update()
