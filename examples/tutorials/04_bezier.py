"""
Draw a cubic bezier curve
"""
from easygraphics import *

def main():
    init_graph(600, 400)
    points = [300, 50, 200, 50, 200, 200, 100, 200]
    draw_bezier(*points)
    pause()
    close_graph()

easy_run(main)