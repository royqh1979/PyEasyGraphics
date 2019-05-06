from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets as qt_widgets


class CalendarDialog(qt_widgets.QDialog):
    """Creates a calendar widget allowing the user to select a date."""

    def __init__(self, title="Calendar"):
        super(CalendarDialog, self).__init__()

        self.setWindowTitle(title)
        layout = qt_widgets.QGridLayout()
        layout.setColumnStretch(1, 1)

        self.cal = qt_widgets.QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.clicked[QtCore.QDate].connect(self.show_date)
        layout.addWidget(self.cal, 0, 0, 1, 2)

        self.date_label = qt_widgets.QLabel()
        self.date = self.cal.selectedDate()
        self.date_label.setText(self.date.toString())
        layout.addWidget(self.date_label, 1, 0)

        button_box = qt_widgets.QDialogButtonBox()
        confirm_button = button_box.addButton(qt_widgets.QDialogButtonBox.Ok)
        confirm_button.clicked.connect(self.confirm)
        layout.addWidget(button_box, 1, 1)

        self.setLayout(layout)

    def show_date(self, date):
        self.date = self.cal.selectedDate()
        self.date_label.setText(self.date.toString())

    def confirm(self):
        self.date = self.cal.selectedDate()
        self.close()


if __name__ == '__main__':
    app = qt_widgets.QApplication([])
    cal = CalendarDialog(title="title")
    app.exec_()
    date = cal.date.toString()
    print(date)
