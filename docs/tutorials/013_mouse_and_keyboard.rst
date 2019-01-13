Mouse and Keyboard
==================
Often we need to get input from the user in the programs. Easygrphics provides simple ways to get user's input
from keyboard and mouse.

Pause for input
---------------
The most used user input function in Easygraphics is pause(). This function pause the program, and
wait for user to click on the graphics window, or press any key, then continue the program.

Mouse Clicking
--------------
We can use get_click() to pause the program and wait for a mouse clicking. This function will
return the x,y coordinates of the position clicked, and buttons that are pressed when clicking.

.. code-block:: python

    from easygraphics import *
    init_graph(800,600)
    set_render_mode(RenderMode.RENDER_MANUAL)

    while is_run():
        x,y,buttons=get_click()
        str="clicked on %d,%d ."%(x,y)
        if contains_left_button(buttons):
            str+=" left button down"
        if contains_right_button(buttons):
            str+=" right button down"
        if contains_mid_button(buttons):
            str+=" mid button down"
        clear_device()
        draw_text(0,600,str)

    close_graph()

Cursor Positions
----------------
Sometimes we need to get the position of the cursor. We can use get_cursor_pos() to get this job done.

The following program continuously displays mouse cursor's position.

.. code-block:: python

    from easygraphics import *

    init_graph(800, 600)
    set_render_mode(RenderMode.RENDER_MANUAL)

    while is_run():
        if delay_fps(30):
            x, y = get_cursor_pos()
            clear_device()
            draw_text(0, 600, "%d,%d" % (x, y))

    close_graph()

Mouse Button Press and Release
------------------------------
You can use get_mouse_msg() to get mouse button press and release messages.

Non-Blocking mouse processing
-----------------------------
get_click()/get_mouse_msg() will block the program if there are no mouse press/click in the last 100ms. If you want to
check the mouse operation non-blockly, you could use the non-blocking function has_mouse_msg() to see if there
are any mouse messages, and then use get_mouse_msg() to get the mouse message.

The following program continuously check display cursor's postion and mouse button press/release events.

.. code-block:: python

    from easygraphics import *

    init_graph(800, 600)
    set_render_mode(RenderMode.RENDER_MANUAL)

    set_fill_color("white")
    while is_run():
        if delay_fps(30):
            x, y = get_cursor_pos()
            fill_rect(0, 580, 390, 600)
            draw_text(0, 600, "%d,%d" % (x, y))
            if has_mouse_msg():
                x, y, type, buttons = get_mouse_msg()
                if type == MouseMessageType.PRESS_MESSAGE:
                    typestr = "pressed"
                else:
                    typestr = "released"
                fill_rect(400, 580, 800, 600)
                draw_text(400, 600, "button %s at %d,%d" % (typestr, x, y))

    close_graph()

Mouse Message Demo
------------------

The following program draws a bezier curve interactively

First click on the window to set the first control point of the curve.
Then click on the window to set the second control point of the curve.
Then drag from any of the above two control points to set the third and the fourth control point.

.. code-block:: python

    from easygraphics import *
    from PyQt5 import QtCore

    init_graph(800, 600)
    set_render_mode(RenderMode.RENDER_MANUAL)

    x1, y1, buttons = get_click()
    circle(x1, y1, 3)
    x2, y2, buttons = get_click()
    circle(x2, y2, 3)
    line(x1, y1, x2, y2)

    x3, y3 = x1, y1
    x4, y4 = x2, y2
    reg1 = QtCore.QRect(x1 - 2, y1 - 2, 5, 5)
    reg2 = QtCore.QRect(x2 - 2, y2 - 2, 5, 5)
    draging_which_point = 0
    while is_run():
        if delay_fps(60):
            if draging_which_point == 1:
                draw_line(x1, y1, x, y)
                draw_bezier((x1, y1, x, y, x4, y4, x2, y2))
            elif draging_which_point == 2:
                draw_line(x2, y2, x, y)
                draw_bezier((x1, y1, x3, y3, x, y, x2, y2))

            if has_mouse_msg():
                x, y, type, buttons = get_mouse_msg()
                if type == MouseMessageType.PRESS_MESSAGE:
                    if reg1.contains(x, y):
                        draging_which_point = 1
                        set_color(Color.WHITE)
                        set_composition_mode(CompositionMode.SRC_XOR_DEST)
                        x, y = x3, y3
                    elif reg2.contains(x, y):
                        draging_which_point = 2
                        set_color(Color.WHITE)
                        set_composition_mode(CompositionMode.SRC_XOR_DEST)
                        x, y = x4, y4
                    else:
                        draging_which_point = 0
                elif type == MouseMessageType.RELEASE_MESSAGE:
                    if draging_which_point == 1:
                        x3, y3 = x, y
                    elif draging_which_point == 2:
                        x4, y4 = x, y
                    draging_which_point = 0

                    set_color(Color.BLACK)
                    set_composition_mode(CompositionMode.SOURCE)
                    clear_device()
                    draw_line(x1, y1, x3, y3)
                    draw_line(x2, y2, x4, y4)
                    circle(x1, y1, 3)
                    circle(x2, y2, 3)
                    draw_bezier((x1, y1, x3, y3, x4, y4, x2, y2))
            else:
                if draging_which_point == 1:
                    x, y = get_cursor_pos()
                    draw_line(x1, y1, x, y)
                    draw_bezier((x1, y1, x, y, x4, y4, x2, y2))
                elif draging_which_point == 2:
                    x, y = get_cursor_pos()
                    draw_line(x2, y2, x, y)
                    draw_bezier((x1, y1, x3, y3, x, y, x2, y2))

    close_graph()
Char Input
----------
We can use has_kb_hit() to see if there is any ascii char pressed, and use get_char() to get the inputted char.
has_kb_hit() is non-blocking, and get_char() is blocking.

The following program is a simple print game.

.. code-block:: python

    from easygraphics import *
    import random


    def show_welcome():
        clear_device()
        set_color("yellow")
        set_font_size(64)
        draw_text(160, 110, "Print Game");
        set_color("white");
        c = 0
        set_font_size(20)
        while not has_kb_hit():
            set_color(color_rgb(c, c, c))
            draw_text(180, 400, "Press any key to continue")
            c = (c + 8) % 255;
            delay_fps(30)
        ch = get_char()
        print(ch)
        clear_device()


    def show_goodbye():
        clear_device();
        set_color("yellow");
        set_font_size(48);
        draw_text(104, 180, "Bye!!!");
        pause()


    if __name__ == "__main__":
        init_graph(640, 480)
        set_render_mode(RenderMode.RENDER_MANUAL)
        set_background_color("black")

        show_welcome()
        random.seed()
        set_font_size(20)
        set_fill_color("black")

        while is_run():
            target = chr(65 + random.randint(0, 25))
            x = random.randint(0, 620)
            for y in range(16, 460):
                set_color("white")
                draw_text(x, y, target)
                if has_kb_hit():
                    key = get_char()
                    if key.upper() == target:
                        fill_rect(x - 2, y - 22, x + 22, y + 2)  # clear the char and generate next char
                        break
                    if key == " ":
                        show_goodbye()
                        close_graph()
                        exit()
                if delay_fps(60):
                    fill_rect(x - 2, y - 22, x + 22, y + 2)  # clear the char
                else:
                    break

        close_graph()

Key Pressed
-----------
We can use has_kb_msg() to see if there is any key pressed, and use get_key() to get the pressed key.
has_kb_msg() is non-blocking, and get_key() is blocking.




