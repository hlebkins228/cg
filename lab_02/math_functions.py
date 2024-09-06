import numpy as np


def rotate(x_cords: list, y_cords: list, rotation_center_x: float, rotation_center_y: float, angle: float) -> tuple:
    rotated_x_list = list()
    rotated_y_list = list()
    angle_in_radians = to_radians(angle)

    for x, y in zip(x_cords, y_cords):
        # переход в новую систему координат
        shifted_x = x - rotation_center_x
        shifted_y = y - rotation_center_y
        # поворот
        rotated_x = shifted_x * np.cos(angle_in_radians) + shifted_y * np.sin(angle_in_radians)
        rotated_y = shifted_y * np.cos(angle_in_radians) - shifted_x * np.sin(angle_in_radians)
        # возврат в старую систему координат
        new_x = rotated_x + rotation_center_x
        new_y = rotated_y + rotation_center_y
        # добавление в список новых координат
        rotated_x_list.append(new_x)
        rotated_y_list.append(new_y)

    return rotated_x_list, rotated_y_list


def move(x_cords: list, y_cords: list, shift_x: float, shift_y: float) -> tuple:
    shifted_x_list = list()
    shifted_y_list = list()

    for x, y in zip(x_cords, y_cords):
        # перенос каждой точки
        shifted_x = x + shift_x
        shifted_y = y + shift_y
        # добавление в список новых координат
        shifted_x_list.append(shifted_x)
        shifted_y_list.append(shifted_y)

    return shifted_x_list, shifted_y_list


def scale(x_cords: list, y_cords: list, center_x: float, center_y: float, scale_kx: float, scale_ky: float) -> tuple:
    scale_x_list = list()
    scale_y_list = list()
    
    for x, y in zip(x_cords, y_cords):
        scale_x_list.append(x * scale_kx + center_x * (1 - scale_kx))
        scale_y_list.append(y * scale_ky + center_y * (1 - scale_ky))

    return scale_x_list, scale_y_list


def to_radians(angle: float):
    return -np.radians(angle)