from constants import (
    REP_PHASE_PREPARATION,
    REP_PHASE_LIFTING,
    REP_PHASE_LOWERING,
)

def get_item_closest_to_time(items, timestamp):
    if not items:
        return None

    return min(
        items,
        key=lambda item: abs(
            item["timestamp_seconds"] - timestamp
        )
    )

def get_timeline_items_for_repetition(timeline, rep_number):
    return [
        item for item in timeline
        if item.get("rep_number") == rep_number
        and item.get("pose_detected")
        and item.get("metrics") is not None
    ]

def get_phase_items(items, phase):
    return [
        item for item in items
        if item.get("rep_phase") == phase
    ]


def get_first_timestamp(items):
    if not items:
        return None

    return items[0]["timestamp_seconds"]


def get_last_timestamp(items):
    if not items:
        return None

    return items[-1]["timestamp_seconds"]


def calculate_duration_from_items(items):
    if len(items) < 2:
        return 0.0

    return (
        items[-1]["timestamp_seconds"]
        - items[0]["timestamp_seconds"]
    )

def get_metric_values(items, metric_name):
    values = []

    for item in items:
        value = item["metrics"].get(metric_name)

        if value is not None:
            values.append(value)

    return values


def get_bar_y_values(items):
    values = []

    for item in items:
        bar_position = item.get("bar_position")

        if bar_position is not None:
            values.append(bar_position["y"])

    return values


def calculate_min_max_change(values):
    if not values:
        return {
            "min": None,
            "max": None,
            "change": None,
        }

    min_value = min(values)
    max_value = max(values)

    return {
        "min": min_value,
        "max": max_value,
        "change": max_value - min_value,
    }

def summarize_repetition(timeline, repetition):
    rep_number = repetition["rep_number"]

    items = get_timeline_items_for_repetition(
        timeline,
        rep_number,
    )

    preparation_items = get_phase_items(
        items,
        REP_PHASE_PREPARATION,
    )

    lifting_items = get_phase_items(
        items,
        REP_PHASE_LIFTING,
    )

    lowering_items = get_phase_items(
        items,
        REP_PHASE_LOWERING,
    )

    top_item = get_item_closest_to_time(
        items,
        repetition["top_time"],
    )
    top_hip_angle = None
    top_knee_angle = None
    top_back_angle = None

    if top_item is not None:
        top_hip_angle = top_item["metrics"].get(
            "hip_angle"
        )

        top_knee_angle = top_item["metrics"].get(
            "knee_angle"
        )

        top_back_angle = top_item["metrics"].get(
            "back_inclination_angle"
        )

    back_values = get_metric_values(items, "back_inclination_angle")
    hip_values = get_metric_values(items, "hip_angle")
    knee_values = get_metric_values(items, "knee_angle")
    bar_y_values = get_bar_y_values(items)

    back_summary = calculate_min_max_change(back_values)
    hip_summary = calculate_min_max_change(hip_values)
    knee_summary = calculate_min_max_change(knee_values)
    bar_y_summary = calculate_min_max_change(bar_y_values)

    preparation_start_time = get_first_timestamp(preparation_items)
    lifting_start_time = get_first_timestamp(lifting_items)
    top_time = get_last_timestamp(lifting_items)
    lowering_end_time = get_last_timestamp(lowering_items)

    preparation_duration = calculate_duration_from_items(preparation_items)
    lifting_duration = calculate_duration_from_items(lifting_items)
    lowering_duration = calculate_duration_from_items(lowering_items)

    total_duration = 0.0

    if lifting_start_time is not None and lowering_end_time is not None:
        total_duration = lowering_end_time - lifting_start_time

    return {
        "rep_number": rep_number,

        "preparation_start_time": preparation_start_time,
        "lifting_start_time": lifting_start_time,
        "top_time": top_time,
        "lowering_end_time": lowering_end_time,

        "duration_seconds": total_duration,
        "preparation_duration_seconds": preparation_duration,
        "lifting_duration_seconds": lifting_duration,
        "lowering_duration_seconds": lowering_duration,

        "bar_y_min": bar_y_summary["min"],
        "bar_y_max": bar_y_summary["max"],
        "bar_y_range": bar_y_summary["change"],

        "back_angle_min": back_summary["min"],
        "back_angle_max": back_summary["max"],
        "back_angle_change": back_summary["change"],

        "hip_angle_min": hip_summary["min"],
        "hip_angle_max": hip_summary["max"],
        "hip_angle_change": hip_summary["change"],

        "knee_angle_min": knee_summary["min"],
        "knee_angle_max": knee_summary["max"],
        "knee_angle_change": knee_summary["change"],

        "top_hip_angle": top_hip_angle,
        "top_knee_angle": top_knee_angle,
        "top_back_angle": top_back_angle,
    }


def summarize_repetitions(timeline, repetitions):
    return [
        summarize_repetition(timeline, repetition)
        for repetition in repetitions
    ]


def print_repetition_summaries(summaries):
    if not summaries:
        print("\nBrak podsumowań powtórzeń.")
        return

    print("\nRepetition summaries:\n")

    for summary in summaries:
        print(
            f"rep={summary['rep_number']:2d} | "
            f"duration={summary['duration_seconds']:5.2f}s | "
            f"prep={summary['preparation_duration_seconds']:5.2f}s | "
            f"lifting={summary['lifting_duration_seconds']:5.2f}s | "
            f"lowering={summary['lowering_duration_seconds']:5.2f}s | "
            f"bar_range={summary['bar_y_range']:.3f} | "
            f"back_change={summary['back_angle_change']:.2f}° | "
            f"hip_change={summary['hip_angle_change']:.2f}° | "
            f"knee_change={summary['knee_angle_change']:.2f}°"
        )