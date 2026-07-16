"""Grade-adjusted pace (GAP).

Uses the Minetti et al. (2002) polynomial for the energy cost of running on a
gradient, normalized to the flat cost, to convert actual speed on a slope into
the equivalent flat-ground speed. Altitude is smoothed before the gradient is
taken because barometric altimeter noise dwarfs real per-second elevation change.
"""

_MINETTI_COEFFS = (155.4, -30.4, -43.3, 46.3, 19.5, 3.6)  # J/kg/m, grade as fraction
_FLAT_COST = 3.6
_MAX_GRADE = 0.30  # the polynomial is only validated to ±45%; clamp well inside
_ALTITUDE_SMOOTH_S = 15.0
_MIN_SEGMENT_M = 2.0  # ignore gradient when barely moving
_MAX_GAP_DT_S = 30.0  # treat larger sample gaps as pauses


def grade_cost_factor(grade: float) -> float:
    """Energy cost of running at `grade` relative to flat running (1.0 = flat)."""
    g = min(max(grade, -_MAX_GRADE), _MAX_GRADE)
    cost = 0.0
    for coeff in _MINETTI_COEFFS:
        cost = cost * g + coeff
    return max(cost / _FLAT_COST, 0.3)


def _smooth(values: list[float | None], time_s: list[float], window_s: float) -> list[float | None]:
    """Centered moving average over a time window, None-aware."""
    smoothed: list[float | None] = [None] * len(values)
    half = window_s / 2.0
    start = 0
    end = 0
    for i, t in enumerate(time_s):
        while start < len(time_s) and time_s[start] < t - half:
            start += 1
        while end < len(time_s) and time_s[end] <= t + half:
            end += 1
        window = [v for v in values[start:end] if v is not None]
        smoothed[i] = sum(window) / len(window) if window else None
    return smoothed


def gap_speed_series(
    time_s: list[float],
    distance_m: list[float | None],
    speed_mps: list[float | None],
    altitude_m: list[float | None],
) -> list[float | None]:
    """Per-sample grade-adjusted speed. Falls back to raw speed where altitude
    or distance is missing."""
    n = len(time_s)
    if n < 2 or len(speed_mps) != n:
        return [s for s in speed_mps]
    if len(altitude_m) != n or len(distance_m) != n:
        return [s for s in speed_mps]

    alt = _smooth(altitude_m, time_s, _ALTITUDE_SMOOTH_S)
    gap: list[float | None] = [speed_mps[0]]
    for i in range(1, n):
        speed = speed_mps[i]
        if speed is None:
            gap.append(None)
            continue
        d_prev, d_cur = distance_m[i - 1], distance_m[i]
        a_prev, a_cur = alt[i - 1], alt[i]
        if None in (d_prev, d_cur, a_prev, a_cur) or (d_cur - d_prev) < _MIN_SEGMENT_M:
            gap.append(speed)
            continue
        grade = (a_cur - a_prev) / (d_cur - d_prev)
        gap.append(speed * grade_cost_factor(grade))
    return gap


def average_moving_speed(
    time_s: list[float], speed_mps: list[float | None], min_speed: float = 0.5
) -> float | None:
    """Time-weighted average speed over moving samples, skipping pauses."""
    total_time = 0.0
    total_dist = 0.0
    for i in range(1, len(time_s)):
        speed = speed_mps[i] if i < len(speed_mps) else None
        if speed is None or speed < min_speed:
            continue
        dt = time_s[i] - time_s[i - 1]
        if dt <= 0 or dt > _MAX_GAP_DT_S:
            continue
        total_time += dt
        total_dist += speed * dt
    if total_time <= 0:
        return None
    return total_dist / total_time
