from easygraphics.turtle import *

def main():
    create_world(400,400)

    for i in range(4):
        fd(100)
        lt(90)

    # use pen_up to move the turtle without a trace
    pen_up()
    rt(135)
    fd(70)
    lt(135)
    pen_down()

    for i in range(4):
        fd(200)
        lt(90)

    pause()
    close_world()

easy_run(main)
