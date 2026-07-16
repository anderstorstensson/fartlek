"""Daily wellness sync from Garmin Connect (sleep, HRV, RHR, body battery, stress).

Each Garmin endpoint is fetched defensively: the payload shapes vary between
account types and API versions, and any single missing metric must not break
the sync — a day is stored with whatever could be read.
"""

import logging
from datetime import date, timedelta

from sqlalchemy import select

from backend.db import session_scope
from backend.models import DailyWellness

logger = logging.getLogger(__name__)

DEFAULT_BACKFILL_DAYS = 90
_REFRESH_TAIL_DAYS = 2  # today/yesterday keep changing; always re-fetch them


def _dig(payload, *path):
    value = payload
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _fetch_day(client, day: date) -> dict:
    iso = day.isoformat()
    fields: dict = {}

    try:
        summary = client.get_user_summary(iso) or {}
        fields["resting_hr"] = summary.get("restingHeartRate")
        fields["stress_avg"] = summary.get("averageStressLevel")
        fields["body_battery_max"] = summary.get("bodyBatteryHighestValue")
        fields["body_battery_min"] = summary.get("bodyBatteryLowestValue")
        fields["steps"] = summary.get("totalSteps")
        if fields["stress_avg"] is not None and fields["stress_avg"] < 0:
            fields["stress_avg"] = None  # Garmin uses -1/-2 for "no data"
    except Exception as exc:
        logger.debug("Wellness: user summary failed for %s: %s", iso, exc)

    try:
        hrv = client.get_hrv_data(iso) or {}
        fields["hrv_last_night_avg"] = _dig(hrv, "hrvSummary", "lastNightAvg")
        fields["hrv_status"] = _dig(hrv, "hrvSummary", "status")
    except Exception as exc:
        logger.debug("Wellness: HRV failed for %s: %s", iso, exc)

    try:
        sleep = client.get_sleep_data(iso) or {}
        dto = sleep.get("dailySleepDTO") or {}
        fields["sleep_s"] = dto.get("sleepTimeSeconds")
        fields["deep_sleep_s"] = dto.get("deepSleepSeconds")
        fields["sleep_score"] = _dig(dto, "sleepScores", "overall", "value")
    except Exception as exc:
        logger.debug("Wellness: sleep failed for %s: %s", iso, exc)

    return {k: v for k, v in fields.items() if v is not None}


def sync_wellness(client, backfill_days: int | None = None) -> int:
    """Fetch wellness from the day after the newest stored row (or a backfill
    window) through today. Returns the number of days written."""
    today = date.today()
    with session_scope() as session:
        newest = session.scalars(
            select(DailyWellness.day).order_by(DailyWellness.day.desc()).limit(1)
        ).first()

    if backfill_days is not None:
        start = today - timedelta(days=backfill_days)
    elif newest is not None:
        start = min(newest + timedelta(days=1), today - timedelta(days=_REFRESH_TAIL_DAYS))
    else:
        start = today - timedelta(days=DEFAULT_BACKFILL_DAYS)

    written = 0
    day = start
    while day <= today:
        fields = _fetch_day(client, day)
        if fields:
            with session_scope() as session:
                row = session.get(DailyWellness, day)
                if row is None:
                    row = DailyWellness(day=day)
                    session.add(row)
                for key, value in fields.items():
                    setattr(row, key, value)
            written += 1
        day += timedelta(days=1)
    return written
