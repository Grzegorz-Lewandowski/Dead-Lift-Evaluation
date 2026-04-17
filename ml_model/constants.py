IMPORTANT_JOINTS = {
    11: "left_shoulder",
    12: "right_shoulder",
    15: "left_wrist",
    16: "right_wrist",
    23: "left_hip",
    24: "right_hip",
    25: "left_knee",
    26: "right_knee",
    27: "left_ankle",
    28: "right_ankle",
}

SKELETON_CONNECTIONS = [
    (11, 12),
    (11, 23),
    (12, 24),
    (23, 24),
    (23, 25),
    (25, 27),
    (24, 26),
    (26, 28),
    (15, 11),
    (16, 11)
]

MODEL_PATH = "models/pose_landmarker_lite.task"
DEFAULT_IMAGE_PATH = "sample.jpg"
DEFAULT_VISUALIZATION_OUTPUT_PATH = "output_visualization.png"

MIN_VISIBILITY_THRESHOLD = 0.5