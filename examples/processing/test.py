from PyQt5 import QtCore

from easygraphics.processing import *
from easygraphics import *


def setup():
    set_size(800, 600)
    set_rect_mode(ShapeMode.CORNER)
    set_ellipse_mode(ShapeMode.CENTER)


def draw():
    # draw_rect(100, 100, 20, 100)
    # draw_ellipse(100, 70, 60, 60)
    # draw_ellipse(81, 70, 16, 32)
    # draw_ellipse(119, 70, 16, 32)
    # draw_line(90, 150, 80, 160)
    # draw_line(110, 150, 120, 160)
    painter = get_target().get_painter()
    set_font_size(40)

    draw_rect(100,100,50,50)
    draw_line(100,100,50,50)
    painter.drawText(100,100,100,50,QtCore.Qt.AlignCenter,"lala")


run_app(globals())
