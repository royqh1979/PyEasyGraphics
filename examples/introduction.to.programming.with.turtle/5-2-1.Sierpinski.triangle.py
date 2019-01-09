from easygraphics.turtle import *


def nest_tri(size, level):
    if level == 0:
        return
    for i in range(3):
        nest_tri(size / 2, level - 1)
        fd(size)
        rt(120)


create_world(800, 600)
set_speed(1000)

setxy(-200, -150)
rt(30)

nest_tri(400, 7)

pause()
close_world()
