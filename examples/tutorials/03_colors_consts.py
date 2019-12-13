"""
Use predefined colors

In this example, we use defined RED const to get red color.

"""
from easygraphics import *

def main():
    init_graph(640, 480)

    # set color to read 将色彩设为红色
    set_color(Color.RED)

    draw_circle(300, 200, 100)
    pause()

easy_run(main)