"""
Draw a cubic bezier curve
"""
if __name__ == "__main__":
    from easygraphics import *

    init_graph(600, 400)
    points = [300, 50, 200, 50, 200, 200, 100, 200]
    draw_bezier(*points)
    pause()
    close_graph()
