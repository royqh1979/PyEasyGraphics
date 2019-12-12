from easygraphics.turtle import *

def main():
    create_world(800, 600)

    set_speed(100)

    for i in range(6):
        for j in range(360):
            fd(2)
            rt(1)
        rt(60)

    pause()
    close_world()

easy_run(main)