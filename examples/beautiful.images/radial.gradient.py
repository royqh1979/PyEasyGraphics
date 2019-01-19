"""
Radial Gradient

Adapted form "Processing Creative Coding and Computational Art", Page 88.
"""
from easygraphics import *

init_graph(500, 500)
set_background_color("black")

for i in range(256):
    set_fill_color(color_gray(i))
    fill_ellipse(get_width() // 2, get_height() // 2, 256 - i, 256 - i)

pause()
close_graph()
