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


def format_debug_value(value, precision=2):
    if value is None:
        return "-"

    if isinstance(value, float):
        return f"{value:.{precision}f}"

    return str(value)


def get_check_message(evaluation, check_name):
    check = evaluation.get("checks", {}).get(check_name)

    if check is None:
        return "-"

    return check.get("message", "-")


def print_analysis_debug_summary(summaries, evaluations, consistency_evaluation):
    print("\n=== PODSUMOWANIE ANALIZY DO OPISU WYNIKÓW ===\n")

    print(
        "rep;"
        "validity;"
        "reasons;"
        "duration_s;"
        "bar_y_range;"
        "median_bar_y_range;"
        "start_knee_angle;"
        "start_hip_angle;"
        "start_back_angle;"
        "top_knee_angle;"
        "top_hip_angle;"
        "top_back_angle;"
        "back_angle_change;"
        "shoulder_below_hip_at_start;"
        "start_position_message;"
        "start_torso_message;"
        "bar_range_message;"
        "hip_lockout_message;"
        "knee_lockout_message"
    )

    evaluations_by_rep = {
        evaluation["rep_number"]: evaluation
        for evaluation in evaluations
    }

    for summary in summaries:
        rep_number = summary["rep_number"]
        evaluation = evaluations_by_rep.get(rep_number, {})

        reasons = evaluation.get("validity_reasons", [])
        reasons_text = ", ".join(reasons) if reasons else "-"

        print(
            f"{rep_number};"
            f"{evaluation.get('rep_validity', '-')};"
            f"{reasons_text};"
            f"{format_debug_value(summary.get('duration_seconds'))};"
            f"{format_debug_value(summary.get('bar_y_range'), 3)};"
            f"{format_debug_value(summary.get('median_bar_y_range'), 3)};"
            f"{format_debug_value(summary.get('lifting_start_knee_angle'))};"
            f"{format_debug_value(summary.get('lifting_start_hip_angle'))};"
            f"{format_debug_value(summary.get('lifting_start_back_angle'))};"
            f"{format_debug_value(summary.get('top_knee_angle'))};"
            f"{format_debug_value(summary.get('top_hip_angle'))};"
            f"{format_debug_value(summary.get('top_back_angle'))};"
            f"{format_debug_value(summary.get('back_angle_change'))};"
            f"{summary.get('shoulder_below_hip_at_start')};"
            f"{get_check_message(evaluation, 'start_position')};"
            f"{get_check_message(evaluation, 'start_torso_position')};"
            f"{get_check_message(evaluation, 'bar_range')};"
            f"{get_check_message(evaluation, 'hip_lockout')};"
            f"{get_check_message(evaluation, 'knee_lockout')}"
        )

    print("\n=== OCENA SPÓJNOŚCI SERII ===\n")

    print(f"overall_status={consistency_evaluation.get('overall_status', '-')}")

    for check_name, check in consistency_evaluation.get("checks", {}).items():
        print(
            f"{check_name};"
            f"{check.get('status', '-')};"
            f"{check.get('message', '-')}"
        )

    print("\n=== KONIEC PODSUMOWANIA ===\n")


class DeadliftAnalyzer:
    """
    Main service class for deadlift video analysis.
    This class does not use a fixed video path.
    The video path is passed from outside, for example from Django after upload.
    """

    def __init__(self, estimator=None, debug_print=False):
        self.estimator = estimator or PoseEstimator()
        self.debug_print = debug_print

    def analyze(self, video_path: str) -> dict:
        timeline = analyze_video(video_path, self.estimator)

        repetitions = detect_repetitions(timeline)

        timeline = assign_repetitions_to_timeline(
            timeline,
            repetitions,
        )

        summaries = summarize_repetitions(
            timeline,
            repetitions,
        )

        evaluations = evaluate_repetitions(summaries)

        consistency_evaluation = evaluate_repetition_consistency(summaries)

        if self.debug_print:
            print_analysis_debug_summary(
                summaries,
                evaluations,
                consistency_evaluation,
            )

        return {
            "repetitions_count": len(repetitions),
            "timeline": timeline,
            "repetitions": repetitions,
            "summaries": summaries,
            "evaluations": evaluations,
            "consistency_evaluation": consistency_evaluation,
        }