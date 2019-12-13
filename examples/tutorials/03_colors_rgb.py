"""
Use predefined colors

In this example, we use rgb() and RGB values 255,0,0 to get red color.

"""
from easygraphics import *

def main():
    init_graph(640, 480)

    # set color to read 将色彩设为红色
    set_color(rgb(255, 0, 0))

    draw_circle(300, 200, 100)
    pause()

easy_run(main)