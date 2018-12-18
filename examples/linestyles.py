from easygraphics import *
from PyQt5.QtCore import Qt


def draw_with_line_style(x, y, style):
    set_line_style(eval(style))
    rect(x + 20, y + 20, x + 180, y + 180)
    set_line_style(LineStyle.SOLID_LINE)
    draw_rect_text(x + 20, y + 180, 160, 20, style, flags=Qt.AlignVCenter | Qt.AlignHCenter)


init_graph(800, 600)
set_font_size(14)

draw_with_line_style(0, 0, 'LineStyle.CENTER_LINE')
draw_with_line_style(200, 0, 'LineStyle.DASH_DOT_DOT_LINE')
draw_with_line_style(400, 0, 'LineStyle.DASH_DOT_LINE')
draw_with_line_style(600, 0, 'LineStyle.DASH_LINE')
draw_with_line_style(0, 200, 'LineStyle.DASHED_LINE')
draw_with_line_style(200, 200, 'LineStyle.DOT_LINE')
draw_with_line_style(400, 200, 'LineStyle.DOTTED_LINE')
draw_with_line_style(600, 200, 'LineStyle.NO_PEN')
draw_with_line_style(0, 400, 'LineStyle.NULL_LINE')
draw_with_line_style(200, 400, 'LineStyle.SOLID_LINE')
