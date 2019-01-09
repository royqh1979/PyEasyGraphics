from easygraphics.turtle import *
from easygraphics import *
import math
import random


def distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.hypot(dx, dy)


last_x = 0
last_y = 0


def smell(x, y):
    global last_x, last_y
    current_x = get_x()
    curretn_y = get_y()
    if (distance(current_x, curretn_y, x, y) > distance(last_x, last_y, x, y)):
        result = -1
    else:
        result = 1
    last_x = current_x
    last_y = curretn_y
    return result


def find_by_smell(x, y, angle=1):
    while is_run():
        fd(1)
        if smell(x, y) == -1:
            rt(angle)


def find_by_smell2(x, y, d1, d2, smell_turn, rand_turn):
    while is_run():
        fd(random.randint(d1, d2))
        lt(random.randint(-rand_turn, rand_turn))
        if smell(x, y) == -1:
            rt(smell_turn)


create_world(800, 600)
set_speed(100)
random.seed(100)

set_fill_color("red")
fill_circle(200, 200, 4)

# find_by_smell(200,200)
# find_by_smell(200,200,20)
# find_by_smell(200,200,60)
find_by_smell(200, 200, 120)
# find_by_smell2(200,200,1,2,60,10)
# find_by_smell2(200,200,1,2,60,30)
# find_by_smell2(200,200,1,2,60,120)

pause()
close_world()
