from easygraphics.turtle import *

def main():
    create_world(800, 600)

    for i in range(60):
        fd(2)
        rt(1)
    rt(120)

    for i in range(60):
        fd(2)
        rt(1)
    rt(120)

    pause()
    close_world()

easy_run(main)