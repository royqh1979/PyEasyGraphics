from collections import deque
from pathlib import Path
from typing import Union, Callable
import math

from PyQt5 import QtGui, QtCore

from easygraphics.consts import FillStyle, Color, LineStyle, CompositionMode, FillRule, ShapeMode, VertexType
import qimage2ndarray as qn

_in_ipython = False
try:
    __IPYTHON__
    import IPython.display

    _in_ipython = True
except NameError:
    pass

__all__ = ['Image']


class Image:
    """
    The image class.

    Use PyQt's QImage to save the drawing, and QPainter as the underlying drawing device.

    Note that the painter is keep and reused, if you want to draw on the image by yourself,
    please use get_painter() to get the painter and draw.And also note there is a mask image
    for background processing. You should get the mask right or you will get wrong result
    with set_background_color() and draw_image(with_background=False).
    """

    def __init__(self, image: QtGui.QImage):
        self._image = image
        self._image_view = None
        self._color = _to_qcolor(Color.BLACK)
        self._line_style = LineStyle.SOLID_LINE
        self._line_width = 1
        self._fill_color = _to_qcolor(Color.WHITE)
        self._fill_style = FillStyle.SOLID_FILL
        self._fill_rule = FillRule.ODD_EVEN_FILL
        self._background_color = _to_qcolor(Color.WHITE)
        self._mask = QtGui.QImage(image.width(), image.height(), QtGui.QImage.Format_ARGB32_Premultiplied)
        self._mask_view = qn.raw_view(self._mask)
        self._mask.fill(MASK_WHITE)
        self._pen = QtGui.QPen()
        self._pen.setColor(Color.BLACK)
        self._pen.setCapStyle(QtCore.Qt.RoundCap)
        self._pen.setJoinStyle(QtCore.Qt.RoundJoin)
        self._pen.setCosmetic(True)
        self._brush = QtGui.QBrush(Color.WHITE, FillStyle.SOLID_FILL)
        self._x = 0
        self._y = 0
        self._flip_y = False
        self._painter = QtGui.QPainter()
        self._mask_painter = QtGui.QPainter()
        self._init_painter()
        self._init_mask_painter()
        self._updated_listeners = []
        self._transform_stack = []
        self._rect_mode = ShapeMode.CORNERS
        self._ellipse_mode = ShapeMode.RADIUS
        self._old_flip_y = False
        self._old_rect_mode = ShapeMode.CORNERS
        self._old_ellipse_mode = ShapeMode.RADIUS
        self._old_color = _to_qcolor(Color.BLACK)
        self._old_line_style = LineStyle.SOLID_LINE
        self._old_line_width = 1
        self._old_fill_color = _to_qcolor(Color.WHITE)
        self._old_fill_style = FillStyle.SOLID_FILL
        self._old_fill_rule = FillRule.ODD_EVEN_FILL
        self._old_background_color = _to_qcolor(Color.WHITE)
        self._shape_path = None
        self._shape_vertext_type = VertexType.POLY_LINE
        self._shape_vertices = []
        self._shape_transformed_vertices = []
        self._is_curve_shape = False

    def _init_painter(self):
        p = self._painter
        p.begin(self._image)
        p.setCompositionMode(CompositionMode.SOURCE_OVER)
        # p.setRenderHint(QtGui.QPainter.Antialiasing) # flood fill will not work when anti-aliasing is on
        self._default_rect = p.viewport()

    def set_antialiasing(self,anti:bool=True):
        """
        Set Anti Aliasing

        :param anti: if antialiasing should be set
        """
        self._painter.setRenderHint(QtGui.QPainter.Antialiasing,anti)

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
        Set pen.

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
        Set the brush.

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

    def set_fill_rule(self, rule):
        """
        Set the fill rule (algorithm) for filling polygons.

        :param rule: the rule to be used for filling polygons
        """
        self._fill_rule = rule

    def get_fill_rule(self):
        """
        Get the fill rule (algorithm) for filling polygons.

        :return: the rule used for filling polygons
        """
        return self._fill_rule

    def get_background_color(self):
        """
        Get the background color of the image.

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
        foreground = _get_foreground(self)
        self._image.fill(background_color)
        self._painter.save()
        self._painter.resetTransform()
        self._painter.setCompositionMode(CompositionMode.SOURCE_OVER)
        self._painter.drawImage(0, 0, foreground)
        self._painter.restore()
        self._updated()

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
        return self._line_width

    def set_line_width(self, width: float):
        """
        Set line width (thinkness).

        It will be used when drawing lines or shape outlines.

        :param width: line width
        """
        self._line_width = width
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
        return self._fill_style

    def set_fill_style(self, fill_style):
        """
        Set fill style of the specified image.

        It will be used when drawing and fill shapes.
        Valid values are the consts defined in FillStyle

        :param fill_style: fill style
        """
        self._fill_style = fill_style
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
        Reset the view port setting.
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

    def set_clipping(self, clipping: bool):
        """
        Set clipping.

        Use set_clip_rect() to set the clip rectangle.

        :param clipping:  True will turn on clipping, False will turn off clipping
        """
        self._painter.setClipping(clipping)
        self._mask_painter.setClipping(clipping)

    def set_window(self, left: int, top: int, width: int, height: int):
        """
        Set the logical drawing window.

        All your drawing is first drawing on the logical window, then mapping to view port (see set_view_port()).
        The logical window\'s 4 corner points to streched to match the view port.

        If your view port is 200x200，and you use set_window(-50,-50,100,100) to get a 100x100 logical window with
        the left-top corner at (-50,-50) , then the logical window\'s left corner (-50,-50) is set to view port\'s (0,0),
        and right-bottom corner (50,50) is set to view port\'s right bottom corner (200,200). All logical points is
        mapping accordingly.

        If you just want to transform the drawing, use set_origin()/translate()/rotate()/scale().

        The drawing outside the logical window is not clipped. If you want to clip it, use set_clip_rect().

        :param left: x pos of the logical window's left-top corner
        :param top: y pos of the logical window's left-top corner
        :param width: width of the logical window
        :param height: height of the logical window
        """
        window = QtCore.QRect(left, top, width, height)
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

    def rotate(self, degree: float, x: float = 0, y: float = 0):
        """
        Rotates the coordinate system around the point (x,y) with the given angle (in degree) clockwise.

        :param degree: the rotate angle (in degree)
        :param x: the x coordinate of the rotation center
        :param y: the y coordinate of the rotation center
        """
        self.translate(x, y)
        self._painter.rotate(degree)
        self._mask_painter.rotate(degree)
        self.translate(-x, -y)

    def scale(self, sx: float, sy: float):
        """
        Scales the coordinate system by (sx, sy).

        :param sx: scale factor on x axis.
        :param sy: scale factor on y axis.
        """
        self._painter.scale(sx, sy)
        self._mask_painter.scale(sx, sy)

    def shear(self, sh: float, sv: float, x: float = 0, y: float = 0):
        """
        Shear (skew) the coordinates around the point (x,y) by sh,sv.

        :param sh: shear ratio on the x-axis
        :param sv: shear ratio on the y-axis
        :param x: the x coordinate of the skew center
        :param y: the y coordinate of the skew center
        """
        self.translate(x, y)
        self._painter.shear(sh, sv)
        self._mask_painter.shear(sh, sv)
        self.translate(-x, -y)

    skew = shear

    def reflect(self, x: float, y: float, x1: float = 0, y1: float = 0):
        """
        Reflect the coordinates against the line passing (x1,y1) and (x,y).

        **Note that all things will get reflected, including text!**
        If you just want to draw on a normal coordinate system with the y-axis grows bottom up,
        use set_flip_y()..

        :param x: x coordinate value of the first point
        :param y: y coordinate value of the first point
        :param x1: the x coordinate of  the second point
        :param y1: the y coordinate of the second point
        """
        if math.isclose(x, x1) and math.isclose(y, y1):
            raise ValueError("point(x,y) and point(x1,y1) should not be the same!")
        self.translate(x1, y1)
        transform = self._get_reflect_transform(x - x1, y - y1)
        self._painter.setTransform(transform, True)
        self._mask_painter.setTransform(transform, True)
        self.translate(-x1, -y1)

    @staticmethod
    def _get_reflect_transform(x, y):
        xx = x * x
        yy = y * y
        ll = xx + yy
        xy2 = 2 * x * y
        transform = QtGui.QTransform((xx - yy) / ll, xy2 / ll, xy2 / ll, (yy - xx) / ll, 0, 0)
        return transform

    flip = reflect

    mirror = reflect

    def set_flip_y(self, flip_y: bool) -> None:
        """
        Reflect with x-aixs as the axis (upside down). Texts will not flip.

        **Don't translate the origin to other points** (but you can translate and then translate back)
        before drawing any text. Or the text position's calculation will get wrong! So if you want to
        set the origin to the image/image's center, call set_flip_y() after the set_origin() or
        translate()!

        **Note**: Use this functions instead of the reflect()/flip()/mirror(),if you only
        want to draw on an ordinary coordinate system with y-axis grows bottom-up.

        :param flip_y: True to turn on the flip, False to turn off.
        """
        if flip_y == self._flip_y:  # do nothing if flip not changed
            return
        # translate around the x-axis ( if the image is already flipped, this will flip the image back).
        self.reflect(1, 0)
        self._flip_y = flip_y

    def get_transform(self) -> QtGui.QTransform:
        """
        Get transform matrix of the image.

        :return: the transform matrix
        """
        return self._painter.transform()

    def set_transform(self, transform: QtGui.QTransform):
        """
        Set image's transform matrix.

        :param transform: the transform matrix to set
        """
        self._painter.setTransform(transform)
        self._mask_painter.setTransform(transform)

    def push_transform(self):
        """
        Push (save) the current transform to the transform stack.
        """
        self._transform_stack.append(self._painter.transform())

    def pop_transform(self):
        """
        Pop the last saved transform from the transform stack, and use it as the current transform.
        """
        if len(self._transform_stack) <= 0:
            raise RuntimeError("No more transforms to pop!")
        transform = self._transform_stack.pop()
        self.set_transform(transform)

    def reset_transform(self):
        """
        Reset all transforms (translate/rotate/scale).
        """
        self._flip_y = False
        self._painter.resetTransform()
        self._mask_painter.resetTransform()

    def clear_view_port(self):
        """
        Clear view port to show the background.
        """
        p = self._painter
        mode = p.compositionMode()
        p.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        p.fillRect(1, 1, p.window().width() - 1, p.window().height() - 1, self._background_color)
        p.setCompositionMode(mode)
        self._mask_painter.fillRect(1, 1, p.window().width() - 1, p.window().height() - 1, MASK_WHITE)
        self._updated()

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
        Draw a line from the current drawing position (x,y) to (x+dx,y+dy),
        then set the drawing position is set to (x+dx,y+dy).

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
        if self._no_pen():
            self._mask_painter.setPen(LineStyle.NO_PEN)
        else:
            self._mask_painter.setPen(MASK_BLACK)
        if self._no_brush():
            self._mask_painter.setBrush(FillStyle.NULL_FILL)
        else:
            self._mask_painter.setBrush(MASK_BLACK)
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
        self._updated()

    def _no_pen(self):
        return self._painter.pen().style() == LineStyle.NO_PEN

    def _no_brush(self):
        return self._painter.brush().style() == FillStyle.NULL_FILL

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
        self._updated()

    line = draw_line

    def ellipse(self, x1: float, y1: float, x2: float, y2: float):
        """
        Draw an ellipse outline centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y.

        The ellipse is not filled.

        :param x1: x coordinate value of the ellipse's center
        :param y1: y coordinate value of the ellipse's center
        :param x2: radius on x-axis of the ellipse
        :param y2: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw_outline()
        self._draw_ellipse(p, x1, y1, x2, y2)
        self._updated()

    def _draw_ellipse(self, p, x1, y1, x2, y2):
        rect = _calc_rect(x1, y1, x2, y2, self._ellipse_mode)
        p.drawEllipse(rect)
        self._mask_painter.drawEllipse(rect)

    def draw_ellipse(self, x1: float, y1: float, x2: float, y2: float):
        """
        Draw an ellipse centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y.

        The ellipse is filled and has outline.

        :param x1: x coordinate value of the ellipse's center
        :param y1: y coordinate value of the ellipse's center
        :param x2: radius on x-axis of the ellipse
        :param y2: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw()
        self._draw_ellipse(p, x1, y1, x2, y2)
        self._updated()

    def fill_ellipse(self, x1: float, y1: float, x2: float, y2: float):
        """
        Fill an ellipse centered at (x,y) , radius on x-axis is radius_x, radius on y-axis is radius_y.

        The ellipse dosen't has outline.

        :param x1: x coordinate value of the ellipse's center
        :param y1: y coordinate value of the ellipse's center
        :param x2: radius on x-axis of the ellipse
        :param y2: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_fill()
        self._draw_ellipse(p, x1, y1, x2, y2)
        self._updated()

    def draw_arc(self, x1: float, y1: float, start_angle: float, end_angle: float, x2: float, y2: float):
        """
        Draw an elliptical arc from start_angle to end_angle. The base ellipse is centered at (x,y)  \
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

          Note: Positive values for the angles mean counter-clockwise
          while negative values mean the clockwise direction. Zero degrees is at the 3 o'clock position.

        :param x1: x coordinate value of the ellipse's center
        :param y1: y coordinate value of the ellipse's center
        :param start_angle: start angle of the arc
        :param end_angle: end angle of the arc
        :param x2: radius on x-axis of the ellipse
        :param y2: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw_outline()
        angle_len = end_angle - start_angle
        rect = _calc_rect(x1, y1, x2, y2, self._ellipse_mode)
        s = start_angle * 16
        al = angle_len * 16
        p.drawArc(rect, s, al)
        self._mask_painter.drawArc(rect, s, al)
        self._updated()

    arc = draw_arc

    def pie(self, x1: float, y1: float, start_angle: float, end_angle: float, x2: float, y2: float):
        """
        Draw an elliptical pie outline from start_angle to end_angle. The base ellipse is centered at (x,y)
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        The pie is not filled.

          Note: Positive values for the angles mean counter-clockwise
          while negative values mean the clockwise direction. Zero degrees is at the 3 o'clock position.

        :param x1: x coordinate value of the ellipse's center
        :param y1: y coordinate value of the ellipse's center
        :param start_angle: start angle of the pie
        :param end_angle: end angle of the pie
        :param x2: radius on x-axis of the ellipse
        :param y2: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw_outline()
        angle_len = end_angle - start_angle
        rect = _calc_rect(x1, y1, x2, y2, self._ellipse_mode)
        s = start_angle * 16
        al = angle_len * 16
        p.drawPie(rect, s, al)
        self._mask_painter.drawPie(rect, s, al)
        self._updated()

    def draw_pie(self, x1: float, y1: float, start_angle: float, end_angle: float, x2: float, y2: float):
        """
        Draw an elliptical pie from start_angle to end_angle. The base ellipse is centered at (x,y)
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        The pie is filled and has outline.

          Note: Positive values for the angles mean counter-clockwise
          while negative values mean the clockwise direction. Zero degrees is at the 3 o'clock position.

        :param x1: x coordinate value of the ellipse's center
        :param y1: y coordinate value of the ellipse's center
        :param start_angle: start angle of the pie
        :param end_angle: end angle of the pie
        :param x2: radius on x-axis of the ellipse
        :param y2: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw()
        angle_len = end_angle - start_angle
        rect = _calc_rect(x1, y1, x2, y2, self._ellipse_mode)
        s = start_angle * 16
        al = angle_len * 16
        p.drawPie(rect, s, al)
        self._mask_painter.drawPie(rect, s, al)
        self._updated()

    def fill_pie(self, x1: float, y1: float, start_angle: float, end_angle: float, x2: float, y2: float):
        """
        Fill an elliptical pie from start_angle to end_angle. The base ellipse is centered at (x,y)
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        The pie doesn\'t have outline.

          Note: Positive values for the angles mean counter-clockwise
          while negative values mean the clockwise direction. Zero degrees is at the 3 o'clock position.

        :param x1: x coordinate value of the ellipse's center
        :param y1: y coordinate value of the ellipse's center
        :param start_angle: start angle of the pie
        :param end_angle: end angle of the pie
        :param x2: radius on x-axis of the ellipse
        :param y2: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_fill()
        angle_len = end_angle - start_angle
        rect = _calc_rect(x1, y1, x2, y2, self._ellipse_mode)
        s = start_angle * 16
        al = angle_len * 16
        p.drawPie(rect, s, al)
        self._mask_painter.drawPie(rect, s, al)
        self._updated()

    def chord(self, x1: float, y1: float, start_angle: float, end_angle: float, x2: float, y2: float):
        """
        Draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        The chord is not filled.

          Note: Positive values for the angles mean counter-clockwise
          while negative values mean the clockwise direction. Zero degrees is at the 3 o'clock position.

        :param x1: x coordinate value of the ellipse's center
        :param y1: y coordinate value of the ellipse's center
        :param start_angle: start angle of the chord
        :param end_angle: end angle of the chord
        :param x2: radius on x-axis of the ellipse
        :param y2: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw_outline()
        angle_len = end_angle - start_angle
        rect = _calc_rect(x1, y1, x2, y2, self._ellipse_mode)
        s = start_angle * 16
        al = angle_len * 16
        p.drawChord(rect, s, al)
        self._mask_painter.drawChord(rect, s, al)
        self._updated()

    def draw_chord(self, x1: float, y1: float, start_angle: float, end_angle: float, x2: float, y2: float):
        """
        Draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        The chord is filled and has outline

          Note: Positive values for the angles mean counter-clockwise
          while negative values mean the clockwise direction. Zero degrees is at the 3 o'clock position.

        :param x1: x coordinate value of the ellipse's center
        :param y1: y coordinate value of the ellipse's center
        :param start_angle: start angle of the chord
        :param end_angle: end angle of the chord
        :param x2: radius on x-axis of the ellipse
        :param y2: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_draw()
        angle_len = end_angle - start_angle
        rect = _calc_rect(x1, y1, x2, y2, self._ellipse_mode)
        s = start_angle * 16
        al = angle_len * 16
        p.drawChord(rect, s, al)
        self._mask_painter.drawChord(rect, s, al)
        self._updated()

    def fill_chord(self, x1: float, y1: float, start_angle: float, end_angle: float, x2: float, y2: float):
        """
        Draw an elliptical chord outline from start_angle to end_angle. The base ellipse is centered at (x,y)
        which radius on x-axis is radius_x and radius on y-axis is radius_y.

        The chord doesn\'t have outline.

          Note: Positive values for the angles mean counter-clockwise
          while negative values mean the clockwise direction. Zero degrees is at the 3 o'clock position.

        :param x1: x coordinate value of the ellipse's center
        :param y1: y coordinate value of the ellipse's center
        :param start_angle: start angle of the chord
        :param end_angle: end angle of the chord
        :param x2: radius on x-axis of the ellipse
        :param y2: radius on y-axis of the ellipse
        """
        p = self._prepare_painter_for_fill()
        angle_len = end_angle - start_angle
        rect = _calc_rect(x1, y1, x2, y2, self._ellipse_mode)
        s = start_angle * 16
        al = angle_len * 16
        p.drawChord(rect, s, al)
        self._mask_painter.drawChord(rect, s, al)
        self._updated()

    def draw_bezier(self, x0: float, y0: float, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
        """
        Draw a cubic bezier curve.

        points (x0,y0),(x1,y1),(x2,y2),(x3,y3) are the control points of the curve,

        :param x0: x coordinate of the first control point
        :param y0: y coordinate of the first control point
        :param x1: x coordinate of the second control point
        :param y1: y coordinate of the second control point
        :param x2: x coordinate of the third control point
        :param y2: y coordinate of the third control point
        :param x3: x coordinate of the fourth control point
        :param y3: y coordinate of the fourth control point
        """
        path = QtGui.QPainterPath(QtCore.QPointF(x0, y0))
        path.cubicTo(x1, y1, x2, y2, x3, y3)
        p = self._prepare_painter_for_draw_outline()
        p.drawPath(path)
        self._mask_painter.drawPath(path)
        self._updated()

    bezier = draw_bezier

    def draw_curve(self, *points):
        """
        Draw a Catmull-Rom spline.

        :param points: control points
        """
        if len(points) < 8:
            raise RuntimeError("must have at least 4 control points to draw Catmull-Rom curve!")
        for i in range(7, len(points), 2):
            x0, y0 = points[i - 5], points[i - 4]
            x1 = -points[i - 7] / 6 + points[i - 5] + points[i - 3] / 6
            y1 = -points[i - 6] / 6 + points[i - 4] + points[i - 2] / 6
            x2 = points[i - 5] / 6 + points[i - 3] - points[i - 1] / 6
            y2 = points[i - 4] / 6 + points[i - 2] - points[i] / 6
            x3, y3 = points[i - 3], points[i - 2]
            self.draw_bezier(x0, y0, x1, y1, x2, y2, x3, y3)

    curve = draw_curve

    def draw_quadratic(self, x0, y0, x1, y1, x2, y2):
        """
        Draw a quadratic bezier curve.

        points (x0,y0),(x1,y1),(x2,y2) are the control points of the curve,

        :param x0: x coordinate of the first control point
        :param y0: y coordinate of the first control point
        :param x1: x coordinate of the second control point
        :param y1: y coordinate of the second control point
        :param x2: x coordinate of the third control point
        :param y2: y coordinate of the third control point
        """
        path = QtGui.QPainterPath(QtCore.QPointF(x0, y0))
        path.quadTo(x1, y1, x2, y2)
        p = self._prepare_painter_for_draw_outline()
        p.drawPath(path)
        self._mask_painter.drawPath(path)
        self._updated()

    quadratic = draw_quadratic

    def draw_lines(self, *points):
        """
        Draw lines.

        "points" is a 2D point pair list. It should contain even number of points, and each 2 points
        make a point pair. And each point have 2 coordinate values(x,y). So if you have n point pairs,
        the points list should have 4*n values.

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
        p = self._prepare_painter_for_draw_outline()
        p.drawLines(qlines)
        self._mask_painter.drawLines(qlines)
        self._updated()

    lines = draw_lines

    def draw_poly_line(self, *end_points):
        """
        Draw a poly line.

        "end_points" is a 2D points list. Each 2 values in the list make a point.
        A poly line will be drawn to connect adjacent end_points defined by the the list.

        For examples , if "end_points" is [50,50,550,350, 50,150,550,450, 50,250,550,550], draw_poly_line()
        will draw 5 lines: (50,50) to (550,350), (550,350) to (50,150), (50,150) to (550,450),
        (550,540) to (50,250) and(50,250) to (550,550).

        :param end_points: point value list
        """
        qpoints = self._convert_to_qpoints(end_points)
        p = self._prepare_painter_for_draw_outline()
        p.drawPolyline(*qpoints)
        self._mask_painter.drawPolyline(*qpoints)
        self._updated()

    poly_line = draw_poly_line

    @staticmethod
    def _convert_to_qpoints(points):
        """
        Convert point list to QPoint list
        :param points:
        :return:
        """
        numpoints = len(points) // 2
        if numpoints < 2:
            raise ValueError
        qpoints = []
        for i in range(numpoints):
            qpoints.append(QtCore.QPointF(points[i * 2], points[i * 2 + 1]))
        return qpoints

    def polygon(self, *vertices):
        """
        Draw polygon outline.

        "vertices" is a 2D point list. Each 2 values in the list make a point. A polygon will be drawn
        to connect adjacent points defined by the the list.

        For examples , if "vertices" is [50,50,550,350, 50,150], polygon() will draw a triangle with
        vertices at (50,50) , (550,350) and (50,150).

        The polygon is not filled.

        :param vertices: point value list
        """
        polygon = self._convert_to_qpolygon(vertices)
        p = self._prepare_painter_for_draw_outline()
        p.drawPolygon(polygon, self._fill_rule)
        self._mask_painter.drawPolygon(polygon, self._fill_rule)
        self._updated()

    def draw_polygon(self, *vertices):
        """
        Draw a polygon.

        "vertices" is a 2D point list. Each 2 values in the list make a point. A polygon will be drawn to
        connect adjacent points defined by the the list.

        For examples , if "vertices" is [50,50,550,350, 50,150], draw_polygon() will draw a triangle with
        vertices at (50,50) , (550,350) and (50,150)

        The polygon is filled and has outline.

        :param vertices: point value list
        """
        polygon = self._convert_to_qpolygon(vertices)
        p = self._prepare_painter_for_draw()
        p.drawPolygon(polygon, self._fill_rule)
        self._mask_painter.drawPolygon(polygon, self._fill_rule)
        self._updated()

    def _convert_to_qpolygon(self, vertices):
        qpoints = self._convert_to_qpoints(vertices)
        polygon = QtGui.QPolygonF(qpoints)
        return polygon

    def fill_polygon(self, *vertices):
        """
        Fill a polygon.

        "vertices" is a 2D point list. Each 2 values in the list make a point. A polygon will be drawn to
        connect adjacent points defined by the the list.

        For examples , if "vertices" is [50,50,550,350, 50,150], fill_polygon() will fill a triangle
        with vertices at (50,50) , (550,350) and (50,150).

        The polygon doesn\'t have outline.

        :param vertices: point value list
        """
        polygon = self._convert_to_qpolygon(vertices)
        p = self._prepare_painter_for_fill()
        p.drawPolygon(polygon, self._fill_rule)
        self._mask_painter.drawPolygon(polygon, self._fill_rule)
        self._updated()

    def path(self, path: QtGui.QPainterPath):
        """
        Draw a path.

        :param path: path to be drawn
        """
        p = self._prepare_painter_for_draw_outline()
        p.drawPath(path)
        self._mask_painter.drawPath(path)
        self._updated()

    def draw_path(self, path: QtGui.QPainterPath):
        """
        Draw and fill a path.

        :param path: path to drawn and fill
        """
        p = self._prepare_painter_for_draw()
        p.drawPath(path)
        self._mask_painter.drawPath(path)
        self._updated()

    def fill_path(self, path: QtGui.QPainterPath):
        """
        Fill the region enclosed by the path

        :param path: the path enclosing the region
        """
        p = self._painter
        self._prepare_painter_for_fill()
        p.fillPath(path, p.brush())
        self._mask_painter.fillPath(path, self._mask_painter.brush())
        self._updated()

    def _draw_rect(self, p, x1, y1, x2, y2):
        rect = _calc_rect(x1, y1, x2, y2, self._rect_mode)
        p.drawRect(rect)
        self._mask_painter.drawRect(rect)

    def rect(self, x1: float, y1: float, x2: float, y2: float):
        """
        Draws a rectangle outline with upper left corner at (left, top) and lower right corner at (right,bottom).

        The rectangle is not filled.

        :param x1: x coordinate value of the upper left corner
        :param y1: y coordinate value of the upper left corner
        :param x2: x coordinate value of the lower right corner
        :param y2: y coordinate value of the lower right corner
        """
        p = self._prepare_painter_for_draw_outline()
        self._draw_rect(p, x1, y1, x2, y2)
        self._updated()

    def draw_rect(self, x1: float, y1: float, x2: float, y2: float):
        """
        Draws a rectangle with upper left corner at (left, top) and lower right corner at (right,bottom).

        The rectangle is filled and has outline.

        :param x1: x coordinate value of the upper left corner
        :param y1: y coordinate value of the upper left corner
        :param x2: x coordinate value of the lower right corner
        :param y2: y coordinate value of the lower right corner
        """
        p = self._prepare_painter_for_draw()
        self._draw_rect(p, x1, y1, x2, y2)
        self._updated()

    def fill_rect(self, x1: float, y1: float, x2: float, y2: float):
        """
        Draws a rectangle with upper left corner at (left, top) and lower right corner at (right,bottom).

        The rectangle doesn't have outline.

        :param x1: x coordinate value of the upper left corner
        :param y1: y coordinate value of the upper left corner
        :param x2: x coordinate value of the lower right corner
        :param y2: y coordinate value of the lower right corner
        """
        p = self._prepare_painter_for_fill()
        self._draw_rect(p, x1, y1, x2, y2)
        self._updated()

    def _draw_rounded_rect(self, p, x1, y1, x2, y2, round_x, round_y):
        rect = _calc_rect(x1, y1, x2, y2, self._rect_mode)
        p.drawRoundedRect(rect, round_x, round_y)
        self._mask_painter.drawRoundedRect(rect, round_x, round_y)

    def rounded_rect(self, x1: float, y1: float, x2: float, y2: float, round_x: float, round_y: float):
        """
        Draws a rounded rectangle outline with upper left corner at (left, top) , lower right
        corner at (right,bottom). Raidus on x-axis of the corner ellipse arc is round_x,
        radius on y-axis of the corner ellipse arc is round_y.

        The rectangle is not filled.

        :param x1: x coordinate value of the upper left corner
        :param y1: y coordinate value of the upper left corner
        :param x2: x coordinate value of the lower right corner
        :param y2: y coordinate value of the lower right corner
        :param round_x: raidus on x-axis of the corner ellipse arc
        :param round_y: radius on y-axis of the corner ellipse arc
        """
        p = self._prepare_painter_for_draw_outline()
        self._draw_rounded_rect(p, x1, y1, x2, y2, round_x, round_y)
        self._updated()

    def draw_rounded_rect(self, x1: float, y1: float, x2: float, y2: float, round_x: float, round_y: float):
        """
        Draws a rounded rectangle with upper left corner at (left, top) , lower right corner at (right,bottom).
        raidus on x-axis of the corner ellipse arc is round_x, radius on y-axis of the corner ellipse arc is round_y.

        The rectangle is filled and has outline.

        :param x1: x coordinate value of the upper left corner
        :param y1: y coordinate value of the upper left corner
        :param x2: x coordinate value of the lower right corner
        :param y2: y coordinate value of the lower right corner
        :param round_x: raidus on x-axis of the corner ellipse arc
        :param round_y: radius on y-axis of the corner ellipse arc
        """
        p = self._prepare_painter_for_draw()
        self._draw_rounded_rect(p, x1, y1, x2, y2, round_x, round_y)
        self._updated()

    def fill_rounded_rect(self, x1: float, y1: float, x2: float, y2: float, round_x: float, round_y: float):
        """
        Fill a rounded rectangle with upper left corner at (left, top) , lower right corner at (right,bottom).
        raidus on x-axis of the corner ellipse arc is round_x, radius on y-axis of the corner ellipse arc is round_y.

        The rectangle doesn't have outline.

        :param x1: x coordinate value of the upper left corner
        :param y1: y coordinate value of the upper left corner
        :param x2: x coordinate value of the lower right corner
        :param y2: y coordinate value of the lower right corner
        :param round_x: radius on x-axis of the corner ellipse arc
        :param round_y: radius on y-axis of the corner ellipse arc
        """
        p = self._prepare_painter_for_fill()
        self._draw_rounded_rect(p, x1, y1, x2, y2, round_x, round_y)
        self._updated()

    def clear(self):
        """
        Clear the image to show the background.
        """
        self._image.fill(self._background_color)
        self._mask.fill(MASK_WHITE)
        self._updated()

    def fill_image(self, color):
        """
        Fill the whole image with the specified color.

        :param color: the fill color
        """
        self.save_settings()
        self.reset_transform()
        self.set_rect_mode(ShapeMode.CORNER)
        self.set_fill_color(color)
        self.fill_rect(-1, -1, self.get_width() + 2, self.get_height() + 2)
        self.restore_settings()

    def draw_image(self, x: int, y: int, image: "Image", width:int=0, height:int=0, src_x: int = 0, src_y: int = 0, src_width: int = 0,
                   src_height: int = 0, with_background=True, composition_mode=None):
        """
        Copy part of the source image (src_image) to the destination image (dst_image).

        (x, y) specifies the top-left point in the destination image that is to be drawn onto.

        (width, height) specifies the size of drawing part on the destination image.The default is (0, 0).

        (src_x, src_y) specifies the top-left point of the part in the source image that is to
        be drawn. The default is (0, 0).

        (src_width, src_height) specifies the size of the part of the source image that is to be drawn.
        The default, (0, 0) (and negative) means all the way to the bottom-right of the image.

        if with_background is False, the source image's background will not be copied.

        The final result will depend on the composition mode and the source image's background.
        In the default mode (CompositionMode.SOURCE_OVER), the transparent background in the source
        will not overwrite the destination.


        :param x: x coordinate value of the upper left point on the destination image
        :param y: y coordinate value of the upper left point on the destination image
        :param image: the source image to be copied
        :param width: width of the drawing part on the destination image
        :param height: height of the drawing part on the destination image
        :param src_x: x coordinate value of the top-left point of of the part to be drawn
        :param src_y: y coordinate value of the top-left point of of the part to be drawn
        :param src_width: witdh of the top-left point of of the part to be drawn
        :param src_height: height of the top-left point of of the part to be drawn
        :param with_background: if the background should be copied.
        :param composition_mode: if is None, use dst image's composition mode to copy.
        """
        p = self._painter
        old_mode = CompositionMode.SOURCE_OVER
        if composition_mode is not None:
            old_mode = p.compositionMode()
            p.setCompositionMode(composition_mode)
        img = _prepare_image_for_copy(image, with_background)
        if width<1 or height<1:
            p.drawImage(x, y, img, src_x, src_y, src_width, src_height)
            self._mask_painter.fillRect(x, y, src_width, src_height, QtCore.Qt.color0)
        else:
            if src_width<1:
                src_width = img.width() - x
            if src_height<1:
                src_height = img.height() - y
            target = QtCore.QRectF(x,y,width,height)
            source = QtCore.QRectF(src_x,src_y,src_width,src_height)
            p.drawImage(target,img,source)
            self._mask_painter.fillRect(x, y, width, height, QtCore.Qt.color0)
        if composition_mode is not None:
            p.setCompositionMode(old_mode)
        self._updated()

    def get_mask(self) -> QtGui.QImage:
        """
        Get background mask image.

        :return: background mask
        """
        return self._mask

    def draw_to_device(self, device: QtGui.QPaintDevice):
        """
        Draw the whole image to the specified device.

        :param device: the device to be drawn on
        """
        p = QtGui.QPainter()
        p.begin(device)
        p.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
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
        if self._fill_style == FillStyle.NULL_FILL:  # no need to fill
            return
        if self._image_view is None:
            self._image_view = qn.raw_view(self._image)
        queue = deque()
        transform = self._painter.combinedTransform()
        new_pos = transform.map(QtCore.QPoint(x, y))
        queue.append((new_pos.x(), new_pos.y()))
        bc = _to_qcolor(border_color).rgba()
        fc = _to_qcolor(self._fill_color).rgba()
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
            self._image_view[y, x] = fc
            self._mask_view[y, x] = MASK_BLACK.rgba()
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))
        self._updated()

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
        qcolor = _to_qcolor(color)
        self._image.setPixel(x, y, qcolor.rgba())
        self._mask.setPixel(x, y, MASK_BLACK.rgba())
        self._updated()

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
        if self._flip_y:
            transform = self._painter.transform()
            self.reflect(1, 0)
            y = -(y - self.text_height())
            p.drawText(x, y, msg)
            self._mask_painter.drawText(x, y, msg)
            self._painter.setTransform(transform)
            self._mask_painter.setTransform(transform)
        else:
            p.drawText(x, y, msg)
            self._mask_painter.drawText(x, y, msg)
        self._updated()

    def draw_rect_text(self, x: int, y: int, width: int, height: int, flags=QtCore.Qt.AlignCenter, *args, sep=' '):
        """
        Print the given texts in the specified rectangle area.

        Flags are defined as TextFlag const.

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
        if self._flip_y:
            transform = self._painter.transform()
            self.reflect(1, 0)
            y = -(y + height)
            p.drawText(x, y, width, height, flags, msg)
            self._mask_painter.drawText(x, y, width, height, flags, msg)
            self._painter.setTransform(transform)
            self._mask_painter.setTransform(transform)
        else:
            p.drawText(x, y, width, height, flags, msg)
            self._mask_painter.drawText(x, y, width, height, flags, msg)
        self._updated()

    def begin_shape(self, type=VertexType.POLY_LINE):
        """
        Begin a shape definition

        :param type: the type of the shape. See VertexType const for more information
        """
        if self._shape_path is not None:
            raise RuntimeError("a shape is drawing, end it first!")
        self._shape_vertext_type = type
        self._shape_path = QtGui.QPainterPath()
        self._shape_vertices.clear()
        self._shape_transformed_vertices.clear()
        self._is_curve_shape = False

    def curve_vertex(self, x: float, y: float):
        """
        Define a Catmull-Rom curve vertex.

        :param x: x pos of the vertex
        :param y: y pos of the vertex
        """
        if len(self._shape_vertices) == 0:
            if self._shape_vertext_type == VertexType.POLY_LINE:
                self._is_curve_shape = True
            else:
                raise RuntimeError("curve vertex must begin_shape() with VertexType.PLOY_LINE!")
        if len(self._shape_vertices) > 0 and not self._is_curve_shape:
            raise RuntimeError("curve vertex must be the first vertex call after begin_shape")
        self._shape_vertices.append(x)
        self._shape_vertices.append(y)
        transform = self.get_transform()
        point = transform.map(QtCore.QPointF(x, y))
        self._shape_transformed_vertices.append(point.x())
        self._shape_transformed_vertices.append(point.y())
        if len(self._shape_vertices) >= 8:
            x0, y0 = self._shape_transformed_vertices[-6], self._shape_transformed_vertices[-5]
            x1 = -self._shape_transformed_vertices[-8] / 6 + self._shape_transformed_vertices[-6] + self._shape_transformed_vertices[-4] / 6
            y1 = -self._shape_transformed_vertices[-7] / 6 + self._shape_transformed_vertices[-5] + self._shape_transformed_vertices[-3] / 6
            x2 = self._shape_transformed_vertices[-6] / 6 + self._shape_transformed_vertices[-4] - self._shape_transformed_vertices[-2] / 6
            y2 = self._shape_transformed_vertices[-5] / 6 + self._shape_transformed_vertices[-3] - self._shape_transformed_vertices[-1] / 6
            x3, y3 = self._shape_transformed_vertices[-4], self._shape_transformed_vertices[-3]

            if len(self._shape_vertices)==8:
                self._shape_path.moveTo(x0,y0)
            self._shape_path.cubicTo(x1,y1,x2,y2,x3,y3)

    def vertex(self, x: float, y: float):
        """
        Define a vertex.

        :param x: x pos of the vertex
        :param y: y pos of the vertex
        """
        if self._is_curve_shape:
            raise RuntimeError("no other vertex can be defined after curve vertex!")
        self._vertex(x,y)

    def _vertex(self, x: float, y: float):
        self._shape_vertices.append(x)
        self._shape_vertices.append(y)
        transform = self.get_transform()
        point = transform.map(QtCore.QPointF(x, y))
        self._shape_transformed_vertices.append(point.x())
        self._shape_transformed_vertices.append(point.y())
        if self._shape_vertext_type == VertexType.POLY_LINE:
            if self._shape_path.elementCount() > 0:
                self._shape_path.lineTo(point.x(), point.y())
            else:
                self._shape_path.moveTo(point.x(), point.y())
        elif self._shape_vertext_type == VertexType.POINTS:
            self.draw_point(x, y)
        elif self._shape_vertext_type == VertexType.LINES:
            if len(self._shape_vertices) % 4 == 0:
                self.push_transform()
                self.reset_transform()
                self.draw_line(self._shape_transformed_vertices[-4], self._shape_transformed_vertices[-3],
                               self._shape_transformed_vertices[-2], self._shape_transformed_vertices[-1])
                self.pop_transform()
        elif self._shape_vertext_type == VertexType.TRIANGLES:
            if len(self._shape_vertices) % 6 == 0:
                self.push_transform()
                self.reset_transform()
                self.draw_polygon(self._shape_transformed_vertices[-6], self._shape_transformed_vertices[-5],
                                  self._shape_transformed_vertices[-4], self._shape_transformed_vertices[-3],
                                  self._shape_transformed_vertices[-2], self._shape_transformed_vertices[-1])
                self.pop_transform()
        elif self._shape_vertext_type == VertexType.TRIANGLE_STRIP:
            if len(self._shape_vertices) >= 6:
                self.push_transform()
                self.reset_transform()
                self.draw_polygon(self._shape_transformed_vertices[-6], self._shape_transformed_vertices[-5],
                                  self._shape_transformed_vertices[-4], self._shape_transformed_vertices[-3],
                                  self._shape_transformed_vertices[-2], self._shape_transformed_vertices[-1])
                self.pop_transform()
        elif self._shape_vertext_type == VertexType.TRIANGLE_FAN:
            if len(self._shape_vertices) >= 6:
                self.push_transform()
                self.reset_transform()
                self.draw_polygon(self._shape_transformed_vertices[0], self._shape_transformed_vertices[1],
                                  self._shape_transformed_vertices[-4], self._shape_transformed_vertices[-3],
                                  self._shape_transformed_vertices[-2], self._shape_transformed_vertices[-1])
                self.pop_transform()
        elif self._shape_vertext_type == VertexType.QUADS:
            n = len(self._shape_vertices)
            if n % 8 == 0:
                self.push_transform()
                self.reset_transform()
                self.draw_polygon(self._shape_transformed_vertices[-8], self._shape_transformed_vertices[-7],
                                  self._shape_transformed_vertices[-6], self._shape_transformed_vertices[-5],
                                  self._shape_transformed_vertices[-4], self._shape_transformed_vertices[-3],
                                  self._shape_transformed_vertices[-2], self._shape_transformed_vertices[-1])
                self.pop_transform()
        elif self._shape_vertext_type == VertexType.QUAD_STRIP:
            n = len(self._shape_vertices)
            if n >= 8 and n % 4 == 0:
                self.push_transform()
                self.reset_transform()
                self.draw_polygon(self._shape_transformed_vertices[-8], self._shape_transformed_vertices[-7],
                                  self._shape_transformed_vertices[-6], self._shape_transformed_vertices[-5],
                                  self._shape_transformed_vertices[-2], self._shape_transformed_vertices[-1],
                                  self._shape_transformed_vertices[-4], self._shape_transformed_vertices[-3])
                self.pop_transform()

    def bezier_vertex(self, x1, y1, x2, y2, x3, y3):
        """
        Define a cubic Bezier curve. The first control point of the curve the vertex defined last time.

        :param x1: x pos of the second control point
        :param y1: y pos of the second control point
        :param x2: x pos of the third control point
        :param y2: y pos of the third control point
        :param x3: x pos of the fourth control point
        :param y3: y pos of the fourth control point
        """
        if self._is_curve_shape:
            raise RuntimeError("no other vertex can be defined after curve vertex!")
        if self._shape_path.elementCount() <= 0:
            raise RuntimeError("Must call vertex() to set the start point before define bezier curve!")
        if self._shape_vertext_type != VertexType.POLY_LINE:
            raise RuntimeError("berzier_vertex() can only used with VertexType.POLY_LINE vertices!")
        transform = self.get_transform()
        p1 = transform.map(QtCore.QPointF(x1, y1))
        p2 = transform.map(QtCore.QPointF(x2, y2))
        p3 = transform.map(QtCore.QPointF(x3, y3))
        self._shape_path.cubicTo(p1.x(), p1.y(), p2.x(), p2.y(), p3.x(), p3.y())

    def quadratic_vertex(self, x1, y1, x2, y2):
        """
        Define a quadratic Bezier curve vertex. The first control point of the curve the vertex defined last time.

        :param x1: x pos of the second control point
        :param y1: y pos of the second control point
        :param x2: x pos of the third control point
        :param y2: y pos of the third control point
        """
        if self._is_curve_shape:
            raise RuntimeError("no other vertex can be defined after cuver vertex!")
        if self._shape_path.elementCount() <= 0:
            raise RuntimeError("Must call vertex() to set the start point before define bezier curve!")
        if self._shape_vertext_type != VertexType.POLY_LINE:
            raise RuntimeError("quadratic_vertex() can only used with VertexType.POLY_LINE vertices!")
        transform = self.get_transform()
        p1 = transform.map(QtCore.QPointF(x1, y1))
        p2 = transform.map(QtCore.QPointF(x2, y2))
        self._shape_path.quadTo(p1.x(), p1.y(), p2.x(), p2.y())

    def end_shape(self, close=False):
        """
        End a shape definition

        :param close: if the shape should be closed. Only polylines can be closed.
        """
        if self._shape_vertext_type == VertexType.POLY_LINE:
            if close:
                self._vertex(self._shape_vertices[0], self._shape_vertices[1])
                self.push_transform()
                self.reset_transform()
                self.draw_path(self._shape_path)
                self.pop_transform()
            else:
                self.push_transform()
                self.reset_transform()
                self.path(self._shape_path)
                self.pop_transform()
        elif close:
            raise RuntimeError("Only VertexType.POLY_LINE vertices can close!")
        self._shape_path = None
        self._shape_vertices.clear()
        self._shape_transformed_vertices.clear()

    def set_font(self, font: QtGui.QFont):
        """
        Set font of the specified image.

        :param font: the font will be used
        """
        self._painter.setFont(font)
        self._mask_painter.setFont(font)

    def get_font(self) -> QtGui.QFont:
        """
        Get font of the specified image.

        :return: the font used by the specified image
        """
        return self._painter.font()

    def set_font_size(self, size: int):
        """
        Set font size of the specified image.

        :param size: font size of the specified image
        """
        font = self._painter.font()
        font.setPixelSize(size)
        self._painter.setFont(font)
        self._mask_painter.setFont(font)

    def get_font_size(self) -> int:
        """
        Get font size of the specified image.

        :return: font size of the specified image
        """
        return self._painter.font().pixelSize()

    def text_width(self, text: str) -> int:
        """
        Return width of the text.

        :param text: the text
        :return: width of the text
        """
        return self._painter.fontMetrics().width(text)

    def text_height(self) -> int:
        """
        Return height of the text (font height).

        :return: height of the text (font height)
        """
        return self._painter.fontMetrics().height()

    def close(self):
        """
        Close and clean up the specified image.

        :param image: the image to be closed
        """
        if self._painter is not None and self._painter.isActive():
            self._painter.end()
        self._painter = None
        if self._mask_painter is not None and self._mask_painter.isActive():
            self._mask_painter.end()
        self._mask_painter = None
        self._updated_listeners.clear()

    def get_painter(self) -> QtGui.QPainter:
        """
        Get the QPainter instance for drawing the image.

        :return: the painter used internally
        """
        return self._painter

    def get_mask_painter(self) -> QtGui.QPainter:
        """
        Get the QPainter instance for drawing the mask.

        :return: the mask painter used internally
        """
        return self._mask_painter

    def save_settings(self):
        """
        Save current drawing settings.

        See restore_settings().

        Note: current position won't  be saved and restored.

        """
        self._painter.save()
        self._mask_painter.save()
        self._old_flip_y = self._flip_y
        self._old_rect_mode = self._rect_mode
        self._old_ellipse_mode = self._ellipse_mode
        self._old_color = self._color
        self._old_line_style = self._line_style
        self._old_line_width = self._line_width
        self._old_fill_color = self._fill_color
        self._old_fill_style = self._fill_style
        self._old_fill_rule = self._fill_rule
        self._old_background_color = self._background_color

    def restore_settings(self):
        """
        Restore previously saved drawing settings.

        See save_settings().

        Note: current position won't  be saved and restored.
        """
        self._painter.restore()
        self._mask_painter.restore()
        self._flip_y = self._old_flip_y
        self._rect_mode = self._old_rect_mode
        self._ellipse_mode = self._old_ellipse_mode
        self._color = self._old_color
        self._line_style = self._old_line_style
        self._line_width = self._old_line_width
        self._fill_color = self._old_fill_color
        self._fill_style = self._old_fill_style
        self._fill_rule = self._old_fill_rule
        self._background_color = self._old_background_color

    def save(self, filename: str, with_background=True):
        """
        Save image to file.

        Set with_background to False to get a transparent background image.

        Note that JPEG format doesn\'t support transparent. Use PNG format if you want a transparent background.
        
        :param filename: path of the file
        :param with_background: True to save the background together. False not
        """
        img = _prepare_image_for_copy(self, with_background)
        img.save(filename)

    def to_bytes(self, with_background=True, format: str = "PNG") -> bytes:
        """
        Convert the image to the specified format (i.e. PNG format) bytes.

        :param with_background:  True to save the background together. False not
        :param format: format of the bytes content
        :return: bytes in the specified format
        """
        ba = QtCore.QByteArray()
        buffer = QtCore.QBuffer(ba)
        buffer.open(QtCore.QIODevice.ReadWrite)
        img = _prepare_image_for_copy(self, with_background)
        img.save(buffer, "PNG")
        buffer.close()
        return ba.data()

    def copy(self,x:int,y:int,width:int,height:int) -> "Image":
        """
        Create an copy of the image.

        :param x: left-top of the copied area
        :param y: left-top of the copied area
        :param width: width of the copy area
        :param height:  height of the copy area
        :return: new copy
        """
        new_image = self._image.copy(x,y,width,height)
        return Image(new_image)

    def scaled(self,width:int,height:int) -> "Image":
        """
        Create a scaled copy with the specified width and height.
        :param width: width of the copy
        :param height:  height of the copy
        :return: new copy
        """
        new_image =  self._image.scaled(width,height,QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        return Image(new_image)

    def set_rect_mode(self, mode):
        self._rect_mode = mode

    def get_rect_mode(self):
        return self._rect_mode

    def set_ellipse_mode(self, mode):
        self._ellipse_mode = mode

    def get_ellipse_mode(self):
        return self._ellipse_mode

    def _updated(self):
        for listener in self._updated_listeners:
            listener()

    def add_updated_listener(self, listener: Callable[[], None]):
        """
        Add a listener for updated event.

        :param listener: the listener to add
        """
        self._updated_listeners.append(listener)

    def remove_updated_listener(self, listener: Callable[[], None]):
        """
        Remove a updated event listener.

        :param listener: the listener to remove
        """
        try:
            self._updated_listeners.remove(listener)
        except ValueError:
            pass

    if _in_ipython:
        def display_in_ipython(self):
            image = self.to_bytes(True)
            IPython.display.display(IPython.display.Image(image))

    def __del__(self):
        self.close()

    @staticmethod
    def create(width: int, height: int) -> "Image":
        """
        Create a new image.

        :param width: width of the new image
        :param height: height of the new image
        :return: the created image
        """
        qimage = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32_Premultiplied)
        qimage.fill(Color.WHITE)
        image = Image(qimage)
        return image

    @staticmethod
    def create_from_file(filename: str) -> "Image":
        """
        Load a image from the file.

        :param filename: the image file
        :return: the loaded image
        """
        p = Path(filename)
        if not p.exists():
            raise ValueError(f"File {filename} not exists.")
        image = QtGui.QImage(filename)
        return Image(image)


def _calc_rect(x1: float, y1: float, x2: float, y2: float, mode) -> QtCore.QRectF:
    if mode == ShapeMode.RADIUS:
        p1 = QtCore.QPointF(x1 - x2, y1 - y2)
        p2 = QtCore.QPointF(x1 + x2, y1 + y2)
        rect = QtCore.QRectF(p1, p2)
    elif mode == ShapeMode.CENTER:
        p1 = QtCore.QPointF(x1 - x2 / 2, y1 - y2 / 2)
        p2 = QtCore.QPointF(x1 + x2 / 2, y1 + y2 / 2)
        rect = QtCore.QRectF(p1, p2)
    elif mode == ShapeMode.CORNER:
        rect = QtCore.QRectF(x1, y1, x2, y2)
    else:
        p1 = QtCore.QPointF(x1, y1)
        p2 = QtCore.QPointF(x2, y2)
        rect = QtCore.QRectF(p1, p2)
    return rect


def _to_qcolor(val: Union[int, str, QtGui.QColor]) -> Union[QtGui.QColor, int]:
    if isinstance(val, type(QtGui.QColor)):
        color = val
    else:
        color = QtGui.QColor(val)
    return color


def _prepare_image_for_copy(image: Image, with_background: bool) -> QtGui.QImage:
    img = image.get_image()
    if not with_background:
        img = _get_foreground(image)
    return img


def _get_foreground(image):
    img = QtGui.QImage(image.get_width(), image.get_height(), QtGui.QImage.Format_ARGB32_Premultiplied)
    img.fill(Color.TRANSPARENT)
    painter = QtGui.QPainter()
    painter.begin(img)
    mask = QtGui.QBitmap.fromImage(image.get_mask().createMaskFromColor(MASK_WHITE.rgba()))
    region = QtGui.QRegion(mask)
    painter.setClipRegion(region)
    painter.drawImage(0, 0, image.get_image())
    painter.end()
    return img


MASK_WHITE = _to_qcolor(Color.WHITE)
MASK_BLACK = _to_qcolor(Color.BLACK)
