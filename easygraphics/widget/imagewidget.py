from easygraphics.image import Image
from PyQt5 import QtCore, QtWidgets, QtGui

__all__ = ['ImageWidget']


class ImageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._image = None

    def setImage(self, image: Image):
        """
        Set the widget's underlying Image object.

        :param image: the underlying image object
        """
        self._image = image
        image.add_updated_listener(self.update)
        self.setFixedWidth(image.get_width())
        self.setFixedHeight(image.get_height())

    def getImage(self) -> Image:
        """
        Get the underlying image object.

        :return: the underlying image object
        """
        return self._image

    def paintEvent(self, e: QtGui.QPaintEvent):
        self._image.draw_to_device(self)
