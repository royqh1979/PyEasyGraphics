from easygraphics import *

init_graph(200,200)

#draw bezier curves
set_color("black")
set_fill_color("yellow")
begin_shape()
vertex(30, 70) # first point
bezier_vertex(25, 25, 100, 50, 50, 100)
bezier_vertex(20, 130, 75, 140, 120, 120)
end_shape()

# draw control lines
set_color("lightgray")
line(30,70,25,25)
line(100,50,50,100)

line(50,100,20,130)
line(75,40,120,120)

# draw control points
set_fill_color("red")
fill_circle(30,70,3)
fill_circle(25,25,3)
fill_circle(100,50,3)

set_fill_color("blue")
fill_circle(50,100,3)
fill_circle(20,130,3)
fill_circle(75,40,3)
fill_circle(120,120,3)

pause()
close_graph()
