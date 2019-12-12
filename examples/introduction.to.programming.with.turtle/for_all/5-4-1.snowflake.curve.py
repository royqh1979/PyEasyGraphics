from easygraphics.turtle import *


def snowflake_side(size, level):
    if level == 0:
        fd(size)
        return
    snowflake_side(size / 3, level - 1)
    lt(60)
    snowflake_side(size / 3, level - 1)
    rt(120)
    snowflake_side(size / 3, level - 1)
    lt(60)
    snowflake_side(size / 3, level - 1)


def snowflake(size, level):
    for i in range(3):
        snowflake_side(size, level)
        rt(120)

def main():
    create_world(800, 600)
    set_speed(100)

    setxy(-250, 150)

    rt(90)
    snowflake(500, 4)

    hide()
    pause()
    close_world()

easy_run(main)