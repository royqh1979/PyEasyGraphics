from easygraphics import *

init_graph(800, 600)
set_render_mode(RenderMode.RENDER_MANUAL)
set_fill_color("red")
set_background_color("black")
t = 0
while is_run():
    t = t + 1
    t = t % 350
    clear()
    push_transform()
    translate(400, 300)
    rotate(t)
    begin_shape()
    for i in range(5):
        vertex(100, 0)
        rotate(144)
    end_shape()
    pop_transform()
    delay_fps(60)

close_graph()
