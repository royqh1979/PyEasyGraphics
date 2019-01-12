Music(Audio)
============
Easygraphics provides simple ways to play musics.

The following program shows how to use the functions in :doc:`easygraphics.music <../apis/easygraphics.music>` to play music:

.. code-block:: python

    from easygraphics.music import *
    from easygraphics.dialog import *

    # For legal reasons please prepare a music file by yourself
    load_music("test.mp3")
    play_music()
    show_message("ok!")
    close_music()

