from easygraphics import *
from easygraphics.turtle import *

create_world()
cs()
set_speed(10)
set_fill_color("yellow")
begin_fill()
gotoxy(200, 200)
gotoxy(200, -200)
home()
end_fill()

begin_fill()
setxy(200, 0)

gotoxy(250, 50)

gotoxy(250, -50)

gotoxy(200, 0)
end_fill()

setxy(50, -10)

move_arc(10, 360)

hide()
pause()
close_graph()
