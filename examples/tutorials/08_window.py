"""
Use window
"""
from easygraphics import *

def main():
    init_graph(600, 400)
    set_window(-3, -2, 6, 4)

    circle(0, 0, 1.5)
    pause()
    close_graph()

easy_run(main)