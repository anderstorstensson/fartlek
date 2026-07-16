"""Historical weather enrichment from Open-Meteo (free, no API key).

Activities with GPS get temperature, humidity, wind and a WMO weather code for
the hour nearest the activity midpoint. The archive API lags a few days behind
real time, so recent activities use the forecast API's past_days window; an
activity that can't be resolved yet stays NULL and is retried on the next run.
"""

import logging
import time
from datetime import date, datetime, timedelta, timezone

import requests
from sqlalchemy import select

from backend.db import session_scope
from backend.models import Activity

logger = logging.getLogger(__name__)

_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
_HOURLY_VARS = "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
_ARCHIVE_LAG_DAYS = 6
_REQUEST_PAUSE_S = 0.15  # stay far under Open-Meteo's rate limits
_TIMEOUT_S = 15


def _first_position(stream) -> tuple[float, float] | None:
    if stream is None or not stream.lat:
        return None
    for lat, lng in zip(stream.lat, stream.lng):
        if lat is not None and lng is not None:
            return lat, lng
    return None


def _fetch_hour(lat: float, lng: float, when_utc: datetime) -> dict | None:
    day = when_utc.date()
    use_archive = day <= date.today() - timedelta(days=_ARCHIVE_LAG_DAYS)
    params = {
        "latitude": round(lat, 4),
        "longitude": round(lng, 4),
        "hourly": _HOURLY_VARS,
        "wind_speed_unit": "ms",
        "timezone": "UTC",
    }
    if use_archive:
        url = _ARCHIVE_URL
        params["start_date"] = day.isoformat()
        params["end_date"] = day.isoformat()
    else:
        url = _FORECAST_URL
        params["past_days"] = _ARCHIVE_LAG_DAYS + 1
        params["forecast_days"] = 1

    response = requests.get(url, params=params, timeout=_TIMEOUT_S)
    response.raise_for_status()
    hourly = response.json().get("hourly") or {}
    times = hourly.get("time") or []
    if not times:
        return None

    target = when_utc.replace(tzinfo=None)
    best_idx = min(
        range(len(times)),
        key=lambda i: abs((datetime.fromisoformat(times[i]) - target).total_seconds()),
    )
    if abs((datetime.fromisoformat(times[best_idx]) - target).total_seconds()) > 5400:
        return None  # nearest hour is too far off (archive hasn't caught up)

    def _pick(key):
        values = hourly.get(key) or []
        return values[best_idx] if best_idx < len(values) else None

    return {
        "weather_temp_c": _pick("temperature_2m"),
        "weather_humidity_pct": _pick("relative_humidity_2m"),
        "weather_wind_mps": _pick("wind_speed_10m"),
        "weather_code": _pick("weather_code"),
    }


def enrich_missing_weather(limit: int | None = None) -> int:
    """Fill weather fields for GPS activities that don't have them yet."""
    with session_scope() as session:
        ids = list(
            session.scalars(
                select(Activity.id)
                .where(Activity.has_gps.is_(True))
                .where(Activity.weather_temp_c.is_(None))
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
            midpoint = activity.start_time_utc.replace(tzinfo=timezone.utc) + timedelta(
                seconds=(activity.elapsed_s or 0) / 2
            )
            try:
                fields = _fetch_hour(position[0], position[1], midpoint)
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
