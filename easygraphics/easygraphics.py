import threading
import sys
import time
from typing import List
from functools import reduce

from PyQt5 import QtWidgets

from .consts import *
from .graphwin import GraphWin
from .image import Image
from .dialog import invoke_in_app_thread

__all__ = [
    'Color', 'FillStyle', 'LineStyle', 'RenderMode', 'WriteMode',  # consts
    # 'GraphWin', 'Image',
    #  setting functions #
    'set_line_style', 'get_line_style', 'set_line_width', 'get_line_width',
    'get_color', 'set_color', 'get_fill_color', 'set_fill_color', 'get_fill_style', 'set_fill_style',
    'get_background_color', 'set_background_color', 'set_font', 'get_font', 'set_font_size', 'get_font_size',
    'set_write_mode', 'get_write_mode', 'get_x', 'get_y', 'set_view_port', 'reset_view_port', 'set_origin',
    'set_render_mode', 'get_render_mode', 'get_drawing_pos', 'set_clip_rect', 'disable_clip',
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


def set_view_port(left: int, top: int, right: int, bottom: int, clip: bool = True, image: Image = None):
    """
    set the view port of the the specified image

    View port is the drawing zone on the image.

    >>> from easygraphics import *
    >>> init_graph(800,600)
    >>> draw_rect(100,100,300,300)
    >>> set_view_port(100,100,300,300)
    >>> circle(100,100,50)
    >>> circle(100,100,100)
    >>> circle(100,100,120)
    >>> pause()
    >>> close_graph()

    :param left: left of the view port rectangle
    :param top: top of the view port rectangle
    :param right: right of the view port rectangle
    :param bottom: bottom of the view port rectangle
    :param clip: if True, drawings outside the port rectangle will be cliped
    :param image: the target image whose view port is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_view_port(left, top, right, bottom)
    width = right - left
    height = bottom - top
    image.set_window(0, 0, width, height)
    if clip:
        image.set_clip_rect(0, 0, width, height)


def reset_view_port(image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.reset_view_port()
    image.reset_window()
    image.disable_clip()


def set_clip_rect(left: int, top: int, right: int, bottom: int, image: Image = None):
    """
    set the clip rect

    Drawings outside the clip rect will be clipped.

    :param left: left of the clip rectangle
    :param top: top of the clip rectangle
    :param right: right of the clip rectangle
    :param bottom: bottom of the clip rectangle
    :param image: the target image whose clip rect is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_clip_rect(left, top, right, bottom)


def disable_clip(image: Image = None):
    """
    disable clipping

    drawings will not be clipped

    :param image: the target image whose clip rect is to be disabled. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.disable_clip()


def set_window(origin_x: int, origin_y: int, width: int, height: int, image: Image = None):
    """
    set the logical drawing window

    All your drawing is first drawing on the logical window, then mapping to view port (see set_view_port()).\
    The logical window's 4 corner points to streched to match the view port.

    If your view port is 200x200，and you use set_window(-50,-50,100,100) to get a 100x100 logical window with \
    the origin at (-50,50) , then the logical window's origin (0,0) is mapping to view port's (-50,-50), and \
    right-bottom corner (100,100) is mapping to view port's right bottom corner (200,200). All logical points is \
    mapping accordingly.

    If you just want to transform the drawing, use set_origin()/translate()/rotate()/scale().

    The drawing outside the logical window is not clipped. If you want to clip it, use set_clip_rect().

    :param origin_x: x pos of the logical window's origin
    :param origin_y: y pos of the logical window's origin
    :param width: width of the logical window
    :param height: height of the logical window
    :param image: the target image whose logical window is to be set. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_window(origin_x, origin_y, width, height)


def reset_window(image: Image = None):
    """
    reset/remove the logical window

    see set_window()

    :param image: the target image whose logical window is to be reset. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.reset_window()


def set_origin(x: float, y: float, image: Image = None):
    """
    set the drawing systems' origin(0,0) to (x,y)

    The effect of this function is , when drawing, x and y is added to points coordinates.
    That is, if you want to draw a point at (x0,y0), it's really drawn at (x0+x,x0+y)

    the default origin is on left-top of the specified image

    :param x: x coordinate value the new origin
    :param y: y coordinate value the new origin
    :param image: the target image whose origin is to be removed. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.translate(x, y)


def translate(offset_x: float, offset_y: float, image: Image = None):
    """
    Translates the coordinate system by the given offset; i.e. the given offset is added to points.

    :param offset_x: offset on the x coordinate
    :param offset_y: offset on the y coordinate
    :param image: the target image to be translated. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.translate(offset_x, offset_y)


def rotate(degree: float, image: Image = None):
    """
    Rotates the coordinate system the given angle (in degree)clockwise .

    :param degree: the rotate angle (in degree)
    :param image: the target image to be rotated. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.rotate(degree)


def scale(sx: float, sy: float, image: Image = None):
    """
    Scales the coordinate system by (sx, sy).

    :param sx: scale factor on x axis.
    :param sy: scale factor on y axis.
    :param image: the target image to be scaled. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.scale(sx, sy)


def reset_transform(image: Image = None):
    """
    reset all transforms (translate/rotate/scale)

    :param image: the target image to be reset. None means it is the target image
        (see set_target() and get_target()).
    """
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
    image, on_screen = _check_on_screen(image)
    image.draw_line(x1, y1, x2, y2)
    if on_screen:
        _win.invalid()


line = draw_line


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
    image, on_screen = _check_on_screen(image)
    image.draw_arc(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


arc = draw_arc


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


def draw_lines(points: List[float], image: Image = None):
    """
    draw lines
    points is a 2D point pair list. It should contain even points, and each 2 points make a point pair.
    And each point have 2 coordinate values(x,y). So if you have n point pairs, the points list should have 4*n values.

    For examples , if points is [50,50,550,350, 50,150,550,450, 50,250,550,550], draw_lines() will draw 3 lines:
    (50,50) to (550,350), (50,150) to (550,450), (50,250) to (550,550)

    >>> from easygraphics import *
    >>> init_graph(600,600)
    >>> points=[50,50,550,350,50,150,550,450,50,250,550,550]
    >>> draw_lines(points)
    >>> pause()
    >>> close_graph()

    :param points: point value list
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_lines(points)
    if on_screen:
        _win.invalid()


lines = draw_lines


def draw_poly_line(points: List[float], image: Image = None):
    """
    draw poly lines

    points is a 2D point list. Each 2 values in the list make a point. A poly line will be drawn to connect adjecent
    points defined by the the list.

    For examples , if points is [50,50,550,350, 50,150,550,450, 50,250,550,550], draw_poly_line() will draw 5 lines:
    (50,50) to (550,350), (550,350) to (50,150), (50,150) to (550,450), (550,540) to (50,250)
    and(50,250) to (550,550)

    >>> from easygraphics import *
    >>> init_graph(600,600)
    >>> points=[50,50,550,350,50,150,550,450,50,250,550,550]
    >>> draw_poly_line(points)
    >>> pause()
    >>> close_graph()

    :param points: point value list
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_poly_line(points)
    if on_screen:
        _win.invalid()


poly_line = draw_poly_line


def polygon(points: List[float], image: Image = None):
    """
    draw polygon outline

    points is a 2D point list. Each 2 values in the list make a point. A polygon will be drawn to connect adjecent
    points defined by the the list.

    For examples , if points is [50,50,550,350, 50,150], poly_gon() will draw a triangle with vertices at
    (50,50) , (550,350) and (50,150)

    The polygon is not filled.

    >>> from easygraphics import *
    >>> init_graph(600,600)
    >>> set_color(Color.RED)
    >>> points=[50,50,550,350,50,150]
    >>> polygon(points)
    >>> pause()
    >>> close_graph()

    :param points: point value list
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.polygon(points)
    if on_screen:
        _win.invalid()


def draw_polygon(points: List[float], image: Image = None):
    """
    draw polygon

    points is a 2D point list. Each 2 values in the list make a point. A polygon will be drawn to connect adjecent
    points defined by the the list.

    For examples , if points is [50,50,550,350, 50,150], poly_gon() will draw a triangle with vertices at
    (50,50) , (550,350) and (50,150)

    The polygon is filled and has outline.

    >>> from easygraphics import *
    >>> init_graph(600,600)
    >>> set_color(Color.RED)
    >>> set_fill_color(Color.LIGHTMAGENTA)
    >>> points=[50,50,550,350,50,150]
    >>> draw_polygon(points)
    >>> pause()
    >>> close_graph()

    :param points: point value list
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.polygon(points)
    if on_screen:
        _win.invalid()
    image, on_screen = _check_on_screen(image)
    image.draw_polygon(points)
    if on_screen:
        _win.invalid()


def fill_polygon(points: List[float], image: Image = None):
    """
    fill polygon

    points is a 2D point list. Each 2 values in the list make a point. A polygon will be drawn to connect adjecent
    points defined by the the list.

    For examples , if points is [50,50,550,350, 50,150], poly_gon() will draw a triangle with vertices at
    (50,50) , (550,350) and (50,150)

    The polygon doesn't have outline.

    >>> from easygraphics import *
    >>> init_graph(600,600)
    >>> set_fill_color(Color.LIGHTMAGENTA)
    >>> points=[50,50,550,350,50,150]
    >>> fill_polygon(points)
    >>> pause()
    >>> close_graph()

    :param points: point value list
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.fill_polygon(points)
    if on_screen:
        _win.invalid()


def rect(left: float, top: float, right: float, bottom: float, image: Image = None):
    """
    Draws a rectangle outline with upper left corner at (left, top) and lower right corner at (right,bottom)

    the rectangle is not filled

    :param left: x coordinate value of the upper left corner
    :param top: y coordinate value of the upper left corner
    :param right: x coordinate value of the lower right corner
    :param bottom: y coordinate value of the lower right corner
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.rect(left, top, right, bottom)
    if on_screen:
        _win.invalid()


def draw_rect(left: float, top: float, right: float, bottom: float, image: Image = None):
    """
    Draws a rectangle with upper left corner at (left, top) and lower right corner at (right,bottom)

    the rectangle is filled and has outline

    :param left: x coordinate value of the upper left corner
    :param top: y coordinate value of the upper left corner
    :param right: x coordinate value of the lower right corner
    :param bottom: y coordinate value of the lower right corner
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_rect(left, top, right, bottom)
    if on_screen:
        _win.invalid()


def fill_rect(left: float, top: float, right: float, bottom: float, image: Image = None):
    """
    Draws a rectangle with upper left corner at (left, top) and lower right corner at (right,bottom)

    the rectangle doesn't have outline

    :param left: x coordinate value of the upper left corner
    :param top: y coordinate value of the upper left corner
    :param right: x coordinate value of the lower right corner
    :param bottom: y coordinate value of the lower right corner
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.fill_rect(left, top, right, bottom)
    if on_screen:
        _win.invalid()


def rounded_rect(left: float, top: float, right: float, bottom: float, round_x: float, round_y: float,
                 image: Image = None):
    """
    Draws a rounded rectangle outline with upper left corner at (left, top) , lower right corner at (right,bottom).
    raidus on x-axis of the corner ellipse arc is round_x, radius on y-axis of the corner ellipse arc is round_y.

    the rectangle is not filled

    :param left: x coordinate value of the upper left corner
    :param top: y coordinate value of the upper left corner
    :param right: x coordinate value of the lower right corner
    :param bottom: y coordinate value of the lower right corner
    :param round_x: raidus on x-axis of the corner ellipse arc
    :param round_y: radius on y-axis of the corner ellipse arc
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.rounded_rect(left, top, right, bottom, round_x, round_y)
    if on_screen:
        _win.invalid()


def draw_rounded_rect(left: float, top: float, right: float, bottom: float, round_x: float, round_y: float,
                      image: Image = None):
    """
    Draws a rounded rectangle with upper left corner at (left, top) , lower right corner at (right,bottom).
    raidus on x-axis of the corner ellipse arc is round_x, radius on y-axis of the corner ellipse arc is round_y.

    the rectangle is filled and has outline

    :param left: x coordinate value of the upper left corner
    :param top: y coordinate value of the upper left corner
    :param right: x coordinate value of the lower right corner
    :param bottom: y coordinate value of the lower right corner
    :param round_x: raidus on x-axis of the corner ellipse arc
    :param round_y: radius on y-axis of the corner ellipse arc
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_rounded_rect(left, top, right, bottom, round_x, round_y)
    if on_screen:
        _win.invalid()


def fill_rounded_rect(left: float, top: float, right: float, bottom: float, round_x: float, round_y: float,
                      image: Image = None):
    """
    Fill a rounded rectangle with upper left corner at (left, top) , lower right corner at (right,bottom).
    raidus on x-axis of the corner ellipse arc is round_x, radius on y-axis of the corner ellipse arc is round_y.

    the rectangle doesn't have outline

    :param left: x coordinate value of the upper left corner
    :param top: y coordinate value of the upper left corner
    :param right: x coordinate value of the lower right corner
    :param bottom: y coordinate value of the lower right corner
    :param round_x: raidus on x-axis of the corner ellipse arc
    :param round_y: radius on y-axis of the corner ellipse arc
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.fill_rounded_rect(left, top, right, bottom, round_x, round_y)
    if on_screen:
        _win.invalid()


def flood_fill(x: int, y: int, border_color, image: Image = None):
    """
    flood fill the image starting from(x,y) and ending at borders with border_color

    The fill region border must be closed,or the whole image will be filled!

    :param x: x coordinate value of the start point
    :param y: y coordinate value of the start point
    :param border_color: color of the fill region border
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.flood_fill(x, y, border_color)
    if on_screen:
        _win.invalid()


def draw_image(x: int, y: int, src_image: Image, src_x: int = 0, src_y: int = 0, src_width: int = -1,
               src_height: int = -1, dst_image: Image = None):
    """
    copy part of the source image (src_image) to the destination image (self) at (x,y)

    (x, y) specifies the top-left point in the destination image that is to be drawn onto.

    (sx, sy) specifies the top-left point of the part in the source image that is to \
     be drawn. The default is (0, 0).

    (sw, sh) specifies the size of the part of the source image that is to be drawn.  \
    The default, (0, 0) (and negative) means all the way to the bottom-right of the image.

    :param x: x coordinate value of the upper left point on the destination image
    :param y: y coordinate value of the upper left point on the destination image
    :param src_image: the source image to be copied
    :param src_x: x coordinate value of the top-left point of of the part to be drawn
    :param src_y: y coordinate value of the top-left point of of the part to be drawn
    :param src_width: witdh of the top-left point of of the part to be drawn
    :param src_height: height of the top-left point of of the part to be drawn
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    dst_image, on_screen = _check_on_screen(dst_image)
    dst_image.draw_image(x, y, src_image, src_x, src_y, src_width, src_height)
    if on_screen:
        _win.invalid()


def clear_device(image: Image = None):
    """
    Clear the image with the background color

    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.clear()
    if on_screen:
        _win.invalid()


def clear_view_port(image: Image = None):
    """
    clear view port with the background color

    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.clear_view_port()
    if on_screen:
        _win.invalid()


# text processing
def draw_text(x, y, *args, sep=' ', image: Image = None):
    """
    Prints the given texts beginning at the given position (x,y)

    :param x: x coordinate value of the start point
    :param y: y coordinate value of the start point
    :param args: things to be printed (like print())
    :param sep: seperator used to join strings
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_text(x, y, *args, sep=sep)
    if on_screen:
        _win.invalid()


def draw_rect_text(x: int, y: int, width: int, height: int, *args, flags=QtCore.Qt.AlignCenter, sep: str = ' ',
                   image: Image = None):
    """
    print the given texts in the specified rectangle area

    Available flags are: （Defined in pyqt5's PyQt5.QtCore pacakge)

    * Qt.AlignLeft          Aligns with the left edge.
    * Qt::AlignRight        Aligns with the right edge.
    * Qt::AlignHCenter      Centers horizontally in the available space.
    * Qt::AlignJustify      Justifies the text in the available space.
    * Qt::AlignTop          Aligns with the top.
    * Qt::AlignBottom       Aligns with the bottom.
    * Qt::AlignVCenter      Centers vertically in the available space.
    * Qt::AlignCenter       Centers in both dimensions.
    * Qt::TextDontClip      If it's impossible to stay within the given bounds, it prints outside.
    * Qt::TextSingleLine    Treats all whitespace as spaces and prints just one line.
    * Qt::TextExpandTabs    Makes the U+0009 (ASCII tab) character move to the next tab stop.
    * Qt::TextShowMnemonic  Displays the string "&P" as P For an ampersand, use "&&".
    * Qt::TextWordWrap      Breaks lines at appropriate points, e.g. at word boundaries.

    :param x: x coordinate of the output rectangle's upper left corner
    :param y: y coordinate of the output rectangle's upper left corner
    :param width: width of the output rectangle
    :param height: height of the output rectangle
    :param args: things to be printed (like print())
    :param flags: align flags
    :param sep: seperator used to join strings
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_rect_text(x, y, width, height, flags, *args, sep=sep)
    if on_screen:
        _win.invalid()


def text_width(text: str, image: Image = None):
    """
    return width of the text

    :param text: the text
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    return image.text_width(text)


def text_height(image: Image = None):
    """
    return height of the text (font height)

    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    return image.text_height()


# image processing #

def set_target(image: Image = None):
    """
    set the target image for drawing on

    :param image: the target image which will be painted on. None means paint on the grapchis window.
    """
    global _target_image
    _check_app_run()
    if image is None:
        _target_image = _win.get_canvas()
    else:
        _target_image = image


def get_target() -> Image:
    """
    get the target image for drawing on

    :return: the target image which will be painted on. None means paint on the grapchis window.
    """
    _check_app_run()
    return _target_image


def create_image(width, height) -> Image:
    """
    create a new image

    :param width: width of the new image
    :param height: height of the new image
    :return: the created image
    """
    image = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32_Premultiplied)
    image.fill(QtCore.Qt.transparent)
    return Image(image)


def save_image(filename: str, image: Image = None):
    """
    save image to file

    :param filename: path of the file
    :param image: the target image which will be saved. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.get_image().save(filename)


def create_image_from_file(filename: str) -> Image:
    """
    load image form the specified file

    :param filename: path of the file
    :return: loaded image
    """
    image = QtGui.QImage(filename)
    return Image(image)


# utils

def rgb(red: int, green: int, blue: int, alpha: int = 255):
    """
    create a color with r,g,b

    :param red: red value
    :param green: green value
    :param blue: blue value
    :param alpha: alpha value of the color. 255 means fully opaque
    :return: the color
    """
    return QtGui.QColor(red, green, blue, alpha)


def _qpoint_to_point_list_fun(lst: List[float], p: QtCore.QPointF) -> List[float]:
    lst.append(p.x())
    lst.append(p.y())
    return lst


def qpoints_to_point_list(qpoints: List[QtCore.QPointF]) -> List[float]:
    """
    convert QPointF list to point list

    :param qpoints: QPointF list
    :return: line value list
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
    """
    Test if the graphics system is running.(
    :return:
    """
    return _is_run


def delay(milliseconds: int):
    """
    Delay the programm for specified milliseconds
    :param milliseconds: time to delay
    """
    _check_app_run()
    _win.delay(milliseconds)


def delay_fps(fps: int):
    """
    Delay the program to control fps (Frame pers seconds)

    valid fps value is 1-1000, this value is **not checked** for speed

    this function won't skip frames

    :param fps: the descire fps
    """
    _check_app_run()
    _win.delay_fps(fps)


def delay_jfps(fps, max_skip_count=10):
    """
    delay to control fps with frame skiping

    if we don't have enough time to delay, we'll skip some frames
    :param fps: frames per second (max is 1000)
    :param max_skip_count: max num of  frames to skip
    """
    _check_app_run()
    _win.delay_jfps(fps, max_skip_count)


# mouse and keyboards #

def kb_hit():
    """
    see if any ascii char key is hitted in the last 100 ms
    use it with get_char()

    :return:  True if hitted, False or not
    """
    _check_app_run()
    return _win.kb_hit()


def kb_msg():
    """
    see if any key is hitted in the last 100 ms
    use it with get_key()

    :return:  True if hitted, False or not
    """
    _check_app_run()
    return _win.kb_msg()


def mouse_msg():
    """
    see if there's any mouse message(event) in the last 100 ms
    use it with get_mouse()

    :return:  True if any mouse message, False or not
    """
    _check_app_run()
    return _win.mouse_msg()


def get_mouse():
    """
    get the key inputted by keybord
    if not any  key is pressed in last 100 ms, the program will stop and wait for the next key hitting

    :return: x of the cursor, y of the cursor , mouse buttons down
        ( Qt.LeftButton or Qt.RightButton or Qt.MidButton or Qt.NoButton)
    """
    _check_app_run()
    return _win.get_mouse()


def get_char():
    """
    get the ascii char inputted by keybord
    if not any char key is pressed in last 100 ms, the program will stop and wait for the next key hitting

    :return: the character inputted by keybord
    """
    _check_app_run()
    return _win.get_char()


def get_key():
    """
    get the key inputted by keyboard
    if not any  key is pressed in last 100 ms, the program will stop and wait for the next key hitting

    :return: keyboard code (see http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#Key-enum) , keyboard modifier codes
        (see http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#KeyboardModifier-enum)
    """
    _check_app_run()
    return _win.get_key()


# init and close graphics #

def set_caption(title: str):
    """
    set the graph window's caption

    :param title: caption title
    """
    _win.setWindowTitle(title)


def init_graph(width: int = 800, height: int = 600):
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
    time.sleep(0.05)  # wait 50ms for app thread to exit


def _check_app_run():
    if not is_run():
        raise RuntimeError("Easygrphics is not inited or has been closed! Run init_graph() first!")


def _check_on_screen(image: Image) -> (QtGui.QImage, bool):
    _check_app_run()
    if image is None:
        image = _target_image
    on_screen = image is _win.get_canvas()
    # _validate_image(image)
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
    set_font_size(18)
    _win.show()
    set_caption("Python Easy Graphics")
    # init finished, can draw now
    _start_event.set()
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
