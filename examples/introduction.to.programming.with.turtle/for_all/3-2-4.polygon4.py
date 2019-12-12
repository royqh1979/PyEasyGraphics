from easygraphics.turtle import *

def main():
    create_world(800, 600)

    side = 100;
    angle = 108;
    n = 10;
    for i in range(n):
        fd(side)
        rt(angle)

    pause()
    close_world()

easy_run(main)