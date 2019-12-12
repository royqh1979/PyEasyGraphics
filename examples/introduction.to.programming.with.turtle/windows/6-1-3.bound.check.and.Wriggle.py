from easygraphics.turtle import *
from easygraphics import *
import random


def check_forward(distance):
    x = get_x()
    y = get_y()
    set_immediate(True)
    pu()
    hide()
    fd(distance)
    forward_failed = is_out_of_window()
    setxy(x, y)
    pd()
    show()
    set_immediate(False)
    if not forward_failed:
        fd(distance)
    return forward_failed


def wriggle():
    while is_run():
        rt(1)
        forward_failed = check_forward(1)
        if not forward_failed:
            break


def random_move(d1, d2, a1, a2):
    while is_run():
        lt(random.randint(a1, a2))
        forward_failed = check_forward(random.randint(d1, d2))
        if forward_failed:
            wriggle()


create_world(800, 600)
set_speed(10)
random.seed()

# random_move(1,10,0,10)
# random_move(1,10,-10,5)
random_move(1, 10, -10, 10)

pause()
close_world()
