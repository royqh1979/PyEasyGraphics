from collections import deque
from typing import List, Union

from PyQt5 import QtGui, QtCore

from easygraphics.consts import FillStyle, Color, LineStyle, CompositionMode

__all__ = ['Image']

class Image:
    def __init__(self, image: QtGui.QImage):
        self._image = image
        self._color = Color.BLACK
        self._line_style = LineStyle.SOLID_LINE
        self._lineWidth = 1
        self._fill_color = Color.WHITE
        self._fill_Style = FillStyle.SOLID_FILL
        self._background_color = Color.WHITE
        self._mask = QtGui.QBitmap(image.width(), image.height())
        self._mask.fill(QtCore.Qt.color1)
        self._pen = QtGui.QPen()
        self._brush = QtGui.QBrush(Color.WHITE, FillStyle.SOLID_FILL)
        self._x = 0
        self._y = 0
        self._painter = QtGui.QPainter()
        self._mask_painter = QtGui.QPainter()
        self._init_painter()
        self._init_mask_painter()

    def _init_painter(self):
        p = self._painter
        p.begin(self._image)
        p.setCompositionMode(CompositionMode.SOURCE)
        # p.setRenderHint(QtGui.QPainter.Antialiasing) # flood fill will not work when anti-aliasing is on
        self._default_rect = p.viewport()

    def _init_mask_painter(self):
        p = self._mask_painter
        p.begin(self._mask)
        p.setCompositionMode(CompositionMode.SOURCE)
        # p.setRenderHint(QtGui.QPainter.Antialiasing) # flood fill will not work when anti-aliasing is on

    def get_image(self) -> QtGui.QImage:
        """
        Get the internal QImage.

        **note** EasyGraphics don't require and release qpainter each time. Because there can only be one QPainter \
        for each QImage at time, so if you want to draw on this image customly, use get_painter() to get \
        the internal QPainter instance.

        :return: the QImage instance used internally
        """
        return self._image

    def get_width(self) -> int:
        """
        Get the width of the image.

        :return: image width
        """
        return self._image.width()

    def get_height(self):
        """
        Get the height  of the image.

        :return: image height
        """
        return self._image.height()

    def get_pen(self) -> QtGui.QPen:
        """
        Get the pen of the image

        :return: pen
        """
        return self._pen

    def set_pen(self, pen: QtGui.QPen):
        """
        Set pen

        :param pen: the pen to use.
        :return:
        """
        self._pen = pen

    def get_brush(self) -> QtGui.QBrush:
        """
        Get brush of the image

        :return: the brush
        """
        return self._brush

    def set_brush(self, brush: QtGui.QBrush):
        """
        Set brush

        :param brush: the brush
        """
        self._brush = brush

    def get_color(self):
        """
        Get the foreground (drawing) color of the specified image.

        It will be used when drawing lines or shape outlines.

        :return: foreground color
        """
        return self._color

    def set_color(self, color):
        """
        Set the foreground (drawing) color of the specified image.

        It will be used when drawing lines or shape outlines.

        The possible color could be consts defined in Color class,
        or the color created by rgb() function,
        or PyQt5's QColor , QGradient object or QtCore.Qt.GlobalColor consts (see the pyqt reference).

        :param color: foreground color
        """
        color = _to_qcolor(color)
        self._color = color
        self._pen.setColor(color)

    def get_fill_color(self):
        """
        Get the fill color of the specified image.

        It will be used when drawing and fill shapes.

        :return: fill color
        """
        return self._fill_color

    def set_fill_color(self, fill_color):
        """
        Set the fill (drawing) color of the specified image.

        It will be used when drawing and fill shapes.

        The possible color could be consts defined in Color class,
        or the color created by rgb() function,
        or PyQt5's QColor , QGradient object or QtCore.Qt.GlobalColor consts (see the pyqt reference).

        :param fill_color: fill color
        """
        fill_color = _to_qcolor(fill_color)
        self._fill_color = fill_color
        self._brush.setColor(fill_color)

    def get_background_color(self):
        """
        Get the background color of the image.

        It will be used when the image is cleared. (see clear_device())

        :return: background color
        """
        return self._background_color

    def set_background_color(self, background_color):
        """
        Set and change the background color.

        The possible color could be consts defined in Color class,
        or the color created by rgb() function,
        or PyQt5's QColor , QGradient object or QtCore.Qt.GlobalColor consts (see the pyqt reference).

        :param background_color: background color
        """
        background_color = _to_qcolor(background_color)
        self._background_color = background_color
        if self._painter.hasClipping():
            old_clip_region = self._painter.clipRegion()
            is_clipping = True
        else:
            is_clipping = False
        region = QtGui.QRegion(self._mask)
        self._painter.setClipping(True)
        self._painter.setClipRegion(region)
        self._painter.fillRect(0, 0, self.get_width(), self.get_height(), self._background_color)
        if is_clipping:
            self._painter.setClipRegion(old_clip_region)
        else:
            self._painter.setClipping(False)

    def get_line_style(self):
        """
        Get line style.

        The line style will be used when drawing lines and shape outlines.

        :return: line style
        """
        return self._line_style

    def set_line_style(self, line_style):
        """
        Set line style.

        The line style will be used when drawing lines and shape outlines.
        Possible value is one of the consts defined in LineStyle.

        :param line_style: line style
        """
        self._line_style = line_style
        self._pen.setStyle(line_style)

    def get_line_width(self) -> float:
        """
        Get line width (thickness).

        It will be used when drawing lines or shape outlines.

        :return: line width
        """
        return self._lineWidth

    def set_line_width(self, width: float):
        """
        Set line width (thinkness) of the specified image.

        It will be used when drawing lines or shape outlines.

        :param width: line width
        """
        self._lineWidth = width
        if isinstance(width, int):
            self._pen.setWidth(width)
        else:
            self._pen.setWidthF(width)

    def get_fill_style(self):
        """
        Get fill style of the specified image.

        It will be used when drawing and fill shapes.

        :return: fill style
        """
        return self._fill_Style

    def set_fill_style(self, fill_style):
        """
        Set fill style of the specified image.

        It will be used when drawing and fill shapes.
        Valid values are the consts defined in FillStyle

        :param fill_style: fill style
        """
        self._fill_Style = fill_style
        self._brush.setStyle(fill_style)

    def set_view_port(self, left: int, top: int, right: int, bottom: int):
        """
        Set the view port of the the specified image.

        View port is the drawing zone on the image.

        The drawing outside the view port is not clipped. If you want to clip the drawing ,use set_clip_rect()

        **if view port and "logical window" don't have the same width and height,
        drawing will get zoomed.** So set_window() is often used with the set_view_port

        :param left: left of the view port rectangle
        :param top: top of the view port rectangle
        :param right: right of the view port rectangle
        :param bottom: bottom of the view port rectangle
        """
        view_port = QtCore.QRect(left, top, right - left, bottom - top)
        self._painter.setViewport(view_port)
        self._mask_painter.setViewport(view_port)

    def reset_view_port(self):
        """
        Disable the view port setting.
        """
        self._painter.setViewport(self._default_rect)
        self._mask_painter.setViewport(self._default_rect)

    def set_clip_rect(self, left: int, top: int, right: int, bottom: int):
        """
        Set the clip rect.

        Drawings outside the clip rect will be clipped.

        :param left: left of the clip rectangle
        :param top: top of the clip rectangle
        :param right: right of the clip rectangle
        :param bottom: bottom of the clip rectangle
        """
        clip_rect = QtCore.QRect(left, top, right - left, bottom - top)
        self._painter.setClipRect(clip_rect)
        self._mask_painter.setClipRect(clip_rect)

    def disable_clip(self):
        """
        Disable clipping.

        Drawings will not be clipped.
        """
        self._painter.setClipping(False)
        self._mask_painter.setClipping(False)

    def set_window(self, origin_x: int, origin_y: int, width: int, height: int):
        """
        Set the logical drawing window.

        All your drawing is first drawing on the logical window, then mapping to view port (see set_view_port()).\
        The logical window's 4 corner points to streched to match the view port.

        If your view port is 200x200，and you use set_window(-50,-50,100,100) to get a 100x100 logical window with \
        the origin at (-50,50) , then the logical window's origin (0,0) is mapping to view port's (-50,-50), and \
        right-bottom corner (100,100) is mapping to view port's right bottom corner (200,200). All logical points is \
        mapping accordingly.

        If you just want to transform the drawing, use set_origin()/translate()/rotate()/scale().

        The drawing outside the logical window is not clipped. If you want to clip it, use set_clip_rect().

        :param origin_x: x pos of the logical window's origin
        :param origin_y: y pos of the logical window's origin
        :param width: width of the logical window
        :param height: height of the logical window
        """
        window = QtCore.QRect(origin_x, origin_y, width, height)
        self._painter.setWindow(window)
        self._mask_painter.setWindow(window)

    def reset_window(self):
        """
        Reset/remove the logical window.(see set_window())
        """
        self._painter.setWindow(self._default_rect)
        self._mask_painter.setWindow(self._default_rect)

    def translate(self, offset_x: float, offset_y: float):
        """
        Translates the coordinate system by the given offset; i.e. the given offset is added to points.

        :param offset_x: offset on the x coordinate
        :param offset_y: offset on the y coordinate
        """
        self._painter.translate(offset_x, offset_y)
        self._mask_painter.translate(offset_x, offset_y)

    def rotate(self, degree: float):
        """
        Rotates the coordinate system the given angle (in degree) clockwise.

        :param degree: the rotate angle (in degree)
        """
        self._painter.rotate(degree)
        self._mask_painter.rotate(degree)

    def scale(self, sx: float, sy: float):
        """
        Scales the coordinate system by (sx, sy).

        :param sx: scale factor on x axis.
        :param sy: scale factor on y axis.
        """
        self._painter.scale(sx, sy)
        self._mask_painter.scale(sx, sy)

    def reset_transform(self):
        """
        Reset all transforms (translate/rotate/scale).
        """
        self._painter.resetTransform()
        self._mask_painter.resetTransform()

    def clear_view_port(self):
        """
        Clear view port to show the background.
        """
        p = self._painter
        mode = p.compositionMode()
        p.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        p.fillRect(1, 1, p.window().width() - 1, p.window().height() - 1, Color.TRANSPARENT)
        p.setCompositionMode(mode)
        self._mask_painter.fillRect(1, 1, p.window().width() - 1, p.window().height() - 1, QtCore.Qt.color1)

    def set_composition_mode(self, mode):
        """
        Get composition mode of the specified image.

        Composition modes are used to specify how the pixels in the source (image/pen/brush),
        are merged with the pixel in the destination image.

        :param mode: composition mode
        """
        self._painter.setCompositionMode(mode)

    def get_composition_mode(self):
        """
        Get composition mode of the specified image.

        When drawing ,the composition mode will decide how the result pixel color will be computed
         (using source color and color of the destination).

        :return: composition mode
        """
        return self._painter.compositionMode()

    def move_to(self, x, y):
        """
        Set the drawing position to (x,y).

        The drawing position is used by line_to(), line_rel() and move_rel().

        :param x: x coordinate value of the new drawing position
        :param y: y coordinate value of the new drawing position
        """
        self._x = x
        self._y = y

    def move_rel(self, dx: float, dy: float):
        """
        Move the drawing position by (dx,dy).

        If the old position is (x,y), then the new position will be (x+dx,y+dy).

        The drawing position is used by line_to(), line_rel().

        :param dx: x coordinate offset of the new drawing position
        :param dy: y coordinate offset of the new drawing position
        """
        self._x += dx
        self._y += dy

    def line_to(self, x: float, y: float):
        """
        Draw a line from the current drawing position to (x,y), then set the drawing position is set to (x,y).

        :param x: x coordinate value of the new drawing position
        :param y: y coordinate value of the new drawing position
        """
        self.line(self._x, self._y, x, y)
        self.move_to(x, y)

    def line_rel(self, dx: float, dy: float):
        """
         Draw a line from the current drawing position (x,y) to (x+dx,y+dy), \
         then set the drawing position is set to (x+d,y+dy).

        :param dx: x coordinate offset of the new drawing position
        :param dy: y coordinate offset of the new drawing position
        """
        self.line(self._x, self._y, self._x + dx, self._y + dy)
        self.move_rel(dx, dy)

    def get_x(self) -> float:
        """
        Get the x coordinate value of the current drawing position (x,y).

        Some drawing functions will use the current pos to draw.(see line_to(),line_rel(),move_to(),move_rel()).

        :return: the x coordinate value of the current drawing position
        """
        return self._x

    def get_y(self) -> float:
        """
        Get the y coordinate value of the current drawing position (x,y).

        Some drawing functions will use the current pos to draw.(see line_to(),line_rel(),move_to(),move_rel())

        :return: the y coordinate value of the current drawing position
        """
        return self._y

    def _prepare_painter(self, pen: QtGui.QPen, brush: QtGui.QBrush) -> QtGui.QPainter:
        p = self._painter
        p.setPen(pen)
        p.setBrush(brush)
        if self._pen_transparent():
            self._mask_painter.setPen(QtCore.Qt.color1)
        else:
            self._mask_painter.setPen(QtCore.Qt.color0)
        if self._brush_transparent():
            self._mask_painter.setBrush(QtCore.Qt.color1)
        else:
            self._mask_painter.setBrush(QtCore.Qt.color0)
        return p

    def _prepare_painter_for_draw_outline(self) -> QtGui.QPainter:
        """ prepare painter for draw outline """
        return self._prepare_painter(self._pen, FillStyle.NULL_FILL)

    def _prepare_painter_for_draw(self) -> QtGui.QPainter:
        """ prepare painter for draw (with outline and fill)"""
        return self._prepare_painter(self._pen, self._brush)

    def _prepare_painter_for_fill(self) -> QtGui.QPainter:
        """ prepare painter for fill (without outline)"""
        return self._prepare_painter(LineStyle.NO_PEN, self._brush)

    def draw_point(self, x: float, y: float):
        """
        Draw a point at (x,y) on the specified image.

        :param x: x coordinate value of the drawing point
        :param y: y coordinate value of the drawing point
        """
        p = self._prepare_painter_for_draw_outline()
        point = QtCore.QPointF(x, y)
        p.drawPoint(point)
        self._mask_painter.drawPoint(point)

    def _pen_transparent(self):
        return self._painter.pen().style() == LineStyle.NO_PEN or self._painter.pen().color().alpha == 0

    def _brush_transparent(self):
        return self._painter.brush().style() == FillStyle.NULL_FILL or self._painter.pen().color().alpha == 1

    def draw_line(self, x1: float, y1: float, x2: float, y2: float):
        """
        Draw a line from (x1,y1) to (x2,y2) on the specified image.

        :param x1: x coordinate value of the start point
        :param y1: y coordinate value of the start point
        :param x2: x coordinate value of the end point
        :param y2: y coordinate value of the start point
        """
        p = self._prepare_painter_for_draw_outline()
        p1 = QtCore.QPointF(x1, y1)
        p2 = QtCore.QPointF(x2, y2)
        p.drawLine(p1, p2)
        self._mask_painter.drawLine(p1, p2)

    line = draw_line

    def ellipse(self, x: float, y: float, radius_x: float, radius_y: float):
        """
        Draw an ellipse outline centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y.

        The ellipse is not filled.

        :param x: x coordinate value of the ellipse's center
        :param y: y coordinate value of the ellipse's center
        :param radius_x: radius on x-axis of the ellipse
        :param radius_y: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw_outline()
        p1 = QtCore.QPointF(x, y)
        p.drawEllipse(p1, radius_x, radius_y)
        self._mask_painter.drawEllipse(p1, radius_x, radius_y)

    def draw_ellipse(self, x: float, y: float, radius_x: float, radius_y: float):
        """
        Draw an ellipse centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y.

        The ellipse is filled and has outline.

        :param x: x coordinate value of the ellipse's center
        :param y: y coordinate value of the ellipse's center
        :param radius_x: radius on x-axis of the ellipse
        :param radius_y: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw()
        p.drawEllipse(QtCore.QPointF(x, y), radius_x, radius_y)
        self._mask_painter.drawEllipse(QtCore.QPointF(x, y), radius_x, radius_y)

    def fill_ellipse(self, x: float, y: float, radius_x: float, radius_y: float):
        """
        Fill an ellipse centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y.

        The ellipse dosen't has outline.

        :param x: x coordinate value of the ellipse's center
        :param y: y coordinate value of the ellipse's center
        :param radius_x: radius on x-axis of the ellipse
        :param radius_y: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_fill()
        p.drawEllipse(QtCore.QPointF(x, y), radius_x, radius_y)
        self._mask_painter.drawEllipse(QtCore.QPointF(x, y), radius_x, radius_y)

    def draw_arc(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
        Draw an elliptical arc from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        **note**: Degree 0 is at 3 o'clock position, and is increasing clockwisely. That is, degree 90 is \
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
        rect = QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y)
        s = start_angle * 16
        al = angle_len * 16
        p.drawArc(rect, s, al)
        self._mask_painter.drawArc(rect, s, al)

    arc = draw_arc

    def pie(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
        Draw an elliptical pie outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        The pie is not filled.

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
        rect = QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y)
        s = start_angle * 16
        al = angle_len * 16
        p.drawPie(rect, s, al)
        self._mask_painter.drawPie(rect, s, al)

    def draw_pie(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
        Draw an elliptical pie from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        The pie is filled and has outline.

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
        rect = QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y)
        s = start_angle * 16
        al = angle_len * 16
        p.drawPie(rect, s, al)
        self._mask_painter.drawPie(rect, s, al)

    def fill_pie(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
        Fill an elliptical pie from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        The pie doesn\'t have outline.

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
        rect = QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y)
        s = start_angle * 16
        al = angle_len * 16
        p.drawPie(rect, s, al)
        self._mask_painter.drawPie(rect, s, al)

    def chord(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
         Draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
         which radius on x-axis is radius_x and radius on y-axis is radius_y.

         The chord is not filled.

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
        rect = QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y)
        s = start_angle * 16
        al = angle_len * 16
        p.drawChord(rect, s, al)
        self._mask_painter.drawChord(rect, s, al)

    def draw_chord(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
        Draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        The chord is filled and has outline.

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
        rect = QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y)
        s = start_angle * 16
        al = angle_len * 16
        p.drawChord(rect, s, al)
        self._mask_painter.drawChord(rect, s, al)

    def fill_chord(self, x: float, y: float, start_angle: float, end_angle: float, radius_x: float, radius_y: float):
        """
        Draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        The chord doesn't have outline.

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
        rect = QtCore.QRectF(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y)
        s = start_angle * 16
        al = angle_len * 16
        p.drawChord(rect, s, al)
        self._mask_painter.drawChord(rect, s, al)

    def draw_bezier(self, poly_points: list):
        """
        Draw a bezier curve.

        "poly_points" is a 2D point list. Each point has 2 coordinate values in the list. \
        So if you have 4 points (x0,y0),(x1,y1),(x2,y2),(x3,y3), the list should be  \
        [x0,y0,x1,y1,x2,y2,x3,y3] .

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
        self._mask_painter.drawPath(path)

    bezier = draw_bezier

    def draw_lines(self, points: List[float]):
        """
        Draw lines.

        "points" is a 2D point pair list. It should contain even points, and each 2 points make a point pair.
        And each point have 2 coordinate values(x,y). So if you have n point pairs, the points list should have 4*n
        values.

        For examples , if points is [50,50,550,350, 50,150,550,450, 50,250,550,550], draw_lines() will draw 3 lines:
        (50,50) to (550,350), (50,150) to (550,450), (50,250) to (550,550)

        :param points: point value list
        """
        numpoints = len(points) // 2
        if numpoints < 2:
            raise ValueError
        qlines = []
        for i in range(0, numpoints, 2):
            qlines.append(QtCore.QLineF(*points[i * 2:i * 2 + 4]))
        print(len(qlines))
        p = self._prepare_painter_for_draw_outline()
        p.drawLines(qlines)
        self._mask_painter.drawLines(qlines)

    lines = draw_lines

    def draw_poly_line(self, points: List[float]):
        """
        Draw poly lines.

        "points" is a 2D point list. Each 2 values in the list make a point. A poly line will be drawn to connect
        adjecent points defined by the the list.

        For examples , if points is [50,50,550,350, 50,150,550,450, 50,250,550,550], draw_poly_line() will draw 5 lines:
        (50,50) to (550,350), (550,350) to (50,150), (50,150) to (550,450), (550,540) to (50,250)
        and(50,250) to (550,550)

        :param points: point value list
        """
        qpoints = self._convert_to_qpoints(points)
        p = self._prepare_painter_for_draw_outline()
        p.drawPolyline(*qpoints)
        self._mask_painter.drawPolyline(*qpoints)

    poly_line = draw_poly_line

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
        """
        Draw polygon outline.

        "points" is a 2D point list. Each 2 values in the list make a point. A polygon will be drawn to connect adjacent
        points defined by the the list.

        For examples , if points is [50,50,550,350, 50,150], poly_gon() will draw a triangle with vertices at
        (50,50) , (550,350) and (50,150)

        The polygon is not filled.

        :param points: point value list
        """
        qpoints = self._convert_to_qpoints(points)
        p = self._prepare_painter_for_draw_outline()
        p.drawPolygon(*qpoints)
        self._mask_painter.drawPolygon(*qpoints)

    def draw_polygon(self, points: List[float]):
        """
        Draw polygon

        "points" is a 2D point list. Each 2 values in the list make a point. A polygon will be drawn to connect adjacent
        points defined by the the list.

        For examples , if points is [50,50,550,350, 50,150], poly_gon() will draw a triangle with vertices at
        (50,50) , (550,350) and (50,150)

        The polygon is filled and has outline.

        :param points: point value list
        """
        qpoints = self._convert_to_qpoints(points)
        p = self._prepare_painter_for_draw()
        p.drawPolygon(*qpoints)
        self._mask_painter.drawPolygon(*qpoints)

    def fill_polygon(self, points: List[float]):
        """
        Fill polygon

        "points" is a 2D point list. Each 2 values in the list make a point. A polygon will be drawn to connect adjacent
        points defined by the the list.

        For examples , if points is [50,50,550,350, 50,150], poly_gon() will draw a triangle with vertices at
        (50,50) , (550,350) and (50,150)

        The polygon doesn't have outline.

        :param points: point value list
        """
        qpoints = self._convert_to_qpoints(points)
        p = self._prepare_painter_for_fill()
        p.drawPolygon(*qpoints)
        self._mask_painter.drawPolygon(*qpoints)

    def path(self, path: QtGui.QPainterPath):
        """
        Draw a path.

        :param path: path to be drawn
        """
        p = self._prepare_painter_for_draw_outline()
        p.drawPath(path)
        self._mask_painter.drawPath(path)

    def draw_path(self, path: QtGui.QPainterPath):
        """
        Draw and fill a path.

        :param path: path to drawn and fill
        """
        p = self._prepare_painter_for_draw()
        p.drawPath(path)
        self._mask_painter.drawPath(path)

    def fill_path(self, path: QtGui.QPainterPath):
        """
        Fill the region enclosed by the path

        :param path: the path enclosing the region
        """
        p = self._painter
        self._prepare_painter_for_fill()
        p.fillPath(path, p.brush())
        self._mask_painter.fillPath(path, self._mask_painter.brush())

    def rect(self, left: float, top: float, right: float, bottom: float):
        """
        Draws a rectangle outline with upper left corner at (left, top) and lower right corner at (right,bottom).

        The rectangle is not filled.

        :param left: x coordinate value of the upper left corner
        :param top: y coordinate value of the upper left corner
        :param right: x coordinate value of the lower right corner
        :param bottom: y coordinate value of the lower right corner
        """
        p = self._prepare_painter_for_draw_outline()
        p.drawRect(left, top, right - left, bottom - top)
        self._mask_painter.drawRect(left, top, right - left, bottom - top)

    def draw_rect(self, left: float, top: float, right: float, bottom: float):
        """
        Draws a rectangle with upper left corner at (left, top) and lower right corner at (right,bottom).

        The rectangle is filled and has outline.

        :param left: x coordinate value of the upper left corner
        :param top: y coordinate value of the upper left corner
        :param right: x coordinate value of the lower right corner
        :param bottom: y coordinate value of the lower right corner
        """
        p = self._prepare_painter_for_draw()
        p.drawRect(left, top, right - left, bottom - top)
        self._mask_painter.drawRect(left, top, right - left, bottom - top)

    def fill_rect(self, left: float, top: float, right: float, bottom: float):
        """
        Draws a rectangle with upper left corner at (left, top) and lower right corner at (right,bottom).

        The rectangle doesn't have outline.

        :param left: x coordinate value of the upper left corner
        :param top: y coordinate value of the upper left corner
        :param right: x coordinate value of the lower right corner
        :param bottom: y coordinate value of the lower right corner
        """
        p = self._prepare_painter_for_fill()
        p.drawRect(left, top, right - left, bottom - top)
        self._mask_painter.drawRect(left, top, right - left, bottom - top)

    def rounded_rect(self, left: float, top: float, right: float, bottom: float, round_x: float, round_y: float):
        """
        Draws a rounded rectangle outline with upper left corner at (left, top) , lower right corner at (right,bottom).
        raidus on x-axis of the corner ellipse arc is round_x, radius on y-axis of the corner ellipse arc is round_y.

        The rectangle is not filled.

        :param left: x coordinate value of the upper left corner
        :param top: y coordinate value of the upper left corner
        :param right: x coordinate value of the lower right corner
        :param bottom: y coordinate value of the lower right corner
        :param round_x: raidus on x-axis of the corner ellipse arc
        :param round_y: radius on y-axis of the corner ellipse arc
        """
        p = self._prepare_painter_for_draw_outline()
        p.drawRoundedRect(left, top, right - left, bottom - top, round_x, round_y)
        self._mask_painter.drawRoundedRect(left, top, right - left, bottom - top, round_x, round_y)

    def draw_rounded_rect(self, left: float, top: float, right: float, bottom: float, round_x: float, round_y: float):
        """
        Draws a rounded rectangle with upper left corner at (left, top) , lower right corner at (right,bottom).
        raidus on x-axis of the corner ellipse arc is round_x, radius on y-axis of the corner ellipse arc is round_y.

        The rectangle is filled and has outline.

        :param left: x coordinate value of the upper left corner
        :param top: y coordinate value of the upper left corner
        :param right: x coordinate value of the lower right corner
        :param bottom: y coordinate value of the lower right corner
        :param round_x: raidus on x-axis of the corner ellipse arc
        :param round_y: radius on y-axis of the corner ellipse arc
        """
        p = self._prepare_painter_for_draw()
        p.drawRoundedRect(left, top, right - left, bottom - top, round_x, round_y)
        self._mask_painter.drawRoundedRect(left, top, right - left, bottom - top, round_x, round_y)

    def fill_rounded_rect(self, left: float, top: float, right: float, bottom: float, round_x: float, round_y: float):
        """
        Fill a rounded rectangle with upper left corner at (left, top) , lower right corner at (right,bottom).
        raidus on x-axis of the corner ellipse arc is round_x, radius on y-axis of the corner ellipse arc is round_y.

        The rectangle doesn't have outline.

        :param left: x coordinate value of the upper left corner
        :param top: y coordinate value of the upper left corner
        :param right: x coordinate value of the lower right corner
        :param bottom: y coordinate value of the lower right corner
        :param round_x: radius on x-axis of the corner ellipse arc
        :param round_y: radius on y-axis of the corner ellipse arc
        """
        p = self._prepare_painter_for_fill()
        p.drawRoundedRect(left, top, right - left, bottom - top, round_x, round_y)
        self._mask_painter.drawRoundedRect(left, top, right - left, bottom - top, round_x, round_y)

    def clear(self):
        """
        Clear the image to show the background.
        """
        self._image.fill(self._background_color)
        self._mask.fill(QtCore.Qt.color1)

    def draw_image(self, x: int, y: int, image: "Image", src_x: int = 0, src_y: int = 0, src_width: int = -1,
                   src_height: int = -1, with_background=True, composition_mode=None):
        """
        Copy part of the source image (image) to the destination image (self) at (x,y).

        (x, y) specifies the top-left point in the destination image that is to be drawn onto.

        (sx, sy) specifies the top-left point of the part in the source image that is to \
         be drawn. The default is (0, 0).

        (sw, sh) specifies the size of the part of the source image that is to be drawn.  \
        The default, (0, 0) (and negative) means all the way to the bottom-right of the image.

        If with_background is False, the source image's background will not be copied.

        The final result will depend on the composition mode and the source image's background.
        In the default mode (CompositionMode.SOURCE), the source will fully overwrite the destination).

        If you want to get a transparent copy, you should use CompositionMode.SOURCE_OVER and with_background = False.

        :param x: x coordinate value of the upper left point on the destination image
        :param y: y coordinate value of the upper left point on the destination image
        :param image: the source image to be copied
        :param src_x: x coordinate value of the top-left point of of the part to be drawn
        :param src_y: y coordinate value of the top-left point of of the part to be drawn
        :param src_width: witdh of the top-left point of of the part to be drawn
        :param src_height: height of the top-left point of of the part to be drawn
        :param with_background: if the background should be copied.
        :param composition_mode: if is None, use dst image's composition mode to copy.
        """
        p = self._painter
        old_mode = CompositionMode.SOURCE
        if composition_mode is not None:
            old_mode = p.compositionMode()
            p.setCompositionMode(composition_mode)
        img = image.get_image()
        if not with_background:
            img = QtGui.QImage(image.get_width(), image.get_height(), QtGui.QImage.Format_ARGB32_Premultiplied)
            img.fill(Color.TRANSPARENT)
            painter = QtGui.QPainter()
            painter.begin(img)
            region = QtGui.QRegion(image._mask)
            full_region = QtGui.QRegion(0, 0, image.get_width(), image.get_height())
            new_region = full_region.subtracted(region)
            painter.setClipRegion(new_region)
            painter.drawImage(0, 0, image.get_image())
            painter.end()
        p.drawImage(x, y, img, src_x, src_y, src_width, src_height)
        self._mask_painter.fillRect(x, y, src_width, src_height, QtCore.Qt.color0)
        if composition_mode is not None:
            p.setCompositionMode(old_mode)

    def draw_to_device(self, device: QtGui.QPaintDevice):
        """
        Draw the whole image to the specified device.

        :param device: the device to be drawn on
        """
        p = QtGui.QPainter()
        p.begin(device)
        p.drawImage(0, 0, self._image)
        p.end()

    def flood_fill(self, x: int, y: int, border_color):
        """
        Flood fill the image starting from(x,y) and ending at borders with border_color.

        The fill region border must be closed,or the whole image will be filled!

        :param x: x coordinate value of the start point
        :param y: y coordinate value of the start point
        :param border_color: color of the fill region border
        """
        if self._fill_Style == FillStyle.NULL_FILL:  # no need to fill
            return
        queue = deque()
        transform = self._painter.combinedTransform()
        new_pos = transform.map(QtCore.QPoint(x, y))
        queue.append((new_pos.x(), new_pos.y()))
        bc = QtGui.QColor(border_color).rgba()
        sc = QtGui.QColor(self._fill_color)
        flags = [0] * (self._image.width() * self._image.height())
        r = None
        if self._painter.hasClipping():
            r = self._painter.clipBoundingRect()
            r = transform.mapRect(r)
        self._mask_painter.setPen(QtCore.Qt.color0)
        while len(queue) > 0:
            x, y = queue.popleft()
            if x < 0 or y < 0 or x >= self._image.width() or y >= self._image.height():
                continue
            if r is not None and not r.contains(x, y):
                continue
            if flags[self._image.width() * y + x] == 1:
                continue
            pc = self._image.pixel(x, y)
            if bc == pc:
                continue
            flags[self._image.width() * y + x] = 1
            self._image.setPixelColor(x, y, sc)
            self._mask_painter.drawPoint(x, y)
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))

    def get_pixel(self, x: int, y: int) -> QtGui.QColor:
        """
        Get a pixel's color on the specified image.

        :param x: x coordinate value of the pixel
        :param y: y coordinate value of the pixel
        :return: color of the pixel
        """
        return QtGui.QColor(self._image.pixel(x, y))

    def put_pixel(self, x: int, y: int, color):
        """
        Set a pixel's color on the specified image.

        :param x: x coordinate value of the pixel
        :param y: y coordinate value of the pixel
        :param color: the color
        """
        self._image.setPixel(x, y, color)

    def draw_text(self, x: int, y: int, *args, sep=' '):
        """
        Prints the given texts beginning at the given position (x,y).

        :param x: x coordinate value of the start point
        :param y: y coordinate value of the start point
        :param args: things to be printed
        :param sep: seperator used to join strings
        """
        msgs = map(str, args)
        msg = sep.join(msgs)
        p = self._prepare_painter_for_draw()
        p.drawText(x, y, msg)
        self._mask_painter.drawText(x, y, msg)

    def draw_rect_text(self, x: int, y: int, width: int, height: int, flags=QtCore.Qt.AlignCenter, *args, sep=' '):
        """
        print the given texts in the specified rectangle area

        Available flags are: （Defined in pyqt5's PyQt5.QtCore pacakge)

        * Qt.AlignLeft          Aligns with the left edge.
        * Qt::AlignRight        Aligns with the right edge.
        * Qt::AlignHCenter      Centers horizontally in the available space.
        * Qt::AlignJustify      Justifies the text in the available space.
        * Qt::AlignTop          Aligns with the top.
        * Qt::AlignBottom       Aligns with the bottom.
        * Qt::AlignVCenter      Centers vertically in the available space.
        * Qt::AlignCenter       Centers in both dimensions.
        * Qt::TextDontClip      If it's impossible to stay within the given bounds, it prints outside.
        * Qt::TextSingleLine    Treats all whitespace as spaces and prints just one line.
        * Qt::TextExpandTabs    Makes the U+0009 (ASCII tab) character move to the next tab stop.
        * Qt::TextShowMnemonic  Displays the string "&P" as P For an ampersand, use "&&".
        * Qt::TextWordWrap      Breaks lines at appropriate points, e.g. at word boundaries.

        :param x: x coordinate of the output rectangle's upper left corner
        :param y: y coordinate of the output rectangle's upper left corner
        :param width: width of the output rectangle
        :param height: height of the output rectangle
        :param args: things to be printed (like print())
        :param flags: align flags
        :param sep: seperator used to join strings
        """
        msgs = map(str, args)
        msg = sep.join(msgs)
        p = self._prepare_painter_for_draw()
        p.drawText(x, y, width, height, flags, msg)
        self._mask_painter.drawText(x, y, width, height, flags, msg)

    def set_font(self, font: QtGui.QFont):
        """
        set font of the specified image

        :param font:
        """
        self._painter.setFont(font)
        self._mask_painter.setFont(font)

    def get_font(self) -> QtGui.QFont:
        """
        get font of the specified image

        :return: the font
        """
        return self._painter.font()

    def set_font_size(self, size: int):
        """
        set font size of the specified image
        :param size: font size
        """
        font = self._painter.font()
        font.setPixelSize(size)
        self._painter.setFont(font)
        self._mask_painter.setFont(font)

    def get_font_size(self) -> int:
        """
        get font size of the specified image
        :return: font size
        """
        return self._painter.font().pixelSize()

    def text_width(self, text: str) -> int:
        """
        return width of the text

        :param text: the text
        """
        return self._painter.fontMetrics().width(text)

    def text_height(self) -> int:
        """
        return height of the text (font height)
        """
        return self._painter.fontMetrics().height()

    def close(self):
        self._painter.end()
        self._mask_painter.end()

    def get_painter(self) -> QtGui.QPainter:
        """
        get the QPainter instance for drawing the image
        :return: the painter used internally
        """
        return self._painter


def _to_qcolor(val: Union[int, str, QtGui.QColor]) -> Union[QtGui.QColor, int]:
    if isinstance(val, str) or type(val) == int:
        # don't use isinstance(val,int), because predefined Color values (eg. Color.RED) will also make it True!
        color = QtGui.QColor(val)
        if not color.isValid():
            raise ValueError("%s is not a valid color!" % str(val))
    else:
        color = val
    return color
