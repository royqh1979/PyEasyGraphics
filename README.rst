
===============================
Introduction to PyEasyGraphics
===============================

A Borland Graphics Interface like Grahics library for python


`Borland Graphics Interface <https://en.wikipedia.org/wiki/Borland_Graphics_Interface />`_, also known
as `Turbo C Graphics <http://www.softwareandfinance.com/Turbo_C/Graphics/>`_, is an easy-to-use graphics library
bundled with Turbo C/Turbo C++/Borland C++.

Because it is easy to learn and use, it is very good for using for kids and beginners to learn basic programming ,
computer graphics.

.. image:: https://badge.fury.io/py/easygraphics.png
    :target: http://badge.fury.io/py/easygraphics

.. image:: https://pypip.in/d/easygraphics/badge.png
        :target: https://pypi.python.org/pypi/easygraphics

* Free software: MIT license
* Documentation: https://pyeasygraphics.readthedocs.io/en/latest/
* Documentation (Chinese Version): http://easygraphics.royqh.net

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
Some code is taken from `easygui_qt <https://github.com/aroberge/easygui_qt/>`_ and
`qtutils <https://bitbucket.org/philipstarkey/qtutils>`_, thanks a lot!