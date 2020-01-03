"""
Interference and moire pattern

Adapted form "Processing Creative Coding and Computational Art", Page 134.
"""
import math

from easygraphics import *

def main():
    init_graph(400, 400)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_background_color("black")
    set_color("white")

    interval = get_width() * 0.03
    spacer = interval

    angle = 0
    y = 0
    amplitude = 0.05
    wave_gap = 10
    frequency = 0.1
    ring_growth_rate = 0.5
    is_inactive = True
    while is_run():
        if has_mouse_msg():
            msg = get_mouse_msg()
            if msg.type == MouseMessageType.PRESS_MESSAGE:
                is_inactive = False
            elif msg.type == MouseMessageType.RELEASE_MESSAGE:
                is_inactive = True
        if is_inactive:
            if spacer > interval:
                spacer -= ring_growth_rate
        else:
            angle = 0
            if spacer < interval * 2:
                spacer += ring_growth_rate
        if delay_jfps(30):
            clear_device()
            py = 0
            for i in range(0, get_height(), wave_gap):
                for j in range(get_width()):
                    mouse_x, mouse_y = get_cursor_pos()
                    py = i + math.sin(math.radians(angle)) * mouse_y * amplitude
                    draw_point(j, py)
                    angle += mouse_x * frequency
            i = 0
            while i < get_width() / 2 * spacer / interval:
                ellipse(mouse_x, mouse_y, (10 + i) / 2, (10 + i) / 2)
                i += spacer

    close_graph()

easy_run(main)