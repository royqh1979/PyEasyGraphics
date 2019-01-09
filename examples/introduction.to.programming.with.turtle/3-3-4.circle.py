from easygraphics.turtle import *

create_world(800, 600)

size = 3
for i in range(360):
    fd(size)
    rt(1)

pause()
close_world()
