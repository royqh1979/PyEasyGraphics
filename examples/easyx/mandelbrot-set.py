# demo from EasyX Library
# Mandelbrot Set
# https://codebus.cn/yangw/post/mandelbrot-set

from easygraphics import *

def main():
    width=800
    height=600
    init_graph(width,height)

    for x in range(width):
        for y in range(height):
            c=complex(-2.1 + (1.1- -2.1)*(x/width),
                      -1.2+(1.2- -1.2)*(y/height))
            z=complex(0,0)
            k=0
            while k<180:
                if (z.real*z.real+z.imag*z.imag)>4:
                    break
                z = z*z+c
                k+=1
            if k>=180:
                put_pixel(x,y,Color.BLACK)
            else:
                put_pixel(x,y,color_hsl((k<<5) % 360,255,127))

    pause()
    close_graph()

easy_run(main)
