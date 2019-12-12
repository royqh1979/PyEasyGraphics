from easygraphics.turtle import *


def inspi(side, angle, inc):
    while is_run():
        fd(side)
        rt(angle)
        angle += inc;


create_world(800, 600)
set_speed(1000)

# inspi(15,0,7)
# inspi(50,40,30)
inspi(50, 2, 20)

close_world()
