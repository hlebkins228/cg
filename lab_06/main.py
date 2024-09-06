import sys
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QMessageBox
from copy import deepcopy


from ui import Ui
from draw import Draw
from qtable import QTable


class App(Ui):
    """Модель программы для лабораторной работы №5."""
    color_edges = QtGui.QColor(1, 1, 1)  # Цвет для граней фигуры.
    color_seed_pixel = QtGui.QColor(255, 0, 0)  # Цвет пикселя затравки.
    color_canvas = QtGui.QColor(255, 255, 255)  # Цвет фона.
    color_filling = QtGui.QColor(125, 125, 255)  # Цвет заливки.
    color_under_seed_pixel = color_canvas  # Цвет под пикселем затравки.

    seed_pixel = tuple()  # Пиксель затравки.

    mode_delay = True  # Режим задержки.

    number_figure_points = 0  # Количество точек текущей фигуры.
    list_figure_points = list()  # Список точек текущей фигуры.

    number_figure_edges = 0  # Количество ребер текущей фигур.
    list_figure_edges = list()  # Список ребер текущей фигуры.

    number_unfilled_figures = 0  # Количество незаполненных фигур
    list_unfilled_figures = list()  # Список всех незаполненных фигур.

    number_all_figures = 0  # Количество всех фигур (как незаполненных, так и заполненных)

    def __init__(self, MainWindow: QtWidgets.QMainWindow):
        super().__init__()
        self._setUi(MainWindow)

        self.draw = Draw(self.painter, self.label_pixels_custom, self.pixmap)
        self.table = QTable(self.tableWidget)

        self.checked_mode_filling_checkbox = self.checkbox_delay_on
        self._setCheckedStatusCheckbox(self.checkbox_delay_on, True)

        self._setColorFilling(self.color_filling)
        self._setPushButtonColor(self.pushbutton_set_color_filling, self.color_filling)

        MainWindow.show()

        self._workApp()

    def _workApp(self):
        """Реализует работу приложения."""
        self._workCheckBoxes()
        self._workPushButtons()
        self._workMouseButtons()

        MainWindow.setCentralWidget(self.centralwidget)

    def _workCheckBoxes(self):
        """Реализует работу чекбоксов."""
        # Чекбоксы выбора режима заливки.
        self.checkbox_delay_on.clicked.connect(lambda: self._uncheckModeFillingCheckbox(self.checkbox_delay_on))
        self.checkbox_delay_off.clicked.connect(lambda: self._uncheckModeFillingCheckbox(self.checkbox_delay_off))

    def _workPushButtons(self):
        """Реализует работу кнопок."""
        # Выбор цвета заливки.
        self.pushbutton_set_color_filling.clicked.connect(lambda: self._clickPushButtonSetColorFilling())
        # Добавление точки на полотно.
        self.pushbutton_add_point.clicked.connect(lambda: self._clickPushButtonAddPoint())
        # Добавление пикселя затравки.
        self.pushbutton_add_seed_pixel.clicked.connect(lambda: self._clickPushButtonAddSeedPixel())
        # Замыкание фигуры.
        self.pushbutton_close_figure.clicked.connect(lambda: self._clickPushButtonCloseFigure())
        # Заливка.
        self.pushbutton_filling.clicked.connect(lambda: self._clickPushButtonFilling())
        # Очистка полотна.
        self.push_button_clear_canvas.clicked.connect(lambda: self._clickPushButtonClearCanvas())
        

    def _workMouseButtons(self):
        """Реализует работу кнопок мыши."""
        self.label_pixels_custom.leftButtonPressed.connect(self._clickLeftButtonMouse)
        self.label_pixels_custom.middleButtonPressed.connect(self._clickMiddleButtonMouse)
        self.label_pixels_custom.rightButtonPressed.connect(self._clickRightButtonMouse)

    def _showInfoWindow(self, info_window: QtWidgets.QMessageBox):
        """Выводит на экран информационное окно."""
        info_window.exec()

    def _updatePixmap(self):
        """Обновляет состояние полотна пикселей."""
        self.label_pixels_custom.setPixmap(self.pixmap)

    def _setCheckedStatusCheckbox(self, checkbox: QtWidgets.QCheckBox, status: bool):
        """Устанавливает статус чекбоксу."""
        checkbox.setChecked(status)

    def _setCheckedModeFillingCheckbox(self, checkbox: QtWidgets.QCheckBox):
        """Устанавливает, какой чекбокс режима закраски был нажат."""
        self.checked_mode_filling_checkbox = checkbox

    def _uncheckModeFillingCheckbox(self, checkbox: QtWidgets.QCheckBox):
        """Снимает выбор предыдущего выбранного чекбокса, отвечающего за выбор режима заливки."""
        if self.checked_mode_filling_checkbox != checkbox:
            self._setCheckedStatusCheckbox(self.checked_mode_filling_checkbox, False)
        else:
            self._setCheckedStatusCheckbox(checkbox, True)

        self._setCheckedModeFillingCheckbox(checkbox)
        self._chooseModeFilling()

    def _setPushButtonColor(self, pushbutton: QtWidgets.QPushButton, color: QtGui.QColor):
        """Устанавливает цвет кнопки."""
        pushbutton.setStyleSheet(f"background-color: {color.name()};")

    def _setModeFilling(self, status: bool):
        """Устанавливает режим, в котором работает заливка заливки."""
        self.mode_delay = status

    def _chooseModeFilling(self):
        """Выбирает режим заливки в зависимости от выбранного чекбокса."""
        if self.checkbox_delay_on.isChecked():
            self._setModeFilling(True)
        elif self.checkbox_delay_off.isChecked():
            self._setModeFilling(False)
        else:
            self._setModeFilling(True)

    def _paintOverCanvas(self):
        """Закрашивает полотно."""
        self.pixmap.fill(self.color_canvas)
        self._updatePixmap()

    def _setColorFilling(self, color: QtGui.QColor):
        """Устанавливает цвет заливки."""
        self.color_filling = color

    def _chooseColorFilling(self):
        """Выбирает цвет заливки."""
        if self.qcolor_dialog_filling.exec():
            self._setColorFilling(self.qcolor_dialog_filling.selectedColor())

    def _listPointsAddPoint(self, point: tuple):
        """Добавляет точку в список точек."""
        self.number_figure_points += 1
        self.list_figure_points.append(point)

    def _listPointsClear(self):
        """Очищает список точек."""
        self.number_figure_points = 0
        self.list_figure_points.clear()

    def _listEdgesAddEdge(self, edge: tuple):
        """Добавляет ребро текущей фигуры в список ребер текущей фигуры."""
        self.number_figure_edges += 1
        self.list_figure_edges.append(edge)

    def _listEdgesClear(self):
        """Очищает список ребер текущей фигуры."""
        self.number_figure_edges = 0
        self.list_figure_edges.clear()

    def _listFiguresAddFigure(self, figure: list):
        """Добавляет фигуру в список фигур."""
        self.number_unfilled_figures += 1
        self.number_all_figures += 1
        self.list_unfilled_figures.append(figure)

    def _listFiguresClear(self):
        """Очищает список фигур."""
        self.number_unfilled_figures = 0
        self.list_unfilled_figures.clear()

    def _setCoordinatesSeedPixel(self, point: tuple):
        """Устанавливает координаты пикселя затравки."""
        if point != ():
            self.draw.updateImageInformation()
            self.color_under_seed_pixel = self.draw.image.pixelColor(point[0], point[1])
        self.seed_pixel = point

    def _readIntLineEdit(self, line_edit: QtWidgets.QLineEdit) -> int:
        """Читает целочисленные данные с поля ввода."""
        try:
            data = int(line_edit.text())

            return data
        except ValueError:
            raise ValueError

    def _readPointXCoordinate(self) -> int:
        """Читает координату точки по оси X."""
        try:
            x = self._readIntLineEdit(self.line_edit_x)

            return x
        except ValueError:
            return -1

    def _readPointYCoordinate(self) -> int:
        """Читает координату точки по оси Y."""
        try:
            y = self._readIntLineEdit(self.line_edit_y)

            return y
        except ValueError:
            return -1

    def _drawPoint(self, point: tuple, color: QtGui.QColor):
        """Рисует точку на полотне."""
        self.draw.setPainterColor(color)

        self.draw.drawPixel(point)
        self._updatePixmap()

    def _drawLineSegment(self, point0: tuple, point1: tuple, color: QtGui.QColor):
        """Рисует отрезок на полотне."""
        self.draw.setPainterColor(color)

        self.draw.drawLineSegment(point0, point1)
        self._updatePixmap()

    def _addPoint(self, point: tuple):
        """Добавляет точку на полотно."""
        x, y = point

        self._listPointsAddPoint(point)
        self.table.tableAddRow(self.number_figure_points, x, y)

        self._drawPoint(point, self.color_edges)

        if self.number_figure_points >= 2:
            self._listEdgesAddEdge((self.list_figure_points[-2], self.list_figure_points[-1]))
            self._drawLineSegment(self.list_figure_points[-2], self.list_figure_points[-1], self.color_edges)
        if self.number_figure_points >= 3:
            if self.list_figure_points[-1] == self.list_figure_points[0]:
                self._showInfoWindow(self.info_window05)

                self._closeFigure()

    def _closeFigure(self):
        """Замыкает фигуру."""
        if self.number_figure_edges <= 1:
            self._showInfoWindow(self.info_window02)
        else:
            if self.list_figure_points[-1] != self.list_figure_points[0]:
                self._listEdgesAddEdge((self.list_figure_points[-1], self.list_figure_points[0]))
                self._drawLineSegment(self.list_figure_points[-1], self.list_figure_points[0], self.color_edges)

            self._listFiguresAddFigure(deepcopy(self.list_figure_edges))

            self.table.tableAddRow("-" * 6, f"фигура №{self.number_all_figures}", "-" * 21)

            self._listPointsClear()
            self._listEdgesClear()

    def _clickLeftButtonMouse(self, x, y):
        """Реагирует на нажатие левой кнопки мыши."""
        point = (x, y)
        self._addPoint(point)

    def _clickMiddleButtonMouse(self, x, y):
        """Реагирует на нажатие центральной кнопки мыши."""
        if self.seed_pixel != ():
            self.draw.updateImageInformation()
            self._drawPoint(self.seed_pixel, self.color_under_seed_pixel)

        point = (x, y)
        self._setCoordinatesSeedPixel(point)

        self._drawPoint(self.seed_pixel, self.color_seed_pixel)

    def _clickRightButtonMouse(self):
        """Реагирует на нажатие правой кнопки мыши."""
        self._closeFigure()

    def _clickPushButtonSetColorFilling(self):
        """Реагирует на нажатие кнопки смены цвета заливки."""
        self._chooseColorFilling()
        self._setPushButtonColor(self.pushbutton_set_color_filling, self.color_filling)

    def _clickPushButtonAddPoint(self):
        """Реагирует на нажатие кнопки добавление точки."""
        x = self._readPointXCoordinate()
        y = self._readPointYCoordinate()

        if x == -1 or y == -1:
            self._showInfoWindow(self.info_window01)
        else:
            point = (x, y)
            self._addPoint(point)

    def _clickPushButtonAddSeedPixel(self):
        """Реагирует на нажатие кнопки добавления пикселя затравки."""
        x = self._readPointXCoordinate()
        y = self._readPointYCoordinate()

        if x == -1 or y == -1:
            self._showInfoWindow(self.info_window02)
        else:
            if self.seed_pixel != ():
                self.draw.updateImageInformation()
                self._drawPoint(self.seed_pixel, self.color_under_seed_pixel)

            point = (x, y)
            self._setCoordinatesSeedPixel(point)

            self._drawPoint(self.seed_pixel, self.color_seed_pixel)

    def _clickPushButtonCloseFigure(self):
        """Реагирует на нажатие кнопки замыкания фигуры."""
        self._closeFigure()

    def _clickPushButtonFilling(self):
        """Реагирует на нажатие кнопки заливки."""
        if self.seed_pixel == ():
            self._showInfoWindow(self.info_window06)
        else:
         
            self.draw.fillLineWithSeed(self.seed_pixel, self.color_filling, self.mode_delay)
            self._updatePixmap()

            self._setCoordinatesSeedPixel(())

            self._listFiguresClear()

    def _clickPushButtonClearCanvas(self):
        """Реагирует на нажатие кнопки очистки полотна."""
        self._listPointsClear()
        self._listEdgesClear()

        self.table.tableClear()

        self.number_all_figures = 0

        self._paintOverCanvas()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    work = App(MainWindow)

    sys.exit(app.exec())