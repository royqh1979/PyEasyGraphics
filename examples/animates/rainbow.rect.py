from easygraphics import *
import math
import gc
import objgraph

init_graph(600, 600)

while is_run():
    if delay_jfps(30):
        gc.collect()
        cursor_x, cursor_y = get_cursor_pos()
        for x in range(50):
            for y in range(50):
                dist = math.hypot(12 * x - cursor_x, 12 * y - cursor_y)
                c = color_hsv(min(dist * 0.5, 255), 255, 255)
                set_fill_color(c)
                draw_rect(x * 12, y * 12, x * 12 + 10, y * 12 + 10)

pause()
close_graph()
