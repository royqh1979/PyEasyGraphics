from easygraphics import *
from easygraphics.turtle import *

def main():
    create_world(800, 600)
    set_speed(100)
    set_pen_size(5)
    # 瓜皮-绿色

    setxy(-95, 0)
    rt(30)
    forward(-210)
    rt(90)
    set_fill_color("green")
    begin_fill()
    move_arc(400, 60)
    lt(90)
    fd(50)
    lt(90)
    move_arc(-350, 60)
    rt(90)
    backward(50)
    end_fill()

    # 果肉-红色

    set_fill_color("red")
    begin_fill()
    forward(400)
    lt(60)
    backward(350)
    lt(90)
    move_arc(-350, 60)
    end_fill()

    # 瓜子
    set_pen_size(30)
    draw_point(0, 100)
    draw_point(50, 0)
    draw_point(-50, 0)
    draw_point(0, -100)
    draw_point(100, -100)
    draw_point(-100, -100)

    hide()
    pause()
    close_world()

easy_run(main)