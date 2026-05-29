from analysis.side_selection import select_better_visible_side
from analysis.biomechanical_metrics import calculate_single_side_biomechanical_metrics
from utils.video_frame_util import iter_video_frames
from constants import VIDEO_FRAME_STRIDE
from analysis.barbell_metrics import calculate_bar_position


def analyze_video(video_path, estimator, frame_stride=VIDEO_FRAME_STRIDE):
    timeline = []

    for frame_number, timestamp_seconds, frame in iter_video_frames(
        video_path,
        frame_stride=frame_stride,
    ):
        joints = estimator.detect_pose_from_frame(frame)

        if joints is None:
            timeline.append({
                "frame_number": frame_number,
                "timestamp_seconds": timestamp_seconds,
                "pose_detected": False,
                "selected_side": None,
                "metrics": None,
                "bar_position": None,
            })
            continue

        selected_side = select_better_visible_side(joints)

        metrics = calculate_single_side_biomechanical_metrics(
            joints,
            selected_side,
        )

        bar_position = calculate_bar_position(joints)

        timeline.append({
            "frame_number": frame_number,
            "timestamp_seconds": timestamp_seconds,
            "pose_detected": True,
            "selected_side": selected_side,
            "metrics": metrics,
            "bar_position": bar_position,
        })

    return timeline


def print_video_timeline(timeline):
    print("\nVideo analysis timeline:\n")

    for item in timeline:
        frame = item["frame_number"]
        time = item["timestamp_seconds"]
        rep_number = item.get("rep_number")
        rep_phase = item.get("rep_phase")

        rep_display = "-" if rep_number is None else str(rep_number)
        phase_display = "-" if rep_phase is None else rep_phase

        if not item["pose_detected"]:
            print(
                f"frame={frame:5d} | "
                f"time={time:6.2f}s | "
                f"rep={rep_display:>2s} | "
                f"phase={phase_display:8s} | "
                f"pose not detected"
            )
            continue

        metrics = item["metrics"]
        side = item["selected_side"]

        print(
            f"frame={frame:5d} | "
            f"time={time:6.2f}s | "
            f"rep={rep_display:>2s} | "
            f"phase={phase_display:8s} | "
            f"side={side:5s} | "
            f"knee={metrics['knee_angle']:7.2f}° | "
            f"hip={metrics['hip_angle']:7.2f}° | "
            f"back={metrics['back_inclination_angle']:7.2f}°"
        )

