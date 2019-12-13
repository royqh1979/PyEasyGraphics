from easygraphics.turtle import *

create_world(800, 600)

set_speed(500)

for k in range(8):
    for j in range(6):
        for i in range(60):
            fd(1)
            rt(1)
        rt(120)
        for i in range(60):
            fd(1)
            rt(1)
        rt(120)
        rt(60)

    for i in range(45):
        fd(3)
        lt(1)

pause()
close_world()
