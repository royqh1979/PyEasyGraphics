from easygraphics import *

DELAY_TIME = 200  # delay in drawing

init_graph(800, 600)
set_origin(400, 300)
# fill the background
set_background_color(Color.WHITE)
clear_device()

# head 头
set_fill_color(color_rgb(7, 190, 234))
set_color(Color.BLACK)
draw_rounded_rect(-135, -206, 135, 54, 248, 248)
delay(DELAY_TIME)


## face 脸
set_fill_color(Color.WHITE)
draw_ellipse(0, -46, 115, 95)
delay(DELAY_TIME)

# right eye 右眼
draw_rounded_rect(-63, -169, 0, -95, 56, 56)
delay(DELAY_TIME)
# left eye 左眼
draw_rounded_rect(0, -169, 63, -95, 56, 56)
delay(DELAY_TIME)

# right eyeball 右眼球
set_fill_color(Color.BLACK)
draw_circle(-16, -116, 6)
delay(DELAY_TIME)

# left eyeball 左眼球
draw_circle(16, -116, 6)
delay(DELAY_TIME)

# nose 鼻子
set_fill_color(color_rgb(201, 62, 0))
draw_circle(0, -92, 15)
delay(DELAY_TIME)

# philtrum 人中
line(0, -77, 0, -4)
delay(DELAY_TIME)
# mouse 嘴
arc(0, -112, 180 * 5 / 4, 180 * 7 / 4, 108, 108)
delay(DELAY_TIME)
# whistkers 胡须
line(-42, -73, -90, -91)
line(42, -73, 90, -91)
line(-41, -65, -92, -65)
line(41, -65, 92, -65)
line(-42, -57, -90, -39)
line(42, -57, 90, -39)
delay(DELAY_TIME)

# body 身体

# arms 手臂
line(-76, 32, -138, 72)
line(76, 32, 138, 72)
line(-96, 96, -116, 110)
line(96, 96, 116, 110)
delay(DELAY_TIME)

# legs 腿
line(-96, 85, -96, 178)  # 腿外侧
line(96, 85, 96, 178)
arc(0, 179, 0, 180, 15, 11)  # 腿内侧
delay(DELAY_TIME)

# hands 手
set_fill_color(Color.WHITE)
draw_circle(-140, 99, 27)
draw_circle(140, 99, 27)
delay(DELAY_TIME)

# foots 脚
draw_rounded_rect(-112, 178, -2, 205, 24, 24)
draw_rounded_rect(2, 178, 112, 205, 24, 24)
delay(DELAY_TIME)

# fill body with blue 身体填充蓝色
set_fill_color(color_rgb(7, 190, 234))
flood_fill(0, 100, Color.BLACK)
delay(DELAY_TIME)

# tummy 肚皮
set_fill_color(Color.WHITE)
draw_circle(0, 81, 75)
fill_rect(-60, 4, 60, 24)  # 用白色矩形擦掉多余的肚皮
delay(DELAY_TIME)

# pocket 口袋
draw_pie(0, 81, 180, 360, 58, 58)
delay(DELAY_TIME)

# bell 铃铛

#  rope 绳子
set_fill_color(color_rgb(169, 38, 0))
draw_rounded_rect(-100, 23, 100, 42, 12, 12)
delay(DELAY_TIME)

# outline of the bell 铃铛外形
set_fill_color(color_rgb(245, 237, 38))
draw_circle(0, 49, 19)
delay(DELAY_TIME)

# hole in the bell 铃铛上的洞
set_fill_color(Color.BLACK)
draw_ellipse(0, 53, 4, 4)
delay(DELAY_TIME)

# texture on the bell 铃铛上的纹路
set_line_width(3)
line(0, 57, 0, 68)
set_line_width(1)
line(-16, 40, 16, 40)
line(-18, 44, 18, 44)

set_background_color(Color.LIGHT_RED)
pause()
close_graph()
