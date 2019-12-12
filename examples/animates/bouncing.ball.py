"""
Bouncing ball

Adapted form "Processing Creative Coding and Computational Art", Page 77.
"""
from easygraphics import *

def main():
    init_graph(400, 400)
    set_render_mode(RenderMode.RENDER_MANUAL)

    set_background_color("black")
    set_fill_color("white")
    x_speed = 3
    y_speed = 6
    ball_radius = 10

    x_pos = get_width() // 2
    y_pos = get_height() // 2

    while is_run():
        clear()
        x_pos += x_speed
        y_pos += y_speed
        if x_pos < ball_radius or x_pos > get_width() - ball_radius:
            x_speed = -x_speed
        if y_pos < ball_radius or y_pos > get_height() - ball_radius:
            y_speed = -y_speed

        fill_ellipse(x_pos, y_pos, ball_radius, ball_radius)
        delay_fps(30)

    close_graph()

easy_run(main)