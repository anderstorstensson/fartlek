from datetime import datetime

from backend.models import Activity, AthleteSettings
from backend.sync.importer import _compute_loads


def _activity(gap_speed: float | None) -> Activity:
    return Activity(
        id=1, name="Hill run", sport="running",
        start_time_utc=datetime(2026, 7, 1, 6, 0), start_time_local=datetime(2026, 7, 1, 8, 0),
        moving_s=3600, distance_m=12000, gap_speed_mps=gap_speed,
    )


def _settings(use_gap: bool) -> AthleteSettings:
    return AthleteSettings(
        id=1, resting_hr=50, max_hr=190, lthr=170,
        threshold_pace_s_per_km=270.0, rtss_use_gap=use_gap,
    )


def test_rtss_uses_gap_when_enabled():
    # GAP 3.5 m/s vs raw 12000/3600 = 3.33 m/s → higher rTSS with GAP
    with_gap = _activity(gap_speed=3.5)
    _compute_loads(with_gap, None, _settings(use_gap=True))

    raw_only = _activity(gap_speed=3.5)
    _compute_loads(raw_only, None, _settings(use_gap=False))

    assert with_gap.rtss > raw_only.rtss


def test_rtss_falls_back_to_raw_pace_without_gap():
    activity = _activity(gap_speed=None)
    _compute_loads(activity, None, _settings(use_gap=True))
    assert activity.rtss is not None and activity.rtss > 0
