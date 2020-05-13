"""
Draw a bus with a transparent background and copy it many times
"""
from easygraphics import *
import draw_bus

def main():
    init_graph(750, 450)
    img = create_image(210, 130)
    set_target(img)  # set target to img
    draw_bus.draw_bus()
    set_target()  # set target back to the graphics window
    set_background_color("black")
    for i in range(0, 9):
        x = i % 3 * 250 + 20
        y = i // 3 * 150 + 10
        save_settings()
        # transforms
        translate(x, y)
        translate(105, 65)
        rotate(45)
        translate(-105, -65)

        draw_image(0, 0, img)
        restore_settings()
    pause()
    img.close()
    close_graph()

easy_run(main)