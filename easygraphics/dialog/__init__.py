"""
An easy-to-use dialogs library.

You can use it to create and show dialogs.

Based on code from EasyGUI_Qt(https://github.com/aroberge/easygui_qt/). The original EasyGUI-Qt
library won't work properly with EasyGraphics. So use this library instead.

A simple example:

>>> from easygraphics.dialog import *
>>> name=get_string("name")
>>> show_message("Your name is "+name)
"""
from .dialog import *

__all__ = dialog.__all__
