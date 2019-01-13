"""
Sine Waves

From "Math Adventures with Python" Part II, Chapter 6, "Making Sine Waves"
"""
from easygraphics import *
import math

width = 800
height = 400

init_graph(width, height)

set_render_mode(RenderMode.RENDER_MANUAL)

translate(150, height // 2)

circle_list = []
r1 = 100  # radius of the circle
r2 = 5  # radius of the point on the circle outline
t = 0
while is_run():
    t += 0.05
    if delay_jfps(60):
        clear_device()
        set_color("black")
        circle(0, 0, r1)  # draw circle

        # point on the circle outline
        x = r1 * math.sin(t)
        y = r1 * math.cos(t)
        set_fill_color("red")
        draw_circle(x, y, r2)

        # line to the wave
        set_color("green")
        set_fill_color("green")
        line(x, y, 200, y)
        fill_circle(200, y, r2)

        circle_list = [y] + circle_list[:500]

        for i in range(1, len(circle_list)):
            line(200 + i - 1, circle_list[i - 1], 200 + i, circle_list[i])

close_graph()
