Draw with the Current Position
==============================

In easygraphics, each image (including the graphics window) stores "a current position".
Use this position, we can draw lines relatively.

The related functions are:

.. currentmodule:: easygraphics

.. autosummary::

    get_x
    get_y
    get_drawing_pos
    move_to
    move_rel
    line_to
    line_rel

The following program draws a dash line by using the current position.

.. code-block:: python

    from easygraphics import *

    init_graph(400,100)

    move_to(50,50)
    for i in range(10):
        line_rel(10,0)
        move_rel(20,0)
    pause()
    close_graph()

Approximate a function curve
----------------------------

Sometimes we need to draw line segments successively.

For example, to plot the function f(x)=sin(x)\'s curve on [-3,3] ,we can use many successive line segements to
approximate the curve:

1. divide [-3,3] into n equal intervals, to get n+1 values evenly distributed on [-3,3]:
   x0,x1,x2,x3,...,xn, and x0=-3, xn=3
2. cacluate function values f(x0),f(x1),f(x2),f(x3), ..., f(xn).
3. draw n line segements:  (x0,f(x0)) to (x1,f(x1)), (x1,f(x1)) to (x2,f(x2)) ..., (xn-1,f(xn-1)) to (xn,f(xn))
4. the resulting line segments is the curve approximation we need.

Apparently, the more greater n is, the more precisely the appoximation is. To minimize the usage of memory,
we should calculate and draw the line segments one by one.

The following program plot a sin(x) curve on [-3,3].

.. code-block:: python

    from easygraphics import *
    import math as m

    init_graph(600,400)
    translate(300,200) # move origin to the center
    scale(100,-100) # zoom each axis 100 times, and make y-axis grow from bottom to top.

    x=-3
    delta=0.01
    move_to(x,m.sin(x))
    while x<=3:
        line_to(x,m.sin(x))
        x=x+delta
    pause()
    close_graph()



