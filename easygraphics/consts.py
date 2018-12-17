from PyQt5 import QtGui, QtCore


class RenderMode:
    RENDER_AUTO = 0
    RENDER_MANUAL = 1


class WriteMode:
    R2_COPYPEN = QtGui.QPainter.CompositionMode_SourceOver
    R2_MASKNOTPEN = QtGui.QPainter.RasterOp_NotSourceAndDestination
    R2_MASKPEN = QtGui.QPainter.RasterOp_SourceAndDestination
    R2_MASKPENNOT = QtGui.QPainter.RasterOp_SourceAndNotDestination
    R2_MERGENOTPEN = QtGui.QPainter.RasterOp_NotSourceOrDestination
    R2_MERGEPEN = QtGui.QPainter.RasterOp_SourceOrDestination
    R2_MERGEPENNOT = QtGui.QPainter.RasterOp_SourceOrNotDestination
    R2_NOP = QtGui.QPainter.CompositionMode_Destination
    R2_NOT = QtGui.QPainter.RasterOp_NotDestination
    R2_NOTCOPYPEN = QtGui.QPainter.RasterOp_NotSource
    R2_NOTMASKPEN = QtGui.QPainter.RasterOp_NotSourceOrNotDestination
    R2_NOTMERGEPEN = QtGui.QPainter.RasterOp_NotSourceAndNotDestination
    R2_NOTXORPEN = QtGui.QPainter.RasterOp_NotSourceXorDestination
    R2_XORPEN = QtGui.QPainter.RasterOp_SourceXorDestination


class LineStyle:
    SOLID_LINE = QtCore.Qt.SolidLine
    CENTER_LINE = QtCore.Qt.DashLine
    DOTTED_LINE = QtCore.Qt.DotLine
    DASHED_LINE = QtCore.Qt.DashDotLine
    NULL_LINE = QtCore.Qt.NoPen
    DASH_LINE = QtCore.Qt.DashLine
    DOT_LINE = QtCore.Qt.DotLine
    DASH_DOT_LINE = QtCore.Qt.DashDotLine
    DASH_DOT_DOT_LINE = QtCore.Qt.DashDotDotLine
    NO_PEN = QtCore.Qt.NoPen


class FillStyle:
    NULL_FILL = QtCore.Qt.NoBrush
    SOLID_FILL = QtCore.Qt.SolidPattern


class Color:
    BLACK = QtCore.Qt.black
    DARKGRAY = QtCore.Qt.darkGray
    BLUE = QtCore.Qt.blue
    LIGHTBLUE = QtGui.QColor(0x54, 0x54, 0xFC)
    GREEN = QtCore.Qt.green
    LIGHTGREEN = QtGui.QColor(0x54, 0xFC, 0x54)
    CYAN = QtCore.Qt.cyan
    LIGHTCYAN = QtGui.QColor(0x54, 0xFC, 0xFC)
    RED = QtCore.Qt.red
    LIGHTRED = QtGui.QColor(0xFC, 0x54, 0x54)
    MAGENTA = QtGui.QColor(0xA8, 0, 0xA8)
    LIGHTMAGENTA = QtGui.QColor(0xFC, 0x54, 0xFC)
    BROWN = QtGui.QColor(0xA8, 0xA8, 0)
    YELLOW = QtCore.Qt.yellow
    LIGHTGRAY = QtGui.QColor(0xA8, 0xA8, 0xA8)
    WHITE = QtCore.Qt.white
    TRANSPARENT = QtCore.Qt.transparent
