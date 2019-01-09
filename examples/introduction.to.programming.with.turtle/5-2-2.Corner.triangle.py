from easygraphics.turtle import *


def corner_tri(size, level):
    if level == 0:
        return
    for i in range(3):
        fd(size)
        corner_tri(size / 2, level - 1)
        rt(120)


create_world(800, 600)
set_speed(100)

setxy(-200, -200)

corner_tri(240, 5)

pause()
close_world()
