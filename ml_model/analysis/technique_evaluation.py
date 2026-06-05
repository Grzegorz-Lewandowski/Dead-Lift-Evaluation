from constants import (
    EVALUATION_STATUS_OK,
    EVALUATION_STATUS_INFO,
    EVALUATION_STATUS_WARNING,

    REP_VALIDITY_VALID,
    REP_VALIDITY_PARTIAL,
    REP_VALIDITY_INVALID,

    MIN_TOP_HIP_ANGLE,
    MIN_TOP_KNEE_ANGLE,
    BAR_RANGE_COMPLETENESS_RATIO,

    START_POSITION_KNEE_ANGLE_DEEP_OFFSET,
    START_POSITION_KNEE_ANGLE_HIGH_OFFSET,

    MAX_BAR_RANGE_VARIATION,
    MAX_REP_DURATION_VARIATION,
    MAX_TOP_HIP_ANGLE_VARIATION,
    MAX_TOP_KNEE_ANGLE_VARIATION,
)


def calculate_median(values):
    values = sorted(values)

    if not values:
        return None

    middle = len(values) // 2

    if len(values) % 2 == 1:
        return values[middle]

    return (
        values[middle - 1]
        + values[middle]
    ) / 2


def calculate_value_range(summaries, key):
    values = [
        summary[key]
        for summary in summaries
        if summary.get(key) is not None
    ]

    if not values:
        return None

    return max(values) - min(values)


def add_relative_bar_range_context(summaries):
    bar_ranges = [
        summary["bar_y_range"]
        for summary in summaries
        if summary.get("bar_y_range") is not None
    ]

    median_bar_range = calculate_median(bar_ranges)

    for summary in summaries:
        summary["median_bar_y_range"] = median_bar_range

    return summaries


def add_start_position_context(summaries):
    start_knee_angles = [
        summary["lifting_start_knee_angle"]
        for summary in summaries
        if summary.get("lifting_start_knee_angle") is not None
    ]

    median_start_knee_angle = calculate_median(start_knee_angles)

    for summary in summaries:
        summary["median_start_knee_angle"] = median_start_knee_angle

    return summaries


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


def evaluate_bar_range(summary):
    bar_range = summary["bar_y_range"]
    median_bar_range = summary.get("median_bar_y_range")

    if bar_range is None or median_bar_range is None:
        return {
            "status": EVALUATION_STATUS_WARNING,
            "message": "Nie udało się ocenić zakresu ruchu sztangi.",
        }

    required_range = median_bar_range * BAR_RANGE_COMPLETENESS_RATIO

    if bar_range >= required_range:
        return {
            "status": EVALUATION_STATUS_OK,
            "message": (
                f"Zakres ruchu sztangi wygląda poprawnie "
                f"({bar_range:.3f}, mediana serii: {median_bar_range:.3f})."
            ),
        }

    return {
        "status": EVALUATION_STATUS_WARNING,
        "message": (
            f"Zakres ruchu sztangi jest niższy niż w pozostałych "
            f"powtórzeniach ({bar_range:.3f}, "
            f"mediana serii: {median_bar_range:.3f})."
        ),
    }


def evaluate_start_position_info(summary):
    start_knee_angle = summary.get("lifting_start_knee_angle")
    start_hip_angle = summary.get("lifting_start_hip_angle")
    start_back_angle = summary.get("lifting_start_back_angle")
    median_start_knee_angle = summary.get("median_start_knee_angle")

    if start_knee_angle is None or median_start_knee_angle is None:
        return {
            "status": EVALUATION_STATUS_INFO,
            "message": "Nie udało się określić pozycji startowej.",
        }

    diff = start_knee_angle - median_start_knee_angle

    if diff <= START_POSITION_KNEE_ANGLE_DEEP_OFFSET:
        position_label = "głębsza pozycja startowa"
    elif diff >= START_POSITION_KNEE_ANGLE_HIGH_OFFSET:
        position_label = "wyższa pozycja startowa"
    else:
        position_label = "pozycja startowa zbliżona do mediany serii"

    return {
        "status": EVALUATION_STATUS_INFO,
        "message": (
            f"{position_label}. "
            f"Kolano: {start_knee_angle:.1f}°, "
            f"biodro: {start_hip_angle:.1f}°, "
            f"tułów: {start_back_angle:.1f}°."
        ),
    }


def evaluate_start_torso_position(summary):
    shoulder_below_hip = summary.get("shoulder_below_hip_at_start")

    if shoulder_below_hip is None:
        return {
            "status": EVALUATION_STATUS_INFO,
            "message": (
                "Nie udało się określić relacji barku i biodra "
                "w pozycji startowej."
            ),
        }

    if shoulder_below_hip:
        return {
            "status": EVALUATION_STATUS_WARNING,
            "message": (
                "W pozycji startowej bark znajduje się niżej niż biodro. "
                "Może to wskazywać na niekorzystne ustawienie tułowia "
                "lub podejrzenie zaokrąglenia pleców."
            ),
        }

    return {
        "status": EVALUATION_STATUS_OK,
        "message": (
            "Relacja barku i biodra w pozycji startowej wygląda poprawnie."
        ),
    }


def evaluate_torso_angle_change(summary):
    back_change = summary["back_angle_change"]

    if back_change is None:
        return {
            "status": EVALUATION_STATUS_INFO,
            "message": "Nie udało się określić zmiany pochylenia tułowia.",
        }

    return {
        "status": EVALUATION_STATUS_INFO,
        "message": (
            f"Zmiana pochylenia tułowia w trakcie ruchu: "
            f"{back_change:.1f}°."
        ),
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


def classify_repetition_validity(checks):
    reasons = []

    hip_lockout = checks.get("hip_lockout")
    knee_lockout = checks.get("knee_lockout")
    bar_range = checks.get("bar_range")

    if hip_lockout and hip_lockout["status"] == EVALUATION_STATUS_WARNING:
        reasons.append("niepełny wyprost biodra")

    if knee_lockout and knee_lockout["status"] == EVALUATION_STATUS_WARNING:
        reasons.append("niepełny wyprost kolana")

    if bar_range and bar_range["status"] == EVALUATION_STATUS_WARNING:
        reasons.append("obniżony zakres ruchu sztangi")

    if not reasons:
        return {
            "validity": REP_VALIDITY_VALID,
            "reasons": [],
        }

    if len(reasons) <= 2:
        return {
            "validity": REP_VALIDITY_PARTIAL,
            "reasons": reasons,
        }

    return {
        "validity": REP_VALIDITY_INVALID,
        "reasons": reasons,
    }


def evaluate_repetition(summary):
    checks = {
        "hip_lockout": evaluate_hip_lockout(summary),
        "knee_lockout": evaluate_knee_lockout(summary),
        "bar_range": evaluate_bar_range(summary),
        "start_position": evaluate_start_position_info(summary),
        "start_torso_position": evaluate_start_torso_position(summary),
        "torso_angle_change": evaluate_torso_angle_change(summary),
        "tempo": evaluate_tempo_info(summary),
    }

    validity_result = classify_repetition_validity(checks)

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
        "rep_validity": validity_result["validity"],
        "validity_reasons": validity_result["reasons"],
        "checks": checks,
    }


def evaluate_repetitions(summaries):
    summaries = add_relative_bar_range_context(summaries)
    summaries = add_start_position_context(summaries)

    evaluations = []

    for summary in summaries:
        evaluation = evaluate_repetition(summary)

        summary["rep_validity"] = evaluation["rep_validity"]
        summary["validity_reasons"] = evaluation["validity_reasons"]

        evaluations.append(evaluation)

    return evaluations


def get_summaries_for_consistency(summaries):
    valid_summaries = [
        summary for summary in summaries
        if summary.get("rep_validity") == REP_VALIDITY_VALID
    ]

    if len(valid_summaries) >= 2:
        return valid_summaries

    return summaries


def evaluate_repetition_consistency(summaries):
    summaries_for_consistency = get_summaries_for_consistency(summaries)

    bar_range_variation = calculate_value_range(
        summaries_for_consistency,
        "bar_y_range",
    )

    duration_variation = calculate_value_range(
        summaries_for_consistency,
        "duration_seconds",
    )

    hip_lockout_variation = calculate_value_range(
        summaries_for_consistency,
        "top_hip_angle",
    )

    knee_lockout_variation = calculate_value_range(
        summaries_for_consistency,
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
                f"Różnica zakresu ruchu sztangi między poprawnymi "
                f"powtórzeniami: {bar_range_variation:.3f}."
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
                f"Różnica czasu trwania poprawnych powtórzeń: "
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
                f"Różnica kąta biodra w górnej pozycji "
                f"dla poprawnych powtórzeń: {hip_lockout_variation:.1f}°."
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
                f"Różnica kąta kolana w górnej pozycji "
                f"dla poprawnych powtórzeń: {knee_lockout_variation:.1f}°."
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