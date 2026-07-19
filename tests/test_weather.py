"""Tests for the pure hourly-series extraction in backend.sync.weather."""

from datetime import datetime, timezone

from backend.sync.weather import _extract_fields


def _hourly(day: str, start_hour: int, temps: list[float], humidity: list[float] | None = None):
    hours = range(start_hour, start_hour + len(temps))
    return {
        "time": [f"{day}T{h:02d}:00" for h in hours],
        "temperature_2m": temps,
        "relative_humidity_2m": humidity or [50.0] * len(temps),
        "wind_speed_10m": [3.0] * len(temps),
        "weather_code": [1] * len(temps),
    }


def _utc(day: str, hour: int, minute: int = 0) -> datetime:
    return datetime.fromisoformat(f"{day}T{hour:02d}:{minute:02d}").replace(tzinfo=timezone.utc)


def test_long_run_gets_start_to_finish_range():
    # 9 -> 21 °C over the morning; a 4 h run 07:00-11:00 should span 11..19.
    hourly = _hourly("2026-07-01", 6, [9.0, 11.0, 13.0, 15.0, 17.0, 19.0, 21.0],
                     humidity=[90.0, 85.0, 80.0, 75.0, 70.0, 65.0, 60.0])
    fields = _extract_fields(hourly, _utc("2026-07-01", 7), _utc("2026-07-01", 11))
    assert fields["weather_temp_c"] == 15.0  # midpoint 09:00
    assert fields["weather_temp_min_c"] == 11.0
    assert fields["weather_temp_max_c"] == 19.0
    assert fields["weather_humidity_min_pct"] == 65.0
    assert fields["weather_humidity_max_pct"] == 85.0


def test_short_run_still_gets_nearest_samples():
    # 40 min run 10:10-10:50 sits between two hourly samples; both are within
    # the half-hour slack, so the range covers them instead of being empty.
    hourly = _hourly("2026-07-01", 9, [14.0, 15.0, 17.0, 18.0])
    fields = _extract_fields(hourly, _utc("2026-07-01", 10, 10), _utc("2026-07-01", 10, 50))
    assert fields["weather_temp_c"] == 15.0  # midpoint 10:30 -> nearest hour 10:00 or 11:00
    assert fields["weather_temp_min_c"] == 15.0
    assert fields["weather_temp_max_c"] == 17.0


def test_empty_series_returns_none():
    assert _extract_fields({}, _utc("2026-07-01", 7), _utc("2026-07-01", 8)) is None
    assert _extract_fields({"time": []}, _utc("2026-07-01", 7), _utc("2026-07-01", 8)) is None


def test_stale_archive_returns_none():
    # Nearest available hour is > 1.5 h from the midpoint: archive hasn't caught up.
    hourly = _hourly("2026-07-01", 0, [10.0, 10.0, 10.0])
    assert _extract_fields(hourly, _utc("2026-07-01", 12), _utc("2026-07-01", 13)) is None


def test_null_values_are_skipped_in_range():
    hourly = _hourly("2026-07-01", 7, [None, 12.0, 14.0])
    fields = _extract_fields(hourly, _utc("2026-07-01", 7), _utc("2026-07-01", 9))
    assert fields["weather_temp_min_c"] == 12.0
    assert fields["weather_temp_max_c"] == 14.0
