# https://codebus.cn/bestans/post/clock-simulation

from easygraphics import *
import math
import datetime

sec_len = 120
min_len = 100
hour_len = 70

def draw_hands(hour:int, min:int, sec:int):
    a_sec = sec * 2 * math.pi / 60
    a_min = min * 2 * math.pi / 60
    a_hour = hour  * 2 * math.pi / 12 + a_min / 12

    x_sec = sec_len * math.sin(a_sec)
    y_sec = sec_len * math.cos(a_sec)
    x_min = min_len * math.sin(a_min)
    y_min = min_len * math.cos(a_min)
    x_hour = hour_len * math.sin(a_hour)
    y_hour = hour_len * math.cos(a_hour)

    set_line_width(10)
    set_color(Color.WHITE)
    line(320+x_hour,240-y_hour,320-x_hour/7,240+y_hour/7)

    set_line_width(6)
    set_color(Color.LIGHT_GRAY)
    line(320+x_min,240-y_min,320-x_min/5,240+y_min/5)

    set_line_width(2)
    set_color(Color.RED)
    line(320+x_sec,240-y_sec,320-x_sec/3,240+y_sec/3)


def prepare_dial(image:Image):
    old_image = get_target()
    set_target(image)
    set_background_color(Color.BLACK)
    clear_device()
    set_color(Color.WHITE)
    circle(320,240,2)
    circle(320,240,60)
    circle(320,240,160)

    for i in range(60):
        x = 320 + 145 * math.sin(i*2*math.pi/60)
        y = 240 + 145 * math.cos(i*2*math.pi/60)
        if i % 15 == 0:
            fill_rect(x-5,y-5,x+5,y+5)
        elif i%5==0:
            circle(x,y,3)
        else:
            put_pixel(x,y,Color.WHITE)

    set_target(old_image)

def main():
    init_graph(640,480)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_caption("Clock")
    dial_image = create_image(640,480)
    prepare_dial(dial_image)
    while is_run():
        t=datetime.datetime.now()
        draw_image(0,0,dial_image)
        draw_hands(t.hour,t.minute,t.second)
        delay_fps(1)

    close_graph()

easy_run(main)