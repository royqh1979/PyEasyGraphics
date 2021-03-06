from easygraphics.turtle import *

def main():
    create_world(400, 300)
    set_speed(10)

    lt(45)

    fd(100)
    lt(90)
    move_arc(100, 90)
    lt(90)
    fd(100)
    lt(90)

    fd(100)
    rt(90)
    move_arc(-100, 90)
    rt(90)
    fd(100)
    rt(90)

    bk(100)
    rt(90)
    move_arc(100, -90)
    rt(90)
    bk(100)
    rt(90)

    bk(100)
    lt(90)
    move_arc(-100, -90)
    lt(90)
    bk(100)
    lt(90)

    pause()

    close_world()

easy_run(main)