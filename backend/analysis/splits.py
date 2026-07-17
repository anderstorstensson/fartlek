"""Distance splits computed from activity streams, plus lap-split helpers.

Most easy runs carry a single FIT lap spanning the whole activity, so per-km
splits are cut from the cumulative distance stream, with the split boundary
time interpolated between samples. Elevation gain uses a hysteresis threshold
on smoothed altitude because raw barometric deltas are noise-dominated (same
rationale as the GAP gradient smoothing).
"""

from dataclasses import dataclass

from backend.analysis.gap import _MAX_GAP_DT_S, _smooth

SPLIT_M = 1000.0
_MILE_M = 1609.34
_MIN_FINAL_SPLIT_M = 200.0
_ALTITUDE_SMOOTH_S = 15.0
_ELEV_THRESHOLD_M = 2.0
_AUTOLAP_TOLERANCE = 0.03


@dataclass(frozen=True)
class Split:
    index: int
    distance_m: float
    elapsed_s: float  # moving time within the split (pause gaps excluded)
    avg_speed_mps: float | None
    elevation_gain_m: float | None
    avg_hr: float | None


def is_autolap(distances: list[float], tolerance: float = _AUTOLAP_TOLERANCE) -> bool:
    """True when the laps look like watch autolaps: every lap except the last
    is one km (or one mile) and the last is at most that long."""
    if len(distances) < 2:
        return False
    for unit in (SPLIT_M, _MILE_M):
        body_ok = all(abs(d - unit) <= unit * tolerance for d in distances[:-1])
        if body_ok and distances[-1] <= unit * (1 + tolerance):
            return True
    return False


def _hysteresis_gain(altitudes: list[float | None], threshold_m: float) -> float | None:
    ref: float | None = None
    gain = 0.0
    for altitude in altitudes:
        if altitude is None:
            continue
        if ref is None:
            ref = altitude
        elif altitude >= ref + threshold_m:
            gain += altitude - ref
            ref = altitude
        elif altitude <= ref - threshold_m:
            ref = altitude
    return gain if ref is not None else None


def elevation_gain(
    time_s: list[float],
    altitude_m: list[float | None],
    threshold_m: float = _ELEV_THRESHOLD_M,
) -> float | None:
    """Total ascent over the whole series; None without usable altitude."""
    if not time_s or len(altitude_m) != len(time_s):
        return None
    return _hysteresis_gain(_smooth(altitude_m, time_s, _ALTITUDE_SMOOTH_S), threshold_m)


def window_elevation_gains(
    time_s: list[float | None],
    altitude_m: list[float | None] | None,
    windows: list[tuple[float, float]],
    threshold_m: float = _ELEV_THRESHOLD_M,
) -> list[float | None]:
    """Ascent within each (start_s, end_s) time window, smoothing once."""
    if not altitude_m or len(altitude_m) != len(time_s):
        return [None] * len(windows)
    clean = [(t, a) for t, a in zip(time_s, altitude_m) if t is not None]
    if not clean:
        return [None] * len(windows)
    times = [t for t, _ in clean]
    smoothed = _smooth([a for _, a in clean], times, _ALTITUDE_SMOOTH_S)
    return [
        _hysteresis_gain(
            [a for t, a in zip(times, smoothed) if start <= t <= end], threshold_m
        )
        for start, end in windows
    ]


def _window_mean(
    times: list[float], values: list[float | None], start: float, end: float
) -> float | None:
    window = [v for t, v in zip(times, values) if start <= t <= end and v is not None]
    return sum(window) / len(window) if window else None


def km_splits(
    time_s: list[float | None],
    distance_m: list[float | None],
    altitude_m: list[float | None] | None,
    hr: list[float | None] | None,
    split_m: float = SPLIT_M,
) -> list[Split]:
    """Cut the cumulative distance stream into `split_m` pieces.

    A trailing remainder shorter than _MIN_FINAL_SPLIT_M is dropped. Sample
    gaps longer than _MAX_GAP_DT_S count as pauses and are excluded from the
    split's moving time.
    """
    pairs = [
        (float(t), float(d))
        for t, d in zip(time_s, distance_m)
        if t is not None and d is not None
    ]
    if len(pairs) < 2:
        return []

    boundaries: list[float] = [pairs[0][0]]  # time at each split edge
    moving: list[float] = []  # moving seconds per completed split
    current = 0.0
    start_d = pairs[0][1]
    next_d = start_d + split_m
    prev_t, prev_d = pairs[0]
    for t, d in pairs[1:]:
        dt = t - prev_t
        if dt <= 0 or d < prev_d:  # out-of-order or distance reset: skip segment
            prev_t, prev_d = t, d
            continue
        paused = dt > _MAX_GAP_DT_S
        segment_start = prev_t
        while d >= next_d and d > prev_d:
            fraction = (next_d - prev_d) / (d - prev_d)
            boundary_t = prev_t + fraction * dt
            if not paused:
                current += boundary_t - segment_start
            boundaries.append(boundary_t)
            moving.append(current)
            current = 0.0
            segment_start = boundary_t
            next_d += split_m
        if not paused:
            current += t - segment_start
        prev_t, prev_d = t, d

    distances = [split_m] * len(moving)
    final_d = pairs[-1][1] - (start_d + len(moving) * split_m)
    if final_d >= _MIN_FINAL_SPLIT_M:
        boundaries.append(pairs[-1][0])
        moving.append(current)
        distances.append(final_d)
    if not moving:
        return []

    n = len(time_s)
    alt = altitude_m if altitude_m and len(altitude_m) == n else [None] * n
    hrs = hr if hr and len(hr) == n else [None] * n
    clean = [(t, a, h) for t, a, h in zip(time_s, alt, hrs) if t is not None]
    times = [t for t, _, _ in clean]
    gains = window_elevation_gains(
        times, [a for _, a, _ in clean], list(zip(boundaries[:-1], boundaries[1:]))
    )
    hr_values = [h for _, _, h in clean]

    return [
        Split(
            index=i,
            distance_m=round(distances[i], 1),
            elapsed_s=round(moving[i], 1),
            avg_speed_mps=distances[i] / moving[i] if moving[i] > 0 else None,
            elevation_gain_m=round(gains[i], 1) if gains[i] is not None else None,
            avg_hr=_window_mean(times, hr_values, boundaries[i], boundaries[i + 1]),
        )
        for i in range(len(moving))
    ]
