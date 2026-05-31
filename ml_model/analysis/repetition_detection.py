from constants import (
    REPETITION_EXTREMA_WINDOW_SIZE,
    MIN_REPETITION_VERTICAL_RANGE,
    MIN_REP_DURATION_SECONDS,
    BAR_Y_SMOOTHING_WINDOW_SIZE,
    BOTTOM_ZONE_RATIO,
    PREPARATION_LOOKBACK_SECONDS,
    MIN_LIFTING_BAR_Y_CHANGE,
    REP_PHASE_IDLE,
    REP_PHASE_PREPARATION,
    REP_PHASE_LIFTING,
    REP_PHASE_LOWERING,
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


def calculate_bottom_zone_threshold(points):
    bottom_y = max(point["bar_y"] for point in points)
    top_y = min(point["bar_y"] for point in points)

    movement_range = bottom_y - top_y

    return bottom_y - (movement_range * BOTTOM_ZONE_RATIO)


def find_lifting_start_between(points, bottom_point, top_point):
    """
    Szuka faktycznego startu podnoszenia:
    pierwszej klatki po dole, gdzie sztanga opuściła bottom zone
    i przesunęła się wystarczająco w górę.
    """

    points_between = [
        point for point in points
        if bottom_point["timestamp_seconds"] <= point["timestamp_seconds"] <= top_point["timestamp_seconds"]
    ]

    if len(points_between) < 2:
        return bottom_point

    bottom_y = bottom_point["bar_y"]
    required_y = bottom_y - MIN_LIFTING_BAR_Y_CHANGE

    for point in points_between:
        if point["bar_y"] <= required_y:
            return point

    return points_between[0]


def find_preparation_start(points, bottom_point, lifting_start_point, bottom_zone_threshold):
    """
    Preparation = czas przed oderwaniem sztangi, gdy zawodnik jest w okolicy dołu.
    Nie próbujemy jeszcze wykrywać pracy biodra; bierzemy krótki setup przed lifting_start,
    ograniczony bottom zone i lookbackiem czasowym.
    """

    earliest_time = lifting_start_point["timestamp_seconds"] - PREPARATION_LOOKBACK_SECONDS

    candidates = [
        point for point in points
        if earliest_time <= point["timestamp_seconds"] <= lifting_start_point["timestamp_seconds"]
        and point["bar_y"] >= bottom_zone_threshold
    ]

    if not candidates:
        return bottom_point

    return candidates[0]


def build_repetitions_from_extrema(points, extrema):
    repetitions = []
    rep_number = 1

    bottom_zone_threshold = calculate_bottom_zone_threshold(points)

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

        lifting_start_point = find_lifting_start_between(
            points,
            first,
            second,
        )

        preparation_start_point = find_preparation_start(
            points,
            first,
            lifting_start_point,
            bottom_zone_threshold,
        )

        duration = third["timestamp_seconds"] - lifting_start_point["timestamp_seconds"]

        has_enough_range = (
            vertical_range_up >= MIN_REPETITION_VERTICAL_RANGE
            and vertical_range_down >= MIN_REPETITION_VERTICAL_RANGE
        )

        has_enough_duration = duration >= MIN_REP_DURATION_SECONDS

        if has_enough_range and has_enough_duration:
            repetitions.append({
                "rep_number": rep_number,

                "preparation_start_frame": preparation_start_point["frame_number"],
                "lifting_start_frame": lifting_start_point["frame_number"],
                "top_frame": second["frame_number"],
                "lowering_end_frame": third["frame_number"],

                "preparation_start_time": preparation_start_point["timestamp_seconds"],
                "lifting_start_time": lifting_start_point["timestamp_seconds"],
                "top_time": second["timestamp_seconds"],
                "lowering_end_time": third["timestamp_seconds"],

                "preparation_duration_seconds": (
                    lifting_start_point["timestamp_seconds"]
                    - preparation_start_point["timestamp_seconds"]
                ),
                "lifting_duration_seconds": (
                    second["timestamp_seconds"]
                    - lifting_start_point["timestamp_seconds"]
                ),
                "lowering_duration_seconds": (
                    third["timestamp_seconds"]
                    - second["timestamp_seconds"]
                ),
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

    repetitions = build_repetitions_from_extrema(
        smoothed_points,
        extrema,
    )

    return repetitions


def assign_repetitions_to_timeline(timeline, repetitions):
    for item in timeline:
        item["rep_number"] = None
        item["rep_phase"] = REP_PHASE_IDLE

    for repetition in repetitions:
        rep_number = repetition["rep_number"]

        preparation_start_frame = repetition["preparation_start_frame"]
        lifting_start_frame = repetition["lifting_start_frame"]
        top_frame = repetition["top_frame"]
        lowering_end_frame = repetition["lowering_end_frame"]

        for item in timeline:
            frame_number = item["frame_number"]

            if preparation_start_frame <= frame_number < lifting_start_frame:
                item["rep_number"] = rep_number
                item["rep_phase"] = REP_PHASE_PREPARATION

            elif lifting_start_frame <= frame_number <= top_frame:
                item["rep_number"] = rep_number
                item["rep_phase"] = REP_PHASE_LIFTING

            elif top_frame < frame_number <= lowering_end_frame:
                item["rep_number"] = rep_number
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
            f"prep={repetition['preparation_start_time']:6.2f}s "
            f"(frame={repetition['preparation_start_frame']:4d}) | "
            f"lift_start={repetition['lifting_start_time']:6.2f}s "
            f"(frame={repetition['lifting_start_frame']:4d}) | "
            f"top={repetition['top_time']:6.2f}s "
            f"(frame={repetition['top_frame']:4d}) | "
            f"end={repetition['lowering_end_time']:6.2f}s "
            f"(frame={repetition['lowering_end_frame']:4d}) | "
            f"prep_dur={repetition['preparation_duration_seconds']:5.2f}s | "
            f"lift_dur={repetition['lifting_duration_seconds']:5.2f}s | "
            f"lower_dur={repetition['lowering_duration_seconds']:5.2f}s"
        )