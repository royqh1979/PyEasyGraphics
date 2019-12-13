from easygraphics.turtle import *
import math


def triangle_spiral(side, angle, side2):
    """
    Draw a spiral formed by successive triangles.

    :param side: length of the first triangles's first side
    :param angle:  the angle between the first side and second side
    :param side2: length of the first triangle's second side
    """
    while is_run():
        a = math.pi - math.radians(angle)
        d = math.sqrt(side * side + side2 * side2 - 2 * side * side2 * math.cos(a))
        a2 = math.degrees(math.acos((d * d + side2 * side2 - side * side) / (2 * d * side2)))
        scale = d / side
        fd(side)
        lt(angle)
        fd(side2)
        lt(180 - a2)
        fd(d)
        lt(180)
        side = side * scale;
        side2 = side2 * scale;


create_world(1024, 768)
set_speed(100)
triangle_spiral(1, 90, 0.5);

close_world()
