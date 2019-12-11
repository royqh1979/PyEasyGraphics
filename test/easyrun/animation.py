from easygraphics import *


def mainloop():
    x = 0
    set_color(Color.BLUE)
    set_fill_color(Color.GREEN)

    while is_run():
        x = (x + 1) % 440
        if delay_jfps(60):
            clear_device()
            draw_ellipse(x + 100, 200, 100, 100)

def main() :
    init_graph(640, 480)
    set_render_mode(RenderMode.RENDER_MANUAL)
    mainloop()
    close_graph()

easy_run(main_func=main)
