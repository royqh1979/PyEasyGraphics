"""
Draw a polyline
"""
if __name__ == "__main__":
    from easygraphics import *

    init_graph(400, 300)
    points = [50, 50, 350, 75, 50, 150, 350, 175, 50, 250, 350, 275]
    draw_poly_line(points)
    pause()
    close_graph()
