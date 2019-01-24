from easygraphics import *

x = 0
y = 0


def draw_compositon(x, y, mode, alpha_value):
    set_background_color(Color.TRANSPARENT)
    set_font_size(18)
    set_line_width(3)
    set_color("black")
    set_composition_mode(CompositionMode.SOURCE)
    draw_rect_text(x, y + 175, 200, 25, mode)
    set_fill_color(to_alpha("orange", alpha_value))
    draw_circle(x + 120, y + 80, 70)

    set_composition_mode(eval("CompositionMode." + mode))
    set_fill_color(to_alpha("darkblue", alpha_value))
    draw_rect(x + 20, y + 80, x + 120, y + 170)


def draw_background(size, width, height):
    mx = width // size
    my = height // size
    for i in range(0, mx + 1):
        for t in range(0, my + 1):
            if (i + t) % 2 == 1:
                set_color("lightgray")
                set_fill_color("lightgray")
            else:
                set_color("white")
                set_fill_color("white")
            draw_rect(i * size, t * size, (i + 1) * size, (t + 1) * size)


def draw_compositon_and_save(mode, alpha_value):
    global x, y
    img1 = create_image(200, 200)
    set_target(img1)
    draw_compositon(0, 0, mode, alpha_value)
    img2 = create_image(200, 200)
    set_target(img2)
    draw_background(20, 200, 200)
    set_target()
    draw_image(0, 0, img1, composition_mode=CompositionMode.SOURCE_OVER, dst_image=img2)
    # img2.save("%s_%d.png" % (mode.lower(), alpha_value))
    draw_image(x, y, img2)
    x += 200
    if x >= 1200:
        y += 200
        x = 0


def draw_compositions(alpha_value):
    draw_compositon_and_save("SOURCE_OVER", alpha_value)
    draw_compositon_and_save("SOURCE_IN", alpha_value)
    draw_compositon_and_save("SOURCE_OUT", alpha_value)
    draw_compositon_and_save("SOURCE_AT_TOP", alpha_value)
    draw_compositon_and_save("SOURCE", alpha_value)
    draw_compositon_and_save("XOR", alpha_value)


def draw_compositions2(alpha_value):
    draw_compositon_and_save("DESTINATION_OVER", alpha_value)
    draw_compositon_and_save("DESTINATION_IN", alpha_value)
    draw_compositon_and_save("DESTINATION_OUT", alpha_value)
    draw_compositon_and_save("DESTINATION_AT_TOP", alpha_value)
    draw_compositon_and_save("DESTINATION", alpha_value)
    draw_compositon_and_save("XOR", alpha_value)


if __name__ == "__main__":
    init_graph(1200, 800)
    draw_compositions(255)
    draw_compositions(150)

    draw_compositions2(255)
    draw_compositions2(150)
    pause()
    close_graph()
