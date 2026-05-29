from constants import LEFT, RIGHT
from utils.joint_utils import get_joint_data


def calculate_wrist_midpoint(joints):
    left_wrist = get_joint_data(joints, f"{LEFT}_wrist")
    right_wrist = get_joint_data(joints, f"{RIGHT}_wrist")

    return {
        "x": (left_wrist["x"] + right_wrist["x"]) / 2,
        "y": (left_wrist["y"] + right_wrist["y"]) / 2,
        "visibility": (left_wrist["visibility"] + right_wrist["visibility"]) / 2,
    }


def calculate_bar_position(joints):
    """
    Przybliżona pozycja sztangi na podstawie środka między nadgarstkami.
    """

    return calculate_wrist_midpoint(joints)