"""
Draw a elastical line
"""
if __name__ == "__main__":
    from easygraphics import *
    import math

    init_graph(400, 300)
    set_render_mode(RenderMode.RENDER_MANUAL)
    translate(200, 150)
    set_fill_color("orange")
    set_line_width(10)
    draw_rounded_rect(-100, -100, 100, 100, 25, 25)

    set_line_width(1)
    set_color(Color.WHITE)
    set_composition_mode(CompositionMode.SRC_XOR_DEST)
    x1, y1 = 0, 0
    theta = 0
    pho = 200
    x, y = pol2cart(pho, theta)
    line(x1, y1, x, y)
    for i in range(0, 360):
        if delay_fps(10):
            line(x1, y1, x, y)
            theta = math.radians(i)
            x, y = pol2cart(pho, theta)
            line(x1, y1, x, y)

    pause()
    close_graph()
