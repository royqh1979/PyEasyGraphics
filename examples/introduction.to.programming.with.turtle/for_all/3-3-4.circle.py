from easygraphics.turtle import *

def main():
    create_world(800, 600)

    size = 3
    for i in range(360):
        fd(size)
        rt(1)

    pause()
    close_world()

easy_run(main)