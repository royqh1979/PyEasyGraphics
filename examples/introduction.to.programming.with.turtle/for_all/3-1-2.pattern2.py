from easygraphics.turtle import *

def main():
    create_world()

    for i in range(4):
        fd(100)
        rt(90)
        fd(100)
        rt(90)
        fd(50)
        rt(90)
        fd(50)
        rt(90)
        fd(100)
        rt(90)
        fd(25)
        rt(90)
        fd(25)
        rt(90)
        fd(50)

    pause()
    close_world()

easy_run(main)