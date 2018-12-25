"""
Draw circles
"""
if __name__ == "__main__":
    from easygraphics import *

    init_graph(400, 300)
    set_color("lightgray")
    draw_rect(100, 50, 300, 250)
    set_color("black")

    set_view_port(100, 50, 300, 250, clip=False)
    circle(100, 100, 50)
    circle(100, 100, 100)
    circle(100, 100, 120)
    pause()
    close_graph()
