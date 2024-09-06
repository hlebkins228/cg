from typing import TypedDict
from random import randint


class Specter(TypedDict):
    radius: int
    center_x: int
    center_y: int
    angle: int


class Line(TypedDict):
    start_x: int
    start_y: int
    end_x: int
    end_y: int


class TimeResults(TypedDict):
    cda: float
    bresenham_float: float
    bresenham_int: float
    bresenham_step: float
    vu: float
    library: float


class StepsResults(TypedDict):
    cda: list
    bresenham_float: list
    bresenham_int: list
    bresenham_step: list
    vu: list


class PlotConf(TypedDict):
    title: str
    x_label: str
    y_label: str
    color: list


# Colors
screen_color_rgb = [255, 255, 255]
line_color_rgb = [0, 0, 0]
specter_color_rgb = [0, 0, 0]

pixmap_width = 1800
pixmap_height = 1350

LINE = 1
SPECTER = 2

POINT_SIZE = 1      # in pixels

# time and steps measurement params
MEASUREMENT_SPECTER_CORDS = Specter(radius=1000, center_x=500, center_y=500, angle=1)
MEASUREMENT_ANGLE = 90


def get_random_rgb_colors_list(colors_count) -> list:
    colors_list = list()
    current_color = list()
    for i in range(colors_count):
        current_color.clear()
        for _ in range(3):
            current_color.append(get_random_rgb_color())

        colors_list.append(current_color.copy())

    return colors_list


def get_random_rgb_color() -> float:
    return randint(0, 255) / 255
