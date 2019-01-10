from easygraphics.turtle import *
import math


def draw_vector(direction, length):
    turn_to(direction)
    fd(length)


def duopoly(side1, angle1, side2, angle2):
    c = 0
    while is_run():
        draw_vector(c * angle1, side1)
        draw_vector(c * angle2, side2)
        c += 1


create_world(800, 600)
set_speed(100)

duopoly(50, 90, 50, 320)
# duopoly(50,90,50,300)
# duopoly(20,10,20,-15)
# duopoly(4,2,8,-2)
# duopoly(100,62,100,300)
# duopoly(20,19,20,-20)
# duopoly(25,45,10,9)
# duopoly(14,32,8,4)

close_world()
