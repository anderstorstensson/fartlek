import re
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from backend.db import get_session
from backend.ics import plan_to_ics
from backend.models import Activity, PlannedWorkout
from backend.schemas import PlanImport, PlanInfo, PlannedWorkoutIn, PlannedWorkoutOut
from backend.sync.gcal import sync_in_background as gcal_sync_in_background

router = APIRouter(prefix="/api/plan", tags=["plan"])


def _activity_map(session: Session, start: date, end: date) -> dict[date, dict[str, list[int]]]:
    """Activity ids per local date in [start, end], split into runs and other sports.

    Walking is excluded — it is never a prescribed session and would falsely
    complete cross-training workouts.
    """
    start_dt = datetime.combine(start, datetime.min.time())
    end_dt = datetime.combine(end + timedelta(days=1), datetime.min.time())
    activities = session.scalars(
        select(Activity)
        .where(Activity.start_time_local >= start_dt)
        .where(Activity.start_time_local < end_dt)
        .where(Activity.sport != "walking")
        .order_by(Activity.start_time_local)
    ).all()
    days: dict[date, dict[str, list[int]]] = {}
    for activity in activities:
        day = days.setdefault(activity.start_time_local.date(), {"runs": [], "other": []})
        kind = "runs" if "running" in (activity.sport or "") else "other"
        day[kind].append(activity.id)
    return days


def _assign_completions(
    workouts: list[PlannedWorkout], days: dict[date, dict[str, list[int]]]
) -> dict[int, int | None]:
    """Pair each planned workout with an activity of the matching kind, in order.

    Run-type workouts consume that day's runs in start-time order (so doubles pair
    AM/PM correctly), `cross` workouts consume non-running activities, `rest` never
    completes.
    """
    consumed: dict[tuple[date, str], int] = {}
    completions: dict[int, int | None] = {}
    for workout in workouts:
        if workout.workout_type == "rest":
            completions[workout.id] = None
            continue
        kind = "other" if workout.workout_type == "cross" else "runs"
        ids = days.get(workout.day, {}).get(kind, [])
        index = consumed.get((workout.day, kind), 0)
        completions[workout.id] = ids[index] if index < len(ids) else None
        consumed[(workout.day, kind)] = index + 1
    return completions


@router.get("", response_model=list[PlannedWorkoutOut])
def get_plan(
    start: date | None = None,
    end: date | None = None,
    session: Session = Depends(get_session),
) -> list[PlannedWorkoutOut]:
    window_start = start or date.today()
    window_end = end or window_start + timedelta(days=28)
    workouts = session.scalars(
        select(PlannedWorkout)
        .where(PlannedWorkout.day >= window_start)
        .where(PlannedWorkout.day <= window_end)
        .order_by(PlannedWorkout.day, PlannedWorkout.id)
    ).all()
    days = _activity_map(session, window_start, window_end)
    completions = _assign_completions(workouts, days)
    return [
        PlannedWorkoutOut(
            id=w.id,
            day=w.day,
            title=w.title,
            workout_type=w.workout_type,
            description=w.description,
            target_distance_m=w.target_distance_m,
            target_duration_s=w.target_duration_s,
            plan_name=w.plan_name,
            completed_activity_id=completions[w.id],
        )
        for w in workouts
    ]


@router.post("", response_model=dict)
def import_plan(payload: PlanImport, session: Session = Depends(get_session)) -> dict:
    if payload.replace_plan:
        plan_names = {w.plan_name for w in payload.workouts}
        session.execute(
            delete(PlannedWorkout).where(PlannedWorkout.plan_name.in_(plan_names))
        )
    for workout in payload.workouts:
        session.add(PlannedWorkout(**workout.model_dump()))
    session.commit()
    gcal_sync_in_background()
    return {"imported": len(payload.workouts)}


@router.get("/export.ics")
def export_ics(
    plan_name: str | None = None, session: Session = Depends(get_session)
) -> Response:
    query = select(PlannedWorkout).order_by(PlannedWorkout.day)
    if plan_name:
        query = query.where(PlannedWorkout.plan_name == plan_name)
    workouts = session.scalars(query).all()
    if not workouts:
        raise HTTPException(status_code=404, detail="No planned workouts to export")
    calendar_name = plan_name or "Fartlek training plan"
    # HTTP headers are latin-1 only — reduce the filename to safe ASCII.
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", plan_name or "fartlek-plan").strip("-")
    filename = safe or "fartlek-plan"
    return Response(
        content=plan_to_ics(workouts, calendar_name=calendar_name),
        media_type="text/calendar; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}.ics"'},
    )


@router.get("/plans", response_model=list[PlanInfo])
def list_plans(session: Session = Depends(get_session)) -> list[PlanInfo]:
    rows = session.execute(
        select(
            PlannedWorkout.plan_name,
            func.count(PlannedWorkout.id),
            func.min(PlannedWorkout.day),
            func.max(PlannedWorkout.day),
        ).group_by(PlannedWorkout.plan_name)
    ).all()
    return [
        PlanInfo(plan_name=name or "(unnamed)", workouts=count, first_day=first, last_day=last)
        for name, count, first, last in rows
    ]


@router.put("/workouts/{workout_id}", response_model=PlannedWorkoutOut)
def update_workout(
    workout_id: int,
    payload: PlannedWorkoutIn,
    session: Session = Depends(get_session),
) -> PlannedWorkoutOut:
    workout = session.get(PlannedWorkout, workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Planned workout not found")
    for field, value in payload.model_dump().items():
        setattr(workout, field, value)
    session.commit()
    gcal_sync_in_background()
    days = _activity_map(session, workout.day, workout.day)
    completions = _assign_completions([workout], days)
    return PlannedWorkoutOut(
        id=workout.id,
        day=workout.day,
        title=workout.title,
        workout_type=workout.workout_type,
        description=workout.description,
        target_distance_m=workout.target_distance_m,
        target_duration_s=workout.target_duration_s,
        plan_name=workout.plan_name,
        completed_activity_id=completions[workout.id],
    )


@router.delete("/workouts/{workout_id}", response_model=dict)
def delete_workout(workout_id: int, session: Session = Depends(get_session)) -> dict:
    workout = session.get(PlannedWorkout, workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Planned workout not found")
    session.delete(workout)
    session.commit()
    gcal_sync_in_background()
    return {"deleted": workout_id}


@router.delete("", response_model=dict)
def delete_plan(plan_name: str, session: Session = Depends(get_session)) -> dict:
    result = session.execute(
        delete(PlannedWorkout).where(PlannedWorkout.plan_name == plan_name)
    )
    session.commit()
    gcal_sync_in_background()
    return {"deleted": result.rowcount}
