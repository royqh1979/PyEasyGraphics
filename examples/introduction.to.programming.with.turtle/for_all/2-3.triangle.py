from easygraphics.turtle import *

def main():
    create_world()

    for i in range(3):
        fd(100)
        rt(120)

    pause()
    close_world()

easy_run(main)