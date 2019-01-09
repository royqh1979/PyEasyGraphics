from easygraphics.turtle import *


def hilbert(size, level, parity):
    if level == 0:
        return
    lt(parity * 90)
    hilbert(size, level - 1, -parity)
    fd(size)
    rt(parity * 90)
    hilbert(size, level - 1, parity)
    fd(size)
    hilbert(size, level - 1, parity)
    rt(parity * 90)
    fd(size)
    hilbert(size, level - 1, -parity)
    lt(parity * 90)


create_world(800, 600)

set_speed(500)
hilbert(5, 5, 1);

pause()
close_world()
