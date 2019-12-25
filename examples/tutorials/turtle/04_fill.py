from easygraphics.turtle import *
from easygraphics import *


def main():
    create_world(300, 300)

    set_fill_rule(FillRule.WINDING_FILL)
    begin_fill()
    for i in range(5):
        fd(100)
        lt(144)
    end_fill()

    pause()
    close_world()


easy_run(main)
