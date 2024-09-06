from PyQt6 import QtWidgets, QtGui, QtCore


class QTable(object):
    """Класс для реализации таблицы на PyQT."""
    number_rows = 0
    font = QtGui.QFont()


    def __init__(self, table: QtWidgets.QTableWidget):
        self.table = table

        self._setupFont(13, False)

    def _setupFont(self, size: int, bold: bool):
        """Настраивает шрифт."""
        self.font.setPointSize(size)
        self.font.setBold(bold)

    def _tableCountRow(self):
        """Определяет текущее количество строк в таблице."""
        self.number_rows = self.table.rowCount()

    def tableAddRow(self, *items, item_edit_status=False):
        """Добавляет в таблицу строку с данными."""
        self._tableCountRow()

        self.table.insertRow(self.number_rows)

        for i in range(len(items)):
            item = QtWidgets.QTableWidgetItem(str(items[i]))
            item.setFont(self.font)

            if item_edit_status == False:
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)

            self.table.setItem(self.number_rows, i, item)

    def tableClear(self):
        """Очищает таблицу."""
        self.table.setRowCount(0)
        self._tableCountRow()
