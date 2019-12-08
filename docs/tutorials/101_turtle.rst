Turtle Graphics
================
The turtle graphics is a classic and popular way to introducing programming to kids.

In the turtle graphics, you control a turtle to move around the graphics window.
The traces left by its move form drawings.


In the following program, we use turtle graphics to draw a star.

.. code-block:: python

    from easygraphics import *
    from easygraphics.turtle import *

    create_world()
    set_color("red")
    set_fill_color("red")
    set_fill_rule(FillRule.WINDING_FILL)
    rt(90)
    begin_fill()
    for i in range(5):
        forward(100)
        right(144)
    end_fill()
    pause()
    close_world()


.. toctree::
    :max-depth: 1

    apis/102_turtle_basic_commands
    apis/103_pen_and_fill
    apis/104_coordinations
