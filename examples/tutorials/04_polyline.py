"""
Draw a polyline
"""
if __name__ == "__main__":
    from easygraphics import *

    init_graph(600, 600)
    points = [50, 50, 550, 350, 50, 150, 550, 450, 50, 250, 550, 550]
    draw_poly_line(points)
    pause()
    close_graph()
