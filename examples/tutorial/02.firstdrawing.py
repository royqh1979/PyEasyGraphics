"""
Fist drawing program
Let's draw a
"""
from easygraphics import *

init_graph(640, 480)
# 设置画图颜色，GREEN是颜色常数，详细可以查graphics.h对这个宏的定义的值
set_color(Color.RED)
# 画一直线，从(50,50)到(450,450)
line(0, 0, 640, 480)

pause()

close_graph()
