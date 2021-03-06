"""
Draw a bus without transformations
"""
from easygraphics import *
import draw_bus

def main():
    init_graph(500, 300)

    # move the origin to the center of the image
    translate(250, 150)

    # rotate around the bus center
    translate(105, 65)
    rotate(180)
    translate(-105, -65)

    # shear arount the bus center
    translate(105, 65)
    shear(0.5, 0.5)
    translate(-105, -65)

    # scale
    scale(1.2, 1.2)
    draw_bus.draw_bus()
    pause()
    close_graph()

easy_run(main)