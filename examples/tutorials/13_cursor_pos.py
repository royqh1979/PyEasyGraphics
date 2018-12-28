from easygraphics import *

init_graph(800, 600)

while is_run():
    x, y = get_cursor_pos()
    clear_device()
    draw_text(0, 600, "%d,%d" % (x, y))
    delay_fps(30)

close_graph()
