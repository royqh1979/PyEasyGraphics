from easygraphics import *

init_graph(800, 600)
# draw view port's border, to better see the effect of view port
# 给视口（view port)画个边框，以便观察视口的效果
set_color(Color.LIGHTGRAY)
draw_rect(100, 50, 300, 250)
set_color(Color.BLACK)
draw_text(50, 300, "set_view_port() with clip=True")
# set the view port , its size is 200*200
# 设置一个视口，其尺寸为200*200
set_view_port(100, 50, 300, 250)
# see the result circle's position and size
# 注意实际画出来的圆的位置和大小
set_color(Color.BLACK)
circle(100, 100, 50)
circle(100, 100, 100)
circle(100, 100, 120)

pause()

# the circle is zoomed, because we don't set logical window explicitlly,
# so the logical window's size is the same with the graphics window (800*600).
# When drawing, circle's radius is value on the logical window. And it's zoomed
# when mapping to the view port.

# now let's try set_window() with the logical window set in accordance with the view port
# 这次我们用set_window()手动将逻辑视窗设置为与视口大小一致
reset_view_port()
set_color(Color.LIGHTGRAY)
draw_rect(450, 50, 650, 250)
set_color(Color.BLACK)
draw_text(400, 300, "set_view_port() with clip=False")
set_view_port(450, 50, 650, 250, False)

set_color(Color.BLACK)
circle(100, 100, 50)
circle(100, 100, 100)
circle(100, 100, 120)


pause()

clear_view_port()

pause()
close_graph()
