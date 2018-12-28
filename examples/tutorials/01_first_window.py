"""
First easy graphics program

In this program, we will:

1. Init the graphics windows
#. wait for mouse click or keyboard hitting
#. close the graphics system (and graphics window)

  **note 1** : init_graph() must be called before any easygraphics drawing functions.

  **note 2** : Don't forget to close_graph() to clean up the system after all drawing work is done.

  **note 3** : You can use the graphics window\'s close button to close the graphics system. But
   this may cause exception. (When there are unfinished drawing operations.）

"""
if __name__ == '__main__':
    from easygraphics import *

    init_graph(800, 600)
    pause()
    close_graph()
