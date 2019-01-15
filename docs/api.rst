API
====================

Subpackages
-----------

.. toctree::

    apis/easygraphics.dialog
    apis/easygraphics.legacy
    apis/easygraphics.music
    apis/easygraphics.turtle
    apis/easygraphics.widget

Package Summary
---------------

System init and close
^^^^^^^^^^^^^^^^^^^^^
.. currentmodule:: easygraphics

.. autosummary::

    close_graph
    init_graph

Drawing Settings
^^^^^^^^^^^^^^^^
.. currentmodule:: easygraphics

.. autosummary::

    get_background_color
    get_color
    get_composition_mode
    get_drawing_pos
    get_fill_color
    get_fill_rule
    get_fill_style
    get_font
    get_font_size
    get_height
    get_line_style
    get_line_width
    get_width
    get_write_mode
    get_drawing_x
    get_drawing_y
    reset_view_port
    reset_window
    restore_settings
    save_settings
    set_background_color
    set_caption
    set_clip_rect
    set_clipping
    set_color
    set_composition_mode
    set_fill_color
    set_fill_rule
    set_fill_style
    set_font
    set_font_size
    set_line_style
    set_line_width
    set_view_port
    set_window
    set_write_mode
    text_height
    text_width

Basic Drawing
^^^^^^^^^^^^^

.. currentmodule:: easygraphics

.. autosummary::

    arc
    bezier
    chord
    circle
    clear_device
    clear_view_port
    draw_arc
    draw_bezier
    draw_chord
    draw_circle
    draw_ellipse
    draw_line
    draw_lines
    draw_pie
    draw_point
    draw_poly_line
    draw_polygon
    draw_rect
    draw_rect_text
    draw_rounded_rect
    draw_text
    ellipse
    fill_chord
    fill_circle
    fill_ellipse
    fill_pie
    fill_polygon
    fill_rect
    fill_rounded_rect
    flood_fill
    get_pixel
    line
    line_rel
    line_to
    lines
    move_rel
    move_to
    pie
    poly_line
    polygon
    put_pixel
    rect
    rounded_rect


Transform
^^^^^^^^^

.. currentmodule:: easygraphics

.. autosummary::

    flip
    get_transform
    mirror
    pop_transform
    push_transform
    reflect
    reset_transform
    rotate
    scale
    set_flip_y
    set_origin
    set_transform
    shear
    skew
    translate

Animation
^^^^^^^^^

.. currentmodule:: easygraphics

.. autosummary::

    delay
    delay_fps
    delay_jfps
    get_render_mode
    is_run
    set_render_mode

Image Processing
^^^^^^^^^^^^^^^^
.. currentmodule:: easygraphics

.. autosummary::

    add_record
    begin_recording
    capture_screen
    close_image
    create_image
    draw_image
    end_recording
    get_target
    load_image
    put_image
    save_image
    save_recording
    set_target

Keyboard and Mouse
^^^^^^^^^^^^^^^^^^
.. currentmodule:: easygraphics

.. autosummary::

    contains_left_button
    contains_mid_button
    contains_right_button
    get_char
    get_click
    get_cursor_pos
    get_key
    get_mouse_msg
    has_kb_hit
    has_kb_msg
    has_mouse_msg
    pause

Color & utilities
^^^^^^^^^^^^^^^^^
.. currentmodule:: easygraphics

.. autosummary::

    cart2pol
    color_cmyk
    color_hsv
    color_rgb
    pol2cart
    rgb
    show_image
    to_alpha


Constants
^^^^^^^^^
.. currentmodule:: easygraphics

.. autosummary::

    Color
    CompositionMode
    FillStyle
    FillRule
    LineStyle
    MouseMessageType
    RenderMode
    TextFlags

API Details
-----------

.. automodule:: easygraphics
    :members:
    :undoc-members:

