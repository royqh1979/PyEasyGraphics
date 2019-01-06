from easygraphics import *
from easygraphics.turtle import *

create_world()
set_color("red")
set_fill_color("red")
set_fill_rule(FillRule.WINDING_FILL)
begin_fill()
for i in range(5):
    forward(100)
    right(144)
end_fill()
