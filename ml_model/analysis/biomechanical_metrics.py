from analysis.angle_calculation import calculate_angle_from_joints
from constants import ANGLE_DEFINITIONS


def calculate_all_angles(joints):
    """
    Oblicza wszystkie zdefiniowane kąty biomechaniczne.
    """

    angles = {}

    for angle_name, joint_triplet in ANGLE_DEFINITIONS.items():

        joint_a, joint_b, joint_c = joint_triplet

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


def print_all_angles(joints):
    """
    Wypisuje wszystkie kąty w czytelnej formie.
    """

    angles = calculate_all_angles(joints)

    print("\nBiomechanical angles:\n")

    for angle_name, value in angles.items():

        if value is None:

            print(
                f"{angle_name:25s} | ERROR"
            )

        else:

            print(
                f"{angle_name:25s} | "
                f"{value:.2f}°"
            )