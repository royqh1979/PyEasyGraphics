from easygraphics.turtle import *
from easygraphics import *


def main():
    create_world(300, 300)

    set_line_width(3)
    set_color("red")
    set_background_color("lightgray")
    set_fill_color(Color.LIGHT_BLUE)

    begin_fill()
    for i in range(4):
        fd(100)
        lt(90)
    end_fill()

    circle(50, 50, 30)
    fill_rect(-100, -100, -50, -50)
    pause()
    close_world()


easy_run(main)
