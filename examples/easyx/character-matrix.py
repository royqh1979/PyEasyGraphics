# A demo program
# origin: https://codebus.cn/yangw/post/character-matrix
import random
from easygraphics import *

def main():
    init_graph(640,480)
    set_render_mode(RenderMode.RENDER_MANUAL)
    set_font_size(16)
    while is_run():
        if has_kb_hit():
            break
        for i in range(479):
            set_color(Color.GREEN)
            for j in range(3):
                x=random.randrange(80)*8
                y=random.randrange(20)*24
                c=random.randrange(26)+65
                draw_text(x,y,chr(c))
            set_color(Color.BLACK)
            line(0,i,639,i)
            delay(1)
    close_graph()

easy_run(main)