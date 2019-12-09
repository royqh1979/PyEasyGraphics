from easygraphics.processing import *
from easygraphics import *


def setup():
    set_size(400, 300)
    set_fill_color("red")


def draw():
    set_line_width(4)
    begin_shape(VertexType.QUAD_STRIP)
    vertex(30, 20)
    vertex(30, 75)
    vertex(50, 20)
    vertex(50, 75)
    vertex(65, 20)
    vertex(65, 75)
    vertex(85, 20)
    vertex(85, 75)
    end_shape(True)


run_app(globals())
