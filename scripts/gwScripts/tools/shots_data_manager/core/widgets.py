
try:
    from PySide6 import QtWidgets
except:
    from PySide2 import QtWidgets

from gwScripts.tools.shots_data_manager.core.shots import Shots


class Table(QtWidgets.QTableWidget):
    """
    Custom QTableWidget for the ShotsDataManager.
    Implements and overrides methods to tailor its use for shot data manipulation.
    """
    def __init__(self, parent):
        """
        Initializes the dialog.

        :param parent: Use to parent the dialog to another widget.
        :type parent: QtWidgets.QWidget

        :return: None
        :rtype: None
        """
        super(Table, self).__init__(parent)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Shot Name", "Start Frame", "End Frame"])

    def populate(self, shots_data):
        """
        Populates the table with the information from the shots data object.

        :param shots_data: Shots information in a dictionary form.
        :type shots_data: Shots

        :return: None
        :rtype: None
        """
        if not isinstance(shots_data, Shots):
            raise TypeError("Expected Shots instance, got {}".format(type(shots_data)))

        self.clear()
        self.setRowCount(len(shots_data))
        for row in range(self.rowCount()):
            shot_name = shots_data.get_shot_name(row)
            start_frame = self._exact_frame(shots_data.get_shot_start(row))
            end_frame = self._exact_frame(shots_data.get_shot_end(row))
            self.setItem(row, 0, QtWidgets.QTableWidgetItem(shot_name))
            self.setItem(row, 1, QtWidgets.QTableWidgetItem(str(start_frame)))
            self.setItem(row, 2, QtWidgets.QTableWidgetItem(str(end_frame)))

    def rename_shots(self, name, start, incr, padd):
        """
        Renames the items in all rows based on given parameters.

        :param name: The base name to give each item for shot renaming.
        :type name: str

        :param start: The starting shot number for shot renaming.
        :type start: int

        :param incr: The increment number for shot renaming.
        :type incr: int

        :param padd: The padding amount for shot renaming.
        :type padd: int

        :return: None
        :rtype: None
        """
        for row in range(self.rowCount()):
            shot_name = name + str(start + (incr * row)).zfill(padd)
            self.setItem(row, 0, QtWidgets.QTableWidgetItem(str(shot_name)))

    def clear(self):
        """
        Override of :meth:`QtWidgets.QTableWidget.clear`.
        """
        self.setRowCount(0)
        self.setRowCount(1)

    def insertRow(self):
        """
        Override of :meth:`QtWidgets.QTableWidget.insertRow`.
        Inserts the new row after the last selected item, if selected.
        """
        if self.selected_items_rows:
            super(Table, self).insertRow(max(self.selected_items_rows) + 1)
        else:
            super(Table, self).insertRow(self.rowCount())

    def removeRow(self):
        """
        Override of :meth:`QtWidgets.QTableWidget.removeRow`.
        Removes the rows of selected items, if selected.
        """
        if self.selected_items_rows:
            for i in sorted(self.selected_items_rows, reverse=True):
                super(Table, self).removeRow(i)
        else:
            super(Table, self).removeRow(self.rowCount() - 1)

    def resizeEvent(self, event):
        """
        Override of :meth:`QtWidgets.QTableWidget.resizeEvent`.
        Resizes the columns to the new size based on a fixed ratio.
        """
        super(Table, self).resizeEvent(event)
        width = event.size().width()
        self.setColumnWidth(0, width * 0.6)
        self.setColumnWidth(1, width * 0.2)
        self.setColumnWidth(2, width * 0.2)

    @property
    def selected_items_rows(self):
        """
        :return: The row numbers for selected rows in the table.
        :rtype: list[int]
        """
        return [item.row() for item in self.selectedIndexes()]

    @property
    def shots_data(self):
        """
        :return: The data of all the shots in the table, in a dict form.
        :rtype: Shots
        """
        shots_data = Shots()
        for row in range(self.rowCount()):
            name = "" if not self.item(row, 0) else self.item(row, 0).text()
            start = 0 if not self.item(row, 1) else float(self.item(row, 1).text())
            end = 0 if not self.item(row, 2) else float(self.item(row, 2).text())
            shots_data.insert_shot(row, name, start, end)
        return shots_data

    @staticmethod
    def _exact_frame(frame):
        """
        Frame number as an integer if it is whole, otherwise as a float.

        :param frame: The input frame number.
        :type frame: int | float

        :return: The frame number in its most exact form.
        :rtype: int | float
        """
        _frame = float(frame)
        return int(round(_frame)) if round(_frame) == _frame else _frame


class NumericDelegate(QtWidgets.QStyledItemDelegate):
    """
    Custom delegate that keeps the numbering within a whole numbers range.
    """
    MIN_RANGE = -999999999
    MAX_RANGE = 999999999
    BASE_RANGE = 1

    def createEditor(self, parent, option, index):
        """
        Override of :meth:`QtWidgets.QStyledItemDelegate.createEditor`.

        :return: QSpinBox widget with the correct range.
        :rtype: QtWidgets.QSpinBox
        """
        whole_nums = QtWidgets.QSpinBox(parent)
        whole_nums.setRange(self.MIN_RANGE, self.MAX_RANGE)
        return whole_nums
