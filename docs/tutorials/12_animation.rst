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

Skipping Frames
^^^^^^^^^^^^^^^
Sometimes a drawing can be complicated slow, and we can't finish a frame's drawing
in the specified frame time. This will create lags in the animation.

The delay_jfps() can skip some frames ( if a frame is using too mush time, the successive frames
will be skipped to keep up with the specified fps)

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
    draw_polygon([0,0, 0,60, 160,60, 160,40, 125,20, 110, 0])
    set_fill_color("darkgray")
    draw_circle(35,60,20)
    draw_circle(120,60,20)
    set_fill_color("transparent")
    draw_rect(10,10,40,25)
    draw_rect(50, 10, 80, 25)

    set_target()
    x = 0
    while is_run():
        x = (x + 3) % 750
        draw_image(0, 0, background)
        draw_image(x, 350, car)
        delay_fps(60)

    background.close()
    car.close()
    close_graph()