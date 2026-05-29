import cv2

from constants import (
    IMPORTANT_JOINTS,
    SKELETON_CONNECTIONS,
    VIDEO_FRAME_STRIDE,
)
from utils.joint_utils import get_joint_id


def draw_pose_on_frame(frame, joints):
    height, width, _ = frame.shape
    output_frame = frame.copy()

    for joint_name in IMPORTANT_JOINTS:
        joint_id = get_joint_id(joint_name)
        joint_data = joints[joint_id]

        x = int(joint_data["x"] * width)
        y = int(joint_data["y"] * height)

        cv2.circle(output_frame, (x, y), 6, (0, 255, 0), -1)

        cv2.putText(
            output_frame,
            joint_name,
            (x + 5, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    for joint_a, joint_b in SKELETON_CONNECTIONS:
        joint_a_id = get_joint_id(joint_a)
        joint_b_id = get_joint_id(joint_b)

        joint_a_data = joints[joint_a_id]
        joint_b_data = joints[joint_b_id]

        x1 = int(joint_a_data["x"] * width)
        y1 = int(joint_a_data["y"] * height)

        x2 = int(joint_b_data["x"] * width)
        y2 = int(joint_b_data["y"] * height)

        cv2.line(output_frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

    return output_frame


def create_annotated_video(
    input_video_path,
    output_video_path,
    estimator,
    frame_stride=VIDEO_FRAME_STRIDE,
):
    video_capture = cv2.VideoCapture(input_video_path)

    if not video_capture.isOpened():
        raise FileNotFoundError(
            f"Nie udało się otworzyć filmu: {input_video_path}"
        )

    fps = video_capture.get(cv2.CAP_PROP_FPS)
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    video_writer = cv2.VideoWriter(
        output_video_path,
        fourcc,
        fps,
        (width, height),
    )

    frame_number = 0

    while True:
        success, frame = video_capture.read()

        if not success:
            break

        if frame_number % frame_stride == 0:
            joints = estimator.detect_pose_from_frame(frame)

            if joints is not None:
                frame = draw_pose_on_frame(frame, joints)

        video_writer.write(frame)

        frame_number += 1

    video_capture.release()
    video_writer.release()

    print(f"Zapisano film z wizualizacją: {output_video_path}")