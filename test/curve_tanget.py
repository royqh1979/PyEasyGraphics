import math

from easygraphics import *

def main():
    init_graph(200,100)
    curve(5, 26, 73, 24, 73, 61, 15, 65)

    steps = 6
    for i in range(steps+1):
        t = i / steps
        x = curve_point(5, 73, 73, 15, t)
        y = curve_point(26, 24, 61, 65, t)
        tx = curve_tangent(5, 73, 73, 15, t)
        ty = curve_tangent(26, 24, 61, 65, t)
        a = math.atan2(ty,tx)
        a -= math.pi/2
        line(x,y,math.cos(a)*8+x,math.sin(a)*8+y)

    pause()
    close_graph()

easy_run(main)