from easygraphics import *
from easygraphics.dialog import *

def main():
    init_graph(600, 400)
    set_render_mode(RenderMode.RENDER_MANUAL)

    while is_run():
        if has_mouse_msg():
            x, y, type, buttons, modifiers = get_mouse_msg()
            if type == MouseMessageType.PRESS_MESSAGE:
                color = get_color(get_background_color())
                set_background_color(color)
        delay_fps(60)

    close_graph()

easy_run(main)