import cv2
import matplotlib.pyplot as plt

from utils.joint_utils import get_joint_id

from constants import (
    IMPORTANT_JOINTS,
    SKELETON_CONNECTIONS,
    DEFAULT_VISUALIZATION_OUTPUT_PATH)

def draw_landmarks_on_image(
    image_path,
    joints,
    save_path=DEFAULT_VISUALIZATION_OUTPUT_PATH):

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(
            f"Nie udało się wczytać obrazu: {image_path}"
        )

    image_rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )
    height, width, _ = image.shape

    plt.figure(figsize=(8, 10))
    plt.imshow(image_rgb)

    # rysuj punkty

    for joint_name in IMPORTANT_JOINTS:
        joint_id = get_joint_id(joint_name)
        data = joints[joint_id]

        x_px = int(data["x"] * width)
        y_px = int(data["y"] * height)

        plt.scatter(
            x_px,
            y_px,
            s=80
        )

        plt.text(
            x_px,
            y_px,
            joint_name,
            fontsize=9
        )

    # rysuj linie skeleton

    for joint_a, joint_b in SKELETON_CONNECTIONS:
        id_a = get_joint_id(joint_a)
        id_b = get_joint_id(joint_b)

        x1 = int(joints[id_a]["x"] * width)
        y1 = int(joints[id_a]["y"] * height)

        x2 = int(joints[id_b]["x"] * width)
        y2 = int(joints[id_b]["y"] * height)

        plt.plot(
            [x1, x2],
            [y1, y2],
            linewidth=2
        )

    plt.title("Important Joints Visualization")
    plt.axis("off")

    plt.savefig(
        save_path,
        bbox_inches="tight"
    )

    print(f"Zapisano obraz: {save_path}")
    plt.show()