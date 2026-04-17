import math

from utils.joint_utils import get_joint_data


def calculate_angle_from_points(point_a, point_b, point_c):
    """
    Oblicza kąt ABC w stopniach.
    point_b jest wierzchołkiem kąta.

    Każdy punkt powinien mieć postać:
    (x, y)
    """

    ax, ay = point_a
    bx, by = point_b
    cx, cy = point_c

    vector_ba = (ax - bx, ay - by)
    vector_bc = (cx - bx, cy - by)

    length_ba = math.sqrt(vector_ba[0] ** 2 + vector_ba[1] ** 2)
    length_bc = math.sqrt(vector_bc[0] ** 2 + vector_bc[1] ** 2)

    if length_ba == 0 or length_bc == 0:
        raise ValueError("Nie można obliczyć kąta dla wektora o długości 0.")

    dot_product = (
        vector_ba[0] * vector_bc[0]
        + vector_ba[1] * vector_bc[1]
    )

    cosine_angle = dot_product / (length_ba * length_bc)

    # zabezpieczenie przed błędami numerycznymi
    cosine_angle = max(-1.0, min(1.0, cosine_angle))

    angle_radians = math.acos(cosine_angle)
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees


def get_2d_point(joints, joint_name):
    """
    Zwraca punkt (x, y) dla zadanego stawu na podstawie jego nazwy.
    """
    joint_data = get_joint_data(joints, joint_name)
    return joint_data["x"], joint_data["y"]


def calculate_angle_from_joints(joints, joint_a_name, joint_b_name, joint_c_name):
    """
    Oblicza kąt dla trzech stawów wskazanych nazwami.

    Przykład:
    calculate_angle_from_joints(
        joints,
        "right_hip",
        "right_knee",
        "right_ankle"
    )
    """
    point_a = get_2d_point(joints, joint_a_name)
    point_b = get_2d_point(joints, joint_b_name)
    point_c = get_2d_point(joints, joint_c_name)

    return calculate_angle_from_points(point_a, point_b, point_c)