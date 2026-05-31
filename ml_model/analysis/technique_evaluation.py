from constants import (
    EVALUATION_STATUS_OK,
    EVALUATION_STATUS_WARNING,
    EVALUATION_STATUS_INFO,
    MAX_LIFTING_TO_LOWERING_RATIO,
    MIN_BAR_Y_RANGE,
    MAX_TORSO_ANGLE_CHANGE_INFO,
    MAX_TORSO_ANGLE_CHANGE_WARNING,
    MIN_TOP_HIP_ANGLE,
    MIN_TOP_KNEE_ANGLE,
    MAX_BAR_RANGE_VARIATION,
    MAX_REP_DURATION_VARIATION,
    MAX_TOP_HIP_ANGLE_VARIATION,
    MAX_TOP_KNEE_ANGLE_VARIATION,
)

def evaluate_repetition_consistency(summaries):
    bar_range_variation = calculate_value_range(
        summaries,
        "bar_y_range",
    )

    duration_variation = calculate_value_range(
        summaries,
        "duration_seconds",
    )

    hip_lockout_variation = calculate_value_range(
        summaries,
        "top_hip_angle",
    )

    knee_lockout_variation = calculate_value_range(
        summaries,
        "top_knee_angle",
    )

    checks = {}

    if bar_range_variation is not None:
        checks["bar_range_consistency"] = {
            "status": (
                EVALUATION_STATUS_OK
                if bar_range_variation <= MAX_BAR_RANGE_VARIATION
                else EVALUATION_STATUS_WARNING
            ),
            "message": (
                f"Różnica zakresu ruchu sztangi między powtórzeniami: "
                f"{bar_range_variation:.3f}."
            ),
        }

    if duration_variation is not None:
        checks["duration_consistency"] = {
            "status": (
                EVALUATION_STATUS_OK
                if duration_variation <= MAX_REP_DURATION_VARIATION
                else EVALUATION_STATUS_INFO
            ),
            "message": (
                f"Różnica czasu trwania powtórzeń: "
                f"{duration_variation:.2f}s."
            ),
        }

    if hip_lockout_variation is not None:
        checks["hip_lockout_consistency"] = {
            "status": (
                EVALUATION_STATUS_OK
                if hip_lockout_variation <= MAX_TOP_HIP_ANGLE_VARIATION
                else EVALUATION_STATUS_WARNING
            ),
            "message": (
                f"Różnica kąta biodra w górnej pozycji: "
                f"{hip_lockout_variation:.1f}°."
            ),
        }

    if knee_lockout_variation is not None:
        checks["knee_lockout_consistency"] = {
            "status": (
                EVALUATION_STATUS_OK
                if knee_lockout_variation <= MAX_TOP_KNEE_ANGLE_VARIATION
                else EVALUATION_STATUS_WARNING
            ),
            "message": (
                f"Różnica kąta kolana w górnej pozycji: "
                f"{knee_lockout_variation:.1f}°."
            ),
        }

    has_warning = any(
        check["status"] == EVALUATION_STATUS_WARNING
        for check in checks.values()
    )

    return {
        "overall_status": (
            EVALUATION_STATUS_WARNING
            if has_warning
            else EVALUATION_STATUS_OK
        ),
        "checks": checks,
    }

def calculate_value_range(summaries, key):
    values = [
        summary[key]
        for summary in summaries
        if summary.get(key) is not None
    ]

    if not values:
        return None

    return max(values) - min(values)

def evaluate_hip_lockout(summary):
    hip_angle = summary["top_hip_angle"]

    if hip_angle is None:
        return {
            "status": EVALUATION_STATUS_WARNING,
            "message": "Nie udało się ocenić wyprostu biodra.",
        }

    if hip_angle >= MIN_TOP_HIP_ANGLE:
        return {
            "status": EVALUATION_STATUS_OK,
            "message": (
                f"Wyprost biodra w górnej pozycji "
                f"({hip_angle:.1f}°)."
            ),
        }

    return {
        "status": EVALUATION_STATUS_WARNING,
        "message": (
            f"Niepełny wyprost biodra "
            f"({hip_angle:.1f}°)."
        ),
    }

def evaluate_knee_lockout(summary):
    knee_angle = summary["top_knee_angle"]

    if knee_angle is None:
        return {
            "status": EVALUATION_STATUS_WARNING,
            "message": "Nie udało się ocenić wyprostu kolana.",
        }

    if knee_angle >= MIN_TOP_KNEE_ANGLE:
        return {
            "status": EVALUATION_STATUS_OK,
            "message": (
                f"Wyprost kolana w górnej pozycji "
                f"({knee_angle:.1f}°)."
            ),
        }

    return {
        "status": EVALUATION_STATUS_WARNING,
        "message": (
            f"Niepełny wyprost kolana "
            f"({knee_angle:.1f}°)."
        ),
    }

def evaluate_torso_angle_change(summary):
    back_change = summary["back_angle_change"]

    if back_change is None:
        return {
            "status": EVALUATION_STATUS_WARNING,
            "message": "Nie udało się ocenić zmiany pochylenia tułowia.",
        }

    if back_change <= MAX_TORSO_ANGLE_CHANGE_INFO:
        return {
            "status": EVALUATION_STATUS_OK,
            "message": "Zmiana pochylenia tułowia mieści się w oczekiwanym zakresie.",
        }

    if back_change <= MAX_TORSO_ANGLE_CHANGE_WARNING:
        return {
            "status": EVALUATION_STATUS_INFO,
            "message": "Widoczna większa zmiana pochylenia tułowia w trakcie powtórzenia.",
        }

    return {
        "status": EVALUATION_STATUS_WARNING,
        "message": "Bardzo duża zmiana pochylenia tułowia — warto sprawdzić kontrolę ruchu bioder i tułowia.",
    }


def evaluate_bar_range(summary):
    bar_range = summary["bar_y_range"]

    if bar_range is None:
        return {
            "status": EVALUATION_STATUS_WARNING,
            "message": "Nie udało się ocenić zakresu ruchu sztangi.",
        }

    if bar_range >= MIN_BAR_Y_RANGE:
        return {
            "status": EVALUATION_STATUS_OK,
            "message": "Zakres pionowego ruchu sztangi wygląda poprawnie.",
        }

    return {
        "status": EVALUATION_STATUS_WARNING,
        "message": "Zakres pionowego ruchu sztangi jest niski — możliwe niepełne powtórzenie.",
    }


def evaluate_tempo(summary):
    lifting_duration = summary["lifting_duration_seconds"]
    lowering_duration = summary["lowering_duration_seconds"]

    if lifting_duration is None or lowering_duration is None:
        return {
            "status": EVALUATION_STATUS_WARNING,
            "message": "Nie udało się ocenić tempa powtórzenia.",
        }

    if lifting_duration == 0 or lowering_duration == 0:
        return {
            "status": EVALUATION_STATUS_WARNING,
            "message": "Jedna z faz ruchu ma zerowy czas trwania.",
        }

    ratio = lowering_duration / lifting_duration

    if ratio <= MAX_LIFTING_TO_LOWERING_RATIO:
        return {
            "status": EVALUATION_STATUS_OK,
            "message": "Tempo faz ruchu wygląda poprawnie.",
        }

    return {
        "status": EVALUATION_STATUS_WARNING,
        "message": "Faza opuszczania jest wyraźnie dłuższa od fazy podnoszenia.",
    }

def evaluate_tempo_info(summary):
    lifting_duration = summary["lifting_duration_seconds"]
    lowering_duration = summary["lowering_duration_seconds"]

    if lifting_duration is None or lowering_duration is None:
        return {
            "status": EVALUATION_STATUS_INFO,
            "message": "Nie udało się określić tempa faz ruchu.",
        }

    return {
        "status": EVALUATION_STATUS_INFO,
        "message": (
            f"Czas podnoszenia: {lifting_duration:.2f}s, "
            f"czas opuszczania: {lowering_duration:.2f}s."
        ),
    }

def evaluate_repetition(summary):
    checks = {
        "hip_lockout": evaluate_hip_lockout(summary),
        "knee_lockout": evaluate_knee_lockout(summary),

        "bar_range": evaluate_bar_range(summary),

        "torso_angle_change": evaluate_torso_angle_change(summary),

        "tempo": evaluate_tempo_info(summary),
    }

    has_warning = any(
        check["status"] == EVALUATION_STATUS_WARNING
        for check in checks.values()
    )

    overall_status = (
        EVALUATION_STATUS_WARNING
        if has_warning
        else EVALUATION_STATUS_OK
    )

    return {
        "rep_number": summary["rep_number"],
        "overall_status": overall_status,
        "checks": checks,
    }


def evaluate_repetitions(summaries):
    return [
        evaluate_repetition(summary)
        for summary in summaries
    ]

def print_consistency_evaluation(evaluation):
    print("\nSeries consistency evaluation:\n")

    print(f"status={evaluation['overall_status']}")

    for check_name, check_result in evaluation["checks"].items():
        print(
            f"  - {check_name:25s} | "
            f"{check_result['status']:7s} | "
            f"{check_result['message']}"
        )

def print_technique_evaluations(evaluations):
    if not evaluations:
        print("\nBrak ocen techniki.")
        return

    print("\nTechnique evaluation:\n")

    for evaluation in evaluations:
        print(
            f"rep={evaluation['rep_number']:2d} | "
            f"status={evaluation['overall_status']}"
        )

        for check_name, check_result in evaluation["checks"].items():
            print(
                f"  - {check_name:16s} | "
                f"{check_result['status']:7s} | "
                f"{check_result['message']}"
            )

        print()