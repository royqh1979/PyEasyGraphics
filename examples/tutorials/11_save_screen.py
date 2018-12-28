"""
Draw a bus on the graphics window and save it
"""
if __name__ == "__main__":
    from easygraphics import *
    import draw_bus

    init_graph(600, 400)
    draw_bus.draw_bus()
    save_image("bus_screen.png")
    pause()
    close_graph()
