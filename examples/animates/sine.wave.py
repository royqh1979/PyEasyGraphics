"""
Sine Wave

The original program is from https://processing.org/examples/sinewave.html
"""
from easygraphics import *
import math

x_spacing = 16  # How far apart should each horizontal location be spaced
theta = 0  # Start angle at 0
amplitude = 75  # Height of wave
period = 500  # How many pixels before the wave repeats

init_graph(640, 360)
set_render_mode(RenderMode.RENDER_MANUAL)

translate(0, get_height() // 2)

w = get_width() + 16  # Width of entire wave
dx = (2 * math.pi / period) * x_spacing

set_background_color("black")
set_fill_color("white")
while is_run():
    theta += 0.02
    if delay_jfps(60):
        clear_device()
        x = theta
        for i in range(w // x_spacing):
            y = math.sin(x) * amplitude
            fill_circle(i * x_spacing, y, 8)
            x += dx

close_graph()
