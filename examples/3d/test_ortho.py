from easygraphics import *
from easygraphics.utils3d import ortho_look_at, isometric_projection
from PyQt5.QtGui import QVector3D
import math


def get_vector(degree1, degree2, length):
    rad = math.radians(degree1)
    p_len = length * math.cos(rad)
    h_len = length * math.sin(rad)
    rad2 = math.radians(degree2)
    len_x = p_len * math.cos(rad2)
    len_y = p_len * math.sin(rad2)
    return QVector3D(len_x, len_y, h_len)


init_graph(800, 600)
translate(400, 300)
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

degree = 120
degree2 = 45
eye = get_vector(degree, degree2, 1)
up = get_vector(degree + 90, degree2, 1)

print(eye)
print(up)
# matrix_ortho = ortho_look_at(eye.x(), eye.y(), eye.z(),
#                              up.x(), up.y(), up.z())
matrix_ortho = isometric_projection()

points = []
for p_3d in points_3d:
    x, y, z = p_3d
    v = QVector3D(x, y, z)
    v_2 = matrix_ortho.map(v)
    print((x, y, z), '-->', (v_2.x(), v_2.y()))
    points.append((v_2.x(), v_2.y()))


def edge(i, j, color):
    set_color(color)
    x1, y1 = points[i - 1]
    x2, y2 = points[j - 1]
    line(x1, y1, x2, y2)


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

pause()
close_graph()
