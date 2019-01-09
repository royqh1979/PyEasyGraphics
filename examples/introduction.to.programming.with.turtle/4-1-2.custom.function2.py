from easygraphics.turtle import *


def arcl(side, degree):
    for i in range(degree):
        fd(side)
        lt(1)


def arcr(side, degree):
    for i in range(degree):
        fd(side)
        rt(1)


create_world(800, 600)

set_speed(50)

for i in range(9):
    arcr(1, 360)
    rt(40)

pause()
close_world()
