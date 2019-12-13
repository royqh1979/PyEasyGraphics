from easygraphics.turtle import *

create_world(800, 600)

set_speed(1)

move_ellipse(200, 140, 60)
pen_up()
home()
pen_down()
move_arc(200, 60)
lt(90)
fd(200)
lt(120)
fd(200)
lt(90)
move_ellipse(200, 300, 60)
gotoxy(-200, 0)

pause()
close_world()
