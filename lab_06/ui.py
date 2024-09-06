import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator


class CustomLabel(QtWidgets.QLabel):
    """Кастомный виджет QLabel для работы с кнопками мыши."""
    # Задание доступных сигналов.
    leftButtonPressed = QtCore.pyqtSignal(int, int)  # Сигнал от левой кнопки мыши.
    middleButtonPressed =  QtCore.pyqtSignal(int, int)  # Сигнал от центральной кнопки мыши.
    rightButtonPressed = QtCore.pyqtSignal()  # Сигнал от правой кнопки мыши.

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        if event.button() == Qt.MouseButton.LeftButton:
            self.leftButtonPressed.emit(x, y)
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleButtonPressed.emit(x, y)
        if event.button() == Qt.MouseButton.RightButton:
            self.rightButtonPressed.emit()

class Ui(object):
    """Класс пользовательского интерфейса."""
    canvas_length = 1001
    canvas_width = 901

    def _setUi(self, MainWindow):
        """Создает пользовательский интерфейс."""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 1000)
        MainWindow.move(240, 0)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.font = QtGui.QFont()
        self.validator = QIntValidator()

        self._setPushButtons()
        self._setCheckBoxes()
        self._setQColorDialogs()
        self._setLineEdits()
        self._setTableWidget()
        self._setWidget()
        self._setQPixmap()
        self._setLabels()
        self._setInfoWindows()

        MainWindow.setCentralWidget(self.centralwidget)

    def _setupFont(self, size: int, bold: bool):
        """Настраивает шрифт."""
        self.font.setPointSize(size)
        self.font.setBold(bold)

    def _setupValidator(self, reg_exp: str):
        """Настраивает валидатор по регулярному выражению."""
        self.validator = QIntValidator()

    def _setLabels(self):
        """Устанавливает поля с текстом (надписи)."""
        self._setupFont(16, True)

        # Надпись 'Режим закраски'.
        self.label_shade_mode = QtWidgets.QLabel(self.centralwidget)
        self.label_shade_mode.setGeometry(QtCore.QRect(0, 0, 400, 40))
        self.label_shade_mode.setFont(self.font)
        self.label_shade_mode.setStyleSheet("""background-color: rgb(145, 145, 145);
                                               color: rgb(255, 255, 255);""")
        self.label_shade_mode.setText("Режим закраски")
        self.label_shade_mode.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_shade_mode.setObjectName("label_shade_mode")

        # Надпись 'Цвета'.
        self.label_colors = QtWidgets.QLabel(self.centralwidget)
        self.label_colors.setGeometry(QtCore.QRect(0, 90, 400, 40))
        self.label_colors.setFont(self.font)
        self.label_colors.setStyleSheet("""background-color: rgb(145, 145, 145);
                                               color: rgb(255, 255, 255);""")
        self.label_colors.setText("Цвета")
        self.label_colors.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_colors.setObjectName("label_colors")

        # Надпись 'Точки'.
        self.label_draw_figure = QtWidgets.QLabel(self.centralwidget)
        self.label_draw_figure.setGeometry(QtCore.QRect(0, 170, 400, 40))
        self.label_draw_figure.setFont(self.font)
        self.label_draw_figure.setStyleSheet("""background-color: rgb(145, 145, 145);
                                                       color: rgb(255, 255, 255);""")
        self.label_draw_figure.setText("Точки")
        self.label_draw_figure.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_draw_figure.setObjectName("label_points")

        # Надпись 'Рисование фигуры'.
        self.label_draw_figure = QtWidgets.QLabel(self.centralwidget)
        self.label_draw_figure.setGeometry(QtCore.QRect(0, 735, 400, 40))
        self.label_draw_figure.setFont(self.font)
        self.label_draw_figure.setStyleSheet("""background-color: rgb(145, 145, 145);
                                                       color: rgb(255, 255, 255);""")
        self.label_draw_figure.setText("Рисование фигуры")
        self.label_draw_figure.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_draw_figure.setObjectName("label_draw_figure")

        self._setupFont(14, False)

        # Надпись 'Цвет заливки'.
        self.label_color_filling = QtWidgets.QLabel(self.centralwidget)
        self.label_color_filling.setGeometry(QtCore.QRect(20, 135, 150, 30))
        self.label_color_filling.setFont(self.font)
        self.label_color_filling.setText("Цвет заливки")
        self.label_color_filling.setObjectName("label_color_filling")

        # Надпись 'X'.
        self.label_x = QtWidgets.QLabel(self.centralwidget)
        self.label_x.setGeometry(QtCore.QRect(100, 210, 30, 30))
        self.label_x.setFont(self.font)
        self.label_x.setText("X")
        self.label_x.setObjectName("label_x")

        # Надпись 'Y'.
        self.label_right_mouse = QtWidgets.QLabel(self.centralwidget)
        self.label_right_mouse.setGeometry(QtCore.QRect(290, 210, 30, 30))
        self.label_right_mouse.setFont(self.font)
        self.label_right_mouse.setText("Y")
        self.label_right_mouse.setObjectName("label_y")

        self._setupFont(16, True)

        # Надпись 'Размер полотна ...x... пикселей'.
        self.label_canvas_size = QtWidgets.QLabel(self.centralwidget)
        self.label_canvas_size.setGeometry(650, 0, 600, 30)
        self.label_canvas_size.setFont(self.font)
        self.label_canvas_size.setText(f"""Размер полотна - {self.canvas_length}x{self.canvas_width} пикселей""")
        self.label_canvas_size.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_canvas_size.setObjectName("label_canvas_size")

    def _setPushButtons(self):
        """Устанавливает кнопки."""
        self._setupFont(16, True)

        # Кнопка выбора цвета заливки
        self.pushbutton_set_color_filling = QtWidgets.QPushButton(self.centralwidget)
        self.pushbutton_set_color_filling.setGeometry(QtCore.QRect(150, 135, 80, 30))
        self.pushbutton_set_color_filling.setObjectName("pushbutton_set_color_line_segment")

        # Кнопка добавления точки.
        self.pushbutton_add_point = QtWidgets.QPushButton(self.centralwidget)
        self.pushbutton_add_point.setGeometry(QtCore.QRect(20, 280, 360, 40))
        self.pushbutton_add_point.setFont(self.font)
        self.pushbutton_add_point.setText("Добавить точку")
        self.pushbutton_add_point.setObjectName("pushbutton_add_point")

        # Кнопка добавления затравочного пикселя.
        self.pushbutton_add_seed_pixel = QtWidgets.QPushButton(self.centralwidget)
        self.pushbutton_add_seed_pixel.setGeometry(QtCore.QRect(20, 325, 360, 40))
        self.pushbutton_add_seed_pixel.setFont(self.font)
        self.pushbutton_add_seed_pixel.setText("Добавить пиксель затравки")
        self.pushbutton_add_seed_pixel.setObjectName("pushbutton_add_seed_pixel")

        # Кнопка замыкания фигуры.
        self.pushbutton_close_figure = QtWidgets.QPushButton(self.centralwidget)
        self.pushbutton_close_figure.setGeometry(QtCore.QRect(20, 370, 360, 40))
        self.pushbutton_close_figure.setFont(self.font)
        self.pushbutton_close_figure.setText("Замкнуть фигуру")
        self.pushbutton_close_figure.setObjectName("pushbutton_close_figure")

        # Кнопка заливки.
        self.pushbutton_filling = QtWidgets.QPushButton(self.centralwidget)
        self.pushbutton_filling.setGeometry(QtCore.QRect(20, 785, 360, 40))
        self.pushbutton_filling.setFont(self.font)
        self.pushbutton_filling.setText("Залить")
        self.pushbutton_filling.setObjectName("pushbutton_filling")

        # Кнопка очистки полотна.
        self.push_button_clear_canvas = QtWidgets.QPushButton(self.centralwidget)
        self.push_button_clear_canvas.setGeometry(QtCore.QRect(20, 830, 360, 40))
        self.push_button_clear_canvas.setFont(self.font)
        self.push_button_clear_canvas.setText("Очистить полотно")
        self.push_button_clear_canvas.setObjectName("push_button_clear_canvas")

    def _setCheckBoxes(self):
        """Устанавливает чекбоксы."""
        self._setupFont(14, False)

        # Чекбокс выбора режима закраски - с задержкой.
        self.checkbox_delay_on = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_delay_on.setGeometry(QtCore.QRect(10, 50, 230, 30))
        self.checkbox_delay_on.setFont(self.font)
        self.checkbox_delay_on.setText("С задержкой")
        self.checkbox_delay_on.setObjectName("checkbox_delay_on")

        # Чекбокс выбора режима закраски - без задержки.
        self.checkbox_delay_off = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_delay_off.setGeometry(QtCore.QRect(195, 50, 140, 30))
        self.checkbox_delay_off.setFont(self.font)
        self.checkbox_delay_off.setText("Без задержки")
        self.checkbox_delay_off.setObjectName("checkbox_delay_off")

    def _setQColorDialogs(self):
        """Устанавливает окна выбора цвета"""
        self.qcolor_dialog_filling = QtWidgets.QColorDialog()

    def _setLineEdits(self):
        """Устанавливает поля ввода."""
        self._setupFont(14, False)
        self._setupValidator("[0-9]+")

        # Поле ввода координаты точки по оси X.
        self.line_edit_x = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_x.setGeometry(QtCore.QRect(20, 240, 170, 30))
        self.line_edit_x.setFont(self.font)
        self.line_edit_x.setValidator(self.validator)
        self.line_edit_x.setText("")
        self.line_edit_x.setObjectName("line_edit_x")

        # Поле ввода координаты точки по оси Y.
        self.line_edit_y = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_y.setGeometry(QtCore.QRect(210, 240, 170, 30))
        self.line_edit_y.setFont(self.font)
        self.line_edit_y.setValidator(self.validator)
        self.line_edit_y.setText("")
        self.line_edit_y.setObjectName("line_edit_y")

    def _setTableWidget(self):
        """Устанавливает таблицу"""
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setGeometry(QtCore.QRect(20, 425, 362, 300))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setStyleSheet("""QTableWidget {background-color: rgb(255, 255, 255);}
                                          QHeaderView::section {
                                                background-color: rgb(166, 166, 166);
                                                color: rgb(255, 255, 255);
                                                font-weight: bold;
                                                font-size: 14pt;}""")
        self.tableWidget.verticalHeader().setVisible(False)  # Убираем строковую индексацию

        column1 = QtWidgets.QTableWidgetItem("№")
        column2 = QtWidgets.QTableWidgetItem("X")
        column3 = QtWidgets.QTableWidgetItem("Y")

        column1.setFont(self.font)
        column2.setFont(self.font)
        column3.setFont(self.font)

        self.tableWidget.setHorizontalHeaderItem(0, column1)
        self.tableWidget.setHorizontalHeaderItem(1, column2)
        self.tableWidget.setHorizontalHeaderItem(2, column3)

        # Настройка размеров колонок.
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 155)
        self.tableWidget.setColumnWidth(2, 155)

        # Убирание полос прокрутки.
        
        # self.tableWidget.setVerticalScrollBarPolicy(QtCore.ScrollBarAlwaysOff)
        # self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def _setWidget(self):
        """Устанавливает виджет."""
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(400, 0, self.canvas_length + 100, self.canvas_width + 100))
        self.widget.setStyleSheet("""background-color: rgb(200, 200, 200);""")
        self.widget.setObjectName("widget")

    def _setQPixmap(self):
        """Устанавливает пиксельное полотно."""
        # Устанавливаем label для вставки в него пиксельного полотна.
        self.label_pixels = QtWidgets.QLabel(self.centralwidget)
        self.label_pixels.setGeometry(QtCore.QRect(450, 50, self.canvas_length, self.canvas_width))

        self.label_pixels_custom = CustomLabel(self.label_pixels)

        self.pixmap = QtGui.QPixmap(self.canvas_length, self.canvas_width)
        self.pixmap.fill(QtGui.QColor(255, 255, 255))

        self.painter = QtGui.QPainter(self.pixmap)

        self.label_pixels_custom.setPixmap(self.pixmap)

    def _setInfoWindows(self):
        """Устанавливает информационные окна."""
        self._setupFont(14, False)

        # Ошибка - 'Некорректное определение координат точки.'.
        self.info_window01 = QtWidgets.QMessageBox()
        self.info_window01.setWindowTitle("ОШИБКА!")
        self.info_window01.setText("Некорректное определение координат точки.")

        # Ошибка - 'Некорректное определение координат пикселя затравки.'.
        self.info_window02 = QtWidgets.QMessageBox()
        self.info_window02.setWindowTitle("ОШИБКА!")
        self.info_window02.setText("Некорректное определение координат пикселя затравки.")

        # Ошибка - 'Недостаточно ребер у фигуры для ее замыкания.'.
        self.info_window03 = QtWidgets.QMessageBox()
        self.info_window03.setWindowTitle("ОШИБКА!")
        self.info_window03.setText("Недостаточно ребер у фигуры для замыкания.")

        # Ошибка - 'Не определено ни одной фигуры.'.
        self.info_window04 = QtWidgets.QMessageBox()
        self.info_window04.setWindowTitle("ОШИБКА!")
        self.info_window04.setText("Не определено ни одной фигуры.")

        # Сообщение - 'Вы замкнули фигуру.'.
        self.info_window05 = QtWidgets.QMessageBox()
        self.info_window05.setWindowTitle("СООБЩЕНИЕ!")
        self.info_window05.setText("Вы замкнули фигуру.")

        # Ошибка - 'Координаты затравочного пикселя не определены.'.
        self.info_window06 = QtWidgets.QMessageBox()
        self.info_window06.setWindowTitle("ОШИБКА!")
        self.info_window06.setText("Координаты затравочного пикселя не определены.")

        self.info_window01.setFont(self.font)
        self.info_window02.setFont(self.font)
        self.info_window03.setFont(self.font)
        self.info_window04.setFont(self.font)
        self.info_window05.setFont(self.font)
        self.info_window06.setFont(self.font)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui()
    ui._setUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())