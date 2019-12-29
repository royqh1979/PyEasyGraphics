from easygraphics import *

def main():
    init_graph(200,100)
    curve(5, 26, 5, 26, 73, 24, 73, 61)
    curve(5, 26, 73, 24, 73, 61, 15, 65)
    set_fill_color("white")
    steps = 6
    for i in range(steps+1):
        t = i / steps
        x = curve_point(5, 5, 73, 73, t)
        y = curve_point(26, 26, 24, 61, t)
        ellipse(x, y, 3, 3)
        x = curve_point(5, 73, 73, 15, t)
        y = curve_point(26, 24, 61, 65, t)
        ellipse(x, y, 3, 3)
    pause()
    close_graph()

easy_run(main)