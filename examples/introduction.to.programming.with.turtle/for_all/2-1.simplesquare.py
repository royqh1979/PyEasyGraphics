from easygraphics.turtle import *

def main():
    create_world()

    set_pen_size(1)
    set_speed(10)

    fd(100)
    rt(90)
    fd(100)
    rt(90)
    fd(100)
    rt(90)
    fd(100)
    rt(90)

    pause()
    close_world()

easy_run(main)