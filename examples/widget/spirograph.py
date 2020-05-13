# spirograph
import math
import random
import threading

from PyQt5 import QtWidgets,QtGui,QtCore
from easygraphics import *
from easygraphics.graphwin import GraphWin
import easygraphics.dialog

Outer_Color = Color.LIGHT_BLUE
Inner_Color = Color.LIGHT_CYAN
Drawing_Point_Color = Color.LIGHT_RED

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        self._mainFrame = GraphWin(600, 600)  # drawing frame
        layout.addWidget(self._mainFrame)
        controlPane = QtWidgets.QFrame()
        controlPaneLayout = QtWidgets.QVBoxLayout()
        controlPane.setLayout(controlPaneLayout)
        layout.addWidget(controlPane)

        self._info = QtWidgets.QLabel("Graph Infos")
        controlPane.layout().addWidget(self._info)

        inputForm = QtWidgets.QFrame()
        formLayout = QtWidgets.QFormLayout()
        inputForm.setLayout(formLayout)
        self._sldOuter = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self._sldOuter.setFixedWidth(150)
        self._sldOuter.setRange(100, 300)
        self._sldOuter.setValue(300)
        self._sldOuter.setTracking(True)
        self._sldOuter.valueChanged.connect(self.on_outer_value_changed)
        formLayout.addRow("Radius of outer circle:", self._sldOuter)
        self._sldInner = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self._sldInner.setFixedWidth(150)
        self._sldInner.setRange(10, 200)
        self._sldInner.setValue(150)
        self._sldInner.valueChanged.connect(self.on_inner_value_changed)
        formLayout.addRow("Radius of inner circle:", self._sldInner)
        self._sldDistance = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self._sldDistance.setFixedWidth(150)
        self._sldDistance.setRange(8, 150)
        self._sldDistance.setValue(100)
        self._sldDistance.valueChanged.connect(self.on_distance_value_changed)
        formLayout.addRow("Distance form draw point to center", self._sldDistance)
        self._sldSpeed = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self._sldSpeed.setFixedWidth(150)
        self._sldSpeed.setRange(10, 50000)
        self._sldSpeed.setValue(100)
        self._sldSpeed.valueChanged.connect(self.on_speed_changed)
        formLayout.addRow("Drawing Speed", self._sldSpeed)
        self._speed = 100
        controlPane.layout().addWidget(inputForm)
        controlPaneLayout.addStretch()
        self._btnChangePatternColor = QtWidgets.QPushButton("change color")
        self._btnChangePatternColor.clicked.connect(self.on_change_color_clicked)
        controlPane.layout().addWidget(self._btnChangePatternColor)
        self._btnToggleStart = QtWidgets.QPushButton("start")
        self._btnToggleStart.clicked.connect(self.on_toggle_start_clicked)
        controlPane.layout().addWidget(self._btnToggleStart)
        self._btnClear = QtWidgets.QPushButton("Clear")
        self._btnClear.clicked.connect(self.on_clear_clicked)
        controlPane.layout().addWidget(self._btnClear)
        self._is_run = True
        self._pause = True
        self._outer_image = create_image(600, 600)
        self._outer_image.set_background_color(Color.TRANSPARENT)
        self._inner_image = create_image(600, 600)
        self._inner_image.set_background_color(Color.TRANSPARENT)
        self._pattern_image = create_image(600, 600)
        self._degree = 0
        self._pattern_color = Color.RED
        self.update_info()

    def on_speed_changed(self, value):
        self._speed = value

    def on_change_color_clicked(self):
        self._pattern_color = easygraphics.dialog.get_color(self._pattern_color)

    def on_clear_clicked(self):
        self._pattern_image.clear()
        self.update_images()
        self.update()

    def on_outer_value_changed(self, value):
        self._sldInner.setMaximum(value)
        self.update_outer_circle()
        self._pattern_image.clear()
        self.update_info()
        self.update()

    def update_info(self):
        self._info.setText(
            f"Outer R: {self._sldOuter.value()} Inner r: {self._sldInner.value()} distance: {self._sldDistance.value()}")

    def update_outer_circle(self):
        R = self._sldOuter.value()
        self._outer_image.clear()
        self._outer_image.set_color(Outer_Color)
        self._outer_image.ellipse(300, 300, R, R)

    def update_inner_circle(self):
        R = self._sldOuter.value()
        r = self._sldInner.value()
        distance = self._sldDistance.value()
        degree2=-self._degree*r/R
        x1=300+(R-r)*math.cos(degree2)
        y1=300+(R-r)*math.sin(degree2)
        x=distance*math.cos(self._degree)+x1
        y=distance*math.sin(self._degree)+y1
        self._inner_image.clear()
        self._inner_image.set_color(Inner_Color)
        self._inner_image.set_fill_color(Drawing_Point_Color)
        self._inner_image.ellipse(x1,y1,r,r)
        self._inner_image.line(x1,y1,x,y)
        self._inner_image.fill_ellipse(x,y,3,3)

    def update_pattern(self):
        R=self._sldOuter.value()
        r=self._sldInner.value()
        distance = self._sldDistance.value()
        degree2=-self._degree*r/R
        x1=300+(R-r)*math.cos(degree2)
        y1=300+(R-r)*math.sin(degree2)
        x=distance*math.cos(self._degree)+x1
        y=distance*math.sin(self._degree)+y1
        color = self._pattern_color
        self._pattern_image.set_fill_color(color)
        self._pattern_image.fill_ellipse(x,y,2,2)

    def on_inner_value_changed(self,value):
        self._sldDistance.setMaximum(value)
        self._pattern_image.clear()
        self.update_info()
        self.update()

    def on_distance_value_changed(self,value):
        self._pattern_image.clear()
        self.update_info()
        self.update()

    def on_toggle_start_clicked(self):
        if self._pause:
            self._pause = False
            self._btnToggleStart.setText("Pause")
        else:
            self._pause = True
            self._btnToggleStart.setText("Start")

    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        self._mainFrame.closeEvent(e)

    def update_images(self) -> None:
        self._mainFrame.get_canvas().clear()
        self._mainFrame.get_canvas().draw_image(0, 0, self._pattern_image)
        self._mainFrame.get_canvas().draw_image(0, 0, self._inner_image)
        self._mainFrame.get_canvas().draw_image(0, 0, self._outer_image)

    def run(self):
        self._mainFrame.set_immediate(False)
        self.update_outer_circle()
        self.update_inner_circle()
        self.update_images()
        while self._mainFrame.is_run():
            if not self._pause:
                if self._degree > self._sldOuter.value() * 2 * math.pi:
                    self._degree = 0
                self._degree = self._degree + 0.01
                self.update_pattern()
                if self._mainFrame.delay_jfps(self._speed):
                    self.update_inner_circle()
                    self.update_images()
            else:
                self._mainFrame.delay(30)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = MyWindow()
    win.setWindowTitle("Spirograph")
    win.show()
    thread = threading.Thread(target=win.run)
    thread.start()
    app.exec()
    thread.join()
