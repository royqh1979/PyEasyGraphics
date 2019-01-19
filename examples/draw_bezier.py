"""
The following program draws a bezier curve interactively

First click on the window to set the first control point of the curve.
Then click on the window to set the second control point of the curve.
Then drag from any of the above two control points to set the third and the fourth control point.

"""
if __name__ == "__main__":
    from easygraphics import *
    from PyQt5 import QtCore

    init_graph(800, 600)
    set_render_mode(RenderMode.RENDER_MANUAL)

    x1, y1, buttons = get_click()
    circle(x1, y1, 3)
    x2, y2, buttons = get_click()
    circle(x2, y2, 3)
    line(x1, y1, x2, y2)

    x3, y3 = x1, y1
    x4, y4 = x2, y2
    reg1 = QtCore.QRect(x1 - 2, y1 - 2, 5, 5)
    reg2 = QtCore.QRect(x2 - 2, y2 - 2, 5, 5)
    draging_which_point = 0
    while is_run():
        if draging_which_point == 1:
            draw_line(x1, y1, x, y)
            draw_bezier(x1, y1, x, y, x4, y4, x2, y2)
        elif draging_which_point == 2:
            draw_line(x2, y2, x, y)
            draw_bezier(x1, y1, x3, y3, x, y, x2, y2)

        if has_mouse_msg():
            x, y, type, buttons = get_mouse_msg()
            if type == MouseMessageType.PRESS_MESSAGE:
                if reg1.contains(x, y):
                    draging_which_point = 1
                    set_color(Color.WHITE)
                    set_composition_mode(CompositionMode.SRC_XOR_DEST)
                    x, y = x3, y3
                elif reg2.contains(x, y):
                    draging_which_point = 2
                    set_color(Color.WHITE)
                    set_composition_mode(CompositionMode.SRC_XOR_DEST)
                    x, y = x4, y4
                else:
                    draging_which_point = 0
            elif type == MouseMessageType.RELEASE_MESSAGE:
                if draging_which_point == 1:
                    x3, y3 = x, y
                elif draging_which_point == 2:
                    x4, y4 = x, y
                draging_which_point = 0

                set_color(Color.BLACK)
                set_composition_mode(CompositionMode.SOURCE)
                clear_device()
                draw_line(x1, y1, x3, y3)
                draw_line(x2, y2, x4, y4)
                circle(x1, y1, 3)
                circle(x2, y2, 3)
                draw_bezier(x1, y1, x3, y3, x4, y4, x2, y2)

        else:
            if draging_which_point == 1:
                x, y = get_cursor_pos()
                draw_line(x1, y1, x, y)
                draw_bezier(x1, y1, x, y, x4, y4, x2, y2)
            elif draging_which_point == 2:
                x, y = get_cursor_pos()
                draw_line(x2, y2, x, y)
                draw_bezier(x1, y1, x3, y3, x, y, x2, y2)
        delay_fps(60)

    close_graph()
