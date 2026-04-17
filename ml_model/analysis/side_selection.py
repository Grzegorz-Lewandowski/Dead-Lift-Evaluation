from constants import (
    LEFT,
    RIGHT,
    SIDES,
    SIDE_SELECTION_JOINT_PARTS,
)

from utils.joint_utils import get_joint_data


def calculate_side_visibility_score(joints, side):
    """
    Oblicza średni visibility score dla wybranej strony.
    """

    if side not in SIDES:
        raise ValueError(
            f"side must be one of {SIDES}"
        )

    total_visibility = 0.0
    joint_count = 0

    for joint_part in SIDE_SELECTION_JOINT_PARTS:

        joint_name = f"{side}_{joint_part}"

        joint_data = get_joint_data(
            joints,
            joint_name
        )

        total_visibility += joint_data["visibility"]
        joint_count += 1

    if joint_count == 0:
        return 0.0

    return total_visibility / joint_count


def get_side_visibility_scores(joints):
    """
    Zwraca visibility score dla obu stron.
    """

    return {
        LEFT: calculate_side_visibility_score(
            joints,
            LEFT,
        ),
        RIGHT: calculate_side_visibility_score(
            joints,
            RIGHT,
        ),
    }


def select_better_visible_side(joints):
    """
    Zwraca LEFT albo RIGHT.
    """

    scores = get_side_visibility_scores(
        joints
    )

    if scores[LEFT] >= scores[RIGHT]:
        return LEFT

    return RIGHT