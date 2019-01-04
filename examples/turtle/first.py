from easygraphics import *
from easygraphics.turtle import *

create_world(800, 600)

set_color("red")
set_fill_color("lightyellow")

begin_fill()
for i in range(0, 6):
    fd(100)
    lt(60)
end_fill()

pause()
close_world()
