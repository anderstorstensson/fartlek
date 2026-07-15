import os
import tempfile
from datetime import datetime

import pytest

os.environ["FARTLEK_SCHEDULER_ENABLED"] = "0"
os.environ["FARTLEK_DATA_DIR"] = tempfile.mkdtemp(prefix="fartlek-test-")

from fastapi.testclient import TestClient  # noqa: E402

from backend.db import session_scope  # noqa: E402
from backend.main import app  # noqa: E402
from backend.models import Activity, Stream  # noqa: E402


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
    assert client.put("/api/settings", json={**base, "zone_mode": "manual"}).status_code == 422

    # Restore default mode for other tests.
    client.put("/api/settings", json={**base, "zone_mode": "max_hr"})


def test_settings_validation(client):
    bad = {"resting_hr": 5, "max_hr": 188, "lthr": 168,
           "threshold_pace_s_per_km": 255, "sex": "male"}
    assert client.put("/api/settings", json=bad).status_code == 422


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

    for note_id in (created["id"], weekly["id"]):
        assert client.delete(f"/api/notes/{note_id}").json() == {"deleted": note_id}
    assert client.delete("/api/notes/99999").status_code == 404


def test_sync_status(client):
    body = client.get("/api/sync/status").json()
    assert body["total_activities"] == 1
    assert body["logged_in"] in (True, False)
