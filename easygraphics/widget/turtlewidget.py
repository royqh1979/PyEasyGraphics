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
        self._image.set_background_color("white")
        self._image.clear()
        self._canvas = Image.create(width, height)
        self.setFixedWidth(self._image.get_width())
        self.setFixedHeight(self._image.get_height())
        self._world = TurtleWorld(self._image)
        self._turtle = self._world.create_turtle()
        self._is_running = True
        self._last_fps_time = 0

    def closeEvent(self, e: QtGui.QCloseEvent):
        self.close()
        super().closeEvent(e)

    def close(self):
        """
        Close the widget.

        """
        self._is_running = False
        self._world.close()
        self._image.close()
        super().close()

    def hideEvent(self, QHideEvent):
        self._is_running = False

    def showEvent(self, QShowEvent):
        self._start_refresh_loop()

    def is_run(self):
        """
        Test if the turtle world is running.

        :return: True if is running, False if not.
        """
        return self._is_running

    def getWorld(self) -> TurtleWorld:
        """
        Get the underlying turtle world.

        :return: the turtle world
        """
        return self._world

    def getTurtle(self) -> Turtle:
        """
        Get the turtle.

        :return: the turtle
        """
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
        if tt - self._last_fps_time < nanotime:
            QtCore.QThread.usleep((self._last_fps_time + nanotime - tt) // 1000)
        self._last_fps_time = time.perf_counter_ns()

    def run_animated_code(self, f):
        """
        Run turtle code.

        :param f: the callable object(function or method) to run
         """

        def nf():
            self._world._immediate = False
            f()
            self._world._immediate = True

        work_thread = threading.Thread(target=nf)
        work_thread.start()

