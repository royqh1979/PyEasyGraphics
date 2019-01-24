from easygraphics.processing import *
from easygraphics import *


def setup():
    set_size(800, 600)
    set_fill_color("red")


t = 0


def draw():
    global t
    clear()
    t = t + 1
    t = t % 350
    translate(400, 300)
    rotate(t)
    begin_shape()
    for i in range(5):
        vertex(100, 0)
        rotate(144)
    end_shape()


run_app(globals())
