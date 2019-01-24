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
    set_line_width(4)
    begin_shape()
    vertex(30, 20)
    bezier_vertex(80, 0, 80, 75, 30, 75)
    bezier_vertex(50, 80, 60, 25, 30, 20)
    end_shape()


run_app(globals())
