"""Heart-rate zones (5-zone model) and time-in-zone from streams.

Three zone bases are supported:
  * max_hr — % of max HR (Z1 starts at 50%)
  * lthr   — % of lactate threshold HR (Friel-style: Z5 starts at LTHR)
  * manual — explicit lower bounds in bpm
"""

from dataclasses import dataclass

ZONE_BOUNDS_PCT_MAX = [0.50, 0.60, 0.70, 0.80, 0.90]  # lower bounds of Z1..Z5
ZONE_BOUNDS_PCT_LTHR = [0.65, 0.85, 0.90, 0.95, 1.00]
ZONE_COUNT = len(ZONE_BOUNDS_PCT_MAX)


@dataclass(frozen=True)
class Zone:
    name: str
    low_bpm: int
    high_bpm: int | None  # None = open-ended top zone


def _zones_from_bounds(bounds: list[int]) -> list[Zone]:
    zones: list[Zone] = []
    for i, low in enumerate(bounds):
        high = bounds[i + 1] if i + 1 < len(bounds) else None
        zones.append(Zone(name=f"Z{i + 1}", low_bpm=low, high_bpm=high))
    return zones


def hr_zones(
    zone_mode: str,
    max_hr: int,
    lthr: int,
    manual_bounds: list[int] | None = None,
) -> list[Zone]:
    if zone_mode == "manual" and manual_bounds and len(manual_bounds) == ZONE_COUNT:
        return _zones_from_bounds([int(b) for b in manual_bounds])
    if zone_mode == "lthr":
        return _zones_from_bounds([round(pct * lthr) for pct in ZONE_BOUNDS_PCT_LTHR])
    return _zones_from_bounds([round(pct * max_hr) for pct in ZONE_BOUNDS_PCT_MAX])


def zones_for_settings(settings) -> list[Zone]:
    """Zones from an AthleteSettings row."""
    return hr_zones(
        settings.zone_mode, settings.max_hr, settings.lthr, settings.manual_zone_bounds
    )


def time_in_zones(
    time_s: list[float], hr: list[float | None], zones: list[Zone]
) -> list[float]:
    """Seconds spent in each of Z1..Z5 (samples below Z1 are ignored)."""
    totals = [0.0] * len(zones)
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
