from typing import List

from .processingwidget import ProcessingWidget
from easygraphics import Image, color_rgb, color_cmyk, color_hsv, rgb, to_alpha, pol2cart, cart2pol
from easygraphics.consts import *
from PyQt5 import QtCore, QtWidgets, QtGui

_widget = None
_app = None
mouse_x = 0
mouse_y = 0
prev_mouse_x = 0
prev_mouse_y = 0
mouse_pressed = False

__all__ = [
    # consts
    'Color', 'FillStyle', 'LineStyle', 'RenderMode', 'CompositionMode', 'TextFlags',
    'MouseMessageType', 'FillRule', 'ShapeMode', 'VertexType',
    # virtual functions
    # control functions
    'redraw', 'loop', 'noloop', 'run_app',
    #  setting functions #
    'set_line_style', 'get_line_style', 'set_line_width', 'get_line_width',
    'get_color', 'set_color', 'get_fill_color', 'set_fill_color', 'get_fill_style', 'set_fill_style',
    'get_background_color', 'set_background_color', 'set_font', 'get_font', 'set_font_size', 'get_font_size',
    'set_composition_mode', 'get_composition_mode', 'get_drawing_x', 'get_drawing_y', 'set_view_port',
    'reset_view_port', 'set_origin', 'get_fill_rule', 'set_fill_rule',
    'get_drawing_pos', 'set_clip_rect', 'set_clipping',
    'set_window', 'reset_window', 'translate', 'rotate', 'scale', 'skew', 'shear', 'set_flip_y',
    'reflect', 'flip', 'mirror', 'reset_transform', 'save_settings', 'restore_settings',
    'get_width', 'get_height', 'get_write_mode', 'set_write_mode', 'get_transform', 'set_transform',
    'push_transform', 'pop_transform', 'set_size', 'full_screen',
    'set_rect_mode', 'get_rect_mode', 'set_ellipse_mode', 'get_ellipse_mode',
    # drawing functions #
    'draw_point', 'put_pixel', 'get_pixel', 'line', 'draw_line', 'move_to', 'move_rel', 'line_to', 'line_rel',
    'ellipse', 'draw_ellipse', 'fill_ellipse',
    'arc', 'draw_arc', 'pie', 'draw_pie', 'fill_pie', 'chord', 'draw_chord', 'fill_chord',
    'bezier', 'draw_bezier', 'lines', 'draw_lines', 'poly_line', 'draw_poly_line', 'polygon', 'draw_polygon',
    'fill_polygon', 'rect', 'draw_rect', 'fill_rect', 'rounded_rect', 'draw_rounded_rect', 'fill_rounded_rect',
    'flood_fill', 'draw_image', 'clear', 'clear_view_port',
    'quadratic', 'draw_quadratic', 'begin_shape', 'end_shape', 'vertex', 'bezier_vertex', 'quadratic_vertex',
    # text functions #
    'draw_text', 'draw_rect_text', 'text_width', 'text_height',
    # time control functions#
    'delay',
    # keyboard and mouse functions #
    'mouse_x', 'mouse_y', 'mouse_pressed', 'on_mouse_wheel', 'on_mouse_dragged',
    'on_mouse_released', 'on_mouse_pressed', 'on_mouse_clicked', 'prev_mouse_y', 'prev_mouse_x',
    # utility functions #
    'color_rgb', 'color_cmyk', 'color_hsv', 'rgb', 'to_alpha', 'pol2cart', 'cart2pol',
    # 'GraphWin',
    'Image'
]


def delay(milliseconds: int):
    QtCore.QThread.msleep(milliseconds)


def setup():
    set_size(400, 300)


def draw():
    raise RuntimeError("Must implement draw() function!")


def set_line_style(line_style):
    _widget.get_canvas().set_line_style(line_style)


def get_line_style() -> int:
    return _widget.get_canvas().get_line_style()


def set_line_width(width: float):
    _widget.get_canvas().set_line_width(width)


def get_line_width() -> float:
    return _widget.get_canvas().get_line_width()


def get_color() -> QtGui.QColor:
    return _widget.get_canvas().get_color()


def set_color(color):
    _widget.get_canvas().set_color(color)


def get_fill_color() -> QtGui.QColor:
    return _widget.get_canvas().get_fill_color()


def set_fill_color(color):
    _widget.get_canvas().set_fill_color(color)


def get_fill_style() -> int:
    return _widget.get_canvas().get_fill_style()


def set_fill_style(style):
    _widget.get_canvas().set_fill_style(style)


def get_drawing_x() -> float:
    return _widget.get_canvas().get_x()


def get_drawing_y() -> float:
    return _widget.get_canvas().get_y()


def get_drawing_pos() -> (float, float):
    return _widget.get_canvas().get_x(), _widget.get_canvas().get_y()


def get_background_color() -> QtGui.QColor:
    return _widget.get_canvas().get_background_color()


def set_background_color(color):
    _widget.get_canvas().set_background_color(color)


def set_font(font: QtGui.QFont):
    _widget.get_canvas().set_font(font)


def get_font() -> QtGui.QFont:
    return _widget.get_canvas().get_font()


def set_font_size(size: int):
    _widget.get_canvas().set_font_size(size)


def get_font_size() -> int:
    return _widget.get_canvas().get_font_size()


def set_composition_mode(mode):
    _widget.get_canvas().set_composition_mode(mode)


set_write_mode = set_composition_mode


def get_composition_mode() -> int:
    return _widget.get_canvas().get_composition_mode()


get_write_mode = get_composition_mode


def set_view_port(left: int, top: int, right: int, bottom: int, clip: bool = True):
    _widget.get_canvas().set_view_port(left, top, right, bottom, clip)


def reset_view_port():
    _widget.get_canvas().reset_view_port()


def get_fill_rule() -> int:
    return _widget.get_canvas().get_fill_rule()


def set_fill_rule(rule):
    _widget.get_canvas().set_fill_rule(rule)


def set_clip_rect(left: int, top: int, right: int, bottom: int):
    _widget.get_canvas().set_clip_rect(left, top, right, bottom)


def set_clipping(clipping: bool):
    _widget.get_canvas().set_clipping(clipping)


def set_window(left: int, top: int, width: int, height: int):
    _widget.get_canvas().set_window(left, top, width, height)


def reset_window():
    _widget.get_canvas().reset_window()


def translate(offset_x: float, offset_y: float):
    _widget.get_canvas().translate(offset_x, offset_y)


set_origin = translate


def rotate(degree: float, x: float = 0, y: float = 0):
    _widget.get_canvas().rotate(degree, x, y)


def scale(sx: float, sy: float):
    _widget.get_canvas().scale(sx, sy)


def skew(sh: float, sv: float, x: float = 0, y: float = 0):
    _widget.get_canvas().skew(sh, sv, x, y)


def shear(sh: float, sv: float, x: float = 0, y: float = 0):
    _widget.get_canvas().shear(sh, sv, x, y)


def set_flip_y(flip_y: bool) -> None:
    return _widget.get_canvas().set_flip_y(flip_y)


def reflect(x: float, y: float, x1: float = 0, y1: float = 0):
    _widget.get_canvas().reflect(x, y, x1, y1)


def flip(x: float, y: float, x1: float = 0, y1: float = 0):
    _widget.get_canvas().flip(x, y, x1, y1)


def mirror(x: float, y: float, x1: float = 0, y1: float = 0):
    _widget.get_canvas().mirror(x, y, x1, y1)


def reset_transform():
    _widget.get_canvas().reset_transform()


def save_settings():
    _widget.get_canvas().save_settings()


def restore_settings():
    _widget.get_canvas().restore_settings()


def get_width() -> int:
    return _widget.get_canvas().get_width()


def get_height() -> int:
    return _widget.get_canvas().get_height()


def get_transform() -> QtGui.QTransform:
    return _widget.get_canvas().get_transform()


def set_transform(transform: QtGui.QTransform):
    _widget.get_canvas().set_transform(transform)


def push_transform():
    _widget.get_canvas().push_transform()


def pop_transform():
    _widget.get_canvas().pop_transform()


def draw_point(x: float, y: float):
    _widget.get_canvas().draw_point(x, y)


def put_pixel(x: int, y: int, color):
    _widget.get_canvas().put_pixel(x, y, color)


def get_pixel(x: int, y: int) -> QtGui.QColor:
    return _widget.get_canvas().get_pixel(x, y)


def line(x1, y1, x2, y2):
    _widget.get_canvas().line(x1, y1, x2, y2)


def draw_line(x1, y1, x2, y2):
    _widget.get_canvas().draw_line(x1, y1, x2, y2)


def move_to(x: float, y: float):
    _widget.get_canvas().move_to(x, y)


def move_rel(dx: float, dy: float):
    _widget.get_canvas().move_rel(dx, dy)


def line_to(x: float, y: float):
    _widget.get_canvas().line_to(x, y)


def line_rel(dx: float, dy: float):
    _widget.get_canvas().line_rel(dx, dy)


def ellipse(x, y, radius_x, radius_y):
    _widget.get_canvas().ellipse(x, y, radius_x, radius_y)


def draw_ellipse(x, y, radius_x, radius_y):
    _widget.get_canvas().draw_ellipse(x, y, radius_x, radius_y)


def fill_ellipse(x, y, radius_x, radius_y):
    _widget.get_canvas().fill_ellipse(x, y, radius_x, radius_y)


def arc(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
    _widget.get_canvas().arc(x, y, start_angle, end_angle, radius_x, radius_y)


def draw_arc(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
             ):
    _widget.get_canvas().draw_arc(x, y, start_angle, end_angle, radius_x, radius_y)


def pie(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
        ):
    _widget.get_canvas().pie(x, y, start_angle, end_angle, radius_x, radius_y)


def draw_pie(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
             ):
    _widget.get_canvas().draw_pie(x, y, start_angle, end_angle, radius_x, radius_y)


def fill_pie(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
             ):
    _widget.get_canvas().fill_pie(x, y, start_angle, end_angle, radius_x, radius_y)


def chord(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
          ):
    _widget.get_canvas().chord(x, y, start_angle, end_angle, radius_x, radius_y)


def draw_chord(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
               ):
    _widget.get_canvas().draw_chord(x, y, start_angle, end_angle, radius_x, radius_y)


def fill_chord(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
               ):
    _widget.get_canvas().fill_chord(x, y, start_angle, end_angle, radius_x, radius_y)


def begin_shape(type=VertexType.POLY_LINE):
    _widget.get_canvas().begin_shape(type)


def end_shape(close=False):
    _widget.get_canvas().end_shape(close)


def vertex(x: float, y: float):
    _widget.get_canvas().vertex(x, y)


def bezier_vertex(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
    _widget.get_canvas().bezier_vertex(x1, y1, x2, y2, x3, y3)


def quadratic_vertex(x1: float, y1: float, x2: float, y2: float):
    _widget.get_canvas().quadratic_vertex(x1, y1, x2, y2)


def bezier(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
    _widget.get_canvas().bezier(x0, y0, x1, y1, x2, y2, x3, y3)


def draw_bezier(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
    _widget.get_canvas().draw_bezier(x0, y0, x1, y1, x2, y2, x3, y3)


def quadratic(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float):
    _widget.get_canvas().bezier(x0, y0, x1, y1, x2, y2)


def draw_quadratic(x0: float, y0: float, x1: float, y1: float, x2: float, y2: float):
    _widget.get_canvas().draw_bezier(x0, y0, x1, y1, x2, y2)


def lines(points: List[float]):
    _widget.get_canvas().lines(points)


def draw_lines(points: List[float]):
    _widget.get_canvas().draw_lines(points)


def poly_line(end_points: List[float]):
    _widget.get_canvas().poly_line(end_points)


def draw_poly_line(end_points: List[float]):
    _widget.get_canvas().draw_poly_line(end_points)


def polygon(vertices: List[float]):
    _widget.get_canvas().polygon(vertices)


def draw_polygon(vertices: List[float]):
    _widget.get_canvas().draw_polygon(vertices)


def fill_polygon(vertices: List[float]):
    _widget.get_canvas().fill_polygon(vertices)


def rect(left: float, top: float, right: float, bottom: float):
    _widget.get_canvas().rect(left, top, right, bottom)


def draw_rect(left: float, top: float, right: float, bottom: float):
    _widget.get_canvas().draw_rect(left, top, right, bottom)


def fill_rect(left: float, top: float, right: float, bottom: float):
    _widget.get_canvas().fill_rect(left, top, right, bottom)


def rounded_rect(left: float, top: float, right: float, bottom: float, round_x: float, round_y: float,
                 ):
    _widget.get_canvas().rounded_rect(left, top, right, bottom, round_x, round_y)


def draw_rounded_rect(left: float, top: float, right: float, bottom: float, round_x: float, round_y: float,
                      ):
    _widget.get_canvas().draw_rounded_rect(left, top, right, bottom, round_x, round_y)


def fill_rounded_rect(left: float, top: float, right: float, bottom: float, round_x: float, round_y: float,
                      ):
    _widget.get_canvas().fill_rounded_rect(left, top, right, bottom, round_x, round_y)


def flood_fill(x: int, y: int, border_color):
    _widget.get_canvas().flood_fill(x, y, border_color)


def draw_image(x: int, y: int, src_image: Image, src_x: int = 0, src_y: int = 0, src_width: int = -1,
               src_height: int = -1, with_background=True, composition_mode=None, ):
    _widget.get_canvas().draw_image(x, y, src_image, src_x, src_y, src_width, src_height, with_background,
                                    composition_mode, )


def clear_view_port():
    _widget.get_canvas().clear_view_port()


def clear():
    _widget.get_canvas().clear()


def fill_image(color):
    _widget.get_canvas().fill_image(color)


def draw_text(x, y, *args, sep=' '):
    _widget.get_canvas().draw_text(x, y, *args, sep)


def draw_rect_text(x: int, y: int, width: int, height: int, *args, flags=132, sep: str = ' '):
    _widget.get_canvas().draw_rect_text(x, y, width, height, *args, flags, sep)


def text_width(text: str) -> int:
    return _widget.get_canvas().text_width(text)


def text_height() -> int:
    return _widget.get_canvas().text_height()


def set_rect_mode(mode):
    _widget.get_canvas().set_rect_mode(mode)


def set_ellipse_mode(mode):
    _widget.get_canvas().set_ellipse_mode(mode)


def get_rect_mode():
    return _widget.get_canvas().get_rect_mode()


def get_ellipse_mode():
    return _widget.get_canvas().get_ellipse_mode()


# functions from Processing Widget

def set_size(width: int, height: int):
    _widget.set_size(width, height)


def full_screen():
    _widget.fullscreen()


def noloop():
    _widget.noloop()


def loop():
    _widget.loop()


def redraw():
    global mouse_x, mouse_y, prev_mouse_x, prev_mouse_y
    pos = _widget.mapFromGlobal(QtGui.QCursor.pos())
    mouse_x = pos.x()
    mouse_y = pos.y()
    _widget.redraw()
    prev_mouse_x = mouse_x
    prev_mouse_y = mouse_y


def get_canvas() -> Image:
    return _widget.get_canvas()


def run_app(_globals):
    global _app, _widget, setup, draw, on_mouse_clicked
    global on_mouse_pressed, on_mouse_released, on_mouse_dragged, on_mouse_wheel
    if 'setup' in _globals:
        setup = _globals['setup']
    if 'draw' in _globals:
        draw = _globals['draw']
    if 'on_mouse_clicked' in _globals:
        on_mouse_clicked = _globals['on_mouse_clicked']
    if 'on_mouse_pressed' in _globals:
        on_mouse_pressed = _globals['on_mouse_pressed']
    if 'on_mouse_released' in _globals:
        on_mouse_released = _globals['on_mouse_released']
    if 'on_mouse_dragged' in _globals:
        on_mouse_dragged = _globals['on_mouse_dragged']
    if 'on_mouse_wheel' in _globals:
        on_mouse_wheel = _globals['on_mouse_wheel']
    _app = QtWidgets.QApplication([])
    _widget = _Processing_Widget()
    _widget.start()
    _widget.show()
    _app.exec()
    _widget = None
    _app = None


# mouse functions #

def on_mouse_clicked():
    pass


def on_mouse_pressed():
    pass


def on_mouse_released():
    pass


def on_mouse_dragged():
    pass


def on_mouse_wheel(e: QtGui.QWheelEvent):
    pass


class _Processing_Widget(ProcessingWidget):
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
