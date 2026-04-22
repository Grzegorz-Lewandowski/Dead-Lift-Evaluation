import math

from constants import SIDES
from utils.joint_utils import get_joint_data


def calculate_back_inclination_angle(joints, side):
    """
    Oblicza kąt pochylenia tułowia względem pionu.

    Wykorzystuje punkty:
    - {side}_hip
    - {side}_shoulder

    Zwraca kąt w stopniach:
    - 0°   -> tułów idealnie pionowy
    - większa wartość -> większe pochylenie do przodu
    """

    if side not in SIDES:
        raise ValueError(f"side must be one of {SIDES}")

    shoulder = get_joint_data(joints, f"{side}_shoulder")
    hip = get_joint_data(joints, f"{side}_hip")

    dx = shoulder["x"] - hip["x"]
    dy = shoulder["y"] - hip["y"]

    # wektor pionowy "w górę" w obrazie ma postać (0, -1)
    vertical_x = 0.0
    vertical_y = -1.0

    dot_product = dx * vertical_x + dy * vertical_y
    magnitude_back = math.sqrt(dx ** 2 + dy ** 2)
    magnitude_vertical = 1.0

    if magnitude_back == 0:
        raise ValueError("Back vector has zero length.")

    cosine_angle = dot_product / (magnitude_back * magnitude_vertical)
    cosine_angle = max(-1.0, min(1.0, cosine_angle))

    angle_radians = math.acos(cosine_angle)
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees


def get_back_visibility_score(joints, side):
    """
    Zwraca średnią visibility dla punktów bark-biodro.
    """
    if side not in SIDES:
        raise ValueError(f"side must be one of {SIDES}")

    shoulder = get_joint_data(joints, f"{side}_shoulder")
    hip = get_joint_data(joints, f"{side}_hip")

    return (shoulder["visibility"] + hip["visibility"]) / 2.0