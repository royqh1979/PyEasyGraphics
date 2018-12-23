"""
The BGI compatible module

This module defines all the functions in the BGI
"""
import easygraphics as eg

from easygraphics.image import Image

__all__ = [
    'SOLID_LINE', 'DOTTED_LINE', 'CENTER_LINE', 'DASHED_LINE', 'USERBIT_LINE', 'NULL_LINE',
    'NORM_WIDTH', 'THICK_WIDTH',
    'COPY_PUT', 'XOR_PUT', 'AND_PUT', 'OR_PUT', 'NOT_PUT',
    'LEFT_TEXT', 'CENTER_TEXT', 'RIGHT_TEXT', 'TOP_TEXT', 'BOTTOM_TEXT',
    'arc', 'bar', 'circle', 'cleardevice', 'clearviewport', 'closegraph',
    'drawpoly', 'ellipse', 'fillellipse', 'fillpoly', 'floodfill',
    'getbkcolor', 'getcolor', 'getfillsettings', 'getimage', 'getlinesettings',
    'getmaxx', 'getmaxy', 'getpixel', 'getx', 'gety', 'initgraph', 'line',
    'linerel', 'lineto', 'moverel', 'moveto', 'outtext', 'outtextxy',
    'pieslice', 'putimage', 'putpixel', 'rectangle', 'sector', 'setbkcolor',
    'setcolor', 'setfillstyle', 'setlinestyle', 'settextjustify', 'setviewport',
    'setwritemode', 'textheight', 'textwidth'
]

SOLID_LINE = eg.LineStyle.SOLID_LINE
"""Solid line"""
DOTTED_LINE = eg.LineStyle.DOT_LINE
"""Dotted line"""
CENTER_LINE = eg.LineStyle.DASH_LINE
"""Center line"""
DASHED_LINE = eg.LineStyle.DASH_DOT_LINE
"""Dashed line"""
USERBIT_LINE = eg.LineStyle.SOLID_LINE
"""User defined line (Not implemented)"""
NULL_LINE = eg.LineStyle.NO_PEN
"""No line"""

NORM_WIDTH = 1
"""1 pixel wide"""
THICK_WIDTH = 3
"""3 pixel wide"""

COPY_PUT = eg.CompositionMode.SOURCE
"""Copy source bitmap image"""
XOR_PUT = eg.CompositionMode.SRC_XOR_DEST
"""Exclusive-or source image with that on the screen"""
OR_PUT = eg.CompositionMode.SRC_OR_DEST
"""Inclusive-or source image with that on the screen"""
AND_PUT = eg.CompositionMode.SRC_AND_DEST
"""And source image with that on the screen"""
NOT_PUT = eg.CompositionMode.NOT_SRC
"""Copy inverse of the source image"""

LEFT_TEXT = 0
CENTER_TEXT = 1
RIGHT_TEXT = 2
BOTTOM_TEXT = 0
TOP_TEXT = 2

_text_v_align = LEFT_TEXT
_text_h_align = TOP_TEXT


def arc(x: int, y: int, start: int, end: int, rad: int, img: Image = None):
    """
    Draw a Circular Arc

    arc() draws the outline of an arc in the current drawing color.  The
    circular arc is centered at ('x','y') with a radius of 'rad'.  The arc
    travels from 'start' to 'end.

    **Note**:    'start' and 'end' are in degrees; 0 degrees is a 3
        o'clock.
    """
    eg.arc(x, y, start, end, rad, rad, img)


bar = eg.fill_rect


def bar3d():
    pass


circle = eg.circle

cleardevice = eg.clear_device

clearviewport = eg.clear_view_port

closegraph = eg.close_graph

drawpoly = eg.draw_poly_line

ellipse = eg.arc

fillellipse = eg.draw_ellipse

fillpoly = eg.fill_polygon

floodfill = eg.flood_fill

getbkcolor = eg.get_background_color

getcolor = eg.get_color


def getfillsettings(img: Image = None):
    """
    get fill settings

    :return: fill style, fill color
    """
    return eg.get_fill_style(img), eg.get_fill_color(img)


getimage = eg.capture_screen


def getlinesettings(img: Image = None):
    """
    Get line settings

    :return: line style, line width
    """
    return eg.get_line_style(img), eg.get_line_width(img)


def getmaxx(img: Image = None) -> int:
    """
    Get the maximum x value of graphics screen

    :return: the maximum x value
    """
    return eg.get_width(img) - 1


def getmaxy(img: Image = None):
    """
    Get the maximum y value of graphics screen

    :return: the maximum y value
    """
    return eg.get_height(img) - 1


getpixel = eg.get_pixel

getx = eg.get_x

gety = eg.get_y

initgraph = eg.init_graph

line = eg.line

linerel = eg.line_rel

lineto = eg.line_to

moverel = eg.move_rel

moveto = eg.move_to


def outtext(text: str, img: Image = None):
    """
    Display the given text on the current position

    :param text: text to be displayed
    """
    outtextxy(eg.get_x(), eg.get_y(), text, image=img)


def outtextxy(x: int, y: int, text: str, img: Image = None):
    """
    Display the given text on the specified position

    :param x: x pos of the string
    :param y: y pos of the string
    :param text: text to be displayed
    """
    x_offset = 0
    if _text_h_align == CENTER_TEXT:
        x_offset = -(eg.text_width(text, img) // 2)
    if _text_h_align == RIGHT_TEXT:
        x_offset = -eg.text_width(text, img)
    y_offset = 0
    if _text_v_align == TOP_TEXT:
        y_offset = eg.text_height(img)
    if _text_v_align == CENTER_TEXT:
        y_offset = eg.text_height(img) // 2
    eg.draw_text(x + x_offset, y + y_offset, text, image=img)


def pieslice(x: float, y: float, start_angle: int, end_angle: int, r: float, img: Image = None):
    eg.draw_pie(x, y, start_angle, end_angle, r, r, image=img)


def putimage(left: int, top: int, src_image: Image, mode: int, dst_image: Image = None):
    """
    Puts a previously-saved bit image back onto the screen.

    The coordinates ('left','top') are used to place the image on the
    screen.

    image is a previously screen copy (using getimage()).

    'op' determines how the color for each destination pixel is computed. This is based on the pixel
    already on the screen and the source pixel in memory. The available ops are COPY_PUT,
    XOR_PUT, OR_PUT, AND_PUT and NOT_PUT

    :param left: left position on the screen to be copied
    :param top: top position on the screen to be copied
    :param src_image: the image to be copied
    :param op: copy operation
    """
    eg.draw_image(left, top, src_image, composition_mode=mode, dst_image=dst_image)


putpixel = eg.put_pixel

rectangle = eg.rect

sector = eg.draw_pie

setbkcolor = eg.set_background_color

setcolor = eg.set_color


def setfillstyle(pattern, color, img: Image = None):
    """
    Set fill pattern
    :param pattern: fill style
    :param color: fill color
    """
    eg.set_fill_style(pattern, img)
    eg.set_fill_color(color, img)


def setlinestyle(linstyle, upattern, thickness, img: Image = None):
    """
    Set line style
    :param linstyle: line style
    :param upattern:  no use
    :param thickness: line width
    :param img:
    :return:
    """
    eg.set_line_style(linstyle, img)
    eg.set_line_width(thickness, img)


def settextjustify(horiz: int, vert: int):
    """
    Set Current Text Justification Settings

    settextjustify() controls text justification with respect to the
    current position (CP).  The text is justified horizontally and
    vertically.

    Constants of the text_just for 'horiz' are: LEFT_TEXT, CENTER_TEXT, RIGHT_TEXT

    Constants of the text_just for 'vert' are: TOP_TEXT, CENTER_TEXT, BOTTOM_TEXT
    """
    _text_v_align = vert
    _text_h_align = horiz


setviewport = eg.set_view_port


def setwritemode(mode, img: Image = None):
    """
    Set Write Mode for Line Drawing

    This function sets the writing mode for line drawing. If mode is 0,
    lines overwrite the screen's current contents. On the other hand,
    If mode is 1, an exclusive OR (XOR) is done.
    """
    eg.set_write_mode(mode, img)


textheight = eg.text_height

textwidth = eg.text_width
