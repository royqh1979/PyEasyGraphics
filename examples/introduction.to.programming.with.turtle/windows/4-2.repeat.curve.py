from easygraphics.turtle import *


def polyspi(side, angle, inc):
    while is_run():
        fd(side)
        rt(angle)
        side += inc


create_world(800, 600)

set_speed(100)

polyspi(0, 117, 5)

close_world()
