
Sample program
==============

This is a simple moving ball sample.

.. code:: python

    from easygraphics import *

    def mainloop():
        x = 0;
        set_color(Color.BLUE);
        set_fill_color(Color.GREEN);

        while is_run():
            x = ( x + 1 ) % 440;
            clear_device();
            draw_circle(x + 100, 200, 100);
            delay_fps(60)

    init_graph(640, 480)
    mainloop()
    close_graph()

