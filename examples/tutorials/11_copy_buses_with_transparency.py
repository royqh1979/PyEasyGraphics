"""
Draw a bus with a transparent background and copy it many times
"""
if __name__ == "__main__":
    from easygraphics import *
    import draw_bus

    init_graph(750, 450)
    img = create_image(210, 130)
    set_background_color(Color.TRANSPARENT, img)  # set img's background to transparency
    set_target(img)  # set target to img
    draw_bus.draw_bus()
    set_target()  # set target back to the graphics window
    set_background_color("black")
    for i in range(0, 9):
        x = i % 3 * 250
        y = i // 3 * 150
        draw_image(x + 20, y + 10, img)

    pause()
    img.close()
    close_graph()
