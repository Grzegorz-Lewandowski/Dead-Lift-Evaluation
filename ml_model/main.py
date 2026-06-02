from analysis.deadlift_analyzer import DeadliftAnalyzer
from utils.video_visualization_util import create_annotated_video

from constants import (
    DEFAULT_VIDEO_PATH,
    DEFAULT_OUTPUT_VIDEO_PATH,
)


def main():
    analyzer = DeadliftAnalyzer()

    result = analyzer.analyze(DEFAULT_VIDEO_PATH)

    print("\nTechnique evaluation:\n")
    for evaluation in result["evaluations"]:
        print(
            f"rep={evaluation['rep_number']:2d} | "
            f"status={evaluation['overall_status']}"
        )

        for check_name, check_result in evaluation["checks"].items():
            print(
                f"  - {check_name:25s} | "
                f"{check_result['status']:7s} | "
                f"{check_result['message']}"
            )

        print()

    print("\nSeries consistency evaluation:\n")
    consistency = result["consistency_evaluation"]

    print(f"status={consistency['overall_status']}")

    for check_name, check_result in consistency["checks"].items():
        print(
            f"  - {check_name:25s} | "
            f"{check_result['status']:7s} | "
            f"{check_result['message']}"
        )

    create_annotated_video(
        DEFAULT_VIDEO_PATH,
        DEFAULT_OUTPUT_VIDEO_PATH,
        analyzer.estimator,
    )


if __name__ == "__main__":
    main()