"""Estimate future daily training load from planned workouts.

Used to extend the CTL/ATL/TSB curve past today so the athlete can see the
form (TSB) the current plan produces on race day. Loads are estimated on the
TSS scale (hours × IF² × 100) from each workout's target duration or distance
and a typical intensity factor per workout type; TRIMP-model projections are
rescaled by the athlete's own recent TRIMP-per-hrTSS ratio.
"""

import statistics
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models import Activity, AthleteSettings, PlannedWorkout

# Typical session intensity factor (vs threshold) per workout type. Interval
# and tempo values are session averages including recoveries, not rep paces.
_TYPE_IF = {
    "easy": 0.68,
    "long": 0.72,
    "tempo": 0.87,
    "intervals": 0.92,
    "race": 1.00,
    "cross": 0.65,
    "rest": 0.0,
}
_TRIMP_RATIO_WINDOW_DAYS = 60


def _workout_hours(workout: PlannedWorkout, threshold_speed_mps: float, intensity: float) -> float:
    if workout.target_duration_s:
        return workout.target_duration_s / 3600.0
    if workout.target_distance_m and threshold_speed_mps > 0 and intensity > 0:
        speed = threshold_speed_mps * intensity
        return workout.target_distance_m / speed / 3600.0
    return 0.0


def estimated_tss(workout: PlannedWorkout, settings: AthleteSettings) -> float:
    intensity = _TYPE_IF.get(workout.workout_type, 0.68)
    if intensity <= 0:
        return 0.0
    threshold_speed = (
        1000.0 / settings.threshold_pace_s_per_km if settings.threshold_pace_s_per_km else 0.0
    )
    hours = _workout_hours(workout, threshold_speed, intensity)
    return hours * intensity**2 * 100.0


def trimp_per_tss_ratio(session: Session) -> float:
    """The athlete's recent TRIMP:hrTSS ratio, to translate TSS-scale estimates
    into the TRIMP model. Falls back to 1.0 without enough data."""
    since = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(
        days=_TRIMP_RATIO_WINDOW_DAYS
    )
    rows = session.execute(
        select(Activity.trimp, Activity.hrtss)
        .where(Activity.start_time_utc >= since)
        .where(Activity.trimp.is_not(None))
        .where(Activity.hrtss.is_not(None))
    ).all()
    ratios = [trimp / tss for trimp, tss in rows if tss and tss > 0]
    if len(ratios) < 5:
        return 1.0
    return statistics.median(ratios)


def projected_daily_loads(
    session: Session,
    settings: AthleteSettings,
    start: date,
    end: date,
    model: str,
) -> dict[date, float]:
    """Estimated load per future day from uncompleted planned workouts."""
    workouts = session.scalars(
        select(PlannedWorkout).where(PlannedWorkout.day >= start).where(PlannedWorkout.day <= end)
    ).all()
    scale = trimp_per_tss_ratio(session) if model == "trimp" else 1.0
    loads: dict[date, float] = {}
    for workout in workouts:
        tss = estimated_tss(workout, settings)
        if tss <= 0:
            continue
        loads[workout.day] = loads.get(workout.day, 0.0) + tss * scale
    return loads
