"""Training load metrics.

Two independent load models are supported:
  * TRIMP (Banister): HR-based, works for any activity with heart rate.
  * rTSS (TrainingPeaks-style): pace-based, running only, with hrTSS as the
    HR-based fallback so both series share the ~100-points-per-threshold-hour scale.
"""

import math

_TRIMP_COEFF = {"male": (0.64, 1.92), "female": (0.86, 1.67)}


def hr_reserve_fraction(hr: float, resting_hr: float, max_hr: float) -> float:
    if max_hr <= resting_hr:
        return 0.0
    frac = (hr - resting_hr) / (max_hr - resting_hr)
    return min(max(frac, 0.0), 1.0)


def banister_trimp(
    duration_min: float, avg_hr: float, resting_hr: float, max_hr: float, sex: str = "male"
) -> float:
    """Classic session TRIMP from average HR."""
    if duration_min <= 0 or avg_hr <= 0:
        return 0.0
    a, b = _TRIMP_COEFF.get(sex, _TRIMP_COEFF["male"])
    frac = hr_reserve_fraction(avg_hr, resting_hr, max_hr)
    return duration_min * frac * a * math.exp(b * frac)


def trimp_from_samples(
    time_s: list[float],
    hr: list[float | None],
    resting_hr: float,
    max_hr: float,
    sex: str = "male",
) -> float:
    """Sample-by-sample TRIMP integration; more accurate than session average
    for interval workouts because of the exponential HR weighting."""
    if len(time_s) < 2 or len(hr) != len(time_s):
        return 0.0
    a, b = _TRIMP_COEFF.get(sex, _TRIMP_COEFF["male"])
    total = 0.0
    for i in range(1, len(time_s)):
        sample_hr = hr[i]
        if sample_hr is None or sample_hr <= 0:
            continue
        dt_min = max(time_s[i] - time_s[i - 1], 0.0) / 60.0
        if dt_min > 0.5:  # gap (auto-pause) — don't accumulate load across it
            continue
        frac = hr_reserve_fraction(sample_hr, resting_hr, max_hr)
        total += dt_min * frac * a * math.exp(b * frac)
    return total


def rtss(moving_s: float, distance_m: float, threshold_pace_s_per_km: float) -> float:
    """Running Training Stress Score from average pace vs threshold pace.

    IF = NGP / threshold speed (average moving speed as NGP approximation);
    rTSS = hours * IF^2 * 100, i.e. one hour at threshold = 100.
    """
    if moving_s <= 0 or distance_m <= 0:
        return 0.0
    return rtss_from_speed(moving_s, distance_m / moving_s, threshold_pace_s_per_km)


def rtss_from_speed(
    moving_s: float, speed_mps: float, threshold_pace_s_per_km: float
) -> float:
    """rTSS from an already-normalized speed (e.g. grade-adjusted speed as NGP)."""
    if moving_s <= 0 or speed_mps <= 0 or threshold_pace_s_per_km <= 0:
        return 0.0
    threshold_speed = 1000.0 / threshold_pace_s_per_km
    intensity_factor = speed_mps / threshold_speed
    return (moving_s / 3600.0) * intensity_factor**2 * 100.0


def hrtss(duration_s: float, avg_hr: float, lthr: float) -> float:
    """HR-based TSS approximation, used for non-running activities in rTSS mode."""
    if duration_s <= 0 or avg_hr <= 0 or lthr <= 0:
        return 0.0
    intensity_factor = min(avg_hr / lthr, 1.15)
    return (duration_s / 3600.0) * intensity_factor**2 * 100.0
