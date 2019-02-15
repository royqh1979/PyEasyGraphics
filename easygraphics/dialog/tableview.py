from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from typing import List, Union
import inspect


class ListTableViewModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, column_names: List[str] = None):
        super().__init__()
        # check we have valid data lists
        if len(args) < 1:
            raise RuntimeError("No data list provided!")
        for lst in args:
            if not hasattr(lst, '__getitem__'):
                raise RuntimeError("must provide list-like objects to display!")
        self._datas = args
        if column_names is None:
            self._column_names = []
            f_back = inspect.currentframe().f_back
            for i in range(len(args)):
                self._column_names.append("list_" + str(i))
        else:
            if len(column_names) != len(args):
                raise RuntimeError("field names must have the same length with data lists!")
            self._column_names = column_names

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._datas[0])

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._column_names)

    def data(self, index: QtCore.QModelIndex, role=None):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        elif role == QtCore.Qt.DisplayRole:
            lst = self._datas[index.column()]
            if len(lst) <= index.row():
                return QtCore.QVariant()
            return str(lst[index.row()])
        return QtCore.QVariant()

    def headerData(self, section: int, orientation, role=None):
        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        elif role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._column_names[section]
            else:
                return section + 1
        return QtCore.QVariant()


class ObjectTableViewModel(QtCore.QAbstractTableModel):
    def __init__(self, datas: List, fields: List[str], field_names: List[str] = None):
        super().__init__()
        self._datas = datas

        if fields is None:
            if len(datas) > 0:
                fields = list(filter(lambda x: not x.startswith("_"), dir(datas[0])))
            else:
                fields = []
        self._fields = fields
        if field_names is None:
            self._field_names = fields
        else:
            self._field_names = field_names


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
            return str(getattr(data, field, ""))
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
    def __init__(self, model: Union[ObjectTableViewModel, ListTableViewModel], title="Demo"):
        super().__init__(None,
                         QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle(title)

        # set up a special case for quick demo

        layout = QtWidgets.QVBoxLayout()
        self._model = model
        self._table_view = QtWidgets.QTableView()
        self._table_view.setModel(self._model)
        if isinstance(model, ObjectTableViewModel):
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
