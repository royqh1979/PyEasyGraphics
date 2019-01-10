from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from easygraphics.widget import TurtleWidget
from easygraphics import *
from easygraphics.turtle import *
import random


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self._turtleWidget = TurtleWidget(None, 800, 600)
        area = QScrollArea()
        area.setWidget(self._turtleWidget)
        area.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout(self)
        layout.addWidget(area)

        control_panel = QWidget()
        self.setup_panel(control_panel)
        layout.addWidget(control_panel)
        self.setLayout(layout)

    def setup_panel(self, panel):
        layout = QtWidgets.QFormLayout(panel)
        form_layout = QtWidgets.QFormLayout()
        label1 = QtWidgets.QLabel(panel)
        label1.setText("size")
        form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, label1)
        self._sb_size = QtWidgets.QSpinBox(panel)
        self._sb_size.setMinimum(0)
        self._sb_size.setMaximum(150)
        self._sb_size.setValue(100)
        form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self._sb_size)
        label2 = QtWidgets.QLabel(panel)
        label2.setText("angle")
        form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, label2)
        self._sb_angle = QtWidgets.QSpinBox(panel)
        self._sb_angle.setMinimum(0)
        self._sb_angle.setMaximum(500)
        self._sb_angle.setValue(120)
        form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self._sb_angle)
        label_3 = QtWidgets.QLabel(panel)
        label_3.setText("level")
        form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, label_3)
        self._sb_level = QtWidgets.QSpinBox(panel)
        self._sb_level.setObjectName("spinBox_3")
        self._sb_level.setMinimum(0)
        self._sb_level.setMaximum(100)
        self._sb_level.setValue(4)
        form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self._sb_level)
        layout.setLayout(0, QtWidgets.QFormLayout.FieldRole, form_layout)
        button = QtWidgets.QPushButton(panel)
        button.setText("draw")
        button.clicked.connect(self.button_clicked)
        layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, button)

    def corner_poly(self, size, angle, level):
        if level == 0:
            return
        total_turn = 0
        turtle = self._turtleWidget.getTurtle()
        while self._turtleWidget.is_run():
            turtle.fd(size)
            self.corner_poly(size / 2, -angle, level - 1)
            turtle.rt(angle)
            total_turn += angle
            if total_turn % 360 == 0:
                break

    def button_clicked(self):
        self._turtleWidget.run(self.draw)

    def draw(self):
        size = self._sb_size.value()
        angle = self._sb_angle.value()
        level = self._sb_level.value()
        world = self._turtleWidget.getWorld()
        world.clear()
        turtle = self._turtleWidget.getTurtle()
        turtle.set_speed(200)
        self.corner_poly(size, angle, level)


if __name__ == "__main__":
    app = QApplication([])
    random.seed()

    window = MyWindow()

    window.show()

    app.exec()
