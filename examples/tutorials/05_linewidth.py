"""
Draw a rectangle with thick borders.
"""
from easygraphics import *

def main():
    init_graph(400, 300)
    set_line_width(10)
    draw_rect(50, 50, 350, 250)
    pause()
    close_graph()

easy_run(main)