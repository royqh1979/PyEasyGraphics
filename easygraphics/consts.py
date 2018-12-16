from PyQt5.QtGui import *
from PyQt5.QtCore import *


class RenderMode:
    RENDER_AUTO = 0
    RENDER_MANUAL = 1


class WriteMode:
    R2_COPYPEN = QPainter.CompositionMode_SourceOver
    R2_MASKNOTPEN = QPainter.RasterOp_NotSourceAndDestination
    R2_MASKPEN = QPainter.RasterOp_SourceAndDestination
    R2_MASKPENNOT = QPainter.RasterOp_SourceAndNotDestination
    R2_MERGENOTPEN = QPainter.RasterOp_NotSourceOrDestination
    R2_MERGEPEN = QPainter.RasterOp_SourceOrDestination
    R2_MERGEPENNOT = QPainter.RasterOp_SourceOrNotDestination
    R2_NOP = QPainter.CompositionMode_Destination
    R2_NOT = QPainter.RasterOp_NotDestination
    R2_NOTCOPYPEN = QPainter.RasterOp_NotSource
    R2_NOTMASKPEN = QPainter.RasterOp_NotSourceOrNotDestination
    R2_NOTMERGEPEN = QPainter.RasterOp_NotSourceAndNotDestination
    R2_NOTXORPEN = QPainter.RasterOp_NotSourceXorDestination
    R2_XORPEN = QPainter.RasterOp_SourceXorDestination


class LineStyle:
    SOLID_LINE = Qt.SolidLine
    CENTER_LINE = Qt.DashLine
    DOTTED_LINE = Qt.DotLine
    DASHED_LINE = Qt.DashDotLine
    NULL_LINE = Qt.NoPen
    DASH_LINE = Qt.DashLine
    DOT_LINE = Qt.DotLine
    DASH_DOT_LINE = Qt.DashDotLine
    DASH_DOT_DOT_LINE = Qt.DashDotDotLine
    NO_PEN = Qt.NoPen


class FillStyle:
    NULL_FILL = Qt.NoBrush
    SOLID_FILL = Qt.SolidPattern


class Color:
    BLACK = Qt.black
    DARKGRAY = Qt.darkGray
    BLUE = Qt.blue
    LIGHTBLUE = QColor(0x54, 0x54, 0xFC)
    GREEN = Qt.green
    LIGHTGREEN = QColor(0x54, 0xFC, 0x54)
    CYAN = Qt.cyan
    LIGHTCYAN = QColor(0x54, 0xFC, 0xFC)
    RED = Qt.red
    LIGHTRED = QColor(0xFC, 0x54, 0x54)
    MAGENTA = QColor(0xA8, 0, 0xA8)
    LIGHTMAGENTA = QColor(0xFC, 0x54, 0xFC)
    BROWN = QColor(0xA8, 0xA8, 0)
    YELLOW = Qt.yellow
    LIGHTGRAY = QColor(0xA8, 0xA8, 0xA8)
    WHITE = Qt.white
    TRANSPARENT = Qt.transparent
