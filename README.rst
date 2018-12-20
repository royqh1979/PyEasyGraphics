===============================
Introduction to EasyGraphics
===============================

A Borland Graphics Interface like Grahics library for python

Borland Graphics Interface( https://en.wikipedia.org/wiki/Borland_Graphics_Interface ),also known
as Turbo C Graphics(http://www.softwareandfinance.com/Turbo_C/Graphics/), is an easy-to-use graphics library
bundled with Turbo C/Turbo C++/Borland C++.

Because it is easy to learn and use, it is very good for using for kids and beginners to learn basic programming ,
computer graphics.

Sample program
----------------------
.. code:: python

    from easygraphics import *

    def mainloop():
        x = 0;
        set_color(Color.BLUE);
        set_fill_color(Color.GREEN);

        while is_run():
            x = ( x + 1 ) % 440;
            clear_device();
            draw_ellipse(x + 100, 200, 100, 100);
            delay_fps(60)

    init_graph(640, 480)
    mainloop()
    close_graph()


Special Thanks
---------------
Some code is taken from easygui_qt(https://github.com/aroberge/easygui_qt) and qtutils(https://bitbucket.org/philipstarkey/qtutils),
thanks a lot!