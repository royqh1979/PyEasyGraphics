import copy
import random
import time
from dataclasses import dataclass
from enum import Enum, unique
from typing import List

import numpy as np
from PyQt5 import QtGui, QtCore

from easygraphics import *
from easygraphics import dialog

WIDTH = 10  # 游戏区宽度
HEIGHT = 22  # 游戏区高度
UNIT = 20  # 每个游戏区单位的实际像素
DROP_SPEED = 90  # 下落速度（帧数），60帧=1秒


@unique
class CMD(Enum):
    ROTATE = 1
    LEFT = 2
    RIGHT = 3
    DOWN = 4
    SINK = 5
    QUIT = 6


@unique
class DRAW(Enum):
    SHOW = 1
    CLEAR = 2
    FIX = 3


@dataclass
class Block:
    dir: List[List[int]]  # 方块的四个旋转状态
    color: QtGui.QColor  # 方块的颜色


g_blocks = []

# I
g_blocks.append(Block([
    [0, 0, 0, 0,
     1, 1, 1, 1,
     0, 0, 0, 0,
     0, 0, 0, 0],
    [0, 1, 0, 0,
     0, 1, 0, 0,
     0, 1, 0, 0,
     0, 1, 0, 0],
    [0, 0, 0, 0,
     1, 1, 1, 1,
     0, 0, 0, 0,
     0, 0, 0, 0],
    [0, 1, 0, 0,
     0, 1, 0, 0,
     0, 1, 0, 0,
     0, 1, 0, 0],
], Color.RED))

# 口
g_blocks.append(Block([
    [0, 0, 0, 0,
     0, 1, 1, 0,
     0, 1, 1, 0,
     0, 0, 0, 0],
    [0, 0, 0, 0,
     0, 1, 1, 0,
     0, 1, 1, 0,
     0, 0, 0, 0],
    [0, 0, 0, 0,
     0, 1, 1, 0,
     0, 1, 1, 0,
     0, 0, 0, 0],
    [0, 0, 0, 0,
     0, 1, 1, 0,
     0, 1, 1, 0,
     0, 0, 0, 0],
], Color.BLUE))

# L
g_blocks.append(Block([
    [0, 1, 0, 0,
     0, 1, 0, 0,
     0, 1, 1, 0,
     0, 0, 0, 0],
    [0, 0, 0, 0,
     0, 0, 1, 0,
     1, 1, 1, 0,
     0, 0, 0, 0],
    [0, 0, 0, 0,
     0, 1, 1, 0,
     0, 0, 1, 0,
     0, 0, 1, 0],
    [0, 0, 0, 0,
     0, 1, 1, 1,
     0, 1, 0, 0,
     0, 0, 0, 0],
], Color.MAGENTA))

# 反L
g_blocks.append(Block([
    [0, 0, 1, 0,
     0, 0, 1, 0,
     0, 1, 1, 0,
     0, 0, 0, 0],
    [0, 0, 0, 0,
     1, 1, 1, 0,
     0, 0, 1, 0,
     0, 0, 0, 0],
    [0, 0, 0, 0,
     0, 1, 1, 0,
     0, 1, 0, 0,
     0, 1, 0, 0],
    [0, 0, 0, 0,
     0, 1, 0, 0,
     0, 1, 1, 1,
     0, 0, 0, 0],
], Color.YELLOW))

# L
g_blocks.append(Block([
    [0, 0, 0, 0,
     1, 1, 0, 0,
     0, 1, 1, 0,
     0, 0, 0, 0],
    [0, 0, 0, 0,
     0, 0, 1, 0,
     0, 1, 1, 0,
     0, 1, 0, 0],
    [0, 0, 0, 0,
     1, 1, 0, 0,
     0, 1, 1, 0,
     0, 0, 0, 0],
    [0, 0, 0, 0,
     0, 0, 1, 0,
     0, 1, 1, 0,
     0, 1, 0, 0],
], Color.CYAN))

# 反Z
g_blocks.append(Block([
    [0, 0, 1, 1,
     0, 1, 1, 0,
     0, 0, 0, 0,
     0, 0, 0, 0],
    [0, 1, 0, 0,
     0, 1, 1, 0,
     0, 0, 1, 0,
     0, 0, 0, 0],
    [0, 0, 1, 1,
     0, 1, 1, 0,
     0, 0, 0, 0,
     0, 0, 0, 0],
    [0, 1, 0, 0,
     0, 1, 1, 0,
     0, 0, 1, 0,
     0, 0, 0, 0],
], Color.GREEN))

# T
g_blocks.append(Block([
    [0, 1, 0, 0,
     1, 1, 1, 0,
     0, 0, 0, 0,
     0, 0, 0, 0],
    [0, 1, 0, 0,
     1, 1, 0, 0,
     0, 1, 0, 0,
     0, 0, 0, 0],
    [0, 0, 0, 0,
     1, 1, 1, 0,
     0, 1, 0, 0,
     0, 0, 0, 0],
    [0, 1, 0, 0,
     0, 1, 1, 0,
     0, 1, 0, 0,
     0, 0, 0, 0],
], Color.BROWN))


# 定义当前方块、下一个方块的信息
@dataclass
class BlockInfo:
    id: int = 0  # 方块 ID
    x: int = 0  # 方块在游戏区中的坐标
    y: int = 0
    dir: int = 0  # 方向


g_cur_block = BlockInfo()
g_next_block = BlockInfo()

g_world = np.zeros((WIDTH, HEIGHT))

g_quit_game = False


def main():
    init()
    new_game()
    frame_count = 0
    while is_run() or g_quit_game:
        c = get_command(frame_count)
        dispatch_command(c)
        if c == CMD.QUIT:
            if dialog.get_yes_or_no("您要退出游戏吗？", "提醒"):
                break  # quit the game
        frame_count += 1
        delay_fps(60)
    close_graph()


def init():
    init_graph(640, 480)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_background_color(Color.BLACK)
    set_color(Color.WHITE)
    set_fill_color(Color.TRANSPARENT)
    set_caption("Tetris")

    # 显示操作说明
    set_font_size(14)
    draw_text(20, 330, "操作说明")
    draw_text(20, 350, "上：旋转")
    draw_text(20, 370, "左：左移")
    draw_text(20, 390, "右：右移")
    draw_text(20, 410, "下：下移")
    draw_text(20, 430, "空格：沉底")
    draw_text(20, 450, "ESC：退出")

    set_origin(220, 20)

    # 绘制游戏区边界
    rect(-1, -1, WIDTH * UNIT, HEIGHT * UNIT)
    rect((WIDTH + 1) * UNIT - 1, -1, (WIDTH + 5) * UNIT, 4 * UNIT)


def new_game():
    global g_quit_game
    # 清空游戏区
    set_fill_color(Color.BLACK)
    fill_rect(0, 0, WIDTH * UNIT - 1, HEIGHT * UNIT - 1)
    g_world.fill(0)
    g_quit_game = False
    # 生成下一个方块
    g_next_block.id = random.randrange(7)
    g_next_block.dir = random.randrange(4)
    g_next_block.x = WIDTH + 1
    g_next_block.y = HEIGHT - 1
    # 获取新方块
    new_block()


def game_over():
    global g_quit_game
    if dialog.get_yes_or_no("游戏结束。\n您想重新来一局吗？", "游戏结束"):
        new_game()
    else:
        g_quit_game = True


last_down_frame_count = 0


def get_command(frame_count):
    global last_down_frame_count
    if has_kb_msg():
        key = get_key()
        k = key.key
        if k == QtCore.Qt.Key_W or k == QtCore.Qt.Key_Up:
            return CMD.ROTATE
        elif k == QtCore.Qt.Key_S or k == QtCore.Qt.Key_Down:
            last_down_frame_count = frame_count
            return CMD.DOWN
        elif k == QtCore.Qt.Key_A or k == QtCore.Qt.Key_Left:
            return CMD.LEFT
        elif k == QtCore.Qt.Key_D or k == QtCore.Qt.Key_Right:
            return CMD.RIGHT
        elif k == QtCore.Qt.Key_Space:
            last_down_frame_count = frame_count
            return CMD.SINK
        elif k == QtCore.Qt.Key_Escape:
            return CMD.QUIT
    if frame_count - last_down_frame_count > DROP_SPEED:
        last_down_frame_count = frame_count
        return CMD.DOWN
    else:
        return None


def dispatch_command(cmd):
    if cmd is CMD.ROTATE:
        on_rotate()
    elif cmd is CMD.LEFT:
        on_left()
    elif cmd is CMD.RIGHT:
        on_right()
    elif cmd is CMD.DOWN:
        on_down()
    elif cmd is CMD.SINK:
        on_sink()


def is_blank_row(block, i: int) -> bool:
    return block[i * 4] == 0 \
           and block[i * 4 + 1] == 0 \
           and block[i * 4 + 2] == 0 \
           and block[i * 4 + 3] == 0


def new_block():
    g_cur_block.id = g_next_block.id
    g_cur_block.dir = g_next_block.dir
    g_cur_block.x = (WIDTH - 4) // 2
    g_cur_block.y = HEIGHT + 2
    g_next_block.id = random.randrange(7)
    g_next_block.dir = random.randrange(4)

    # 下移新方块直到有局部显示
    block = g_blocks[g_cur_block.id].dir[g_cur_block.dir]
    i = 3
    while is_blank_row(block, i):
        g_cur_block.y -= 1
        i -= 1

    draw_block(g_cur_block)

    # 绘制下一个方块
    set_fill_color(Color.BLACK)
    fill_rect((WIDTH + 1) * UNIT, 0, (WIDTH + 5) * UNIT - 1, 4 * UNIT - 1)
    draw_block(g_next_block)


# 画单元方块
def draw_unit(x: int, y: int, c: QtGui.QColor, _draw: DRAW):
    # 计算单元方块对应的屏幕坐标
    left = x * UNIT
    top = (HEIGHT - y - 1) * UNIT
    right = (x + 1) * UNIT - 1
    bottom = (HEIGHT - y) * UNIT - 1

    # 画单元方块
    if _draw is DRAW.SHOW:
        # 画普通方块
        set_color(0x006060)
        rounded_rect(left + 1, top + 1, right - 1, bottom - 1, 5, 5)
        set_color(0x003030)
        rounded_rect(left, top, right, bottom, 8, 8)
        set_fill_color(c)
        set_color(Color.LIGHT_GRAY)
        draw_rect(left + 2, top + 2, right - 2, bottom - 2)
    elif _draw is DRAW.FIX:
        # 画固定的方块
        c = QtGui.QColor(c)
        set_fill_color(rgb(c.red() * 2 // 3, c.green() * 2 // 3, c.blue() * 2 // 3))
        set_color(Color.DARK_GRAY)
        draw_rect(left + 1, top + 1, right - 1, bottom - 1)
    elif _draw is DRAW.CLEAR:
        # 擦除方块
        set_fill_color(Color.BLACK)
        fill_rect(x * UNIT, (HEIGHT - y - 1) * UNIT, (x + 1) * UNIT, (HEIGHT - y) * UNIT);


# 画方块
def draw_block(_block: BlockInfo, _draw: DRAW = DRAW.SHOW):
    block = g_blocks[_block.id].dir[_block.dir]
    for i in range(16):
        if block[i] == 1:
            x = _block.x + i % 4
            y = _block.y - i // 4
            if (y < HEIGHT):
                draw_unit(x, y, g_blocks[_block.id].color, _draw)


# 检测指定方块是否可以放下
def CheckBlock(_block: BlockInfo) -> bool:
    block = g_blocks[_block.id].dir[_block.dir]
    for i in range(16):
        if block[i] == 1:
            x = _block.x + i % 4
            y = _block.y - i // 4
            if (x < 0) or (x >= WIDTH) or (y < 0):
                return False
            if (y < HEIGHT) and g_world[x][y] == 1:
                return False
    return True


def check_rotate():
    tmp = copy.copy(g_cur_block)
    tmp.dir += 1
    if tmp.dir >= 4:
        tmp.dir = 0
    if CheckBlock(tmp):
        return 0
    tmp.x = g_cur_block.x - 1
    if CheckBlock(tmp):
        return -1
    tmp.x = g_cur_block.x + 1
    if CheckBlock(tmp):
        return 1
    tmp.x = g_cur_block.x - 2
    if CheckBlock(tmp):
        return -2
    tmp.x = g_cur_block.x + 2
    if CheckBlock(tmp):
        return 2
    return None


# 旋转方块
def on_rotate():
    dx = check_rotate()
    if dx is None:
        return
    # 旋转
    draw_block(g_cur_block, DRAW.CLEAR)
    g_cur_block.dir += 1
    if g_cur_block.dir >= 4:
        g_cur_block.dir = 0
    g_cur_block.x += dx
    draw_block(g_cur_block)


# 左移方块
def on_left():
    tmp = copy.copy(g_cur_block)
    tmp.x -= 1
    if CheckBlock(tmp):
        draw_block(g_cur_block, DRAW.CLEAR)
        g_cur_block.x -= 1
        draw_block(g_cur_block)


# 右移方块
def on_right():
    tmp = copy.copy(g_cur_block)
    tmp.x += 1
    if CheckBlock(tmp):
        draw_block(g_cur_block, DRAW.CLEAR)
        g_cur_block.x += 1
        draw_block(g_cur_block)


# 下移方块
def on_down():
    tmp = copy.copy(g_cur_block)
    tmp.y -= 1
    if CheckBlock(tmp):
        draw_block(g_cur_block, DRAW.CLEAR)
        g_cur_block.y -= 1
        draw_block(g_cur_block)
    else:
        on_sink()  # 不可下移时，执行“沉底方块”操作


# 沉底方块
def on_sink():
    # 连续下移方块
    draw_block(g_cur_block, DRAW.CLEAR)
    tmp = copy.copy(g_cur_block)
    tmp.y -= 1
    while CheckBlock(tmp):
        tmp.y -= 1
        g_cur_block.y -= 1
    draw_block(g_cur_block, DRAW.FIX)

    # 固定方块在游戏区
    block = g_blocks[g_cur_block.id].dir[g_cur_block.dir]
    for i in range(16):
        if block[i] == 1:
            if g_cur_block.y - i // 4 >= HEIGHT:
                # 如果方块的固定位置超出高度，结束游戏
                game_over();
                return;
            else:
                g_world[g_cur_block.x + i % 4][g_cur_block.y - i // 4] = 1

    # 检查是否需要消掉行，并标记
    remove = [0] * 4  # 标记方块涉及的 4 行是否有消除行为
    y = g_cur_block.y
    while y >= max(g_cur_block.y - 3, 0):
        can_clear = True
        for x in range(WIDTH):
            if g_world[x][y] == 0:
                can_clear = False
                break
        if can_clear:
            remove[g_cur_block.y - y] = 1
            set_fill_color(Color.LIGHT_GREEN)
            set_color(Color.LIGHT_GREEN)
            fill_rect(0, (HEIGHT - y - 1) * UNIT + UNIT / 2 - 5, WIDTH * UNIT - 1,
                      (HEIGHT - y - 1) * UNIT + UNIT / 2 + 5);
        # setfillstyle(BS_SOLID);
        y -= 1

    if sum(remove) > 0:  # 如果产生整行消除
        # 擦掉刚才标记的行
        for i in range(4):
            if remove[i] == 1:
                # 延时 100 毫秒
                time.sleep(0.1)
                for y in range(g_cur_block.y - i + 1, HEIGHT):
                    for x in range(WIDTH):
                        g_world[x][y - 1] = g_world[x][y]
                        g_world[x][y] = 0
                img = create_image(WIDTH * UNIT, (HEIGHT - (g_cur_block.y - i + 1)) * UNIT)
                get_image(220, 20, WIDTH * UNIT, (HEIGHT - (g_cur_block.y - i + 1)) * UNIT, img)
                draw_image(0, UNIT, img)

    # 产生新方块
    new_block()


easy_run(main)
