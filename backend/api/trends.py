from collections import defaultdict
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.analysis.training_load import fitness_series
from backend.db import get_session
from backend.models import Activity, BestEffort
from backend.schemas import (
    FitnessPoint,
    FormSnapshot,
    LogbookActivity,
    LogbookWeek,
    RecordEntry,
    StatsSummary,
    WeeklyStat,
    WeekSummary,
)

router = APIRouter(prefix="/api", tags=["trends"])


def _activity_load(activity: Activity, model: str) -> float:
    if model == "rtss":
        value = activity.rtss if activity.rtss is not None else activity.hrtss
    else:
        value = activity.trimp
    return value or 0.0


def _daily_loads(session: Session, model: str) -> dict[date, float]:
    loads: dict[date, float] = defaultdict(float)
    for activity in session.scalars(select(Activity)).all():
        loads[activity.start_time_local.date()] += _activity_load(activity, model)
    return dict(loads)


@router.get("/trends/fitness", response_model=list[FitnessPoint])
def fitness_trend(
    model: str = Query("trimp", pattern="^(trimp|rtss)$"),
    days: int = Query(365, ge=7, le=3650),
    session: Session = Depends(get_session),
) -> list[FitnessPoint]:
    today = date.today()
    series = fitness_series(_daily_loads(session, model), today - timedelta(days=days), today)
    return [
        FitnessPoint(
            day=p.day, load=round(p.load, 1), ctl=round(p.ctl, 1),
            atl=round(p.atl, 1), tsb=round(p.tsb, 1),
        )
        for p in series
    ]


def _week_start(day: date) -> date:
    return day - timedelta(days=day.weekday())


@router.get("/trends/weekly", response_model=list[WeeklyStat])
def weekly_trend(
    weeks: int = Query(52, ge=1, le=520), session: Session = Depends(get_session)
) -> list[WeeklyStat]:
    first_week = _week_start(date.today()) - timedelta(weeks=weeks - 1)
    buckets: dict[date, WeeklyStat] = {}
    for i in range(weeks):
        ws = first_week + timedelta(weeks=i)
        buckets[ws] = WeeklyStat(
            week_start=ws, run_distance_m=0, total_moving_s=0, load_trimp=0,
            load_rtss=0, activities=0, runs=0, ascent_m=0,
        )
    for activity in session.scalars(select(Activity)).all():
        ws = _week_start(activity.start_time_local.date())
        stat = buckets.get(ws)
        if stat is None:
            continue
        stat.total_moving_s += activity.moving_s
        stat.load_trimp += activity.trimp or 0.0
        stat.load_rtss += _activity_load(activity, "rtss")
        stat.activities += 1
        stat.ascent_m += activity.ascent_m or 0.0
        if activity.is_run:
            stat.runs += 1
            stat.run_distance_m += activity.distance_m
    return [buckets[k] for k in sorted(buckets)]


@router.get("/logbook", response_model=list[LogbookWeek])
def logbook(
    weeks: int = Query(16, ge=1, le=104),
    until: date | None = None,
    session: Session = Depends(get_session),
) -> list[LogbookWeek]:
    """Training-log weeks (newest first). `until` = newest Monday to include."""
    newest_ws = _week_start(until or date.today())
    oldest_ws = newest_ws - timedelta(weeks=weeks - 1)
    buckets: dict[date, LogbookWeek] = {
        oldest_ws + timedelta(weeks=i): LogbookWeek(week_start=oldest_ws + timedelta(weeks=i))
        for i in range(weeks)
    }

    start_dt = datetime.combine(oldest_ws, datetime.min.time())
    end_dt = datetime.combine(newest_ws + timedelta(days=7), datetime.min.time())
    activities = session.scalars(
        select(Activity)
        .where(Activity.start_time_local >= start_dt)
        .where(Activity.start_time_local < end_dt)
        .order_by(Activity.start_time_local)
    ).all()

    for activity in activities:
        day = activity.start_time_local.date()
        week = buckets.get(_week_start(day))
        if week is None:
            continue
        week.total_moving_s += activity.moving_s
        if activity.is_run:
            week.runs += 1
            week.run_distance_m += activity.distance_m
        week.activities.append(
            LogbookActivity(
                id=activity.id,
                name=activity.name,
                sport=activity.sport,
                day_index=day.weekday(),
                distance_m=activity.distance_m,
                moving_s=activity.moving_s,
                start_time_local=activity.start_time_local,
                is_workout=activity.is_workout,
            )
        )

    return [buckets[k] for k in sorted(buckets, reverse=True)]


@router.get("/records", response_model=list[RecordEntry])
def records(
    top: int = Query(3, ge=1, le=10), session: Session = Depends(get_session)
) -> list[RecordEntry]:
    efforts = session.scalars(
        select(BestEffort).order_by(BestEffort.label, BestEffort.duration_s)
    ).all()
    per_label: dict[str, int] = defaultdict(int)
    results: list[RecordEntry] = []
    for effort in efforts:
        if per_label[effort.label] >= top:
            continue
        per_label[effort.label] += 1
        results.append(
            RecordEntry(
                label=effort.label,
                distance_m=effort.distance_m,
                duration_s=effort.duration_s,
                activity_id=effort.activity_id,
                activity_name=effort.activity.name,
                start_time_local=effort.activity.start_time_local,
            )
        )
    return results


@router.get("/stats/summary", response_model=StatsSummary)
def stats_summary(session: Session = Depends(get_session)) -> StatsSummary:
    today = date.today()
    this_ws = _week_start(today)
    last_ws = this_ws - timedelta(weeks=1)
    weeks = {this_ws: WeekSummary(), last_ws: WeekSummary()}

    activities = session.scalars(select(Activity)).all()
    for activity in activities:
        ws = _week_start(activity.start_time_local.date())
        summary = weeks.get(ws)
        if summary is None:
            continue
        summary.total_moving_s += activity.moving_s
        summary.load_trimp += activity.trimp or 0.0
        summary.activities += 1
        if activity.is_run:
            summary.runs += 1
            summary.run_distance_m += activity.distance_m

    snapshots = {}
    for model in ("trimp", "rtss"):
        series = fitness_series(
            _daily_loads(session, model), today - timedelta(days=6), today
        )
        last = series[-1]
        snapshots[model] = FormSnapshot(
            ctl=round(last.ctl, 1), atl=round(last.atl, 1), tsb=round(last.tsb, 1)
        )

    return StatsSummary(
        this_week=weeks[this_ws],
        last_week=weeks[last_ws],
        form_trimp=snapshots["trimp"],
        form_rtss=snapshots["rtss"],
        total_activities=len(activities),
    )
