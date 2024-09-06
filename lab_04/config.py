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


class Circle(TypedDict):
    center_x: int
    center_y: int
    radius: int


class Ellipse(TypedDict):
    center_x: int
    center_y: int
    radius_x: int
    radius_y: int


class CircleSpecter(TypedDict):
    center_x: int
    center_y: int
    radius: int
    step: int
    count: int


class EllipseSpecter(TypedDict):
    center_x: int
    center_y: int
    radius_x: int
    radius_y: int
    step: int
    count: int


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


class Point(TypedDict):
    x: float
    y: float


class PointsSet(TypedDict):
    x_cords: list[float]
    y_cords: list[float]


class CircleTime(TypedDict):
    center_x: int
    center_y: int
    start_radius: int
    end_radius: int
    step: int


class EllipseTime(TypedDict):
    center_x: int
    center_y: int
    start_radius_x: int
    start_radius_y: int
    end_radius_x: int
    step: int


screen_color_rgb = [255, 255, 255]
line_color_rgb = [0, 0, 0]
specter_color_rgb = [0, 0, 0]

pixmap_width = 1000
pixmap_height = 840

CIRCLE = 1
ELLIPSE = 2
CIRCLE_SPECTER = 3
ELLIPSE_SPECTER = 4

POINT_SIZE = 1      # in pixels

# rotate angle to draw circles
ROTATE_ANGLE = 45
ROTATE_STEP = 1

# time measurement params
MEASUREMENTS_COUNT = 100
MEASUREMENT_COLOR = 'black'
MS_CONVERT = 1_000
MCS_CONVERT = 1_000_000

CIRCLE_TIME = CircleTime(center_x=500, center_y=500, start_radius=50, end_radius=500, step=50)
ELLIPSE_TIME = EllipseTime(center_x=500, center_y=500, start_radius_x=50, start_radius_y=25, end_radius_x=500, step=50)

CANONICAL_PLOT = ['red', "Каноническая"]
PARAMETRIC_PLOT = ['cyan', "Параметрическая"]
BRESENHAM_PLOT = ['#12D936', "Брезенхем"]
MIDPOINT_PLOT = ['#59563F', "Средняя точка"]
LIBRARY_PLOT = ['purple', "Библиотечная"]


def get_random_rgb_color() -> tuple:        # for plt.plot(color=color)
    return randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255


class PointsSetTest:
    def __init__(self, x: list, y: list):
        self.x_cords: list = x
        self.y_cords: list = y

    def __add__(self, other):
        if not isinstance(other, PointsSetTest):
            raise TypeError("Invalid type for + with PointsSet")
        else:
            return PointsSetTest(self.x_cords + other.x_cords, self.y_cords + other.y_cords)

    def __getitem__(self, key) -> list:
        attr_dict = vars(self)
        if not isinstance(key, str):
            raise TypeError("invalid type for key!")
        elif not (key in attr_dict.keys()):
            raise ValueError("No such attribute!")
        else:
            return list(attr_dict[key])

    def print(self) -> None:
        print(f"x_cords: {' '.join([str(i) for i in self.x_cords])}")
        print(f"y_cords: {' '.join([str(i) for i in self.y_cords])}")
