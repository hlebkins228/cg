from typing import TypedDict
import numpy as np


figure_color = 'red'

float_regexp = "^[-+]?[0-9]*[.]?[0-9]+(?:[eE][-+]?[0-9]+)?$"

cache_size = 10

x_lim_l = -25
x_lim_r = 25
y_lim_l = -25
y_lim_r = 25

class FigureCache(TypedDict):
    below_part: list
    bottom_part: list
    semicircle_x: list
    semicircle_y: list
    big_circle_x: list
    big_circle_y: list
    small_circle_x: list
    small_circle_y: list


def get_circle_points(radius_x: float, radius_y: float, center_x: float, center_y: float, semicircle=False):
    if semicircle:
        angle_theta = np.linspace(np.pi / 2, 1.5 * np.pi, accuracy)
        circle_x_list = list(radius_x * np.cos(angle_theta) + center_x)
        circle_y_list = list(radius_y * np.sin(angle_theta) + center_y)
    else:
        angle_theta = np.linspace(0, 2 * np.pi, accuracy)
        circle_x_list = list(radius_x * np.cos(angle_theta) + center_x)
        circle_y_list = list(radius_y * np.sin(angle_theta) + center_y)
    
    return circle_x_list, circle_y_list


start_below_figure_part = {
        'x': [-6, -3, -4, 1, 2, 6, 11],
        'y': [2, 2, 4, 4, 2, 2, 5]
        }

start_bottom_figure_part = dict()
start_bottom_figure_part['x'] = start_below_figure_part['x']
start_bottom_figure_part['y'] = tuple([-y for y in start_below_figure_part['y']])

start_head_center = [6, 0]
start_tail_center = [-6, 0]

start_big_radius = 2
start_small_radius = 0.5
accuracy = 100

semicircle_x_list, semicircle_y_list = get_circle_points(start_big_radius / 2, start_big_radius, start_tail_center[0], start_tail_center[1], semicircle=True)
small_head_circle_x, small_head_circle_y = get_circle_points(start_small_radius, start_small_radius, start_head_center[0], start_head_center[1])
big_head_circle_x, big_head_circle_y = get_circle_points(start_big_radius, start_big_radius, start_head_center[0], start_head_center[1])


start_figure_params = FigureCache(
    bottom_part=start_bottom_figure_part, below_part=start_below_figure_part, semicircle_x=semicircle_x_list,
    semicircle_y=semicircle_y_list, small_circle_x=small_head_circle_x, small_circle_y=small_head_circle_y,
    big_circle_x=big_head_circle_x, big_circle_y=big_head_circle_y
                                  )

