"""
Use the current position to draw a dash line
"""
from easygraphics import *

def main():
    init_graph(400, 100)
    move_to(50, 50)
    for i in range(10):
        line_rel(10, 0)
        move_rel(20, 0)
    pause()
    close_graph()

easy_run(main)