Drawing using Processing
========================

`Processing <https://processing.org>`_ is a simple programming environment to help user create interactive animations.
easygraphics.processing is a processing-like animation framework.

In processing, we override (redefine) some key functions to tell the framework how to work.

In the following program, we redefined two functions in processing to draw a rotating star.

The function setup() is called by the framework when the program begins.

We use it to do preparing works, such as defining window size, setting foreground , background color and frame refresh rate(fps), and so on.

The function draw() is called by the framework to draw frames.

Each time before a frame is to be displayed, this function is called.

Finally we use run_app(globals()) to start the processing frame work.

.. code:: python

    from easygraphics.processing import *
    from easygraphics import *

    # this overriding function is called by processing at the beginning
    def setup():
        set_size(800, 600)
        set_fill_color("red")

    t = 0

    # this overriding function is called by processing every frame
    def draw():
        global t
        clear()
        t = t + 1
        t = t % 360
        translate(400, 300)
        rotate(t)
        begin_shape()
        for i in range(5):
            vertex(100, 0)
            rotate(144)
        end_shape()


    # run the processing app
    run_app(globals())

