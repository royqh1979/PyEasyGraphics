"""
A simple music play library.

You can use it to load and play music files.

A simple example:

>>> from easygraphics.music import *
>>> # For legal reasons please prepare a music file by yourself
>>> load_music("test.mp3")
>>> play_music()
>>> close_music()

"""
from .music import *

__all__ = music.__all__
