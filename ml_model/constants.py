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

MODEL_PATH = "models/pose_landmarker_heavy.task"
DEFAULT_IMAGE_PATH = "tests/test_data/front.jpeg"
DEFAULT_VISUALIZATION_OUTPUT_PATH = "tests/test_data/output_visualization.png"
DEFAULT_VIDEO_PATH = "tests/test_data/pants_side.MOV"
DEFAULT_OUTPUT_VIDEO_PATH = "tests/test_data/output_video.mp4"

# --- ANALYSIS PARAMS ---

VIDEO_FRAME_STRIDE = 5
MIN_VISIBILITY_THRESHOLD = 0.5

# -- BARBEL AND REPETITION ---

BAR_POSITION_METHOD = "wrist_midpoint"
BAR_Y_SMOOTHING_WINDOW_SIZE = 5
REPETITION_BOTTOM_TOLERANCE = 0.08
MIN_REP_DURATION_SECONDS = 1.0

REPETITION_EXTREMA_WINDOW_SIZE = 2
MIN_REPETITION_VERTICAL_RANGE = 0.12
MIN_REP_DURATION_SECONDS = 1.0

REP_PHASE_LIFTING = "lifting"
REP_PHASE_LOWERING = "lowering"