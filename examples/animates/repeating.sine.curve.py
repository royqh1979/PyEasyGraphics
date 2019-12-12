"""
Repeating sine curve

Adapted form "Processing Creative Coding and Computational Art", Page 133.
"""
import math
from easygraphics import *

def main():
    init_graph(400, 400)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_background_color("white")

    angle = 0
    y = 0
    amplitude = 72
    wave_gap = 14
    frequency = 6
    while is_run():
        if y < get_height():
            py = 0
            for i in range(get_width()):
                py = y + math.sin(math.radians(angle)) * amplitude
                draw_point(i, py)
                angle += frequency
            y += wave_gap
        delay_fps(30)

    close_graph()

easy_run(main)