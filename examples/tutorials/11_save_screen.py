"""
Draw a bus on the graphics window and save it
"""
from easygraphics import *
import draw_bus

def main():
    init_graph(600, 400)
    draw_bus.draw_bus()
    save_image("bus_screen.png")
    pause()
    close_graph()

easy_run(main)