from easygraphics.turtle import *
from easygraphics import *


def main():
    create_world(300, 300)

    # set the turtle heading to top-left corner of the graphics window
    facing(-150, 150)
    fd(100)

    draw_text(-140, -130, "(%.2f, %.2f), heading(%.2f)" % (get_x(), get_y(), get_heading()))
    pause()
    close_world()


easy_run(main)
