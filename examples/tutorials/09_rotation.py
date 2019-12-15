"""
Draw a bus without transformations
"""
from easygraphics import *
import draw_bus

def main():
    init_graph(500, 300)

    # rotate around the (105,65)
    rotate(-45, 105, 65)

    draw_bus.draw_bus()
    pause()
    close_graph()

easy_run(main)