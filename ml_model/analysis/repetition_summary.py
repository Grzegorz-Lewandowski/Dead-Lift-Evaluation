from constants import (
    REP_PHASE_PREPARATION,
    REP_PHASE_LIFTING,
    REP_PHASE_LOWERING,
)
from utils.joint_utils import get_joint_data

def get_joint_from_item(item, joint_name):
    if item is None:
        return None

    joints = item.get("joints")

    if joints is None:
        return None

    return get_joint_data(joints, joint_name)

def get_timeline_items_for_repetition(timeline, rep_number):
    return [
        item for item in timeline
        if item.get("rep_number") == rep_number
        and item.get("pose_detected")
        and item.get("metrics") is not None
    ]

def get_joint_from_item(item, joint_name):
    if item is None:
        return None

    joints = item.get("joints")

    if joints is None:
        return None

    from utils.joint_utils import get_joint_data

    return get_joint_data(joints, joint_name)

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


def get_item_closest_to_time(items, timestamp):
    if not items or timestamp is None:
        return None

    return min(
        items,
        key=lambda item: abs(
            item["timestamp_seconds"] - timestamp
        )
    )


def get_metric_from_item(item, metric_name):
    if item is None:
        return None

    metrics = item.get("metrics")

    if metrics is None:
        return None

    return metrics.get(metric_name)


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

    top_item = get_item_closest_to_time(
        items,
        top_time,
    )

    lifting_start_item = get_item_closest_to_time(
        items,
        lifting_start_time,
    )

    top_hip_angle = get_metric_from_item(top_item, "hip_angle")
    top_knee_angle = get_metric_from_item(top_item, "knee_angle")
    top_back_angle = get_metric_from_item(
        top_item,
        "back_inclination_angle",
    )

    lifting_start_hip_angle = get_metric_from_item(
        lifting_start_item,
        "hip_angle",
    )

    lifting_start_knee_angle = get_metric_from_item(
        lifting_start_item,
        "knee_angle",
    )

    lifting_start_back_angle = get_metric_from_item(
        lifting_start_item,
        "back_inclination_angle",
    )

    selected_side = None

    if lifting_start_item is not None:
        selected_side = lifting_start_item.get("selected_side")

    lifting_start_shoulder_y = None
    lifting_start_hip_y = None
    shoulder_below_hip_at_start = None

    if selected_side is not None:
        shoulder = get_joint_from_item(
            lifting_start_item,
            f"{selected_side}_shoulder",
        )

        hip = get_joint_from_item(
            lifting_start_item,
            f"{selected_side}_hip",
        )

        if shoulder is not None and hip is not None:
            lifting_start_shoulder_y = shoulder["y"]
            lifting_start_hip_y = hip["y"]

            shoulder_below_hip_at_start = (
                lifting_start_shoulder_y > lifting_start_hip_y
            )

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

        "lifting_start_hip_angle": lifting_start_hip_angle,
        "lifting_start_knee_angle": lifting_start_knee_angle,
        "lifting_start_back_angle": lifting_start_back_angle,

        "lifting_start_shoulder_y": lifting_start_shoulder_y,
        "lifting_start_hip_y": lifting_start_hip_y,
        "shoulder_below_hip_at_start": shoulder_below_hip_at_start,
    }

def summarize_repetitions(timeline, repetitions):
    return [
        summarize_repetition(timeline, repetition)
        for repetition in repetitions
    ]


def format_number(value, precision=2):
    if value is None:
        return "-"

    return f"{value:.{precision}f}"


def print_repetition_summaries(summaries):
    if not summaries:
        print("\nBrak podsumowań powtórzeń.")
        return

    print("\nRepetition summaries:\n")

    for summary in summaries:
        print(
            f"rep={summary['rep_number']:2d} | "
            f"duration={format_number(summary['duration_seconds'])}s | "
            f"prep={format_number(summary['preparation_duration_seconds'])}s | "
            f"lifting={format_number(summary['lifting_duration_seconds'])}s | "
            f"lowering={format_number(summary['lowering_duration_seconds'])}s | "
            f"bar_range={format_number(summary['bar_y_range'], 3)} | "
            f"back_change={format_number(summary['back_angle_change'])}° | "
            f"hip_change={format_number(summary['hip_angle_change'])}° | "
            f"knee_change={format_number(summary['knee_angle_change'])}° | "
            f"top_hip={format_number(summary['top_hip_angle'])}° | "
            f"top_knee={format_number(summary['top_knee_angle'])}° | "
            f"start_knee={format_number(summary['lifting_start_knee_angle'])}°"
        )