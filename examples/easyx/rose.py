# https://codebus.cn/zhaoh/post/roses-for-valentine-s-day
# http://www.romancortes.com/blog/1k-rose/
import random
from math import sin,cos,pow

from easygraphics import *
from dataclasses import dataclass
import numpy as np

rosesize = 500
h = -250

@dataclass
class DOT:
    x:float
    y:float
    z:float
    red: float
    green: float
    # blue calculated using red

def calc(a:float,b:float,c:float)->DOT:
    if c>60: # 花柄
        d = DOT(
            sin(a*7)*(13+5/(0.2+pow(b*4,4)))-sin(b)*50,
            b * rosesize + 50,
            625 + cos(a * 7) * (13 + 5 / (0.2 + pow(b * 4, 4))) + b * 400,
            a * 1 - b / 2,
            a
        )
        return d

    A = a*2-1
    B = b*2-1
    if (A*A + B*B<1):
        if c>37: # Leaves
            j = int(c) & 1
            n = 6 if j==1 else 4
            o = 0.5 / (a + 0.01) + cos(b * 125) * 3 - a * 300
            w = b * h

            d=DOT(
                o * cos(n) + w * sin(n) + j * 610 - 390,
                o * sin(n) - w * cos(n) + 550 - j * 350,
                1180 + cos(B + A) * 99 - j * 300,
                0.4 - a * 0.1 + pow(1 - B * B, -h * 6) * 0.15 - a * b * 0.4 + cos(a + b) / 5
                    + pow(cos((o * (a + 1) + (w if B>0 else -w)) / 25), 30) * 0.1 * (1 - B * B),
                o / 1000 + 0.7 - o * w * 0.000003
            )
            return d
        elif c>32: # 花萼
            c = c * 1.16 - 0.15
            o = a * 45 - 20
            w = b * b * h
            z = o * sin(c) + w * cos(c) + 620

            d=DOT(
                o * cos(c) - w * sin(c),
                28 + cos(B * 0.5) * 99 - b * b * b * 60 - z / 2 - h,
                z,
                (b * b * 0.3 + pow((1 - (A * A)), 7) * 0.15 + 0.3) * b,
              b * 0.7
            )
            return d

        # 花
        o = A * (2 - b) * (80 - c * 2)
        w = 99 - cos(A) * 120 - cos(b) * (-h - c * 4.9) + cos(pow(1 - b, 7)) * 50 + c * 2
        z = o * sin(c) + w * cos(c) + 700

        d = DOT(
            o * cos(c) - w * sin(c),
            B * 99 - cos(pow(b, 7)) * 50 - c / 3 - z / 1.35 + 450,
            z,
            (1 - b / 1.2) * 0.9 + a * 0.1,
            pow((1 - b), 20) / 4 + 0.05
        )
        return d
    return None

def main():
    init_graph(640,480)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_background_color(Color.WHITE)

    zBuffer = np.zeros((rosesize,rosesize))

    while is_run():
        for i in range(10000):
            dot = calc( random.random(),random.random(),random.randrange(46)/0.74)
            if dot is None:
                continue
            z = int(dot.z+0.5)
            x = int(dot.x*rosesize/z-h+0.5)
            y = int(dot.y*rosesize/z-h+0.5)
            if y>=rosesize:
                continue
            if zBuffer[x,y]==0 or zBuffer[x,y]>z:
                zBuffer[x,y]=z
                r=~int(dot.red*h)
                if r<0:
                    r=0
                elif r>255:
                    r=255
                g=~int(dot.green*h)
                if g<0:
                    g=0
                elif g>255:
                    g=255
                b=~int(dot.red*dot.red*-80)
                if b<0:
                    b=0
                elif b>255:
                    b=255
                put_pixel(x+50,y-20,rgb(r,g,b))
        delay(1)
    close_graph()

easy_run(main)