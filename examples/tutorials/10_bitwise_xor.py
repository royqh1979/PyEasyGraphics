"""
Draw a elastical line
"""
if __name__ == "__main__":
    from easygraphics import *

    init_graph(400, 200)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_background_color("white")
    x = 100
    ellipse(x, 100, 100, 50)  # draw a ellipse
    set_color("white")
    set_composition_mode(CompositionMode.SRC_XOR_DEST)
    while is_run():
        old_x = x
        x = (x + 5) % 400
        ellipse(old_x, 100, 100, 50)  # clear the ellipse last drawn
        ellipse(x, 100, 100, 50)  # draw a new ellipse
        delay_fps(30)

    close_graph()
