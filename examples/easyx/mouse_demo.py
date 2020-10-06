# a demo from EasyX Library
# mouse demo
# https://codebus.cn/yangw/post/mouse-operation

from easygraphics import *

def main():
    init_graph()

    while is_run():
        if has_mouse_msg():
            m = get_mouse_msg()
            if m.type == MouseMessageType.PRESS_MESSAGE:
                if contains_left_button(m.button):
                    # left button is down
                    if contains_ctrl(m.modifiers):
                        # draw big square
                        rect(m.x-10,m.y-10,m.x+10,m.y+10)
                    else:
                        # draw little square
                        rect(m.x-5,m.y-5,m.x+5,m.y+5)
                elif contains_right_button(m.button):
                    # right button is down, quit
                    break
        else:
            # draw red dots when mouse is moving
            x,y = get_cursor_pos()
            put_pixel(x,y,Color.RED)

easy_run(main)