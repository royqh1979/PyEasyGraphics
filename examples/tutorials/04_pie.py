from easygraphics import *

def main():
    init_graph(400, 300)
    set_color("red")
    set_fill_color("lightyellow")
    draw_pie(200, 150, 135, 45, 100, 70)
    pause()
    close_graph()

easy_run(main)
