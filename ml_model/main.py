from analysis.pose_estimation import PoseEstimator
from analysis.video_analysis import analyze_video, print_video_timeline
from utils.video_visualization_util import create_annotated_video
from analysis.repetition_detection import (
    detect_repetitions,
    assign_repetitions_to_timeline,
    print_detected_repetitions,
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

    print_video_timeline(timeline)
    print_detected_repetitions(repetitions)

    create_annotated_video(
        DEFAULT_VIDEO_PATH,
        DEFAULT_OUTPUT_VIDEO_PATH,
        estimator,
    )


if __name__ == "__main__":
    main()