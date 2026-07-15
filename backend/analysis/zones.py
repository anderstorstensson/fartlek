"""Heart-rate zones (5-zone model as %max HR) and time-in-zone from streams."""

from dataclasses import dataclass

ZONE_BOUNDS_PCT_MAX = [0.50, 0.60, 0.70, 0.80, 0.90]  # lower bounds of Z1..Z5


@dataclass(frozen=True)
class Zone:
    name: str
    low_bpm: int
    high_bpm: int | None  # None = open-ended top zone


def hr_zones(max_hr: int) -> list[Zone]:
    zones: list[Zone] = []
    for i, low_pct in enumerate(ZONE_BOUNDS_PCT_MAX):
        high_pct = ZONE_BOUNDS_PCT_MAX[i + 1] if i + 1 < len(ZONE_BOUNDS_PCT_MAX) else None
        zones.append(
            Zone(
                name=f"Z{i + 1}",
                low_bpm=round(low_pct * max_hr),
                high_bpm=round(high_pct * max_hr) if high_pct else None,
            )
        )
    return zones


def time_in_zones(
    time_s: list[float], hr: list[float | None], max_hr: int
) -> list[float]:
    """Seconds spent in each of Z1..Z5 (samples below Z1 are ignored)."""
    totals = [0.0] * len(ZONE_BOUNDS_PCT_MAX)
    zones = hr_zones(max_hr)
    for i in range(1, len(time_s)):
        sample_hr = hr[i] if i < len(hr) else None
        if sample_hr is None or sample_hr <= 0:
            continue
        dt = time_s[i] - time_s[i - 1]
        if dt <= 0 or dt > 30:  # skip gaps
            continue
        for zone_idx in range(len(zones) - 1, -1, -1):
            if sample_hr >= zones[zone_idx].low_bpm:
                totals[zone_idx] += dt
                break
    return totals
