"""
Draw a rectangle with custom line shape.
"""
from easygraphics import *

def main():
    init_graph(400, 300)
    set_line_width(10)
    target_image = get_target()
    pen = target_image.get_pen()
    pen.setDashPattern([1, 5, 2, 5])
    draw_rect(50, 50, 350, 250)
    pause()
    close_graph()

easy_run(main)