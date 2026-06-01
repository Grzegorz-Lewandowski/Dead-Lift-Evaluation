import sys
from pathlib import Path


# Ścieżka do głównego katalogu projektu: Dead-Lift-Evaluation/
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Ścieżka do folderu ml_model/
ML_MODEL_ROOT = PROJECT_ROOT / "ml_model"

# Dodajemy ml_model do sys.path, ponieważ obecny kod importuje np.:
# from analysis.pose_estimation import PoseEstimator
# from constants import ...
if str(ML_MODEL_ROOT) not in sys.path:
    sys.path.append(str(ML_MODEL_ROOT))


from analysis.pose_estimation import PoseEstimator
from analysis.video_analysis import analyze_video
from analysis.repetition_detection import (
    detect_repetitions,
    assign_repetitions_to_timeline,
)
from analysis.repetition_summary import summarize_repetitions
from analysis.technique_evaluation import (
    evaluate_repetitions,
    evaluate_repetition_consistency,
)


def run_deadlift_analysis(video_path: str) -> dict:
    """
    Runs real deadlift analysis based on uploaded video file.

    This function is an adapter between Django API and the existing ml_model code.
    """

    estimator = PoseEstimator()

    timeline = analyze_video(video_path, estimator)

    repetitions = detect_repetitions(timeline)
    timeline = assign_repetitions_to_timeline(timeline, repetitions)

    summaries = summarize_repetitions(timeline, repetitions)

    evaluations = evaluate_repetitions(summaries)
    consistency_evaluation = evaluate_repetition_consistency(summaries)

    result = {
        "repetitions_count": len(repetitions),
        "evaluations": evaluations,
        "consistency_evaluation": consistency_evaluation,
    }

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

    # Obsługa numpy int / float / bool, jeśli wystąpią w wynikach.
    if hasattr(value, "item"):
        return value.item()

    return value