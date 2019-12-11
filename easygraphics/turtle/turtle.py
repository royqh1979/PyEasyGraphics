import sys

from . import turleclass
import easygraphics as eg

TurtleWorld = turleclass.TurtleWorld
Turtle = turleclass.Turtle

__all__ = [
    'create_world', 'close_world', 'forward', 'fd', 'backward', 'back', 'bk',
    'left_turn', 'lt', 'right_turn', 'rt', 'left', 'right', 'clear_screen', 'cs', 'gotoxy', 'home',
    'turn_to', 'facing', 'begin_fill', 'end_fill', 'setxy', 'set_heading', 'move_arc', 'move_ellipse',
    'get_y', 'get_x', 'get_heading', 'get_turtle', 'get_turtle_world', 'set_pen_size',
    'set_immediate', 'set_speed', 'pen_down', 'pen_up', 'pu', 'pd', 'hide', 'show', 'pause',
    'is_run', 'is_out_of_window',
    'Turtle', 'TurtleWorld', 'turtle_run']

_turtle = None
_world = None

_in_shell = bool(getattr(sys, 'ps1', sys.flags.interactive))  # if in interactive mode (eg. in IPython shell)

def turtle_run(main_func,width: int = 800, height: int = 600) -> None:
    def _main_func():
        global _turtle, _world
        _world = TurtleWorld()
        _turtle = Turtle(_world)
        main_func()
    eg.easy_run(_main_func,width,height)


def create_world(width: int = 800, height: int = 600) -> None:
    """
    Create an world for turtle drawing.

    :param width: width of the graphics window
    :param height: height of the graphics window
    """
    global _turtle, _world
    if eg.in_easy_run_mode():
        if not _world:
            raise RuntimeError("Must use turtle_run to run turtle code!")
        eg.init_graph(width,height)
        return
    if _world is not None:
        raise ValueError("The world has been created! ")
    if not eg.is_run():
        eg.init_graph(width, height)
    _world = TurtleWorld()
    _turtle = Turtle(_world)


def close_world() -> None:
    """
    Close the turtle world and the graphics window.

    """
    global _world, _turtle
    if _world is not None:
        _world.close()
        _world = None
        _turtle.close()
        _turtle = None
        eg.close_graph()


def get_turtle_world() -> TurtleWorld:
    """
    Get the current turtle world.

    :return: the current turtle world
    """
    return _world


def get_turtle() -> Turtle:
    """
    Get the current turtle.

    :return: the current turtle
    """
    return _turtle


def _check_turtle():
    if _turtle is None:
        create_world()
    elif _in_shell:
        if not eg.is_run():
            raise RuntimeError("Must run close_world() to clean up the world!")


def forward(distance: float):
    """
    Move the turtle forward by the specified distance, in the direction the turtle is heading.

    :param distance: the distance to move
    """
    _check_turtle()
    _turtle.forward(distance)


fd = forward


def backward(distance: float):
    """
    Move the turtle backward by the specified distance, in the direction the turtle is heading.

    :param distance: the distance to move
    """
    _check_turtle()
    _turtle.backward(distance)


bk = backward

back = backward


def left_turn(degree: float):
    """
    Turn turtle left (counter-clockwise) by \"degree\" degree.

    :param degree: the degree to turn
    """
    _check_turtle()
    _turtle.left_turn(degree)


lt = left_turn

left = left_turn


def right_turn(degree: float):
    """
    Turn turtle right (clockwise) by \"degree\" degree.

    :param degree: the degree to turn
    """
    _check_turtle()
    _turtle.right_turn(degree)


rt = right_turn

right = right_turn


def move_arc(radius: float, angle: float = 360):
    """
    The center is radius units left of the turtle. That is, if radius > 0,
    the center is on the left of the turtle; if radius < 0, the center is on the right of the turtle.

    If angle > 0, the turtle moves forward around the center; if angle < 0,
    the turtle moves backward around the center. So:

    * if angle > 0 and radius > 0, the turtle moves forward and turns counter-clockwise;
    * if angle > 0 and raidus < 0, the turtle move forward and turns clockwise;
    * if angle <0 and radius > 0, the turtle moves backward and turns clockwise;
    * if angle <0 and radius < 0, the turtle moves backward and turns counter-clockwise.

    :param radius: radius of the arc
    :param angle: how many degrees the turtle will move
    """
    _check_turtle()
    _turtle.move_arc(radius, angle)


def move_ellipse(radius_left: float, radius_top: float, angle: float = 360):
    """
    Move the turtle in an elliptical path.

    "radius_left" is the radius of the ellipse on the direction perpendicular to the turtle's
    orientation, it can be postive or negtive;"radius_top" is the radius of the ellipse
    on the direction parallel to the turtle's orientation, it must be postive.

    The center is radius_left units left of the turtle. That is, if radius_left > 0,
    the center is on the left of the turtle; if radius_left < 0, the center is on the right of the turtle.

    If angle > 0, the turtle moves forward around the center; if angle < 0,
    the turtle moves backward around the center. So:

    * if angle > 0 and radius_left > 0, the turtle moves forward and turns counter-clockwise;
    * if angle > 0 and radius_left < 0, the turtle move forward and turns clockwise;
    * if angle <0 and radius_left > 0, the turtle moves backward and turns clockwise;
    * if angle <0 and radius_left < 0, the turtle moves backward and turns counter-clockwise.

    :param radius_left: the radius of the ellipse on the direction perpendicular to the turtle's orientation
    :param radius_top: the radius of the ellipse on the direction parallel to the turtle's orientation
    :param angle: how many degrees the turtle will move
    """
    _check_turtle()
    _turtle.move_ellipse(radius_left, radius_top, angle)


def clear_screen():
    """
    Delete all drawings from the screen. Do not move turtle.
    """
    _check_turtle()
    _world.clear_screen()


cs = clear_screen


def begin_fill():
    """
    Begin to record the turtle's shape drawing path for filling.
    """
    _check_turtle()
    _turtle.begin_fill()


def end_fill():
    """
    Fill the shape enclosed by the turtle's drawing path after the last call to begin_fill.
    """
    _check_turtle()
    if eg.is_run():
        _turtle.end_fill()


def facing(x: float, y: float):
    """
    Turn the turtle to face the point(x,y).

    :param x: x coordinate value of the target point
    :param y: y coordinate value of the target point
    """
    _check_turtle()
    _turtle.facing(x, y)


def gotoxy(x: float, y: float):
    """
    Move the turtle to point (x,y). Will leave traces if the pen is down.

    :param x: x coordinate value of the destination point.
    :param y: x coordinate value of the destination point.
    """
    _check_turtle()
    _turtle.gotoxy(x, y)


def setxy(x: float, y: float):
    """
    Set the turtle's current position to point (x,y). Will not leave traces.

    :param x: x coordinate value of the destination point.
    :param y: y coordinate value of the destination point.
    """
    _check_turtle()
    _turtle.setxy(x, y)


def home():
    """
    Move the turtle back to the origin(0,0), and heading up. Will leave traces if the pen is down.
    """
    _check_turtle()
    _turtle.home()


def turn_to(angle):
    """
    Turn the angle to orient to the specified angle.

    :param angle: the new heading angle (in degrees).
    """
    _check_turtle()
    _turtle.turn_to(angle)


def set_heading(angle):
    """
    Set the angle current heading to the specified angle.

    :param angle: the new heading angle (in degrees).
    """
    _check_turtle()
    _turtle.set_heading(angle)


def get_heading() -> float:
    """
    Get the turtle's heading angle.

    :return: the turtle's heading angle.
    """
    _check_turtle()
    return _turtle.get_heading()


def get_x() -> float:
    """
    Get the turtle's current x position.

    :return: the turtle's x position.
    """
    _check_turtle()
    return _turtle.get_x()


def get_y() -> float:
    """
    Get the turtle's current y position.

    :return: the turtle's y position.
    """
    _check_turtle()
    return _turtle.get_y()


def hide():
    """
    Hide the turtle.
    """
    _check_turtle()
    _turtle.hide()


def show():
    """
    Show the turtle.
    """
    _check_turtle()
    _turtle.show()


def pen_down():
    """
    Pull the pen down – drawing when the turtle moving.
    """
    _check_turtle()
    _turtle.pen_down()


pd = pen_down


def pen_up():
    """
    Pull the pen up – no drawing when the turtle moving.
    """
    _check_turtle()
    _turtle.pen_up()


pu = pen_up


def set_speed(speed):
    """
    Set moving speed of the turtle.

    :param speed: the new speed
    """
    _check_turtle()
    _turtle.set_speed(speed)


def is_out_of_window() -> bool:
    """
    Test if the turtle is out of the graphics window.

    :return: True if the turtle is out of the window, False otherwise.
    """
    _check_turtle()
    return _turtle.is_out_of_window()


def set_immediate(immediate: bool):
    """
    Set if there are animations when the turtle moving.

    :param immediate: True to turn off animation (the move finishes immediately). False to turn on.
    """
    _check_turtle()
    _world.set_immediate(immediate)


set_pen_size = eg.set_line_width

pause = eg.pause

is_run = eg.is_run
