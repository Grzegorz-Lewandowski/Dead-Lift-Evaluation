import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ML_MODEL_ROOT = PROJECT_ROOT / "ml_model"

if str(ML_MODEL_ROOT) not in sys.path:
    sys.path.append(str(ML_MODEL_ROOT))


from analysis.deadlift_analyzer import DeadliftAnalyzer


def run_deadlift_analysis(video_path: str) -> dict:
    """
    Runs real deadlift analysis based on uploaded video file.

    The video_path comes from Django upload:
    analysis.video.path
    """

    analyzer = DeadliftAnalyzer()
    result = analyzer.analyze(video_path)

    return make_json_serializable(result)


def make_json_serializable(value):
    """
    Converts values returned by numpy / OpenCV / ML logic into normal Python types
    accepted by Django JSONField.
    """

    if isinstance(value, dict):
        return {
            str(key): make_json_serializable(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            make_json_serializable(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return [
            make_json_serializable(item)
            for item in value
        ]

    if hasattr(value, "item"):
        return value.item()

    return value