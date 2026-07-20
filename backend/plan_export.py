"""Shared helpers for exporting the training plan (ICS feed, Google Calendar).

Export keys must survive plan re-imports: replace_plan deletes and recreates
rows, so database ids change even when the workouts themselves are unchanged.
Keys are therefore derived from (plan_name, day, ordinal-within-day) — a
revised plan updates its existing calendar events in place instead of
orphaning them and creating duplicates.
"""

import hashlib
from datetime import date

from backend.models import PlannedWorkout


def stable_keys(workouts: list[PlannedWorkout]) -> dict[int, str]:
    """Map each workout id to a key that is stable across delete-and-recreate
    imports. Doubles (two workouts on one day in the same plan) get distinct
    ordinals in id order, which matches their creation order."""
    ordered = sorted(workouts, key=lambda w: (w.plan_name, w.day, w.id))
    keys: dict[int, str] = {}
    counts: dict[tuple[str, date], int] = {}
    for workout in ordered:
        slot = (workout.plan_name, workout.day)
        ordinal = counts.get(slot, 0)
        counts[slot] = ordinal + 1
        raw = f"{workout.plan_name}|{workout.day.isoformat()}|{ordinal}"
        keys[workout.id] = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]
    return keys


def description_text(workout: PlannedWorkout) -> str:
    parts = []
    if workout.description:
        parts.append(workout.description)
    if workout.target_distance_m:
        parts.append(f"Target: {workout.target_distance_m / 1000:.1f} km")
    if workout.target_duration_s:
        minutes = int(workout.target_duration_s // 60)
        parts.append(f"Duration: {minutes} min")
    if workout.plan_name:
        parts.append(f"Plan: {workout.plan_name}")
    return "\n".join(parts)
