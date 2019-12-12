from easygraphics.turtle import *


def lbranch(size, angle, level):
    fd(2 * size)
    node(size, angle, level - 1)
    bk(2 * size)


def rbranch(size, angle, level):
    fd(size)
    node(size, angle, level - 1)
    bk(size)


def node(size, angle, level):
    if level == 0:
        return
    lt(angle)
    lbranch(size, angle, level)
    rt(2 * angle)
    rbranch(size, angle, level)
    lt(angle)

def main():
    create_world(800, 600)
    set_speed(100)

    pen_up()
    back(200)
    pen_down()

    lbranch(20, 20, 8)

    pause()
    close_world()

easy_run(main)