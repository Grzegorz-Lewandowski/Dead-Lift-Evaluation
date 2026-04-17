from analysis.pose_estimation import PoseEstimator
from utils.visualization_util import draw_landmarks_on_image
from constants import IMPORTANT_JOINTS, DEFAULT_IMAGE_PATH


def main():
    image_path = DEFAULT_IMAGE_PATH

    estimator = PoseEstimator()
    joints = estimator.detect_pose_from_image(image_path)

    if joints is None:
        print("Nie wykryto sylwetki.")
        return

    print("Najważniejsze stawy:\n")

    for joint_id, joint_name in IMPORTANT_JOINTS.items():
        data = joints[joint_id]

        print(
            f"{joint_name:15s} | "
            f"x: {data['x']:.3f} | "
            f"y: {data['y']:.3f} | "
            f"z: {data['z']:.3f} | "
            f"visibility: {data['visibility']:.3f}"
        )

    draw_landmarks_on_image(image_path, joints)


if __name__ == "__main__":
    main()