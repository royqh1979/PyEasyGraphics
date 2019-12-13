"""
Draw a polyline
"""
from easygraphics import *

def main():
    init_graph(400, 300)
    draw_poly_line(50, 50, 350, 75, 50, 150, 350, 175, 50, 250, 350, 275)
    pause()
    close_graph()

easy_run(main)