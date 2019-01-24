from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from easygraphics.processing import *
import random


class MyProcessingWidget(ProcessingWidget):
    def __init__(self):
        self._t = 0
        super().__init__()

    def setup(self):
        self.set_size(200, 150)
        self.get_canvas().translate(0, 0)

    def draw(self):
        self._t = self._t + 2
        self.get_canvas().ellipse(self._t, self._t, 20, 20)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        imageWidget = MyProcessingWidget()
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
        pass


if __name__ == "__main__":
    app = QApplication([])
    random.seed()
    window = MyWindow()
    window.show()

    app.exec()
