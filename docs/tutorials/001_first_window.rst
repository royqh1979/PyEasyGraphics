The First window
================

In this program, we will create and show a graphics window:

1. Define the easygraphics main function

    In the main function, we:

    #. Init the graphics window
    #. wait for mouse click or keyboard hitting
    #. close the graphics system (and graphics window)

2. Run the main function

  **note 1** : You must use easy_run() to run the main function.

  **note 2** : init_graph() must be called before any easygraphics drawing functions.

  **note 3** : Don't forget to close_graph() to clean up the system after all drawing work is done.

  **note 4** : You can use the graphics window\'s close button to close the graphics system. But this may cause exception. (When there are unfinished drawing operations.）

.. code-block:: python

    from easygraphics import *

    def main():
        init_graph(800, 600)
        pause()
        close_graph()

    easy_run(main)