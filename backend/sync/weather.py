"""Historical weather enrichment from Open-Meteo (free, no API key).

Activities with GPS get temperature, humidity, wind and a WMO weather code for
the hour nearest the activity midpoint, plus a start-to-finish min/max range
for temperature and humidity (long runs and races can warm up considerably
between start and finish). The archive API lags a few days behind real time,
so recent activities use the forecast API's past_days window; an activity that
can't be resolved yet stays NULL and is retried on the next run.
"""

import logging
import time
from datetime import date, datetime, timedelta, timezone

import requests
from sqlalchemy import or_, select

from backend.db import session_scope
from backend.models import Activity

logger = logging.getLogger(__name__)

_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
_HOURLY_VARS = "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
_ARCHIVE_LAG_DAYS = 6
_REQUEST_PAUSE_S = 0.15  # stay far under Open-Meteo's rate limits
_TIMEOUT_S = 15
# A run "touches" the hourly samples within half an hour of it, so even a
# sub-hour run picks up its nearest sample(s) for the min/max range.
_RANGE_SLACK_S = 1800


def _first_position(stream) -> tuple[float, float] | None:
    if stream is None or not stream.lat:
        return None
    for lat, lng in zip(stream.lat, stream.lng):
        if lat is not None and lng is not None:
            return lat, lng
    return None


def _extract_fields(hourly: dict, start_utc: datetime, end_utc: datetime) -> dict | None:
    """Pick midpoint values and start-to-finish min/max from an hourly series."""
    times = hourly.get("time") or []
    if not times:
        return None

    start = start_utc.replace(tzinfo=None)
    end = end_utc.replace(tzinfo=None)
    midpoint = start + (end - start) / 2
    parsed = [datetime.fromisoformat(t) for t in times]

    best_idx = min(
        range(len(parsed)),
        key=lambda i: abs((parsed[i] - midpoint).total_seconds()),
    )
    if abs((parsed[best_idx] - midpoint).total_seconds()) > 5400:
        return None  # nearest hour is too far off (archive hasn't caught up)

    def _value(key, idx):
        values = hourly.get(key) or []
        return values[idx] if idx < len(values) else None

    span = [
        i
        for i, t in enumerate(parsed)
        if (start - t).total_seconds() <= _RANGE_SLACK_S
        and (t - end).total_seconds() <= _RANGE_SLACK_S
    ]

    def _min_max(key):
        values = [v for v in (_value(key, i) for i in span) if v is not None]
        if not values:
            return None, None
        return min(values), max(values)

    temp_min, temp_max = _min_max("temperature_2m")
    humidity_min, humidity_max = _min_max("relative_humidity_2m")
    return {
        "weather_temp_c": _value("temperature_2m", best_idx),
        "weather_humidity_pct": _value("relative_humidity_2m", best_idx),
        "weather_wind_mps": _value("wind_speed_10m", best_idx),
        "weather_code": _value("weather_code", best_idx),
        "weather_temp_min_c": temp_min,
        "weather_temp_max_c": temp_max,
        "weather_humidity_min_pct": humidity_min,
        "weather_humidity_max_pct": humidity_max,
    }


def _fetch_weather(lat: float, lng: float, start_utc: datetime, end_utc: datetime) -> dict | None:
    use_archive = end_utc.date() <= date.today() - timedelta(days=_ARCHIVE_LAG_DAYS)
    params = {
        "latitude": round(lat, 4),
        "longitude": round(lng, 4),
        "hourly": _HOURLY_VARS,
        "wind_speed_unit": "ms",
        "timezone": "UTC",
    }
    if use_archive:
        url = _ARCHIVE_URL
        params["start_date"] = start_utc.date().isoformat()
        params["end_date"] = end_utc.date().isoformat()  # spans midnight when needed
    else:
        url = _FORECAST_URL
        params["past_days"] = _ARCHIVE_LAG_DAYS + 1
        params["forecast_days"] = 1

    response = requests.get(url, params=params, timeout=_TIMEOUT_S)
    response.raise_for_status()
    hourly = response.json().get("hourly") or {}
    return _extract_fields(hourly, start_utc, end_utc)


def enrich_missing_weather(limit: int | None = None) -> int:
    """Fill weather fields for GPS activities that don't have them yet.

    Also picks up rows enriched before the min/max range existed (point fields
    set, range fields NULL) and refetches them to fill the range.
    """
    with session_scope() as session:
        ids = list(
            session.scalars(
                select(Activity.id)
                .where(Activity.has_gps.is_(True))
                .where(
                    or_(
                        Activity.weather_temp_c.is_(None),
                        Activity.weather_temp_min_c.is_(None),
                    )
                )
                .order_by(Activity.start_time_utc.desc())
            ).all()
        )
    if limit is not None:
        ids = ids[:limit]

    enriched = 0
    for activity_id in ids:
        with session_scope() as session:
            activity = session.get(Activity, activity_id)
            if activity is None:
                continue
            position = _first_position(activity.stream)
            if position is None:
                continue
            start_utc = activity.start_time_utc.replace(tzinfo=timezone.utc)
            end_utc = start_utc + timedelta(seconds=activity.elapsed_s or 0)
            try:
                fields = _fetch_weather(position[0], position[1], start_utc, end_utc)
            except Exception as exc:
                logger.warning("Weather fetch failed for %s: %s", activity_id, exc)
                continue
            if fields is None or fields.get("weather_temp_c") is None:
                continue
            for key, value in fields.items():
                setattr(activity, key, value)
            enriched += 1
        time.sleep(_REQUEST_PAUSE_S)
    return enriched
