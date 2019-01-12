Turtle Graphics
================
The turtle graphics is a classic and popular way to introducing programming to kids.

In the turtle graphics, you control a turtle to move around the graphics window.
The traces left by its move form drawings.


In the following program, we use turtle graphics to draw a star.

.. code-block:: python

    from easygraphics.turtle import *

    create_world(800,600)
    set_render_mode(RenderMode.RENDER_MANUAL)

    while is_run():
        if has_mouse_msg():
            x,y,type,buttons = get_mouse_msg()
            if type == MouseMessageType.PRESS_MESSAGE:
                color = get_color(get_background_color())
                set_background_color(color)
        delay_fps(60)

    close_graph()


.. toctree::
    :max-depth: 1

    apis/102_turtle_basic_commands
    apis/103_pen_and_fill
    apis/104_coordinations
