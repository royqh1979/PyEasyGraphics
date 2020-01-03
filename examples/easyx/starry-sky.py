# demo program of easyX Library
# from: https://codebus.cn/yangw/post/starry-sky
import random
from dataclasses import dataclass
from PyQt5 import QtCore, QtGui

from easygraphics import *

MAXSTAR = 200 # number of stars

@dataclass
class Star:
    x:int
    y:int
    step:float
    color:QtGui.QColor
star = [Star(0,0,0,None) for i in range(MAXSTAR)]

def init_star(i:int):
    global star
    star[i].x=0
    star[i].y = random.randrange(get_height())
    star[i].step = random.randrange(5000)/1000+1
    star[i].color = color_gray(star[i].step * 255 / 6 + 0.5)

def move_star(i:int):
    # erase old star
    put_pixel(star[i].x,star[i].y,Color.BLACK)
    # calculate new position of the star
    star[i].x += star[i].step
    if star[i].x>=get_width():
        init_star(i)
    # draw new star
    put_pixel(star[i].x,star[i].y,star[i].color)

def main():
    init_graph(1024,768)
    set_caption("Starry Sky")
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_background_color(Color.BLACK)
    for i in range(MAXSTAR):
        init_star(i)
        star[i].x = random.randrange(get_width())

    while is_run():
        if has_kb_hit():
            break
        for i in range(MAXSTAR):
            move_star(i)
        delay_fps(30)

    close_graph()

easy_run(main)



