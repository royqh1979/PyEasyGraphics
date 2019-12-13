"""
Use flood fill to draw a petal
"""
from easygraphics import *

def main():
    init_graph(400, 200)
    arc(200, -40, 180, 360, 220, 220)
    arc(200, 240, 0, 180, 220, 220)
    set_fill_color(Color.DARK_RED)
    flood_fill(200, 100, Color.BLACK)
    pause()
    close_graph()

easy_run(main)