"""
Draw a color table
"""
from PyQt5.QtCore import Qt

_x = 0
_y = 0
_width = 200
_height = 70


def draw_color(color_str):
    global _x, _y
    color = eval(color_str)
    set_fill_color(color)
    draw_rect(_x + 5, _y + 5, _x + _width - 5, _y + _height - 25)
    draw_rect_text(_x, _y + _height - 25, _width, 20, color_str, flags=Qt.AlignCenter)
    _x += _width
    if _x + _width > get_width():
        _x = 0
        _y += _height


if __name__ == "__main__":
    from easygraphics import *

    init_graph(600, 560)

    draw_color("Color.BLACK")
    draw_color("Color.DARK_GRAY")
    draw_color("Color.LIGHT_GRAY")

    draw_color("Color.BLUE")
    draw_color("Color.LIGHT_BLUE")
    draw_color("Color.DARK_BLUE")

    draw_color("Color.GREEN")
    draw_color("Color.LIGHT_GREEN")
    draw_color("Color.DARK_GREEN")

    draw_color("Color.CYAN")
    draw_color("Color.LIGHT_CYAN")
    draw_color("Color.DARK_CYAN")

    draw_color("Color.RED")
    draw_color("Color.LIGHT_RED")
    draw_color("Color.DARK_RED")

    draw_color("Color.MAGENTA")
    draw_color("Color.LIGHT_MAGENTA")
    draw_color("Color.DARK_MAGENTA")

    draw_color("Color.YELLOW")
    draw_color("Color.LIGHT_YELLOW")
    draw_color("Color.DARK_YELLOW")

    draw_color("Color.BROWN")
    draw_color("Color.WHITE")
    draw_color("Color.TRANSPARENT")

    pause()
    save_image("consts-color.jpg")
    close_graph()
