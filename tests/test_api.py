import os
import tempfile
from datetime import datetime

import pytest

os.environ["FARTLEK_SCHEDULER_ENABLED"] = "0"
os.environ["FARTLEK_DATA_DIR"] = tempfile.mkdtemp(prefix="fartlek-test-")

from fastapi.testclient import TestClient  # noqa: E402

from backend.db import session_scope  # noqa: E402
from backend.main import app  # noqa: E402
from backend.models import (  # noqa: E402
    Activity,
    BestEffort,
    CoachMessage,
    DailyWellness,
    Lap,
    Stream,
)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        with session_scope() as session:
            session.add(
                Activity(
                    id=1,
                    name="Morning Run",
                    sport="running",
                    start_time_utc=datetime(2026, 7, 13, 6, 0),
                    start_time_local=datetime(2026, 7, 13, 8, 0),
                    elapsed_s=3600,
                    moving_s=3500,
                    distance_m=12000,
                    avg_hr=150,
                    trimp=110.0,
                    rtss=95.0,
                    hrtss=90.0,
                    perceived_exertion=7,
                    feel=3,
                )
            )
            session.add(
                Stream(
                    activity_id=1,
                    time_s=[0, 1, 2],
                    distance_m=[0, 5, 10],
                    hr=[120, 125, 130],
                    speed_mps=[3.0, 3.1, 3.2],
                    altitude_m=[10, 11, 12],
                    cadence=[170, 172, 171],
                    lat=[59.0, 59.001, 59.002],
                    lng=[18.0, 18.001, 18.002],
                )
            )
        yield test_client


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_list_activities(client):
    body = client.get("/api/activities").json()
    assert body["total"] == 1
    assert body["items"][0]["name"] == "Morning Run"


def test_self_evaluation_served(client):
    item = client.get("/api/activities").json()["items"][0]
    assert item["perceived_exertion"] == 7
    assert item["feel"] == 3
    detail = client.get("/api/activities/1").json()
    assert detail["perceived_exertion"] == 7
    assert detail["feel"] == 3


def test_has_analysis_marker(client):
    assert client.get("/api/activities").json()["items"][0]["has_analysis"] is False

    note = client.post(
        "/api/notes",
        json={"activity_id": 1, "kind": "session", "title": "t", "content": "c"},
    ).json()
    assert client.get("/api/activities").json()["items"][0]["has_analysis"] is True
    assert client.get("/api/activities/1").json()["has_analysis"] is True
    week = next(w for w in client.get("/api/logbook?weeks=4").json()
                if w["week_start"] == "2026-07-13")
    assert week["activities"][0]["has_analysis"] is True

    client.delete(f"/api/notes/{note['id']}")
    assert client.get("/api/activities").json()["items"][0]["has_analysis"] is False


def test_activity_detail_and_404(client):
    assert client.get("/api/activities/1").status_code == 200
    assert client.get("/api/activities/999").status_code == 404


def test_fitness_trend(client):
    points = client.get("/api/trends/fitness?model=trimp&days=30").json()
    assert len(points) == 31
    assert any(p["load"] > 0 for p in points)
    assert points[-1]["ctl"] > 0


def test_fitness_trend_rejects_bad_model(client):
    assert client.get("/api/trends/fitness?model=bogus").status_code == 422


def test_weekly_trend(client):
    stats = client.get("/api/trends/weekly?weeks=8").json()
    assert len(stats) == 8
    assert sum(s["runs"] for s in stats) == 1


def test_settings_roundtrip(client):
    payload = {
        "resting_hr": 48,
        "max_hr": 188,
        "lthr": 168,
        "threshold_pace_s_per_km": 255,
        "sex": "male",
    }
    updated = client.put("/api/settings", json=payload).json()
    assert updated["max_hr"] == 188
    assert len(updated["zones"]) == 5
    assert client.get("/api/settings").json()["resting_hr"] == 48


def test_settings_zone_modes(client):
    base = {"resting_hr": 48, "max_hr": 188, "lthr": 168,
            "threshold_pace_s_per_km": 255, "sex": "male"}

    lthr_zones = client.put(
        "/api/settings", json={**base, "zone_mode": "lthr"}
    ).json()["zones"]
    assert lthr_zones[4]["low_bpm"] == 168  # Z5 starts at LTHR

    manual = client.put(
        "/api/settings",
        json={**base, "zone_mode": "manual",
              "manual_zone_bounds": [100, 130, 145, 160, 172]},
    ).json()
    assert [z["low_bpm"] for z in manual["zones"]] == [100, 130, 145, 160, 172]
    assert manual["zones"][4]["high_bpm"] is None

    # Manual mode requires 5 strictly increasing bounds.
    bad = client.put(
        "/api/settings",
        json={**base, "zone_mode": "manual", "manual_zone_bounds": [100, 90, 145, 160, 172]},
    )
    assert bad.status_code == 422
    # Merge semantics: stored bounds satisfy a bare mode switch, so clearing
    # them explicitly is what makes manual-without-bounds invalid.
    assert client.put(
        "/api/settings",
        json={**base, "zone_mode": "manual", "manual_zone_bounds": None},
    ).status_code == 422

    # Restore default mode (and clear the stored bounds) for other tests.
    client.put(
        "/api/settings",
        json={**base, "zone_mode": "max_hr", "manual_zone_bounds": None},
    )


def test_settings_validation(client):
    bad = {"resting_hr": 5, "max_hr": 188, "lthr": 168,
           "threshold_pace_s_per_km": 255, "sex": "male"}
    assert client.put("/api/settings", json=bad).status_code == 422


def test_units_setting(client):
    assert client.get("/api/settings").json()["units"] == "metric"

    updated = client.put("/api/settings", json={"units": "imperial"}).json()
    assert updated["units"] == "imperial"
    assert client.get("/api/settings").json()["units"] == "imperial"

    # Display-only setting: a partial update must not touch anything else.
    assert updated["threshold_pace_s_per_km"] == client.get(
        "/api/settings"
    ).json()["threshold_pace_s_per_km"]

    assert client.put("/api/settings", json={"units": "miles"}).status_code == 422
    assert client.put("/api/settings", json={"units": "freedom"}).status_code == 422

    client.put("/api/settings", json={"units": "metric"})  # restore for other tests


def test_partial_settings_update_preserves_other_fields(client):
    """A partial PUT (e.g. the coach updating threshold pace) must never reset
    unmentioned settings to their defaults — the bug that wiped tone/model."""
    client.put("/api/settings", json={
        "coaching_tone": "drill", "coach_model": "sonnet", "display_locale": "en-GB",
    })

    updated = client.put("/api/settings", json={"threshold_pace_s_per_km": 240}).json()
    assert updated["threshold_pace_s_per_km"] == 240
    assert updated["coaching_tone"] == "drill"
    assert updated["coach_model"] == "sonnet"
    assert updated["display_locale"] == "en-GB"

    # Cross-field rules validate against the MERGED state: switching to manual
    # zones with bounds explicitly null is rejected, without touching other fields.
    assert client.put(
        "/api/settings", json={"zone_mode": "manual", "manual_zone_bounds": None}
    ).status_code == 422
    assert client.get("/api/settings").json()["coaching_tone"] == "drill"

    # restore
    client.put("/api/settings", json={
        "coaching_tone": "balanced", "coach_model": "", "display_locale": "",
    })


def test_logbook(client):
    weeks = client.get("/api/logbook?weeks=4").json()
    assert len(weeks) == 4
    # Weeks come newest first; 2026-07-13 is a Monday in the current week.
    assert weeks[0]["week_start"] > weeks[1]["week_start"]
    week = next(w for w in weeks if w["week_start"] == "2026-07-13")
    assert week["runs"] == 1
    assert week["run_distance_m"] == 12000
    assert week["activities"][0]["day_index"] == 0


def test_logbook_until_pagination(client):
    weeks = client.get("/api/logbook?weeks=2&until=2026-06-01").json()
    assert [w["week_start"] for w in weeks] == ["2026-06-01", "2026-05-25"]
    assert all(w["activities"] == [] for w in weeks)


def test_track_thumbnail(client):
    points = client.get("/api/activities/1/track").json()
    assert len(points) == 3
    assert points[0] == [59.0, 18.0]
    assert points[-1] == [59.002, 18.002]
    # No stream -> empty list rather than 404, so thumbnails degrade quietly.
    assert client.get("/api/activities/999/track").json() == []


def test_plan_import_and_completion(client):
    payload = {
        "replace_plan": True,
        "workouts": [
            # Same date as the seeded run -> should be marked completed.
            {"day": "2026-07-13", "title": "Easy 10K", "workout_type": "easy",
             "target_distance_m": 10000, "plan_name": "test-plan"},
            {"day": "2026-07-14", "title": "Rest", "workout_type": "rest",
             "plan_name": "test-plan"},
        ],
    }
    assert client.post("/api/plan", json=payload).json() == {"imported": 2}

    workouts = client.get("/api/plan?start=2026-07-13&end=2026-07-14").json()
    assert len(workouts) == 2
    assert workouts[0]["completed_activity_id"] == 1
    assert workouts[1]["completed_activity_id"] is None  # rest days never "complete"

    plans = client.get("/api/plan/plans").json()
    assert plans[0]["plan_name"] == "test-plan"
    assert plans[0]["workouts"] == 2

    # replace_plan replaces, not appends
    client.post("/api/plan", json=payload)
    assert client.get("/api/plan/plans").json()[0]["workouts"] == 2

    assert client.delete("/api/plan?plan_name=test-plan").json() == {"deleted": 2}
    assert client.get("/api/plan/plans").json() == []


def test_plan_typed_completion_and_doubles(client):
    payload = {
        "workouts": [
            # Three sessions on the seeded run's date: a double (two runs) + strength.
            {"day": "2026-07-13", "title": "AM Easy 10K", "workout_type": "easy",
             "target_distance_m": 10000, "plan_name": "typed-test"},
            {"day": "2026-07-13", "title": "PM Easy 6K", "workout_type": "easy",
             "target_distance_m": 6000, "plan_name": "typed-test"},
            {"day": "2026-07-13", "title": "Strength A", "workout_type": "cross",
             "target_duration_s": 2700, "plan_name": "typed-test"},
        ],
    }
    client.post("/api/plan", json=payload)

    # One run exists that day: it completes the first run workout only — never the
    # second half of the double, and never the strength session.
    by_title = {w["title"]: w for w in
                client.get("/api/plan?start=2026-07-13&end=2026-07-13").json()}
    assert by_title["AM Easy 10K"]["completed_activity_id"] == 1
    assert by_title["PM Easy 6K"]["completed_activity_id"] is None
    assert by_title["Strength A"]["completed_activity_id"] is None

    # A strength activity completes the cross workout.
    with session_scope() as session:
        session.add(Activity(id=2, name="Gym", sport="strength_training",
                             start_time_utc=datetime(2026, 7, 13, 16, 0),
                             start_time_local=datetime(2026, 7, 13, 18, 0),
                             elapsed_s=2700, moving_s=2700, distance_m=0))
    by_title = {w["title"]: w for w in
                client.get("/api/plan?start=2026-07-13&end=2026-07-13").json()}
    assert by_title["Strength A"]["completed_activity_id"] == 2
    assert by_title["PM Easy 6K"]["completed_activity_id"] is None

    with session_scope() as session:
        session.delete(session.get(Activity, 2))
    client.delete("/api/plan?plan_name=typed-test")


def test_plan_update_workout(client):
    payload = {
        "workouts": [
            {"day": "2026-07-16", "title": "Tempo 6K", "workout_type": "tempo",
             "plan_name": "adjust-test"},
        ],
    }
    client.post("/api/plan", json=payload)
    workout = client.get("/api/plan?start=2026-07-16&end=2026-07-16").json()[0]

    # Simulate "feeling sick": convert the tempo to an easy run two days later.
    updated = client.put(
        f"/api/plan/workouts/{workout['id']}",
        json={"day": "2026-07-18", "title": "Easy 6K", "workout_type": "easy",
              "description": "post-cold, keep HR in Z2", "plan_name": "adjust-test"},
    ).json()
    assert updated["day"] == "2026-07-18"
    assert updated["workout_type"] == "easy"

    assert client.get("/api/plan?start=2026-07-16&end=2026-07-16").json() == []
    assert client.put("/api/plan/workouts/99999", json=payload["workouts"][0]).status_code == 404
    client.delete("/api/plan?plan_name=adjust-test")


def test_plan_ics_export(client):
    payload = {
        "workouts": [
            {"day": "2026-08-03", "title": "6 × 1000m @ 3:26-3:32", "workout_type": "intervals",
             "description": "[vo2max] 2K warmup, 6x1000 w/ 2min jog, 2K cooldown",
             "target_distance_m": 12000, "plan_name": "ics-test"},
            {"day": "2026-08-05", "title": "Long run, easy", "workout_type": "long",
             "target_distance_m": 26000, "plan_name": "ics-test"},
        ],
    }
    client.post("/api/plan", json=payload)

    response = client.get("/api/plan/export.ics?plan_name=ics-test")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/calendar")
    body = response.text
    assert body.startswith("BEGIN:VCALENDAR")
    assert body.count("BEGIN:VEVENT") == 2
    assert "DTSTART;VALUE=DATE:20260803" in body
    assert "SUMMARY:6 × 1000m @ 3:26-3:32" in body
    assert "2K warmup\\, 6x1000 w/ 2min jog\\, 2K cooldown" in body  # commas escaped
    # RFC 5545: no unfolded line may exceed 75 octets
    assert all(len(line.encode()) <= 75 for line in body.split("\r\n"))

    assert client.get("/api/plan/export.ics?plan_name=nonexistent").status_code == 404
    client.delete("/api/plan?plan_name=ics-test")


def test_plan_ics_export_non_ascii_plan_name(client):
    # Em-dash and colon in the plan name must not break the download headers.
    name = "sub-2:45 Valencia — Dec 6"
    client.post("/api/plan", json={"workouts": [
        {"day": "2026-08-10", "title": "Easy 10K", "workout_type": "easy",
         "target_distance_m": 10000, "plan_name": name},
    ]})
    from urllib.parse import quote
    response = client.get(f"/api/plan/export.ics?plan_name={quote(name)}")
    assert response.status_code == 200
    disposition = response.headers["content-disposition"]
    assert disposition.encode("latin-1")  # header must be encodable
    assert 'filename="sub-2-45-Valencia-Dec-6.ics"' in disposition
    assert "X-WR-CALNAME:sub-2:45 Valencia — Dec 6" in response.text
    client.delete(f"/api/plan?plan_name={quote(name)}")


def test_plan_validates_workout_type(client):
    bad = {"workouts": [{"day": "2026-07-13", "title": "X", "workout_type": "fartlek"}]}
    assert client.post("/api/plan", json=bad).status_code == 422


def test_notes_crud(client):
    created = client.post(
        "/api/notes",
        json={"activity_id": 1, "kind": "session", "title": "Morning Run analysis",
              "content": "## Solid aerobic run\n- decoupling 2.1%"},
    ).json()
    assert created["id"] > 0

    by_activity = client.get("/api/notes?activity_id=1").json()
    assert len(by_activity) == 1
    assert by_activity[0]["title"] == "Morning Run analysis"
    assert client.get("/api/notes?activity_id=999").json() == []

    updated = client.put(
        f"/api/notes/{created['id']}",
        json={"activity_id": 1, "kind": "session", "title": "Morning Run analysis v2",
              "content": "revised"},
    ).json()
    assert updated["title"] == "Morning Run analysis v2"

    weekly = client.post(
        "/api/notes",
        json={"kind": "weekly", "title": "W28 check-in", "content": "on plan",
              "period_start": "2026-07-06", "period_end": "2026-07-12"},
    ).json()
    assert client.get("/api/notes?kind=weekly").json()[0]["id"] == weekly["id"]

    assert client.post("/api/notes", json={"kind": "bogus", "title": "x", "content": "y"}).status_code == 422

    race_note = client.post(
        "/api/notes",
        json={"activity_id": 1, "kind": "race", "title": "City 10K 39:30 — even split",
              "content": "held plan pace"},
    ).json()
    assert client.get("/api/notes?kind=race").json()[0]["id"] == race_note["id"]
    client.delete(f"/api/notes/{race_note['id']}")

    for note_id in (created["id"], weekly["id"]):
        assert client.delete(f"/api/notes/{note_id}").json() == {"deleted": note_id}
    assert client.delete("/api/notes/99999").status_code == 404


def test_coach_history_and_guards(client, monkeypatch):
    from backend.api import coach as coach_module
    loopback = {"host": f"127.0.0.1:{coach_module.config.port}"}

    # off by default: the agent endpoint — and the chat history — refuse until enabled
    assert client.get("/api/coach/status").json()["enabled"] is False
    assert client.get("/api/coach/messages", headers=loopback).status_code == 403
    assert client.post(
        "/api/coach/messages", json={"text": "hi"}, headers=loopback
    ).status_code == 403
    monkeypatch.setattr(coach_module.config, "coach_enabled", True, raising=False)

    assert client.get("/api/coach/messages", headers=loopback).json() == []

    with session_scope() as session:
        session.add(CoachMessage(role="user", content="how was my run?"))
        session.add(CoachMessage(role="assistant", content="## Solid\n…"))
    history = client.get("/api/coach/messages", headers=loopback).json()
    assert [m["role"] for m in history] == ["user", "assistant"]

    # history is behind the DNS-rebinding guard too
    assert client.get(
        "/api/coach/messages", headers={"host": "evil.example.com"}
    ).status_code == 403

    # refuses to run when not bound to localhost
    monkeypatch.setattr(coach_module.config, "host", "0.0.0.0", raising=False)
    assert client.post(
        "/api/coach/messages", json={"text": "hi"}, headers=loopback
    ).status_code == 403
    monkeypatch.setattr(coach_module.config, "host", "127.0.0.1", raising=False)

    # refuses a non-loopback Host header (DNS-rebinding guard) even when bound locally
    assert client.post(
        "/api/coach/messages", json={"text": "hi"}, headers={"host": "evil.example.com"}
    ).status_code == 403

    # clear error when the CLI is missing
    monkeypatch.setattr(coach_module.shutil, "which", lambda _: None)
    assert client.post(
        "/api/coach/messages", json={"text": "hi"}, headers=loopback
    ).status_code == 503

    assert client.post("/api/coach/reset", headers=loopback).json() == {"reset": True}
    assert client.get("/api/coach/messages", headers=loopback).json() == []


def test_sync_status(client):
    body = client.get("/api/sync/status").json()
    assert body["total_activities"] == 1
    assert body["logged_in"] in (True, False)


def test_streams_include_dynamics_arrays(client):
    """Rows imported before the dynamics columns existed serve [] not null."""
    body = client.get("/api/activities/1/streams").json()
    for key in ("power", "vertical_oscillation", "vertical_ratio",
                "step_length", "stance_time", "respiration"):
        assert body[key] == []


def test_streams_include_pace_zones(client):
    body = client.get("/api/activities/1/streams").json()
    assert len(body["pace_zones"]) == 5
    assert len(body["time_in_pace_zones_s"]) == 5
    assert body["pace_zones"][4]["high_speed_mps"] is None
    assert len(body["gap_speed_mps"]) == len(body["speed_mps"])


def test_coach_model_roundtrip(client):
    base = {"resting_hr": 48, "max_hr": 188, "lthr": 168,
            "threshold_pace_s_per_km": 255, "sex": "male"}
    assert client.get("/api/settings").json()["coach_model"] == ""
    updated = client.put("/api/settings", json={**base, "coach_model": "sonnet"}).json()
    assert updated["coach_model"] == "sonnet"
    assert client.put(
        "/api/settings", json={**base, "coach_model": "rm -rf /; sonnet"}
    ).status_code == 422
    client.put("/api/settings", json={**base, "coach_model": ""})


def test_display_locale_roundtrip(client):
    base = {"resting_hr": 48, "max_hr": 188, "lthr": 168,
            "threshold_pace_s_per_km": 255, "sex": "male"}
    assert client.get("/api/settings").json()["display_locale"] == ""
    updated = client.put("/api/settings", json={**base, "display_locale": "en-GB"}).json()
    assert updated["display_locale"] == "en-GB"
    assert client.put(
        "/api/settings", json={**base, "display_locale": "not a locale!!"}
    ).status_code == 422
    client.put("/api/settings", json={**base, "display_locale": ""})


def test_coaching_tone_roundtrip(client):
    base = {"resting_hr": 48, "max_hr": 188, "lthr": 168,
            "threshold_pace_s_per_km": 255, "sex": "male"}
    assert client.get("/api/settings").json()["coaching_tone"] == "balanced"
    updated = client.put("/api/settings", json={**base, "coaching_tone": "drill"}).json()
    assert updated["coaching_tone"] == "drill"
    assert client.put(
        "/api/settings", json={**base, "coaching_tone": "brutal"}
    ).status_code == 422
    client.put("/api/settings", json={**base, "coaching_tone": "balanced"})


def test_manual_pace_zones_roundtrip(client):
    base = {"resting_hr": 48, "max_hr": 188, "lthr": 168,
            "threshold_pace_s_per_km": 255, "sex": "male"}

    updated = client.put("/api/settings", json={
        **base, "pace_zone_mode": "manual",
        "manual_pace_zone_bounds": [450, 340, 300, 278, 255],
    }).json()
    assert updated["pace_zone_mode"] == "manual"
    assert updated["pace_zones"][0]["low_speed_mps"] == round(1000 / 450, 3)

    # bounds must get faster (decreasing s/km)
    assert client.put("/api/settings", json={
        **base, "pace_zone_mode": "manual",
        "manual_pace_zone_bounds": [300, 340, 300, 278, 255],
    }).status_code == 422

    restored = client.put("/api/settings", json={**base, "pace_zone_mode": "threshold"}).json()
    assert len(restored["pace_zones"]) == 5


def test_activity_edit_title_tag_and_note(client):
    updated = client.patch(
        "/api/activities/1",
        json={"name": "Easy shakeout", "tag": "recovery", "user_note": "slept badly"},
    ).json()
    assert updated["name"] == "Easy shakeout"
    assert updated["tag"] == "recovery"
    assert updated["user_note"] == "slept badly"

    # partial patch leaves other fields alone; empty tag clears it
    updated = client.patch("/api/activities/1", json={"tag": ""}).json()
    assert updated["tag"] is None
    assert updated["name"] == "Easy shakeout"

    assert client.patch("/api/activities/1", json={"tag": "bogus"}).status_code == 422
    assert client.patch("/api/activities/999", json={"tag": "race"}).status_code == 404

    with session_scope() as session:
        activity = session.get(Activity, 1)
        assert activity.name_locked  # user title survives future auto-naming
        activity.name = "Morning Run"  # restore for other tests
        activity.name_locked = False
        activity.user_note = ""


def test_activity_delete_cascades(client):
    # A throwaway activity with each cascade child, so the shared id=1 fixture
    # (relied on by other tests) is untouched.
    with session_scope() as session:
        session.add(
            Activity(
                id=777,
                name="Scratch run",
                sport="running",
                start_time_utc=datetime(2026, 7, 14, 6, 0),
                start_time_local=datetime(2026, 7, 14, 8, 0),
            )
        )
        session.flush()
        session.add(Stream(activity_id=777, time_s=[0, 1], hr=[120, 121]))
        session.add(Lap(activity_id=777, lap_index=0, distance_m=1000))
        session.add(
            BestEffort(
                activity_id=777,
                label="1K",
                distance_m=1000,
                duration_s=240,
                start_time_utc=datetime(2026, 7, 14, 6, 1),
            )
        )

    assert client.delete("/api/activities/777").status_code == 204
    assert client.get("/api/activities/777").status_code == 404

    with session_scope() as session:
        assert session.get(Activity, 777) is None
        assert session.get(Stream, 777) is None
        assert session.query(Lap).filter_by(activity_id=777).count() == 0
        assert session.query(BestEffort).filter_by(activity_id=777).count() == 0

    # deleting a missing activity is a clean 404
    assert client.delete("/api/activities/999").status_code == 404


def test_activity_detail_has_derived_fields(client):
    body = client.get("/api/activities/1").json()
    for key in ("gap_speed_mps", "decoupling_pct", "efficiency_index",
                "avg_power_w", "weather_temp_c", "weather_temp_min_c",
                "weather_temp_max_c", "weather_humidity_min_pct",
                "weather_humidity_max_pct"):
        assert key in body


def test_pace_twins_served_alongside_speed():
    # Every speed field gets a ready-made pace (s/km) so clients never re-derive
    # from m/s. 3.745 m/s -> 267.0 s/km -> 4:27 /km.
    from backend.schemas import ActivityDetail, LapOut, pace_s_per_km

    assert pace_s_per_km(3.745) == 267.0
    assert pace_s_per_km(None) is None
    assert pace_s_per_km(0.2) is None  # below walking: no meaningful pace

    lap = LapOut(
        lap_index=0, start_offset_s=0, elapsed_s=300, distance_m=1000,
        avg_hr=150, max_hr=160, avg_speed_mps=3.33, intensity="active",
    )
    assert lap.model_dump()["avg_pace_s_per_km"] == round(1000 / 3.33, 1)


def test_activity_detail_exposes_pace_twins(client):
    body = client.get("/api/activities/1").json()
    assert "avg_pace_s_per_km" in body
    assert "gap_pace_s_per_km" in body
    for lap in body["laps"]:
        assert "avg_pace_s_per_km" in lap


def test_weekly_zones(client):
    weeks = client.get("/api/trends/zones?weeks=8").json()
    assert len(weeks) == 8
    assert all(len(w["zone_seconds"]) == 5 for w in weeks)
    # the seeded 3-sample stream contributes a little Z-time somewhere
    assert client.get("/api/trends/zones?weeks=0").status_code == 422


def test_efficiency_trend(client):
    # seeded activity has no efficiency_index yet -> empty list, not an error
    assert client.get("/api/trends/efficiency?days=30").json() == []

    with session_scope() as session:
        activity = session.get(Activity, 1)
        activity.efficiency_index = 1.25
        activity.decoupling_pct = 3.2
    points = client.get("/api/trends/efficiency?days=30").json()
    assert len(points) == 1
    assert points[0]["efficiency_index"] == 1.25
    assert points[0]["decoupling_pct"] == 3.2


def test_fitness_projection_from_plan(client):
    from datetime import date, timedelta

    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    payload = {
        "replace_plan": True,
        "workouts": [
            {"day": tomorrow, "title": "Easy hour", "workout_type": "easy",
             "target_duration_s": 3600, "plan_name": "projection-test"},
        ],
    }
    assert client.post("/api/plan", json=payload).status_code == 200

    points = client.get("/api/trends/fitness?model=rtss&days=7&project_days=7").json()
    assert len(points) == 15  # 7 back + today + 7 forward
    future = [p for p in points if p["projected"]]
    assert len(future) == 7
    assert any(p["load"] > 0 for p in future)  # the planned workout carries load

    unprojected = client.get("/api/trends/fitness?model=rtss&days=7").json()
    assert all(not p["projected"] for p in unprojected)

    client.delete("/api/plan?plan_name=projection-test")


def test_races_crud_and_prediction(client):
    from datetime import date, datetime as dt, timedelta, timezone as tz

    race_day = (date.today() + timedelta(days=42)).isoformat()
    created = client.post(
        "/api/races",
        json={"name": "City 10K", "day": race_day, "distance_m": 10000,
              "target_time_s": 2400},
    ).json()
    assert created["id"] > 0
    assert created["days_until"] == 42
    assert created["predicted_time_s"] is None  # no recent best efforts yet

    with session_scope() as session:
        session.add(BestEffort(
            activity_id=1, label="5K", distance_m=5000, duration_s=1200,
            start_time_utc=dt.now(tz.utc).replace(tzinfo=None),
        ))
    listed = client.get("/api/races?upcoming=true").json()
    assert listed[0]["name"] == "City 10K"
    assert 2480 < listed[0]["predicted_time_s"] < 2510  # Riegel from the 20:00 5K

    updated = client.put(
        f"/api/races/{created['id']}",
        json={"name": "City 10K", "day": race_day, "distance_m": 10000,
              "target_time_s": 2350},
    ).json()
    assert updated["target_time_s"] == 2350

    assert client.post(
        "/api/races",
        json={"name": "Bad", "day": race_day, "distance_m": 10000, "priority": "X"},
    ).status_code == 422

    assert client.delete(f"/api/races/{created['id']}").json() == {"deleted": created["id"]}
    assert client.delete(f"/api/races/{created['id']}").status_code == 404


def test_wellness_and_readiness(client):
    from datetime import date, timedelta

    assert client.get("/api/wellness").json() == []
    assert client.get("/api/wellness/readiness").json() is None

    with session_scope() as session:
        today = date.today()
        for i in range(1, 11):  # baseline: HRV 60, RHR 50
            session.add(DailyWellness(
                day=today - timedelta(days=i), resting_hr=50,
                hrv_last_night_avg=60.0, sleep_score=80,
            ))
        session.add(DailyWellness(  # today: HRV crashed, RHR up, sleep poor
            day=today, resting_hr=58, hrv_last_night_avg=45.0, sleep_score=50,
        ))

    days = client.get("/api/wellness?days=30").json()
    assert len(days) == 11

    readiness = client.get("/api/wellness/readiness").json()
    assert readiness["status"] == "rest"
    assert set(readiness["flags"]) == {"hrv-low", "rhr-elevated", "sleep-poor"}
    assert readiness["hrv_baseline"] == 60.0
