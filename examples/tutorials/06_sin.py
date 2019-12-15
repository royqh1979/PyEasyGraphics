"""
Use the current position to draw a dash line
"""
from easygraphics import *
import math as m

def main():
    init_graph(600, 400)
    translate(300, 200)  # move origin to the center
    scale(100, -100)  # zoom each axis 100 times, and make y-axis grow from bottom to top.

    x = -3
    delta = 0.01
    move_to(x, m.sin(x))
    while x <= 3:
        line_to(x, m.sin(x))
        x = x + delta
    pause()
    close_graph()

easy_run(main)