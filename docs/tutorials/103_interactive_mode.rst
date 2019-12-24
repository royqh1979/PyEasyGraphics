Interactive Mode
================
On Windows and Linux, we can run easygraphics in python's interactive mode.

Demo fro easygraphics
---------------------
.. code-block:: python

    from easygraphics import *
    init_graph()
    line(50,50,100,100)

    close_graph()

Demo for Turtle Graphics
------------------------
.. code-block:: python
    from easygraphics.turtle import *
    create_world()
    fd(100)
    lt(90)
    close_world()



Clear the screen
----------------
If you are using turtle graphics, clear_screen() clears the turtle graphics window, and reset the turtle to its initial position and state.
cs() / clear() is the short form.

If you are using easygraphics, clear_device() clears the graphics window.


