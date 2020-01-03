import os
import time
import random

from PyQt5 import QtCore

from easygraphics import *
import winsound

UP = 8
RIGHT = 4
DOWN = 2
LEFT = 1

GRID_SIZE = 20

START_X = 21
START_Y = 21
END_X = 481
END_Y = 361

SNAKE_COLOR = Color.YELLOW

SNAKE_SIZE_X = 3
SNAKE_SIZE_Y = 9

class Snake:
    def __init__(self):
        self.length = 5
        self.now = RIGHT
        self.prev = self.now
        self.pos = [ [0,0] for x in range(100)]
        for i in range(self.length):
            self.pos[i][0] = 201 + (self.length - i - 1) * GRID_SIZE
            self.pos[i][1] = 301
        self.caught = False
        self.score = 0
        self.delay_time = 150
        self.generate_egg()
        self.egGen = 1
        old_color = get_color()
        set_line_style(LineStyle.DASH_DOT_DOT_LINE)
        set_color(Color.RED)
        rect(START_X - 15, START_Y - 15, END_X + 15, END_Y + 15)
        rect(END_X + 25, START_Y - 15, get_width() - 15, END_Y + 15)
        rect(START_X - 15, END_Y + 25, get_width() - 15, get_height() - 5)
        line(END_X + 25, START_Y + 75, get_width() - 15, START_Y + 75)
        line(END_X + 25, START_Y + 200, get_width() - 15, START_Y + 200)
        line(END_X + 25, START_Y + 275, get_width() - 15, START_Y + 275)
        set_color(Color.BLUE)
        draw_text(514, 40, "SCORE")
        set_color(Color.GREEN)
        draw_text(524, 110, " CONTROLS ")
        draw_text(522, 135, "e = QUIT")
        draw_text(522, 155, "ARROWS - MOVEMENT")
        set_color(Color.LIGHT_RED)
        draw_text(get_width()-500, get_height()-110, "SNAKE")
        set_color(old_color)
        self.display_score()

    def check_eat_egg(self)->bool:
        if (self.e1 == self.pos[0][0])  and (self.e2 == self.pos[0][1]):
            self.sound_eat()
            self.generate_egg()
            self.delay_time-=1
            self.update_score()
            self.length+=1

    def sound_eat(self):
        if os.name == 'nt':
            winsound.Beep(2500,2)

    def sound_caught(self):
        if os.name == 'nt':
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

    def update_score(self):
        #settextstyle(8,0,1);
        self.score = self.score + self.delay_time // 10
        self.display_score()

    def display_score(self):
        set_fill_color(get_background_color())
        fill_rect(585, 20, 700,50)
        set_color(Color.RED)
        draw_text(585, 40, self.score)

    def update_head_position(self):
        if self.prev == UP :
            self.pos[0][1] -= GRID_SIZE
        if self.prev == RIGHT :
            self.pos[0][0] += GRID_SIZE
        if self.prev == DOWN :
            self.pos[0][1] += GRID_SIZE
        if self.prev == LEFT :
            self.pos[0][0] -= GRID_SIZE

    def check(self):
        if self.is_caught():
            self.do_caught()

    def is_caught(self):
        x=self.pos[0][0]
        y=self.pos[0][1]
        if x > END_X:
            return True
        elif x < START_X:
            return True
        if y > END_Y:
            return True
        elif y < START_Y:
            return True
        for i in range(1, self.length):
            if x == self.pos[i][0] and y == self.pos[i][1]:
                return True
        return False


    def show(self):
        # erase tail
        set_fill_color(get_background_color())
        fill_ellipse(self.pos[self.length-1][0], self.pos[self.length-1][1], SNAKE_SIZE_Y, SNAKE_SIZE_Y)

        #erase head background
        set_fill_color(get_background_color())
        fill_ellipse(self.pos[0][0],self.pos[0][1], SNAKE_SIZE_Y, SNAKE_SIZE_Y)

        # draw head
        set_fill_color(SNAKE_COLOR)
        if self.now == UP or  self.now == DOWN:
            fill_ellipse(self.pos[0][0],self.pos[0][1],SNAKE_SIZE_X,SNAKE_SIZE_Y)
        elif self.now == RIGHT or self.now == LEFT:
            fill_ellipse(self.pos[0][0],self.pos[0][1],SNAKE_SIZE_Y,SNAKE_SIZE_X)

    def update_body_pos(self):
        i= self.length - 1
        while i>=1:
            self.pos[i][0] = self.pos[i - 1][0]
            self.pos[i][1] = self.pos[i - 1][1]
            i-=1

    def move(self):
        while is_run():
            self.prev = self.now
            if has_kb_msg():
                self.check_keys()
                self.correct_direction()
            self.update_head_position()
            self.check()
            if self.caught:
                break
            self.check_eat_egg()
            self.update_body_pos()
            self.show()
            delay(self.delay_time)

    def on_y(self,direction):
        if direction == DOWN or direction == UP:
            return True
        return False

    def on_x(self,direction):
        if direction == LEFT or direction == RIGHT:
            return True
        return False

    def same_direction(self,dir1,dir2):
        if self.on_x(dir1) and self.on_x(dir2):
            return True
        if self.on_y(dir1) and self.on_y(dir2):
            return True
        return False

    def correct_direction(self) -> None:
        """
        If the new direction is not valid, reset it to previous direction

        """
        if self.same_direction(self.now,self.prev):
            self.now=self.prev

    def do_caught(self):
        self.caught = True
        self.sound_caught()
        for i in range(7):
            if i %2 !=0:
                set_color(Color.LIGHT_GREEN)
                draw_text(512,250,"GAME OVER")
                delay(900)
            else:
                set_fill_color(get_background_color())
                fill_rect(512,230,612,250)
                delay(500)
        delay(1000)

    def check_keys(self):
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
            self.caught = True

    def generate_egg(self):
        """
        Generate an egg
        """
        while True:
            self.e1 = random.randrange(0,100) * GRID_SIZE + START_X
            self.e2 = random.randrange(0,100) * GRID_SIZE + START_Y
            if self.is_egg_valid():
                break
        old_color = get_color()
        set_color(Color.LIGHT_GRAY)
        set_fill_color(Color.Values[random.randrange(1,len(Color.Values))])
        fill_ellipse(self.e1,self.e2,SNAKE_SIZE_X+2,SNAKE_SIZE_X+2)
        set_color(old_color)

    def is_egg_valid(self) -> bool:
        if self.e1 >= END_X + 1 or self.e2 >= END_Y + 1:
            return False
        for i in range(self.length):
            if self.e1 == self.pos[i][0] and self.e2 == self.pos[i][1]:
                return False
        return True

def main():
    init_graph(800,600)
    set_background_color(Color.BLACK)
    set_render_mode(RenderMode.RENDER_MANUAL)
    snake = Snake()
    snake.move()
    close_graph()


easy_run(main)