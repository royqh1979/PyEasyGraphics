Basic Commands
================
In this tutorial, we will introduce basic commands of the turtle graphics.

Move the turtle
---------------
Forward(x) function move the turtle x steps forward.
fd(x) is the short form of forward(x).

.. code-block:: python

    from easygraphics.turtle import *

    def main():
        create_world(250,250)
        fd(100)
        pause()
        close_world()

    easy_run(main)

.. image:: ../../docs/images/turtle/01_fd.png

backward(x) function move the turtle x steps backward.
back(x) and bk(x) is the short form of backward(x).

    .. code-block:: python

    from easygraphics.turtle import *

    def main():
        create_world(400,400)
        bk(100)
        pause()
        close_world()

    easy_run(main)

.. image:: ../../docs/images/turtle/01_bk.png

Turning the turtle
------------------

right_turn(x) turns the turtle x degrees clockwise. right(x) and rt(x) are its short form.

left_turn(x) turns the turtle x degrees counter-clockwise. left(x) and lt(x) are its short form

The following program draws a 30 degree angle.

.. code-block:: python

    from easygraphics.turtle import *

    def main():
        create_world(400,400)
        fd(80)
        bk(80)
        rt(30)
        fd(80)
        pause()
        close_world()

    easy_run(main)

.. image:: ../../docs/images/turtle/01_angle.png

Return to Home
--------------

Pen Up and Pen Down
-------------------

Show and Hide the Turtle
------------------------

Clear the screen/canvas
-----------------------

Fill the shapes
---------------






The turtle graphics is a classic and popular way to introducing programming to kids.

In the turtle graphics, you control a turtle to move around the graphics window.
The traces left by its move form drawings.

In the following program, we use turtle graphics to draw a star.

.. code-block:: python

    from easygraphics import *
    from easygraphics.turtle import *

    def main():
        create_world()
        set_color("red")
        set_fill_color("red")
        set_fill_rule(FillRule.WINDING_FILL)
        right(90)
        begin_fill()
        for i in range(5):
            forward(100)
            right(144)
        end_fill()
        pause()
        close_world()

    easy_run(main)


.. toctree::
    :max-depth: 1

    tutorials/102_turtle_basic_commands
    tutorials/103_pen_and_fill
    tutorials/104_coordinations
