import os

import matplotlib.pyplot as plt


def create_repetition_bar_y_plot(timeline, repetitions):
    valid_points = []

    for item in timeline:
        if not item.get("pose_detected"):
            continue

        bar_position = item.get("bar_position") or {}

        if bar_position.get("y") is None:
            continue

        valid_points.append({
            "frame_number": item.get("frame_number"),
            "timestamp_seconds": item.get("timestamp_seconds"),
            "bar_y": bar_position.get("y"),
        })

    if not valid_points:
        print("No valid bar_y points found. Chart was not generated.")
        return

    smoothed_bar_y_by_frame = calculate_smoothed_bar_y(valid_points)

    timestamps = []
    smoothed_values = []

    for point in valid_points:
        frame_number = point["frame_number"]
        smoothed_value = smoothed_bar_y_by_frame.get(frame_number)

        if smoothed_value is None:
            continue

        timestamps.append(point["timestamp_seconds"])
        smoothed_values.append(smoothed_value)

    output_path = "ml_model/visualizations/bar_y_repetition_detection.png"
    os.makedirs("ml_model/visualizations", exist_ok=True)

    plt.figure(figsize=(12, 6))

    plt.plot(
        timestamps,
        smoothed_values,
        linewidth=2,
        label="Wygładzona pozycja sztangi"
    )

    for repetition in repetitions:
        rep_number = repetition.get("rep_number")

        preparation_start_time = repetition.get("preparation_start_time")
        lifting_start_time = repetition.get("lifting_start_time")
        top_time = repetition.get("top_time")
        lowering_end_time = repetition.get("lowering_end_time")

        if lifting_start_time is not None:
            plt.axvline(lifting_start_time, linestyle="--", linewidth=1)

        if top_time is not None:
            plt.axvline(top_time, linestyle=":", linewidth=1)

            plt.text(
                top_time,
                min(smoothed_values),
                str(rep_number),
                ha="center",
                va="bottom",
                fontsize=8
            )

        if lowering_end_time is not None:
            plt.axvline(lowering_end_time, linestyle="-.", linewidth=1)

        if preparation_start_time is not None and lowering_end_time is not None:
            plt.axvspan(
                preparation_start_time,
                lowering_end_time,
                alpha=0.06
            )

    plt.title("Przebieg pionowej pozycji sztangi w czasie")
    plt.xlabel("Czas nagrania [s]")
    plt.ylabel("Współrzędna bar_y")

    # W obrazie wartość 0 znajduje się u góry, a 1 na dole.
    # Odwrócenie osi ułatwia interpretację ruchu sztangi.
    plt.gca().invert_yaxis()

    plt.grid(True, linewidth=0.5)
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved repetition bar_y chart to: {output_path}")


def calculate_smoothed_bar_y(valid_points):
    smoothed_bar_y_by_frame = {}

    window_radius = 2

    for index, point in enumerate(valid_points):
        window_start = max(0, index - window_radius)
        window_end = min(len(valid_points), index + window_radius + 1)

        window_points = valid_points[window_start:window_end]

        window_values = [
            window_point["bar_y"]
            for window_point in window_points
            if window_point.get("bar_y") is not None
        ]

        if not window_values:
            continue

        smoothed_value = sum(window_values) / len(window_values)
        smoothed_bar_y_by_frame[point["frame_number"]] = smoothed_value

    return smoothed_bar_y_by_frame