"""
Draw text
"""
from easygraphics import *

def main():
    init_graph(400, 50)
    draw_text(50, 30, "There", "are", 5, "dogs", "under", "the", "tree", ".")
    pause()
    close_graph()

easy_run(main)