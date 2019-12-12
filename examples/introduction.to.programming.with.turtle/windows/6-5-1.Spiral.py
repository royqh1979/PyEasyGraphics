from easygraphics.turtle import *
import math


def eqspi(size, angle, scale):
    while is_run():
        fd(size)
        lt(angle)
        size = size * scale


create_world(1024, 768)
set_speed(100)

eqspi(1, 1, 1.001)

close_world()
