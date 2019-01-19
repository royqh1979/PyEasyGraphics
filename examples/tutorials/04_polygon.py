"""
Draw a polygon
"""
if __name__ == "__main__":
    from easygraphics import *

    init_graph(400, 300)
    set_color(Color.DARK_BLUE)
    set_fill_color(Color.LIGHT_MAGENTA)
    draw_polygon(50, 50, 350, 250, 50, 150)
    pause()
    close_graph()
