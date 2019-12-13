from easygraphics.turtle import *


def ldragon(size, level):
    if level == 0:
        fd(size)
        return
    ldragon(size, level - 1)
    lt(90)
    rdragon(size, level - 1)


def rdragon(size, level):
    if level == 0:
        fd(size)
        return
    ldragon(size, level - 1)
    rt(90)
    rdragon(size, level - 1)


create_world(800, 600)
set_speed(100)

setxy(200, 0)

ldragon(5, 11)
hide()

pause()
close_world()
