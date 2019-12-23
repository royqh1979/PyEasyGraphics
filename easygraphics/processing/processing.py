from typing import Callable

from .processingwidget import ProcessingWidget
from easygraphics import *
from PyQt5 import QtWidgets, QtGui

_widget = None
_app = None
mouse_x = 0
# x coordinate of the mouse cursor
mouse_y = 0
# y coordinate of the mouse cursor
prev_mouse_x = 0
# x coordinate of the mouse cursor's last position
prev_mouse_y = 0
# y coordinate of the mouse cursor's last position
mouse_pressed = False
# if the mouse button is pressed

__all__ = [
    # register functions
    'register_setup','register_on_mouse_clicked','register_on_mouse_dragged',
    'register_on_mouse_pressed','register_on_mouse_released','register_on_mouse_wheel',
    # control functions
    'redraw', 'loop', 'noloop', 'run_app',
    'set_size', 'full_screen', 'draw', 'setup', 'set_frame_rate', 'get_frame_rate',
    # keyboard and mouse functions #
    'mouse_x', 'mouse_y', 'mouse_pressed', 'on_mouse_wheel', 'on_mouse_dragged',
    'on_mouse_released', 'on_mouse_pressed', 'on_mouse_clicked', 'prev_mouse_y', 'prev_mouse_x',
    'ProcessingWidget'
]


def setup():
    """
    Set up the processing context.

    You should redefine this function in your program.
    """
    set_size(400, 300)


def draw():
    """
    Draw an animation frame.

    You should redefine this function in your program.

    :return:
    """
    pass


# functions from Processing Widget

def set_size(width: int, height: int):
    """
    Open a canvas window with the specified size.

    :param width: width of the canvas
    :param height: height of the canvas
    """
    _widget.set_size(width, height)
    set_target(_widget.get_canvas())


def full_screen():
    """
    Open a full screen canvas.
    """
    _widget.fullscreen()
    set_target(_widget.get_canvas())


def noloop():
    """
    Stop looping.
    """
    _widget.noloop()


def loop():
    """
    Start looping.
    """
    _widget.loop()


def redraw():
    """
    Call draw() to draw a frame once.

    You must NOT redefine this function!
    """
    global mouse_x, mouse_y, prev_mouse_x, prev_mouse_y
    pos = _widget.mapFromGlobal(QtGui.QCursor.pos())
    mouse_x = pos.x()
    mouse_y = pos.y()
    _widget.redraw()
    prev_mouse_x = mouse_x
    prev_mouse_y = mouse_y


def get_canvas() -> Image:
    """
    Get the canvas image.

    :return: the canvas image
    """
    return _widget.get_canvas()


def get_frame_rate() -> int:
    """
    Get the animation frame rate (fps).

    :return: the frame rate
    """
    return _widget.get_frame_rate()


def set_frame_rate(fps: int):
    """
    Set the animation frame rate (fps).

    :param fps: the frame rate
    """
    _widget.set_frame_rate(fps)

def register_setup(setup_func:Callable):
    """
    Register the setup function
    :param setup_func: the setup function
    """
    global setup
    setup = setup_func

def register_on_mouse_clicked(func:Callable):
    """
    Register the on mouse clicked event handler
    :param func: the mouse clicked event handler
    """
    global on_mouse_clicked
    on_mouse_clicked = func

def register_on_mouse_pressed(func:Callable):
    """
    Register the on mouse pressed event handler
    :param func: the mouse pressed event handler
    """
    global on_mouse_pressed
    on_mouse_pressed = func

def register_on_mouse_released(func:Callable):
    """
    Register the on mouse released event handler
    :param func: the mouse released event handler
    """
    global on_mouse_released
    on_mouse_released = func

def register_on_mouse_dragged(func:Callable):
    """
    Register the on mouse dragged event handler
    :param func: the mouse dragged event handler
    """
    global on_mouse_dragged
    on_mouse_dragged = func

def register_on_mouse_wheel(func:Callable):
    """
    Register the on mouse wheel event handler
    :param func: the mouse wheel event handler
    """
    global on_mouse_wheel
    on_mouse_wheel = func

def run_app(_globals):
    """
    Run the processing app.

    :param _globals: the python globals dict.
    """
    global _app, _widget, setup, draw, on_mouse_clicked
    global on_mouse_pressed, on_mouse_released, on_mouse_dragged, on_mouse_wheel
    if 'setup' in _globals and callable(_globals['setup']):
        setup = _globals['setup']
    if draw not in _globals['draw'] or not callable(_globals['draw']):
        raise RuntimeError("Must implement draw() function!")
    else:
        draw = _globals['draw']
    if 'on_mouse_clicked' in _globals and callable(_globals['on_mouse_clicked']):
        on_mouse_clicked = _globals['on_mouse_clicked']
    if 'on_mouse_pressed' in _globals and callable(_globals['on_mouse_pressed']):
        on_mouse_pressed = _globals['on_mouse_pressed']
    if 'on_mouse_released' in _globals and callable(_globals['on_mouse_released']):
        on_mouse_released = _globals['on_mouse_released']
    if 'on_mouse_dragged' in _globals and callable(_globals['on_mouse_dragged']):
        on_mouse_dragged = _globals['on_mouse_dragged']
    if 'on_mouse_wheel' in _globals and callable(_globals['on_mouse_wheel']):
        on_mouse_wheel = _globals['on_mouse_wheel']
    _app = QtWidgets.QApplication([])
    _widget = _ProcessingWidget()
    _widget.start()
    _widget.show()
    _app.exec()
    _widget = None
    _app = None


# mouse functions #

def on_mouse_clicked():
    """
    The mouse click event handler.

    You can redefine this function to handle the mouse click event.
    """
    pass


def on_mouse_pressed():
    """
    The mouse press event handler.

    You can redefine this function to handle the mouse press event.
    """
    pass


def on_mouse_released():
    """
    The mouse release event handler.

    You can redefine this function to handle the mouse release event.
    """
    pass


def on_mouse_dragged():
    """
    The mouse drag event handler.

    You can redefine this function to handle the mouse drag event.
    """
    pass


def on_mouse_wheel(e: QtGui.QWheelEvent):
    """
    The mouse wheel event handler.

    You can redefine this function to handle the mouse wheel event.
    """
    pass


class _ProcessingWidget(ProcessingWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, auto_start=False, **kwargs)

    def setup(self):
        setup()

    def draw(self):
        draw()

    def on_mouse_clicked(self):
        on_mouse_clicked()

    def on_mouse_pressed(self):
        global mouse_pressed
        mouse_pressed = True
        on_mouse_pressed()

    def on_mouse_released(self):
        global mouse_pressed
        on_mouse_released()
        mouse_pressed = False

    def on_mouse_dragged(self):
        on_mouse_dragged()

    def on_mouse_wheel(self, e: QtGui.QWheelEvent):
        on_mouse_wheel(e)
