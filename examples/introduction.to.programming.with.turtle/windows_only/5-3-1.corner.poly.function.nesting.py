from easygraphics.turtle import *


def cor_poly(size, angle):
    if size < 10:
        return
    total_turn = 0
    while total_turn == 0 or total_turn % 360 != 0:
        cor_poly_step(size, angle)
        total_turn += angle;


def cor_poly_step(size, angle):
    fd(size)
    cor_poly(size / 2, -angle)
    rt(angle)


create_world(800, 600)
set_speed(100)

cor_poly(100, 90);
# cor_poly(100,120)
# cor_poly(50,60)
# cor_poly(50,144)

pause()
close_world()
