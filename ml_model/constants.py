# --- SIDES ---

LEFT = "left"
RIGHT = "right"

SIDES = (
    LEFT,
    RIGHT,
)

# --- IMPORTANT JOINTS ---

JOINT_IDS = {
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
}

IMPORTANT_JOINTS = [
    "left_shoulder",
    "right_shoulder",
    "left_wrist",
    "right_wrist",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
]

SKELETON_CONNECTIONS = [
    ("left_shoulder", "left_hip"),
    ("right_shoulder", "right_hip"),
    ("left_hip", "right_hip"),
    ("left_shoulder", "right_shoulder"),
    ("left_hip", "left_knee"),
    ("left_knee", "left_ankle"),
    ("right_hip", "right_knee"),
    ("right_knee", "right_ankle"),
    ("left_wrist", "left_shoulder"),
    ("right_wrist", "right_shoulder"),
]
# --- SIDE SELECTION JOINT PARTS
SIDE_SELECTION_JOINT_PARTS = (
    "shoulder",
    "wrist",
    "hip",
    "knee",
    "ankle",
)

# --- SINGLE-SIDE ANGLE DEFINITIONS ---

SINGLE_SIDE_ANGLE_DEFINITIONS = {
    "knee_angle": (
        "{side}_hip",
        "{side}_knee",
        "{side}_ankle",
    ),
    "hip_angle": (
        "{side}_shoulder",
        "{side}_hip",
        "{side}_knee",
    ),
    "shoulder_angle": (
        "{side}_hip",
        "{side}_shoulder",
        "{side}_wrist",
    ),
}

# --- PATHS ---

MODEL_PATH = "models/pose_landmarker_lite.task"
DEFAULT_IMAGE_PATH = "sample.jpg"
DEFAULT_VISUALIZATION_OUTPUT_PATH = "output_visualization.png"

MIN_VISIBILITY_THRESHOLD = 0.5