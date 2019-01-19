"""
The draw_bus() function
"""
from easygraphics import *


def draw_bus():
    """
    Draw a simple bus.
    """
    set_color("lightgray")
    rect(0, 0, 210, 130)

    set_color("red")
    set_fill_color("blue")

    draw_circle(60, 100, 10)  # draw tyre
    draw_circle(140, 100, 10)  # draw tyre
    rect(20, 20, 190, 100)

    # draw window
    x = 30
    while x < 115:
        rect(x, 40, x + 10, 50)
        x += 15

    # draw door
    rect(160, 40, 180, 100)
    line(170, 40, 170, 100)
    circle(170, 70, 5)

    # draw text
    draw_text(0, 130, "A good old bus.")
