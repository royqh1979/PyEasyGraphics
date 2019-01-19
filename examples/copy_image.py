if __name__ == "__main__":
    from easygraphics import *
    init_graph(800, 600)
    set_render_mode(RenderMode.RENDER_MANUAL)
    background = create_image(800, 600)
    set_target(background)
    set_background_color(Color.LIGHT_YELLOW)
    set_fill_color(Color.RED)
    draw_circle(150, 150, 50)
    set_fill_color(Color.DARK_BLUE)
    draw_rect(0, 400, 800, 600)

    moving_object = create_image(200, 150)
    set_target(moving_object)
    set_background_color(Color.TRANSPARENT)
    set_fill_color(Color.GREEN)
    draw_ellipse(100, 75, 90, 70)


    set_target()
    x = 0
    while is_run():
        x = (x + 3) % 750
        draw_image(0, 0, background)
        draw_image(x, 380, moving_object)
        delay_fps(60)

    background.close()
    moving_object.close()
    close_graph()
