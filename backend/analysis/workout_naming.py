"""Derive a session name from interval structure, e.g. "10×3 min / 1 min rest".

Only runs flagged as structured workouts are named this way; everything else
keeps its Garmin name. Reps are described by distance when the laps hit round
distances (an 800m-rep session), otherwise by duration (a 3-min-rep session);
if the work laps are neither time- nor distance-uniform (pyramids, fartleks),
no name is derived and the original stays.
"""

import statistics

_MIN_WORK_LAPS = 2


def _fmt_duration(seconds: float) -> str:
    s = int(round(seconds / 5.0) * 5)  # lap timing jitter — snap to 5 s
    if s < 60:
        return f"{s} s"
    minutes, rest = divmod(s, 60)
    if rest == 0:
        return f"{minutes} min"
    return f"{minutes}:{rest:02d}"


def _fmt_distance(meters: float) -> str:
    m = int(round(meters / 50.0) * 50)
    if m >= 1000 and m % 500 == 0:
        km = m / 1000
        return f"{km:g} km"
    return f"{m} m"


def _uniform(values: list[float], tolerance_abs: float, tolerance_frac: float) -> bool:
    if not values:
        return False
    median = statistics.median(values)
    allowed = max(tolerance_abs, median * tolerance_frac)
    return all(abs(v - median) <= allowed for v in values)


def _spread(values: list[float]) -> float:
    median = statistics.median(values)
    if median <= 0:
        return float("inf")
    return (max(values) - min(values)) / median


def workout_name(laps: list[dict]) -> str | None:
    """laps: dicts with elapsed_s, distance_m, intensity (as parsed from FIT)."""
    work = [lap for lap in laps if lap.get("intensity") == "active"]
    rests = [lap for lap in laps if lap.get("intensity") == "rest"]
    if len(work) < _MIN_WORK_LAPS or (not rests and len(work) < 3):
        return None

    durations = [lap["elapsed_s"] for lap in work if lap.get("elapsed_s")]
    distances = [lap["distance_m"] for lap in work if lap.get("distance_m")]
    if len(durations) < len(work) and len(distances) < len(work):
        return None

    # The watch-controlled dimension is (near-)exact across reps, the other one
    # drifts with pace — describe the reps by whichever spreads less.
    time_first = (
        len(durations) == len(work)
        and (len(distances) < len(work) or _spread(durations) <= _spread(distances))
    )
    time_rep = (
        _fmt_duration(statistics.median(durations))
        if len(durations) == len(work) and _uniform(durations, 10.0, 0.10)
        else None
    )
    distance_rep = (
        _fmt_distance(statistics.median(distances))
        if len(distances) == len(work) and _uniform(distances, 30.0, 0.03)
        else None
    )
    rep = (time_rep or distance_rep) if time_first else (distance_rep or time_rep)
    if rep is None:
        return None

    name = f"{len(work)}×{rep}"
    rest_durations = [lap["elapsed_s"] for lap in rests if lap.get("elapsed_s")]
    if rest_durations:
        name += f" / {_fmt_duration(statistics.median(rest_durations))} rest"
    return name
