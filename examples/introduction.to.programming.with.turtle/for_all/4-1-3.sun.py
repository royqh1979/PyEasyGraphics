from easygraphics.turtle import *

def main():
    def arcl(side, degree):
        for i in range(degree):
            fd(side)
            lt(1)


    def arcr(side, degree):
        for i in range(degree):
            fd(side)
            rt(1)


    create_world(800, 600)

    set_speed(100)

    for i in range(9):
        for j in range(2):
            arcl(1, 90)
            arcr(1, 90)
            rt(160)
    pause()
    close_world()

easy_run(main)