"""
Draw a bus without transformations
"""
if __name__ == "__main__":
    from easygraphics import *
    import draw_bus

    init_graph(500, 300)

    translate(0, 65)
    reflect(1, 0)
    translate(0, -65)

    draw_bus.draw_bus()
    pause()
    close_graph()
