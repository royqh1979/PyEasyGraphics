if __name__ == "__main__":
    from easygraphics import *

    init_graph(600, 160)
    set_color(Color.BLACK)
    set_fill_color(Color.RED)

    circle(100, 75, 60)
    draw_rect_text(0, 140, 200, 20, "circle()", flags=TextFlags.ALIGN_CENTER)

    draw_circle(300, 75, 60)
    draw_rect_text(200, 140, 200, 20, "draw_circle()", flags=TextFlags.ALIGN_CENTER)

    fill_circle(500, 75, 60)
    draw_rect_text(400, 140, 200, 20, "fill_circle()", flags=TextFlags.ALIGN_CENTER)

    pause()
    # save_image("circles.png")
    close_graph()
