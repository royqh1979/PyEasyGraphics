# https://codebus.cn/zhaoh/post/screensaver-mystify
# 该程序模仿的 Windows 经典屏幕保护程序“变幻线”，并使用了面向对象技术编写，初学面向对象时可以作为参考。
#
# 程序中，由多个连续的节点构成一个顶点对象，由四个顶点构成一个多边形对象，主程序有两个多边形在各自运动。更详细的，请参考源代码。
import random
from typing import List

from easygraphics import *
from dataclasses import dataclass

WIDTH = 800
HEIGHT = 600
MAX_STEP = 9

@dataclass
class Point:
    x:int
    y:int

class Vertex:
    def __init__(self,count:int):
        self.step_x = random.choice([-1,1])*random.randint(1,MAX_STEP)
        self.step_y = random.choice([-1,1])*random.randint(1,MAX_STEP)
        self.points = []
        self.points.append(Point(random.randrange(WIDTH), random.randrange(HEIGHT)))
        self._index = 0
        for i in range(1,count):
            p = self.points[i-1]
            self.points.append(Point(p.x-self.step_x,p.y-self.step_y))

    def get_head(self):
        return self.points[self._index]

    def get_next(self):
        i = self._index+1
        if i >= len(self.points):
            i=0
        return self.points[i]

    def move(self):
        p_head = self.get_head()
        p_next = self.get_next()

        p_next.x = p_head.x + self.step_x
        p_next.y = p_head.y + self.step_y
        self._index += 1
        if self._index >= len(self.points):
            self._index = 0

        p = self.get_head()
        if p.x < 0:
            p.x = 0
            self.step_x = random.randint(1,MAX_STEP)
        elif p.x >= WIDTH:
            p.x = WIDTH-1
            self.step_x = -random.randint(1,MAX_STEP)
        if p.y < 0:
            p.y = 0
            self.step_y = random.randint(1,MAX_STEP)
        elif p.y >= HEIGHT:
            p.y = HEIGHT-1
            self.step_y = -random.randint(1,MAX_STEP)

class Polygon:
    def __init__(self,lines:int):
        self.color = color_hsl(random.randrange(360),255,127)
        self.vertex=[]
        for i in range(4):
            self.vertex.append(Vertex(lines))

    def move(self):
        # erase polygon tail
        set_color(Color.BLACK)
        move_to(self.vertex[3].get_next().x,self.vertex[3].get_next().y)
        for i in range(4):
            line_to(self.vertex[i].get_next().x,self.vertex[i].get_next().y)

        # move every vertex
        for i in range(4):
            self.vertex[i].move()

        # draw polygon head
        set_color(self.color)
        move_to(self.vertex[3].get_head().x,self.vertex[3].get_head().y)
        for i in range(4):
            line_to(self.vertex[i].get_head().x,self.vertex[i].get_head().y)

        # 1% chance to change color
        if random.randrange(100)==0:
            self.color = color_hsl(random.randrange(360),255,127)

def main():
    init_graph(WIDTH,HEIGHT)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_background_color(Color.BLACK)
    s1 = Polygon(7)
    s2 = Polygon(12)

    while is_run():
        s1.move()
        s2.move()
        delay_fps(30)

    close_graph()

easy_run(main)