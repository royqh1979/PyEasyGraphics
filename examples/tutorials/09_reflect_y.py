"""
Draw a bus without transformations
"""
from easygraphics import *
import draw_bus

def main():
    init_graph(500, 300)

    translate(250, 150)
    translate(105,65)
    rotate(-45)
    translate(-105,-65)

    reflect(1,0)

    translate(105, -65)
    shear(0.2,0.2)
    translate(-105, 65)

    draw_bus.draw_bus()
    set_color("blue")
    draw_rect_text(0,0,210,130,"This is a very good day!")
    pause()
    close_graph()

easy_run(main)