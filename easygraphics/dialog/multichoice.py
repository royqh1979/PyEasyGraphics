from PyQt5 import QtCore
from PyQt5 import QtWidgets
from typing import List


class MultipleChoicesDialog(QtWidgets.QDialog):
    """Dialog with the possibility of selecting one or more
       items from a list"""

    def __init__(self, choices: List[str] = None, title: str = "Title"):
        super(MultipleChoicesDialog, self).__init__(None, QtCore.Qt.WindowSystemMenuHint |
                                                    QtCore.Qt.WindowTitleHint)
        if choices is None:
            choices = ["Item %d" % i for i in range(10)]
        self.setWindowTitle(title)
        self.selection = []

        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.choices_widget = QtWidgets.QListWidget()
        self.choices_widget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        for choice in choices:
            item = QtWidgets.QListWidgetItem()
            item.setText(choice)
            self.choices_widget.addItem(item)
        main_layout.addWidget(self.choices_widget)

        button_box_layout = QtWidgets.QGridLayout()
        selection_completed_btn = QtWidgets.QPushButton("Ok")
        selection_completed_btn.clicked.connect(self.selection_completed)
        select_all_btn = QtWidgets.QPushButton("Select all")
        select_all_btn.clicked.connect(self.select_all)
        clear_all_btn = QtWidgets.QPushButton("Clear all")
        clear_all_btn.clicked.connect(self.clear_all)
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.cancel)

        button_box = QtWidgets.QWidget()
        button_box_layout.addWidget(selection_completed_btn, 0, 0)
        button_box_layout.addWidget(cancel_btn, 0, 1)
        button_box_layout.addWidget(select_all_btn, 1, 0)
        button_box_layout.addWidget(clear_all_btn, 1, 1)
        button_box.setLayout(button_box_layout)

        main_layout.addWidget(button_box)
        self.setLayout(main_layout)
        self.show()
        self.raise_()

    def selection_completed(self):
        """Selection completed, set the value and close"""
        self.selection = [item.text() for item in
                          self.choices_widget.selectedItems()]
        self.close()

    def select_all(self):
        """Set all possible values as selected"""
        self.choices_widget.selectAll()
        self.selection = [item.text() for item in
                          self.choices_widget.selectedItems()]

    def clear_all(self):
        """Reset to have no selected values"""
        self.choices_widget.clearSelection()
        self.selection = []

    def cancel(self):
        """cancel and set the selection to an empty list"""
        self.selection = []
        self.close()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.cancel()
        elif e.key() == QtCore.Qt.Key_Enter:
            self.selection_completed()
        else:
            super(MultipleChoicesDialog, self).keyPressEvent(e)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    dialog = MultipleChoicesDialog()
    dialog.exec_()
    print(dialog.selection)
