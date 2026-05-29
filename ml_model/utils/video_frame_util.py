import cv2


def iter_video_frames(video_path, frame_stride=1):
    """
    Iteruje po klatkach filmu.

    Zwraca:
    - frame_number
    - timestamp_seconds
    - frame
    """

    video_capture = cv2.VideoCapture(video_path)

    if not video_capture.isOpened():
        raise FileNotFoundError(
            f"Nie udało się otworzyć filmu: {video_path}"
        )

    fps = video_capture.get(cv2.CAP_PROP_FPS)

    frame_number = 0

    while True:
        success, frame = video_capture.read()

        if not success:
            break

        if frame_number % frame_stride == 0:
            timestamp_seconds = frame_number / fps if fps else 0.0

            yield frame_number, timestamp_seconds, frame

        frame_number += 1

    video_capture.release()