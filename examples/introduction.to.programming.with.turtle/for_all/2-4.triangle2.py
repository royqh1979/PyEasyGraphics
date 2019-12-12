from easygraphics.turtle import *

def main():
    create_world()
    rt(30);

    for i in range(3):
        fd(100)
        rt(120)
    lt(30);

    pause()
    close_world()

easy_run(main)