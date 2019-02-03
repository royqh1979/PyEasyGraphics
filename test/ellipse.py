import time

from easygraphics import *

init_graph(600, 600)
set_render_mode(RenderMode.RENDER_AUTO)
ellipse(100, 100, 50, 50)
time.sleep(2)
pause()
close_graph()
