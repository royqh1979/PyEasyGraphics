"""
Use predefined colors

In this example, we use color name "red" to get red color.

"""
if __name__ == '__main__':
    from easygraphics import *

    init_graph(640, 480)

    # set color to read 将色彩设为红色
    set_color("red")
    draw_circle(300, 200, 100)
    pause()
