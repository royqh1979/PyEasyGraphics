from easygraphics.turtle import *
from easygraphics import *

def main():
    create_world(400, 300)
    set_speed(5)

    lt(45)

    set_fill_color(Color.LIGHT_RED)
    begin_fill()
    fd(100)
    lt(90)
    move_ellipse(100, 50, 90)
    lt(90)
    fd(50)
    lt(90)
    end_fill()

    begin_fill()
    fd(100)
    rt(90)
    move_ellipse(-100, 50, 90)
    rt(90)
    fd(50)
    rt(90)
    end_fill()

    begin_fill()
    bk(100)
    rt(90)
    move_ellipse(100, 50, -90)
    rt(90)
    bk(50)
    rt(90)
    end_fill()

    begin_fill()
    bk(100)
    lt(90)
    move_ellipse(-100, 50, -90)
    lt(90)
    bk(50)
    lt(90)
    end_fill()

    pause()

    close_world()

easy_run(main)