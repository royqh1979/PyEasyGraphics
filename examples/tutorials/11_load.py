"""
Load and display a image
"""
if __name__ == "__main__":
    from easygraphics import *

    init_graph(800, 600)
    img = load_image("test.png")
    draw_image((get_width() - img.get_width()) // 2,
               (get_height() - img.get_height()) // 2, img)
    pause()
    img.close()
    close_graph()
