from easygraphics import *
from PyQt5.QtCore import Qt


def draw_with_line_style(x, y, style):
    set_line_style(eval(style))
    rect(x + 45, y + 20, x + 205, y + 180)
    set_line_style(LineStyle.SOLID_LINE)
    draw_rect_text(x + 20, y + 180, 210, 20, style, flags=Qt.AlignVCenter | Qt.AlignHCenter)
    img = create_image(172, 170)
    capture_screen(x + 40, y + 15, x + 215, y + 185, img)
    styles = style.split(".")
    img.save(styles[1].lower() + ".png")
    # img.close()


init_graph(750, 400)
set_font_size(14)
set_line_width(3)
draw_with_line_style(0, 0, 'LineStyle.SOLID_LINE')
draw_with_line_style(250, 0, 'LineStyle.DASH_LINE')
draw_with_line_style(500, 0, 'LineStyle.DOT_LINE')
draw_with_line_style(0, 200, 'LineStyle.DASH_DOT_LINE')
draw_with_line_style(250, 200, 'LineStyle.DASH_DOT_DOT_LINE')
draw_with_line_style(500, 200, 'LineStyle.NO_PEN')

pause()
close_graph()
