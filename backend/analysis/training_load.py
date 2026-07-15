"""Fitness (CTL) / Fatigue (ATL) / Form (TSB) modelling.

Exponentially weighted moving averages of daily training load with the
standard 42-day and 7-day time constants (same model as Strava's
Fitness & Freshness and TrainingPeaks' Performance Management Chart).
"""

import math
from dataclasses import dataclass
from datetime import date, timedelta

CTL_DAYS = 42.0
ATL_DAYS = 7.0

_CTL_ALPHA = 1.0 - math.exp(-1.0 / CTL_DAYS)
_ATL_ALPHA = 1.0 - math.exp(-1.0 / ATL_DAYS)


@dataclass(frozen=True)
class DayLoad:
    day: date
    load: float
    ctl: float
    atl: float
    tsb: float  # form: yesterday's CTL - yesterday's ATL


def fitness_series(
    daily_loads: dict[date, float], start: date, end: date
) -> list[DayLoad]:
    """Build the day-by-day CTL/ATL/TSB series over [start, end].

    Loads before `start` should be included in `daily_loads` if a warmed-up
    starting value is desired; the series itself always begins at `start`.
    """
    if end < start:
        return []

    warmup_days = sorted(d for d in daily_loads if d < start)
    ctl = atl = 0.0
    for day in _iter_days(warmup_days[0], start - timedelta(days=1)) if warmup_days else []:
        load = daily_loads.get(day, 0.0)
        ctl += (load - ctl) * _CTL_ALPHA
        atl += (load - atl) * _ATL_ALPHA

    series: list[DayLoad] = []
    for day in _iter_days(start, end):
        tsb = ctl - atl  # form uses values *before* today's load
        load = daily_loads.get(day, 0.0)
        ctl += (load - ctl) * _CTL_ALPHA
        atl += (load - atl) * _ATL_ALPHA
        series.append(DayLoad(day=day, load=load, ctl=ctl, atl=atl, tsb=tsb))
    return series


def _iter_days(start: date, end: date):
    day = start
    while day <= end:
        yield day
        day += timedelta(days=1)
