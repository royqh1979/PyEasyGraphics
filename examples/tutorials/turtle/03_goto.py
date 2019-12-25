from easygraphics.turtle import *


def main():
    create_world(300, 300)
    gotoxy(50, -100)
    for i in range(360):
        fd(1)
        lt(1)
    pause()
    cs()
    setxy(50, -100)
    for i in range(360):
        fd(1)
        lt(1)

    pause()
    close_world()


easy_run(main)
