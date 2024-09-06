from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import sys

from main_window import Ui_MainWindow
from config import points_size, plot_fontsize, points_color_1, points_color_2
from config import columns_count, cord_regexp, calc_accuracy, eps
from point_add_window import Ui_Dialog

from math_functions import find_best_circles_params

class MainApp(QMainWindow):
    def __init__(self, first_points_set, second_points_set):
        super(MainApp, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.points_set_1 = first_points_set
        self.points_set_2 = second_points_set

        self.circle_color_1 = 'orange'
        self.circle_color_2 = 'blue'
        self.lines_color = 'purple'

        self.min_x_cord = min([*self.points_set_1[0], *self.points_set_2[0]])
        self.max_x_cord = max([*self.points_set_1[0], *self.points_set_2[0]])

        self.circles_to_draw_dict = None
        self.figures_drawn = False

        self.prev_axes_len = 0

        self.changed_table_index = 1

        self.show_point_labels = False
        self.show_axes = False

        self.new_changes = True

        self.plot_layout = QVBoxLayout(self.ui.graphics_widget)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.plot_layout.addWidget(self.canvas)

        self.update_plot(points_list_1=self.points_set_1, points_list_2=self.points_set_2)
        
        self.init_table(self.ui.table_1, self.points_set_1[0], self.points_set_1[1])
        self.init_table(self.ui.table_2, self.points_set_2[0], self.points_set_2[1])
        self.table_1_rows_count = self.ui.table_1.rowCount()
        self.table_2_rows_count = self.ui.table_2.rowCount()
        
        self.selected_table_number = 1
        self.ui.set_button_1.setChecked(True)

        self.point_add_dialog = PointDialog()

        self.add_functions_connection()
        
    def init_plot(self):
        self.plot = self.figure.add_subplot(111)
        self.plot.margins(0.1)
        self.plot.set_aspect('auto')
        
        if self.show_axes:
            self.plot.set_axis_on()
        else:
            self.plot.set_axis_off()
    
    def label_points(self, points_list):
        indent = (self.max_x_cord - self.min_x_cord) / 80       # константа 80 подобрана экспериментально
        for x, y in zip(*points_list):
            self.plot.text(x + indent, y, f"({x}, {y})", fontsize=plot_fontsize)

    def init_table(self, table: QTableWidget, x_cords: list, y_cords: list):
        table.setRowCount(len(x_cords))
        table.setColumnCount(2)

        table.setHorizontalHeaderLabels(("X", "Y"))

        for column_index in range(columns_count):
            table.setColumnWidth(column_index, int(table.width() * 0.9 / columns_count))

        for row_index in range(table.rowCount()):
            table.setItem(row_index, 0, QTableWidgetItem(str(x_cords[row_index])))
            table.setItem(row_index, 1, QTableWidgetItem(str(y_cords[row_index])))

        table.resizeRowsToContents()
    
    def update_plot(self, points_list_1, points_list_2):
        self.figure.clear()

        self.init_plot()
        self.plot.scatter(points_list_1[0], points_list_1[1], s=points_size, c=[points_color_1])
        self.plot.scatter(points_list_2[0], points_list_2[1], s=points_size, c=[points_color_2])

        if self.circles_to_draw_dict is None or not self.figures_drawn:
            # если не найдены фигуры для рисования или же они не должны быть нарисованы 
            # (при нажатии кнопки "очистить" вызывается метод figures_clear который переводит figures_drawn в False)
            pass
        else:
            self.draw_figures()

        if self.show_point_labels:
            self.label_points(points_list_1)
            self.label_points(points_list_2)

        self.canvas.draw()

    def get_data_from_table(self, table: QTableWidget):
        updated_data = [[], []]
        
        for row_index in range(table.rowCount()):
            try:
                x = float(table.item(row_index, 0).text())
                y = float(table.item(row_index, 1).text())
            except ValueError:
                pass
            else:
                updated_data[0].append(x)
                updated_data[1].append(y)

        return updated_data
    
    def table_1_changed(self):
        self.changed_table_index = 1
    
    def table_2_changed(self):
        self.changed_table_index = 2
    
    def table_1_selected(self):
        self.selected_table_number = 1
    
    def table_2_selected(self):
        self.selected_table_number = 2

    def update_points_from_tables(self, item: QTableWidgetItem):
        if self.changed_table_index == 1:
            if item.row() >= self.table_1_rows_count:
                return
        elif self.changed_table_index == 2:
            if item.row() >= self.table_2_rows_count:
                return

        try:
            float(item.text())
        except ValueError:
            self.show_message_box(1)
            if self.changed_table_index == 1:
                item.setText(str(self.points_set_1[item.column()][item.row()]))
            elif self.changed_table_index == 2:
                item.setText(str(self.points_set_2[item.column()][item.row()]))
        else:
            if self.changed_table_index == 1:
                self.points_set_1 = self.get_data_from_table(self.ui.table_1)
            elif self.changed_table_index == 2:
                self.points_set_2 = self.get_data_from_table(self.ui.table_2)
            
            self.new_changes = True

            self.update_plot(self.points_set_1, self.points_set_2)
    
    def update_points(self):
        if self.selected_table_number == 1:
            self.points_set_1 = self.get_data_from_table(self.ui.table_1)
        elif self.selected_table_number == 2:
            self.points_set_2 = self.get_data_from_table(self.ui.table_2)

        self.new_changes = True

        self.update_plot(self.points_set_1, self.points_set_2)

    def show_add_point_dialog(self):
        self.point_add_dialog.show()
    
    def add_point(self):
        if self.selected_table_number == 1:
            row_index = self.ui.table_1.rowCount()
            self.ui.table_1.setRowCount(row_index + 1)

            self.ui.table_1.setItem(row_index, 0, QTableWidgetItem(str(self.point_add_dialog.x_value)))
            self.ui.table_1.setItem(row_index, 1, QTableWidgetItem(str(self.point_add_dialog.y_value)))

            self.table_1_rows_count = row_index + 1
            
        elif self.selected_table_number == 2:
            row_index = self.ui.table_2.rowCount()
            self.ui.table_2.setRowCount(row_index + 1)

            self.ui.table_2.setItem(row_index, 0, QTableWidgetItem(str(self.point_add_dialog.x_value)))
            self.ui.table_2.setItem(row_index, 1, QTableWidgetItem(str(self.point_add_dialog.y_value)))
            
            self.table_2_rows_count = row_index + 1

        self.update_points()
    
    def del_point(self):
        if self.selected_table_number == 1:
            selected_row = self.ui.table_1.currentRow()
            if selected_row >= 0:
                self.ui.table_1.removeRow(selected_row)
                self.ui.table_1.setCurrentCell(-1, -1)
                self.table_1_rows_count -= 1
                self.update_points()

        elif self.selected_table_number == 2:
            selected_row = self.ui.table_2.currentRow()
            if selected_row >= 0:
                self.ui.table_2.removeRow(selected_row)
                self.ui.table_2.setCurrentCell(-1, -1)
                self.table_2_rows_count -= 1
                self.update_points()
    
    def del_all_points(self):
        if self.selected_table_number == 1:
            self.ui.table_1.clearContents()
            self.ui.table_1.setRowCount(0)
            self.table_1_rows_count = 0

            self.update_points()

        elif self.selected_table_number == 2:
            self.ui.table_2.clearContents()
            self.ui.table_2.setRowCount(0)
            self.table_2_rows_count = 0

            self.update_points()
    
    def set_axes_visible(self):
        state = int(self.ui.axes_visibility_check.checkState())
        if state == 2:
            self.show_axes = True
            self.plot.set_axis_on()
            self.canvas.draw()
        elif state == 0:
            self.show_axes = False
            self.plot.set_axis_off()
            self.canvas.draw()
            
    def set_cords_visible(self):
        state = int(self.ui.cords_visibility_check.checkState())
        if state == 2:
            self.show_point_labels = True
            self.update_plot(self.points_set_1, self.points_set_2)
        elif state == 0:
            self.show_point_labels = False
            self.update_plot(self.points_set_1, self.points_set_2)
    
    def draw_circle(self, circle_params: tuple, color: str):
        circle = plt.Circle(circle_params[0], circle_params[1], edgecolor=color, fill=False)

        self.plot.add_artist(circle)
    
    def draw_line(self, cords: tuple, color: str):
        new_cords = [[cords[0][0], cords[1][0]], [cords[0][1], cords[1][1]]]
        line = Line2D(new_cords[0], new_cords[1], color=color)

        self.plot.add_line(line)
    
    def scale_axes_for_circles(self, circles_list: list):
        x_min, x_max = self.plot.get_xlim()
        y_min, y_max = self.plot.get_ylim()
            
        for circle in circles_list:
            x_min, x_max = min(x_min, circle[0][0] - circle[1]), max(x_max, circle[0][0] + circle[1])
            y_min, y_max = min(y_min, circle[0][1] - circle[1]), max(y_max, circle[0][1] + circle[1])

        x_min, x_max = round(x_min, calc_accuracy), round(x_max, calc_accuracy)
        y_min, y_max = round(y_min, calc_accuracy), round(y_max, calc_accuracy)
        axes_len = round(max(x_max - x_min, y_max - y_min), calc_accuracy)

        if abs(axes_len - self.prev_axes_len) > eps:
            x_min -= axes_len * 0.06
            y_min -= axes_len * 0.06
            axes_len *= 1.12
            self.prev_axes_len = axes_len

            self.plot.set_xlim(x_min, x_min + axes_len)
            self.plot.set_ylim(y_min, y_min + axes_len)

            self.canvas.draw()

    def find_best_circles(self):
        if self.new_changes:
            best_circles_dict = find_best_circles_params(self.points_set_1, self.points_set_2)
            if best_circles_dict is None:
                self.show_message_box(2)
            else:
                self.circles_to_draw_dict = best_circles_dict
                self.figures_drawn = True

                self.update_plot(self.points_set_1, self.points_set_2)
                self.new_changes = False

    def draw_figures(self):
        if self.circles_to_draw_dict is None:
            pass
        else:
            best_circles_dict = self.circles_to_draw_dict
            self.figures_drawn = True
            # получение всех необходимых параметров в удобном виде
            circle_center_1 = best_circles_dict['circle_1'][0]
            circle_center_2 = best_circles_dict['circle_2'][0]

            touch_points_1 = best_circles_dict['points_1']
            touch_points_2 = best_circles_dict['points_2']

            # изображение фигур на графике
            self.draw_circle(best_circles_dict['circle_1'], self.circle_color_1)   # первая окружность
            self.draw_line((circle_center_1, touch_points_1[0]), self.lines_color) # радиус к точке касания 1
            self.draw_line((circle_center_1, touch_points_2[0]), self.lines_color) # радиус к точке касания 2

            self.draw_circle(best_circles_dict['circle_2'], self.circle_color_2)   # вторая окужность
            self.draw_line((circle_center_2, touch_points_1[1]), self.lines_color) # радиус к точке касания 1
            self.draw_line((circle_center_2, touch_points_2[1]), self.lines_color) # радиус к точке касания 2

            self.draw_line((touch_points_1[0], touch_points_1[1]), self.lines_color) # первая общая касательная
            self.draw_line((touch_points_2[0], touch_points_2[1]), self.lines_color) # вторая общая касательная

            # отрисовка и обновление масштаба
            self.scale_axes_for_circles((best_circles_dict['circle_1'], best_circles_dict['circle_2']))
            self.canvas.draw()
        
    def clear_figures(self):
        if self.figures_drawn:
            self.figures_drawn = False
            self.new_changes = True

            self.update_plot(self.points_set_1, self.points_set_2)

    def show_message_box(self, message_code):
        ans_window = QMessageBox()
        text = "None"

        if message_code == 1:
            text = "Введены некорректные данные!"
            ans_window.setIcon(QMessageBox.Warning)
        elif message_code == 2:
            text = "При заданных точках построение невозможно!"
            ans_window.setIcon(QMessageBox.Warning)

        ans_window.setText(text)
        ans_window.exec_()

    def add_functions_connection(self):
        self.ui.table_1.itemChanged.connect(self.table_1_changed)
        self.ui.table_1.itemChanged.connect(self.update_points_from_tables)
        
        self.ui.table_2.itemChanged.connect(self.table_2_changed)
        self.ui.table_2.itemChanged.connect(self.update_points_from_tables)

        self.ui.add_button.clicked.connect(self.show_add_point_dialog)
        self.point_add_dialog.ui.button_box.accepted.connect(self.add_point)
        self.ui.del_button.clicked.connect(self.del_point)
        self.ui.del_all_button.clicked.connect(self.del_all_points)
        self.ui.clear_button.clicked.connect(self.clear_figures)

        self.ui.set_button_1.clicked.connect(self.table_1_selected)
        self.ui.set_button_2.clicked.connect(self.table_2_selected)

        self.ui.calc_button.clicked.connect(self.find_best_circles)

        self.ui.axes_visibility_check.clicked.connect(self.set_axes_visible)
        self.ui.cords_visibility_check.clicked.connect(self.set_cords_visible)


def input_start_points():
    points_set_1 = list()
    points_set_2 = list()

    set_1_size = size_input(1)
    print()
    points_list_1 = points_input(set_1_size)
    print("\n--- Координаты точек 1-го множества введены успешно! ---\n")

    set_2_size = size_input(2)
    print()
    points_list_2 = points_input(set_2_size)
    print("\n--- Координаты точек 2-го множества введены успешно! ---\n")

    return points_list_1, points_list_2
    

def size_input(set_number):
    while True:
        try:
            set_size = int(input(f"Введите кол-во точек в {set_number}-ом множестве: "))
        except ValueError:
            print("\nВведено некорректное значение!\n")
        else:
            if set_size <= 0:
                print("\nКол-во точек не может быть отрицательным!\n")
            else:
                return set_size


def points_input(points_count):
    points_list = [[], []]

    for i in range(1, points_count + 1):
        while True:
            try:
                x, y = map(float, input(f"Введите координаты {i}-й точки (x и y через пробел): ").split())
            except ValueError:
                print("\nКоординаты введены некорректно!\n")
            else:
                break
        
        points_list[0].append(x)
        points_list[1].append(y)

    return points_list


def get_test_points():
    set_1 = [[-50, -100, -20], [70, 30, 10]]
    set_2 = [[1, 4, 7], [20, 22, 10]]

    return set_1, set_2


class PointDialog(QDialog):
    def __init__(self):
        super(PointDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.input_regexp = QRegExpValidator(QRegExp(cord_regexp))
        self.ui.x_input_line.setValidator(self.input_regexp)
        self.ui.y_input_line.setValidator(self.input_regexp)

        self.ui.button_box.accepted.connect(self.ok_clicked)
        self.ui.button_box.rejected.connect(self.cancel_clicked)

        self.test = 1
    
    def ok_clicked(self):
        self.x_value = float(self.ui.x_input_line.text())
        self.y_value = float(self.ui.y_input_line.text())

        self.ui.x_input_line.setText("")
        self.ui.y_input_line.setText("")
    
    def cancel_clicked(self):
        self.ui.x_input_line.setText("")
        self.ui.y_input_line.setText("")


if __name__ == "__main__":
    sets_tuple = get_test_points()
    
    app = QApplication(sys.argv)
    
    calc_window = MainApp(first_points_set=sets_tuple[0], second_points_set=sets_tuple[1])
    calc_window.show()

    sys.exit(app.exec())

