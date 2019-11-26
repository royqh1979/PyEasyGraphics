import math
import os
import threading
from typing import Optional
import time

from PyQt5 import QtGui, QtCore

import easygraphics as eg
from easygraphics.image import Image


class TurtleWorld(object):
    """
    Turtles move and draw in a world. This is the class representing the world.

    You must remember to close it by calling the close() method, if you have finished
    the drawing and won't use it anymore.


     Note that in the default world, we are using a normal coordinate system that (0,0) is in the center of
     the graphics window (image), the X-axis grows from left to right, and the Y-axis grows from bottom to top.
     A positive degree means turn counter-clockwise, and a negtive degree means turn clockwise.
    """

    def __init__(self, canvas: Optional[Image] = None):
        """
        Init the turtle world.

        :param canvas: the underlying image of the world. None means it's the graphics window.
        """
        if canvas is None:
            self._win = eg.get_graphics_window()
            self._world_image = eg.create_image(eg.get_width(), eg.get_height())
        else:
            self._world_image = canvas
            self._win = None
        self._width = self._world_image.get_width()
        self._height = self._world_image.get_height()
        self._world_image.reset_transform()
        self._world_image.translate(self._width // 2, self._height // 2)
        self._world_image.set_flip_y(True)
        self._buffer_image = eg.create_image(self._width, self._height)
        self._buffer_image.translate(self._width // 2, self._height // 2)
        self._buffer_image.set_flip_y(True)
        self._turtles = []
        self._running = True
        if self._win is not None:
            self._immediate = False
            self._win.set_immediate(False)
            self._start_refresh_loop()
            eg.set_target(self._world_image)
        else:
            self._immediate = True

    def close(self):
        """
        Close the turtles world.
        """
        self._running = False
        for turtle in self._turtles:
            turtle.close()
        self._turtles.clear()
        self._buffer_image.close()
        self._world_image.close()

    def create_snap_shot(self) -> Image:
        """
        Create a snap shot of the current drawing.

        :return: the snap shot image.
        """
        image = eg.create_image(self._width, self._height)
        self.snap_shot_to_image(image)
        return image

    def _render(self):
        self.snap_shot_to_image(self._win.get_canvas())

    def snap_shot_to_image(self, image, x=0, y=0):
        """
        Create a snap shot to the specified image.

        The snap shot will be copied to the image's (x,y).

        :param image: the image to copy the snap shot
        :param x: x coordinate value of the target position
        :param y: y coordinate value of the target position
        """
        buffer = self._buffer_image
        buffer.save_settings()
        buffer.reset_transform()
        buffer.draw_image(0, 0, self._world_image, composition_mode=eg.CompositionMode.SOURCE)
        buffer.set_transform(self._world_image.get_transform())
        for turtle in self._turtles:
            if turtle.is_show():
                buffer.push_transform()
                buffer.translate(turtle.get_x(), turtle.get_y())
                buffer.rotate(turtle.get_heading() + 90)
                buffer.draw_image(-turtle.get_icon().get_width() // 2,
                                  -turtle.get_icon().get_height() // 2, turtle.get_icon(),
                                  composition_mode=eg.CompositionMode.SOURCE_OVER)
                buffer.pop_transform()
        buffer.restore_settings()
        image.draw_image(x, y, buffer, composition_mode=eg.CompositionMode.SOURCE)

    def add_turtle(self, turtle: "Turtle"):
        """
        Put the turtle into the world.

        :param turtle: the turtle
        """
        self._turtles.append(turtle)

    def create_turtle(self):
        """
        Create a new turtle in the world and put it to the origin(0,0).

        If x and y are None, the turtle is put on the center.

        :return: the created turtle.
        """
        turtle = Turtle(self)
        return turtle

    def is_on_screen(self) -> bool:
        """
        Test if the underlying image is the graphics window.

        :return: True if the underlying image is the graphics window, False otherwise.
        """
        return self._win is not None

    def __del__(self):
        self.close()

    def is_immediate(self) -> bool:
        """
        Check if there are animations when turtles moving.

        :return: True if there aren't any animations (the move finishes immediately), False otherwise.
        """
        return self._immediate

    def set_immediate(self, immediate: bool):
        """
        Set if there are animations when turtles moving.

        :param immediate: True to turn off animation (the move finishes immediately). False to turn on.
        """
        if self._win is None:
            raise RuntimeError("We can't set immediate if not in graphics window!")
        self._immediate = immediate

    def get_width(self) -> float:
        """
        Get the width of the underlying graphics window (image).

        :return: width of the underlying graphics window (image)
        """
        return self._width

    def get_height(self) -> float:
        """
        Get the height of the underlying graphics window (image).

        :return: height of the underlying graphics window (image)
        """
        return self._height

    def _start_refresh_loop(self):
        self._refresh_thread = threading.Thread(target=self._refresh_loop)
        self._refresh_thread.start()

    def is_running(self):
        return self._running

    def _refresh_loop(self):
        while eg.is_run() :
            if not self._win.isVisible():
                self.set_immediate(True)
            if self._win.delay_fps(60):
                if not self._running:
                    break
                self._render()

        self.close()

    def get_world_image(self):
        """
        Return the drawing image of the world.

        :return: the drawing image of the world.
        """
        return self._world_image

    def clear_screen(self):
        """
        Delete all drawings from the screen. Do not move turtle.
        """
        for turtle in self._turtles:
            turtle.cancle_fill()
        self.get_world_image().clear()

    cs = clear_screen

    clear = clear_screen


class Turtle(object):
    """
    The Turtle class.
    """
    BASE_STEP = 1
    DEFAULT_ORENTATION = 90

    def __init__(self, world: TurtleWorld):
        """
        Initiator of the turtle class.

        :param world: the turtle world that the turtle will live in.
        """
        self._world = world
        self._x = 0
        self._y = 0
        self._heading = self.DEFAULT_ORENTATION
        self._pen_down = True
        self._speed = 500
        self._show_turtle = True
        self._icon = self.create_turtle_icon()
        self._last_fps_time = 0
        self._fillpath = []
        self._lock = threading.Lock()
        self._drawing_event = threading.Event()
        world.add_turtle(self)

    def set_speed(self, speed: int):
        """
        Set moving speed of the turtle.

        :param speed: the new speed
        """
        if speed <= 1:
            speed = 1
        self._speed = speed * 50

    def begin_fill(self):
        """
        Begin to record the turtle's shape drawing path for filling.
        """
        if self.is_filling():
            raise RuntimeError("last fill not finished! call end_fill() first!")
        self._fillpath.append(self._x)
        self._fillpath.append(self._y)

    def is_filling(self) -> bool:
        """
        Test if it is recording the turtle's drawing path (for fill).

        :return:
        """
        return len(self._fillpath) > 0

    def cancle_fill(self):
        """
        Cancle the turtle's drawing path recording.
        """
        self._fillpath.clear()

    def end_fill(self):
        """
        Fill the shape enclosed by the turtle's drawing path after the last call to begin_fill.
        """
        if not self.is_filling():
            return
        image = eg.create_image(self._world.get_width(), self._world.get_height())
        image.set_pen(QtGui.QPen(self._world.get_world_image().get_pen()))
        image.set_color(eg.Color.TRANSPARENT)
        image.set_line_style(eg.LineStyle.SOLID_LINE)
        image.set_brush(QtGui.QBrush(self._world.get_world_image().get_brush()))
        image.set_fill_rule(self._world.get_world_image().get_fill_rule())
        image.set_composition_mode(eg.CompositionMode.SOURCE)
        transform = self._world.get_world_image().get_transform()
        image.set_transform(transform)
        image.draw_polygon(*self._fillpath)
        self._world.get_world_image().reset_transform()
        self._world.get_world_image().draw_image(0, 0, image, with_background=False,
                                                 composition_mode=eg.CompositionMode.SOURCE_OVER)
        self._world.get_world_image().set_transform(transform)
        image.close()
        self._fillpath.clear()

    def forward(self, distance: float):
        """
        Move the turtle forward by the specified distance, in the direction the turtle is heading.

        :param distance: the distance to move
        """
        delta_x = self.BASE_STEP * math.cos(math.radians(self._heading))
        delta_y = self.BASE_STEP * math.sin(math.radians(self._heading))
        if distance < 0:
            delta_x = -delta_x
            delta_y = -delta_y
            distance = - distance
        old_x = x = self._x
        old_y = y = self._y
        i = 0
        image = self._world.get_world_image()
        while i < distance:
            if i + 1 < distance:
                x += delta_x
                y += delta_y
            else:
                x += (distance - i) * delta_x
                y += (distance - i) * delta_y
            if self._pen_down:
                image.line(old_x, old_y, x, y)
            old_x = x
            old_y = y
            self._x = x
            self._y = y
            self._refresh()
            if self.is_filling():
                self._fillpath.append(self._x)
                self._fillpath.append(self._y)
            i += 1

    fd = forward

    def backward(self, distance: float):
        """
        Move the turtle backward by the specified distance, in the direction the turtle is heading.

        :param distance: the distance to move
        """
        self.forward(-distance)

    bk = backward

    back = backward

    def left_turn(self, degree: float):
        """
        Turn turtle left (counter-clockwise) by \"degree\" degree.

        :param degree: the degree to turn
        """
        start_angle = self._heading
        if not self._world.is_immediate():
            if degree > 0:
                i = 0
                while i < degree:
                    self._heading = start_angle + i
                    self._refresh()
                    i += 2
            else:
                n_degree = - degree
                i = 0
                while i < n_degree:
                    self._heading = start_angle - i
                    self._refresh()
                    i += 2
        self._heading = (start_angle + degree) % 360
        if self._heading < 0:
            self._heading += 360
        self._refresh()

    lt = left_turn

    left = left_turn

    def right_turn(self, degree: float):
        """
        Turn turtle right (clockwise) by \"degree\" degree.

        :param degree: the degree to turn
        """
        self.left_turn(-degree)

    rt = right_turn

    right = right_turn

    def move_arc(self, radius: float, angle: float = 360):
        """
        Move the turtle in a arc path.

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
        abs_radius = abs(radius)
        if radius > 0:
            center_direction = self._heading + 90
            new_heading = self._heading + angle
            new_direction = new_heading - 90
        else:
            center_direction = self._heading - 90
            new_heading = self._heading - angle
            new_direction = new_heading + 90
        center_x = self._x + abs_radius * math.cos(math.radians(center_direction))
        center_y = self._y + abs_radius * math.sin(math.radians(center_direction))
        new_x = center_x + abs_radius * math.cos(math.radians(new_direction))
        new_y = center_y + abs_radius * math.sin(math.radians(new_direction))
        step = abs_radius * math.radians(1)
        abs_angle = abs(angle)
        i = 1
        while i < abs_angle:
            if angle > 0:
                self.forward(step)
                if radius > 0:
                    self.left_turn(1)
                else:
                    self.right_turn(1)
            else:
                self.backward(step)
                if radius > 0:
                    self.right_turn(1)
                else:
                    self.left_turn(1)
            i = i + 1
        self.gotoxy(new_x, new_y)
        self.set_heading(new_heading)

    def move_ellipse(self, radius_left: float, radius_top: float, angle: float = 360):
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
        if radius_top < 0:
            raise RuntimeError("The radius_top parameter must not less than 0!")
        abs_radius_left = abs(radius_left)
        if abs_radius_left > radius_top:
            a = abs_radius_left
            b = radius_top
            base_angle = 0
        else:
            a = radius_top
            b = abs_radius_left
            base_angle = 90
        e = math.sqrt(1 - b * b / a / a)

        if radius_left > 0:
            center_direction = self._heading + 90
        else:
            center_direction = self._heading - 90
        center_x = self._x + abs_radius_left * math.cos(math.radians(center_direction))
        center_y = self._y + abs_radius_left * math.sin(math.radians(center_direction))
        old_heading = self._heading
        abs_angle = abs(angle)
        if radius_left > 0:
            signed_angle = 90
        else:
            signed_angle = -90
        i = 1
        print(a, b, base_angle, center_x, center_y, old_heading)
        while i < abs_angle:
            if angle > 0:
                signed_i = i
            else:
                signed_i = -i
            r = b / math.sqrt(1 - (e * math.cos(math.radians(signed_i + base_angle))) ** 2)
            if radius_left > 0:
                new_heading = old_heading + signed_i
            else:
                new_heading = old_heading - signed_i
            heading_signed_angle = new_heading - signed_angle
            new_x = center_x + r * math.cos(math.radians(heading_signed_angle))
            new_y = center_y + r * math.sin(math.radians(heading_signed_angle))
            self.gotoxy(new_x, new_y)
            self._heading = new_heading

            self._refresh()
            i = i + 1

        r = b / math.sqrt(1 - (e * math.cos(math.radians(angle + base_angle))) ** 2)
        if radius_left > 0:
            new_heading = old_heading + angle
        else:
            new_heading = old_heading - angle
        heading_signed_angle = new_heading - signed_angle
        new_x = center_x + r * math.cos(math.radians(heading_signed_angle))
        new_y = center_y + r * math.sin(math.radians(heading_signed_angle))
        self.gotoxy(new_x, new_y)
        self.set_heading(new_heading)

    def is_show(self):
        """
        Check if the turtle is shown.

        :return: True the turtle is shown, False the turtle is hiding.
        """
        return self._show_turtle

    def show(self):
        """
        Show the turtle.
        """
        self._show_turtle = True

    def hide(self):
        """
        Hide the turtle.
        """
        self._show_turtle = False

    def gotoxy(self, x, y):
        """
        Move the turtle to point (x,y). Will leave traces if the pen is down.

        :param x: x coordinate value of the destination point.
        :param y: x coordinate value of the destination point.
        """
        if self._pen_down:
            self._world.get_world_image().line(x, y, self._x, self._y)
        self._x = x
        self._y = y
        if self.is_filling():
            self._fillpath.append(self._x)
            self._fillpath.append(self._y)

    def setxy(self, x, y):
        """
        Set the turtle's current position to point (x,y). Will not leave traces.

        :param x: x coordinate value of the destination point.
        :param y: y coordinate value of the destination point.
        """
        self._x = x
        self._y = y
        if self.is_filling():
            self._fillpath.append(self._x)
            self._fillpath.append(self._y)

    def set_heading(self, angle):
        """
        Set the angle current heading to the specified angle.

        :param angle: the new heading angle (in degrees).
        """
        self._heading = angle

    def turn_to(self, angle):
        """
        Turn the angle to orient to the specified angle.

        :param angle: the new heading angle (in degrees).
        """
        angle = angle % 360
        if angle < 0:
            angle = angle + 360
        self.left_turn(angle - self._heading)

    def facing(self, x, y):
        """
        Turn the turtle to face the point(x,y).

        :param x: x coordinate value of the point facing to
        :param y: y coordinate value of the point facing to
        """
        delta_x = x - self._x
        delta_y = y - self._y
        angle = math.degrees(math.atan2(delta_y, delta_x))
        self.turn_to(angle)

    def home(self):
        """
        Move the turtle back to the origin(0,0), and heading up. Will leave traces if the pen is down.
        """
        self.gotoxy(0, 0)
        self.set_heading(self.DEFAULT_ORENTATION)

    def pen_down(self):
        """
        Pull the pen down – drawing when the turtle moving.
        """
        self._pen_down = True

    def pen_up(self):
        """
        Pull the pen up – no drawing when the turtle moving.
        """
        self._pen_down = False

    pd = pen_down

    pu = pen_up

    def get_x(self) -> float:
        """
        Get the turtle's current x position.

        :return: the turtle's x position.
        """
        return self._x

    def get_y(self) -> float:
        """
        Get the turtle's current y position.

        :return: the turtle's y position.
        """
        return self._y

    def get_heading(self) -> float:
        """
        Get the turtle's heading angle.

        :return: the turtle's heading angle.
        """
        return self._heading

    def get_icon(self) -> Image:
        """
        Get the icon image of the turtle.

        :return: the icon image
        """
        return self._icon

    def close(self):
        """
        Close and cleanup the turtle.
        """
        self._icon.close()

    def __del__(self):
        self.close()

    @staticmethod
    def create_turtle_icon() -> Image:
        """
        Create the default turtle icon.

        :return: the turtle icon image
        """
        # width = 10
        # height = 10
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon = eg.load_image(base_dir + os.path.sep + "turtle.png")
        return icon

    def is_out_of_window(self) -> bool:
        """
        Test if the turtle is out of the graphics window.

        :return: True if the turtle is out of the window, False otherwise.
        """
        transform = self._world.get_world_image().get_transform()
        p = QtCore.QPointF(self._x, self._y)
        p_device = transform.map(p)
        rect = self._world.get_world_image().get_image().rect()
        return not rect.contains(round(p_device.x()), round(p_device.y()))

    def _refresh(self):
        if not self._world.is_immediate():
            self._delay_fps(self._speed)

    def _delay_fps(self, fps: int):
        """
        Delay to control fps without frame skipping. Never skip frames.

        :param fps: the desire fps
        """
        nanotime = 1000000000 // fps
        if self._last_fps_time == 0:
            self._last_fps_time = time.perf_counter_ns()
        tt = time.perf_counter_ns()
        while tt - self._last_fps_time < nanotime:
            tt = time.perf_counter_ns()
        self._last_fps_time = tt
