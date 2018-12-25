"""
Draw a polygon
"""
if __name__ == "__main__":
    from easygraphics import *

    init_graph(600, 600)
    set_color(Color.DARK_BLUE)
    set_fill_color(Color.LIGHT_MAGENTA)
    points = [50, 50, 550, 350, 50, 150]
    draw_polygon(points)
    pause()
    close_graph()
