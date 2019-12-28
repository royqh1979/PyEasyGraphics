from easygraphics import *

def main():
    init_graph(200,100)
    bezier(85, 20, 10, 10, 90, 90, 15, 80)
    set_fill_color("white")
    steps = 10
    for i in range(steps+1):
        t = i / steps
        x = bezier_point(85, 10, 90, 15, t)
        y = bezier_point(20, 10, 90, 80, t)
        draw_ellipse(x, y, 3, 3)
    pause()
    close_graph()

easy_run(main)