"""
Rainbow

From "Math Adventures with Python" Part II, Chapter 5, "Drawing Complex Patterns Using Triangles"
"""
import sys

from easygraphics import *
import math
import random


def triangle(size):
    """
    Draw an equilateral triangle

    :param size:
    """
    size_b = size * math.sqrt(3) / 2
    size_c = size / 2
    polygon(0, -size, -size_b, size_c, size_b, size_c)

def main():
    random.seed()
    width = 800
    height = 600
    init_graph(width, height)
    set_render_mode(RenderMode.RENDER_MANUAL)
    translate(width / 2, height / 2)

    t = 0
    while is_run():
        t = random.randrange(0, 255)
        for i in range(90):
            if delay_jfps(60):
                rotate(360 / 90)
                push_transform()
                c = color_hsv((t + i * 255 / 90) % 255, 255, 255)
                set_color(c)
                translate(200, 0)
                rotate(2 * i * 360 / 90)
                triangle(100)
                pop_transform()

    close_graph()

easy_run(main)