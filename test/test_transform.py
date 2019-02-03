"""
Draw a bus without transformations
"""
if __name__ == "__main__":
    from easygraphics import *
    import draw_bus

    init_graph(500, 300)

    # move the origin to the center of the image
    translate(250, 150)
    transform = get_target().get_painter().transform()
    print(transform.map(0, 0))

    # rotate around the bus center
    translate(105, 65)
    rotate(180)
    translate(-105, -65)
    transform = get_target().get_painter().transform()
    print(transform.map(0, 0))

    # shear arount the bus center
    # translate(105, 65)
    # shear(0.5, 0.5)
    # translate(-105, -65)
    #
    # transform = get_target().get_painter().transform()
    # print(transform.map(0,0))

    # scale
    scale(1.2, 1.2)
    draw_bus.draw_bus()
    pause()
    close_graph()
