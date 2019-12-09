from easygraphics import *

init_graph(400,300)
set_color(Color.BLACK)
set_fill_color(Color.LIGHT_GRAY)
# set the axis origin to (200,150)
translate(200, 150)
begin_shape()
for i in range(5):
    vertex(0,-100)
    rotate(144)
end_shape()
pause()
close_graph()
