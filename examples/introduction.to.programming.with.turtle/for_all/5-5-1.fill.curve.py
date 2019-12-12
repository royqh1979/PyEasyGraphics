from easygraphics.turtle import *


def Fill(size, level):
    if level == 0:
        fd(size)
        return
    Fill(size / 3, level - 1)
    lt(90)
    Fill(size / 3, level - 1)
    for i in range(3):
        rt(90)
        Fill(size / 3, level - 1)
    for i in range(3):
        lt(90)
        Fill(size / 3, level - 1)
    rt(90)
    Fill(size / 3, level - 1)

def main():
    create_world(800, 600)
    set_speed(500)

    setxy(0, -200)

    Fill(400, 4);

    pause()
    close_world()

easy_run(main)