from constants import (
    REPETITION_EXTREMA_WINDOW_SIZE,
    MIN_REPETITION_VERTICAL_RANGE,
    MIN_REP_DURATION_SECONDS,
    REP_PHASE_LIFTING,
    REP_PHASE_LOWERING,
    BAR_Y_SMOOTHING_WINDOW_SIZE,
)

def get_valid_bar_points(timeline):
    points = []

    for item in timeline:
        if not item["pose_detected"]:
            continue

        bar_position = item.get("bar_position")

        if bar_position is None:
            continue

        points.append({
            "frame_number": item["frame_number"],
            "timestamp_seconds": item["timestamp_seconds"],
            "bar_y": bar_position["y"],
        })

    return points


def smooth_bar_y_points(points, window_size=BAR_Y_SMOOTHING_WINDOW_SIZE):
    if window_size <= 1:
        return points

    smoothed_points = []
    half_window = window_size // 2

    for index, point in enumerate(points):
        start_index = max(0, index - half_window)
        end_index = min(len(points), index + half_window + 1)

        window_points = points[start_index:end_index]

        smoothed_bar_y = sum(
            window_point["bar_y"]
            for window_point in window_points
        ) / len(window_points)

        smoothed_point = point.copy()
        smoothed_point["raw_bar_y"] = point["bar_y"]
        smoothed_point["bar_y"] = smoothed_bar_y

        smoothed_points.append(smoothed_point)

    return smoothed_points


def is_local_maximum(points, index, window_size):
    current_y = points[index]["bar_y"]

    for offset in range(1, window_size + 1):
        if current_y <= points[index - offset]["bar_y"]:
            return False

        if current_y <= points[index + offset]["bar_y"]:
            return False

    return True


def is_local_minimum(points, index, window_size):
    current_y = points[index]["bar_y"]

    for offset in range(1, window_size + 1):
        if current_y >= points[index - offset]["bar_y"]:
            return False

        if current_y >= points[index + offset]["bar_y"]:
            return False

    return True


def find_local_extrema(points, window_size=REPETITION_EXTREMA_WINDOW_SIZE):
    extrema = []

    if len(points) < (window_size * 2 + 1):
        return extrema

    for index in range(window_size, len(points) - window_size):
        point = points[index]

        if is_local_maximum(points, index, window_size):
            extrema.append({
                "type": "bottom",
                **point,
            })

        elif is_local_minimum(points, index, window_size):
            extrema.append({
                "type": "top",
                **point,
            })

    return extrema


def build_repetitions_from_extrema(extrema):
    repetitions = []
    rep_number = 1

    index = 0

    while index < len(extrema) - 2:
        first = extrema[index]
        second = extrema[index + 1]
        third = extrema[index + 2]

        valid_sequence = (
            first["type"] == "bottom"
            and second["type"] == "top"
            and third["type"] == "bottom"
        )

        if not valid_sequence:
            index += 1
            continue

        vertical_range_up = first["bar_y"] - second["bar_y"]
        vertical_range_down = third["bar_y"] - second["bar_y"]

        duration = third["timestamp_seconds"] - first["timestamp_seconds"]

        has_enough_range = (
            vertical_range_up >= MIN_REPETITION_VERTICAL_RANGE
            and vertical_range_down >= MIN_REPETITION_VERTICAL_RANGE
        )

        has_enough_duration = duration >= MIN_REP_DURATION_SECONDS

        if has_enough_range and has_enough_duration:
            repetitions.append({
                "rep_number": rep_number,

                "start_frame": first["frame_number"],
                "top_frame": second["frame_number"],
                "end_frame": third["frame_number"],

                "start_time": first["timestamp_seconds"],
                "top_time": second["timestamp_seconds"],
                "end_time": third["timestamp_seconds"],

                "duration_seconds": duration,

                "vertical_range_up": vertical_range_up,
                "vertical_range_down": vertical_range_down,
            })

            rep_number += 1
            index += 2
        else:
            index += 1

    return repetitions


def detect_repetitions(timeline):
    points = get_valid_bar_points(timeline)

    smoothed_points = smooth_bar_y_points(points)

    extrema = find_local_extrema(smoothed_points)

    repetitions = build_repetitions_from_extrema(extrema)

    return repetitions


def assign_repetitions_to_timeline(timeline, repetitions):
    """
    Dodaje do każdego elementu timeline:
    - rep_number
    - rep_phase
    """

    for item in timeline:
        item["rep_number"] = None
        item["rep_phase"] = None

    for repetition in repetitions:
        rep_number = repetition["rep_number"]

        start_frame = repetition["start_frame"]
        top_frame = repetition["top_frame"]
        end_frame = repetition["end_frame"]

        for item in timeline:
            frame_number = item["frame_number"]

            if start_frame <= frame_number <= end_frame:
                item["rep_number"] = rep_number

                if frame_number <= top_frame:
                    item["rep_phase"] = REP_PHASE_LIFTING
                else:
                    item["rep_phase"] = REP_PHASE_LOWERING

    return timeline


def print_detected_repetitions(repetitions):
    if not repetitions:
        print("\nNie wykryto pełnych powtórzeń.")
        return

    print("\nDetected repetitions:\n")

    for repetition in repetitions:
        print(
            f"rep={repetition['rep_number']:2d} | "
            f"start={repetition['start_time']:6.2f}s "
            f"(frame={repetition['start_frame']:4d}) | "
            f"top={repetition['top_time']:6.2f}s "
            f"(frame={repetition['top_frame']:4d}) | "
            f"end={repetition['end_time']:6.2f}s "
            f"(frame={repetition['end_frame']:4d}) | "
            f"duration={repetition['duration_seconds']:5.2f}s | "
            f"range_up={repetition['vertical_range_up']:.3f}"
        )