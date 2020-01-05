# https://codebus.cn/contributor/post/zrxrk-reversi
from PyQt5 import QtGui

from easygraphics import dialog

from easygraphics import *
from typing import List
import numpy as np

imgs:List[Image]=[]
map = np.zeros((8,8))
B=1
W=2
black = 0
white = 0
now = 0

def load_images():
    imgs.append(load_image("reversi/black_block.jpg"))
    imgs.append(load_image("reversi/white_block.jpg"))
    imgs.append(load_image("reversi/black_pieces_black_block.jpg"))
    imgs.append(load_image("reversi/black_pieces_white_block.jpg"))
    imgs.append(load_image("reversi/white_pieces_black_block.jpg"))
    imgs.append(load_image("reversi/white_pieces_white_block.jpg"))

def print_board():
    global black,white
    black = 0
    white = 0
    for x in range(8):
        for y in range(8):
            if map[x][y]==0:
                if (x+y)%2==1:
                    put_image(60*x,60*y,imgs[0])
                else:
                    put_image(60*x,60*y,imgs[1])
            elif map[x][y]==B:
                if (x+y)%2==1:
                    put_image(60*x,60*y,imgs[2])
                else:
                    put_image(60*x,60*y,imgs[3])
                black+=1
            elif map[x][y]==W:
                if (x+y)%2==1:
                    put_image(60*x,60*y,imgs[4])
                else:
                    put_image(60*x,60*y,imgs[5])
                white+=1

def print_current():
    set_fill_color(Color.WHITE)
    fill_rect(530,60,590,120)
    fill_rect(530,360,590,420)
    if now == B:
        put_image(530,60,imgs[3])
    else:
        put_image(530,360,imgs[4])

directions = (
    (1,0),
    (-1,0),
    (0,1),
    (0,-1),
    (1,1),
    (1,-1),
    (-1,1),
    (-1,-1)
)
def update(x:int, y:int, a:int):
    b = W if a==B else B
    map[x][y]=a
    for d in directions:
        x1=x+d[0]
        y1=y+d[1]
        if x1<0 or x1>=8:
            continue
        if y1<0 or y1>=8:
            continue
        if map[x1][y1]!=b:
            continue
        x2 = x1
        y2 = y1
        can_reverse = True
        while True:
            x2+=d[0]
            y2+=d[1]
            if x2<0 or x2>=8:
                break
            if y2<0 or y2>=8:
                break
            if map[x2][y2]==a:
                break
            if map[x2][y2]==0:
                can_reverse=False
                break
        if not can_reverse:
            continue
        x2=x
        y2=y
        while True:
            x2 += d[0]
            y2 += d[1]
            if x2<0 or x2>=8:
                break
            if y2<0 or y2>=8:
                break
            if map[x2][y2]==a:
                break
            map[x2][y2]=a
    print_board()

def judge(x:int,y:int,a:int)->bool:
    if map[x][y]!=0:
        return False
    b = W if a==B else B
    for d in directions:
        x1=x+d[0]
        y1=y+d[1]
        if x1<0 or x1>=8:
            continue
        if y1<0 or y1>=8:
            continue
        if map[x1][y1]!=b:
            continue
        x2 = x1
        y2 = y1
        can_reverse = True
        while True:
            x2+=d[0]
            y2+=d[1]
            if x2<0 or x2>=8:
                break
            if y2<0 or y2>=8:
                break
            if map[x2][y2]==a:
                break
            if map[x2][y2]==0:
                can_reverse=False
                break
        if can_reverse:
            return True
    return False

def losed(a:int)->None:
    for x in range(8):
        for y in range(8):
            if judge(x,y,a):
                return False
    return True


def finised()->None:
    if black+white == 64:
        return True
    return False

def show_result()->bool:
    if black > white:
        msg = f"黑: {black} 白: {black}，黑胜，是否重新开始？"
        result = dialog.get_yes_or_no(msg,"黑胜")
    elif black < white:
        msg = f"黑: {black} 白: {black}，白胜，是否重新开始？"
        result = dialog.get_yes_or_no(msg,"白胜")
    else:
        msg = f"黑: {black} 白: {black}，平局，是否重新开始？"
        result = dialog.get_yes_or_no(msg,"平局")
    return result

def play():
    global now
    map.fill(0)
    map[3][4]=map[4][3]=B
    map[3][3]=map[4][4]=W
    now=B
    print_board()
    print_current()
    while True:
        msg = get_click()
        if not is_run():
            break
        x=msg.x//60
        y=msg.y//60
        if judge(x,y,now):
            update(x,y,now)
            now = B if now == W else W
            print_current()
        if finised() or losed(W) or losed(B):
            break

def main():
    init_graph(640,480)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_background_color(Color.WHITE)
    load_images()
    while is_run():
        play()
        if is_run() and not show_result():
            break
    close_graph()

easy_run(main)