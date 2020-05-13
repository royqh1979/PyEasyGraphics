"""
Rainbow

From "Math Adventures with Python" Part II, Chapter 5, "Creating an interactive Rainbow Grid"
"""
from easygraphics import *
import math

def main():
    init_graph(600, 600)

    set_render_mode(RenderMode.RENDER_MANUAL)

    while is_run():
        cursor_x, cursor_y = get_cursor_pos()
        for x in range(30):
            for y in range(30):
                dist = math.hypot(20 * x - cursor_x, 20 * y - cursor_y)
                c = color_hsv(min(dist * 0.5, 255), 255, 255)
                set_fill_color(c)
                draw_rect(x * 20, y * 20, x * 20 + 18, y * 20 + 18)
        delay_fps(60)

    pause()
    close_graph()

easy_run(main)
