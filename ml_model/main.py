from analysis.deadlift_analyzer import DeadliftAnalyzer
from analysis.video_analysis import print_video_timeline
from analysis.repetition_detection import print_detected_repetitions
from analysis.repetition_summary import print_repetition_summaries
from utils.video_visualization_util import create_annotated_video

from constants import (
    DEFAULT_VIDEO_PATH,
    DEFAULT_OUTPUT_VIDEO_PATH,
)


def print_technique_evaluations(evaluations):
    print("\nTechnique evaluation:\n")

    for evaluation in evaluations:
        print(
            f"rep={evaluation['rep_number']:2d} | "
            f"status={evaluation['overall_status']} | validity={evaluation['rep_validity']}"
        )

        for check_name, check_result in evaluation["checks"].items():
            print(
                f"  - {check_name:25s} | "
                f"{check_result['status']:7s} | "
                f"{check_result['message']}"
            )

        print()


def print_consistency_evaluation(consistency):
    print("\nSeries consistency evaluation:\n")

    print(f"status={consistency['overall_status']}")

    for check_name, check_result in consistency["checks"].items():
        print(
            f"  - {check_name:25s} | "
            f"{check_result['status']:7s} | "
            f"{check_result['message']}"
        )


def main():
    analyzer = DeadliftAnalyzer()

    result = analyzer.analyze(DEFAULT_VIDEO_PATH)

    print_video_timeline(result["timeline"])
    print_detected_repetitions(result["repetitions"])
    print_repetition_summaries(result["summaries"])

    print_technique_evaluations(result["evaluations"])
    print_consistency_evaluation(result["consistency_evaluation"])

    create_annotated_video(
        DEFAULT_VIDEO_PATH,
        DEFAULT_OUTPUT_VIDEO_PATH,
        analyzer.estimator,
    )


if __name__ == "__main__":
    main()