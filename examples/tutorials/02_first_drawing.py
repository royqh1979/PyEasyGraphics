"""
Fist drawing program

Let\'s draw a line from (0,0) to (640,480)

In computer graphics, we normally use a screen coordinate system as below:

.. image:: ../../docs/images/graphics/coordinates.png

In this system, the origin (0,0) is at screen\'s upper left corner, and y-axis is growing top-down.

So in this sample we are drawing a line from upper left corner to lower right corner.

"""
if __name__ == '__main__':
    from easygraphics import *

    init_graph(640, 480)
    line(0, 0, 640, 480)
    pause()
    close_graph()
