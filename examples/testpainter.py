from easygraphics import *
from PyQt5.QtGui import *

init_graph(800, 600)

img = create_image(800, 600)
i = img.get_image()
p = QPainter()
p.begin(i)
p.drawRect(50, 50, 200, 200)

for e in range(1, 10):
    p1 = QPainter()
    p1.begin(i)
    p1.drawEllipse(e * 5, e * 5, 50, 50)
    p1.end()

p.end()

draw_image(0, 0, img)
