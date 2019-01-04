import sys
import threading
import time
import math
from functools import reduce
from typing import List, Optional

from PyQt5 import QtWidgets

from .consts import *
from ._utils import invoke_in_app_thread
from .graphwin import GraphWin
from .image import Image

__all__ = [
    # consts
    'Color', 'FillStyle', 'LineStyle', 'RenderMode', 'CompositionMode', 'TextFlags',
    'MouseMessageType',
    #  setting functions #
    'set_line_style', 'get_line_style', 'set_line_width', 'get_line_width',
    'get_color', 'set_color', 'get_fill_color', 'set_fill_color', 'get_fill_style', 'set_fill_style',
    'get_background_color', 'set_background_color', 'set_font', 'get_font', 'set_font_size', 'get_font_size',
    'set_composition_mode', 'get_composition_mode', 'get_x', 'get_y', 'set_view_port', 'reset_view_port', 'set_origin',
    'set_render_mode', 'get_render_mode', 'get_drawing_pos', 'set_clip_rect', 'set_clipping',
    'set_window', 'reset_window', 'translate', 'rotate', 'scale', 'skew', 'shear', 'set_flip_y',
    'reflect', 'flip', 'mirror', 'reset_transform', 'save_settings', 'restore_settings',
    'get_width', 'get_height', 'get_write_mode', 'set_write_mode',
    # drawing functions #
    'draw_point', 'put_pixel', 'get_pixel', 'line', 'draw_line', 'move_to', 'move_rel', 'line_to', 'line_rel',
    'circle', 'draw_circle', 'fill_circle', 'ellipse', 'draw_ellipse', 'fill_ellipse',
    'arc', 'draw_arc', 'pie', 'draw_pie', 'fill_pie', 'chord', 'draw_chord', 'fill_chord',
    'bezier', 'draw_bezier', 'lines', 'draw_lines', 'poly_line', 'draw_poly_line', 'polygon', 'draw_polygon',
    'fill_polygon', 'rect', 'draw_rect', 'fill_rect', 'rounded_rect', 'draw_rounded_rect', 'fill_rounded_rect',
    'flood_fill', 'draw_image', 'capture_screen', 'clear_device', 'clear_view_port',
    # text functions #
    'draw_text', 'draw_rect_text', 'text_width', 'text_height',
    # image functions #
    'set_target', 'get_target', 'create_image', 'save_image', 'close_image', 'load_image', 'put_image',
    # time control functions#
    'pause', 'delay', 'delay_fps', 'delay_jfps', 'is_run',
    # keyboard and mouse functions #
    'has_kb_msg', 'has_kb_hit', 'has_mouse_msg', 'get_key', 'get_char', 'get_mouse_msg', 'get_cursor_pos', 'get_click',
    "contains_left_button", "contains_right_button", "contains_mid_button",
    # init and close graph window #
    'init_graph', 'close_graph', 'set_caption', 'get_graphics_window',
    # utility functions #
    'color_rgb', 'color_cmyk', 'color_hsv', 'rgb', 'to_alpha', 'pol2cart', 'cart2pol',
    # 'GraphWin',
    'Image',
]


#  settings

def set_line_style(line_style, image: Image = None):
    """
    Set line style of the specified image.

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
    Get line style of the specified image.

    The line style will be used when drawing lines or shape outlines.

    :param image: the target image whose line style is to be gotten. None means it is the target image
        (see set_target() and get_target())
    :return: line style used by the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_line_style()


def set_line_width(width: float, image: Image = None):
    """
    Set line width (thickness) of the specified image.

    It will be used when drawing lines or shape outlines

    :param width: line width (line thickness)
    :param image: the target image whose line width is to be set. None means it is the target image
        (see set_target() and get_target())
    """
    image, on_screen = _check_on_screen(image)
    image.set_line_width(width)


def get_line_width(image: Image = None) -> float:
    """
    Get line width (thinkness) of the specified image.

    It will be used when drawing lines or shape outlines

    :param image: the target image whose line width is to be gotten. None means it is the target image
        (see set_target() and get_target())
    :return: line width (line thickness) of the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_line_width()


def get_width(image: Image = None) -> int:
    """
    Get width of the specified image.

    :param image: the target image whose width is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: width of the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_width()


def get_height(image: Image = None) -> int:
    """
    Get height of the specified image.

    :param image: the target image whose width is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: height of the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_height()


def get_color(image: Image = None):
    """
    Get the foreground (drawing) color of the specified image.

    it will be used when drawing lines or shape outlines

    :param image: the target image whose foreground color is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: foreground color of the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_color()


def set_color(color, image: Image = None):
    """
    Set the foreground (drawing) color of the specified image.

    it will be used when drawing lines or shape outlines.

    the possible color could be consts defined in Color class,
    or the color created by rgb() function,
    or PyQt5\'s QColor , QGradient object or Qt.GlobalColor consts (see the pyqt reference).

    :param color:  the foreground color
    :param image: the target image whose foreground color is to be set. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_color(color)


def get_fill_color(image: Image = None):
    """
    Get the fill color of the specified image.

    it will be used when drawing and fill shapes.

    :param image: the target image whose fill color is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: fill color of the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_fill_color()


def set_fill_color(color, image: Image = None):
    """
    Set the fill (drawing) color of the specified image.

    It will be used when drawing and fill shapes.

    the possible color could be consts defined in Color class,
    or the color created by rgb() function,
    or PyQt5\'s QColor , QGradient object or Qt.GlobalColor consts (see the pyqt reference).

    :param color:  the fill color
    :param image: the target image whose fill color is to be set. None means it is the target image
         (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_fill_color(color)


def get_fill_style(image: Image = None):
    """
    Get fill style of the specified image.

    it will be used when drawing and fill shapes.

    :param image: the target image whose fill style is to be gotten. None means it is the target image
         (see set_target() and get_target()).
    :return: fill style of the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_fill_style()


def set_fill_style(style, image: Image = None):
    """
     Set fill style of the specified image.

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
    Get the background color of the image.

    it will be used when the image is cleared. (see clear_device())

    :param image: the target image whose background color is to be gotten. None means it is the target image
         (see set_target() and get_target()).
    :return: background color of the specified image
    """

    image, on_screen = _check_on_screen(image)
    return image.get_background_color()


def set_background_color(color, image: Image = None):
    """
    Set and change the background color.

    the possible color could be consts defined in Color class,
    or the color created by rgb() function,
    or PyQt5\'s QColor , QGradient object or Qt.GlobalColor consts (see the pyqt reference).

    :param color:  the background color
    :param image: the target image whose background color is to be set. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_background_color(color)
    if on_screen:
        _win.invalid()


def set_font(font: QtGui.QFont, image: Image = None):
    """
    Set font of the specified image.

    :param font: the font will be used
    :param image: the target image whose font is to be set. None means it is the target image
         (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_font(font)


def get_font(image: Image = None) -> QtGui.QFont:
    """
    Get font of the specified image.

    :param image: the target image whose font is to be gotten. None means it is the target image
         (see set_target() and get_target()).
    :return: the font used by the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_font()


def set_composition_mode(mode, image: Image = None):
    """
    Set composition mode of the specified image.

    Composition modes are used to specify how the pixels in the source (image/pen/brush),
    are merged with the pixel in the destination image.

    :param mode: composition mode
    :param image: the target image whose composition mode is to be set. None means it is the target image
         (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_composition_mode(mode)


def get_composition_mode(image: Image = None):
    """
    Get composition mode of the specified image.

    When drawing ,the composition mode will decide how the result pixel color will be computed
     (using source color and color of the destination)

    :param image: the target image whose composition mode is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: composition mode
    """
    image, on_screen = _check_on_screen(image)
    return image.get_composition_mode()


get_write_mode = get_composition_mode

set_write_mode = set_composition_mode


def set_font_size(size: int, image: Image = None):
    """
    Set font size of the specified image.

    :param size: font size of the specified image
    :param image: the target image whose write mode is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_font_size(size)


def get_font_size(image: Image = None) -> int:
    """
    Get font size of the specified image.

    :param image: the target image whose write mode is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: font size of the specified image
    """
    image, on_screen = _check_on_screen(image)
    return image.get_font_size()


def get_x(image: Image = None) -> float:
    """
    Get the x coordinate value of the current drawing position (x,y).

    Some drawing functions will use the current pos to draw.(see line_to(),line_rel(),move_to(),move_rel()).

    :param image: the target image whose drawing pos is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: the x coordinate value of the current drawing position
    """
    image, on_screen = _check_on_screen(image)
    return image.get_x()


def get_y(image: Image = None) -> float:
    """
    Get the y coordinate value of the current drawing position (x,y).

    Some drawing functions will use the current pos to draw.(see line_to(),line_rel(),move_to(),move_rel()).

    :param image: the target image whose drawing pos is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return: the y coordinate value of the current drawing position
    """
    image, on_screen = _check_on_screen(image)
    return image.get_y()


def get_drawing_pos(image: Image = None) -> (float, float):
    """
    Get the current drawing position (x,y).

    Some drawing functions will use the current pos to draw.(see line_to(),line_rel(),move_to(),move_rel()).

    :param image: the target image whose drawing pos is to be gotten. None means it is the target image
        (see set_target() and get_target()).
    :return:  the current drawing position (x,y)
    """
    image, on_screen = _check_on_screen(image)
    return image.get_x(), image.get_y()


def set_view_port(left: int, top: int, right: int, bottom: int, clip: bool = True, image: Image = None):
    """
    Set the view port of the the specified image.

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
    :param clip: if True, drawings outside the port rectangle will be clipped
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
    else:
        image.set_clipping(False)


def reset_view_port(image: Image = None):
    """
    Reset the view port setting.

    :param image: the target image whose view port is to be reset. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.reset_view_port()
    image.reset_window()
    image.set_clipping(False)


def set_clip_rect(left: int, top: int, right: int, bottom: int, image: Image = None):
    """
    Set the clip rect.

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


def set_clipping(clipping: bool, image: Image = None):
    """
    Set clipping.

    Use set_clip_rect() to set the clip rectangle.

    :param clipping:  True will turn on clipping, False will turn off clipping
    :param image: the target image whose clip rect is to be disabled. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_clipping(clipping)


def set_window(origin_x: int, origin_y: int, width: int, height: int, image: Image = None):
    """
    Set the logical drawing window.

    All your drawing is first drawing on the logical window, then mapping to view port (see set_view_port()).\
    The logical window\'s 4 corner points to streched to match the view port.

    If your view port is 200x200，and you use set_window(-50,-50,100,100) to get a 100x100 logical window with \
    the origin at (-50,50) , then the logical window\'s origin (0,0) is mapping to view port\'s (-50,-50), and \
    right-bottom corner (100,100) is mapping to view port\'s right bottom corner (200,200). All logical points is \
    mapping accordingly.

    If you just want to transform the drawing, use set_origin()/translate()/rotate()/scale().

    The drawing outside the logical window is not clipped. If you want to clip it, use set_clip_rect().

    :param origin_x: x pos of the logical window\'s origin
    :param origin_y: y pos of the logical window\'s origin
    :param width: width of the logical window
    :param height: height of the logical window
    :param image: the target image whose logical window is to be set. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_window(origin_x, origin_y, width, height)


def reset_window(image: Image = None):
    """
    Reset/remove the logical window.

    See set_window().

    :param image: the target image whose logical window is to be reset. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.reset_window()


def set_origin(x: float, y: float, image: Image = None):
    """
    Set the drawing systems' origin(0,0) to (x,y).

    The effect of this function is , when drawing, x and y is added to points coordinates.
    That is, if you want to draw a point at (x0,y0), it\'s really drawn at (x0+x,x0+y)

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
    Translates the coordinate system by the given offset; i.e.the given offset is added to points.

    :param offset_x: offset on the x coordinate
    :param offset_y: offset on the y coordinate
    :param image: the target image to be translated. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.translate(offset_x, offset_y)


def rotate(degree: float, x: float = 0, y: float = 0, image: Image = None):
    """
    Rotates the coordinate system around the point (x,y) with the given angle (in degree) clockwise.

    :param degree: the rotate angle (in degree)
    :param x: the x coordinate of the rotation center
    :param y: the y coordinate of the rotation center
    :param image: the target image to be rotated. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.rotate(degree, x, y)


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


def shear(sh: float, sv: float, x: float = 0, y: float = 0, image: Image = None):
    """
    Shear (skew) the coordinates around the point (x,y) by sh,sv.

    :param sh: shear ratio on the x-axis
    :param sv: shear ratio on the y-axis
    :param x: the x coordinate of the skew center
    :param y: the y coordinate of the skew center
    :param image: the target image to be sheared. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.shear(sh, sv, x, y)


skew = shear


def reflect(x: float, y: float, x1: float = 0, y1: float = 0, image: Image = None):
    """
    Reflect the coordinates against the line passing (x1,y1) and (x,y).

    **Note that all things will get reflected, including text!**
    If you just want to draw on a normal coordinate system with the y-axis grows bottom up,
    use flip_y().

    :param x: x coordinate value
    :param y: y coordinate value
    :param x1: the x coordinate of  the second point
    :param y1: the y coordinate of the second point
    :param image: the target image to be reflected. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.reflect(x, y, x1, y1)


mirror = reflect

flip = reflect


def set_flip_y(flip_y: bool, image: Image = None) -> None:
    """
    Reflect without texts using the x-axis as the axis (image upside down).

    Texts will not get flipped.

    **Don't translate the origin to other points** (but you can translate and then translate back)
    before drawing any text. Or the text position's calculation will get wrong! So if you want to
    set the origin to the image/image's center, call set_flip_y() after the set_origin() or
    translate()!

    **Note**: Use this functions instead of the reflect()/flip()/mirror(),if you only
    want to draw on an ordinary coordinate system with y-axis grows bottom-up.

    :param flip_y: True to turn on the flip, False to turn off.
    :param image: the target image to be flipped. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.set_flip_y(flip_y)


def reset_transform(image: Image = None):
    """
    Reset all transforms (translate/rotate/scale).

    :param image: the target image to be reset. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.reset_transform()


def save_settings(image: Image = None):
    """
    Save current drawing settings.

    See restore_settings().

    Note: background_color and current position won't  be saved and restored.


    :param image: the target image whose drawing settings is to be saved. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.save_settings()


def restore_settings(image: Image = None):
    """
    Restore previously saved drawing settings.

    See save_settings().

    Note: background_color and current position won't  be saved and restored.

    :param image: the target image whose drawing settings is to be restored. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.restore_settings()


def set_render_mode(mode: int):
    """
    Set render mode of the graphics window.

    This mode will control how the graphics window is updated.

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
    Set render mode of the graphics window.

    This mode will control how the graphics window is updated.
    See **set_render_mode()**

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
    Draw a point at (x,y) on the specified image.

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
    Set a pixel\'s color on the specified image.

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
    Get a pixel\'s color on the specified image.

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
    Draw a line from (x1,y1) to (x2,y2) on the specified image.

    It\'s the same with line().

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
    Set the drawing position to (x,y).

    The drawing position is used by line_to(), line_rel() and move_rel().

    :param x: x coordinate value of the new drawing position
    :param y: y coordinate value of the new drawing position
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.move_to(x, y)


def move_rel(dx: float, dy: float, image: Image = None):
    """
    Move the drawing position by (dx,dy).

    If the old position is (x,y), then the new position will be (x+dx,y+dy).

    The drawing position is used by line_to(), line_rel().

    :param dx: x coordinate offset of the new drawing position
    :param dy: y coordinate offset of the new drawing position
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.move_rel(dx, dy)


def line_to(x: float, y: float, image: Image = None):
    """
    Draw a line from the current drawing position to (x,y), then set the drawing position is set to (x,y).

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
    Draw a line from the current drawing position (x,y) to (x+dx,y+dy), \
    then set the drawing position is set to (x+dx,y+dy).

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
    Draw a circle outline centered at (x,y) with radius r.

    The circle is not filled.

    :param x: x coordinate value of the circle\'s center
    :param y: y coordinate value of the circle\'s center
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
    Draw a circle centered at (x,y) with radius r.

    The circle is filled and has outline.

    :param x: x coordinate value of the circle\'s center
    :param y: y coordinate value of the circle\'s center
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
    Fill a circle centered at (x,y) with radius r.

    The circle doesn\'t has outline.

    :param x: x coordinate value of the circle\'s center
    :param y: y coordinate value of the circle\'s center
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
    Draw an ellipse outline centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y.

    The ellipse is not filled.

    :param x: x coordinate value of the ellipse\'s center
    :param y: y coordinate value of the ellipse\'s center
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
    Draw an ellipse centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y.

    The ellipse is filled and has outline.

    :param x: x coordinate value of the ellipse\'s center
    :param y: y coordinate value of the ellipse\'s center
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
    Fill an ellipse centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y.

    The ellipse doesn\'t has outline.

    :param x: x coordinate value of the ellipse\'s center
    :param y: y coordinate value of the ellipse\'s center
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
    Draw an elliptical arc from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    **note**: Degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse\'s center
    :param y: y coordinate value of the ellipse\'s center
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
    Draw an elliptical pie outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    The pie is not filled.

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse\'s center
    :param y: y coordinate value of the ellipse\'s center
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
    Draw an elliptical pie from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    The pie is filled and has outline.

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse\'s center
    :param y: y coordinate value of the ellipse\'s center
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
    Fill an elliptical pie from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    The pie doesn\'t have outline.

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse\'s center
    :param y: y coordinate value of the ellipse\'s center
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
    Draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    The chord is not filled.

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse\'s center
    :param y: y coordinate value of the ellipse\'s center
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
    Draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    The chord is filled and has outline

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse\'s center
    :param y: y coordinate value of the ellipse\'s center
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
    Draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
    which radius on x-axis is radius_x and radius on y-axis is radius_y.

    The chord doesn\'t have outline.

    **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
    at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

    :param x: x coordinate value of the ellipse\'s center
    :param y: y coordinate value of the ellipse\'s center
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


def draw_bezier(control_points: List[float], image: Image = None):
    """
    Draw a cubic bezier curve.

    "control_points" is a list of 4 control points. Each point has 2 coordinate values in the list ,
    so there should be 8 values int the list.

    That is , if your 4 control points  are (x0,y0),(x1,y1),(x2,y2),(x3,y3), "control_points" should be  \
    [x0,y0,x1,y1,x2,y2,x3,y3] .

    >>> from easygraphics import *
    >>> init_graph(600,400)
    >>> points=[300,50,200,50,200,200,100,200]
    >>> draw_bezier(points)
    >>> pause()
    >>> close_graph()

    :param control_points: the control points list
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_bezier(control_points)
    if on_screen:
        _win.invalid()


bezier = draw_bezier


def draw_lines(points: List[float], image: Image = None):
    """
    Draw lines.

    "points" is a 2D point pair list. It should contain even points, and each 2 points make a point pair.
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


def draw_poly_line(end_points: List[float], image: Image = None):
    """
    Draw a poly line.

    "end_points" is a 2D points list. Each 2 values in the list make a point. A poly line will be drawn to connect
    adjacent end_points defined by the the list.

    For examples , if "end_points" is [50,50,550,350, 50,150,550,450, 50,250,550,550], draw_poly_line() will draw
    5 lines: (50,50) to (550,350), (550,350) to (50,150), (50,150) to (550,450), (550,540) to (50,250)
    and(50,250) to (550,550)

    >>> from easygraphics import *
    >>> init_graph(600,600)
    >>> points=[50,50,550,350,50,150,550,450,50,250,550,550]
    >>> draw_poly_line(points)
    >>> pause()
    >>> close_graph()

    :param end_points: point value list
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.draw_poly_line(end_points)
    if on_screen:
        _win.invalid()


poly_line = draw_poly_line


def polygon(vertices: List[float], image: Image = None):
    """
    Draw polygon outline.

    "vertices" is a 2D point list. Each 2 values in the list make a point. A polygon will be drawn to connect adjacent
    points defined by the the list.

    For examples , if "vertices" is [50,50,550,350, 50,150], poly_gon() will draw a triangle with vertices at
    (50,50) , (550,350) and (50,150)

    The polygon is not filled.

    >>> from easygraphics import *
    >>> init_graph(600,600)
    >>> set_color(Color.RED)
    >>> points=[50,50,550,350,50,150]
    >>> polygon(points)
    >>> pause()
    >>> close_graph()

    :param vertices: point value list
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.polygon(vertices)
    if on_screen:
        _win.invalid()


def draw_polygon(vertices: List[float], image: Image = None):
    """
    Draw a polygon.

    "vertices" is a 2D point list. Each 2 values in the list make a point. A polygon will be drawn to connect adjacent
    points defined by the the list.

    For examples , if "vertices" is [50,50,550,350, 50,150], poly_gon() will draw a triangle with vertices at
    (50,50) , (550,350) and (50,150)

    The polygon is filled and has outline.

    >>> from easygraphics import *
    >>> init_graph(600,600)
    >>> set_color(Color.RED)
    >>> set_fill_color(Color.LIGHT_MAGENTA)
    >>> points=[50,50,550,350,50,150]
    >>> draw_polygon(points)
    >>> pause()
    >>> close_graph()

    :param vertices: point value list
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.polygon(vertices)
    if on_screen:
        _win.invalid()
    image, on_screen = _check_on_screen(image)
    image.draw_polygon(vertices)
    if on_screen:
        _win.invalid()


def fill_polygon(vertices: List[float], image: Image = None):
    """
    Fill a polygon.

    "points" is a 2D point list. Each 2 values in the list make a point. A polygon will be drawn to connect adjacent
    points defined by the the list.

    For examples , if points is [50,50,550,350, 50,150], poly_gon() will draw a triangle with vertices at
    (50,50) , (550,350) and (50,150)

    The polygon doesn\'t have outline.

    >>> from easygraphics import *
    >>> init_graph(600,600)
    >>> set_fill_color(Color.LIGHT_MAGENTA)
    >>> points=[50,50,550,350,50,150]
    >>> fill_polygon(points)
    >>> pause()
    >>> close_graph()

    :param vertices: point value list
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.fill_polygon(vertices)
    if on_screen:
        _win.invalid()


def rect(left: float, top: float, right: float, bottom: float, image: Image = None):
    """
    Draws a rectangle outline with upper left corner at (left, top) and lower right corner at (right,bottom).

    The rectangle is not filled.

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
    Draws a rectangle with upper left corner at (left, top) and lower right corner at (right,bottom).

    The rectangle is filled and has outline.

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
    Draws a rectangle with upper left corner at (left, top) and lower right corner at (right,bottom).

    The rectangle doesn\'t have outline.

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

    The rectangle is not filled.

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

    The rectangle is filled and has outline.

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

    The rectangle doesn\'t have outline.

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
    Flood fill the image starting from(x,y) and ending at borders with border_color.

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
               src_height: int = -1, with_background=True, composition_mode=None, dst_image: Image = None):
    """
    Copy part of the source image (src_image) to the destination image (dst_image).

    (x, y) specifies the top-left point in the destination image that is to be drawn onto.

    (sx, sy) specifies the top-left point of the part in the source image that is to \
     be drawn. The default is (0, 0).

    (sw, sh) specifies the size of the part of the source image that is to be drawn.  \
    The default, (0, 0) (and negative) means all the way to the bottom-right of the image.

    if with_background is False, the source image's background will not be copied.

    The final result will depend on the composition mode and the source image's background.
    In the default mode (CompositionMode.SOURCE_OVER), the source will fully overwrite the destination).

    If you want to get a transparent copy, you should use draw_image_transparent().

    :param x: x coordinate value of the upper left point on the destination image
    :param y: y coordinate value of the upper left point on the destination image
    :param src_image: the source image to be copied
    :param src_x: x coordinate value of the top-left point of of the part to be drawn
    :param src_y: y coordinate value of the top-left point of of the part to be drawn
    :param src_width: witdh of the top-left point of of the part to be drawn
    :param src_height: height of the top-left point of of the part to be drawn
    :param with_background: if the background should be copied.
    :param composition_mode: if is None, use dst image's composition mode to copy.
    :param dst_image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    dst_image, on_screen = _check_on_screen(dst_image)
    dst_image.draw_image(x, y, src_image, src_x, src_y, src_width, src_height, with_background, composition_mode)
    if on_screen:
        _win.invalid()


put_image = draw_image


def capture_screen(left: int, top: int, right: int, bottom: int, target_img: Image):
    """
    Caputre specified region on the graphics windows to target image.

    :param left: x coordinate of the capture region\'s upper left corner
    :param top: y coordinate of the capture region\'s upper left corner
    :param right: x coordinate of the capture region\'s bottom right corner
    :param bottom: y coordinate of the capture region\'s bottom right corner
    :param target_img: image to save the capture
    """
    draw_image(0, 0, _win.get_canvas(), src_x=left, src_y=top,
               src_width=right - left, src_height=bottom - top, dst_image=target_img)


def clear_device(image: Image = None):
    """
    Clear the image to show the background.

    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.clear()
    if on_screen:
        _win.invalid()


def clear_view_port(image: Image = None):
    """
    clear view port to show the background.

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
    Prints the given texts beginning at the given position (x,y).

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
    Print the given texts in the specified rectangle area.

    Flags are defined as TextFlag const.

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
    Return width of the text.

    :param text: the text
    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    return image.text_width(text)


def text_height(image: Image = None):
    """
    Return height of the text (font height).

    :param image: the target image which will be painted on. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    return image.text_height()


# image processing #

_is_target_on_screen = True

_target_image = None


def set_target(image: Image = None):
    """
    Set the target image for drawing on.

    :param image: the target image which will be painted on. None means paint on the grapchis window.
    """
    global _target_image, _is_target_on_screen
    _check_app_run()
    if image is None:
        if _headless:
            raise RuntimeError("Can't set target to graphics window in headless mode!")
        _is_target_on_screen = True
        _target_image = _win.get_canvas()
    else:
        _is_target_on_screen = False
        _target_image = image


def get_target() -> Optional[Image]:
    """
    Get the target image for drawing on.

    :return: the target image which will be painted on. None means paint on the grapchis window.
    """
    if _is_target_on_screen:
        _check_app_run()
    return _target_image


def create_image(width, height) -> Image:
    """
    Create a new image.

    :param width: width of the new image
    :param height: height of the new image
    :return: the created image
    """
    image = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32_Premultiplied)
    image.fill(Color.WHITE)
    return Image(image)


def close_image(image: Image):
    """
    Close the specied image.

    :param image: the image to be closed
    """
    image.close()


def load_image(filename: str) -> Image:
    """
    Load a image from the file.

    :param filename: the image file
    :return: the loaded image
    """
    image = QtGui.QImage(filename)
    return Image(image)


def save_image(filename: str, with_background=True, image: Image = None):
    """
    Save image to file.

    Set with_background to False to get a transparent background image.

    Note that JPEG format doesn\'t support transparent. Use PNG format if you want a transparent background.

    :param filename: path of the file
    :param with_background: True to save the background together. False not
    :param image: the target image which will be saved. None means it is the target image
        (see set_target() and get_target()).
    """
    image, on_screen = _check_on_screen(image)
    image.save(filename, with_background)


def create_image_from_file(filename: str) -> Image:
    """
    Load image form the specified file.

    :param filename: path of the file
    :return: loaded image
    """
    image = QtGui.QImage(filename)
    return Image(image)


# utils

def color_rgb(red: int, green: int, blue: int, alpha: int = 255) -> QtGui.QColor:
    """
    Create a color with RGB color values r,g,b.

    :param red: red value
    :param green: green value
    :param blue: blue value
    :param alpha: alpha channel value of the color. 255 means fully opaque
    :return: the color
    """
    return QtGui.QColor(red, green, blue, alpha)


rgb = color_rgb


def color_cmyk(c: int, m: int, y: int, k: int, alpha: int = 255) -> QtGui.QColor:
    """
    Create a color with CMYK color values c,m,y,k.

    :param c: cyan value
    :param m: magenta value
    :param y: yellow value
    :param k: black value
    :param alpha: alpha channel value of the color. 255 means fully opaque
    :return: the color
    """
    return QtGui.QColor.fromCmyk(c, m, y, k, alpha)


def color_hsv(h: int, s: int, v: int, alpha: int = 255) -> QtGui.QColor:
    """
    Create a color with HSV color values h,s,v.

    :param h: hue value
    :param s: saturation value
    :param v: lightness value
    :param alpha: alpha channel value of the color. 255 means fully opaque
    :return: the color
    """
    return QtGui.QColor.fromHsv(h, s, v, alpha)


def to_alpha(new_color, alpha: int = None) -> QtGui.QColor:
    """
    Get new color based on the given color and alpha.

    :param new_color: the base color
    :param alpha:  new color's alpha
    :return: new color with base color and the given alpha value
    """
    """
    """
    new_color = QtGui.QColor(new_color)
    if not new_color.isValid():
        raise ValueError(str(new_color) + " is not a valid color!")
    new_color.setAlpha(alpha)
    return new_color


def cart2pol(x, y):
    """
    Transform a point from cartesian coordinates to polar coordinates.

    :param x: x coordinate value of the point
    :param y: y coordinate value of the point
    :return: rho (distance from the pole (origin) to the point),
        theta (the angle between the polar-axis and the line connecting the pole and the point, in radians)
    """
    return math.hypot(x, y), math.atan2(y, x)


def pol2cart(rho, theta):
    """
    Transform a point from polar coordinates to cartesian coordinates.

    :param rho: rho coordinate value of the point
    :param theta: theta coordinate value of the point (in radians)
    :return: x,y coordinate value of the point
    """
    return rho * math.cos(theta), rho * math.sin(theta)


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
    Pause the grogram and wait for mouse clicking or keyboard hitting.

    >>> from easygraphics import *
    >>> init_graph(800,600)
    >>> pause()
    >>> close_graph()
    """
    if not is_run():
        return
    _check_not_headless()
    _win.pause()


def is_run() -> bool:
    """
    Test if the graphics system is running.

    :return: True if the graphics system is running.
    """
    return _is_run


def delay(milliseconds: int):
    """
    Delay the programm for specified milliseconds

    :param milliseconds: time to delay
    """
    _check_app_run(True)
    _win.delay(milliseconds)


def delay_fps(fps: int):
    """
    Delay the program to control fps (Frame per seconds).

    Valid fps value is 1-1000, this value is **not checked** for speed.

    This function won\'t skip frames.

    :param fps: the desire fps
    """
    _check_app_run(True)
    _win.delay_fps(fps)


def delay_jfps(fps, max_skip_count=0):
    """
    Delay to control fps with frame skipping.

    If we don't have enough time to delay, we\'ll skip some frames.

    :param fps: frames per second (max is 1000)
    :param max_skip_count: max num of  frames to skip (0 means no limit)
    :return: True if this frame should not be skipped
    """
    _check_app_run(True)
    return _win.delay_jfps(fps, max_skip_count)


# mouse and keyboards #

def has_kb_hit() -> bool:
    """
    See if any ascii char key is hitted in the last 100 ms.
    Use it with get_char().

    :return:  True if hitted, False or not
    """
    _check_app_run(True)
    return _win.has_kb_hit()


def has_kb_msg() -> bool:
    """
    See if any key is hitted in the last 100 ms.
    Use it with get_key().

    :return:  True if hitted, False or not
    """
    _check_app_run(True)
    return _win.has_kb_msg()


def has_mouse_msg() -> bool:
    """
    See if there is any mouse message(event) in the last 100 ms.

    Use it with get_mouse_msg().

    :return:  True if any mouse message, False or not
    """
    _check_app_run(True)
    return _win.has_mouse_msg()


def get_mouse_msg() -> (int, int, int, int):
    """
    Get the mouse message.

    If there is not any  mouse button is pressed or released in last 100 ms, the program will stop and wait for
    the next key hitting.

    :return: x of the cursor, y of the cursor , type, mouse buttons down
        ( QtCore.Qt.LeftButton or QtCore.Qt.RightButton or QtCore.Qt.MidButton or QtCore.Qt.NoButton)

    """
    _check_app_run(True)
    return _win.get_mouse_msg()


def get_click() -> (int, int, int):
    """
    Get the mouse click message.

    If there is not any  mouse button is clicked in last 100 ms, the program will stop and wait for
    the next key hitting.

    :return: x of the cursor, y of the cursor , mouse buttons down
        ( QtCore.Qt.LeftButton or QtCore.Qt.RightButton or QtCore.Qt.MidButton or QtCore.Qt.NoButton)
    """
    while True:
        _check_app_run(True)
        x, y, _type, buttons = _win.get_mouse_msg()
        if _type == MouseMessageType.RELEASE_MESSAGE:
            return x, y, buttons


def contains_left_button(buttons) -> bool:
    """
    Test if the buttons contains the left mouse button.

    The "buttons" should be values returned by get_click() or get_mouse()

    :param buttons: the buttons to be tested
    :return: if the buttons contains the left mouse button
    """
    return (buttons & QtCore.Qt.LeftButton) > 0


def contains_right_button(buttons) -> bool:
    """
    Test if the buttons contains the right mouse button.

    The "buttons" should be values returned by get_click() or get_mouse()

    :param buttons: the buttons to be tested
    :return: if the buttons contains the right mouse button
    """
    return (buttons & QtCore.Qt.RightButton) > 0


def contains_mid_button(buttons) -> bool:
    """
    Test if the buttons contains the middle mouse button.

    The "buttons" should be values returned by get_click() or get_mouse()

    :param buttons: the buttons to be tested
    :return: if the buttons contains the middle mouse button
    """
    return (buttons & QtCore.Qt.MidButton) > 0


def get_char() -> str:
    """
    Get the ascii char inputted by keyboard.

    If not any char key is pressed in last 100 ms, the program will stop and wait for the next key hitting.

    :return: the character inputted by keyboard
    """
    _check_app_run(True)
    return _win.get_char()


def get_key() -> (int, int):
    """
    Get the key inputted by keyboard.

    If not any  key is pressed in last 100 ms, the program will stop and wait for the next key hitting.

    :return: `keyboard code <http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#Key-enum/>`_ ,
        `keyboard modifier codes <http://pyqt.sourceforge.net/Docs/PyQt4/qt.html#KeyboardModifier-enum)/>`_
    """
    _check_app_run(True)
    return _win.get_key()


def get_cursor_pos() -> (int, int):
    """
    Get position of the mouse cursor

    :return: position's coordinate values (x,y)
    """
    _check_app_run(True)
    return _win.get_cursor_pos()


# init and close graphics #

def set_caption(title: str):
    """
    Set the graph window\'s caption

    :param title: caption title
    """
    _win.setWindowTitle(title)


def init_graph(width: int = 800, height: int = 600, headless: bool = False):
    """
    Init the easygraphics system and show the graphics window.

    If "headless" is True, easygraphics will run in headless mode, which means
    there will be no graphics window. Use this mode if you want to draw and
    save image to files.

    :param width: width of the graphics window (in pixels)
    :param height:  height of the graphics window (in pixels)
    :param headless: True to run in headless mode.

    >>> from easygraphics import *
    >>> init_graph(800,600) #prepare and show a 800*600 window
    """
    global _start_event
    # prepare Events
    if is_run():
        raise RuntimeError("The Graphics Windows is already inited!")
    _start_event = threading.Event()
    _start_event.clear()
    # start GUI thread
    thread = threading.Thread(target=__graphics_thread_func, args=(width, height, headless))
    thread.start()
    # wait GUI initiation finished
    _start_event.wait()


def get_graphics_window() -> GraphWin:
    """
    Get the graphics window

    :return: the graphics window
    """
    return _win


def close_graph():
    """
    Close the graphics windows.

    The program will exit too.

    >>> from easygraphics import *
    >>> init_graph(800,600)
    >>> pause()
    >>> close_graph()
    """
    for image in _created_images:
        image.close()
    _created_images.clear()
    if _app is not None:
        _app.exit(0)
    time.sleep(0.05)  # wait 50ms for app thread to exit


def _check_app_run(check_not_headless: bool = False):
    if not is_run():
        raise RuntimeError("Easygraphics is not inited or has been closed! Run init_graph() first!")
    if check_not_headless:
        _check_not_headless()


def _check_not_headless():
    if _headless:
        raise RuntimeError("Easygraphics is running in headless mode!")


def _check_on_screen(image: Image) -> (QtGui.QImage, bool):
    _check_app_run()
    if image is None:
        image = _target_image
        on_screen = _is_target_on_screen
        if _is_target_on_screen and _headless:
            raise RuntimeError("There are no graphics window in headless mode!")
        else:
            if _target_image is None:
                raise RuntimeError("No target image. Use set_target() to set default target image first!")
    else:
        if not _headless:
            on_screen = image is _win.get_canvas()
        else:
            on_screen = False
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
_headless = False

_created_images = []


def __graphics_thread_func(width: int, height: int, headless=False):
    global _app, _win, _target_image, _is_run, _headless, _is_target_on_screen
    _headless = headless
    _app = QtWidgets.QApplication([])
    _app.setQuitOnLastWindowClosed(True)
    invoke_in_app_thread.init_invoke_in_app()
    if not _headless:
        _win = GraphWin(width, height, _app)
        _is_target_on_screen = True
        _target_image = _win.get_canvas()
        _win.show()
        set_caption("Python Easy Graphics")
        _is_run = True
        set_font_size(18)
    else:
        _is_run = True
        _is_target_on_screen = False
        _target_image = None
    # init finished, can draw now
    _start_event.set()
    _app.exec_()
    _is_run = False
    invoke_in_app_thread.destroy_invoke_in_app()
    if not _headless:
        _win.close()
        _win = None
    _app.quit()
    _app = None
    in_shell = bool(getattr(sys, 'ps1', sys.flags.interactive))  # if in interactive mode (eg. in IPython shell)
    if not in_shell:
        sys.exit(0)
