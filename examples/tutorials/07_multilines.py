"""
Draw text with custom seperators
"""
from easygraphics import *

def main():
    init_graph(400, 300)
    draw_rect(50, 50, 350, 250)  # draw a border to better see the result
    draw_rect_text(50, 50, 300, 200, "There are so many beautiful flowers in the garden!",
                   flags=TextFlags.TEXT_WORD_WRAP | TextFlags.ALIGN_CENTER)
    pause()
    close_graph()

easy_run(main)