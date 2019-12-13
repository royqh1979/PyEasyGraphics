from easygraphics import *

def main():
    init_graph(200,200)
    set_color(Color.BLACK)
    set_fill_color(Color.LIGHT_GRAY)
    points = [(40,40),
              (80,60),
              (100,100),
              (60,120),
              (50,150)]

    # draw the curve
    begin_shape()
    curve_vertex(40,40) # the first control point is also the start point of the curve
    for point in points:
        curve_vertex(point[0],point[1])
    curve_vertex(50,150) # the last control point is also the end point of the curve
    end_shape()

    # draw control points
    set_fill_color(Color.RED)
    for point in points:
        fill_circle(point[0],point[1],3)

    pause()
    close_graph()

easy_run(main)