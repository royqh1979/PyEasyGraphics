"""
A Print game
"""
from easygraphics import *
import random


def show_welcome():
    clear_device()
    set_color("yellow")
    set_font_size(64)
    draw_text(160, 110, "Print Game");
    set_color("white");
    c = 0
    set_font_size(20)
    while not has_kb_hit():
        set_color(color_rgb(c, c, c))
        draw_text(180, 400, "Press any key to continue")
        c = (c + 8) % 255;
        delay_fps(30)
    ch = get_char()
    print(ch)
    clear_device()


def show_goodbye():
    clear_device();
    set_color("yellow");
    set_font_size(48);
    draw_text(104, 180, "Bye!!!");
    pause()


if __name__ == "__main__":
    init_graph(640, 480)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_background_color("black")

    show_welcome()
    random.seed()
    set_font_size(20)
    set_fill_color("black")

    while is_run():
        target = chr(65 + random.randint(0, 25))
        x = random.randint(0, 620)
        for y in range(16, 460):
            set_color("white")
            draw_text(x, y, target)
            if has_kb_hit():
                key = get_char()
                if key.upper() == target:
                    fill_rect(x - 2, y - 22, x + 22, y + 2)  # clear the char and generate next char
                    break
                if key == " ":
                    show_goodbye()
                    close_graph()
                    exit()
            delay_fps(60)
            fill_rect(x - 2, y - 22, x + 22, y + 2)  # clear the char

    close_graph()
