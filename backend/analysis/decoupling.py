"""Aerobic decoupling and efficiency index.

Decoupling compares the speed:HR ratio of the first and second half of a run —
positive drift means the same pace cost more heartbeats late in the run (effort
above current aerobic fitness, heat, or dehydration). Efficiency index is
grade-adjusted meters per minute per heartbeat; rising over months at easy
intensity is the cleanest "getting fitter" signal.

Both are computed from grade-adjusted speed when available so hills don't
masquerade as drift.
"""

_MIN_SPEED_MPS = 0.5
_MAX_GAP_DT_S = 30.0
_MIN_HALF_TIME_S = 600.0  # need ≥10 min per half for a meaningful ratio


def _half_ratios(
    time_s: list[float],
    speed_mps: list[float | None],
    hr: list[float | None],
) -> tuple[float, float] | None:
    """Time-weighted speed/HR ratio for each half of the valid moving time."""
    segments: list[tuple[float, float, float]] = []  # (dt, speed, hr)
    for i in range(1, len(time_s)):
        speed = speed_mps[i] if i < len(speed_mps) else None
        sample_hr = hr[i] if i < len(hr) else None
        if speed is None or speed < _MIN_SPEED_MPS or not sample_hr or sample_hr <= 0:
            continue
        dt = time_s[i] - time_s[i - 1]
        if dt <= 0 or dt > _MAX_GAP_DT_S:
            continue
        segments.append((dt, speed, sample_hr))

    total_time = sum(dt for dt, _, _ in segments)
    if total_time < 2 * _MIN_HALF_TIME_S:
        return None

    ratios: list[float] = []
    halfway = total_time / 2.0
    elapsed = 0.0
    half_dist = half_beats = 0.0
    for dt, speed, sample_hr in segments:
        half_dist += speed * dt
        half_beats += sample_hr * dt
        elapsed += dt
        if elapsed >= halfway and len(ratios) == 0:
            ratios.append(half_dist / half_beats)
            half_dist = half_beats = 0.0
    if half_beats <= 0:
        return None
    ratios.append(half_dist / half_beats)
    return ratios[0], ratios[1]


def aerobic_decoupling_pct(
    time_s: list[float],
    speed_mps: list[float | None],
    hr: list[float | None],
) -> float | None:
    """Percent decline of speed:HR from first to second half (positive = drift)."""
    halves = _half_ratios(time_s, speed_mps, hr)
    if halves is None or halves[1] <= 0:
        return None
    first, second = halves
    return (first / second - 1.0) * 100.0


def efficiency_index(avg_speed_mps: float | None, avg_hr: float | None) -> float | None:
    """Grade-adjusted meters per minute per heartbeat."""
    if not avg_speed_mps or not avg_hr or avg_hr <= 0:
        return None
    return (avg_speed_mps * 60.0) / avg_hr
