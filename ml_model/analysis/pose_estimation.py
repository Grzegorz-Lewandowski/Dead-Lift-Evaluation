import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from constants import MODEL_PATH


class PoseEstimator:
    def __init__(self):
        base_options = python.BaseOptions(
            model_asset_path=MODEL_PATH
        )

        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE
        )

        self.detector = vision.PoseLandmarker.create_from_options(options)

    def detect_pose_from_image(self, image_path):
        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(
                f"Nie udało się wczytać obrazu: {image_path}"
            )

        return self.detect_pose_from_frame(image)

    def detect_pose_from_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        result = self.detector.detect(mp_image)

        if not result.pose_landmarks:
            return None

        detected_pose_landmarks = result.pose_landmarks[0]

        return self.extract_joint_data(detected_pose_landmarks)

    def extract_joint_data(self, landmarks):
        joint_data = {}

        for i, landmark in enumerate(landmarks):
            joint_data[i] = {
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z,
                "visibility": landmark.visibility
            }

        return joint_data