from easygraphics.turtle import *

def main():
    create_world(400,400)
    for i in range(4):
        fd(100)
        lt(90)

    hide()
    pause()
    close_world()

easy_run(main)