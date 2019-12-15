"""
Draw circles
"""
from easygraphics import *

def main():
    init_graph(400, 300)
    circle(100, 100, 50)
    circle(100, 100, 100)
    circle(100, 100, 120)
    pause()
    close_graph()

easy_run(main)