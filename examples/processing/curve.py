from easygraphics.processing import *
from easygraphics import *


def setup():
    set_size(400, 300)
    set_fill_color("red")


t = 0


def draw():
    global t
    t += 1
    t %= 90
    rotate(t)
    clear()
    set_line_width(4)
    begin_shape()
    curve_vertex(5, 26)
    curve_vertex(5, 26)
    curve_vertex(73, 24)
    curve_vertex(73, 61)
    curve_vertex(15, 65)
    curve_vertex(15, 65)
    end_shape()


run_app(globals())
