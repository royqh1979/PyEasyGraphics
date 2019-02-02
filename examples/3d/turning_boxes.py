import math

from easygraphics import *
from easygraphics.utils3d import ortho_45
from PyQt5.QtGui import QMatrix4x4, QVector3D
import random


class box:
    def __init__(self, edge_size):
        self.points = []
        self.points.append((-edge_size, -edge_size, -edge_size))
        self.points.append((edge_size, -edge_size, -edge_size))

        self.points.append((-edge_size, edge_size, -edge_size))
        self.points.append((edge_size, edge_size, -edge_size))
        self.points.append((-edge_size, -edge_size, edge_size))
        self.points.append((edge_size, -edge_size, edge_size))
        self.points.append((-edge_size, edge_size, edge_size))
        self.points.append((edge_size, edge_size, edge_size))


def draw_edge(points, i, j):
    x1, y1 = points[i - 1]
    x2, y2 = points[j - 1]
    line(x1, y1, x2, y2)


def draw_box(points):
    draw_edge(points, 1, 2)
    draw_edge(points, 2, 4)
    draw_edge(points, 3, 4)
    draw_edge(points, 1, 3)
    draw_edge(points, 5, 6)
    draw_edge(points, 6, 8)
    draw_edge(points, 7, 8)
    draw_edge(points, 5, 7)
    draw_edge(points, 1, 5)
    draw_edge(points, 2, 6)
    draw_edge(points, 3, 7)
    draw_edge(points, 4, 8)


boxes = []


def init_boxes(numbers):
    for i in range(n):
        boxes.append(box((i + 1) * 4))


n = 50
init_boxes(n)
random.seed()
init_graph(800, 600)
set_color("gray")
translate(400, 300)
set_render_mode(RenderMode.RENDER_MANUAL)
degree = 0
fps = 30
m_o = ortho_45()
points = []

while is_run():
    if random.choice((-1, 1)) == 1:
        clock_wise = True
    else:
        clock_wise = False
    for degree in range(0, 180 + (n) * 5, 5):
        if not is_run():
            break
        clear()
        for i in range(n):
            box = boxes[i]
            dd = max(degree - i * 5, 0)
            dd = min(dd, 180)
            if not clock_wise:
                dd = -dd
            rad = math.radians(dd)
            cos_2 = math.cos(rad)
            sin_2 = math.sin(rad)
            m = QMatrix4x4(cos_2, sin_2, 0, 0,
                           -sin_2, cos_2, 0, 0,
                           0, 0, 1, 0,
                           0, 0, 0, 1)
            points.clear()
            for p in box.points:
                x, y, z = p
                v = QVector3D(x, y, z)
                v2 = m.map(v)
                v3 = m_o.map(v2)
                points.append((v3.x(), v3.y()))
            draw_box(points)
        delay_fps(fps)
    delay(1000)

close_graph()
