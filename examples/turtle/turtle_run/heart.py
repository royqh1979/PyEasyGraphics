"""
Draw two hearts
"""
from easygraphics import *
from easygraphics.turtle import *


def big_Circle(size):
    # 函数用于绘制心的大圆
    for i in range(150):
        forward(size)
        rt(0.3)


def small_Circle(size):
    # 函数用于绘制心的小圆
    for i in range(210):
        forward(size)
        rt(0.786)


def line(size):
    forward(51 * size)


def heart(x, y, size):
    setxy(x, y)
    set_heading(90)
    lt(60)
    begin_fill()
    forward(51 * size)
    big_Circle(size)
    small_Circle(size)
    lt(120)
    small_Circle(size)
    big_Circle(size)
    line(size)
    lt(120)
    end_fill()


def arrow():
    set_pen_size(5)
    set_heading(0)
    setxy(-400, 0)
    left(15)
    pen_up()
    forward(20)
    pen_down()
    forward(250)
    setxy(339, 178)
    back(66)
    setxy(339, 178)


def arrowHead():
    x = get_x()
    y = get_y()
    set_pen_size(1)
    set_color('red')
    set_fill_color("red")
    begin_fill()
    forward(20)
    right(150)
    forward(35)
    right(120)
    end_fill()
    setxy(x, y)
    set_heading(15)
    begin_fill()
    forward(20)
    left(150)
    forward(35)
    left(120)
    end_fill()


def main():
    create_world(800, 600)

    set_color('red')
    set_fill_color('pink')

    set_speed(100)

    heart(150, 0, 0.9)

    heart(-80, -100, 1.4)

    arrow()

    arrowHead()

    hide()
    pause()
    close_world()

easy_run(main)