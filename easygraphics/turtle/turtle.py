from . import turleclass
import easygraphics as eg

TurtleWorld = turleclass.TurtleWorld
Turtle = turleclass.Turtle

__all__ = [
    'create_world', 'close_world', 'forward', 'fd', 'backward', 'back', 'bk',
    'left_turn', 'lt', 'right_turn', 'rt', 'clear_screen', 'cs', 'gotoxy', 'home',
    'turn_to', 'facing', 'begin_fill', 'end_fill', 'setxy', 'set_heading',
    'get_y', 'get_x', 'get_heading', 'get_turtle', 'get_turtle_world',
    'set_immediate', 'set_speed', 'pen_down', 'pen_up', 'pu', 'pd', 'hide', 'show',
    'Turtle', 'TurtleWorld']

_turtle: Turtle = None
_world: TurtleWorld = None


def create_world(width: int = 800, height: int = 600) -> None:
    """
    Create an world for turtle drawing.

    :param width: width of the graphics window
    :param height: height of the graphics window
    """
    global _turtle, _world
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


def right_turn(degree: float):
    """
    Turn turtle right (clockwise) by \"degree\" degree.

    :param degree: the degree to turn
    """
    _check_turtle()
    _turtle.right_turn(degree)


rt = right_turn


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
    Set the turtle's moving speed.

    :param speed: the new speed
    """
    _check_turtle()
    _turtle.set_speed(speed)


def set_immediate(immediate: bool):
    """
    Set if there are animations when the turtle moving.

    :param immediate: True to turn off animation (the move finishes immediately). Off to turn on.
    """
    _check_turtle()
    _world.set_immediate(immediate)
