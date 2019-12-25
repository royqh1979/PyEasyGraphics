Turtle Graphics
================
The turtle graphics is a classic and popular way to introducing programming to kids.

In the turtle graphics, you control a turtle to move around the graphics window.
The traces left by its move form drawings.

In the following program, we use turtle graphics to draw a star:

In the main function, we:

    #. use create_world(800,600) to create a 800x600 drawing canvas (drawing window)
    #. set the pen color to red and the fill color to red
    #. use right(90) command to turn the turtle 90 degrees clockwise.
    #. use forward(100) command to move the turtle 100 steps forward,then turn the turtle 144 degrees clockwise.
    #. repeat the above step 5 times
    #. use close_world() to close the drawing window.

.. code-block:: python

    from easygraphics import *
    from easygraphics.turtle import *

    def main():
        create_world(800,600)
        set_color("red")
        set_fill_color("red")
        right(90)
        for i in range(5):
            forward(100)
            right(144)
        pause()
        close_world()

    easy_run(main)
