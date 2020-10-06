from easygraphics.processing import *
from easygraphics import *

gamescreen = 0

def setup():
    # 创建一个700ｘ500像素的画布
    set_size(700,500)

def draw() :
    if gamescreen == 0 :
        init_screen()
    # elif gamescreen == 1:
    #     gameplay_screen()
    # elif gamescreen == 2:
    #     gameover_screen()

def init_screen():
    set_background_color(rgb(236,240,241))
    clear()
    set_color(rgb(52,73,94))
    set_font_size(90)
    draw_text(get_width()/2-100,get_height()/2,"乒 乓")
    set_fill_color(rgb(92,167,182))
    set_rect_mode(ShapeMode.CENTER)
    fill_rounded_rect(get_width()/2,get_height()-35,100,30,5)
    set_color(rgb(236,240,241))
    set_font_size(15)
    draw_text(get_width()/2 - 20, get_height()-30,"开始")

run_app(globals())