# a demo program from easyX Library
# It demostrates the use of HSL colorspace
# https://codebus.cn/yangw/post/rainbow

from easygraphics import *

def main():
    init_graph(640,480)

    # open anti aliasing
    set_antialiasing(True)

    # draw a sky by gradient color (through lightness change)
    H = 190     # Hue
    S = 1       # Saturation
    L = 0.7     # Lightness
    for y in range(480):
        L += 0.0005
        set_color(color_hsl(H,S*255,L*255))
        line(0,y,get_width(),y)

    # draw a rainbow by gradient color (throuth hue change)
    H=0
    S=1
    L=0.5
    for r in range(400,344,-1):
        H += 5
        set_color(color_hsl(H,S*255,L*255))
        circle(500,480,r)

    pause()
    close_graph()

easy_run(main)