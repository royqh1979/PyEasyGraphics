from easygraphics import *

def main():
    init_graph(800, 600)
    set_render_mode(RenderMode.RENDER_MANUAL)

    while is_run():
        msg = get_click()
        str = "clicked on %d,%d ." % (msg.x, msg.y)
        clear_device()
        draw_text(0, 600, str)

    close_graph()

easy_run(main)