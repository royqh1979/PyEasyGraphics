from easygraphics.turtle import *


def subspiro(side, angle, n):
    for i in range(n):
        fd(side * i)
        rt(angle)


def spiro(side, angle, n):
    while is_run():
        subspiro(side, angle, n)


create_world(800, 600)
set_speed(100)

# spiro(30,90,10)
spiro(20, 144, 8)
# spiro(20,60,10)

close_world()
