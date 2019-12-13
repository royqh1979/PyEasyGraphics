"""
Use predefined colors

In this example, we use rgb integer (0xff0000) to get red color.

"""
from easygraphics import *

def main():
    init_graph(640, 480)

    # set color to read 将色彩设为红色
    set_color(0xff0000)

    draw_circle(300, 200, 100)
    pause()

easy_run(main)