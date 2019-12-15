"""
Load and display a image
"""
from easygraphics import *

def main():
    init_graph(800, 600)
    img = load_image("test.png")
    draw_image((get_width() - img.get_width()) // 2,
               (get_height() - img.get_height()) // 2, img)
    pause()
    img.close()
    close_graph()

easy_run(main)