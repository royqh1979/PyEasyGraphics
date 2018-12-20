from easygraphics import *

init_graph(600, 600)
points = [50, 50, 550, 350, 50, 150, 550, 450, 50, 250, 550, 550]
draw_lines(points)
pause()
close_graph()


def add(x: float, y: float):
    return x + y


s = add("200", "400")
print(s)
