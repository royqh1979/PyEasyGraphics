import os
import threading
import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from easygraphics.consts import *
from easygraphics.graphwin import GraphWin
from easygraphics.image import Image

if sys.version_info < (3, 6):
    raise OSError("Only Support Python 3.6 and above")


def set_line_style(line_style, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.set_line_style(line_style)


def get_line_style(image: Image = None):
    image, on_screen = _check_on_screen(image)
    return image.get_line_style()


def set_line_width(width, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.set_line_width(width)


def get_line_width(image: Image = None):
    image, on_screen = _check_on_screen(image)
    return image.get_line_width()


def get_color(image: Image = None):
    image, on_screen = _check_on_screen(image)
    return image.get_color()


def set_color(color, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.set_color(color)


def get_fill_color(image: Image = None):
    image, on_screen = _check_on_screen(image)
    return image.get_fill_color()


def set_fill_color(color, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.set_fill_color(color)


def get_fill_style(image: Image = None):
    image, on_screen = _check_on_screen(image)
    return image.get_fill_style()


def set_fill_style(style, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.set_fill_style(style)


def get_background_color(image: Image = None):
    image, on_screen = _check_on_screen(image)
    return image.get_background_color()


def set_background_color(color, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.set_background_color(color)


def draw_point(x, y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_point(x, y)
    if on_screen:
        _win.invalid()


def put_pixel(x, y, image: Image = None):
    draw_point(x, y, image)


def line(x1, y1, x2, y2, image: Image = None):
    """ Draw a line from (x1,y1) to (x2,y2) on image """
    image, on_screen = _check_on_screen(image)
    image.line(x1, y1, x2, y2)
    if on_screen:
        _win.invalid()


def draw_line(x1, y1, x2, y2, image: Image = None):
    """ Draw a line from (x1,y1) to (x2,y2) on image """
    line(x1, y1, x2, y2, image)


def move_to(x, y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.move_to(x, y)
    if on_screen:
        _win.invalid()


def move_rel(dx, dy, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.move_rel(dx, dy)
    if on_screen:
        _win.invalid()


def line_to(x, y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.line_to(x, y)
    if on_screen:
        _win.invalid()


def line_rel(dx, dy, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.line_rel(dx, dy)
    if on_screen:
        _win.invalid()


def circle(x, y, r, image: Image = None):
    """Draw a circle outline whose center is on (x,y) and radius is r """
    image, on_screen = _check_on_screen(image)
    image.ellipse(x, y, r, r)
    if on_screen:
        _win.invalid()


def draw_circle(x, y, r, image: Image = None):
    """Draw a circle whose center is on (x,y) and radius is r """
    image, on_screen = _check_on_screen(image)
    image.draw_ellipse(x, y, r, r)
    if on_screen:
        _win.invalid()


def fill_circle(x, y, r, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.fill_ellipse(x, y, r, r)
    if on_screen:
        _win.invalid()


def ellipse(x, y, radius_x, radius_y, image: Image = None):
    """Draw a circle outline whose center is on (x,y) and radius is r """
    image, on_screen = _check_on_screen(image)
    image.ellipse(x, y, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def draw_ellipse(x, y, radius_x, radius_y, image: Image = None):
    """Draw a circle whose center is on (x,y) and radius is r """
    image, on_screen = _check_on_screen(image)
    image.draw_ellipse(x, y, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def fill_ellipse(x, y, radius_x, radius_y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.fill_ellipse(x, y, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def arc(x, y, start_angle, end_angle, radius_x, radius_y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.arc(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def draw_arc(x, y, start_angle, end_angle, radius_x, radius_y, image: Image = None):
    arc(x, y, start_angle, end_angle, radius_x, radius_y, image)


def pie(x, y, start_angle, end_angle, radius_x, radius_y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.pie(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def draw_pie(x, y, start_angle, end_angle, radius_x, radius_y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_pie(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def fill_pie(x, y, start_angle, end_angle, radius_x, radius_y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.fill_pie(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def chord(x, y, start_angle, end_angle, radius_x, radius_y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.chord(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def draw_chord(x, y, start_angle, end_angle, radius_x, radius_y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_chord(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def fill_chord(x, y, start_angle, end_angle, radius_x, radius_y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.fill_chord(x, y, start_angle, end_angle, radius_x, radius_y)
    if on_screen:
        _win.invalid()


def bezier(polypoints: list, image: Image = None):
    draw_bezier(polypoints, image)


def draw_bezier(polypoints: list, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_bezier(polypoints)
    if on_screen:
        _win.invalid()


def lines(points: list, image: Image = None):
    draw_line(points, image)


def draw_lines(points: list, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_lines(points)
    if on_screen:
        _win.invalid()


def poly_line(points: list, image: Image = None):
    draw_poly_line(points, image)


def draw_poly_line(points: list, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_poly_line(points)
    if on_screen:
        _win.invalid()


def polygon(points: list, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.polygon(points)
    if on_screen:
        _win.invalid()


def draw_polygon(points: list, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_polygon(points)
    if on_screen:
        _win.invalid()


def fill_polygon(points: list, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.fill_polygon(points)
    if on_screen:
        _win.invalid()


def rect(left, top, right, bottom, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.rect(left, top, right, bottom)
    if on_screen:
        _win.invalid()


def draw_rect(left, top, right, bottom, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_rect(left, top, right, bottom)
    if on_screen:
        _win.invalid()


def fill_rect(left, top, right, bottom, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.fill_rect(left, top, right, bottom)
    if on_screen:
        _win.invalid()


def rounded_rect(left, top, right, bottom, round_x, round_y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.rounded_rect(left, top, right, bottom, round_x, round_y)
    if on_screen:
        _win.invalid()


def draw_rounded_rect(left, top, right, bottom, round_x, round_y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.draw_rounded_rect(left, top, right, bottom, round_x, round_y)
    if on_screen:
        _win.invalid()


def fill_rounded_rect(left, top, right, bottom, round_x, round_y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.fill_rounded_rect(left, top, right, bottom, round_x, round_y)
    if on_screen:
        _win.invalid()


def flood_fill(x, y, background_color, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.flood_fill(x, y, background_color)
    if on_screen:
        _win.invalid()


def draw_image(x, y, src_image, dst_image: Image = None):
    dst_image, on_screen = _check_on_screen(dst_image)
    dst_image.draw_image(x, y, src_image)
    if on_screen:
        _win.invalid()


def set_target(image: Image = None):
    global _target_image
    if image is None:
        _target_image = _win.get_canvas()
    else:
        _target_image = image


def get_target() -> Image:
    return _target_image


def set_write_mode(mode, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.set_write_mode(mode)


def get_write_mode(image: Image = None):
    image, on_screen = _check_on_screen(image)
    return image.get_write_mode()


def get_x(image: Image = None):
    image, on_screen = _check_on_screen(image)
    return image.get_x()


def get_y(image: Image = None):
    image, on_screen = _check_on_screen(image)
    return image.get_y()


def moveto(x, y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.move_to(x, y)


def set_view_port(left, top, right, bottom, clip=True, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.set_view_port(left, top, right, bottom, clip)


def reset_view_port(image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.rest_view_port()


def clear_view_port(image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.clear_view_port()
    if on_screen:
        _win.invalid()


def set_origin(x, y, image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.set_origin(x, y)


def clear_device(image: Image = None):
    image, on_screen = _check_on_screen(image)
    image.clear()
    if on_screen:
        _win.invalid()


def create_image(width, height) -> Image:
    image = QImage(width, height, QImage.Format_ARGB32_Premultiplied)
    image.fill(Qt.transparent)
    return Image(image)


def _check_on_screen(image: Image) -> (QImage, bool):
    if image is None:
        image = _target_image
    on_screen = image is _win.get_canvas()
    _validate_image(image)
    return image, on_screen


def _validate_image(image: Image):
    """ check if image is valid to draw on it"""
    if not isinstance(image, Image):
        raise ValueError("image parameter must be None or an instance return by getimage()!")
    if not isinstance(image.get_image(), QImage):
        raise ValueError("don't have valid image")
    if not isinstance(image.get_pen(), QPen):
        raise ValueError("don't have valid pen")
    if not isinstance(image.get_brush(), QBrush):
        raise ValueError("don't have valid pen")
    if not isinstance(image.get_background_color(), QColor) and \
            not isinstance(image.get_background_color(), Qt.GlobalColor):
        raise ValueError("don't have valid background color")


def __start(width, height):
    global _app, _win, _target_image
    _app = QApplication([])
    _app.setQuitOnLastWindowClosed(True)
    _win = GraphWin(width, height, _app)
    _target_image = _win.get_canvas()
    # init finished, can draw now
    _start_event.set()
    _win.show()
    _app.exec_()
    os._exit(0)
    # sys.exit(0) #can't stop main thread


def set_render_mode(mode):
    _win.set_immediate(mode == RenderMode.RENDER_AUTO)


def pause():
    _win.real_update()
    _win.pause()


def is_run():
    return _win.is_run()


def delay(milliseconds):
    _win.delay(milliseconds)


def set_caption(title: str):
    _win.setWindowTitle(title)


def init_graph(width, height):
    """ init graph """
    global _start_event
    # prepare Events
    _start_event = threading.Event()
    _start_event.clear()
    # start GUI thread
    thread = threading.Thread(target=__start, args=(width, height))
    thread.start()
    # wait GUI initiation finished
    _start_event.wait()


def close_graph():
    _app.quit()


init_graph(800, 600)

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
if __name__ == "__main__":
    draw_doraamon()

# close_graph()
