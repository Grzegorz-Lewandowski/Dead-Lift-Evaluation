
# --------- CONSTANTS ---------

# --- SIDES ---

LEFT = "left"
RIGHT = "right"

SIDES = (
    LEFT,
    RIGHT,
)

# --- JOINT PARTS USED FOR SIDE SELECTION ---

SIDE_SELECTION_JOINT_PARTS = (
    "shoulder",
    "wrist",
    "hip",
    "knee",
    "ankle",
)

# --- ANGLES DEFINITIONS ---

ANGLE_DEFINITIONS = {
    # KNEE

    "right_knee_angle": (
        "right_hip",
        "right_knee",
        "right_ankle",
    ),

    "left_knee_angle": (
        "left_hip",
        "left_knee",
        "left_ankle",
    ),

    # HIP

    "right_hip_angle": (
        "right_shoulder",
        "right_hip",
        "right_knee",
    ),

    "left_hip_angle": (
        "left_shoulder",
        "left_hip",
        "left_knee",
    ),

    # SHOULDER

    "right_shoulder_angle": (
        "right_hip",
        "right_shoulder",
        "right_wrist",
    ),

    "left_shoulder_angle": (
        "left_hip",
        "left_shoulder",
        "left_wrist",
    ),
}

# mapowanie nazw stawów na ID MediaPipe

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

# lista ważnych stawów

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

# skeleton connectors opisany nazwami

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

MODEL_PATH = "models/pose_landmarker_lite.task"
DEFAULT_IMAGE_PATH = "sample.jpg"
DEFAULT_VISUALIZATION_OUTPUT_PATH = "output_visualization.png"

MIN_VISIBILITY_THRESHOLD = 0.5