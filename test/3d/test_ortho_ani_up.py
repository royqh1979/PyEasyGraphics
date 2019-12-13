from easygraphics import *
from PyQt5.QtGui import QVector3D, QMatrix4x4
import math


def edge(i, j, color):
    global points
    set_color(color)
    x1, y1 = points[i - 1]
    x2, y2 = points[j - 1]
    line(x1, y1, x2, y2)


def main():
    global points
    init_graph(800, 600)
    set_render_mode(RenderMode.RENDER_MANUAL)
    translate(400, 300)
    set_flip_y(True)
    scale(100, 100)
    points_3d = []
    points_3d.append((0, 0, 0))
    points_3d.append((1, 0, 0))
    points_3d.append((0, 1, 0))
    points_3d.append((1, 1, 0))
    points_3d.append((0, 0, 1))
    points_3d.append((1, 0, 1))
    points_3d.append((0, 1, 1))
    points_3d.append((1, 1, 1))

    points = []
    degree = -1
    length = 1

    eye = QVector3D(1, 1, 1)
    right = QVector3D(-1, 1, 0)
    up_base = QVector3D.crossProduct(eye, right)
    # print(up_base)

    while is_run():
        clear()
        degree += 1

        rotate_m = QMatrix4x4()
        rotate_m.rotate(degree, eye)
        up = rotate_m.map(up_base)
        # up = up_base
        # print(degree)

        matrix_ortho = ortho_look_at(eye.x(), eye.y(), eye.z(),
                                     0, 0, 0,
                                     up.x(), up.y(), up.z())

        points.clear()
        for p_3d in points_3d:
            x, y, z = p_3d
            v = QVector3D(x, y, z)
            v_2 = matrix_ortho.map(v)
            points.append((v_2.x(), v_2.y()))

        set_color("lightgray")
        line(-400, 0, 400, 0)
        line(0, -300, 0, 300)
        edge(1, 2, "red")
        edge(2, 4, "yellow")
        edge(3, 4, "blue")
        edge(1, 3, "green")
        edge(5, 6, "lightred")
        edge(6, 8, "lightyellow")
        edge(7, 8, "lightblue")
        edge(5, 7, "lightgreen")
        edge(1, 5, "black")
        edge(2, 6, "black")
        edge(3, 7, "black")
        edge(4, 8, "black")
        delay(10)

    pause()
    close_graph()

easy_run(main)