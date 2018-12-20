from collections import OrderedDict

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from easygraphics.dialog._indexed_order_list import IndexedOrderedDict

__all__ = ['MultipleFieldsDialog']


class MultipleFieldsDialog(QtWidgets.QDialog):
    """Dialog with multiple fields stored in a dict, with the label
       being the key and the entry being the corresponding value"""

    def __init__(self, labels=None, title="Demo", masks=None):
        super(MultipleFieldsDialog, self).__init__(None,
                                                   QtCore.Qt.WindowSystemMenuHint |
                                                   QtCore.Qt.WindowTitleHint)

        self.enters = IndexedOrderedDict()
        self.setWindowTitle(title)

        # set up a special case for quick demo
        if labels is None:
            labels = ["Regular field", "Masked field"]
            masks = [False, True]
            self.setWindowTitle("MultipleFieldsDialog demo")

        if masks is not None:
            assert len(masks) == len(labels)

        layout = QtWidgets.QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(1, 250)

        self._labels_ = []
        self.fields = []
        for index, choice in enumerate(labels):
            self._labels_.append(QtWidgets.QLabel())
            self._labels_[index].setText(choice)
            self.fields.append(QtWidgets.QLineEdit())
            self.fields[index].setText('')
            self.enters[choice] = ''
            if masks is not None and masks[index]:
                self.fields[index].setEchoMode(QtWidgets.QLineEdit.Password)
            layout.addWidget(self._labels_[index], index, 0)
            layout.addWidget(self.fields[index], index, 1)

        button_box = QtWidgets.QDialogButtonBox()
        confirm_button = button_box.addButton(QtWidgets.QDialogButtonBox.Ok)
        layout.addWidget(button_box, index + 1, 1)
        confirm_button.clicked.connect(self.confirm)
        self.setLayout(layout)
        self.setWindowTitle(title)
        self.show()
        self.raise_()

    def confirm(self):
        """Selection completed, set the value and close"""
        o_dict = self.enters
        for index, item in enumerate(self._labels_):
            o_dict[item.text()] = self.fields[index].text()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    dialog = MultipleFieldsDialog()
    dialog.exec_()
    print(dialog.get_ordered_dict())
