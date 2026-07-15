"""Fastest-effort detection over standard distances (Strava-style 'Best Efforts').

Uses cumulative time/distance arrays and a two-pointer sweep: for each start
sample, advance the end pointer until the window covers the target distance,
interpolating the exact crossing time.
"""

from dataclasses import dataclass

STANDARD_DISTANCES: list[tuple[str, float]] = [
    ("400m", 400.0),
    ("1K", 1000.0),
    ("1 mile", 1609.34),
    ("5K", 5000.0),
    ("10K", 10000.0),
    ("Half marathon", 21097.5),
    ("Marathon", 42195.0),
]


@dataclass(frozen=True)
class Effort:
    label: str
    distance_m: float
    duration_s: float


def best_efforts(time_s: list[float], distance_m: list[float]) -> list[Effort]:
    """Find the fastest contiguous effort for each standard distance covered."""
    n = len(time_s)
    if n < 2 or len(distance_m) != n:
        return []
    total = distance_m[-1] - distance_m[0]

    results: list[Effort] = []
    for label, target in STANDARD_DISTANCES:
        if total < target:
            break
        duration = _fastest_window(time_s, distance_m, target)
        if duration is not None:
            results.append(Effort(label=label, distance_m=target, duration_s=duration))
    return results


def _fastest_window(
    time_s: list[float], distance_m: list[float], target: float
) -> float | None:
    n = len(time_s)
    best: float | None = None
    end = 0
    for start in range(n):
        if end <= start:
            end = start + 1
        while end < n and distance_m[end] - distance_m[start] < target:
            end += 1
        if end >= n:
            break
        # Interpolate the exact time at which the window reaches `target`.
        covered_prev = distance_m[end - 1] - distance_m[start]
        covered_now = distance_m[end] - distance_m[start]
        seg = covered_now - covered_prev
        frac = (target - covered_prev) / seg if seg > 0 else 1.0
        cross_time = time_s[end - 1] + frac * (time_s[end] - time_s[end - 1])
        duration = cross_time - time_s[start]
        if duration > 0 and (best is None or duration < best):
            best = duration
    return best
