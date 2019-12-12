from easygraphics.turtle import *


def inner_tri(size, level):
    if level == 0:
        return
    fd(size / 2)
    rt(60)
    inner_tri(size / 2, level - 1)
    lt(60)
    fd(size / 2)

    rt(120)
    fd(size)
    rt(120)
    fd(size)
    rt(120)

def main():
    create_world(800, 600)
    set_speed(100)

    setxy(-300, -250)
    rt(30)

    inner_tri(600, 6)

    pause()
    close_world()

easy_run(main)