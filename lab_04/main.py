from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QColorDialog
from PyQt6.QtWidgets import QMessageBox

from PyQt6.QtGui import QIntValidator
from PyQt6.QtGui import QColor, QPixmap, QPainter, QPen

import numpy as np

import matplotlib.pyplot as plt

import time
import sys
from math import sqrt

from config import *

from main_window import Ui_MainWindow


class MainApp(QMainWindow):
    def __init__(self, screen_color: list, circle_color: list, ellipse_color: list,
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
        self.circle_button_color = self.get_color_object_with_rgb(circle_color)
        self.ellipse_button_color = self.get_color_object_with_rgb(ellipse_color)
        self.set_default_color_buttons()
        self.update_pixmap_color()
        self.draw_pixmap()
        self.color_dialog = QColorDialog()

        self.pen = QPen(self.screen_button_color, POINT_SIZE)
        self.painter.setPen(self.pen)

        # set up init program state
        self.select_circle_mode()
        self.set_validators_for_input_fields()
        self.ui.canonical_button.setChecked(True)
        self.add_functions_connection()

        self.drawn_state = False

        self.results_plot = plt
        self.figure_size = (20, 15)
        self.plot_font = {'family': 'Calibri', 'color': 'black', 'weight': 'normal', 'size': 14}

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
        self.set_button_css_style(self.ui.circle_color_button, self.circle_button_color)
        self.set_button_css_style(self.ui.ellipse_color_button, self.ellipse_button_color)
        self.set_button_css_style(self.ui.circle_specter_color_button, self.circle_button_color)
        self.set_button_css_style(self.ui.ellipse_specter_color_button, self.ellipse_button_color)

    def detach_widget_from_old_parent(self, target_widget: QWidget, old_parent: QWidget, new_parent: QWidget) -> None:
        self.change_parent(target_widget, new_parent)
        self.normalize_pos(target_widget, old_parent)

    def configurate_widgets(self) -> None:  # special function for detach needed objects from QFrames and move it
        old_parent = self.ui.circle_frame
        self.detach_widget_from_old_parent(self.ui.ellipse_frame, old_parent, self.ui.centralwidget)
        self.detach_widget_from_old_parent(self.ui.circle_specter_frame, old_parent, self.ui.centralwidget)
        self.detach_widget_from_old_parent(self.ui.ellipse_specter_frame, old_parent, self.ui.centralwidget)
        self.detach_widget_from_old_parent(self.ui.ellipse_mode_button, old_parent, self.ui.centralwidget)
        self.detach_widget_from_old_parent(self.ui.circle_mode_button, old_parent, self.ui.centralwidget)
        self.detach_widget_from_old_parent(self.ui.specter_check_box, old_parent, self.ui.centralwidget)

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
        self.ui.label_15.setStyleSheet('QLabel { border: none; }')
        self.ui.label_16.setStyleSheet('QLabel { border: none; }')
        self.ui.label_17.setStyleSheet('QLabel { border: none; }')
        self.ui.label_24.setStyleSheet('QLabel { border: none; }')
        self.ui.label_24.setStyleSheet('QLabel { border: none; }')
        self.ui.label_25.setStyleSheet('QLabel { border: none; }')
        self.ui.label_26.setStyleSheet('QLabel { border: none; }')
        self.ui.label_29.setStyleSheet('QLabel { border: none; }')
        self.ui.label_30.setStyleSheet('QLabel { border: none; }')
        self.ui.label_31.setStyleSheet('QLabel { border: none; }')
        self.ui.label_32.setStyleSheet('QLabel { border: none; }')
        self.ui.label_33.setStyleSheet('QLabel { border: none; }')
        self.ui.label_34.setStyleSheet('QLabel { border: none; }')
        self.ui.label_35.setStyleSheet('QLabel { border: none; }')
        self.ui.label_36.setStyleSheet('QLabel { border: none; }')
        self.ui.label_37.setStyleSheet('QLabel { border: none; }')
        self.ui.label_38.setStyleSheet('QLabel { border: none; }')
        self.ui.label_39.setStyleSheet('QLabel { border: none; }')
        self.ui.label_40.setStyleSheet('QLabel { border: none; }')
        self.ui.label_41.setStyleSheet('QLabel { border: none; }')
        self.ui.label_42.setStyleSheet('QLabel { border: none; }')
        self.ui.label_43.setStyleSheet('QLabel { border: none; }')
        self.ui.label_44.setStyleSheet('QLabel { border: none; }')

    def set_validators_for_input_fields(self) -> None:
        # circle
        self.ui.circle_center_x_field.setValidator(self.validator)
        self.ui.circle_center_y_field.setValidator(self.validator)
        self.ui.circle_raduis_field.setValidator(self.validator)
        # ellipse
        self.ui.ellipse_center_x_field.setValidator(self.validator)
        self.ui.ellipse_center_y_field.setValidator(self.validator)
        self.ui.ellipse_radius_x_field.setValidator(self.validator)
        self.ui.ellipse_radius_y_field.setValidator(self.validator)
        # circle specter
        self.ui.circle_specter_center_x_field.setValidator(self.validator)
        self.ui.circle_specter_center_y_field.setValidator(self.validator)
        self.ui.circle_specter_raduis_field.setValidator(self.validator)
        self.ui.circle_specter_step_field.setValidator(self.validator)
        self.ui.circle_specters_count_field.setValidator(self.validator)
        # ellipse specter
        self.ui.ellipse_specter_center_x_field.setValidator(self.validator)
        self.ui.ellipse_specter_center_y_field.setValidator(self.validator)
        self.ui.ellipse_specter_radius_x_field.setValidator(self.validator)
        self.ui.ellipse_specter_radius_y_field.setValidator(self.validator)
        self.ui.ellipse_specter_step_field.setValidator(self.validator)
        self.ui.ellipse_specters_count_field.setValidator(self.validator)

    def circle_mode_button_is_checked(self) -> bool:
        return self.ui.circle_mode_button.isChecked()

    def ellipse_mode_button_is_checked(self) -> bool:
        return self.ui.ellipse_mode_button.isChecked()

    def specter_check_box_is_checked(self) -> bool:
        return self.ui.specter_check_box.isChecked()

    def set_circle_mode_visible(self) -> None:
        self.ui.circle_mode_button.setChecked(True)
        self.ui.circle_frame.setVisible(True)
        self.ui.circle_label.setVisible(True)

    def set_circle_mode_invisible(self) -> None:
        self.ui.circle_mode_button.setChecked(False)
        self.ui.circle_frame.setVisible(False)
        self.ui.circle_label.setVisible(False)

    def set_ellipse_mode_visible(self) -> None:
        self.ui.ellipse_mode_button.setChecked(True)
        self.ui.ellipse_frame.setVisible(True)
        self.ui.ellipse_label.setVisible(True)

    def set_ellipse_mode_invisible(self) -> None:
        self.ui.ellipse_mode_button.setChecked(False)
        self.ui.ellipse_frame.setVisible(False)
        self.ui.ellipse_label.setVisible(False)

    def set_ellipse_specter_mode_visible(self) -> None:
        self.ui.ellipse_mode_button.setChecked(True)
        self.ui.specter_check_box.setChecked(True)
        self.ui.ellipse_specter_frame.setVisible(True)
        self.ui.ellipse_specter_label.setVisible(True)

    def set_ellipse_specter_mode_invisible(self) -> None:
        self.ui.ellipse_mode_button.setChecked(False)
        self.ui.specter_check_box.setChecked(False)
        self.ui.ellipse_specter_frame.setVisible(False)
        self.ui.ellipse_specter_label.setVisible(False)

    def set_circle_specter_mode_visible(self) -> None:
        self.ui.circle_mode_button.setChecked(True)
        self.ui.specter_check_box.setChecked(True)
        self.ui.circle_specter_frame.setVisible(True)
        self.ui.circle_specter_label.setVisible(True)

    def set_circle_specter_mode_invisible(self) -> None:
        self.ui.circle_mode_button.setChecked(False)
        self.ui.specter_check_box.setChecked(False)
        self.ui.circle_specter_frame.setVisible(False)
        self.ui.circle_specter_label.setVisible(False)

    def set_circle_measurement_button_visible(self) -> None:
        self.ui.time_measurement_circle_button.setVisible(True)
        self.ui.time_measurement_ellipse_button.setVisible(False)

    def set_ellipse_measurement_button_visible(self) -> None:
        self.ui.time_measurement_circle_button.setVisible(False)
        self.ui.time_measurement_ellipse_button.setVisible(True)

    def select_circle_mode(self) -> None:
        self.set_circle_measurement_button_visible()

        if self.specter_check_box_is_checked():
            self.set_circle_mode_invisible()
            self.set_ellipse_mode_invisible()
            self.set_ellipse_specter_mode_invisible()
            self.set_circle_specter_mode_visible()
        else:
            self.set_ellipse_mode_invisible()
            self.set_ellipse_specter_mode_invisible()
            self.set_circle_specter_mode_invisible()
            self.set_circle_mode_visible()

    def select_ellipse_mode(self) -> None:
        self.set_ellipse_measurement_button_visible()

        if self.specter_check_box_is_checked():
            self.set_circle_mode_invisible()
            self.set_ellipse_mode_invisible()
            self.set_circle_specter_mode_invisible()
            self.set_ellipse_specter_mode_visible()
        else:
            self.set_circle_mode_invisible()
            self.set_ellipse_specter_mode_invisible()
            self.set_circle_specter_mode_invisible()
            self.set_ellipse_mode_visible()

    def specter_check_box_clicked(self) -> None:
        if self.circle_mode_button_is_checked():
            self.select_circle_mode()
        elif self.ellipse_mode_button_is_checked():
            self.select_ellipse_mode()

    def set_screen_color(self) -> None:
        color = self.choose_color()
        if color:
            self.screen_button_color = color
            self.set_button_css_style(self.ui.screen_color_button, color)

            self.update_pixmap_color()
            self.draw_all_previous_figures()
            self.draw_pixmap()

    def set_circle_color(self) -> None:
        color = self.choose_color()
        if color:
            self.circle_button_color = color
            self.set_button_css_style(self.ui.circle_color_button, color)
            self.set_button_css_style(self.ui.circle_specter_color_button, color)

    def set_ellipse_color(self) -> None:
        color = self.choose_color()
        if color:
            self.ellipse_button_color = color
            self.set_button_css_style(self.ui.ellipse_color_button, color)
            self.set_button_css_style(self.ui.ellipse_specter_color_button, color)

    def set_circle_specter_color(self) -> None:
        color = self.choose_color()
        if color:
            self.circle_button_color = color
            self.set_button_css_style(self.ui.circle_specter_color_button, color)
            self.set_button_css_style(self.ui.circle_color_button, color)

    def set_ellipse_specter_color(self) -> None:
        color = self.choose_color()
        if color:
            self.ellipse_button_color = color
            self.set_button_css_style(self.ui.ellipse_specter_color_button, color)
            self.set_button_css_style(self.ui.ellipse_color_button, color)

    def update_pen(self, color: QColor, i: float = 1) -> None:
        color.setAlpha(int(255 * i))
        self.pen = QPen(color, POINT_SIZE)
        self.painter.setPen(self.pen)

    def draw_point(self, x: int, y: int) -> None:
        if type(x) is int and type(y) is int and x > 0 and y > 0:
            self.painter.drawPoint(x, y)

    def draw_points_list(self, x_list: list, y_list: list) -> None:
        for point in zip(x_list, y_list):
            self.draw_point(round(point[0]), round(point[1]))

    def circle_draw_canonical(self, cords: Circle, color: QColor) -> None:
        self.__canonical_draw_circle_function(cords, color)

    def ellipse_draw_canonical(self, cords: Ellipse, color: QColor) -> None:
        self.__canonical_draw_ellipse_function(cords, color)

    def circle_specter_draw_canonical(self, cords: CircleSpecter, color: QColor) -> None:
        self.__circle_specter_draw(cords, color, self.__canonical_draw_circle_function)

    def ellipse_specter_draw_canonical(self, cords: EllipseSpecter, color: QColor) -> None:
        self.__ellipse_specter_draw(cords, color, self.__canonical_draw_ellipse_function)

    def circle_draw_parametric(self, cords: Circle, color: QColor) -> None:
        self.__parametric_draw_circle_function(cords, color)

    def ellipse_draw_parametric(self, cords: Ellipse, color: QColor) -> None:
        self.__parametric_draw_ellipse_function(cords, color)

    def circle_specter_draw_parametric(self, cords: CircleSpecter, color: QColor) -> None:
        self.__circle_specter_draw(cords, color, self.__parametric_draw_circle_function)

    def ellipse_specter_draw_parametric(self, cords: EllipseSpecter, color: QColor) -> None:
        self.__ellipse_specter_draw(cords, color, self.__parametric_draw_ellipse_function)

    def circle_draw_bresenham(self, cords: Circle, color: QColor) -> None:
        self.__bresenham_draw_circle_function(cords, color)

    def ellipse_draw_bresenham(self, cords: Ellipse, color: QColor) -> None:
        self.__bresenham_draw_ellipse_function(cords, color)

    def circle_specter_draw_bresenham(self, cords: CircleSpecter, color: QColor) -> None:
        self.__circle_specter_draw(cords, color, self.__bresenham_draw_circle_function)

    def ellipse_specter_draw_bresenham(self, cords: EllipseSpecter, color: QColor) -> None:
        self.__ellipse_specter_draw(cords, color, self.__bresenham_draw_ellipse_function)

    def circle_draw_midpoint(self, cords: Circle, color: QColor) -> None:
        self.__midpoint_draw_circle_function(cords, color)

    def ellipse_draw_midpoint(self, cords: Ellipse, color: QColor) -> None:
        self.__canonical_draw_ellipse_function(cords, color)

    def circle_specter_draw_midpoint(self, cords: CircleSpecter, color: QColor) -> None:
        self.__circle_specter_draw(cords, color, self.__midpoint_draw_circle_function)

    def ellipse_specter_draw_midpoint(self, cords: EllipseSpecter, color: QColor) -> None:
        self.__ellipse_specter_draw(cords, color, self.__canonical_draw_ellipse_function)

    def circle_draw_library(self, cords: Circle, color: QColor) -> None:
        self.__library_draw_circle_function(cords, color)

    def ellipse_draw_library(self, cords: Ellipse, color: QColor) -> None:
        self.__library_draw_ellipse_function(cords, color)

    def circle_specter_draw_library(self, cords: CircleSpecter, color: QColor) -> None:
        self.__circle_specter_draw(cords, color, self.__library_draw_circle_function)

    def ellipse_specter_draw_library(self, cords: EllipseSpecter, color: QColor) -> None:
        self.__ellipse_specter_draw(cords, color, self.__library_draw_ellipse_function)

    @staticmethod
    def __circle_specter_draw(cords: CircleSpecter, color: QColor, draw_function) -> None:
        x_0 = cords['center_x']
        y_0 = cords['center_y']
        start_radius = cords['radius']
        step = cords['step']
        circles_count = cords['count']

        for current_radius in range(start_radius, start_radius + circles_count * step, step):
            current_circle = Circle(center_x=x_0, center_y=y_0, radius=current_radius)
            draw_function(current_circle, color)

    @staticmethod
    def __ellipse_specter_draw(cords: EllipseSpecter, color: QColor, draw_function) -> None:
        x_0 = cords['center_x']
        y_0 = cords['center_y']
        start_radius_x = cords['radius_x']
        start_radius_y = cords['radius_y']
        step_x = cords['step']
        ellipses_count = cords['count']

        current_radius_x = start_radius_x
        current_radius_y = start_radius_y
        step_y = round(step_x * start_radius_y / start_radius_x)

        while current_radius_x < start_radius_x + ellipses_count * step_x:
            current_circle = Ellipse(center_x=x_0, center_y=y_0,
                                     radius_x=round(current_radius_x), radius_y=round(current_radius_y))
            draw_function(current_circle, color)
            current_radius_x += step_x
            current_radius_y += step_y

    @staticmethod
    def __get_symmetrical_points(cords: PointsSet, symmetrical_center: Point) -> PointsSet:
        new_cords_x = list()
        new_cords_y = list()
        for i in range(len(cords['x_cords'])):
            new_cords_x.append(cords['y_cords'][i] - symmetrical_center['y'] + symmetrical_center['x'])
            new_cords_y.append(cords['x_cords'][i] - symmetrical_center['x'] + symmetrical_center['y'])

        return PointsSet(x_cords=new_cords_x, y_cords=new_cords_y)

    def __get_draw_points_circle_canonical(self, cords: Circle, x: int) -> PointsSet:
        center_x = cords['center_x']
        center_y = cords['center_y']
        radius = cords['radius']

        delta = radius ** 2 - (x - center_x) ** 2
        if delta < 0:
            delta = 0
        root = sqrt(delta)

        y_1 = root + center_y
        y_2 = -root + center_y
        symmetrical_x = 2 * center_x - x

        x_cords_1 = [x, x, symmetrical_x, symmetrical_x]
        y_cords_1 = [y_1, y_2, y_1, y_2]

        temp_set = self.__get_symmetrical_points(PointsSet(x_cords=x_cords_1, y_cords=y_cords_1),
                                                 Point(x=center_x, y=center_y))

        x_cords_2, y_cords_2 = temp_set['x_cords'], temp_set['y_cords']

        return PointsSet(x_cords=x_cords_1 + x_cords_2, y_cords=y_cords_1 + y_cords_2)

    def __canonical_draw_circle_function(self, cords: Circle, color: QColor) -> None:
        self.update_pen(color)

        center_x = cords['center_x']
        radius = cords['radius']

        for current_x in range(center_x - radius, center_x + 1):
            current_points_set = self.__get_draw_points_circle_canonical(cords, current_x)
            self.draw_points_list(current_points_set['x_cords'], current_points_set['y_cords'])

    @staticmethod
    def __get_draw_points_ellipse_canonical_x(cords: Ellipse, x: int) -> PointsSet:
        center_x = cords['center_x']
        center_y = cords['center_y']
        radius_x = cords['radius_x']
        radius_y = cords['radius_y']

        delta = radius_y ** 2 - (x - center_x) ** 2 * (radius_y ** 2 / radius_x ** 2)
        if delta < 0:
            delta = 0
        root = sqrt(delta)

        y_1 = root + center_y
        y_2 = -root + center_y
        symmetrical_x = 2 * center_x - x

        x_cords = [x, x, symmetrical_x, symmetrical_x]
        y_cords = [y_1, y_2, y_1, y_2]

        return PointsSet(x_cords=x_cords, y_cords=y_cords)

    @staticmethod
    def __get_draw_points_ellipse_canonical_y(cords: Ellipse, y: int) -> PointsSet:
        center_x = cords['center_x']
        center_y = cords['center_y']
        radius_x = cords['radius_x']
        radius_y = cords['radius_y']

        delta = radius_x ** 2 - (y - center_y) ** 2 * (radius_x ** 2 / radius_y ** 2)
        if delta < 0:
            delta = 0
        root = sqrt(delta)

        x_1 = root + center_x
        x_2 = -root + center_x
        symmetrical_y = 2 * center_y - y

        x_cords = [x_1, x_2, x_1, x_2]
        y_cords = [y, y, symmetrical_y, symmetrical_y]

        return PointsSet(x_cords=x_cords, y_cords=y_cords)

    def __canonical_draw_ellipse_function(self, cords: Ellipse, color: QColor) -> None:
        self.update_pen(color)

        center_x = cords['center_x']
        center_y = cords['center_y']
        radius_x = cords['radius_x']
        radius_y = cords['radius_y']

        sqr_ra = radius_x ** 2
        sqr_rb = radius_y ** 2

        border_x = round(center_x + radius_x / np.sqrt(1 + sqr_rb / sqr_ra))
        border_y = round(center_y + radius_y / np.sqrt(1 + sqr_ra / sqr_rb))

        x_cords = list()
        y_cords = list()

        for x in range(round(center_x), border_x + 1):
            y = center_y + np.sqrt(sqr_ra * sqr_rb - (x - center_x) ** 2 * sqr_rb) / radius_x

            x_cords.append(x)
            y_cords.append(y)

        for y in range(border_y, round(center_y) - 1, -1):
            x = center_x + np.sqrt(sqr_ra * sqr_rb - (y - center_y) ** 2 * sqr_ra) / radius_y

            x_cords.append(x)
            y_cords.append(y)

        new_cords = self.reflect_points_4(PointsSet(x_cords=x_cords, y_cords=y_cords), Point(x=center_x, y=center_y))
        self.draw_points_list(new_cords['x_cords'], new_cords['y_cords'])

    def __parametric_draw_circle_function(self, cords: Circle, color: QColor) -> None:
        self.update_pen(color)

        center_x = cords['center_x']
        center_y = cords['center_y']
        radius = cords['radius']

        step = 1 / radius
        x_cords = list()
        y_cords = list()
        for angle in np.arange(0, np.pi / 4 + step, step):
            for theta in np.arange(0, 2 * np.pi, np.pi / 4):
                current_x = center_x + radius * np.sin(angle + theta)
                current_y = center_y + radius * np.cos(angle + theta)
                x_cords.append(current_x)
                y_cords.append(current_y)

        self.draw_points_list(x_cords, y_cords)

    def __parametric_draw_ellipse_function(self, cords: Ellipse, color: QColor) -> None:
        self.update_pen(color)

        center_x = cords['center_x']
        center_y = cords['center_y']
        radius_x = cords['radius_x']
        radius_y = cords['radius_y']

        step = 1 / max(radius_x, radius_y)
        x_cords = list()
        y_cords = list()
        for angle in np.arange(0, np.pi / 4 + step, step):
            for theta in np.arange(0, 2 * np.pi, np.pi / 4):
                current_x = center_x + radius_x * np.sin(angle + theta)
                current_y = center_y + radius_y * np.cos(angle + theta)
                x_cords.append(current_x)
                y_cords.append(current_y)

        self.draw_points_list(x_cords, y_cords)

    @staticmethod
    def __reflect_cords_by_yx(cords: PointsSet, shift_cords: Point) -> PointsSet:
        x_cords = cords['x_cords'].copy()
        y_cords = cords['y_cords'].copy()
        shift_x = shift_cords['x']
        shift_y = shift_cords['y']

        for i in range(len(x_cords)):
            x_cords[i] -= shift_x
            x_cords[i] = -x_cords[i]
            x_cords[i] += shift_y

            y_cords[i] -= shift_y
            y_cords[i] = -y_cords[i]
            y_cords[i] += shift_x

        return PointsSet(x_cords=y_cords, y_cords=x_cords)

    @staticmethod
    def __reflect_cords_by_x0(cords: PointsSet, center_x: int) -> PointsSet:
        x_cords = cords['x_cords'].copy()
        y_cords = cords['y_cords'].copy()

        for i in range(len(x_cords)):
            x_cords[i] = 2 * center_x - x_cords[i]

        return PointsSet(x_cords=x_cords, y_cords=y_cords)

    @staticmethod
    def __reflect_cords_by_y0(cords: PointsSet, center_y) -> PointsSet:
        x_cords = cords['x_cords'].copy()
        y_cords = cords['y_cords'].copy()

        for i in range(len(y_cords)):
            y_cords[i] = 2 * center_y - y_cords[i]

        return PointsSet(x_cords=x_cords, y_cords=y_cords)

    @staticmethod
    def __points_set_unit(set_1: PointsSet, set_2: PointsSet) -> PointsSet:
        return PointsSet(x_cords=set_1['x_cords'] + set_2['x_cords'], y_cords=set_1['y_cords'] + set_2['y_cords'])

    def reflect_points_8(self, cords: PointsSet, center_cords: Point) -> PointsSet:
        temp_set_1 = self.__reflect_cords_by_yx(cords, shift_cords=center_cords)
        temp_set_2 = self.__points_set_unit(cords, temp_set_1)
        temp_set_1 = self.__reflect_cords_by_x0(temp_set_2, center_x=int(center_cords['x']))
        temp_set_2 = self.__points_set_unit(temp_set_2, temp_set_1)
        temp_set_1 = self.__reflect_cords_by_y0(temp_set_2, center_y=int(center_cords['y']))
        temp_set_2 = self.__points_set_unit(temp_set_2, temp_set_1)

        return temp_set_2

    def reflect_points_4(self, cords: PointsSet, center_cords: Point) -> PointsSet:
        temp_set_1 = self.__reflect_cords_by_y0(cords, center_y=int(center_cords['y']))
        temp_set_2 = self.__points_set_unit(temp_set_1, cords)
        temp_set_1 = self.__reflect_cords_by_x0(temp_set_2, center_x=int(center_cords['x']))
        temp_set_2 = self.__points_set_unit(temp_set_1, temp_set_2)

        return temp_set_2

    def __bresenham_draw_circle_function(self, cords: Circle, color: QColor) -> None:
        self.update_pen(color)

        center_x = cords['center_x']
        center_y = cords['center_y']
        radius = cords['radius']

        x, y = 0, radius

        x_cords = [x + center_x]
        y_cords = [y + center_y]

        delta = 2 * (1 - radius)

        while x < y:
            d = 2 * (delta + y) - 1
            x += 1

            if d >= 0:
                y -= 1
                delta += 2 * (x - y + 1)
            else:
                delta += 2 * x + 1

            x_cords.append(x + center_x)
            y_cords.append(y + center_y)

        new_cords = self.reflect_points_8(PointsSet(x_cords=x_cords, y_cords=y_cords), Point(x=center_x, y=center_y))
        self.draw_points_list(new_cords['x_cords'], new_cords['y_cords'])

    def __bresenham_draw_ellipse_function(self, cords: Ellipse, color: QColor) -> None:
        self.update_pen(color)

        center_x = cords['center_x']
        center_y = cords['center_y']
        radius_x = cords['radius_x']
        radius_y = cords['radius_y']

        x = 0
        y = radius_y

        sqr_ra = radius_x ** 2
        sqr_rb = radius_y ** 2
        delta = sqr_rb - sqr_ra * (2 * radius_y + 1)

        x_cords = [x + center_x]
        y_cords = [y + center_y]

        while y >= 0:
            if delta < 0:
                d1 = 2 * delta + sqr_ra * (2 * y + 2)

                x += 1
                if d1 < 0:
                    delta += sqr_rb * (2 * x + 1)
                else:
                    y -= 1
                    delta += sqr_rb * (2 * x + 1) + sqr_ra * (1 - 2 * y)
            elif delta > 0:
                d2 = 2 * delta + sqr_rb * (2 - 2 * x)

                y -= 1
                if d2 > 0:
                    delta += sqr_ra * (1 - 2 * y)
                else:
                    x += 1
                    delta += sqr_rb * (2 * x + 1) + sqr_ra * (1 - 2 * y)
            else:
                y -= 1
                x += 1
                delta += sqr_rb * (2 * x + 1) + sqr_ra * (1 - 2 * y)

            x_cords.append(x + center_x)
            y_cords.append(y + center_y)

        new_cords = self.reflect_points_4(PointsSet(x_cords=x_cords, y_cords=y_cords), Point(x=center_x, y=center_y))
        self.draw_points_list(new_cords['x_cords'], new_cords['y_cords'])

    def __midpoint_draw_circle_function(self, cords: Circle, color: QColor) -> None:
        self.update_pen(color)

        center_x = cords['center_x']
        center_y = cords['center_y']
        radius = cords['radius']

        x = radius
        y = 0

        x_cords = [x + center_x]
        y_cords = [y + center_y]

        delta = 1 - radius  # 5/4 - r

        while x >= y:
            if delta >= 0:
                x -= 1
                y += 1
                delta += 2 * y + 1 - 2 * x
            else:
                y += 1
                delta += 2 * y + 1

            x_cords.append(x + center_x)
            y_cords.append(y + center_y)

        new_cords = self.reflect_points_8(PointsSet(x_cords=x_cords, y_cords=y_cords), Point(x=center_x, y=center_y))
        self.draw_points_list(new_cords['x_cords'], new_cords['y_cords'])

    def __midpoint_draw_ellipse_function(self, cords: Ellipse, color: QColor) -> None:
        self.update_pen(color)

        center_x = cords['center_x']
        center_y = cords['center_y']
        radius_x = cords['radius_x']
        radius_y = cords['radius_y']

        sqr_ra = radius_x ** 2
        sqr_rb = radius_y ** 2

        x = 0
        y = radius_y

        x_cords = [x + center_x]
        y_cords = [y + center_y]

        border = round(radius_x / np.sqrt(1 + sqr_rb / sqr_ra))
        delta = sqr_rb - round(sqr_ra * (radius_y - 1 / 4))

        while x <= border:
            if delta < 0:
                x += 1
                delta += 2 * sqr_rb * x + 1
            else:
                x += 1
                y -= 1
                delta += 2 * sqr_rb * x - 2 * sqr_ra * y + 1

            x_cords.append(x + center_x)
            y_cords.append(y + center_y)

        x = radius_x
        y = 0

        x_cords.append(x + center_x)
        y_cords.append(y + center_y)

        border = round(radius_y / np.sqrt(1 + sqr_ra / sqr_rb))
        delta = sqr_ra - round(sqr_rb * (radius_x - 1 / 4))

        while y <= border:
            if delta < 0:
                y += 1
                delta += 2 * sqr_ra * y + 1
            else:
                x -= 1
                y += 1
                delta += 2 * sqr_ra * y - 2 * sqr_rb * x + 1

            x_cords.append(x + center_x)
            y_cords.append(y + center_y)

        new_cords = self.reflect_points_4(PointsSet(x_cords=x_cords, y_cords=y_cords), Point(x=center_x, y=center_y))
        self.draw_points_list(new_cords['x_cords'], new_cords['y_cords'])

    def __library_draw_circle_function(self, cords: Circle, color: QColor) -> None:
        self.update_pen(color)

        radius = cords['radius']
        center_x = cords['center_x'] - radius
        center_y = cords['center_y'] - radius

        self.painter.drawEllipse(center_x, center_y, radius * 2, radius * 2)

    def __library_draw_ellipse_function(self, cords: Ellipse, color: QColor) -> None:
        self.update_pen(color)

        radius_x = cords['radius_x']
        radius_y = cords['radius_y']
        center_x = cords['center_x'] - radius_x
        center_y = cords['center_y'] - radius_y

        self.painter.drawEllipse(center_x, center_y, radius_x * 2, radius_y * 2)

    def read_current_data(self) -> bool:
        if self.circle_mode_button_is_checked():
            if self.specter_check_box_is_checked():
                figure_type = CIRCLE_SPECTER
            else:
                figure_type = CIRCLE
        else:
            if self.specter_check_box_is_checked():
                figure_type = ELLIPSE_SPECTER
            else:
                figure_type = ELLIPSE

        draw_function = None

        if figure_type == CIRCLE:
            if self.ui.canonical_button.isChecked():
                draw_function = self.circle_draw_canonical
            elif self.ui.paremetric_button.isChecked():
                draw_function = self.circle_draw_parametric
            elif self.ui.bresenham_button.isChecked():
                draw_function = self.circle_draw_bresenham
            elif self.ui.midpoint_button.isChecked():
                draw_function = self.circle_draw_midpoint
            elif self.ui.library_function_button.isChecked():
                draw_function = self.circle_draw_library

            center_x = self.ui.circle_center_x_field.text()
            center_y = self.ui.circle_center_y_field.text()
            radius = self.ui.circle_raduis_field.text()

            try:
                center_x = int(center_x)
                center_y = int(center_y)
                radius = int(radius)

            except ValueError:
                return False
            else:
                if center_x < 0 or center_y < 0 or radius <= 0:
                    return False

                cords = Circle(center_x=center_x, center_y=center_y, radius=radius)
                color = self.circle_button_color

                self.drawn_figures.append([figure_type, draw_function, cords, color])

                return True

        elif figure_type == ELLIPSE:
            if self.ui.canonical_button.isChecked():
                draw_function = self.ellipse_draw_canonical
            elif self.ui.paremetric_button.isChecked():
                draw_function = self.ellipse_draw_parametric
            elif self.ui.bresenham_button.isChecked():
                draw_function = self.ellipse_draw_bresenham
            elif self.ui.midpoint_button.isChecked():
                draw_function = self.ellipse_draw_midpoint
            elif self.ui.library_function_button.isChecked():
                draw_function = self.ellipse_draw_library

            center_x = self.ui.ellipse_center_x_field.text()
            center_y = self.ui.ellipse_center_y_field.text()
            radius_x = self.ui.ellipse_radius_x_field.text()
            radius_y = self.ui.ellipse_radius_y_field.text()

            try:
                center_x = int(center_x)
                center_y = int(center_y)
                radius_x = int(radius_x)
                radius_y = int(radius_y)
            except ValueError:
                return False
            else:
                if center_x < 0 or center_y < 0 or radius_x <= 0 or radius_y <= 0:
                    return False

                cords = Ellipse(center_x=center_x, center_y=center_y, radius_x=radius_x, radius_y=radius_y)
                color = self.ellipse_button_color

                self.drawn_figures.append([figure_type, draw_function, cords, color])

                return True

        elif figure_type == CIRCLE_SPECTER:
            if self.ui.canonical_button.isChecked():
                draw_function = self.circle_specter_draw_canonical
            elif self.ui.paremetric_button.isChecked():
                draw_function = self.circle_specter_draw_parametric
            elif self.ui.bresenham_button.isChecked():
                draw_function = self.circle_specter_draw_bresenham
            elif self.ui.midpoint_button.isChecked():
                draw_function = self.circle_specter_draw_midpoint
            elif self.ui.library_function_button.isChecked():
                draw_function = self.circle_specter_draw_library

            center_x = self.ui.circle_specter_center_x_field.text()
            center_y = self.ui.circle_specter_center_y_field.text()
            radius = self.ui.circle_specter_raduis_field.text()
            step = self.ui.circle_specter_step_field.text()
            circles_count = self.ui.circle_specters_count_field.text()

            try:
                center_x = int(center_x)
                center_y = int(center_y)
                radius = int(radius)
                step = int(step)
                circles_count = int(circles_count)

            except ValueError:
                return False
            else:
                if center_x < 0 or center_y < 0 or radius < 0 or step <= 0 or circles_count <= 0:
                    return False

                cords = CircleSpecter(center_x=center_x, center_y=center_y, radius=radius,
                                      step=step, count=circles_count)
                color = self.circle_button_color

                self.drawn_figures.append([figure_type, draw_function, cords, color])

                return True

        elif figure_type == ELLIPSE_SPECTER:
            if self.ui.canonical_button.isChecked():
                draw_function = self.ellipse_specter_draw_canonical
            elif self.ui.paremetric_button.isChecked():
                draw_function = self.ellipse_specter_draw_parametric
            elif self.ui.bresenham_button.isChecked():
                draw_function = self.ellipse_specter_draw_bresenham
            elif self.ui.midpoint_button.isChecked():
                draw_function = self.ellipse_specter_draw_midpoint
            elif self.ui.library_function_button.isChecked():
                draw_function = self.ellipse_specter_draw_library

            center_x = self.ui.ellipse_specter_center_x_field.text()
            center_y = self.ui.ellipse_specter_center_y_field.text()
            radius_x = self.ui.ellipse_specter_radius_x_field.text()
            radius_y = self.ui.ellipse_specter_radius_y_field.text()
            step = self.ui.ellipse_specter_step_field.text()
            circles_count = self.ui.ellipse_specters_count_field.text()

            try:
                center_x = int(center_x)
                center_y = int(center_y)
                radius_x = int(radius_x)
                radius_y = int(radius_y)
                step = int(step)
                ellipses_count = int(circles_count)

            except ValueError:
                return False
            else:
                if center_x < 0 or center_y < 0 or radius_x <= 0 or radius_y <= 0 or step <= 0 or ellipses_count <= 0:
                    return False

                cords = EllipseSpecter(center_x=center_x, center_y=center_y, radius_x=radius_x, radius_y=radius_y,
                                       step=step, count=ellipses_count)
                color = self.ellipse_button_color

                self.drawn_figures.append([figure_type, draw_function, cords, color])

                return True

    def __time_measurement_circle(self, draw_function) -> list[tuple[int, int]]:
        color = QColor(MEASUREMENT_COLOR)

        center_x = CIRCLE_TIME['center_x']
        center_y = CIRCLE_TIME['center_y']
        start_radius = CIRCLE_TIME['start_radius']
        step = CIRCLE_TIME['step']
        end_radius = CIRCLE_TIME['end_radius']

        time_results = list()

        current_circle = Circle(center_x=center_x, center_y=center_y, radius=1)
        for current_radius in range(start_radius, end_radius + step, step):
            current_circle['radius'] = current_radius
            time_results.append((current_radius,
                                 self.__figure_draw_time_measure(draw_function, current_circle, color)))

        return time_results

    def __time_measurement_ellipse(self, draw_function) -> list[tuple[int, int]]:
        color = QColor(MEASUREMENT_COLOR)

        center_x = ELLIPSE_TIME['center_x']
        center_y = ELLIPSE_TIME['center_y']
        start_radius_x = ELLIPSE_TIME['start_radius_x']
        start_radius_y = ELLIPSE_TIME['start_radius_y']
        end_radius_x = ELLIPSE_TIME['end_radius_x']
        step_x = ELLIPSE_TIME['step']
        step_y = round(step_x * start_radius_y / start_radius_x)

        time_results = list()

        current_ellipse = Ellipse(center_x=center_x, center_y=center_y, radius_x=1, radius_y=1)
        current_radius_x = start_radius_x
        current_radius_y = start_radius_y

        while current_radius_x <= end_radius_x:
            current_ellipse['radius_x'] = current_radius_x
            current_ellipse['radius_y'] = current_radius_y

            time_results.append((current_radius_x,
                                 self.__figure_draw_time_measure(draw_function, current_ellipse, color)))

            current_radius_x += step_x
            current_radius_y += step_y

        return time_results

    @staticmethod
    def __figure_draw_time_measure(draw_function, figure_params, color) -> int:
        """
        :param draw_function: 
        :param figure_params: 
        :param color: 
        :return: int time in mcs
        """

        start_time = time.time()
        for _ in range(MEASUREMENTS_COUNT):
            draw_function(figure_params, color)
        end_time = time.time()

        return round((end_time - start_time) * MS_CONVERT)

    def time_measurement_circle_canonical(self) -> list[tuple[int, int]]:
        return self.__time_measurement_circle(self.__canonical_draw_circle_function)

    def time_measurement_ellipse_canonical(self) -> list[tuple[int, int]]:
        return self.__time_measurement_ellipse(self.__canonical_draw_ellipse_function)

    def time_measurement_circle_parametric(self) -> list[tuple[int, int]]:
        return self.__time_measurement_circle(self.__parametric_draw_circle_function)

    def time_measurement_ellipse_parametric(self) -> list[tuple[int, int]]:
        return self.__time_measurement_ellipse(self.__parametric_draw_ellipse_function)

    def time_measurement_circle_bresenham(self) -> list[tuple[int, int]]:
        return self.__time_measurement_circle(self.__bresenham_draw_circle_function)

    def time_measurement_ellipse_bresenham(self) -> list[tuple[int, int]]:
        return self.__time_measurement_ellipse(self.__bresenham_draw_ellipse_function)

    def time_measurement_circle_midpoint(self) -> list[tuple[int, int]]:
        return self.__time_measurement_circle(self.__midpoint_draw_circle_function)

    def time_measurement_ellipse_midpoint(self) -> list[tuple[int, int]]:
        return self.__time_measurement_ellipse(self.__midpoint_draw_ellipse_function)

    def time_measurement_circle_library(self) -> list[tuple[int, int]]:
        return self.__time_measurement_circle(self.__library_draw_circle_function)

    def time_measurement_ellipse_library(self) -> list[tuple[int, int]]:
        return self.__time_measurement_ellipse(self.__library_draw_ellipse_function)

    @staticmethod
    def __transform_time_results_to_cords(time_results: list[tuple[int, int]]) -> tuple[list[int], list[int]]:
        radius_list = list()  # x axe
        time_list = list()  # y axe

        for result in time_results:
            radius_list.append(result[0])
            time_list.append(result[1])

        return radius_list, time_list

    def __create_results_plot(self, time_result_function, plot, color: str, label: str) -> None:
        time_results = time_result_function()
        x_cords, y_cords = self.__transform_time_results_to_cords(time_results)

        plot.plot(x_cords, y_cords, color=color, label=label)

    @staticmethod
    def set_plot_figure(plot, window_title: str) -> None:
        plot.figure(num=window_title)

    def show_time_measurement_circle(self):
        plot = self.results_plot
        self.set_plot_figure(plot, "Results")

        self.__create_results_plot(self.time_measurement_circle_canonical, plot, CANONICAL_PLOT[0],
                                   CANONICAL_PLOT[1])
        self.__create_results_plot(self.time_measurement_circle_parametric, plot, PARAMETRIC_PLOT[0],
                                   PARAMETRIC_PLOT[1])
        self.__create_results_plot(self.time_measurement_circle_bresenham, plot, BRESENHAM_PLOT[0],
                                   BRESENHAM_PLOT[1])

        self.__create_results_plot(self.time_measurement_circle_midpoint, plot, MIDPOINT_PLOT[0],
                                   MIDPOINT_PLOT[1])
        self.__create_results_plot(self.time_measurement_circle_library, plot, LIBRARY_PLOT[0],
                                   LIBRARY_PLOT[1])

        plot.title('График зависимости времени рисования окружности от её радиуса', fontdict=self.plot_font)
        plot.xlabel('Радиус окружности', fontdict=self.plot_font, labelpad=5)
        plot.ylabel('Время рисования (мс)', fontdict=self.plot_font, labelpad=5)

        plot.legend()
        plot.tight_layout()
        plot.show()

        self.clear_screen_button_clicked()

    def show_time_measurement_ellipse(self):
        plot = self.results_plot
        self.set_plot_figure(plot, "Results")

        self.__create_results_plot(self.time_measurement_ellipse_canonical, plot, CANONICAL_PLOT[0],
                                   CANONICAL_PLOT[1])
        self.__create_results_plot(self.time_measurement_ellipse_parametric, plot, PARAMETRIC_PLOT[0],
                                   PARAMETRIC_PLOT[1])
        self.__create_results_plot(self.time_measurement_ellipse_bresenham, plot, BRESENHAM_PLOT[0],
                                   BRESENHAM_PLOT[1])
        self.__create_results_plot(self.time_measurement_ellipse_midpoint, plot, MIDPOINT_PLOT[0],
                                   MIDPOINT_PLOT[1])
        self.__create_results_plot(self.time_measurement_ellipse_library, plot, LIBRARY_PLOT[0],
                                   LIBRARY_PLOT[1])

        plot.title('График зависимости времени рисования эллипса от его радиуса', fontdict=self.plot_font)
        plot.xlabel('Радиус эллипса оп оси OX', fontdict=self.plot_font, labelpad=5)
        plot.ylabel('Время рисования (мс)', fontdict=self.plot_font, labelpad=5)

        plot.legend()
        plot.tight_layout()
        plot.show()

        self.clear_screen_button_clicked()

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
        pass
        self.ui.circle_mode_button.clicked.connect(self.select_circle_mode)
        self.ui.ellipse_mode_button.clicked.connect(self.select_ellipse_mode)
        self.ui.specter_check_box.clicked.connect(self.specter_check_box_clicked)
        self.ui.screen_color_button.clicked.connect(self.set_screen_color)
        self.ui.circle_color_button.clicked.connect(self.set_circle_color)
        self.ui.ellipse_color_button.clicked.connect(self.set_ellipse_color)
        self.ui.ellipse_specter_color_button.clicked.connect(self.set_ellipse_specter_color)
        self.ui.circle_specter_color_button.clicked.connect(self.set_circle_specter_color)
        self.ui.draw_circle_button.clicked.connect(self.draw_button_clicked)
        self.ui.draw_ellipse_button.clicked.connect(self.draw_button_clicked)
        self.ui.draw_circle_specter_button.clicked.connect(self.draw_button_clicked)
        self.ui.draw_ellipse_specter_button.clicked.connect(self.draw_button_clicked)
        self.ui.clear_screen_button.clicked.connect(self.clear_screen_button_clicked)
        self.ui.time_measurement_circle_button.clicked.connect(self.show_time_measurement_circle)
        self.ui.time_measurement_ellipse_button.clicked.connect(self.show_time_measurement_ellipse)

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
