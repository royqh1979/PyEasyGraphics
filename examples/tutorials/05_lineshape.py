"""
Draw a rectangle with dash line.
"""
if __name__ == "__main__":
    from easygraphics import *

    init_graph(400, 300)
    set_line_width(10)
    set_line_style(LineStyle.DASH_LINE)
    draw_rect(50, 50, 350, 250)
    pause()
    close_graph()
