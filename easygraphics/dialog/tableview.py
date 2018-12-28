from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from typing import List


class TableViewModel(QtCore.QAbstractTableModel):
    def __init__(self, datas: List, fields: List[str], field_names: List[str] = None):
        self._datas = datas

        if fields == None:
            if len(datas) > 0:
                fields = list(filter(lambda x: not x.startswith("_"), dir(datas[0])))
            else:
                fields = []
        self._fields = fields
        if field_names is None:
            self._field_names = fields
        else:
            self._field_names = field_names
        super().__init__()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._datas)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._fields)

    def data(self, index: QtCore.QModelIndex, role=None):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        elif role == QtCore.Qt.DisplayRole:
            data = self._datas[index.row()]
            field = self._fields[index.column()]
            return getattr(data, field, "")
        return QtCore.QVariant()

    def headerData(self, section: int, orientation, role=None):
        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        elif role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._field_names[section]
            else:
                return section + 1
        return QtCore.QVariant()

    def sort(self, column: int, order=None):
        self.beginResetModel()
        name = self._fields[column]
        key_func = lambda obj: getattr(obj, name)
        if order == QtCore.Qt.DescendingOrder:
            reverse = True
        else:
            reverse = False
        self._datas = sorted(self._datas, key=key_func, reverse=reverse)
        self.endResetModel()


class TableViewDialog(QtWidgets.QDialog):
    def __init__(self, datas: List, fields: List[str] = None, field_names: List[str] = None, title="Demo"):
        super().__init__(None,
                         QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)

        self.setWindowTitle(title)

        # set up a special case for quick demo

        layout = QtWidgets.QVBoxLayout()

        self._model = TableViewModel(datas, fields, field_names)
        self._table_view = QtWidgets.QTableView()
        self._table_view.setModel(self._model)
        self._table_view.setSortingEnabled(True)
        self._table_view.setAlternatingRowColors(True)
        self._table_view.setStyleSheet("QTableView {"
                                       "color: black;"
                                       "gridline-color: black;"
                                       "background-color: seashell; "
                                       "alternate-background-color: 	mintcream;"
                                       "selection-color: white; "
                                       "selection-background-color: rgb(77, 77, 77); "
                                       "border: 2px groove gray;"
                                       "border-radius: 0px;"
                                       "padding: 2px 4px;"
                                       "}"
                                       "QHeaderView {"
                                       "color: black;"
                                       "font-weight: bold;"
                                       "gridline-color: black;"
                                       "padding: 0;"
                                       "}"
                                       )
        layout.addWidget(self._table_view)

        button_box = QtWidgets.QDialogButtonBox()
        confirm_button = button_box.addButton(QtWidgets.QDialogButtonBox.Ok)
        layout.addWidget(button_box)
        confirm_button.clicked.connect(self.confirm)
        self.setLayout(layout)
        self.setWindowTitle(title)

    def confirm(self):
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])


    class A:
        pass


    def create_obj(name, age, sex):
        obj = A()
        obj.name = name
        obj.age = age
        obj.sex = sex
        return obj


    datas = [create_obj("Jack", 22, "M"),
             create_obj("Micheal", 40, "F"),
             create_obj("David", 24, "M")]

    dialog = TableViewDialog(datas, ['name', 'age', 'sex'])
    dialog.show()
