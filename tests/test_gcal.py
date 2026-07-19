from datetime import date

from backend.ics import plan_to_ics
from backend.models import PlannedWorkout
from backend.plan_export import stable_keys
from backend.sync.gcal import event_body, plan_diff


def _workout(id_, day, title="Easy run", plan="base", **kwargs):
    return PlannedWorkout(
        id=id_,
        day=day,
        title=title,
        workout_type=kwargs.pop("workout_type", "easy"),
        description=kwargs.pop("description", ""),
        target_distance_m=kwargs.pop("target_distance_m", None),
        target_duration_s=kwargs.pop("target_duration_s", None),
        plan_name=plan,
    )


def _event(workout, key, event_id):
    return {"id": event_id, **event_body(workout, key)}


def test_stable_keys_survive_reimport_with_new_ids():
    original = [
        _workout(1, date(2026, 8, 3)),
        _workout(2, date(2026, 8, 5), title="Intervals"),
    ]
    reimported = [
        _workout(11, date(2026, 8, 3)),
        _workout(12, date(2026, 8, 5), title="Intervals"),
    ]
    assert list(stable_keys(original).values()) == list(stable_keys(reimported).values())


def test_stable_keys_distinct_for_doubles_and_plans():
    day = date(2026, 8, 3)
    workouts = [
        _workout(1, day, title="AM easy"),
        _workout(2, day, title="PM strides"),
        _workout(3, day, plan="other-plan"),
    ]
    keys = stable_keys(workouts)
    assert len(set(keys.values())) == 3


def test_ics_uids_stable_across_reimport():
    workouts = [_workout(1, date(2026, 8, 3)), _workout(2, date(2026, 8, 4))]
    reimported = [_workout(21, date(2026, 8, 3)), _workout(22, date(2026, 8, 4))]
    uids = [line for line in plan_to_ics(workouts).splitlines() if line.startswith("UID:")]
    assert uids == [
        line for line in plan_to_ics(reimported).splitlines() if line.startswith("UID:")
    ]
    assert len(set(uids)) == 2


def test_event_body_all_day_and_marked():
    workout = _workout(
        1,
        date(2026, 8, 3),
        title="Long run",
        description="Steady, hilly loop",
        target_distance_m=26000,
    )
    body = event_body(workout, "abc123")
    assert body["start"] == {"date": "2026-08-03"}
    assert body["end"] == {"date": "2026-08-04"}
    assert body["summary"] == "Long run"
    assert "Target: 26.0 km" in body["description"]
    assert body["extendedProperties"]["private"] == {"fartlek": "plan", "fartlek_key": "abc123"}


def test_diff_empty_calendar_inserts_everything():
    workouts = [_workout(1, date(2026, 8, 3)), _workout(2, date(2026, 8, 4))]
    to_insert, to_patch, to_delete, unchanged = plan_diff(workouts, [])
    assert len(to_insert) == 2
    assert (to_patch, to_delete, unchanged) == ([], [], 0)


def test_diff_unchanged_plan_is_a_noop():
    workouts = [_workout(1, date(2026, 8, 3)), _workout(2, date(2026, 8, 4))]
    keys = stable_keys(workouts)
    events = [_event(w, keys[w.id], f"ev{w.id}") for w in workouts]
    to_insert, to_patch, to_delete, unchanged = plan_diff(workouts, events)
    assert (to_insert, to_patch, to_delete) == ([], [], [])
    assert unchanged == 2


def test_diff_revised_plan_updates_in_place_without_duplicates():
    original = [
        _workout(1, date(2026, 8, 3)),
        _workout(2, date(2026, 8, 4), title="Tempo"),
        _workout(3, date(2026, 8, 5), title="Long run"),
    ]
    keys = stable_keys(original)
    events = [_event(w, keys[w.id], f"ev{w.id}") for w in original]
    # Trainer revises: new ids (replace_plan), one title changed, long run dropped.
    revised = [
        _workout(11, date(2026, 8, 3)),
        _workout(12, date(2026, 8, 4), title="Tempo 3x10 min"),
    ]
    to_insert, to_patch, to_delete, unchanged = plan_diff(revised, events)
    assert to_insert == []
    assert [(event_id, body["summary"]) for event_id, body in to_patch] == [
        ("ev2", "Tempo 3x10 min")
    ]
    assert to_delete == ["ev3"]
    assert unchanged == 1


def test_diff_removes_duplicate_and_unkeyed_marker_events():
    workout = _workout(1, date(2026, 8, 3))
    key = stable_keys([workout])[1]
    events = [
        _event(workout, key, "ev-good"),
        _event(workout, key, "ev-dupe"),
        {"id": "ev-unkeyed", "summary": "stray", "extendedProperties": {"private": {}}},
    ]
    to_insert, to_patch, to_delete, unchanged = plan_diff([workout], events)
    assert (to_insert, to_patch) == ([], [])
    assert sorted(to_delete) == ["ev-dupe", "ev-unkeyed"]
    assert unchanged == 1
