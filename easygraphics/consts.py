from PyQt5 import QtGui, QtCore


class RenderMode:
    """
    These are the graphics window render mode.
    """
    RENDER_AUTO = 0
    """The graphics window is updated after each drawn."""
    RENDER_MANUAL = 1
    """The graphics window only updated after functions that wait or delay."""


class CompositionMode:
    """
    Defines the modes supported for digital image compositing.

    Composition modes are used to specify how the pixels in one image, the source, are merged \
    with the pixel in another image, the destination.

    Please note that the bitwise operation modes are not supported for pens and brushes with alpha components.

    """
    SOURCE = QtGui.QPainter.CompositionMode_Source
    """(Alpha Composition) The output is the source pixel."""
    SOURCE_OVER = QtGui.QPainter.CompositionMode_SourceOver
    """(Alpha Composition) This is the default mode. The alpha of the source is used to blend the pixel on top of the destination."""
    DESTINATION_OVER = QtGui.QPainter.CompositionMode_DestinationOver
    """(Alpha Composition) The alpha of the destination is used to blend it on top of the source pixels."""
    CLEAR = QtGui.QPainter.CompositionMode_Clear
    """(Alpha Composition) The pixels in the destination are cleared (set to fully transparent) independent of the source."""
    DESTINATION = QtGui.QPainter.CompositionMode_Destination
    """(Alpha Composition) The output is the destination pixel. This means that the blending has no effect."""
    SOURCE_IN = QtGui.QPainter.CompositionMode_SourceIn
    """(Alpha Composition) The output is the source, where the alpha is reduced by that of the destination."""
    DESTINATION_IN = QtGui.QPainter.CompositionMode_DestinationIn
    """(Alpha Composition) The output is the destination, where the alpha is reduced by that of the source."""
    SOURCE_OUT = QtGui.QPainter.CompositionMode_SourceOut
    """(Alpha Composition) The output is the source, where the alpha is reduced by the inverse of destination."""
    DESTINATION_OUT = QtGui.QPainter.CompositionMode_DestinationOut
    """(Alpha Composition) The output is the destination, where the alpha is reduced by the inverse of the source."""
    SOURCE_AT_TOP = QtGui.QPainter.CompositionMode_SourceAtop
    """(Alpha Composition) The source pixel is blended on top of the destination, with the alpha of the source pixel reduced by the alpha of the destination pixel."""
    DESTINATION_AT_TOP = QtGui.QPainter.CompositionMode_DestinationAtop
    """(Alpha Composition) The destination pixel is blended on top of the source, with the alpha of the destination pixel is reduced by the alpha of the source pixel."""
    XOR = QtGui.QPainter.CompositionMode_Xor
    """(Alpha Composition) The source, whose alpha is reduced with the inverse of the destination alpha, is merged with the destination, whose alpha is reduced by the inverse of the source alpha. CompositionMode_Xor is not the same as the bitwise Xor."""
    Plus = QtGui.QPainter.CompositionMode_Plus
    """(Blend mode) Both the alpha and color of the source and destination pixels are added together."""
    MULTIPLY = QtGui.QPainter.CompositionMode_Multiply
    """(Blend mode) The output is the source color multiplied by the destination. Multiplying a color with white leaves the color unchanged, while multiplying a color with black produces black."""
    SCREEN = QtGui.QPainter.CompositionMode_Screen
    """(Blend mode) The source and destination colors are inverted and then multiplied. Screening a color with white produces white, whereas screening a color with black leaves the color unchanged."""
    OVERLAY = QtGui.QPainter.CompositionMode_Overlay
    """(Blend mode) Multiplies or screens the colors depending on the destination color. The destination color is mixed with the source color to reflect the lightness or darkness of the destination."""
    DARKEN = QtGui.QPainter.CompositionMode_Darken
    """(Blend mode) The darker of the source and destination colors is selected."""
    LIGHTEN = QtGui.QPainter.CompositionMode_Lighten
    """(Blend mode) The lighter of the source and destination colors is selected."""
    COLOR_DODGE = QtGui.QPainter.CompositionMode_ColorDodge
    """(Blend mode) The destination color is brightened to reflect the source color. A black source color leaves the destination color unchanged."""
    COLOR_BURN = QtGui.QPainter.CompositionMode_ColorBurn
    """(Blend mode) The destination color is darkened to reflect the source color. A white source color leaves the destination color unchanged."""
    HARD_LIGHT = QtGui.QPainter.CompositionMode_HardLight
    """(Blend mode) Multiplies or screens the colors depending on the source color. A light source color will lighten the destination color, whereas a dark source color will darken the destination color."""
    SOFT_LIGHT = QtGui.QPainter.CompositionMode_SoftLight
    """(Blend mode) Darkens or lightens the colors depending on the source color. Similar to HARD_LIGHT."""
    DIFFERENCE = QtGui.QPainter.CompositionMode_Difference
    """(Blend mode) Subtracts the darker of the colors from the lighter. Painting with white inverts the destination color, whereas painting with black leaves the destination color unchanged."""
    EXCLUSION = QtGui.QPainter.CompositionMode_Exclusion
    """(Blend mode) Similar to DIFFERENCE, but with a lower contrast. Painting with white inverts the destination color, whereas painting with black leaves the destination color unchanged."""
    SRC_OR_DEST = QtGui.QPainter.RasterOp_SourceOrDestination
    """(Raster Op) Does a bitwise OR operation on the source and destination pixels (src OR dst)."""
    SRC_AND_DEST = QtGui.QPainter.RasterOp_SourceAndDestination
    """(Raster Op) Does a bitwise AND operation on the source and destination pixels (src AND dst)."""
    SRC_XOR_DEST = QtGui.QPainter.RasterOp_SourceXorDestination
    """(Raster Op) Does a bitwise XOR operation on the source and destination pixels (src XOR dst)."""
    NOT_SRC_AND_NOT_DEST = QtGui.QPainter.RasterOp_NotSourceAndNotDestination
    """(Raster Op) Does a bitwise NOR operation on the source and destination pixels ((NOT src) AND (NOT dst))."""
    NOT_SRC_OR_NOT_DEST = QtGui.QPainter.RasterOp_NotSourceOrNotDestination
    """(Raster Op) Does a bitwise NAND operation on the source and destination pixels ((NOT src) OR (NOT dst))."""
    NOT_SRC_XOR_DEST = QtGui.QPainter.RasterOp_NotSourceXorDestination
    """(Raster Op) Does a bitwise operation where the source pixels are inverted and then XOR'ed with the destination ((NOT src) XOR dst)."""
    NOT_SRC = QtGui.QPainter.RasterOp_NotSource
    """(Raster Op) Does a bitwise operation where the source pixels are inverted (NOT src)."""
    NOT_SRC_AND_DEST = QtGui.QPainter.RasterOp_NotSourceAndDestination
    """(Raster Op) Does a bitwise operation where the source is inverted and then AND'ed with the destination ((NOT src) AND dst)."""
    SRC_AND_NOT_DEST = QtGui.QPainter.RasterOp_SourceAndNotDestination
    """(Raster Op) Does a bitwise operation where the source is AND'ed with the inverted destination pixels (src AND (NOT dst))."""
    NOT_SRC_OR_DEST = QtGui.QPainter.RasterOp_NotSourceOrDestination
    """(Raster Op) Does a bitwise operation where the source is inverted and then OR'ed with the destination ((NOT src) OR dst)."""
    CLEAR_DEST = QtGui.QPainter.RasterOp_ClearDestination
    """(Raster Op) The pixels in the destination are cleared (set to 0) independent of the source."""
    SET_DEST = QtGui.QPainter.RasterOp_SetDestination
    """(Raster Op) The pixels in the destination are set (set to 1) independent of the source."""
    NOT_DEST = QtGui.QPainter.RasterOp_NotDestination
    """(Raster Op) Does a bitwise operation where the destination pixels are inverted (NOT dst)."""
    SRC_OR_NOT_DEST = QtGui.QPainter.RasterOp_SourceOrNotDestination
    """(Raster Op) Does a bitwise operation where the source is OR'ed with the inverted destination pixels (src OR (NOT dst))."""


class LineStyle:
    """
    These are the line styles that can be drawn. The styles are:

    .. list-table::

        * - |qpen-solid|
          - |qpen-dash|
          - |qpen-dot|
        * - LineStyle.SOLID_LINE
          - LineStyle.DASH_LINE
          - LineStyle.DOT_LINE
        * - |qpen-dashdot|
          - |qpen-dashdotdot|
          -
        * - LineStyle.DASH_DOT_LINE
          - LineStyle.DASH_DOT_DOT_LINE
          - LineStyle.NO_PEN

    .. |qpen-solid| image:: ../docs/images/graphics/qpen-solid.png
    .. |qpen-dash| image:: ../docs/images/graphics/qpen-dash.png
    .. |qpen-dot| image:: ../docs/images/graphics/qpen-dot.png
    .. |qpen-dashdot| image:: ../docs/images/graphics/qpen-dashdot.png
    .. |qpen-dashdotdot| image:: ../docs/images/graphics/qpen-dashdotdot.png
    """
    SOLID_LINE = QtCore.Qt.SolidLine
    """A plain line"""
    DASH_LINE = QtCore.Qt.DashLine
    """Dashes separated by a few pixels."""
    DOT_LINE = QtCore.Qt.DotLine
    """Dots separated by a few pixels."""
    DASH_DOT_LINE = QtCore.Qt.DashDotLine
    """Alternate dots and dashes."""
    DASH_DOT_DOT_LINE = QtCore.Qt.DashDotDotLine
    """One dash, two dots, one dash, two dots."""
    NO_PEN = QtCore.Qt.NoPen
    """no line at all. For example, draw_circle fills but does not draw any boundary line."""


class FillStyle:
    """
    These are the fill style used by draw and fill functions.
    """
    NULL_FILL = QtCore.Qt.NoBrush
    """Not fill at all. For example, draw_circle() will not fill."""
    SOLID_FILL = QtCore.Qt.SolidPattern
    """Fill with solid color. see set_fill_color()."""


class Color:
    """
    These are the predefined Color constants.
    """
    BLACK = QtCore.Qt.black
    """Black color"""
    DARK_GRAY = QtCore.Qt.darkGray
    """Dark Gray color"""
    LIGHT_GRAY = QtGui.QColor(0xA8, 0xA8, 0xA8)
    """Light Gray"""
    BLUE = QtCore.Qt.blue
    """Blue"""
    LIGHT_BLUE = QtGui.QColor(0x54, 0x54, 0xFC)
    """Light blue"""
    DARK_BLUE = QtCore.Qt.darkBlue
    """dark blue"""
    GREEN = QtCore.Qt.green
    """Green"""
    LIGHT_GREEN = QtGui.QColor(0x54, 0xFC, 0x54)
    """Light green"""
    DARK_GREEN = QtCore.Qt.darkGreen
    """dark green"""
    CYAN = QtCore.Qt.cyan
    """cyan"""
    LIGHT_CYAN = QtGui.QColor(0x54, 0xFC, 0xFC)
    """light cyan"""
    DARK_CYAN = QtCore.Qt.darkCyan
    """dark cyan"""
    RED = QtCore.Qt.red
    """red"""
    LIGHT_RED = QtGui.QColor(0xFC, 0x54, 0x54)
    """light red"""
    DARK_RED = QtCore.Qt.darkRed
    """dark red"""
    MAGENTA = QtGui.QColor(0xA8, 0, 0xA8)
    """magenta"""
    LIGHT_MAGENTA = QtGui.QColor(0xFC, 0x54, 0xFC)
    """light magenta"""
    DARK_MAGENTA = QtCore.Qt.darkMagenta
    """dark magenta"""
    BROWN = QtGui.QColor(0xA8, 0xA8, 0)
    """brown"""
    YELLOW = QtCore.Qt.yellow
    """yellow"""
    LIGHT_YELLOW = QtGui.QColor(0xFC, 0xFC, 0x54)
    """light yellow"""
    DARK_YELLOW = QtCore.Qt.darkYellow
    """dark yellow"""
    WHITE = QtCore.Qt.white
    """White"""
    TRANSPARENT = QtCore.Qt.transparent
    """Transparent"""


class TextFlags:
    """
    These are the text drawing flags.
    """
    ALIGN_LEFT = QtCore.Qt.AlignLeft
    """Aligns with the left edge."""
    ALIGN_RIGHT = QtCore.Qt.AlignRight
    """Aligns with the right edge."""
    ALIGN_HCENTER = QtCore.Qt.AlignHCenter
    """Centers horizontally in the available space."""
    ALIGN_JUSTIFY = QtCore.Qt.AlignJustify
    """Justifies the text in the available space."""
    ALIGN_TOP = QtCore.Qt.AlignTop
    """Aligns with the top."""
    ALIGN_BOTTOM = QtCore.Qt.AlignBottom
    """Aligns with the bottom."""
    ALIGN_VCENTER = QtCore.Qt.AlignVCenter
    """Centers vertically in the available space."""
    ALIGN_CENTER = QtCore.Qt.AlignCenter
    """Centers in both dimensions."""
    TEXT_DONT_CLIP = QtCore.Qt.TextDontClip
    """If it\'s impossible to stay within the given bounds, it prints outside."""
    TEXT_SINGLE_LINE = QtCore.Qt.TextSingleLine
    """Treats all whitespace as spaces and prints just one line."""
    TEXT_EXPAND_TABS = QtCore.Qt.TextExpandTabs
    """Makes the U+0009 (ASCII tab) character move to the next tab stop."""
    TEXT_WORD_WRAP = QtCore.Qt.TextWordWrap
    """Breaks lines at appropriate points, e.g. at word boundaries."""


class MouseMessageType:
    """
    These are the mouse message types.
    """
    NO_MESSAGE = 0
    PRESS_MESSAGE = 1
    RELEASE_MESSAGE = 2


class FillRule:
    """
    The Rule for fill polygons.
    """
    ODD_EVEN_FILL = QtCore.Qt.OddEvenFill
    """Specifies that the region is filled using the odd even fill rule. """
    WINDING_FILL = QtCore.Qt.WindingFill
    """Specifies that the region is filled using the non zero winding rule. """
