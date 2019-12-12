from easygraphics.turtle import *


def outward_tri(size, level):
    if level == 0:
        return
    for i in range(3):
        forward(size / 2)
        lt(120)
        outward_tri(size / 2, level - 1)
        rt(120)
        forward(size / 2)
        rt(120)

def main():
    create_world(800, 600)
    set_speed(100)
    outward_tri(100, 4)
    pause()
    close_world()

easy_run(main)