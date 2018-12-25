"""
Use the current position to draw a dash line
"""
if __name__ == "__main__":
    from easygraphics import *

    init_graph(400, 100)
    move_to(50, 50)
    for i in range(10):
        line_rel(10, 0)
        move_rel(20, 0)
    pause()
    close_graph()
