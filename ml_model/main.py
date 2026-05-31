from analysis.pose_estimation import PoseEstimator
from analysis.video_analysis import analyze_video, print_video_timeline
from utils.video_visualization_util import create_annotated_video
from analysis.repetition_detection import (
    detect_repetitions,
    assign_repetitions_to_timeline,
    print_detected_repetitions,
)
from analysis.repetition_summary import (
    summarize_repetitions,
    print_repetition_summaries,
)

from analysis.technique_evaluation import (
    evaluate_repetitions,
    evaluate_repetition_consistency,
    print_technique_evaluations,
    print_consistency_evaluation,
)

from constants import (
    DEFAULT_VIDEO_PATH,
    DEFAULT_OUTPUT_VIDEO_PATH,
)


def main():
    estimator = PoseEstimator()

    timeline = analyze_video(DEFAULT_VIDEO_PATH, estimator)

    repetitions = detect_repetitions(timeline)
    timeline = assign_repetitions_to_timeline(timeline, repetitions)

    summaries = summarize_repetitions(timeline, repetitions)
    evaluations = evaluate_repetitions(summaries)
    consistency_evaluation = evaluate_repetition_consistency(summaries)

    print_video_timeline(timeline)
    print_detected_repetitions(repetitions)
    print_repetition_summaries(summaries)
    print_technique_evaluations(evaluations)
    print_consistency_evaluation(consistency_evaluation)

    create_annotated_video(
        DEFAULT_VIDEO_PATH,
        DEFAULT_OUTPUT_VIDEO_PATH,
        estimator,
    )


if __name__ == "__main__":
    main()