"""
Draw a rectangle with dash line.
"""
from easygraphics import *

def main():
    init_graph(400, 300)
    set_line_width(10)
    set_line_style(LineStyle.DASH_LINE)
    draw_rect(50, 50, 350, 250)
    pause()
    close_graph()

easy_run(main)