.. :changelog:

History
===========
2.0.0-alpha1
------------
 * turn on anti-alias by default
 * remove floodfill() method (we won't use it)
 * remove background mask (it's seldom used and will slow down the drawing speed)

1.0.20
-----------
 * add: Image.copy() method
 * change: draw_image() add width/height parameters ( can copy image with scale)
 * change: only create direct image buffer view when using floodfill()

1.0.19
-----------
 * add: Image.scaled() method


1.0.18
-----------
 * add: put_image()
 * change: capture_screen()'s 3rd and 4th parameter to width and height
 * add: more FillStyle consts

1.0.17
-----------
 * fix: dialogs dosen't work in normal pyqt program
 * change: contains_control() -> contains_ctrl()
 * add: load_image() throw value error if the image file is not exist
 * fix: get_mouse_msg() / get_char() / get_key() not quit correctly when the graphics window is closed

1.0.16
-----------
 * add: set_antialiasing()
 * add: contains_control()/contains_alt()/contains_shit()/contains_meta()
 * change: get_mouse_message() now return a MouseMessage object
 * change: get_key() now return a KeyMessage object

1.0.15
-----------
 * change: use queue to store keyboard/mouse message
 * remove: set_message_outdate_duration()
 * change: now get_message() return 5 results instead of 4
 * add: clear_mouse_msg(), clear_key_msg(), clear_char_msg()
 * add: create_image_from_file()

1.0.14
-----------
 * fix: processing not working
 * fix: get_key() and has_kb_msg() not working
 * add: set_message_outdate_duration()
 * add: bezier_point and bezier_tangent functions
 * add: curve_point and curve_tanget functions
 * add more documents and examples

1.0.13.1
-----------
* fix: immediate mode not work
* fix: set_flip_y() dosen't work when reused after reset_transform()

1.0.13
----------
* add easy_run mode
* now the easy_run mode is the preferred mode to run easygraphics. It can work under Linux, macOS and windows.

1.0.12
----------
* fix: the drawing is not stopped immediately after the turtle window is closed()

1.0.11
----------
* fix: dialog get_username_password() hangs.
* fix: dialog get_color() not work
* fix: dialog show_html()/show_code()/show_text() not work

1.0.10
----------
* add: show_objects() now can show a DataFrame.

1.0.9
----------
* add: enable_sorting parameter in show_objects()

1.0.8
-----------
* fix: crash when show_objects() called successively.
* dialogs will close the auto-started qapplication instance when exception raised.

1.0.7
-----------
* fix: show_objects() don't show non-primitive-type properties correctly

1.0.6
------------
* change: get_open_file_name()/get_file_names()/get_save_file_name() now use native dialogs, to avoid
  crash on pyqt >= 5.11.3
* add: FileFilter const class, and filter parameter in get_open_file_name()/get_file_names()/get_save_file_name()

1.0.5
------------
* add: get_open_file_name() to dialog package.
* fix: get_open_file_name()/get_file_names()/get_save_file_name() not work
* change: get_open_file_name()/get_file_names()/get_save_file_name() return filename(s), instead of tuple


1.0.4
------------
* remove the y-flip setting in ortho_look_at(). If you want to flip y, use set_flip_y() instead


1.0.3
------------
* add: ortho_look_at() function to map 3d point to 2d
* add: isometric_projection() function to map 3d point to 2d from 45degree view port

1.0.2
------------
* add: press ctrl+shift+alt+F10 will create a snapshot of the graphics window.
    The snapshot is saved in the running folder.
* change: close turtle window will automatically close the animation of turtle moving.

1.0.1
-----------
* add: fps settings in easygraphics.processing module
* update: translations
* change: easygraphics.processing module now use functions in easygraphics modules to draw. (Remove duplication defines.)

1.0.0
-----------
* fix: hangs in inactive shell when init_graph again after close_graph()

0.10.1
-----------
* add: color_gray() function.
* change: change lines/polylines/polygon functions parameters
* add: curve() / draw_curve() to draw Catmull-Rom splines.
* add: curve_vertex() to define curve vertices.
* fix: crash when close_graph() and init_graph() again

0.10.0
------------
* change: reimplement close_graph(), simplifies graphics window close event processing.
* add: add begin_shape()/vertex()/bezier_vertex()/quadratic_vertex()/end_shape() functions to easygraphics.

0.9.24
------------
* add begin_recording()/add_record()/save_recording()/end_recording() to create animated png files.
* add ShapeMode consts
* add set_ellipse_mode() and set_rect_mode() to Image class
* add easygraphics.processing module
* fix: Image's save_settings()/restore_settings() now save most settings.
* update: ellipse_mode apply to arc/chord/pie shape drawings.
* add quadratic()/draw_quadratic() function to Image class and easygraphics.processing subpackage
* add begin_shape()/vertex()/bezier_vertex()/quadratic_vertex()/end_shape() function to Image class and easygraphics.processing subpackage
* change: bezier()/draw_bezier now use seperate coordinate values as paramter instead of list.
* add VertexType consts
* add: begin_shape() 's type parameter
* add: end_shape()'s close parameter
* fix: succesive dialog calls may crash the program
* add: fill_image() function to Image class


0.9.23
------------
* fix: frame jumping because of errors in delay_jfps()

0.9.22
-------------
* fix: turtle icon position error when translated.
* fix: hangs when running in qtconsole and spyder

0.9.21
-------------
* add: show_lists_table() to display data lists in table
* add: get_transform()/set_transform()/push_transform()/pop_transform()
* change to BSD license
* fix: close graphics window  when drawing in is_run() and delay_fps()/delay_jfps() loops not throw exception

0.9.20
-------------
* fix: successive dialog calls may crash program.

0.9.19.2
-------------
* fix: license description in readme

0.9.19.1
-------------
* fix: license description in setup.py

0.9.19
-------------
* change to MIT License

0.9.18
-------------
* add ImageWidget and TurtleWidget classes, to embed easygraphics in Qt Applications

0.9.17
-------------
easygraphics.turtle:

* add: is_out_of_window() to check if the turtle is out of the graphics window


0.9.16
-------------
* redefine pause() in turtle
* redefine is_run() in turtle
* fix: default turtle speed
* change: meaning of the turtle's move_arc() function's parameters
* add: move_ellipse() function in easygraphics.turtle package

0.9.15
-------------
* fix package error in setup.py
* change turtle's default speed to 10

0.9.14
-------------
* add: move_arc() function to move turtle in arc

0.9.13
-------------
* add:  set_fill_rule() / get_fill_rule() function, to control how the polygons
  are filled.
* add:  FillRule consts
* Finish chinese translations for apis.
* fix: filling glitches in end_fill()

0.9.12
-------------
* Revert 0.9.11 's angle system change. Keep arc/pie/chord compatible with BGI.
* add show_image() function, to display drawings in the jupyter qtconsole or notebook.
* add show_image_dialog() function, to display a qimage in the dialog.

0.9.11
-------------
* fix: now arc/pie/chord drawing functions has the same angle system with rotate()

0.9.10
-------------
* add: easygraphics.turtle package which implements the turtle graphics.
* change: now rotate()/skew() can transform around any point
* change: now reflect() can using lines not passing the origin as the reflecting axis.

0.9.9
-------------
* add set_flip_y() to make y-axis grows bottom-up. (use reflect() will make texts
  get reflected too.)


0.9.8.1
-------------
* fix: legacy and music subpackage not packed in the binary distributions.

0.9.8
-------------
* fix: delay_fps() now work properly in Manual render mode
* finish chinese translations for tutorials

0.9.7
-------------
* add: load_image() to load image from files
* add: to_alpha() to make a transparently color
* change: use Source Over as the default composition mode (the same with Qt)
* more tutorials
* add: show_table() to display table infomation in a dialog
* change: rename mouse_msg() to has_mouse_msg()
* change: rename kb_hit() to has_kb_hit()
* change: rename get_mouse() to get_mouse_msg()
* change: rename kb_msg() to has_kb_msg()
* finish the tutorials.

0.9.6
-------------
* add: reflection (mirror/flip) and shear (skew) operations.

0.9.5
-------------
* add: headless mode support (no graphics window mode, use it to draw pictures)

0.9.4
-------------
* add: easygraphics.legacy package to better compatible with old BGI programs.
* add: get_click() function to get mouse click event
* change: background implementation to make set_background_color() work correctly
* add: now can use name ("red"), color string ("#ff0000), integer color rgb value (0xff0000) \
    in set_color(), set_fill_color(), set_background_color() functions
* add: cymk() and hsv() to get CYMK and HSV format color
* more tutorials

0.9.3
-------------
* fix : Readme

0.9.2
-------------
* add: easygraphics functions can run in the interactive mode (eg. IPython) correctly
* add: dialogs (in **easygraphics.dialog** package, adopted from
    `easygui_qt <https://github.com/aroberge/easygui_qt/>`_ )
* add: create and save to/from file
* add image transforms (translate/rotate/scale)
* add view port support
* add sphinx docs
* upload docs to readthedocs.org

0.9.1
-------------
* add readme text
* add delay_fps() and rgb() functions

0.9.0
-------------
* add keyboard and mouse message check and handle
* add simple dialogs ( from EasyGUI-Qt (https://github.com/aroberge/easygui_qt) and qtutils (https://bitbucket.org/philipstarkey/qtutils))


0.1.0
-------------
* First release on github
