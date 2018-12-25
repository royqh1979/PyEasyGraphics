"""
Draw a bus without transformations
"""
if __name__ == "__main__":
    from easygraphics import *
    import draw_bus

    init_graph(500, 300)

    translate(105, 0)
    reflect(0, 1)
    translate(-105, 0)
    draw_bus.draw_bus()
    pause()
    close_graph()
