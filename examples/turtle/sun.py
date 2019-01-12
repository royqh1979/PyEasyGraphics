from easygraphics import *
from easygraphics.turtle import *
import math

create_world(400, 300)
translate(0, -100)
set_color("red")
set_fill_color("yellow")
set_speed(100)
begin_fill()
while True:
    forward(200)
    left_turn(170)
    if math.hypot(get_x(), get_y()) < 1:
        break
end_fill()
pause()
close_world()
