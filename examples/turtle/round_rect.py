from easygraphics import *
from easygraphics.turtle import *

create_world(800, 600)
set_speed(20)
set_color("blue")
set_fill_color("lightpink")
begin_fill()
for i in range(4):
    move_arc(10, 90)
    fd(100)
end_fill()
pause()
close_world()
