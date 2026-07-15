import math
from datetime import date, timedelta

from backend.analysis.training_load import ATL_DAYS, CTL_DAYS, fitness_series


def test_empty_loads_give_zero_series():
    series = fitness_series({}, date(2026, 1, 1), date(2026, 1, 10))
    assert len(series) == 10
    assert all(p.ctl == 0 and p.atl == 0 and p.tsb == 0 for p in series)


def test_constant_load_converges_to_load():
    start = date(2025, 1, 1)
    end = start + timedelta(days=400)
    loads = {start + timedelta(days=i): 100.0 for i in range(401)}
    series = fitness_series(loads, start, end)
    assert abs(series[-1].ctl - 100.0) < 1.0
    assert abs(series[-1].atl - 100.0) < 0.1


def test_atl_responds_faster_than_ctl():
    start = date(2026, 1, 1)
    loads = {start + timedelta(days=i): 100.0 for i in range(14)}
    series = fitness_series(loads, start, start + timedelta(days=13))
    last = series[-1]
    assert last.atl > last.ctl
    assert last.tsb < 0  # ramping up -> negative form


def test_tsb_uses_previous_day_values():
    start = date(2026, 1, 1)
    series = fitness_series({start: 100.0}, start, start + timedelta(days=1))
    # Day 1 form must not include day 1's own load.
    assert series[0].tsb == 0.0
    expected_ctl = 100.0 * (1 - math.exp(-1 / CTL_DAYS))
    expected_atl = 100.0 * (1 - math.exp(-1 / ATL_DAYS))
    assert abs(series[1].tsb - (expected_ctl - expected_atl)) < 1e-9


def test_warmup_before_window_is_applied():
    start = date(2026, 3, 1)
    loads = {start - timedelta(days=i): 80.0 for i in range(1, 200)}
    series = fitness_series(loads, start, start)
    assert series[0].ctl > 60  # history before the window counts


def test_invalid_range_returns_empty():
    assert fitness_series({}, date(2026, 1, 2), date(2026, 1, 1)) == []
