from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from backend.db import get_session
from backend.models import Activity, PlannedWorkout
from backend.schemas import PlanImport, PlanInfo, PlannedWorkoutIn, PlannedWorkoutOut

router = APIRouter(prefix="/api/plan", tags=["plan"])


def _completion_map(session: Session, start: date, end: date) -> dict[date, int]:
    """First run activity id per local date in [start, end]."""
    start_dt = datetime.combine(start, datetime.min.time())
    end_dt = datetime.combine(end + timedelta(days=1), datetime.min.time())
    runs = session.scalars(
        select(Activity)
        .where(Activity.start_time_local >= start_dt)
        .where(Activity.start_time_local < end_dt)
        .where(Activity.sport.contains("running"))
        .order_by(Activity.start_time_local)
    ).all()
    completion: dict[date, int] = {}
    for run in runs:
        completion.setdefault(run.start_time_local.date(), run.id)
    return completion


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
        .order_by(PlannedWorkout.day)
    ).all()
    completion = _completion_map(session, window_start, window_end)
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
            completed_activity_id=(
                completion.get(w.day) if w.workout_type not in ("rest",) else None
            ),
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
    return {"imported": len(payload.workouts)}


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
    completion = _completion_map(session, workout.day, workout.day)
    return PlannedWorkoutOut(
        id=workout.id,
        day=workout.day,
        title=workout.title,
        workout_type=workout.workout_type,
        description=workout.description,
        target_distance_m=workout.target_distance_m,
        target_duration_s=workout.target_duration_s,
        plan_name=workout.plan_name,
        completed_activity_id=(
            completion.get(workout.day) if workout.workout_type != "rest" else None
        ),
    )


@router.delete("/workouts/{workout_id}", response_model=dict)
def delete_workout(workout_id: int, session: Session = Depends(get_session)) -> dict:
    workout = session.get(PlannedWorkout, workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Planned workout not found")
    session.delete(workout)
    session.commit()
    return {"deleted": workout_id}


@router.delete("", response_model=dict)
def delete_plan(plan_name: str, session: Session = Depends(get_session)) -> dict:
    result = session.execute(
        delete(PlannedWorkout).where(PlannedWorkout.plan_name == plan_name)
    )
    session.commit()
    return {"deleted": result.rowcount}
