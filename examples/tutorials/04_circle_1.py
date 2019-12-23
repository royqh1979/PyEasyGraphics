"""
Circle
"""
from easygraphics import *

def main():
    init_graph(200, 150)
    set_color(Color.BLUE)
    set_fill_color(Color.RED)
    fill_circle(100, 75, 60)
    pause()
    close_graph()

easy_run(main)