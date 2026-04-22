from analysis.pose_estimation import PoseEstimator
from utils.visualization_util import draw_landmarks_on_image
from utils.joint_utils import get_joint_id

from analysis.side_selection import (
    select_better_visible_side,
    get_side_visibility_scores,
)
from analysis.biomechanical_metrics import print_single_side_biomechanical_metrics

from constants import (
    IMPORTANT_JOINTS,
    DEFAULT_IMAGE_PATH,
    LEFT,
    RIGHT,
)


def main():
    image_path = DEFAULT_IMAGE_PATH

    estimator = PoseEstimator()
    joints = estimator.detect_pose_from_image(image_path)

    if joints is None:
        print("Nie wykryto sylwetki.")
        return

    print("Najważniejsze stawy:\n")

    for joint_name in IMPORTANT_JOINTS:
        joint_id = get_joint_id(joint_name)
        data = joints[joint_id]

        print(
            f"{joint_name:15s} | "
            f"x: {data['x']:.3f} | "
            f"y: {data['y']:.3f} | "
            f"z: {data['z']:.3f} | "
            f"visibility: {data['visibility']:.3f}"
        )

    scores = get_side_visibility_scores(joints)

    print("\nSide visibility scores:")
    print(f"{LEFT:5s} | {scores[LEFT]:.3f}")
    print(f"{RIGHT:5s} | {scores[RIGHT]:.3f}")

    selected_side = select_better_visible_side(joints)

    print(f"\nSelected side for analysis: {selected_side}")

    print_single_side_biomechanical_metrics(joints, selected_side)

    draw_landmarks_on_image(image_path, joints)


if __name__ == "__main__":
    main()