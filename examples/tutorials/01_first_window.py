"""
First easy graphics program

In this program, we will:

1. Init the graphics windows
#. wait for mouse click or keyboard hitting
#. close the window
"""
if __name__ == '__main__':
    from easygraphics import *

    init_graph(800, 600)
    pause()
    close_graph()
