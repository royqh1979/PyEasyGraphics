from easygraphics.turtle import *
import random


def random_move(d1, d2, a1, a2):
    while is_run():
        d = random.randint(a1, a2)
        lt(d)
        fd(random.randint(d1, d2))

def main():
    create_world(800, 600)
    set_speed(10)

    random.seed()

    # random_move(1,10,0,10)
    # random_move(1,10,-10,5)
    random_move(1, 10, -10, 10)

    pause()
    close_world()

easy_run(main)