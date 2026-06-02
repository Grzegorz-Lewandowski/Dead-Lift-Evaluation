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


class DeadliftAnalyzer:
    """
    Main service class for deadlift video analysis.

    This class does not use a fixed video path.
    The video path is passed from outside, for example from Django after upload.
    """

    def __init__(self, estimator=None):
        self.estimator = estimator or PoseEstimator()

    def analyze(self, video_path: str) -> dict:
        timeline = analyze_video(video_path, self.estimator)

        repetitions = detect_repetitions(timeline)
        timeline = assign_repetitions_to_timeline(timeline, repetitions)

        summaries = summarize_repetitions(timeline, repetitions)

        evaluations = evaluate_repetitions(summaries)
        consistency_evaluation = evaluate_repetition_consistency(summaries)

        return {
            "repetitions_count": len(repetitions),
            "evaluations": evaluations,
            "consistency_evaluation": consistency_evaluation,
        }