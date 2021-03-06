from easygraphics import *

def main():
    init_graph(800, 600)
    set_render_mode(RenderMode.RENDER_MANUAL)

    set_fill_color("white")
    while is_run():
        x, y = get_cursor_pos()
        fill_rect(0, 580, 390, 600)
        draw_text(0, 600, "%d,%d" % (x, y))
        if has_mouse_msg():
            msg = get_mouse_msg()
            if msg.type == MouseMessageType.PRESS_MESSAGE:
                typestr = "pressed"
            elif msg.type == MouseMessageType.RELEASE_MESSAGE:
                typestr = "released"
            fill_rect(400, 580, 800, 600)
            draw_text(400, 600, "button %s at %d,%d" % (typestr, x, y))
        delay_fps(30)

    close_graph()

easy_run(main)