from easygraphics.turtle import *
from easygraphics import *
import math
import sys


def distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.hypot(dx, dy)


def factor(x, y):
    d = distance(get_x(), get_y(), x, y)
    if d < 1:
        return 1
    return 1 / d


def vary_step(x, y, side, angle):
    while is_run():
        fd(factor(x, y) * side)
        lt(angle)


def vary_turn(x, y, side, angle):
    while is_run():
        fd(side)
        lt(factor(x, y) * angle);

def main():
    create_world(1024, 768)
    set_speed(100)
    setxy(100, 100)
    set_fill_color("red")
    fill_circle(0, 0, 4)
    # vary_step(0,0,1500,10)
    vary_turn(0, 0, 10, 2000)

    pause()
    close_world()

easy_run(main)