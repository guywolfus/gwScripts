
from gwScripts.tools.shots_data_manager.core.shots import Shots

try:
    from PySide6 import QtWidgets
except:
    from PySide2 import QtWidgets


class Table(QtWidgets.QTableWidget):
    """
    Custom QTableWidget for the ShotsDataManager.
    Implements and overrides methods to tailor its use for shot data manipulation.
    """
    def __init__(self, parent):
        """
        Initializes the dialog.

        :arg QtWidgets.QWidget parent: Optional. Use to parent the dialog to another widget.
            Defaults to `None`.
        :return: None
        :rtype: None
        """
        super(Table, self).__init__(parent)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Shot Name", "Start Frame", "End Frame"])

    def populate(self, shots_data):
        """
        Populates the table with the information from the shots data object.

        :arg Shots shots_data: Shots information in a dictionary form.
        :return: None
        :rtype: None
        """
        if isinstance(shots_data, Shots):
            self.clear()
            self.setRowCount(len(shots_data))
            for row in range(self.rowCount()):
                shot_name = shots_data.get_shot_name(row)
                start_frame = float(shots_data.get_shot_start(row))
                start_frame = int(round(start_frame)) if round(start_frame) == start_frame else start_frame
                end_frame = float(shots_data.get_shot_end(row))
                end_frame = int(round(end_frame)) if round(end_frame) == end_frame else end_frame
                self.setItem(row, 0, QtWidgets.QTableWidgetItem(shot_name))
                self.setItem(row, 1, QtWidgets.QTableWidgetItem(str(start_frame)))
                self.setItem(row, 2, QtWidgets.QTableWidgetItem(str(end_frame)))

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

    def rename_shots(self, name, start, incr, padd):
        """
        Renames the items in all rows based on given parameters.

        :arg str name: The base name to give each item for shot renaming.
        :arg int start: The starting shot number for shot renaming.
        :arg int incr: The increment number for shot renaming.
        :arg int padd: The padding amount for shot renaming.
        :return: None
        :rtype: None
        """
        for row in range(self.rowCount()):
            shot_name = name + str(start + (incr * row)).zfill(padd)
            self.setItem(row, 0, QtWidgets.QTableWidgetItem(str(shot_name)))

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
        :rtype: List[int]
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


class NumericDelegate(QtWidgets.QStyledItemDelegate):
    """
    Custom delegate that keeps the numbering within a whole numbers range.
    """
    min_range = -999999999
    max_range = 999999999
    base_range = 1

    def createEditor(self, parent, option, index):
        """
        Override of :meth:`QtWidgets.QStyledItemDelegate.createEditor`.

        :return: QSpinBox widget with the correct range.
        :rtype: QtWidgets.QSpinBox
        """
        whole_nums = QtWidgets.QSpinBox(parent)
        whole_nums.setRange(self.min_range, self.max_range)
        return whole_nums
