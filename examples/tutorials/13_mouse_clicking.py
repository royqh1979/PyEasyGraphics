from easygraphics import *

init_graph(800, 600)
set_render_mode(RenderMode.RENDER_MANUAL)

while is_run():
    x, y, buttons = get_click()
    str = "clicked on %d,%d ." % (x, y)
    if contains_left_button(buttons):
        str += " left button down"
    if contains_right_button(buttons):
        str += " right button down"
    if contains_mid_button(buttons):
        str += " mid button down"
    clear_device()
    draw_text(0, 600, str)

close_graph()
