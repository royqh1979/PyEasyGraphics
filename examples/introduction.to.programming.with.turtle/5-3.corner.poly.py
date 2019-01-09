from easygraphics.turtle import *


def corner_poly(size, angle, level):
    if level == 0:
        return
    total_turn = 0
    while is_run():
        fd(size)
        corner_poly(size / 2, -angle, level - 1)
        rt(angle)
        total_turn += angle
        if total_turn % 360 == 0:
            break


create_world(800, 600)
set_speed(100)

# corner_poly(100,90,4)
# corner_poly(100,60,3)
corner_poly(100, 120, 4)
# corner_poly(100,144,2)

pause()
close_world()
