from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from easygraphics.widget import ImageWidget
from easygraphics import Image
import random


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self._image = Image.create(800, 600)
        imageWidget = ImageWidget()
        imageWidget.setImage(self._image)
        area = QScrollArea()
        area.setWidget(imageWidget)
        area.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout(self)
        layout.addWidget(area)
        button = QPushButton("Add Circle")
        button.clicked.connect(self.button_clicked)
        layout.addWidget(button)
        self.setLayout(layout)

    def button_clicked(self):
        self._image.ellipse(random.randrange(0, 800), random.randrange(0, 600), 20, 20)


if __name__ == "__main__":
    app = QApplication([])
    random.seed()
    window = MyWindow()
    window.show()

    app.exec()
