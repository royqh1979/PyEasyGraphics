"""
A Morphing star
"""
import math

from easygraphics import *

init_graph(400, 400)
set_render_mode(RenderMode.RENDER_MANUAL)
translate(200, 200)

num = 0
size = 100
points = []
pi_5th = math.pi / 5
pi_2_5th = 2 * pi_5th
while is_run():
    clear()
    points.clear()
    num += 1
    rad = math.radians(num)
    x = size * math.cos(rad)
    y = size * math.sin(rad)
    x1 = x * math.cos(pi_5th) - y / 2 * math.sin(pi_5th)
    y1 = x * math.sin(pi_5th) + y / 2 * math.cos(pi_5th)
    points.append(x)
    points.append(y)
    points.append(x1)
    points.append(y1)
    for i in range(1, 5):
        x2 = x * math.cos(i * pi_2_5th) - y * math.sin(i * pi_2_5th)
        y2 = x * math.sin(i * pi_2_5th) + y * math.cos(i * pi_2_5th)
        x3 = x1 * math.cos(i * pi_2_5th) - y1 * math.sin(i * pi_2_5th)
        y3 = x1 * math.sin(i * pi_2_5th) + y1 * math.cos(i * pi_2_5th)
        points.append(x2)
        points.append(y2)
        points.append(x3)
        points.append(y3)
    draw_polygon(*points)
    delay_fps(60)

close_graph()
