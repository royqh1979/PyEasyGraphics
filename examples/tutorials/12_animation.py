"""
Draws an animation
"""
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

    car = create_image(162, 150)
    set_target(car)
    set_composition_mode(CompositionMode.SOURCE)
    set_background_color(Color.TRANSPARENT)
    set_fill_color("white")
    draw_polygon(0, 0, 0, 60, 160, 60, 160, 40, 125, 20, 110, 0)
    set_fill_color("darkgray")
    draw_circle(35, 60, 20)
    draw_circle(120, 60, 20)
    set_fill_color("transparent")
    draw_rect(10, 10, 40, 25)
    draw_rect(50, 10, 80, 25)

    set_target()
    x = 0
    while is_run():
        x = (x + 2) % 750
        draw_image(0, 0, background)
        draw_image(x, 350, car)
        delay_fps(100)

    background.close()
    car.close()
    close_graph()
