from easygraphics import *

init_graph(headless=True)
img = create_image(800, 600)

set_target(img)
set_fill_color(Color.RED)
draw_circle(200, 200, 50)

save_image("test.png")
close_image(img)
close_graph()
