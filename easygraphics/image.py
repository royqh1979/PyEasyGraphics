from PyQt5.QtGui import *
from PyQt5.QtCore import *
from collections import deque

from easygraphics.consts import WriteMode


class Image:
    def __init__(self, image: QImage):
        self._image = image
        self._color = Qt.black
        self._line_style = Qt.SolidLine
        self._lineWidth = 1
        self._fill_color = Qt.white
        self._fill_Style = Qt.SolidPattern
        self._background_color = Qt.transparent
        self._pen = QPen()
        self._brush = QBrush(Qt.white, Qt.SolidPattern)
        self._clip = False
        self._view_port = None
        self._origin = QPointF(0, 0)
        self._write_mode = WriteMode.R2_COPYPEN
        self._x = 0
        self._y = 0
        self._font = QFont("SansSerif", 14)
        self._font_metrics = QFontMetrics(self._font)

    def get_image(self) -> QImage:
        return self._image

    def get_width(self):
        return self._image.width()

    def get_height(self):
        return self._image.height()

    def get_pen(self) -> QPen:
        return self._pen

    def set_pen(self, pen):
        self._pen = pen

    def get_brush(self) -> QBrush:
        return self._brush

    def set_brush(self, brush):
        self._brush = brush

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color
        self._pen.setColor(color)

    def get_fill_color(self):
        return self._fill_color

    def set_fill_color(self, fill_color):
        self._fill_color = fill_color
        self._brush.setColor(fill_color)

    def get_background_color(self):
        return self._background_color

    def set_background_color(self, background_color):
        self._background_color = background_color

    def get_line_style(self):
        return self._line_style

    def set_line_style(self, line_style):
        self._line_style = line_style
        self._pen.setStyle(line_style)

    def get_line_width(self):
        return self._lineWidth

    def set_line_width(self, width):
        self._lineWidth = width
        if isinstance(width, int):
            self._pen.setWidth(width)
        else:
            self._pen.setWidthF(width)

    def get_fill_style(self):
        return self._fill_Style

    def set_fill_style(self, fill_style):
        self._fill_Style = fill_style
        self._brush.setStyle(fill_style)

    def set_view_port(self, left, top, right, bottom, clip=True):
        self._view_port = QRect(left, top, right - left, bottom - top)
        self._clip = clip

    def rest_view_port(self):
        self._view_port = None
        self._clip = False

    def set_origin(self, x, y):
        self.set_view_port(x, y, 0, 0, False)

    def clear_view_port(self):
        p = QPainter()
        p.begin(self._image)
        p.fillRect(self._view_port, self._background_color)
        p.end()

    def get_view_port(self) -> QRect:
        return self._view_port

    def is_clip(self) -> bool:
        return self._clip

    def set_write_mode(self, mode):
        self._write_mode = mode

    def get_write_mode(self):
        return self._write_mode

    def move_to(self, x, y):
        self._x = x
        self._y = y

    def move_rel(self, dx, dy):
        self._x += dx
        self._y += dy

    def line_to(self, x, y):
        self.line(self._x, self._y, x, y)
        self.move_to(x, y)

    def line_rel(self, dx, dy):
        self.line(self._x, self._y, self._x + dx, self._y + dy)
        self.move_rel(dx, dy)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def _prepare_painter(self, pen: QPen, brush: QBrush) -> QPainter:
        p = QPainter()
        p.begin(self._image)
        if self._clip:
            p.setClipRect(self._view_port)
        if self._view_port is not None:
            p.translate(self._view_port.left(), self._view_port.top())
        p.setCompositionMode(self._write_mode)
        if self._font is not None:
            p.setFont(self._font)
        p.setPen(pen)
        p.setBrush(brush)
        return p

    def _prepare_painter_for_draw_outline(self) -> QPainter:
        ''' prepare painter for draw outline '''
        return self._prepare_painter(self._pen, Qt.NoBrush)

    def _prepare_painter_for_draw(self) -> QPainter:
        ''' prepare painter for draw (with outline and fill)'''
        return self._prepare_painter(self._pen, self._brush)

    def _prepare_painter_for_fill(self) -> QPainter:
        """ prepare painter for fill (without outline)"""
        return self._prepare_painter(Qt.NoPen, self._brush)

    def draw_point(self, x, y):
        p = self._prepare_painter_for_draw_outline()
        p.drawPoint(x, y)
        p.end()

    def draw_line(self, x1, y1, x2, y2):
        ''' Draw a line from (x1,y1) to (x2,y2) on image '''
        p = self._prepare_painter_for_draw_outline()
        p.drawLine(x1, y1, x2, y2)
        p.end()

    def line(self, x1, y1, x2, y2):
        ''' Draw a line from (x1,y1) to (x2,y2) on image '''
        self.draw_line(x1, y1, x2, y2)

    def ellipse(self, x, y, radius_x, radius_y):
        '''Draw a circle outline whose center is on (x,y) and radius is r '''
        p = self._prepare_painter_for_draw_outline()
        p.drawEllipse(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y)
        p.end()

    def draw_ellipse(self, x, y, radius_x, radius_y):
        '''Draw a circle whose center is on (x,y) and radius is r '''
        p = self._prepare_painter_for_draw()
        p.drawEllipse(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y)
        p.end()

    def fill_ellipse(self, x, y, radius_x, radius_y):
        p = self._prepare_painter_for_fill()
        p.drawEllipse(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y)
        p.end()

    def arc(self, x, y, start_angle, end_angle, radius_x, radius_y):
        p = self._prepare_painter_for_draw_outline()
        angle_len = end_angle - start_angle
        p.drawArc(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y, _rotate_angle(start_angle) * 16,
                  angle_len * 16)
        p.end()

    def draw_arc(self, x, y, start_angle, end_angle, radius_x, radius_y):
        self.arc(x, y, start_angle, end_angle, radius_x, radius_y)

    def pie(self, x, y, start_angle, end_angle, radius_x, radius_y):
        p = self._prepare_painter_for_draw_outline()
        angle_len = end_angle - start_angle
        p.drawPie(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y, _rotate_angle(start_angle) * 16,
                  angle_len * 16)
        p.end()

    def draw_pie(self, x, y, start_angle, end_angle, radius_x, radius_y):
        p = self._prepare_painter_for_draw()
        angle_len = end_angle - start_angle
        p.drawPie(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y, _rotate_angle(start_angle) * 16,
                  angle_len * 16)
        p.end()

    def fill_pie(self, x, y, start_angle, end_angle, radius_x, radius_y):
        p = self._prepare_painter_for_fill()
        angle_len = end_angle - start_angle
        p.drawPie(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y, _rotate_angle(start_angle) * 16,
                  angle_len * 16)
        p.end()

    def chord(self, x, y, start_angle, end_angle, radius_x, radius_y):
        p = self._prepare_painter_for_draw_outline()
        angle_len = end_angle - start_angle
        p.drawChord(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y, _rotate_angle(start_angle) * 16,
                    angle_len * 16)
        p.end()

    def draw_chord(self, x, y, start_angle, end_angle, radius_x, radius_y):
        p = self._prepare_painter_for_draw()
        angle_len = end_angle - start_angle
        p.drawChord(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y, _rotate_angle(start_angle * 16),
                    angle_len * 16)
        p.end()

    def fill_chord(self, x, y, start_angle, end_angle, radius_x, radius_y):
        p = self._prepare_painter_for_fill()
        angle_len = end_angle - start_angle
        p.drawChord(x - radius_x, y - radius_y, 2 * radius_x, 2 * radius_y, _rotate_angle(start_angle * 16),
                    angle_len * 16)
        p.end()

    def bezier(self, polypoints: list):
        self.draw_bezier(polypoints)

    def draw_bezier(self, polypoints: list):
        if len(polypoints) % 2 != 0:
            raise ValueError
        numpoints = len(polypoints) // 2
        if numpoints < 4:
            raise ValueError

        path = QPainterPath(QPointF(polypoints[0], polypoints[1]))
        for i in range(1, numpoints, 3):
            path.cubicTo(*polypoints[i * 2:i * 2 + 6])
        p = self._prepare_painter_for_draw_outline()
        p.drawPath(path)
        p.end()

    def lines(self, points: list):
        self.draw_lines(points)

    def draw_lines(self, points: list):
        numpoints = len(points) // 2
        if numpoints < 2:
            raise ValueError
        qpoints = []
        for i in range(0, numpoints, 2):
            qpoints.append(QLineF(*points[i * 2:i * 2 + 4]))
        p = self._prepare_painter_for_draw_outline()
        p.drawLines(*qpoints)
        p.end()

    def poly_line(self, points: list):
        self.draw_poly_line(points)

    def draw_poly_line(self, points: list):
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
            qpoints.append(QPointF(points[i * 2], points[i * 2 + 1]))
        return qpoints

    def polygon(self, points: list):
        qpoints = self._convert_to_qpoints(points)
        p = self._prepare_painter_for_draw_outline()
        p.drawPolygon(*qpoints)
        p.end()

    def draw_polygon(self, points: list):
        qpoints = self._convert_to_qpoints(points)
        p = self._prepare_painter_for_draw()
        p.drawPolygon(*qpoints)
        p.end()

    def fill_polygon(self, points: list):
        qpoints = self._convert_to_qpoints(points)
        p = self._prepare_painter_for_fill()
        p.drawPolygon(*qpoints)
        p.end()

    def path(self, path: QPainterPath):
        p = self._prepare_painter_for_draw_outline()
        p.drawPath(path)
        p.end()

    def draw_path(self, path: QPainterPath):
        p = self._prepare_painter_for_draw()
        p.drawPath(path)
        p.end()

    def fill_path(self, path: QPainterPath):
        p = self._prepare_painter_for_draw()
        p.drawPath(path)
        p.end()

    def rect(self, left, top, right, bottom):
        p = self._prepare_painter_for_draw_outline()
        p.drawRect(left, top, right - left, bottom - top)
        p.end()

    def draw_rect(self, left, top, right, bottom):
        p = self._prepare_painter_for_draw()
        p.drawRect(left, top, right - left, bottom - top)
        p.end()

    def fill_rect(self, left, top, right, bottom):
        p = self._prepare_painter_for_fill()
        p.drawRect(left, top, right - left, bottom - top)
        p.end()

    def rounded_rect(self, left, top, right, bottom, round_x, round_y):
        p = self._prepare_painter_for_draw_outline()
        p.drawRoundedRect(left, top, right - left, bottom - top, round_x, round_y)
        p.end()

    def draw_rounded_rect(self, left, top, right, bottom, round_x, round_y):
        p = self._prepare_painter_for_draw()
        p.drawRoundedRect(left, top, right - left, bottom - top, round_x, round_y)
        p.end()

    def fill_rounded_rect(self, left, top, right, bottom, round_x, round_y):
        p = self._prepare_painter_for_fill()
        p.drawRoundedRect(left, top, right - left, bottom - top, round_x, round_y)
        p.end()

    def clear(self):
        self._image.fill(self._background_color)

    def draw_image(self, x, y, image):
        p = QPainter()
        p.begin(self._image)
        p.setCompositionMode(self._write_mode)
        p.drawImage(x, y, image.get_image())
        p.end()

    def flood_fill(self, x, y, border_color):
        queue = deque()
        if self._view_port is not None:
            queue.append((x + self._view_port.left(), y + self._view_port.top()))
        else:
            queue.append((x, y))
        bc = QColor(border_color)
        sc = QColor(self._fill_color).rgba()
        bits = [0] * (self._image.width() * self._image.height())
        while len(queue) > 0:
            x, y = queue.popleft()
            if x < 0 or y < 0 or x >= self._image.width() or y >= self._image.height():
                continue
            if self._clip and (x < self._view_port.left()
                               or x > self._view_port.right() or y < self._view_port.top()
                               or y > self._view_port.bottom()):
                continue
            if bits[self._image.width() * y + x] == 1:
                continue
            c = self._image.pixel(x, y)
            pc = QColor(c)
            if bc == pc:
                continue
            bits[self._image.width() * y + x] = 1
            self._image.setPixel(x, y, sc)
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))

    def get_pixel(self, x, y) -> QColor:
        return QColor(self._image.pixel(x, y))

    def put_pixel(self, x, y, color):
        self._image.setPixel(x, y, color)

    def draw_text(self, x, y, *args, sep=' '):
        msgs = map(str, args)
        msg = sep.join(args)
        p = self._prepare_painter_for_draw()
        p.drawText(x, y, msg)

    def draw_rect_text(self, x, y, w, h, flags, *args, sep=' '):
        msgs = map(str, args)
        msg = sep.join(args)
        p = self._prepare_painter_for_draw()
        p.drawText(x, y, w, h, msg)

    def set_font(self, font: QFont):
        self._font = font
        self._font_metrics = QFontMetrics(self._font)

    def get_font(self) -> QFont:
        return self._font

    def set_font_size(self, size):
        self._font.setPixelSize(size)
        self._font_metrics = QFontMetrics(self._font)

    def get_font_size(self):
        return self._font.pixelSize()

    def text_width(self, str):
        self._font_metrics.width(str)

    def text_height(self, str):
        self._font_metrics.height()

def _rotate_angle(angle):
    return angle
