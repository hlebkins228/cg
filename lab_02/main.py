from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QKeySequence, QShortcut, QRegularExpressionValidator

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import sys

from main_window import Ui_MainWindow
from config import figure_color, float_regexp, FigureCache, cache_size, accuracy, start_figure_params
from config import x_lim_r, x_lim_l, y_lim_r, y_lim_l

from math_functions import *


class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()

        self.below_figure_part = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.fields_list = (
            self.ui.scale_x_field, self.ui.scale_y_field, self.ui.scale_coefficient_x_field, self.ui.scale_coefficient_y_field, self.ui.shift_x_field, self.ui.shift_y_field,
            self.ui.rotate_angle_field, self.ui.rotate_x_field, self.ui.rotate_y_field
                       )

        self.init_start_figure_params()

        self.color = figure_color
        self.accuracy = accuracy

        self.cache = list()

        self.plot_layout = QVBoxLayout(self.ui.graphics_widget)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.plot_layout.addWidget(self.canvas)

        self.input_regexp = QRegularExpressionValidator(QRegularExpression(float_regexp))
        self.init_input_fields()

        self.undo_hotkey = QShortcut(QKeySequence("Ctrl+Z"), self)

        self.update_plot()
        self.add_functions_connection()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.check_event_geometry(event):
            for field in self.fields_list:
                field.clearFocus()

        super().mousePressEvent(event)

    def check_event_geometry(self, event):
        for field in self.fields_list:
            if field.geometry().contains(event.pos()):
                return False

        return True

    def init_start_figure_params(self):
        self.below_figure_part = start_figure_params['below_part'].copy()

        self.bottom_figure_part = start_figure_params['bottom_part'].copy()

        self.semicircle_x_list = start_figure_params['semicircle_x'].copy()
        self.semicircle_y_list = start_figure_params['semicircle_y'].copy()

        self.small_circle_x_list = start_figure_params['small_circle_x'].copy()
        self.small_circle_y_list = start_figure_params['small_circle_y'].copy()
        self.big_circle_x_list = start_figure_params['big_circle_x'].copy()
        self.big_circle_y_list = start_figure_params['big_circle_y'].copy()

    def init_input_fields(self):
        for field in self.fields_list:
            field.setValidator(self.input_regexp)
            field.setText('0')

        self.ui.scale_coefficient_x_field.setText('1')
        self.ui.scale_coefficient_y_field.setText('1')

    def init_plot(self):
        self.plot = self.figure.add_subplot(111)
        self.plot.margins(0.1)
        self.plot.set_aspect('auto')
        self.plot.set_xlim(x_lim_l, x_lim_r)
        self.plot.set_ylim(y_lim_l, y_lim_r)
        self.plot.set_axis_on()

    def update_plot(self):
        def __draw_figure_part(figure_part: dict, plot, color: str):
            line_1 = Line2D((figure_part['x'][0], figure_part['x'][5]), (figure_part['y'][0], figure_part['y'][5]), color=color)

            wing_1 = Line2D((figure_part['x'][1], figure_part['x'][2]), (figure_part['y'][1], figure_part['y'][2]), color=color)
            wing_2 = Line2D((figure_part['x'][2], figure_part['x'][3]), (figure_part['y'][2], figure_part['y'][3]), color=color)
            wing_3 = Line2D((figure_part['x'][3], figure_part['x'][4]), (figure_part['y'][3], figure_part['y'][4]), color=color)

            line_2 = Line2D((figure_part['x'][-2], figure_part['x'][-1]), (figure_part['y'][-2], figure_part['y'][-1]), color=color)

            plot.add_line(line_1)
            plot.add_line(wing_1)
            plot.add_line(wing_2)
            plot.add_line(wing_3)
            plot.add_line(line_2)

        def __draw_circles(plot, color: str):
            plot.plot(self.semicircle_x_list, self.semicircle_y_list, color=color)
            plot.plot(self.small_circle_x_list, self.small_circle_y_list, color=color)
            plot.plot(self.big_circle_x_list, self.big_circle_y_list, color=color)

        self.figure.clear()
        self.init_plot()

        __draw_figure_part(self.below_figure_part, self.plot, self.color)
        __draw_figure_part(self.bottom_figure_part, self.plot, self.color)
        __draw_circles(self.plot, self.color)

        self.canvas.draw()

    def save_state(self):
        if len(self.cache) >= cache_size:
            self.cache.pop(0)

        current_state = FigureCache(
            below_part=self.below_figure_part.copy(), bottom_part=self.bottom_figure_part.copy(),
            semicircle_x=self.semicircle_x_list.copy(),
            semicircle_y=self.semicircle_y_list.copy(), small_circle_x=self.small_circle_x_list.copy(),
            small_circle_y=self.small_circle_y_list.copy(), big_circle_x=self.big_circle_x_list.copy(),
            big_circle_y=self.big_circle_y_list.copy()
            )

        self.cache.append(current_state)

    def load_state(self):
        if len(self.cache) > 0:
            last_state = self.cache.pop()

            self.below_figure_part = last_state['below_part']
            self.bottom_figure_part = last_state['bottom_part']
            self.semicircle_x_list = last_state['semicircle_x']
            self.semicircle_y_list = last_state['semicircle_y']
            self.small_circle_x_list = last_state['small_circle_x']
            self.small_circle_y_list = last_state['small_circle_y']
            self.big_circle_x_list = last_state['big_circle_x']
            self.big_circle_y_list = last_state['big_circle_y']

            self.update_plot()

    def rotate_button_clicked(self):
        self.rotate_x_field_defult()
        self.rotate_y_field_defult()
        self.rotate_angle_field_defult()

        try:
            rotate_point_x = float(self.ui.rotate_x_field.text())
            rotate_point_y = float(self.ui.rotate_y_field.text())
            rotate_angle = float(self.ui.rotate_angle_field.text())
        except ValueError:
            self.show_message_box(4)
            return

        self.save_state()

        self.below_figure_part['x'], self.below_figure_part['y'] = rotate(self.below_figure_part['x'], self.below_figure_part['y'], rotate_point_x, rotate_point_y, rotate_angle)
        self.bottom_figure_part['x'], self.bottom_figure_part['y'] = rotate(self.bottom_figure_part['x'], self.bottom_figure_part['y'], rotate_point_x, rotate_point_y, rotate_angle)

        self.semicircle_x_list, self.semicircle_y_list = rotate(self.semicircle_x_list, self.semicircle_y_list, rotate_point_x, rotate_point_y, rotate_angle)

        self.small_circle_x_list, self.small_circle_y_list = rotate(self.small_circle_x_list, self.small_circle_y_list, rotate_point_x, rotate_point_y, rotate_angle)
        self.big_circle_x_list, self.big_circle_y_list = rotate(self.big_circle_x_list, self.big_circle_y_list, rotate_point_x, rotate_point_y, rotate_angle)

        self.update_plot()

    def shift_button_clicked(self):
        self.shift_x_field_defult()
        self.shift_y_field_defult()

        try:
            shift_x = float(self.ui.shift_x_field.text())
            shift_y = float(self.ui.shift_y_field.text())
        except ValueError:
            self.show_message_box(4)
            return

        self.save_state()

        self.below_figure_part['x'], self.below_figure_part['y'] = move(self.below_figure_part['x'], self.below_figure_part['y'], shift_x, shift_y)
        self.bottom_figure_part['x'], self.bottom_figure_part['y'] = move(self.bottom_figure_part['x'], self.bottom_figure_part['y'], shift_x, shift_y)

        self.semicircle_x_list, self.semicircle_y_list = move(self.semicircle_x_list, self.semicircle_y_list, shift_x, shift_y)

        self.small_circle_x_list, self.small_circle_y_list = move(self.small_circle_x_list, self.small_circle_y_list, shift_x, shift_y)
        self.big_circle_x_list, self.big_circle_y_list = move(self.big_circle_x_list, self.big_circle_y_list, shift_x, shift_y)

        self.update_plot()

    def scale_button_clicked(self):
        self.scale_x_field_defult()
        self.scale_y_field_defult()
        self.scale_kx_field_defult()
        self.scale_ky_field_defult()

        try:
            scale_x = float(self.ui.scale_x_field.text())
            scale_y = float(self.ui.scale_y_field.text())
            scale_kx = float(self.ui.scale_coefficient_x_field.text())
            scale_ky = float(self.ui.scale_coefficient_y_field.text())
        except ValueError:
            self.show_message_box(4)
            return

        if scale_kx == 0:
            self.show_message_box(1)
        elif scale_ky == 0:
            self.show_message_box(2)
        else:
            self.save_state()

            self.below_figure_part['x'], self.below_figure_part['y'] = scale(self.below_figure_part['x'], self.below_figure_part['y'], scale_x, scale_y, scale_kx, scale_ky)
            self.bottom_figure_part['x'], self.bottom_figure_part['y'] = scale(self.bottom_figure_part['x'], self.bottom_figure_part['y'], scale_x, scale_y, scale_kx, scale_ky)

            self.semicircle_x_list, self.semicircle_y_list = scale(self.semicircle_x_list, self.semicircle_y_list, scale_x, scale_y, scale_kx, scale_ky)

            self.small_circle_x_list, self.small_circle_y_list = scale(self.small_circle_x_list, self.small_circle_y_list,  scale_x, scale_y, scale_kx, scale_ky)
            self.big_circle_x_list, self.big_circle_y_list = scale(self.big_circle_x_list, self.big_circle_y_list, scale_x, scale_y, scale_kx, scale_ky)

            self.update_plot()

    def draw_figure_button_clicked(self):
        self.save_state()
        self.init_start_figure_params()
        self.update_plot()

    def rotate_x_field_defult(self):
        if not self.ui.rotate_x_field.text():
            self.ui.rotate_x_field.setText('0')

    def rotate_y_field_defult(self):
        if not self.ui.rotate_y_field.text():
            self.ui.rotate_y_field.setText('0')

    def rotate_angle_field_defult(self):
        if not self.ui.rotate_angle_field.text():
            self.ui.rotate_angle_field.setText('0')

    def shift_x_field_defult(self):
        if not self.ui.shift_x_field.text():
            self.ui.shift_x_field.setText('0')

    def shift_y_field_defult(self):
        if not self.ui.shift_y_field.text():
            self.ui.shift_y_field.setText('0')

    def scale_x_field_defult(self):
        if not self.ui.scale_x_field.text():
            self.ui.scale_x_field.setText('0')

    def scale_y_field_defult(self):
        if not self.ui.scale_y_field.text():
            self.ui.scale_y_field.setText('0')

    def scale_kx_field_defult(self):
        if not self.ui.scale_coefficient_x_field.text():
            self.ui.scale_coefficient_x_field.setText('1')

    def scale_ky_field_defult(self):
        if not self.ui.scale_coefficient_y_field.text():
            self.ui.scale_coefficient_y_field.setText('1')

    def info_button_clicked(self):
        self.show_message_box(3)

    def show_message_box(self, message_code):
        ans_window = QMessageBox()
        text = "None"

        if message_code == 1:
            text = "Коэффициент масштабирования по оси OX\n не может быть равен 0!"
        elif message_code == 2:
            text = "Коэффициент масштабирования по оси OY\n не может быть равен 0!"
        elif message_code == 3:
            text = "<b>Формулировка задачи:</b><br>Выполнить построение искомой фигуры, реализовать функции поворота,\
                масштабирования и переноса заданной фигуры<br><br><b>Ctrl+Z</b> - шаг назад"
        elif message_code == 4:
            text = "Данные введены некорректно!"

        ans_window.setText(text)
        ans_window.exec()

    def add_functions_connection(self):
        self.ui.info_button.clicked.connect(self.info_button_clicked)
        self.ui.rotate_button.clicked.connect(self.rotate_button_clicked)
        self.ui.shift_button.clicked.connect(self.shift_button_clicked)
        self.ui.scale_button.clicked.connect(self.scale_button_clicked)
        self.ui.draw_figure_button.clicked.connect(self.draw_figure_button_clicked)
        self.undo_hotkey.activated.connect(self.load_state)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    calc_window = MainApp()
    calc_window.show()

    sys.exit(app.exec())

