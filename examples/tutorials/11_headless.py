"""
Draw a bus with a transparent background and copy it many times
"""
from easygraphics import *
import draw_bus

def main():
    init_graph(headless=True)
    img = create_image(210, 130)
    set_target(img)
    draw_bus.draw_bus()
    save_image("headless_bus.png")
    img.close()
    close_graph()

easy_run(main)