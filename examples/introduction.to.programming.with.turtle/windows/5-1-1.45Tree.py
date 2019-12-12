from easygraphics.turtle import *


def branch(len, level):
    if level == 0:
        return
    fd(len)
    lt(45)
    branch(len / 2, level - 1)
    rt(90)
    branch(len / 2, level - 1)
    lt(45)
    bk(len)


create_world(800, 600)
set_speed(100)

pu()
bk(200)
pd()
branch(200, 5)

pause()
close_world()
