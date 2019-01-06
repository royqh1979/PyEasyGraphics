from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from typing import List


class ImageDialog(QtWidgets.QDialog):
    """Dialog with the possibility of selecting one or more
       items from a list"""

    def __init__(self, image: QtGui.QImage, title: str = "Title"):
        super().__init__(None, QtCore.Qt.WindowSystemMenuHint |
                         QtCore.Qt.WindowTitleHint)
        if image is None:
            raise RuntimeError("Must provide a image to display")
        self.setWindowTitle(title)
        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.image_widget = QtWidgets.QLabel(self)
        self.image_widget.setPixmap(QtGui.QPixmap.fromImage(image))
        self.setFixedWidth(image.width())
        self.setFixedHeight(image.height())
        main_layout.addWidget(self.image_widget)

        self.setLayout(main_layout)
        self.show()
        self.raise_()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.cancel()
        elif e.key() == QtCore.Qt.Key_Enter:
            self.selection_completed()
        else:
            super().keyPressEvent(e)
