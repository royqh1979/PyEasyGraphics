from easygraphics import *

init_graph()
set_background_color(Color.LIGHT_GRAY)
clear_device()

set_color(Color.RED)
set_fill_color(Color.LIGHT_BLUE)
draw_circle(200, 200, 100)

img = get_target()
image = img.get_image()

pause()
close_graph()
