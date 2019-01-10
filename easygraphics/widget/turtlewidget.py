from easygraphics.image import Image
from easygraphics.turtle import TurtleWorld, Turtle
import time
import threading
from PyQt5 import QtCore, QtWidgets, QtGui

__all__ = ['TurtleWidget']


class TurtleWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, width=600, height=400):
        super().__init__(parent)
        self._image = Image.create(width, height)
        self._canvas = Image.create(width, height)
        self.setFixedWidth(self._image.get_width())
        self.setFixedHeight(self._image.get_height())
        self._world = TurtleWorld(self._image)
        self._world.set_immediate(False)
        self._turtle = self._world.create_turtle()
        self._is_running = True
        self._last_fps_time = 0

    def closeEvent(self, e: QtGui.QCloseEvent):
        self.close()
        super().closeEvent(e)

    def close(self):
        self._is_running = False
        self._world.close()
        self._image.close()
        super().close()

    def hideEvent(self, QHideEvent):
        self._is_running = False

    def showEvent(self, QShowEvent):
        self._start_refresh_loop()

    def is_run(self):
        return self._is_running

    def getWorld(self) -> TurtleWorld:
        return self._world

    def getTurtle(self) -> Turtle:
        return self._turtle

    def paintEvent(self, e: QtGui.QPaintEvent):
        self._canvas.draw_to_device(self)

    def _refresh(self):
        self._world.snap_shot_to_image(self._canvas)

    def _start_refresh_loop(self):
        self._refresh_thread = threading.Thread(target=self._refresh_loop)
        self._refresh_thread.start()

    def _refresh_loop(self):
        while self.is_run():
            self._refresh()
            self._delay_fps(60)
        self.close()

    def __del__(self):
        self.close()

    def _delay_fps(self, fps: int):
        """
        Delay to control fps without frame skipping. Never skip frames.

        :param fps: the desire fps
        """
        nanotime = 1000000000 // fps
        if self._last_fps_time == 0:
            self._last_fps_time = time.perf_counter_ns()
        self.update()
        tt = time.perf_counter_ns()
        while tt - self._last_fps_time < nanotime:
            tt = time.perf_counter_ns()
        self._last_fps_time = tt

    def run(self, f):
        """
        Run turtle code.

        :param f: the callable object(function or method) to run
        """
        work_thread = threading.Thread(target=f)
        work_thread.start()
