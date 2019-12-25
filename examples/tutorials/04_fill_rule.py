from easygraphics import *


def main():
    init_graph(420, 200)

    set_fill_rule(FillRule.ODD_EVEN_FILL)
    set_fill_color("lightgray")
    draw_polygon(50, 50, 150, 50, 60, 110, 100, 20, 140, 110, 50, 50)

    draw_text(5, 150, "FillRule.ODD_EVEN_FILL")

    translate(220, 0)

    set_fill_rule(FillRule.WINDING_FILL)
    set_fill_color("lightgray")
    draw_polygon(50, 50, 150, 50, 60, 110, 100, 20, 140, 110, 50, 50)

    draw_text(5, 150, "FillRule.WINDING_FILL")

    pause()
    close_graph()


easy_run(main)
