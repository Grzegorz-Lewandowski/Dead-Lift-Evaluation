from analysis.angle_calculation import calculate_angle_from_joints
from analysis.back_metrics import calculate_back_inclination_angle
from constants import (
    SIDES,
    SINGLE_SIDE_ANGLE_DEFINITIONS,
)


def calculate_single_side_angles(joints, side):
    if side not in SIDES:
        raise ValueError(f"side must be one of {SIDES}")

    angles = {}

    for angle_name, joint_triplet in SINGLE_SIDE_ANGLE_DEFINITIONS.items():
        joint_a, joint_b, joint_c = joint_triplet

        joint_a = joint_a.format(side=side)
        joint_b = joint_b.format(side=side)
        joint_c = joint_c.format(side=side)

        try:
            angle_value = calculate_angle_from_joints(
                joints,
                joint_a,
                joint_b,
                joint_c,
            )
            angles[angle_name] = angle_value
        except Exception:
            angles[angle_name] = None

    return angles


def calculate_single_side_biomechanical_metrics(joints, side):
    """
    Główne metryki biomechaniczne dla wybranej strony.
    """

    metrics = calculate_single_side_angles(joints, side)

    try:
        metrics["back_inclination_angle"] = calculate_back_inclination_angle(
            joints,
            side,
        )
    except Exception:
        metrics["back_inclination_angle"] = None

    return metrics


def print_single_side_biomechanical_metrics(joints, side):
    metrics = calculate_single_side_biomechanical_metrics(joints, side)

    print(f"\nSingle-side biomechanical metrics for {side} side:\n")

    for metric_name, value in metrics.items():
        if value is None:
            print(f"{metric_name:25s} | ERROR")
        else:
            print(f"{metric_name:25s} | {value:.2f}°")