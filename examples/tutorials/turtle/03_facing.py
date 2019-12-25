from easygraphics.turtle import *


def main():
    create_world(300, 300)

    # set the turtle heading to top-left corner of the graphics window
    facing(-150, 150)
    fd(100)

    pause()
    close_world()


easy_run(main)
