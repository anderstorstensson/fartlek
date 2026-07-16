"""Daily wellness (sleep, HRV, RHR, body battery, stress) and a readiness summary."""

import statistics
from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db import get_session
from backend.models import DailyWellness
from backend.schemas import ReadinessOut, WellnessDay

router = APIRouter(prefix="/api/wellness", tags=["wellness"])

_BASELINE_DAYS = 30
_HRV_LOW_FACTOR = 0.85
_RHR_HIGH_MARGIN_BPM = 5
_SLEEP_SCORE_LOW = 60


@router.get("", response_model=list[WellnessDay])
def list_wellness(
    days: int = Query(90, ge=1, le=1095), session: Session = Depends(get_session)
) -> list[WellnessDay]:
    since = date.today() - timedelta(days=days)
    rows = session.scalars(
        select(DailyWellness).where(DailyWellness.day >= since).order_by(DailyWellness.day)
    ).all()
    return list(rows)


def _median(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


@router.get("/readiness", response_model=ReadinessOut | None)
def readiness(session: Session = Depends(get_session)) -> ReadinessOut | None:
    """Latest wellness day scored against its 30-day baselines. Null when no data."""
    latest = session.scalars(
        select(DailyWellness).order_by(DailyWellness.day.desc()).limit(1)
    ).first()
    if latest is None:
        return None

    baseline_rows = session.scalars(
        select(DailyWellness)
        .where(DailyWellness.day >= latest.day - timedelta(days=_BASELINE_DAYS))
        .where(DailyWellness.day < latest.day)
    ).all()
    hrv_baseline = _median([r.hrv_last_night_avg for r in baseline_rows if r.hrv_last_night_avg])
    rhr_baseline = _median([float(r.resting_hr) for r in baseline_rows if r.resting_hr])

    flags: list[str] = []
    if latest.hrv_last_night_avg and hrv_baseline and (
        latest.hrv_last_night_avg < hrv_baseline * _HRV_LOW_FACTOR
    ):
        flags.append("hrv-low")
    if latest.resting_hr and rhr_baseline and (
        latest.resting_hr > rhr_baseline + _RHR_HIGH_MARGIN_BPM
    ):
        flags.append("rhr-elevated")
    if latest.sleep_score is not None and latest.sleep_score < _SLEEP_SCORE_LOW:
        flags.append("sleep-poor")

    status = "ready" if not flags else ("caution" if len(flags) == 1 else "rest")
    return ReadinessOut(
        day=latest.day,
        resting_hr=latest.resting_hr,
        resting_hr_baseline=round(rhr_baseline, 1) if rhr_baseline else None,
        hrv_last_night_avg=latest.hrv_last_night_avg,
        hrv_baseline=round(hrv_baseline, 1) if hrv_baseline else None,
        sleep_score=latest.sleep_score,
        sleep_s=latest.sleep_s,
        body_battery_max=latest.body_battery_max,
        stress_avg=latest.stress_avg,
        flags=flags,
        status=status,
    )
