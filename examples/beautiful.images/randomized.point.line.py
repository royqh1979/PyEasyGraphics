"""

Adapted from "Processing Creative Coding and Computational Art",Chapter 6, Page 181
"""

from easygraphics import *
import random


def main():
    init_graph(600, 300)
    width = get_width()
    height = get_height()
    set_background_color('black')
    clear_device()
    set_color('white')

    random.seed()

    rand = 0

    for i in range(width):
        draw_point(i, height / 2 + random.uniform(-rand, rand))
        rand += random.uniform(-5, 5)

    pause()
    close_graph()


easy_run(main)
