"""
Draw a bus without transformations
"""
from easygraphics import *
import draw_bus

def main():
    init_graph(500, 300)

    shear(0.5, 0)
    draw_bus.draw_bus()

    pause()
    close_graph()

easy_run(main)