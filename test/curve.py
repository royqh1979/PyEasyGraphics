from easygraphics import *

init_graph(400, 400)
scale(4, 4)
set_color(color_rgb(255, 102, 0))
draw_curve(5, 26, 5, 26, 73, 24, 73, 61)
set_color("black")
draw_curve(5, 26, 73, 24, 73, 61, 15, 65)
set_color(color_rgb(255, 102, 0))
draw_curve(73, 24, 73, 61, 15, 65, 15, 65)
pause()
close_graph()
