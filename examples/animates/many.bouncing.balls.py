"""
Many Bouncing balls

Adapted form "Processing Creative Coding and Computational Art", Page 90.
"""
from easygraphics import *
import random

def main():
    ball_count = 500
    ball_size = 8
    ball_speed = 3

    x_speed = [0] * ball_count
    y_speed = [0] * ball_count

    x_pos = [0] * ball_count
    y_pos = [0] * ball_count

    ball_radius = [0] * ball_count

    random.seed()
    init_graph(800, 600)
    set_render_mode(RenderMode.RENDER_MANUAL)

    set_background_color("black")
    set_fill_color("white")

    for i in range(ball_count):
        x_speed[i] = random.randint(-ball_speed, ball_speed)
        y_speed[i] = random.randint(1, ball_speed)

        x_pos[i] = get_width() // 2 + random.randint(-get_width() // 3, get_width() // 3)
        y_pos[i] = get_height() // 2 + random.randint(-get_height() // 3, get_height() // 3)

        ball_radius[i] = random.randint(1, round(ball_size / 2))

    while is_run():
        for i in range(ball_count):
            x_pos[i] += x_speed[i]
            y_pos[i] += y_speed[i]
            if x_pos[i] < ball_radius[i] or x_pos[i] > get_width() - ball_radius[i]:
                x_speed[i] = -x_speed[i]
            if y_pos[i] < ball_radius[i] or y_pos[i] > get_height() - ball_radius[i]:
                y_speed[i] = -y_speed[i]
        if delay_jfps(30):
            # clear()
            for i in range(ball_count):
                set_fill_color(color_gray(i * 255 / ball_count))
                fill_ellipse(x_pos[i], y_pos[i], ball_radius[i], ball_radius[i])

    close_graph()

easy_run(main)