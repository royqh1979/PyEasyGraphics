from PyQt5 import QtCore, QtWidgets, QtGui
from easygraphics import Image
import time

__all__ = ['ProcessingWidget']


class ProcessingWidget(QtWidgets.QWidget):
    def __init__(self, *args, init=True, **kwargs):
        super().__init__(*args, **kwargs)
        if init:
            self.init()

    def init(self):
        self._fps = 60
        self._image: Image = None
        self.setup()
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._on_update_frame)
        self._frame_duration = 1000 // self._fps
        self._is_looping = True
        self._schedule_next_frame(self._frame_duration)
        self.mouse_pressed = False
        self.mouse_button = QtCore.Qt.NoButton
        self.mouse_x = 0
        self.mouse_y = 0
        self.prev_mouse_x = 0
        self.prev_mouse_y = 0

    def set_size(self, width: int, height: int):
        if self._image is not None:
            raise RuntimeError("set_size and fullscreen() can run only once!")
        self._image = Image.create(width, height)
        self.setFixedWidth(width)
        self.setFixedHeight(height)

    def full_screen(self):
        desktop = QtWidgets.QApplication.desktop()
        rect = desktop.screenGeometry()
        self.set_size(rect.width(), rect.height())

    def setup(self):
        self.set_size(800, 600)

    def draw(self):
        raise RuntimeError("Must overload draw() method!")

    def noloop(self):
        self._is_looping = False

    def loop(self):
        self._is_looping = True
        self.redraw()
        self._schedule_next_frame(self._frame_duration)

    def _schedule_next_frame(self, duration):
        self._timer.singleShot(duration, self._on_update_frame)

    def paintEvent(self, e: QtGui.QPaintEvent):
        self._image.draw_to_device(self)

    def redraw(self):
        pos = self.mapFromGlobal(QtGui.QCursor.pos())
        self.mouse_x = pos.x()
        self.mouse_y = pos.y()
        self.get_canvas().save_settings()
        self.draw()
        self.update()
        self.get_canvas().restore_settings()
        self.prev_mouse_x = self.mouse_x
        self.prev_mouse_y = self.mouse_y

    def _on_update_frame(self):
        start_time = time.perf_counter_ns()
        self.redraw()
        if self._is_looping:
            end_time = time.perf_counter_ns()
            time_used = (end_time - start_time) // 1000000
            duration = self._frame_duration - time_used % self._frame_duration
            self._schedule_next_frame(duration)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        self.on_mouse_pressed()
        self.mouse_pressed = True
        self.mouse_button = e.button()

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        self.on_mouse_released()
        self.mouse_pressed = False
        self.on_mouse_clicked()
        self.mouse_button = QtCore.Qt.NoButton

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        if self.mouse_pressed:
            self.on_mouse_dragged()

    def wheelEvent(self, e: QtGui.QWheelEvent):
        self.on_mouse_wheel(e)

    def on_mouse_clicked(self):
        pass

    def on_mouse_pressed(self):
        pass

    def on_mouse_released(self):
        pass

    def on_mouse_dragged(self):
        pass

    def on_mouse_wheel(self, e: QtGui.QWheelEvent):
        pass

    def __del__(self):
        self.close()

    def get_canvas(self) -> Image:
        return self._image
