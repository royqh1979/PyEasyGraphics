Dialogs
=======
Easygraphics provides many predefined dialogs to communicate with user interactively.

Output Dialogs
-------------
.. currentmodule:: easygraphics.dialog

.. autosummary::

    show_html
    show_image_dialog
    show_lists_table
    show_message
    show_objects
    show_text
    show_table
    show_code
    show_file

Input Dialogs
--------------
.. currentmodule:: easygraphics.dialog

.. autosummary::

    get_choice
    get_color
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


In the following program, click the graphics window to open a color dialog, select a color and set it as the background.

.. code-block:: python

    from easygraphics import *
    from easygraphics.dialog import *

    init_graph(600,400)
    set_render_mode(RenderMode.RENDER_MANUAL)

    while is_run():
        if has_mouse_msg():
            x,y,type,buttons = get_mouse_msg()
            if type == MouseMessageType.PRESS_MESSAGE:
                color = get_color(get_background_color())
                set_background_color(color)
        delay_fps(60)

    close_graph()



