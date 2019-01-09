from easygraphics.turtle import *

create_world(800, 600)
set_speed(400)

for i in range(6):
    for j in range(60):
        fd(3)
        rt(1)
    rt(120)
    for j in range(60):
        fd(3)
        rt(1)
    rt(120)
    rt(60)
pause()
close_world()
