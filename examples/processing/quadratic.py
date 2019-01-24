from easygraphics.processing import *
from easygraphics import *


def setup():
    set_size(400, 300)
    set_fill_color("red")


t = 0


def draw():
    global t
    clear()
    t += 1
    t = t % 90
    rotate(t)
    set_fill_style(FillStyle.NULL_FILL)
    set_line_width(4)
    begin_shape()
    vertex(20, 20)
    quadratic_vertex(80, 20, 50, 50)
    quadratic_vertex(20, 80, 80, 80)
    vertex(80, 60)
    end_shape()


run_app(globals())
