.. :changelog:

History
=======

0.9.5
---------------------
* add: headless mode support (no graphics window mode, use it to draw pictures)

0.9.4
---------------------
* add: easygraphics.legacy package to better compatible with old BGI programs.
* add: get_click() function to get mouse click event
* change: background implementation to make set_background_color() work correctly
* add: now can use name ("red"), color string ("#ff0000), integer color rgb value (0xff0000) \
    in set_color(), set_fill_color(), set_background_color() functions
* add: cymk() and hsv() to get CYMK and HSV format color
* more tutorials

0.9.3
---------------------
* fix : Readme

0.9.2
---------------------
* add: easygraphics functions can run in the interactive mode (eg. IPython) correctly
* add: dialogs (in **easygraphics.dialog** package, adopted from
    `easygui_qt <https://github.com/aroberge/easygui_qt/>`_ )
* add: create and save to/from file
* add image transforms (translate/rotate/scale)
* add view port support
* add sphinx docs
* upload docs to readthedocs.org

0.9.1
---------------------
* add readme text
* add delay_fps() and rgb() functions

0.9.0
---------------------
* add keyboard and mouse message check and handle
* add simple dialogs ( from EasyGUI-Qt (https://github.com/aroberge/easygui_qt) and qtutils (https://bitbucket.org/philipstarkey/qtutils))


0.1.0
---------------------
* First release on github
