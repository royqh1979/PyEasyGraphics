from easygraphics import *
import time

init_graph(640, 480)
set_color(Color.BLUE);
set_fill_color(Color.GREEN);
set_render_mode(RenderMode.RENDER_MANUAL)

x = 0;
while is_run():
    x = (x + 1) % 440;
    if delay_jfps(60, 0):
        clear_device()
        draw_ellipse(x + 100, 200, 100, 100)
        time.sleep(0.5)
close_graph()
