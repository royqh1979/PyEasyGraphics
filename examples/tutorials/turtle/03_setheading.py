from easygraphics.turtle import *


def main():
    create_world(300, 300)

    # set the turtle's heading to top-left corner of the graphics window
    set_heading(30)
    fd(100)

    pause()
    close_world()


easy_run(main)
