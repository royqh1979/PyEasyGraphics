from easygraphics.turtle import *


def fill(size, level):
    if level == 0:
        fd(size)
        return
    size_interface = size / pow(3, level)
    fill(size / 3, level - 1)
    lt(45)
    fd(size_interface)
    lt(45)
    fill(size / 3, level - 1)
    for i in range(3):
        rt(45)
        fd(size_interface)
        rt(45)
        fill(size / 3, level - 1)
    for i in range(3):
        lt(45)
        fd(size_interface)
        lt(45)
        fill(size / 3, level - 1)
    rt(45)
    fd(size_interface)
    rt(45)
    fill(size / 3, level - 1)

def main():
    create_world(800, 600)
    set_speed(1000)
    setxy(0, -250)
    fill(200, 4);

    pause()
    close_world()

easy_run(main)