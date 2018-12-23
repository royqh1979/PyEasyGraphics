if __name__ == "__main__":
    from easygraphics import *
    from PyQt5 import QtCore

    init_graph(800, 600)

    # we must fill the whole foreground with color,
    # otherwise it will be transparent, and composition will not work
    fill_rect(0, 0, get_width(), get_height())

    x1, y1, type, buttons = get_mouse()
    circle(x1, y1, 3)
    set_color(Color.WHITE)
    set_composition_mode(CompositionMode.SRC_XOR_DEST)
    x2, y2 = x1, y1
    while is_run():
        if mouse_msg():
            draw_line(x1, y1, x2, y2)
            x2, y2, type, buttons = get_mouse()
            if type == MouseMessageType.RELEASE_MESSAGE:
                set_color(Color.BLACK)
                set_composition_mode(CompositionMode.SOURCE)
                circle(x2, y2, 3)
                line(x1, y1, x2, y2)
                break
        else:
            draw_line(x1, y1, x2, y2)
            x2, y2 = get_cursor_pos()
            draw_line(x1, y1, x2, y2)
            delay_fps(60)

    pause()
    close_graph()
