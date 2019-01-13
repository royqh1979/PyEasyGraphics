Animation
=========
By rapidly change the painting (frames) on the graphics window, we can make an animation.


Time Control
------------
Because the computer can draw very fast, we must let it to wait some time
between two frames.

  **Note:** Functions used in this section won't work in the headless mode.

In easygraphics, we can use delay() to pause the program from the specified milliseconds.

Control the FPS
^^^^^^^^^^^^^^^
Because the actual drawing time can be different each time drawing, a better way
to control the speed is by using the delay_fps() function.

FPS is the abbreviation of "frames per second".delay_fps() will calculate each
frame's drawing time, and wait to make each frame displays evenly.

Render Mode
-----------
There are two render mode in EasyGraphics:

1. **RenderMode.AUTO**: All drawings on the graphics window will show immediately.
   This is the default mode, and is for normal drawing.
2. **RenderMode.Manual**: Drawings will not show on the graphics window. Only time control,
   keyboard or mouse functions like pause()/delay()/delay_fps()/get_mouse_msg() will update the graphics window.
   This mode can speed up the animation frames drawing.

It's a good practice to set the render mode to manual when your want to show an animation.

You can use set_render_mode() to set the render mode.

    **Note:** If you are not drawing on the graphics window, this render mode has no effect.

Background
----------
Ofter we need to make an object move in a background. If the background is complicated,
it's not a good idea to recreate the background in each frame.

A common solution is to draw background in one image , and the moving object in another transparent image.
The final result is made by merge the two images.

The following program draws a moving bus on the road (background).Note the use of the is_run() function.

.. code-block:: python

    from easygraphics import *

    init_graph(800, 600)
    set_render_mode(RenderMode.RENDER_MANUAL)

    background = create_image(800, 600)
    set_target(background)
    set_background_color(Color.LIGHT_YELLOW)
    set_fill_color(Color.RED)
    draw_circle(150, 150, 50)
    set_fill_color(Color.DARK_BLUE)
    draw_rect(0, 400, 800, 600)

    car = create_image(162, 150)
    set_target(car)
    set_composition_mode(CompositionMode.SOURCE)
    set_background_color(Color.TRANSPARENT)
    set_fill_color("white")
    draw_polygon([0, 0, 0, 60, 160, 60, 160, 40, 125, 20, 110, 0])
    set_fill_color("darkgray")
    draw_circle(35, 60, 20)
    draw_circle(120, 60, 20)
    set_fill_color("transparent")
    draw_rect(10, 10, 40, 25)
    draw_rect(50, 10, 80, 25)

    set_target()
    x = 0
    while is_run():
        x = (x + 2) % 750
        if delay_fps(100):
            draw_image(0, 0, background)
            draw_image(x, 350, car)

    background.close()
    car.close()
    close_graph()

Skipping Frames
^^^^^^^^^^^^^^^
Sometimes a drawing can be complicated and slow, and we can't finish a frame's drawing
in the specified frame time. This will create lags in the animation.

The delay_jfps() can skip some frames ( if a frame is using too mush time, the successive frames
will be skipped to keep up with the specified fps).

The following example shows how to use delay_jfps() to control time. Note that we
use sleep() to simulate a long-time drawing operation.

.. code-block:: python

    from easygraphics import *
    import time

    init_graph(640, 480)
    set_color(Color.BLUE)
    set_fill_color(Color.GREEN)
    set_render_mode(RenderMode.RENDER_MANUAL)

    x = 0
    while is_run():
        x = (x + 1) % 440
        if delay_jfps(60, 0):
            clear_device()
            draw_ellipse(x + 100, 200, 100, 100)
            time.sleep(0.5)
    close_graph()