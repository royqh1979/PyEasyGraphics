"""
Draw a bus without transformations
"""
if __name__ == "__main__":
    from easygraphics import *
    import draw_bus

    init_graph(500, 300)

    # rotate around the (105,65)
    rotate(-45, 105, 65)

    draw_bus.draw_bus()
    pause()
    close_graph()
