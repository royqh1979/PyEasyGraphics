from easygraphics.turtle import *


def c_curve(size, level):
    if level == 0:
        fd(size)
        return
    c_curve(size, level - 1)
    rt(90)
    c_curve(size, level - 1)
    lt(90)


create_world(800, 600)
set_speed(1000)

pu()
setxy(-100, -100)
pd()
c_curve(10, 10)
hide()
pause()
close_world()
