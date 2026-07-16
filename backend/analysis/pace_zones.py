"""Pace zones (5-zone model) anchored on threshold pace, and time-in-zone.

Zone bounds are fractions of threshold *speed* (Daniels/Friel-inspired):
Z1 recovery/easy, Z2 aerobic, Z3 marathon/tempo, Z4 threshold, Z5 VO2max+.
Samples slower than the Z1 floor (standing, walking breaks) are ignored,
mirroring how HR time-in-zone ignores sub-Z1 samples.
"""

from dataclasses import dataclass

# Lower bounds of Z1..Z5 as a fraction of threshold speed.
PACE_ZONE_BOUNDS_PCT_THRESHOLD = [0.60, 0.80, 0.90, 0.97, 1.06]


@dataclass(frozen=True)
class PaceZone:
    name: str
    low_speed_mps: float
    high_speed_mps: float | None  # None = open-ended top zone


def pace_zones(threshold_pace_s_per_km: float) -> list[PaceZone]:
    if threshold_pace_s_per_km <= 0:
        return []
    threshold_speed = 1000.0 / threshold_pace_s_per_km
    bounds = [pct * threshold_speed for pct in PACE_ZONE_BOUNDS_PCT_THRESHOLD]
    zones: list[PaceZone] = []
    for i, low in enumerate(bounds):
        high = bounds[i + 1] if i + 1 < len(bounds) else None
        zones.append(
            PaceZone(
                name=f"Z{i + 1}",
                low_speed_mps=round(low, 3),
                high_speed_mps=round(high, 3) if high is not None else None,
            )
        )
    return zones


def pace_zones_from_paces(bounds_s_per_km: list[float]) -> list[PaceZone]:
    """Zones from 5 manual lower bounds given as pace (s/km), slowest first."""
    speeds = [1000.0 / p for p in bounds_s_per_km if p > 0]
    if len(speeds) != len(bounds_s_per_km):
        return []
    zones: list[PaceZone] = []
    for i, low in enumerate(speeds):
        high = speeds[i + 1] if i + 1 < len(speeds) else None
        zones.append(
            PaceZone(
                name=f"Z{i + 1}",
                low_speed_mps=round(low, 3),
                high_speed_mps=round(high, 3) if high is not None else None,
            )
        )
    return zones


def pace_zones_for_settings(settings) -> list[PaceZone]:
    """Pace zones from an AthleteSettings row (threshold-derived or manual)."""
    manual = settings.manual_pace_zone_bounds
    if settings.pace_zone_mode == "manual" and manual and len(manual) == 5:
        return pace_zones_from_paces([float(b) for b in manual])
    return pace_zones(settings.threshold_pace_s_per_km)


def time_in_pace_zones(
    time_s: list[float], speed_mps: list[float | None], zones: list[PaceZone]
) -> list[float]:
    """Seconds spent in each of Z1..Z5 (samples below the Z1 floor are ignored)."""
    totals = [0.0] * len(zones)
    for i in range(1, len(time_s)):
        speed = speed_mps[i] if i < len(speed_mps) else None
        if speed is None or speed <= 0:
            continue
        dt = time_s[i] - time_s[i - 1]
        if dt <= 0 or dt > 30:  # skip gaps
            continue
        for zone_idx in range(len(zones) - 1, -1, -1):
            if speed >= zones[zone_idx].low_speed_mps:
                totals[zone_idx] += dt
                break
    return totals
