import time
import random

from PyQt5 import QtCore

from easygraphics import *
import winsound

UP = 8
RIGHT = 4
DOWN = 2
LEFT = 1


class Snake:
    def __init__(self):
        self.dsp = 20
        self.n = 5
        self.prev = 4
        i = self.n
        self.pos = [ [0,0] for x in range(100)]
        while i>=0:
            self.pos[i][0] = 201 + (self.n - i - 1) * self.dsp
            self.pos[i][1] = 301
            i-=1
        self.strtX = 21
        self.strtY = 21
        self.endX = 481
        self.endY = 361
        self.colr = 14
        self.now = self.prev
        self.dsp = 20
        self.stp = 1
        self.cnt = -1
        self.scr = 0
        self.dly = 150
        self.xr = 3
        self.yr = 9
        self.v1=0
        self.v2=0
        self.p1=0
        self.p2=0
        self.generate_egg()
        self.egGen = 1
        self.score()
        old_color = get_color()
        set_line_style(LineStyle.DASH_DOT_DOT_LINE)
        set_color(Color.RED)
        rect(self.strtX-15, self.strtY-15, self.endX+15, self.endY+15)
        rect(self.endX+25, self.strtY-15, get_width()-15, self.endY+15)
        rect(self.strtX-15, self.endY+25, get_width()-15, get_height()-5)
        line(self.endX+25, self.strtY+75, get_width()-15, self.strtY+75)
        line(self.endX+25, self.strtY+200, get_width()-15, self.strtY+200)
        line(self.endX+25, self.strtY+275, get_width()-15, self.strtY+275)
        # set_line_style(0, 1, 1)
        # settextstyle(8,0,1);
        set_color(Color.BLUE)
        draw_text(514, 40, "SCORE")
        set_color(Color.GREEN)
        # set_text_style(11, 0, 5);
        draw_text(524, 110, " CONTROLS ")
        draw_text(522, 135, "p = PAUSE")
        draw_text(522, 155, "g = RESUME")
        draw_text(522, 175, "e = EXIT")
        draw_text(513, 195, "ARROWS")
        draw_text(512, 205, "    -MOVEMENT")
        set_color(Color.LIGHT_RED)
        #settextstyle(4, 0, 9)
        draw_text(get_width()-500, get_height()-110, "SNAKE")
        #settextstyle(8, 0, 1)
        set_color(old_color)

    def checkEgg(self)->bool:
        if (self.e1 == self.p1)  and (self.e2 == self.p2):
            self.sndEt()
            self.generate_egg()
            self.dly-=1
            self.score()
            self.n+=1
    def sndEt(self):
        winsound.Beep(2500,2)

    def sndCgt(self):
        for x in range(1000,0,-1):
            winsound.Beep(x,1)

    def score(self):
        #settextstyle(8,0,1);
        set_color(Color.WHITE)
        draw_text(585,40,self.scr)
        if self.egGen != 1:
            self.scr = self.scr + self.dly / 10
        set_color(Color.RED)
        draw_text(585,40,self.scr)

    def gnrtCond(self):
        if self.n>=367:
            return
        if self.now == UP and self.prev != UP and self.prev != DOWN:
            self.pos[0][0] = self.p1
            self.pos[0][1] = self.p2 - self.dsp
            self.prev = self.now
        elif self.now == RIGHT and self.prev != RIGHT and self.prev != LEFT:
            self.pos[0][0] = self.p1 + self.dsp
            self.pos[0][1] = self.p2
            self.prev = self.now
        elif self.now == DOWN and self.prev != UP and self.prev != DOWN:
            self.pos[0][0] = self.p1
            self.pos[0][1] = self.p2 + self.dsp
            self.prev = self.now
        elif self.now == LEFT and self.prev != LEFT and self.prev != RIGHT:
            self.pos[0][0] = self.p1 - self.dsp
            self.pos[0][1] = self.p2
            self.prev = self.now

    def gnrtUnCond(self):
        if self.prev == UP :
            self.pos[0][0] = self.p1
            self.pos[0][1] = self.p2 - self.dsp
        if self.prev == RIGHT :
            self.pos[0][0] = self.p1 + self.dsp
            self.pos[0][1] = self.p2
        if self.prev == DOWN :
            self.pos[0][0] = self.p1
            self.pos[0][1] = self.p2 + self.dsp
        if self.prev == LEFT :
            self.pos[0][0] = self.p1 - self.dsp
            self.pos[0][1] = self.p2
        self.p1 = self.pos[0][0]
        self.p2 = self.pos[0][1]

    def check(self):
        if self.p1 > self.endX:
            self.p1 = self.strtX
        elif self.p1 < self.strtX:
            self.p1 = self.endX
        if self.p2 > self.endY:
            self.p2 = self.strtY
        elif self.p2 < self.strtY:
            self.p2 = self.endY
        self.pos[0][0] = self.p1
        self.pos[0][1] = self.p2
        for i in range(1,self.n):
            if self.p1 == self.pos[i][0] and self.p2 == self.pos[i][1]:
                self.caught()
                break

    def show(self):
        old_color = get_color()
        if self.egGen != 1:
            set_color(get_background_color())
            # setfillstyle(1,getbkcolor())
            set_fill_color(get_background_color())
            fill_ellipse(self.v1,self.v2,self.yr,self.yr)
        else:
            self.egGen = 0
        if self.egGen == 2:
            self.egGen-=1
        set_color(self.colr)
        #setfillstyle(1,9)
        set_fill_color(Color.LIGHT_BLUE)
        if self.now == 8 or  self.now == 2:
            fill_ellipse(self.pos[0][0],self.pos[0][1],self.xr,self.yr)
        elif self.now == 4 or self.now == 1:
            fill_ellipse(self.pos[0][0],self.pos[0][1],self.yr,self.xr)
        set_color(old_color)

    def transpose(self):
        self.p1 = self.pos[0][0]
        self.p2 = self.pos[0][1]
        if self.egGen==0:
            self.v1 = self.pos[self.n-1][0]
            self.v2 = self.pos[self.n-1][1]
        else:
            self.egGen = 0
        i=self.n-1
        while i>=1:
            self.pos[i][0] = self.pos[i - 1][0]
            self.pos[i][1] = self.pos[i - 1][1]
            i-=1

    def move(self):
        st = 0
        while is_run():
            if not has_kb_msg():
                self.checkEgg()
                if st == 0:
                    self.show()
                else:
                    st = 0
                delay(self.dly//4)
                self.transpose()
                delay(self.dly//4)
                self.gnrtUnCond()
                delay(self.dly//4)
                self.check()
            elif self.stp!=0:
                self.chngDir()
                self.gnrtCond()
                self.check()
                self.show()
                st == 1
            if self.stp == 0:
                break

    def caught(self):
        self.stp = 0
        self.sndCgt()
        for i in range(7):
            if i %2 !=0:
                set_color(Color.LIGHT_GREEN)
                draw_text(512,250,"GAME OVER")
                delay(900)
            else:
                set_color(Color.BLACK)
                draw_text(512,250,"GAME OVER")
                delay(500)
        delay(1000)

    def chngDir(self):
        x,modifiers = get_key()
        if x == QtCore.Qt.Key_Up:
            self.now = UP
        elif x == QtCore.Qt.Key_Right:
            self.now = RIGHT
        elif x == QtCore.Qt.Key_Down:
            self.now = DOWN
        elif x == QtCore.Qt.Key_Left:
            self.now = LEFT
        elif x == QtCore.Qt.Key_E:
            self.caught()
        elif x == QtCore.Qt.Key_P:
            # PAUSE
            self.pause()

    def pause(self):
        twnkl = True
        old_size = get_font_size()
        set_font_size(9)
        while is_run():
            if has_kb_hit():
                x,modifiers=get_key()
                if x == QtCore.Qt.Key_G:
                    old_color = get_color()
                    set_color(Color.BLACK)
                    rect(self.endX+40,self.endY-10,self.getmaxx()-35,self.getmaxy()-160)
                    draw_text(self.endX+60,self.endY-29,"PAUSE")
                    set_color(old_color)
                    break
            else:
                if twnkl:
                    old_clr = get_color()
                    set_color(Color.LIGHT_GREEN)
                    rect(self.endX+40,self.endY-10,get_width()-35,get_height()-160)
                    draw_text(self.endX+60,self.endY-29,"PAUSE")
                    set_color(old_clr)
                    delay(1000)
                else:
                    old_clr = get_color()
                    set_color(Color.BLACK)
                    rect(self.endX+40,self.endY-10,get_width()-35,get_height()-160)
                    draw_text(self.endX+60,self.endY-29,"PAUSE")
                    set_color(old_clr)
                    delay(1000)
            twnkl=not twnkl
        set_font_size(old_size)

    def generate_egg(self):
        """
        Generate an egg
        """
        while True:
            self.e1 = random.randrange(0,100) * self.dsp + self.strtX
            self.e2 = random.randrange(0,100) * self.dsp + self.strtY
            if self.is_egg_valid():
                break
        old_color = get_color()
        set_color(Color.LIGHT_GRAY)
        set_fill_color(Color.Values[random.randrange(len(Color.Values))])
        fill_ellipse(self.e1,self.e2,self.xr+2,self.xr+2)
        set_color(old_color)
        self.egGen = 2;

    def is_egg_valid(self) -> bool:
        if self.e1 >= self.endX + 1 or self.e2 >= self.endY + 1:
            return False
        if self.v1 == self.e1 and self.v2 == self.e2:
            return False
        for i in range(self.n):
            if self.e1 == self.pos[i][0] and self.e2 == self.pos[i][1]:
                return False
        return True

def main():
    init_graph(800,600)
    set_render_mode(RenderMode.RENDER_MANUAL)
    snake = Snake()
    snake.move()
    close_graph()


easy_run(main)