import numpy as np
from config import calc_accuracy, eps, steps_count
import math
from math import atan2, asin, cos, sin, pi


def find_circle_params(cords_list: tuple) -> tuple[tuple[float, float], float] | None:
    """
    Parameters
    ----------
    `cords_list`: tuple with 3 point cords

    Returns 
    -------
    tuple
        if circle is exists, function return
        typle with cords of center of circle and circle radius value
    
    None
        if solution can't be solved, function return None
    
    Raises
    ------
    ValueError
        if `cords_list` len != 3
        
    function behaviour with invalid `cords_list` is undefinded
    """
    
    if len(cords_list) != 3:
        raise ValueError

    vectors_list = list()
    triangle_sides_centers = list()

    for i in range(2):
        vectors_list.append((cords_list[i + 1][0] - cords_list[i][0], cords_list[i + 1][1] - cords_list[i][1]))
        triangle_sides_centers.append((cords_list[i][0] + vectors_list[i][0] / 2, cords_list[i][1] + vectors_list[i][1] / 2))
    
    k_vector = list()
    for i in range(2):
        k_vector.append(vectors_list[i][0] * triangle_sides_centers[i][0] + vectors_list[i][1] * triangle_sides_centers[i][1])

    A = np.array(vectors_list)
    b = np.array(k_vector)
    
    solved_successfully = None
    answer_list = None

    try:
        np_answer = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        solved_successfully = False
    else:
        solved_successfully = True
        answer_list = list(map(lambda x: round(x, calc_accuracy), np_answer))
    

    if solved_successfully:
        circle_radius = find_line_length((cords_list[0], answer_list))

        return (answer_list[0], answer_list[1]), circle_radius
    
    else:
        return None


def find_line_equation_by_2_points(cords_list: tuple) -> tuple[float, float] | None:
    """
    Parameters
    ----------
    `cords_list`: tuple with 2 point cords 

    Returns 
    -------
    tuple
        if points aren't equal, function return (k, b)
    
    None
        if solution can't be solved, function return None
    
    Raises
    ------
    ValueError
        if `cords_list` len != 2
    
    function behaviour with invalid `cords_list` is undefinded
    """

    if len(cords_list) != 2:
        raise ValueError

    if cords_list[0] == cords_list[1]:
        return None
    
    A = np.array([[cords_list[0][0], 1], [cords_list[1][0], 1]])
    b = np.array([cords_list[0][1], cords_list[1][1]])

    answer = np.linalg.solve(A, b)

    return round(answer[0], calc_accuracy), round(answer[1], calc_accuracy)


def find_line_length(cords_list: tuple) -> float:
    line_length = round(((cords_list[1][0] - cords_list[0][0]) ** 2 + (cords_list[1][1] - cords_list[0][1]) ** 2) ** 0.5, calc_accuracy)

    return line_length


def check_for_triangle(cords_list: tuple) -> bool:
    len_list = list()
    
    for i in range(3):
        len_list.append(find_line_length((cords_list[i], cords_list[(i + 1) % 3])))
    
    len_list.sort()

    return len_list[0] + len_list[1] > len_list[2]


def solve_quadratic_equation(a, b, c):
    discriminant = b ** 2 - 4 * a * c

    if discriminant > 0:
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)
        return x1, x2
    
    elif discriminant == 0:
        x1 = -b / (2 * a)
        return x1
    
    else:
        return None
    

def find_all_circles(points_list_1: list) -> list:
    circles_list = list()
    
    for i in range(len(points_list_1) - 2):
        point_1 = points_list_1[i]
        for j in range(i + 1, len(points_list_1) - 1):
            point_2 = points_list_1[j]
            for k in range(j + 1, len(points_list_1)):
                point_3 = points_list_1[k]

                if check_for_triangle((point_1, point_2, point_3)):
                    circles_list.append(find_circle_params((point_1, point_2, point_3)))
    
    return circles_list


def transform_points_data(points_list: list) -> list:
    new_cords_list = list()

    for i in range(len(points_list[0])):
        new_cords_list.append((points_list[0][i], points_list[1][i]))
    
    return new_cords_list


def check_distant(circle_1: tuple, circle_2: tuple) -> bool:
    distance = find_line_length((circle_1[0], circle_2[0]))

    return distance > circle_1[1] + circle_2[1]


def find_intersection_of_tangents(circle_1: tuple, circle_2: tuple) -> tuple:
    full_distance = find_line_length((circle_1[0], circle_2[0]))
    r_1 = circle_1[1]
    r_2 = circle_2[1]

    distance_a = (r_1 * full_distance) / (r_1 + r_2)

    vector_a = ((circle_2[0][0] - circle_1[0][0]) * distance_a / full_distance, (circle_2[0][1] - circle_1[0][1]) * distance_a / full_distance)

    return round(circle_1[0][0] + vector_a[0], calc_accuracy), round(circle_1[0][1] + vector_a[1], calc_accuracy)


def find_leg(leg: float, hypotenuse: float) -> float:
    return round((hypotenuse ** 2 - leg ** 2) ** 0.5, calc_accuracy)


def find_square(circle: tuple, point_cords: tuple) -> float:
    radius = circle[1]
    hypotenuse = find_line_length((circle[0], point_cords))
    leg = find_leg(radius, hypotenuse)

    return leg * radius


def find_square_difference(circle_1: tuple, circle_2: tuple, intersection_point: tuple) -> float:
    return round(abs(find_square(circle_1, intersection_point) - find_square(circle_2, intersection_point)), calc_accuracy)


def find_best_circles(points_list_1: list, points_list_2: list) -> tuple:
    circles_set_1 = find_all_circles(points_list_1)
    circles_set_2 = find_all_circles(points_list_2)

    best_square_diff = float("inf")
    best_circle_1 = None
    best_circle_2 = None
    best_inter_point = None

    circles_found = False

    for circle_1 in circles_set_1:
        for circle_2 in circles_set_2:
            if check_distant(circle_1, circle_2):
                circles_found = True
                inter_point = find_intersection_of_tangents(circle_1, circle_2)
                current_square_diff = find_square_difference(circle_1, circle_2, inter_point)
                
                if current_square_diff < best_square_diff:
                    best_square_diff = current_square_diff
                    best_circle_1 = circle_1
                    best_circle_2 = circle_2
                    best_inter_point = inter_point
    
    if circles_found:
        return best_circle_1, best_circle_2, best_inter_point
    else:
        return None


def find_best_circles_params(points_set_1: list, points_set_2: list) -> dict:
    points_list_1 = transform_points_data(points_set_1)
    points_list_2 = transform_points_data(points_set_2)

    best_circles = find_best_circles(points_list_1, points_list_2)

    if best_circles is None:
        return None
    else:
        touch_points_1, touch_points_2 = find_touch_points(best_circles)

        all_params_dict = {
            'circle_1': best_circles[0],
            'circle_2': best_circles[1],
            'points_1': touch_points_1,
            'points_2': touch_points_2,
            'inter_point': best_circles[2]
                        }

        return all_params_dict


def pos_value(x: float) -> float:
    if x > 0:
        return x
    else:
        return 0


def find_touch_points_old(circle: tuple, point_cords: tuple, leg: float) -> list:
    touch_points = list()
    
    radius = circle[1]
    x_0 = circle[0][0]
    y_0 = circle[0][1]

    equal_check_1 = True
    equal_check_2 = True

    for x in np.arange(x_0 - radius, x_0 + radius, 2 * radius / steps_count):
        a = pos_value(radius ** 2 - (x - x_0) ** 2)
        y_1 = a ** 0.5 + y_0
        y_2 = -(a ** 0.5) + y_0    

        if abs(find_line_length(((x, y_1), point_cords)) - leg) <= eps:
            if equal_check_1:
                touch_points.append((round(x, calc_accuracy), round(y_1, calc_accuracy)))
                equal_check_1 = False
        else:
            equal_check_1 = True

        if abs(find_line_length(((x, y_2), point_cords)) - leg) <= eps:
            if equal_check_2:
                touch_points.append((round(x, calc_accuracy), round(y_2, calc_accuracy)))
                equal_check_2 = False
        else:
            equal_check_2 = True
    
    return touch_points


def find_touch_points(circles: tuple) -> tuple:

    def calculate_pair_points(circle_1, circle_2, short, hypotenuse, sign):
        if (sign >= 0):
            φ2 = atan2(circle_2[0][1] - circle_1[0][1], circle_2[0][0] - circle_1[0][0]) - asin(short/hypotenuse) + pi / 2
        else:
            φ2 = atan2(circle_2[0][1] - circle_1[0][1], circle_2[0][0] - circle_1[0][0]) + asin(short/hypotenuse) - pi / 2

        s1x = round(circle_1[0][0] + circle_1[1] * cos(φ2), calc_accuracy)
        s1y = round(circle_1[0][1] + circle_1[1] * sin(φ2), calc_accuracy)
        s2x = round(circle_2[0][0] + circle_2[1] * cos(φ2 + pi), calc_accuracy)
        s2y = round(circle_2[0][1] + circle_2[1] * sin(φ2 + pi), calc_accuracy)

        return (s1x, s1y), (s2x, s2y)
    
    c_1, c_2 = circles[0], circles[1]
    
    s = c_1[1] + c_2[1]
    h = find_line_length((c_1[0], c_2[0]))    

    return calculate_pair_points(c_1, c_2, s, h, 1), calculate_pair_points(c_1, c_2, s, h, -1)