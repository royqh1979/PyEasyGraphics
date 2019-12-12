from easygraphics.turtle import *
import math


def distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.hypot(dx, dy)


def chamber_spiral(base, s1, s2, a1, a2):
    while is_run():
        lower_left_x = get_x()
        lower_left_y = get_y()
        heading = get_heading()
        fd(base)
        lt(a2)
        fd(s2)
        upper_right_x = get_x()
        upper_right_y = get_y()
        setxy(lower_left_x, lower_left_y)
        set_heading(heading)
        lt(a1)
        fd(s1)

        facing(upper_right_x, upper_right_y)

        new_base = distance(get_x(), get_y(), upper_right_x, upper_right_y);

        scale = new_base / base

        base = new_base
        s1 = s1 * scale
        s2 = s2 * scale

def main():
    create_world(1024, 768)
    set_speed(100)

    chamber_spiral(1, 1, 1.5, 90, 90)

    close_world()

easy_run(main)