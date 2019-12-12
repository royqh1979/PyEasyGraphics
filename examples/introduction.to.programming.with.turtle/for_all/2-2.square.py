from easygraphics.turtle import *

def main():
    create_world()

    set_speed(10)

    for i in range(4):
        fd(100)
        rt(90)

    pause()
    close_world()

easy_run(main)