from easygraphics.turtle import *
from easygraphics import *
import math
import random


def distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.hypot(dx, dy)


def find_by_smell_ortho(x, y, d1, d2, rand_turn):
    while is_run():
        current_x = get_x()
        current_y = get_y()
        d = distance(current_x, current_y, x, y)
        fill_rect(200, 300, 400, 280)
        draw_text(200, 300, "%.2f,%.2f -- %.2f" % (current_x, current_y, d))
        fd(random.uniform(d1, d2) * d)
        lt(random.uniform(-rand_turn, rand_turn) * d)

def main():
    create_world(800, 600)
    set_speed(100)
    random.seed()

    set_fill_color("red")
    fill_circle(50, 50, 4)
    set_fill_color("white")
    find_by_smell_ortho(50, 50, 0.5, 1, 20);

    close_world()

easy_run(main)