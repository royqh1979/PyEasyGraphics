easygraphics.dialog package
===========================
An easy-to-use dialogs library.

You can use it to create and show dialogs.

Based on code from EasyGUI_Qt(https://github.com/aroberge/easygui_qt/). The original EasyGUI-Qt
library won't work properly with EasyGraphics. So use this library instead.

A simple example:

>>> from easygraphics.dialog import *
>>> name=get_string("name")
>>> show_message("Your name is "+name)

Function list
-------------
.. currentmodule:: easygraphics.dialog

.. autosummary::

    get_choice
    get_color
    get_color_hex
    get_color_rgb
    get_continue_or_cancel
    get_date
    get_directory_name
    get_file_names
    get_float
    get_int
    get_list_of_choices
    get_many_strings
    get_new_password
    get_password
    get_save_file_name
    get_string
    get_username_password
    get_yes_or_no
    set_dialog_font_size
    show_message
    show_image_dialog
    show_text
    show_table
    show_code
    show_file

Functions
---------
.. automodule:: easygraphics.dialog
    :members:
    :undoc-members:
