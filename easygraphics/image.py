from PyQt5 import QtGui, QtCore
from collections import deque
from typing import List

from easygraphics.consts import WriteMode, FillStyle

__all__ = ['Image']


class Image:
    def __init__(self, image: QtGui.QImage):
        self._image = image
        self._color = QtCore.Qt.black
        self._line_style = QtCore.Qt.SolidLine
        self._lineWidth = 1
        self._fill_color = QtCore.Qt.white
        self._fill_Style = QtCore.Qt.SolidPattern
        self._background_color = QtCore.Qt.transparent
        self._pen = QtGui.QPen()
        self._brush = QtGui.QBrush(QtCore.Qt.white, QtCore.Qt.SolidPattern)
        self._clip_rect: QtCore.QRect = None
        self._view_port: QtCore.QRect = None
        self._window: QtCore.QRect = None
        self._write_mode = WriteMode.R2_COPYPEN
        self._x = 0
        self._y = 0
        self._font = QtGui.QFont("SansSerif", 14)
        self._font_metrics = QtGui.QFontMetrics(self._font)
        self._transform = QtGui.QTransform()

    def get_image(self) -> QtGui.QImage:
        return self._image

    def get_width(self):
        return self._image.width()

    def get_height(self):
        return self._image.height()

    def get_pen(self) -> QtGui.QPen:
        return self._pen

    def set_pen(self, pen):
        self._pen = pen

    def get_brush(self) -> QtGui.QBrush:
        return self._brush

    def set_brush(self, brush):
        self._brush = brush

    def get_color(self):
        """
        get the foreground (drawing) color of the specified image

        it will be used when drawing lines or shape outlines

        :return: foreground color
        """
        return self._color

    def set_color(self, color):
        """
        set the foreground (drawing) color of the specified image

        it will be used when drawing lines or shape outlines

        the possible color could be consts defined in Color class,
        or the color created by rgb() function,
        or PyQt5's QColor , QGradient object or QtCore.Qt.GlobalColor consts (see the pyqt reference).

        :param color: foreground color
        """
        self._color = color
        self._pen.setColor(color)

    def get_fill_color(self):
        """
        get the fill color of the specified image

        it will be used when drawing and fill shapes.

        :return: fill color
        """
        return self._fill_color

    def set_fill_color(self, fill_color):
        """
        set the fill (drawing) color of the specified image

        it will be used when drawing and fill shapes.

        the possible color could be consts defined in Color class,
        or the color created by rgb() function,
        or PyQt5's QColor , QGradient object or QtCore.Qt.GlobalColor consts (see the pyqt reference).

        :param fill_color: fill color
        """
        self._fill_color = fill_color
        self._brush.setColor(fill_color)

    def get_background_color(self):
        """
        get the background color of the image

        it will be used when the image is cleared. (see clear_device())

        :return: background color
        """
        return self._background_color

    def set_background_color(self, background_color):
        """
        set the background  color of the image

        it will be used when the image is cleared. (see clear_device())

        the possible color could be consts defined in Color class,
        or the color created by rgb() function,
        or PyQt5's QColor , QGradient object or QtCore.Qt.GlobalColor consts (see the pyqt reference).

        :param background_color: background color
        """
        self._background_color = background_color

    def get_line_style(self):
        """
        get line style

        The line style will be used when drawing lines and shape outlines.

        :return: line style
        """
        return self._line_style

    def set_line_style(self, line_style):
        """
        set line style

        The line style will be used when drawing lines and shape outlines.
        Possible value is one of the consts defined in LineStyle.

        :param line_style: line style
        """
        self._line_style = line_style
        self._pen.setStyle(line_style)

    def get_line_width(self) -> float:
        """
        get line width (thickness)

        It will be used when drawing lines or shape outlines

        :return: line width
        """
        return self._lineWidth

    def set_line_width(self, width: float):
        """
        set line width (thinkness) of the specified image

        It will be used when drawing lines or shape outlines

        :param width: line width
        """
        self._lineWidth = width
        if isinstance(width, int):
            self._pen.setWidth(width)
        else:
            self._pen.setWidthF(width)

    def get_fill_style(self):
        """
        get fill style of the specified image

        it will be used when drawing and fill shapes.

        :return: fill style
        """
        return self._fill_Style

    def set_fill_style(self, fill_style):
        """
        set fill style of the specified image

        it will be used when drawing and fill shapes.
        Valid values are the consts defined in FillStyle

        :param fill_style: fill style
        """
        self._fill_Style = fill_style
        self._brush.setStyle(fill_style)

    def set_view_port(self, left: int, top: int, right: int, bottom: int):
        """
        set the view port of the the specified image

        View port is the drawing zone on the image.

        The drawing outside the view port is not clipped. If you want to clip the drawing ,use set_clip_rect()

        **if view port and "logical window" don't have the same width and height,
        drawing will get zoomed.** So set_window() is often used with the set_view_port

        :param left: left of the view port rectangle
        :param top: top of the view port rectangle
        :param right: right of the view port rectangle
        :param bottom: bottom of the view port rectangle
        """
        self._view_port = QtCore.QRect(left, top, right - left, bottom - top)

    def reset_view_port(self):
        """
        reset the view port to the whole image
        """
        self._view_port = None

    def set_clip_rect(self, left: int, top: int, right: int, bottom: int):
        self._clip_rect = QtCore.QRect(left, top, right - left, bottom - top)

    def reset_clip_rect(self):
        self._clip_rect = None

    def set_window(self, left: int, top: int, right: int, bottom: int):
        self._window = QtCore.QRect(left, top, right - left, bottom - top)

    def reset_window(self):
        self._window = None

    def translate(self, x: float, y: float):
        self._transform.translate(x, y)

    def rotate(self, degree: float):
        self._transform.rotate(degree)

    def scale(self, sx: float, sy: float):
        self._transform.scale(sx, sy)

    def reset_transform(self):
        self._transform.reset()

    def clear_view_port(self):
        p = QtGui.QPainter()
        p.begin(self._image)
        p.fillRect(self._view_port, self._background_color)
        p.end()

    def get_view_port(self) -> QtCore.QRect:
        return self._view_port

    def set_write_mode(self, mode):
        """
        set write mode of the specified image

        When drawing ,the write mode will decide how the result pixel color will be computed (using source color and
        color of the destination)

        source color is the color of the pen/brush

        destination color is the color of the pixel will be painted on

        the result color will be computed by bitwise operations

        :param mode: write mode
        """
        self._write_mode = mode

    def get_write_mode(self):
        """
        get write mode of the specified image

        When drawing ,the write mode will decide how the result pixel color will be computed
         (using source color and color of the destination)

        :return: write mode
        """
        return self._write_mode

    def move_to(self, x, y):
        """
        set the drawing position to (x,y)

        the drawing position is used by line_to(), line_rel() and move_rel()

        :param x: x coordinate value of the new drawing position
        :param y: y coordinate value of the new drawing position
        """
        self._x = x
        self._y = y

    def move_rel(self, dx: float, dy: float):
        """
        move the drawing position by (dx,dy)

        if the old position is (x,y), then the new position will be (x+dx,y+dy)

        the drawing position is used by line_to(), line_rel()

        :param dx: x coordinate offset of the new drawing position
        :param dy: y coordinate offset of the new drawing position
        """
        self._x += dx
        self._y += dy

    def line_to(self, x: float, y: float):
        """
        draw a line from the current drawing position to (x,y), then set the drawing position is set to (x,y)

        :param x: x coordinate value of the new drawing position
        :param y: y coordinate value of the new drawing position
        """
        self.line(self._x, self._y, x, y)
        self.move_to(x, y)

    def line_rel(self, dx: float, dy: float):
        """
         draw a line from the current drawing position (x,y) to (x+dx,y+dy), \
         then set the drawing position is set to (x+d,y+dy)

        :param dx: x coordinate offset of the new drawing position
        :param dy: y coordinate offset of the new drawing position
        """
        self.line(self._x, self._y, self._x + dx, self._y + dy)
        self.move_rel(dx, dy)

    def get_x(self) -> float:
        """
        get the x coordinate value of the current drawing position (x,y)

        some drawing functions will use the current pos to draw.(see line_to(),line_rel(),move_to(),move_rel())

        :return: the x coordinate value of the current drawing position
        """
        return self._x

    def get_y(self) -> float:
        """
        get the y coordinate value of the current drawing position (x,y)

        some drawing functions will use the current pos to draw.(see line_to(),line_rel(),move_to(),move_rel())

        :return: the y coordinate value of the current drawing position
        """
        return self._y

    def _prepare_painter(self, pen: QtGui.QPen, brush: QtGui.QBrush) -> QtGui.QPainter:
        p = QtGui.QPainter()
        p.begin(self._image)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        if self._clip_rect is not None:
            p.setClipRect(self._clip_rect)
        if self._view_port is not None:
            print(self._view_port.width(), self._view_port.height())
            p.setViewport(self._view_port)
        if self._window is not None:
            p.setWindow(self._window)
        if self._transform is not None:
            p.setTransform(self._transform)
        p.setCompositionMode(self._write_mode)
        if self._font is not None:
            p.setFont(self._font)
        p.setPen(pen)
        p.setBrush(brush)
        return p

    def _prepare_painter_for_draw_outline(self) -> QtGui.QPainter:
        """ prepare painter for draw outline """
        return self._prepare_painter(self._pen, QtCore.Qt.NoBrush)

    def _prepare_painter_for_draw(self) -> QtGui.QPainter:
        """ prepare painter for draw (with outline and fill)"""
        return self._prepare_painter(self._pen, self._brush)

    def _prepare_painter_for_fill(self) -> QtGui.QPainter:
        """ prepare painter for fill (without outline)"""
        return self._prepare_painter(QtCore.Qt.NoPen, self._brush)

    def draw_point(self, x: float, y: float):
        """
        draw a point at (x,y) on the specified image

        :param x: x coordinate value of the drawing point
        :param y: y coordinate value of the drawing point
        """
        p = self._prepare_painter_for_draw_outline()
        p.drawPoint(QtCore.QPointF(x, y))
        p.end()

    def draw_line(self, x1: float, y1: float, x2: float, y2: float):
        """
        Draw a line from (x1,y1) to (x2,y2) on the specified image

        :param x1: x coordinate value of the start point
        :param y1: y coordinate value of the start point
        :param x2: x coordinate value of the end point
        :param y2: y coordinate value of the start point
        """
        p = self._prepare_painter_for_draw_outline()
        p.drawLine(QtCore.QPointF(x1, y1), QtCore.QPointF(x2, y2))
        p.end()

    def line(self, x1: float, y1: float, x2: float, y2: float):
        """
        Draw a line from (x1,y1) to (x2,y2) on the specified image

        :param x1: x coordinate value of the start point
        :param y1: y coordinate value of the start point
        :param x2: x coordinate value of the end point
        :param y2: y coordinate value of the start point
        """
        self.draw_line(x1, y1, x2, y2)

    def ellipse(self, x: float, y: float, radius_x: float, radius_y: float):
        """
        draw an ellipse outline centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y

        the ellipse is not filled

        :param x: x coordinate value of the ellipse's center
        :param y: y coordinate value of the ellipse's center
        :param radius_x: radius on x-axis of the ellipse
        :param radius_y: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw_outline()
        p.drawEllipse(QtCore.QPointF(x, y), radius_x, radius_y)
        p.end()

    def draw_ellipse(self, x: float, y: float, radius_x: float, radius_y: float):
        """
        draw an ellipse centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y

        the ellipse is filled and has outline.

        :param x: x coordinate value of the ellipse's center
        :param y: y coordinate value of the ellipse's center
        :param radius_x: radius on x-axis of the ellipse
        :param radius_y: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw()
        p.drawEllipse(QtCore.QPointF(x, y), radius_x, radius_y)
        p.end()

    def fill_ellipse(self, x: float, y: float, radius_x: float, radius_y: float):
        """
        fill an ellipse centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y

        the ellipse dosen't has outline

        :param x: x coordinate value of the ellipse's center
        :param y: y coordinate value of the ellipse's center
        :param radius_x: radius on x-axis of the ellipse
        :param radius_y: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_fill()
        p.drawEllipse(QtCore.QPointF(x, y), radius_x, radius_y)
        p.end()

    def arc(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
        draw an elliptical arc from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
        at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

        :param x: x coordinate value of the ellipse's center
        :param y: y coordinate value of the ellipse's center
        :param start_angle: start angle of the arc
        :param end_angle: end angle of the arc
        :param radius_x: radius on x-axis of the ellipse
        :param radius_y: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw_outline()
        angle_len = end_angle - start_angle
        p.drawArc(QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y),
                  start_angle * 16, angle_len * 16)
        p.end()

    def draw_arc(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
        draw an elliptical arc from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
        at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

        :param x: x coordinate value of the ellipse's center
        :param y: y coordinate value of the ellipse's center
        :param start_angle: start angle of the arc
        :param end_angle: end angle of the arc
        :param radius_x: radius on x-axis of the ellipse
        :param radius_y: radius on y-axis of the ellipse
        """
        self.arc(x, y, start_angle, end_angle, radius_x, radius_y)

    def pie(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
        draw an elliptical pie outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        the pie is not filled.

        **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
        at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

        :param x: x coordinate value of the ellipse's center
        :param y: y coordinate value of the ellipse's center
        :param start_angle: start angle of the pie
        :param end_angle: end angle of the pie
        :param radius_x: radius on x-axis of the ellipse
        :param radius_y: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw_outline()
        angle_len = end_angle - start_angle
        p.drawPie(QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y),
                  start_angle * 16, angle_len * 16)
        p.end()

    def draw_pie(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
        draw an elliptical pie from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        the pie is filled and has outline.

        **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
        at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

        :param x: x coordinate value of the ellipse's center
        :param y: y coordinate value of the ellipse's center
        :param start_angle: start angle of the pie
        :param end_angle: end angle of the pie
        :param radius_x: radius on x-axis of the ellipse
        :param radius_y: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw()
        angle_len = end_angle - start_angle
        p.drawPie(QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y), start_angle * 16,
                  angle_len * 16)
        p.end()

    def fill_pie(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
        fill an elliptical pie from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        the pie dosen't have outline.

        **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
        at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

        :param x: x coordinate value of the ellipse's center
        :param y: y coordinate value of the ellipse's center
        :param start_angle: start angle of the pie
        :param end_angle: end angle of the pie
        :param radius_x: radius on x-axis of the ellipse
        :param radius_y: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_fill()
        angle_len = end_angle - start_angle
        p.drawPie(QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y), start_angle * 16,
                  angle_len * 16)
        p.end()

    def chord(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
         draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
         which radius on x-axis is radius_x and radius on y-axis is radius_y.

         the chord is not filled.

         **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
         at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

         :param x: x coordinate value of the ellipse's center
         :param y: y coordinate value of the ellipse's center
         :param start_angle: start angle of the chord
         :param end_angle: end angle of the chord
         :param radius_x: radius on x-axis of the ellipse
         :param radius_y: radius on y-axis of the ellipse
         """
        p = self._prepare_painter_for_draw_outline()
        angle_len = end_angle - start_angle
        p.drawChord(QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y), start_angle * 16,
                    angle_len * 16)
        p.end()

    def draw_chord(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
        draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        the chord is filled and has outline

        **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
        at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

        :param x: x coordinate value of the ellipse's center
        :param y: y coordinate value of the ellipse's center
        :param start_angle: start angle of the chord
        :param end_angle: end angle of the chord
        :param radius_x: radius on x-axis of the ellipse
        :param radius_y: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw()
        angle_len = end_angle - start_angle
        p.drawChord(QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y), start_angle * 16,
                    angle_len * 16)
        p.end()

    def fill_chord(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
        draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        the chord doesn't have outline.

        **note**: degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
        at 12 o'click , degree 180 is at 9 o'clock , degree 270 is at 6 o'clock, etc.

        :param x: x coordinate value of the ellipse's center
        :param y: y coordinate value of the ellipse's center
        :param start_angle: start angle of the chord
        :param end_angle: end angle of the chord
        :param radius_x: radius on x-axis of the ellipse
        :param radius_y: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_fill()
        angle_len = end_angle - start_angle
        p.drawChord(QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y), start_angle * 16,
                    angle_len * 16)
        p.end()

    def bezier(self, poly_points: list):
        """
        draw a bezier curve

        poly_points is a 2D point list. Each point has 2 coordinate values in the list. \
        So if you have 4 points (x0,y0),(x1,y1),(x2,y2),(x3,y3), the list should be  \
        [x0,y0,x1,y1,x2,y2,x3,y3]

        :param poly_points: point list
        """
        self.draw_bezier(poly_points)

    def draw_bezier(self, poly_points: list):
        """
        draw a bezier curve

        poly_points is a 2D point list. Each point has 2 coordinate values in the list. \
        So if you have 4 points (x0,y0),(x1,y1),(x2,y2),(x3,y3), the list should be  \
        [x0,y0,x1,y1,x2,y2,x3,y3]

        :param poly_points: point list
        """
        if len(poly_points) % 2 != 0:
            raise ValueError
        numpoints = len(poly_points) // 2
        if numpoints < 4:
            raise ValueError

        path = QtGui.QPainterPath(QtCore.QPointF(poly_points[0], poly_points[1]))
        for i in range(1, numpoints, 3):
            path.cubicTo(*poly_points[i * 2:i * 2 + 6])
        p = self._prepare_painter_for_draw_outline()
        p.drawPath(path)
        p.end()

    def lines(self, points: List[float]):
        self.draw_lines(points)

    def draw_lines(self, points: List[float]):
        numpoints = len(points) // 2
        if numpoints < 2:
            raise ValueError
        qpoints = []
        for i in range(0, numpoints, 2):
            qpoints.append(QtCore.QLineF(*points[i * 2:i * 2 + 4]))
        p = self._prepare_painter_for_draw_outline()
        p.drawLines(*qpoints)
        p.end()

    def poly_line(self, points: List[float]):
        self.draw_poly_line(points)

    def draw_poly_line(self, points: List[float]):
        qpoints = self._convert_to_qpoints(points)
        p = self._prepare_painter_for_draw_outline()
        p.drawPolyline(*qpoints)
        p.end()

    @staticmethod
    def _convert_to_qpoints(points):
        numpoints = len(points) // 2
        if numpoints < 2:
            raise ValueError
        qpoints = []
        for i in range(numpoints):
            qpoints.append(QtCore.QPointF(points[i * 2], points[i * 2 + 1]))
        return qpoints

    def polygon(self, points: List[float]):
        qpoints = self._convert_to_qpoints(points)
        p = self._prepare_painter_for_draw_outline()
        p.drawPolygon(*qpoints)
        p.end()

    def draw_polygon(self, points: List[float]):
        qpoints = self._convert_to_qpoints(points)
        p = self._prepare_painter_for_draw()
        p.drawPolygon(*qpoints)
        p.end()

    def fill_polygon(self, points: List[float]):
        qpoints = self._convert_to_qpoints(points)
        p = self._prepare_painter_for_fill()
        p.drawPolygon(*qpoints)
        p.end()

    def path(self, path: QtGui.QPainterPath):
        p = self._prepare_painter_for_draw_outline()
        p.drawPath(path)
        p.end()

    def draw_path(self, path: QtGui.QPainterPath):
        p = self._prepare_painter_for_draw()
        p.drawPath(path)
        p.end()

    def fill_path(self, path: QtGui.QPainterPath):
        p = self._prepare_painter_for_draw()
        p.drawPath(path)
        p.end()

    def rect(self, left: float, top: float, right: float, bottom: float):
        p = self._prepare_painter_for_draw_outline()
        p.drawRect(left, top, right - left, bottom - top)
        p.end()

    def draw_rect(self, left: float, top: float, right: float, bottom: float):
        p = self._prepare_painter_for_draw()
        p.drawRect(left, top, right - left, bottom - top)
        p.end()

    def fill_rect(self, left: float, top: float, right: float, bottom: float):
        p = self._prepare_painter_for_fill()
        p.drawRect(left, top, right - left, bottom - top)
        p.end()

    def rounded_rect(self, left: float, top: float, right: float, bottom: float, round_x: float, round_y: float):
        p = self._prepare_painter_for_draw_outline()
        p.drawRoundedRect(left, top, right - left, bottom - top, round_x, round_y)
        p.end()

    def draw_rounded_rect(self, left: float, top: float, right: float, bottom: float, round_x: float, round_y: float):
        p = self._prepare_painter_for_draw()
        p.drawRoundedRect(left, top, right - left, bottom - top, round_x, round_y)
        p.end()

    def fill_rounded_rect(self, left: float, top: float, right: float, bottom: float, round_x: float, round_y: float):
        p = self._prepare_painter_for_fill()
        p.drawRoundedRect(left, top, right - left, bottom - top, round_x, round_y)
        p.end()

    def clear(self):
        self._image.fill(self._background_color)

    def draw_image(self, x: int, y: int, image):
        p = QtGui.QPainter()
        p.begin(self._image)
        p.setCompositionMode(self._write_mode)
        p.drawImage(x, y, image.get_image())
        p.end()

    def flood_fill(self, x: int, y: int, border_color):
        if self._fill_Style == FillStyle.NULL_FILL:  # no need to fill
            return
        queue = deque()
        new_pos = self._transform.map(QtCore.QPoint(x, y))
        queue.append((new_pos.x(), new_pos.y()))
        bc = QtGui.QColor(border_color)
        sc = QtGui.QColor(self._fill_color).rgba()
        bits = [0] * (self._image.width() * self._image.height())
        while len(queue) > 0:
            x, y = queue.popleft()
            if x < 0 or y < 0 or x >= self._image.width() or y >= self._image.height():
                continue
            if self._clip_rect and (x < self._view_port.left()
                                    or x > self._view_port.right() or y < self._view_port.top()
                                    or y > self._view_port.bottom()):
                continue
            if bits[self._image.width() * y + x] == 1:
                continue
            c = self._image.pixel(x, y)
            pc = QtGui.QColor(c)
            if bc == pc:
                continue
            bits[self._image.width() * y + x] = 1
            self._image.setPixel(x, y, sc)
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))

    def get_pixel(self, x: int, y: int) -> QtGui.QColor:
        """
        get a pixel's color on the specified image

        :param x: x coordinate value of the pixel
        :param y: y coordinate value of the pixel
        :return: color of the pixel
        """
        return QtGui.QColor(self._image.pixel(x, y))

    def put_pixel(self, x: int, y: int, color):
        """
        set a pixel's color on the specified image

        :param x: x coordinate value of the pixel
        :param y: y coordinate value of the pixel
        :param color: the color
        """
        self._image.setPixel(x, y, color)

    def draw_text(self, x: int, y: int, *args, sep=' '):
        msgs = map(str, args)
        msg = sep.join(msgs)
        p = self._prepare_painter_for_draw()
        p.drawText(x, y, msg)

    def draw_rect_text(self, x: int, y: int, w: int, h: int, flags, *args, sep=' '):
        msgs = map(str, args)
        msg = sep.join(msgs)
        p = self._prepare_painter_for_draw()
        p.drawText(x, y, w, h, flags, msg)

    def set_font(self, font: QtGui.QFont):
        """
        set font of the specified image

        :param font:
        """
        self._font = font
        self._font_metrics = QtGui.QFontMetrics(self._font)

    def get_font(self) -> QtGui.QFont:
        """
        get font of the specified image

        :return: the font
        """
        return self._font

    def set_font_size(self, size: int):
        """
        set font size of the specified image
        :param size: font size
        """
        self._font.setPixelSize(size)
        self._font_metrics = QtGui.QFontMetrics(self._font)

    def get_font_size(self) -> int:
        """
        get font size of the specified image
        :return: font size
        """
        return self._font.pixelSize()

    def text_width(self, text: str) -> int:
        self._font_metrics.width(text)

    def text_height(self, text: str) -> int:
        self._font_metrics.height()
