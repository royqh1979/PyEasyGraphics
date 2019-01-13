from easygraphics import *

init_graph(800, 600)
set_render_mode(RenderMode.RENDER_MANUAL)

while is_run():
    if delay_fps(30):
        x, y = get_cursor_pos()
        clear_device()
        draw_text(0, 600, "%d,%d" % (x, y))

close_graph()
