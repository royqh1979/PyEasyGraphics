from easygraphics import *

def main():
    init_graph(800, 600)

    line(50, 50, 400, 400)

    set_line_width(20)

    line(50, 400, 400, 50)

    pause()
    close_graph()

easy_run(main)