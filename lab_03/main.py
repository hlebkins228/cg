from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QColorDialog
from PyQt6.QtWidgets import QMessageBox

from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QLine
from PyQt6.QtGui import QColor, QPixmap, QPainter, QPen

import numpy as np

import matplotlib.pyplot as plt

import sys
import time

from config import *

from main_window import Ui_MainWindow


class MainApp(QMainWindow):
    def __init__(self, screen_color: list, line_color: list, specter_color: list,
                 pixmap_size_x: int, pixmap_size_y: int) -> None:
        super(MainApp, self).__init__()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        # already drawn figures
        self.drawn_figures = list()  # List[List[type: int, function, pos: dict, color: QColor]]

        # set up pixmap and painter
        self.pixmap_width = pixmap_size_x
        self.pixmap_height = pixmap_size_y
        self.pixmap = QPixmap(self.pixmap_width, self.pixmap_height)
        self.painter = QPainter(self.pixmap)

        # set up validator for all fields
        self.validator = QIntValidator()

        # set up some widgets
        self.configurate_widgets()
        self.change_labels_style_to_default()

        # set up init color buttons and color dialog
        self.screen_button_color = self.get_color_object_with_rgb(screen_color)
        self.line_button_color = self.get_color_object_with_rgb(line_color)
        self.specter_button_color = self.get_color_object_with_rgb(specter_color)
        self.set_default_color_buttons()
        self.update_pixmap_color()
        self.draw_pixmap()
        self.color_dialog = QColorDialog()

        self.pen = QPen(self.screen_button_color, POINT_SIZE)
        self.painter.setPen(self.pen)

        # set up init program state
        self.select_line_mode()
        self.set_validators_for_input_fields()
        self.ui.cda_button.setChecked(True)
        self.add_functions_connection()

        self.drawn_state = False

        self.results_plot = plt
        self.figure_size = (20, 15)
        self.plot_font = {'family': 'Calibri', 'color': 'black', 'weight': 'normal', 'size': 20}

    @staticmethod
    def normalize_pos(target_widget: QWidget, old_parent_widget: QWidget) -> None:
        offset_x = old_parent_widget.x() + target_widget.x()
        offset_y = old_parent_widget.y() + target_widget.y()

        target_widget.move(offset_x, offset_y)

    @staticmethod
    def change_parent(target_widget: QWidget, new_parent_widget: QWidget) -> None:
        target_widget.setParent(new_parent_widget)

    @staticmethod
    def get_color_object_with_rgb(rgb_color: list) -> QColor:
        return QColor(rgb_color[0], rgb_color[1], rgb_color[2])

    @staticmethod
    def get_button_css_style(color: QColor) -> str:
        k = 0.7
        rgb_color = f"rgb({color.red()}, {color.green()}, {color.blue()})"
        rgb_color_pressed = f"rgb({int(color.red() * k)}, {int(color.green() * k)}, {int(color.blue() * k)})"

        color_button_css = ('QPushButton\n'
                            '{\n'
                            '	border-radius: 4px;\n'
                            '	border: 2px solid rgb(110, 105, 100);\n'
                            f'	background-color: {rgb_color};\n'
                            '}\n\n'
                            'QPushButton:pressed\n'
                            '{\n'
                            f'background-color: {rgb_color_pressed};\n'
                            '}\n')

        return color_button_css

    def update_pixmap_color(self) -> None:
        self.pixmap.fill(self.screen_button_color)

    def draw_pixmap(self) -> None:
        self.ui.pixmap_label.setPixmap(self.pixmap)

    def set_button_css_style(self, button: QPushButton, color: QColor) -> None:
        css_code = self.get_button_css_style(color)
        button.setStyleSheet(css_code)

    def choose_color(self) -> QColor | None:
        color = self.color_dialog.getColor()
        if color.isValid():
            return color
        else:
            return None

    def set_default_color_buttons(self) -> None:
        self.set_button_css_style(self.ui.screen_color_button, self.screen_button_color)
        self.set_button_css_style(self.ui.line_color_button, self.line_button_color)
        self.set_button_css_style(self.ui.specter_color_button, self.specter_button_color)

    def detach_widget_from_old_parent(self, target_widget: QWidget, old_parent: QWidget, new_parent: QWidget) -> None:
        self.change_parent(target_widget, new_parent)
        self.normalize_pos(target_widget, old_parent)

    def configurate_widgets(self) -> None:  # special function for detach needed objects from QFrames and move it
        old_parent = self.ui.line_frame
        self.detach_widget_from_old_parent(self.ui.specter_frame, old_parent, self.ui.centralwidget)
        self.detach_widget_from_old_parent(self.ui.specter_mode_button, old_parent, self.ui.centralwidget)
        self.detach_widget_from_old_parent(self.ui.line_mode_button, old_parent, self.ui.centralwidget)

    def change_labels_style_to_default(self) -> None:
        self.ui.label_1.setStyleSheet('QLabel { border: none; }')
        self.ui.label_2.setStyleSheet('QLabel { border: none; }')
        self.ui.label_3.setStyleSheet('QLabel { border: none; }')
        self.ui.label_4.setStyleSheet('QLabel { border: none; }')
        self.ui.label_5.setStyleSheet('QLabel { border: none; }')
        self.ui.label_6.setStyleSheet('QLabel { border: none; }')
        self.ui.label_7.setStyleSheet('QLabel { border: none; }')
        self.ui.label_8.setStyleSheet('QLabel { border: none; }')
        self.ui.label_9.setStyleSheet('QLabel { border: none; }')
        self.ui.label_10.setStyleSheet('QLabel { border: none; }')
        self.ui.label_11.setStyleSheet('QLabel { border: none; }')
        self.ui.label_12.setStyleSheet('QLabel { border: none; }')
        self.ui.label_13.setStyleSheet('QLabel { border: none; }')
        self.ui.label_14.setStyleSheet('QLabel { border: none; }')
        self.ui.label_15.setStyleSheet('QLabel { border: none; }')
        self.ui.label_16.setStyleSheet('QLabel { border: none; }')
        self.ui.label_17.setStyleSheet('QLabel { border: none; }')

    def set_validators_for_input_fields(self) -> None:
        self.ui.line_start_x_field.setValidator(self.validator)
        self.ui.line_start_y_field.setValidator(self.validator)
        self.ui.line_end_x_field.setValidator(self.validator)
        self.ui.line_end_y_field.setValidator(self.validator)
        self.ui.specter_center_x_field.setValidator(self.validator)
        self.ui.specter_center_y_field.setValidator(self.validator)
        self.ui.specter_radius_field.setValidator(self.validator)
        self.ui.specter_angle_field.setValidator(self.validator)

    def select_line_mode(self) -> None:
        # select line mode button, show line window and line title
        self.ui.line_mode_button.setChecked(True)
        self.ui.line_frame.setVisible(True)
        self.ui.line_label.setVisible(True)

        # unselect specter mode button (if it already selected), hide specter window and specter title
        self.ui.specter_mode_button.setChecked(False)
        self.ui.specter_frame.setVisible(False)
        self.ui.specter_label.setVisible(False)

    def select_specter_mode(self) -> None:
        # select specter mode button, show specter window and specter label
        self.ui.specter_mode_button.setChecked(True)
        self.ui.specter_frame.setVisible(True)
        self.ui.specter_label.setVisible(True)

        # unselect line mode button (if it already selected), hide line window and line label
        self.ui.line_mode_button.setChecked(False)
        self.ui.line_frame.setVisible(False)
        self.ui.line_label.setVisible(False)

    def set_screen_color(self) -> None:
        color = self.choose_color()
        if color:
            self.screen_button_color = color
            self.set_button_css_style(self.ui.screen_color_button, color)

            self.update_pixmap_color()
            self.draw_all_previous_figures()
            self.draw_pixmap()

    def set_line_color(self) -> None:
        color = self.choose_color()
        if color:
            self.line_button_color = color
            self.set_button_css_style(self.ui.line_color_button, color)

    def update_pen(self, color: QColor, i: float = 1) -> None:
        color.setAlpha(int(255 * i))
        self.pen = QPen(color, POINT_SIZE)
        self.painter.setPen(self.pen)

    def set_specter_color(self) -> None:
        color = self.choose_color()
        if color:
            self.specter_button_color = color
            self.set_button_css_style(self.ui.specter_color_button, color)

    def draw_point(self, x: int, y: int) -> None:
        if type(x) is int and type(y) is int and x > 0 and y > 0:
            self.painter.drawPoint(x, y)

    def line_draw_cda(self, cords: Line, color: QColor) -> None:
        self.__cda_draw_line_function(cords, color)

    def specter_draw_cda(self, cords: Specter, color: QColor) -> None:
        self.__specter_draw(cords, color, self.__cda_draw_line_function)

    def line_draw_bresenham_float(self, cords: Line, color: QColor) -> None:
        self.__bresenham_float_draw_line_function(cords, color)

    def specter_draw_bresenham_float(self, cords: Specter, color: QColor) -> None:
        self.__specter_draw(cords, color, self.__bresenham_float_draw_line_function)

    def line_draw_bresenham_int(self, cords: Line, color: QColor) -> None:
        self.__bresenham_int_draw_line_function(cords, color)

    def specter_draw_bresenham_int(self, cords: Specter, color: QColor) -> None:
        self.__specter_draw(cords, color, self.__bresenham_int_draw_line_function)

    def line_draw_bresenham_without_gradation(self, cords: Line, color: QColor) -> None:
        self.__bresenham_without_gradation_draw_line_function(cords, color)

    def specter_draw_bresenham_without_gradation(self, cords: Specter, color: QColor) -> None:
        self.__specter_draw(cords, color, self.__bresenham_without_gradation_draw_line_function)

    def line_draw_vu(self, cords: Line, color: QColor) -> None:
        self.__vu_draw_line_function(cords, color)

    def specter_draw_vu(self, cords: Specter, color: QColor) -> None:
        self.__specter_draw(cords, color, self.__vu_draw_line_function)

    def line_draw_library(self, cords: Line, color: QColor) -> None:
        self.__library_draw_line_function(cords, color)

    def specter_draw_library(self, cords: Specter, color: QColor) -> None:
        self.__specter_draw(cords, color, self.__library_draw_line_function)

    @staticmethod
    def __specter_draw(cords: Specter, color: QColor, draw_function, end_angle: int = 360) -> list:
        x_0 = cords['center_x']
        y_0 = cords['center_y']
        radius = cords['radius']

        steps_count = list()
        for current_angle in np.arange(0, np.deg2rad(end_angle + 1), np.deg2rad(cords['angle'])):
            x = x_0 + np.cos(current_angle) * radius
            y = y_0 + np.sin(current_angle) * radius

            line_cords = Line(start_x=round(x_0), start_y=round(y_0), end_x=round(x), end_y=round(y))

            steps_count.append(draw_function(line_cords, color))

        return steps_count

    def __cda_draw_line_function(self, cords: Line, color: QColor) -> int:
        self.update_pen(color)

        start_x = cords['start_x']
        start_y = cords['start_y']
        end_x = cords['end_x']
        end_y = cords['end_y']

        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)

        if dx >= dy:
            if start_x > end_x:
                start_x, end_x = end_x, start_x
                start_y, end_y = end_y, start_y

            delta_x = 1
            if dx != 0:
                delta_y = dy / dx if start_y <= end_y else -(dy / dx)
            else:
                delta_y = 0

            current_x = start_x
            current_y = start_y
            while current_x <= end_x:
                self.draw_point(round(current_x), round(current_y))
                current_x += delta_x
                current_y += delta_y

            return dy
        else:
            if start_y > end_y:
                start_x, end_x = end_x, start_x
                start_y, end_y = end_y, start_y

            delta_y = 1
            if dy != 0:
                delta_x = dx / dy if start_x <= end_x else -(dx / dy)
            else:
                delta_x = 0

            current_x = start_x
            current_y = start_y
            while current_y <= end_y:
                self.draw_point(round(current_x), round(current_y))
                current_x += delta_x
                current_y += delta_y

            return dx

    def __bresenham_int_draw_line_function(self, cords: Line, color: QColor) -> int:
        self.update_pen(color)

        start_x = cords['start_x']
        start_y = cords['start_y']
        end_x = cords['end_x']
        end_y = cords['end_y']

        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)

        if dx >= dy:
            e = 2 * dy - dx

            if start_x > end_x:
                start_x, end_x = end_x, start_x
                start_y, end_y = end_y, start_y

            current_x = start_x
            current_y = start_y
            delta_y = 1 if start_y <= end_y else -1
            while current_x <= end_x:
                self.draw_point(current_x, current_y)
                current_x += 1
                if e >= 0:
                    current_y += delta_y
                    e -= 2 * dx
                e += 2 * dy

            return dy
        else:
            e = 2 * dx - dy

            if start_y > end_y:
                start_x, end_x = end_x, start_x
                start_y, end_y = end_y, start_y

            current_x = start_x
            current_y = start_y
            delta_x = 1 if start_x <= end_x else -1
            while current_y <= end_y:
                self.draw_point(current_x, current_y)
                current_y += 1
                if e >= 0:
                    current_x += delta_x
                    e -= 2 * dy
                e += 2 * dx

            return dx

    def __bresenham_float_draw_line_function(self, cords: Line, color: QColor) -> int:
        self.update_pen(color)

        start_x = cords['start_x']
        start_y = cords['start_y']
        end_x = cords['end_x']
        end_y = cords['end_y']

        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)

        if dx >= dy:
            tg = dy / dx if dx != 0 else 0
            e = tg - 0.5

            if start_x > end_x:
                start_x, end_x = end_x, start_x
                start_y, end_y = end_y, start_y

            current_x = start_x
            current_y = start_y
            delta_y = 1 if start_y <= end_y else -1
            while current_x <= end_x:
                self.draw_point(current_x, current_y)
                current_x += 1
                if e >= 0:
                    current_y += delta_y
                    e -= 1
                e += tg

            return dy
        else:
            tg = dx / dy if dy != 0 else 0
            e = tg - 0.5

            if start_y > end_y:
                start_x, end_x = end_x, start_x
                start_y, end_y = end_y, start_y

            current_x = start_x
            current_y = start_y
            delta_x = 1 if start_x <= end_x else -1
            while current_y <= end_y:
                self.draw_point(current_x, current_y)
                current_y += 1
                if e >= 0:
                    current_x += delta_x
                    e -= 1
                e += tg

            return dx

    def __bresenham_without_gradation_draw_line_function(self, cords: Line, color: QColor) -> int:
        self.update_pen(color)

        start_x = cords['start_x']
        start_y = cords['start_y']
        end_x = cords['end_x']
        end_y = cords['end_y']

        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)

        if dx == 0 and dy == 0:
            self.draw_point(start_x, start_y)
            return 0

        if dx >= dy:
            i = 1
            m = i * dy / dx
            w = i - m
            e = i / 2

            if start_x > end_x:
                start_x, end_x = end_x, start_x
                start_y, end_y = end_y, start_y

            current_x = start_x
            current_y = start_y
            delta_y = 1 if start_y <= end_y else -1
            while current_x <= end_x:
                self.update_pen(color, i=e / i)
                self.draw_point(current_x, current_y)
                current_x += 1
                if e >= w:
                    current_y += delta_y
                    e -= w
                else:
                    e += m

            return dy
        else:
            i = 1
            m = i * dx / dy
            w = i - m
            e = i / 2

            if start_y > end_y:
                start_x, end_x = end_x, start_x
                start_y, end_y = end_y, start_y

            current_x = start_x
            current_y = start_y
            delta_x = 1 if start_x <= end_x else -1
            while current_y <= end_y:
                self.update_pen(color, i=e / i)
                self.draw_point(current_x, current_y)
                current_y += 1
                if e >= w:
                    current_x += delta_x
                    e -= w
                else:
                    e += m

            return dx

    def __vu_draw_line_function(self, cords: Line, color: QColor) -> int:
        self.update_pen(color)

        start_x = cords['start_x']
        start_y = cords['start_y']
        end_x = cords['end_x']
        end_y = cords['end_y']

        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)

        if dx == 0 and dy == 0:
            self.draw_point(start_x, start_y)
            return 0

        if dx >= dy:
            if start_x > end_x:
                start_x, end_x = end_x, start_x
                start_y, end_y = end_y, start_y

            tg = dy / dx
            tg = tg if start_y <= end_y else -tg
            inter = start_y
            for x in range(start_x, end_x + 1):
                self.update_pen(color, 1 - self.__float_part(inter))
                self.draw_point(x, int(inter))
                self.update_pen(color, self.__float_part(inter))
                self.draw_point(x, int(inter) + 1)
                inter += tg

            return dy
        else:
            if start_y > end_y:
                start_x, end_x = end_x, start_x
                start_y, end_y = end_y, start_y

            tg = dx / dy
            tg = tg if start_x <= end_x else -tg
            inter = start_x
            for y in range(start_y, end_y + 1):
                self.update_pen(color, 1 - self.__float_part(inter))
                self.draw_point(int(inter), y)
                self.update_pen(color, self.__float_part(inter))
                self.draw_point(int(inter) + 1, y)
                inter += tg

            return dx

    def __library_draw_line_function(self, cords: Line, color: QColor) -> None:
        self.update_pen(color)
        line = QLine(cords['start_x'], cords['start_y'], cords['end_x'], cords['end_y'])
        self.painter.drawLine(line)

    @staticmethod
    def __float_part(number: float) -> float:
        return number % 1

    @staticmethod
    def __get_algorithms_ru_names() -> list:
        names = [
            'Алгоритм ЦДА',
            'Алгоритм Брезенхема\n(вещественный)',
            'Алгоритм Брезенхема\n(целочисленный)',
            'Алгоритм Брезенхема\n(c устранением ступенчатости)',
            'Алгоритм Ву',
            'Библиотечная\nфункция'
        ]

        return names

    def __time_measurement(self, line_draw_function) -> float:
        specter_cords = MEASUREMENT_SPECTER_CORDS
        end_angle = MEASUREMENT_ANGLE

        start_time = time.time()
        self.__specter_draw(specter_cords, self.specter_button_color, line_draw_function, end_angle=end_angle)
        end_time = time.time()

        self.clear_screen_button_clicked()

        return (end_time - start_time) / end_angle * 1_000_000  # умножение на 1_000_000 для перевода в мкс

    def cda_time_measurement(self) -> float:
        return self.__time_measurement(self.__cda_draw_line_function)

    def bresenham_float_time_measurement(self) -> float:
        return self.__time_measurement(self.__bresenham_float_draw_line_function)

    def bresenham_int_time_measurement(self) -> float:
        return self.__time_measurement(self.__bresenham_int_draw_line_function)

    def bresenham_without_gradation_time_measurement(self) -> float:
        return self.__time_measurement(self.__bresenham_without_gradation_draw_line_function)

    def vu_time_measurement(self) -> float:
        return self.__time_measurement(self.__vu_draw_line_function)

    def library_time_measurement(self) -> float:
        return self.__time_measurement(self.__library_draw_line_function)

    def __get_time_measurement_dict(self) -> TimeResults:
        time_results = TimeResults(
            cda=self.cda_time_measurement(),
            bresenham_float=self.bresenham_float_time_measurement(),
            bresenham_int=self.bresenham_int_time_measurement(),
            bresenham_step=self.bresenham_without_gradation_time_measurement(),
            vu=self.vu_time_measurement(),
            library=self.library_time_measurement()
        )

        return time_results

    def __steps_measurement(self, line_draw_function) -> list:
        color = self.line_button_color

        specter_cords = MEASUREMENT_SPECTER_CORDS
        end_angle = MEASUREMENT_ANGLE

        result = self.__specter_draw(specter_cords, color, line_draw_function, end_angle=end_angle)

        self.clear_screen_button_clicked()

        return result

    def cda_steps_measurement(self) -> list:
        return self.__steps_measurement(self.__cda_draw_line_function)

    def bresenham_float_steps_measurement(self) -> list:
        return self.__steps_measurement(self.__bresenham_float_draw_line_function)

    def bresenham_int_steps_measurement(self) -> list:
        return self.__steps_measurement(self.__bresenham_int_draw_line_function)

    def bresenham_without_gradation_steps_measurement(self) -> list:
        return self.__steps_measurement(self.__bresenham_without_gradation_draw_line_function)

    def vu_steps_measurement(self) -> list:
        return self.__steps_measurement(self.__vu_draw_line_function)

    def __get_steps_measurement_dict(self) -> StepsResults:
        steps_results = StepsResults(
            cda=self.cda_steps_measurement(),
            bresenham_float=self.bresenham_float_steps_measurement(),
            bresenham_int=self.bresenham_int_steps_measurement(),
            bresenham_step=self.bresenham_without_gradation_steps_measurement(),
            vu=self.vu_steps_measurement(),
        )

        return steps_results

    def clear_results_plot(self) -> None:
        self.results_plot.clf()

    def set_plot_figure(self, window_title: str) -> None:
        self.results_plot.figure(num=window_title, figsize=self.figure_size)

    def show_time_measurement_bar_chart(self) -> None:
        self.set_plot_figure('Замеры времени работы алгоритмов')

        time_results = self.__get_time_measurement_dict()
        colors_list = get_random_rgb_colors_list(7)
        names_list = self.__get_algorithms_ru_names()

        self.results_plot.bar(names_list, list(time_results.values()), color=colors_list)

        self.results_plot.title(f'Среднее время работы алгоритмов для построения отрезка '
                                f'длиной в {MEASUREMENT_SPECTER_CORDS['radius']} пикселей', fontdict=self.plot_font)
        self.results_plot.xlabel('Наименование алгоритма', fontdict=self.plot_font, labelpad=20)
        self.results_plot.ylabel('Время работы (мкс)', fontdict=self.plot_font, labelpad=20)

        self.results_plot.xticks(rotation=45, ha='right', fontname='Calibri', fontsize=20)
        self.results_plot.yticks(fontsize=16)
        self.results_plot.tight_layout()

        self.results_plot.show()

    def show_steps_measurement_bar_chart(self) -> None:
        self.set_plot_figure('Замеры ступенчатости')
        self.results_plot.suptitle(f'Замеры проводятся для отрезка '
                                   f'длиной в {MEASUREMENT_SPECTER_CORDS['radius']} пикселей', fontsize=20)

        steps_results = list(self.__get_steps_measurement_dict().values())
        colors_list = get_random_rgb_colors_list(6)
        names_list = self.__get_algorithms_ru_names()[:-1]

        labels_dict = PlotConf(title='title', x_label='угол (в градусах)', y_label='кол-во ступенек', color=[0, 0, 0])
        n = 3
        m = 3
        index = 1
        step = 2
        for plot_name in names_list:
            labels_dict['title'] = plot_name
            labels_dict['color'] = colors_list[index // 2]
            self.__create_steps_subplot(n, m, index, labels_dict, steps_results[index // 2])
            index += step

        self.results_plot.tight_layout()
        self.results_plot.show()

    def __init_subplot(self, n: int, m: int, index: int) -> None:
        self.results_plot.subplot(n, m, index)

    def __create_steps_subplot(self, n: int, m: int, index: int, labels: PlotConf, data: list) -> None:
        self.__init_subplot(n, m, index)

        self.results_plot.title(labels['title'], fontdict=self.plot_font)
        self.results_plot.xlabel(labels['x_label'], fontdict=self.plot_font, labelpad=10)
        self.results_plot.ylabel(labels['y_label'], fontdict=self.plot_font, labelpad=10)

        x_cords = [i for i in range(0, MEASUREMENT_ANGLE + 1)]
        y_cords = data

        min_len = min(len(x_cords), len(y_cords))
        x_cords = x_cords[:min_len]
        y_cords = y_cords[:min_len]

        x_ticks = x_cords[0:-1:10] + [x_cords[-1]]

        self.results_plot.xticks(x_ticks, fontsize=14)
        self.results_plot.yticks(fontsize=14)

        self.results_plot.plot(x_cords, y_cords, color=labels['color'])

    def read_current_data(self) -> bool:
        if self.ui.line_mode_button.isChecked():
            figure_type = LINE
        else:
            figure_type = SPECTER

        draw_function = None

        if figure_type == LINE:
            if self.ui.cda_button.isChecked():
                draw_function = self.line_draw_cda
            elif self.ui.bresenham_int_button.isChecked():
                draw_function = self.line_draw_bresenham_int
            elif self.ui.bresenham_float_button.isChecked():
                draw_function = self.line_draw_bresenham_float
            elif self.ui.bresenham_without_gradation_button.isChecked():
                draw_function = self.line_draw_bresenham_without_gradation
            elif self.ui.vu_button.isChecked():
                draw_function = self.line_draw_vu
            elif self.ui.library_function_button.isChecked():
                draw_function = self.line_draw_library

            start_x = self.ui.line_start_x_field.text()
            start_y = self.ui.line_start_y_field.text()
            end_x = self.ui.line_end_x_field.text()
            end_y = self.ui.line_end_y_field.text()

            try:
                start_x = int(start_x)
                start_y = int(start_y)
                end_x = int(end_x)
                end_y = int(end_y)

            except ValueError:
                return False
            else:
                if start_x < 0 or start_y < 0 or end_x < 0 or end_y < 0:
                    return False

                cords = Line(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y)
                color = self.line_button_color

                self.drawn_figures.append([figure_type, draw_function, cords, color])

                return True

        elif figure_type == SPECTER:
            if self.ui.cda_button.isChecked():
                draw_function = self.specter_draw_cda
            elif self.ui.bresenham_int_button.isChecked():
                draw_function = self.specter_draw_bresenham_int
            elif self.ui.bresenham_float_button.isChecked():
                draw_function = self.specter_draw_bresenham_float
            elif self.ui.bresenham_without_gradation_button.isChecked():
                draw_function = self.specter_draw_bresenham_without_gradation
            elif self.ui.vu_button.isChecked():
                draw_function = self.specter_draw_vu
            elif self.ui.library_function_button.isChecked():
                draw_function = self.specter_draw_library

            center_x = self.ui.specter_center_x_field.text()
            center_y = self.ui.specter_center_y_field.text()
            radius = self.ui.specter_radius_field.text()
            angle = self.ui.specter_angle_field.text()

            try:
                center_x = int(center_x)
                center_y = int(center_y)
                radius = int(radius)
                angle = int(angle)
            except ValueError:
                return False
            else:
                if center_x < 0 or center_y < 0 or radius < 0 or angle < 0:
                    return False

                cords = Specter(center_x=center_x, center_y=center_y, radius=radius, angle=angle)
                color = self.specter_button_color

                self.drawn_figures.append([figure_type, draw_function, cords, color])

                return True

    def draw_button_clicked(self) -> None:
        rc = self.read_current_data()
        if rc:
            self.draw_figure(self.drawn_figures[-1])
            self.draw_pixmap()
        else:
            self.show_message_box(1)

    @staticmethod
    def draw_figure(data: list) -> None:
        function = data[1]
        cords = data[2]
        color = data[3]

        if function and cords and color:
            function(cords, color)

    def draw_all_previous_figures(self) -> None:
        for data in self.drawn_figures:
            self.draw_figure(data)

    def clear_screen_button_clicked(self) -> None:
        self.drawn_figures.clear()
        self.update_pixmap_color()
        self.draw_pixmap()

    def add_functions_connection(self):
        self.ui.line_mode_button.clicked.connect(self.select_line_mode)
        self.ui.specter_mode_button.clicked.connect(self.select_specter_mode)
        self.ui.screen_color_button.clicked.connect(self.set_screen_color)
        self.ui.line_color_button.clicked.connect(self.set_line_color)
        self.ui.specter_color_button.clicked.connect(self.set_specter_color)
        self.ui.draw_line_button.clicked.connect(self.draw_button_clicked)
        self.ui.draw_specter_button.clicked.connect(self.draw_button_clicked)
        self.ui.clear_screen_button.clicked.connect(self.clear_screen_button_clicked)
        self.ui.time_measurement_button.clicked.connect(self.show_time_measurement_bar_chart)
        self.ui.gradation_measurement_button.clicked.connect(self.show_steps_measurement_bar_chart)

    @staticmethod
    def show_message_box(message_code):
        ans_window = QMessageBox()
        text = "None"

        if message_code == 1:
            text = "Введены некорректные данные!"
        elif message_code == 2:
            text = "Коэффициент масштабирования по оси OY\n не может быть равен 0!"
        elif message_code == 3:
            text = "<b>Формулировка задачи:</b><br>Выполнить построение искомой фигуры, реализовать функции поворота,\
                масштабирования и переноса заданной фигуры<br><br><b>Ctrl+Z</b> - шаг назад"
        elif message_code == 4:
            text = "Данные введены некорректно!"

        ans_window.setText(text)
        ans_window.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    calc_window = MainApp(screen_color_rgb, line_color_rgb, specter_color_rgb, pixmap_width, pixmap_height)
    calc_window.show()

    sys.exit(app.exec())
