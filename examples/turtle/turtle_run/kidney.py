import math

from easygraphics import *
from easygraphics.turtle import *

create_world()

set_speed(1000);
set_color("red")

R = 100

a = 0
while a <= 2 * math.pi:
    x = 400 + R * math.cos(a)
    y = R * math.sin(a)
    r = math.fabs(400 - x)
    s = 2 * math.pi * r / 360
    pu()
    fd(y)
    pd()
    for i in range(1, 361):
        fd(s)
        if 400 > x:
            lt(1)
        else:
            rt(1)
    pu()
    bk(y)
    pd()
    a += math.pi / 30

pause()
close_world()
