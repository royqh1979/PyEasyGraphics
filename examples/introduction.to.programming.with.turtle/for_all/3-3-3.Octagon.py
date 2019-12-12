from easygraphics.turtle import *

def main():
    create_world(800, 600)
    side = 100
    n = 8
    angle = (n - 2) * 180.0 / n
    for i in range(n):
        fd(side)
        rt(180 - angle)

    pause()
    close_world()

easy_run(main)