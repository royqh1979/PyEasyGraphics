"""
Draw text
"""
if __name__ == "__main__":
    from easygraphics import *

    init_graph(400, 50)
    draw_text(50, 30, "There", "are", 5, "dogs", "under", "the", "tree", ".")
    pause()
    close_graph()
