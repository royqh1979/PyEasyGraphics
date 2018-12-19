import threading
import sys
from typing import List
from functools import reduce

from PyQt5 import QtWidgets

from .consts import *
from .graphwin import GraphWin
from .image import Image
from .dialog import invoke_in_app_thread

if sys.version_info < (3, 6):
    raise OSError("Only Support Python 3.6 and above")

__all__ = [
    'Color', 'FillStyle', 'LineStyle', 'RenderMode', 'WriteMode',  # consts
    'GraphWin', 'Image',
    #  setting functions #
    'set_line_style', 'get_line_style', 'set_line_width', 'get_line_width',
    'get_color', 'set_color', 'get_fill_color', 'set_fill_color', 'get_fill_style', 'set_fill_style',
    'get_background_color', 'set_background_color', 'set_font', 'get_font', 'set_font_size', 'get_font_size',
    'set_write_mode', 'get_write_mode', 'get_x', 'get_y', 'set_view_port', 'reset_view_port', 'set_origin',
    'set_render_mode', 'get_render_mode', 'get_drawing_pos', 'set_clip_rect', 'reset_clip_rect',
    'set_window', 'reset_window', 'translate', 'rotate', 'scale', 'reset_transform',
    # drawing functions #
    'draw_point', 'put_pixel', 'get_pixel', 'line', 'draw_line', 'move_to', 'move_rel', 'line_to', 'line_rel',
    'circle', 'draw_circle', 'fill_circle', 'ellipse', 'draw_ellipse', 'fill_ellipse',
    'arc', 'draw_arc', 'pie', 'draw_pie', 'fill_pie', 'chord', 'draw_chord', 'fill_chord',
    'bezier', 'draw_bezier', 'lines', 'draw_lines', 'poly_line', 'draw_poly_line', 'polygon', 'draw_polygon',
    'fill_polygon',
    'rect', 'draw_rect', 'fill_rect', 'rounded_rect', 'draw_rounded_rect', 'fill_rounded_rect', 'flood_fill',
    'draw_image',
    'clear_device', 'clear_view_port',
    # text functions #
    'draw_text', 'draw_rect_text', 'text_width', 'text_height',
    # image functions #
    'set_target', 'get_target', 'create_image',
    # time control functions#
    'pause', 'delay', 'delay_fps', 'delay_jfps', 'is_run',
    # keyboard and mouse functions #
    'kb_msg', 'kb_hit', 'mouse_msg', 'get_key', 'get_char', 'get_mouse',
    # init and close graph window #
    'init_graph', 'close_graph', 'set_caption',
    # utility functions #
    'rgb'
]


#  settings

def set_line_style(line_style, image: Image = None):
    """
    set line style of the specified image

    The line style will be used when drawing lines and shape outlines.
    Possible value is one of the consts defined in LineStyle.

    :param line_style: line style
    :param image: the target image whose line style is to be set. None means it is the default target image
        (see set_target() and get_target())
    """
    image, on_screen = _check_on_screen(image)
    image.set_line_style(line_style)


def get_line_style(image: Image = None):
    """
    get line style of the specified image

    The line style will be used when drawing lines or shape outlines.

    :param image: the target image whose line style is to be gotten. None means it is the target image
        (see set_target() and get_target())
    :return: line style used by the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_line_style()


def set_line_width(width: float, image: Image = None):
    """
    set line width (thickness) of the specified image

    It will be used when drawing lines or shape outlines

    :param width: line width (line thickness)
    :param image: the target image whose line width is to be set. None means it is the target image
        (see set_target() and get_target())
    """
    image, on_screen = _check_on_screen(image)
    image.set_line_width(width)


def get_line_width(image: Image = None) -> float:
    """
    get line width (thinkness) of the specified image

    It will be used when drawing lines or shape outlines

    :param image: the target image whose line width is to be gotten. None means it is the target image
        (see set_target() and get_target())
    :return: line width (line thickness) of the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_line_width()


def get_color(image: Image = None):
    """
    get the foreground (drawing) color of the specified image

    it will be used when drawing lines or shape outlines

    :param image: the target image whose foreground color is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: foreground color of the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_color()


def set_color(color, image: Image = None):
    """
    set the foreground (drawing) color of the specified image.

    it will be used when drawing lines or shape outlines.

    the possible color could be consts defined in Color class,
    or the color created by rgb() function,
    or PyQt5's QColor , QGradient object or Qt.GlobalColor consts (see the pyqt reference).

    :param color:  the foreground color
    :param image: the target image whose foreground color is to be set. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_color(color)


def get_fill_color(image: Image = None):
    """
    get the fill color of the specified image

    it will be used when drawing and fill shapes.

    :param image: the target image whose fill color is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: fill color of the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_fill_color()


def set_fill_color(color, image: Image = None):
    """
    set the fill (drawing) color of the specified image

    it will be used when drawing and fill shapes.

    the possible color could be consts defined in Color class,
    or the color created by rgb() function,
    or PyQt5's QColor , QGradient object or Qt.GlobalColor consts (see the pyqt reference).

    :param color:  the fill color
    :param image: the target image whose fill color is to be set. None means it is the target image
         (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_fill_color(color)


def get_fill_style(image: Image = None):
    """
    get fill style of the specified image

    it will be used when drawing and fill shapes.

    :param image: the target image whose fill style is to be gotten. None means it is the target image
         (see set_target() and get_target()).
    :return: fill style of the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_fill_style()


def set_fill_style(style, image: Image = None):
    """
     set fill style of the specified image

    it will be used when drawing and fill shapes.
    Valid values are the consts defined in FillStyle

    :param style: fill style
    :param image: the target image whose fill style is to be set. None means it is the target image
         (see set_target() and get_target()).
    :return:
    """
    image, on_screen = _check_on_screen(image)
    image.set_fill_style(style)


def get_background_color(image: Image = None):
    """
    get the background color of the image

    it will be used when the image is cleared. (see clear_device())

    :param image: the target image whose background color is to be gotten. None means it is the target image
         (see set_target() and get_target()).
    :return: background color of the specified image
    """

    image, on_screen = _check_on_screen(image)
    return image.get_background_color()


def set_background_color(color, image: Image = None):
    """
    set the background  color of the image

    it will be used when the image is cleared. (see clear_device())

    the possible color could be consts defined in Color class,
    or the color created by rgb() function,
    or PyQt5's QColor , QGradient object or Qt.GlobalColor consts (see the pyqt reference).

    :param color:  the background color
    :param image: the target image whose background color is to be set. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_background_color(color)


def set_font(font: QtGui.QFont, image: Image = None):
    """
    set font of the specified image

    :param font: the font will be used
    :param image: the target image whose font is to be set. None means it is the target image
         (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_font(font)


def get_font(image: Image = None) -> QtGui.QFont:
    """
    get font of the specified image

    :param image: the target image whose font is to be gotten. None means it is the target image
         (see set_target() and get_target()).
    :return: the font used by the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_font()


def set_write_mode(mode, image: Image = None):
    """
    set write mode of the specified image

    When drawing ,the wrtie mode will decide how the result pixel color will be computed
     (using source color and color of the destination)

    source color is the color of the pen/brush.

    destination color is the color of the pixel will be painted on.

    the result color will be computed by bitwise operations

    possibly modes are consts defined in the WriteMode:

    * WriteMode.R2_COPYPEN （The default mode) just use the source color
    * WriteMOde.R2_MASKNOTPEN   （not source color) and (destination color)
    * WriteMOde.R2_MASKPEN   （source color ) and (destination color)
    * WriteMOde.R2_MASKPENNOT   (source color) and (not destination color)
    * WriteMOde.R2_MERGENOTPEN   (not source color) or (destination color)
    * WriteMOde.R2_MERGEPEN   (source color) or (destination color)
    * WriteMOde.R2_MERGEPENNOT   (source color) or (not destination color)
    * WriteMOde.R2_NOP   just use the destination color (nothing really painted)
    * WriteMOde.R2_NOT   (not desination color)
    * WriteMOde.R2_NOTCOPYPEN   (not source color)
    * WriteMOde.R2_NOTMASKPEN   (not source) or (not destination)
    * WriteMOde.R2_NOTMERGEPEN   (not source) and (not destination)
    * WriteMOde.R2_NOTXORPEN   (not source) xor (destination)
    * WriteMOde.R2_XORPEN   (source) xor (destination)

    :param mode: write mode
    :param image: the target image whose write mode is to be set. None means it is the target image
         (see set_target() and get_target()).

    """
    image, on_screen = _check_on_screen(image)
    image.set_write_mode(mode)


def get_write_mode(image: Image = None):
    """
    get write mode of the specified image

    When drawing ,the wrtie mode will decide how the result pixel color will be computed
     (using source color and color of the destination)

    :param image: the target image whose write mode is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: write mode
    """
    image, on_screen = _check_on_screen(image)
    return image.get_write_mode()


def set_font_size(size: int, image: Image = None):
    """
    set font size of the specified image

    :param size: font size of the specified image
    :param image: the target image whose write mode is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_font_size(size)


def get_font_size(image: Image = None) -> int:
    """
    get font size of the specified image

    :param image: the target image whose write mode is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: font size of the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_font_size()


def get_x(image: Image = None) -> float:
    """
    get the x coordinate value of the current drawing position (x,y)

    some drawing functions will use the current pos to draw.(see line_to(),line_rel(),move_to(),move_rel())

    :param image: the target image whose drawing pos is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: the x coordinate value of the current drawing position
    """
    image, on_screen = _check_on_screen(image)
    return image.get_x()


def get_y(image: Image = None) -> float:
    """
    get the y coordinate value of the current drawing position (x,y)

    some drawing functions will use the current pos to draw.(see line_to(),line_rel(),move_to(),move_rel())

    :param image: the target image whose drawing pos is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: the y coordinate value of the current drawing position
    """
    image, on_screen = _check_on_screen(image)
    return image.get_y()


def get_drawing_pos(image: Image = None) -> (float, float):
    """
    get the current drawing position (x,y)

    some drawing functions will use the current pos to draw.(see line_to(),line_rel(),move_to(),move_rel())

    :param image: the target image whose drawing pos is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return:  the current drawing position (x,y)
    """
    image, on_screen = _check_on_screen(image)
    return image.get_x(), image.get_y()


def set_view_port(left: int, top: int, right: int, bottom: int, image: Image = None):
    """
    set the view port of the the specified image

    View port is the drawing zone on the image.

    The drawing outside the view port is not clipped. If you want to clip the drawing ,use set_clip_rect()

    **if view port and "logical window" don't have the same width and height,
    drawing will get zoomed.** So set_window() is often used with the set_view_port

    >>>from easygraphics import *
    >>>init_graph(800,600)
    >>>draw_rect(100,100,300,300)
    >>>set_view_port(100,100,300,300)
    >>>set_window(0,0,200,200)
    >>>circle(100,100,50)
    >>>circle(100,100,100)
    >>>circle(100,100,120)
    >>>pause()
    >>>close_graph()

    :param left: left of the view port rectangle
    :param top: top of the view port rectangle
    :param right: right of the view port rectangle
    :param bottom: bottom of the view port rectangle
    :param image: the target image whose view port is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_view_port(left, top, right, bottom)


def reset_view_port(image: Image = None):
    """
    reset the view port to the whole image

    :param image: the target image whose view port is to be removed. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.reset_view_port()


def set_clip_rect(left: int, top: int, right: int, bottom: int, image: Image = None):
    """
    set
    set the clip rect
    :param left:
    :param top:
    :param right:
    :param bottom:
    :param image:
    :return:
    """
    image, on_screen = _check_on_screen(image)
    image.set_clip_rect(left, top, right, bottom)


def reset_clip_rect(image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.reset_clip_rect()


def set_window(left: int, top: int, right: int, bottom: int, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.set_window(left, top, right, bottom)


def reset_window(image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.reset_window()


def set_origin(x: float, y: float, image: Image = None):
    """
    set the drawing systems' origin(0,0) to (x,y)

    the default origin is on left-top of the specified image

    :param x: x coordinate value the new origin
    :param y: y coordinate value the new origin
    :param image: the target image whose origin is to be removed. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.translate(x, y)


def translate(x: float, y: float, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.translate(x, y)


def rotate(degree: float, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.rotate(degree)


def scale(sx: float, sy: float, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.scale(sx, sy)


def reset_transform(image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.reset_transform()


def set_render_mode(mode: int):
    """
    set render mode of the graphics window

    this mode will control how the graphics window is updated.

    possible values:

    * RenderMode.RENDER_AUTO   (default) update the window immediately after every drawing
    * RenderMode.MANUAL   only update the window after pause()/delay()/delay_fps()/delay_jfps() is called.

    RenderMode.MANUAL is used for animations

    :param mode: render mode
    """
    _check_app_run()
    _win.set_immediate(mode == RenderMode.RENDER_AUTO)


def get_render_mode():
    """
    set render mode of the graphics window

    this mode will control how the graphics window is updated.
    see **set_render_mode()**

    :return: render mode
    """
    _check_app_run()
    if _win.is_immediate():
        return RenderMode.RENDER_AUTO
    else:
        return RenderMode.RENDER_MANUAL


# drawings

def draw_point(x: float, y: float, image: Image = None):
    """
    draw a point at (x,y) on the specified image

    :param x: x coordinate value of the drawing point
    :param y: y coordinate value of the drawing point
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_point(x, y)
    if on_screen:
        _win.invalid()


def put_pixel(x: int, y: int, color, image: Image = None):
    """
    set a pixel's color on the specified image

    :param x: x coordinate value of the pixel
    :param y: y coordinate value of the pixel
    :param color: the color
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.put_pixel(x, y, color)
    if on_screen:
        _win.invalid()


def get_pixel(x: int, y: int, image: Image = None) -> QtGui.QColor:
    """
    get a pixel's color on the specified image

    :param x: x coordinate value of the pixel
    :param y: y coordinate value of the pixel
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    :return: color of the pixel
    """
    image, on_screen = _check_on_screen(image)
    return image.get_pixel(x, y)


def line(x1: float, y1: float, x2: float, y2: float, image: Image = None):
    """
    Draw a line from (x1,y1) to (x2,y2) on the specified image

    it's the same with draw_line()

    :param x1: x coordinate value of the start point
    :param y1: y coordinate value of the start point
    :param x2: x coordinate value of the end point
    :param y2: y coordinate value of the start point
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.line(x1, y1, x2, y2)
    if on_screen:
        _win.invalid()


def draw_line(x1, y1, x2, y2, image: Image = None):
    """
    Draw a line from (x1,y1) to (x2,y2) on the specified image

    it's the same with line()

    :param x1: x coordinate value of the start point
    :param y1: y coordinate value of the start point
    :param x2: x coordinate value of the end point
    :param y2: y coordinate value of the start point
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    line(x1, y1, x2, y2, image)


def move_to(x: float, y: float, image: Image = None):
    """
    set the drawing position to (x,y)

    the drawing position is used by line_to(), line_rel() and move_rel()

    :param x: x coordinate value of the new drawing position
    :param y: y coordinate value of the new drawing position
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.move_to(x, y)


def move_rel(dx: float, dy: float, image: Image = None):
    """
    move the drawing position by (dx,dy)

    if the old position is (x,y), then the new position will be (x+dx,y+dy)

    the drawing position is used by line_to(), line_rel()

    :param dx: x coordinate offset of the new drawing position
    :param dy: y coordinate offset of the new drawing position
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.move_rel(dx, dy)


def line_to(x: float, y: float, image: Image = None):
    """
    draw a line from the current drawing position to (x,y), then set the drawing position is set to (x,y)

    :param x: x coordinate value of the new drawing position
    :param y: y coordinate value of the new drawing position
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.line_to(x, y)
    if on_screen:
        _win.invalid()


def line_rel(dx: float, dy: float, image: Image = None):
    """
     draw a line from the current drawing position (x,y) to (x+dx,y+dy), \
     then set the drawing position is set to (x+d,y+dy)

    :param dx: x coordinate offset of the new drawing position
    :param dy: y coordinate offset of the new drawing position
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.line_rel(dx, dy)
    if on_screen:
        _win.invalid()


def circle(x: float, y: float, r: float, image: Image = None):
    """
    draw a circle outline centered at (x,y) with radius r

    the circle is not filled

    :param x: x coordinate value of the circle's center
    :param y: y coordinate value of the circle's center
    :param r: radius of the circle
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.ellipse(x, y, r, r)
    if on_screen:
        _win.invalid()


def draw_circle(x: float, y: float, r: float, image: Image = None):
    """
    draw a circle centered at (x,y) with radius r

    the circle is filled and has outline

    :param x: x coordinate value of the circle's center
    :param y: y coordinate value of the circle's center
    :param r: radius of the circle
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_ellipse(x, y, r, r)
    if on_screen:
        _win.invalid()


def fill_circle(x: float, y: float, r: float, image: Image = None):
    """
    fill a circle centered at (x,y) with radius r

    the circle dosen't has outline

    :param x: x coordinate value of the circle's center
    :param y: y coordinate value of the circle's center
    :param r: radius of the circle
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.fill_ellipse(x, y, r, r)
    if on_screen:
        _win.invalid()


def ellipse(x, y, radius_x, radius_y, image: Image = None):
    """
    draw an ellipse outline centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y

    the ellipse is not filled

    :param x: x coordinate value of the ellipse's center
    :param y: y coordinate value of the ellipse's center
    :param radius_x: radius on x-axis of the ellipse
    :param radius_y: radius on y-axis of the ellipse
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.ellipse(x, y, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def draw_ellipse(x, y, radius_x, radius_y, image: Image = None):
    """
    draw an ellipse centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y

    the ellipse is filled and has outline

    :param x: x coordinate value of the ellipse's center
    :param y: y coordinate value of the ellipse's center
    :param radius_x: radius on x-axis of the ellipse
    :param radius_y: radius on y-axis of the ellipse
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_ellipse(x, y, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def fill_ellipse(x, y, radius_x, radius_y, image: Image = None):
    """
    fill an ellipse centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y

    the ellipse dosen't has outline

    :param x: x coordinate value of the ellipse's center
    :param y: y coordinate value of the ellipse's center
    :param radius_x: radius on x-axis of the ellipse
    :param radius_y: radius on y-axis of the ellipse
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.fill_ellipse(x, y, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def arc(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
        image: Image = None):
    """
    draw an elliptical arc from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse's center
    :param y: y coordinate value of the ellipse's center
    :param start_angle: start angle of the arc
    :param end_angle: end angle of the arc
    :param radius_x: radius on x-axis of the ellipse
    :param radius_y: radius on y-axis of the ellipse
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.arc(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def draw_arc(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
             image: Image = None):
    """
    draw an elliptical arc from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse's center
    :param y: y coordinate value of the ellipse's center
    :param start_angle: start angle of the arc
    :param end_angle: end angle of the arc
    :param radius_x: radius on x-axis of the ellipse
    :param radius_y: radius on y-axis of the ellipse
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    arc(x, y, start_angle, end_angle, radius_x, radius_y, image)


def pie(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
        image: Image = None):
    """
    draw an elliptical pie outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    the pie is not filled.

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse's center
    :param y: y coordinate value of the ellipse's center
    :param start_angle: start angle of the pie
    :param end_angle: end angle of the pie
    :param radius_x: radius on x-axis of the ellipse
    :param radius_y: radius on y-axis of the ellipse
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.pie(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def draw_pie(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
             image: Image = None):
    """
    draw an elliptical pie from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    the pie is filled and has outline.

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse's center
    :param y: y coordinate value of the ellipse's center
    :param start_angle: start angle of the pie
    :param end_angle: end angle of the pie
    :param radius_x: radius on x-axis of the ellipse
    :param radius_y: radius on y-axis of the ellipse
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_pie(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def fill_pie(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
             image: Image = None):
    """
    fill an elliptical pie from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    the pie dosen't have outline.

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse's center
    :param y: y coordinate value of the ellipse's center
    :param start_angle: start angle of the pie
    :param end_angle: end angle of the pie
    :param radius_x: radius on x-axis of the ellipse
    :param radius_y: radius on y-axis of the ellipse
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.fill_pie(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def chord(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
          image: Image = None):
    """
    draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    the chord is not filled.

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse's center
    :param y: y coordinate value of the ellipse's center
    :param start_angle: start angle of the chord
    :param end_angle: end angle of the chord
    :param radius_x: radius on x-axis of the ellipse
    :param radius_y: radius on y-axis of the ellipse
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.chord(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def draw_chord(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
               image: Image = None):
    """
    draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    the chord is filled and has outline

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse's center
    :param y: y coordinate value of the ellipse's center
    :param start_angle: start angle of the chord
    :param end_angle: end angle of the chord
    :param radius_x: radius on x-axis of the ellipse
    :param radius_y: radius on y-axis of the ellipse
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_chord(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def fill_chord(x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float,
               image: Image = None):
    """
    draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    the chord doesn't have outline.

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse's center
    :param y: y coordinate value of the ellipse's center
    :param start_angle: start angle of the chord
    :param end_angle: end angle of the chord
    :param radius_x: radius on x-axis of the ellipse
    :param radius_y: radius on y-axis of the ellipse
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.fill_chord(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def bezier(poly_points: List[float], image: Image = None):
    """
    draw a bezier curve

    poly_points is a 2D point list. Each point has 2 coordinate values in the list. \
    So if you have 4 points (x0,y0),(x1,y1),(x2,y2),(x3,y3), the list should be  \
    [x0,y0,x1,y1,x2,y2,x3,y3]

    :param poly_points: point list
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    draw_bezier(poly_points, image)


def draw_bezier(poly_points: List[float], image: Image = None):
    """
    draw a bezier curve

    poly_points is a 2D point list. Each point has 2 coordinate values in the list. \
    So if you have 4 points (x0,y0),(x1,y1),(x2,y2),(x3,y3), the list should be  \
    [x0,y0,x1,y1,x2,y2,x3,y3]

    :param poly_points: point list
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_bezier(poly_points)
    if on_screen:
        _win.invalid()


def lines(points: List[float], image: Image = None):
    draw_lines(points, image)


def draw_lines(points: List[float], image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_lines(points)
    if on_screen:
        _win.invalid()


def poly_line(points: List[float], image: Image = None):
    draw_poly_line(points, image)


def draw_poly_line(points: List[float], image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_poly_line(points)
    if on_screen:
        _win.invalid()


def polygon(points: List[float], image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.polygon(points)
    if on_screen:
        _win.invalid()


def draw_polygon(points: List[float], image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_polygon(points)
    if on_screen:
        _win.invalid()


def fill_polygon(points: List[float], image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.fill_polygon(points)
    if on_screen:
        _win.invalid()


def rect(left: float, top: float, right: float, bottom: float, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.rect(left, top, right, bottom)
    if on_screen:
        _win.invalid()


def draw_rect(left: float, top: float, right: float, bottom: float, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_rect(left, top, right, bottom)
    if on_screen:
        _win.invalid()


def fill_rect(left: float, top: float, right: float, bottom: float, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.fill_rect(left, top, right, bottom)
    if on_screen:
        _win.invalid()


def rounded_rect(left: float, top: float, right: float, bottom: float, round_x: float, round_y: float,
                 image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.rounded_rect(left, top, right, bottom, round_x, round_y)
    if on_screen:
        _win.invalid()


def draw_rounded_rect(left: float, top: float, right: float, bottom: float, round_x: float, round_y: float,
                      image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_rounded_rect(left, top, right, bottom, round_x, round_y)
    if on_screen:
        _win.invalid()


def fill_rounded_rect(left: float, top: float, right: float, bottom: float, round_x: float, round_y: float,
                      image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.fill_rounded_rect(left, top, right, bottom, round_x, round_y)
    if on_screen:
        _win.invalid()


def flood_fill(x: int, y: int, background_color, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.flood_fill(x, y, background_color)
    if on_screen:
        _win.invalid()


def draw_image(x: int, y: int, src_image, dst_image: Image = None):
    dst_image, on_screen = _check_on_screen(dst_image)
    dst_image.draw_image(x, y, src_image)
    if on_screen:
        _win.invalid()


def clear_device(image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.clear()
    if on_screen:
        _win.invalid()


def clear_view_port(image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.clear_view_port()
    if on_screen:
        _win.invalid()


# text processing
def draw_text(x, y, *args, sep=' ', image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_text(x, y, *args, sep=sep)
    if on_screen:
        _win.invalid()


def draw_rect_text(x, y, w, h, *args, flags=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop, sep=' ', image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_rect_text(x, y, w, h, flags, *args, sep=sep)
    if on_screen:
        _win.invalid()


def text_width(s: str, image: Image = None):
    image, on_screen = _check_on_screen(image)
    return image.text_width(s)


def text_height(s: str, image: Image = None):
    image, on_screen = _check_on_screen(image)
    return image.text_height(s)


# image processing #

def set_target(image: Image = None):
    global _target_image
    _check_app_run()
    if image is None:
        _target_image = _win.get_canvas()
    else:
        _target_image = image


def get_target() -> Image:
    _check_app_run()
    return _target_image


def create_image(width, height) -> Image:
    image = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32_Premultiplied)
    image.fill(QtCore.Qt.transparent)
    return Image(image)


# utils

def rgb(red, green, blue):
    return QtGui.QColor(red, green, blue)


def _qpoint_to_point_list_fun(lst: List[float], p: QtCore.QPointF) -> List[float]:
    lst.append(p.x())
    lst.append(p.y())


def qpoints_to_point_list(qpoints: List[QtCore.QPointF]) -> List[float]:
    """
    convert QPointF list to point list

    :param qpoints:
    :return:
    """
    return reduce(_qpoint_to_point_list_fun, qpoints, [])


# time control #

def pause():
    """
    pause the grogram and wait for mouse clicking or keyboard hiting

    >>>from easygraphics import *
    >>>init_graph(800,600)
    >>>pause()
    >>>close_graph()
    """
    _win.real_update()
    _win.pause()


def is_run():
    return _is_run


def delay(milliseconds):
    _win.delay(milliseconds)


def delay_fps(fps):
    _win.delay_fps(fps)


def delay_jfps(fps):
    _win.delay_jfps(fps)


# mouse and keyboards #

def kb_hit():
    return _win.kb_hit()


def kb_msg():
    _check_app_run()
    return _win.kb_msg()


def mouse_msg():
    _check_app_run()
    return _win.mouse_msg()


def get_mouse():
    _check_app_run()
    return _win.get_mouse()


def get_char():
    _check_app_run()
    return _win.get_char()


def get_key():
    _check_app_run()
    return _win.get_key()


# init and close graphics #

def set_caption(title: str):
    _win.setWindowTitle(title)


def init_graph(width: int, height: int):
    """
    init the easygraphics system and show the graphics window

    :param width: width of the graphics window (in pixels)
    :param height:  height of the graphics window (in pixels)


    >>>from easygraphics import *
    >>>init_graph(800,600) #prepare and show a 800*600 window
    """
    global _start_event
    # prepare Events
    _start_event = threading.Event()
    _start_event.clear()
    # start GUI thread
    thread = threading.Thread(target=__graphics_thread_func, args=(width, height))
    thread.start()
    # wait GUI initiation finished
    _start_event.wait()


def close_graph():
    """
    close the graphics windows

    the program will exit too
    >>>from easygraphics import *
    >>>init_graph(800,600)
    >>>pause()
    >>>close_graph()
    """
    _app.exit(0)


def _check_app_run():
    if not is_run():
        raise RuntimeError("Easygrphics is not inited or has been closed! Run init_graph() first!")


def _check_on_screen(image: Image) -> (QtGui.QImage, bool):
    _check_app_run()
    if image is None:
        image = _target_image
    on_screen = image is _win.get_canvas()
    _validate_image(image)
    return image, on_screen


def _validate_image(image: Image):
    """ check if image is valid to draw on it"""
    if not isinstance(image, Image):
        raise ValueError("image parameter must be None or an instance return by getimage()!")
    if not isinstance(image.get_image(), QtGui.QImage):
        raise ValueError("don't have valid image")
    if not isinstance(image.get_pen(), QtGui.QPen):
        raise ValueError("don't have valid pen")
    if not isinstance(image.get_brush(), QtGui.QBrush):
        raise ValueError("don't have valid pen")


_is_run = False


def __graphics_thread_func(width: int, height: int):
    global _app, _win, _target_image, _is_run
    _app = QtWidgets.QApplication([])
    _app.setQuitOnLastWindowClosed(True)
    _win = GraphWin(width, height, _app)
    invoke_in_app_thread.init_invoke_in_app()
    _target_image = _win.get_canvas()
    _is_run = True
    # init finished, can draw now
    _start_event.set()
    _win.show()
    _app.exec_()
    _is_run = False
    invoke_in_app_thread.destroy_invoke_in_app()
    _win.close()
    _win = None
    _app.quit()
    _app = None
    in_shell = bool(getattr(sys, 'ps1', sys.flags.interactive))  # if in interactive mode (eg. in IPython shell)
    if not in_shell:
        sys.exit(0)


if __name__ == "__main__":
    pass
# init_graph(800, 600)
# set_color(Color.BLACK)
# circle(300,300,200)
# circle(400,400,100)
# pause()
# set_fill_color(Color.LIGHTBLUE)
# print("haha")
# flood_fill(300,300,Color.BLACK)
# print("lala")
# set_background_color(Color.RED)
# set_color(Color.RED)
# set_write_mode(WriteMode.R2_NOT)
# clear_device()
# line(100,100,400,400)
# set_line_style(LineStyle.DASH_DOT_DOT_LINE)
# set_view_port(0,0,300,300,True)
# line(100,400,400,100)
# pause()
# circle(250,250,200)
# pause()
# draw_circle(250, 250, 150)
# pause()
# clear_view_port()
# reset_view_port()
# set_fill_color(Color.RED)
# fill_circle(250,250,100)
# pause()
# clear_device()
# points=[]
# points.append(300)
# points.append(50)
# points.append(200)
# points.append(50)
# points.append(200)
# points.append(200)
# points.append(100)
# points.append(200)
# draw_bezier(points)
# draw_lines(points)
# pause()
# clear_device()
# draw_poly_line(points)
# pause()
# clear_device()
# draw_lines(points)
# pause()
# clear_device()
# set_background_color(Color.WHITE)
# set_color(Color.BLACK)
# set_fill_color(Color.LIGHTRED)
# set_write_mode(WriteMode.R2_COPYPEN)
# clear_device()
# ellipse(300,300,200,100)
# poly=[50,300, 150,100, 250,300, 200,400,100,400 ]
# draw_polygon(poly)
# pause()
# image=create_image(200,200)
# circle(100,100,50,image)
# draw_image(50,50,image)
# 设置原点 (0, 0) 为屏幕中央（Y轴默认向下为正）
# close_graph()
