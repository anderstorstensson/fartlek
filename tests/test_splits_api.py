import os
import tempfile
from datetime import datetime

import pytest

os.environ["FARTLEK_SCHEDULER_ENABLED"] = "0"
os.environ.setdefault("FARTLEK_DATA_DIR", tempfile.mkdtemp(prefix="fartlek-test-"))

from fastapi.testclient import TestClient  # noqa: E402

from backend.db import session_scope  # noqa: E402
from backend.main import app  # noqa: E402
from backend.models import Activity, Lap, Stream  # noqa: E402


def _activity(id: int, **kwargs) -> Activity:
    defaults = dict(
        name=f"Run {id}",
        sport="running",
        start_time_utc=datetime(2026, 7, 1, 6, 0),
        start_time_local=datetime(2026, 7, 1, 8, 0),
        elapsed_s=1800,
        moving_s=1800,
        distance_m=5000,
    )
    defaults.update(kwargs)
    return Activity(id=id, **defaults)


def _steady_stream(activity_id: int, n: int = 1000, speed: float = 2.5) -> Stream:
    return Stream(
        activity_id=activity_id,
        time_s=[float(i) for i in range(n)],
        distance_m=[i * speed for i in range(n)],
        hr=[145.0] * n,
        speed_mps=[speed] * n,
        altitude_m=[30.0] * n,
        cadence=[170] * n,
        lat=[None] * n,
        lng=[None] * n,
    )


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        with session_scope() as session:
            # 101: structured workout with warmup/active/rest laps
            workout = _activity(101, name="6x800", is_workout=True)
            for i, (dist, elapsed, intensity) in enumerate(
                [(2000, 600, "warmup"), (800, 180, "active"), (100, 60, "rest"),
                 (800, 181, "active"), (1500, 500, "cooldown")]
            ):
                workout.laps.append(
                    Lap(
                        lap_index=i,
                        start_offset_s=sum(l.elapsed_s for l in workout.laps),
                        elapsed_s=elapsed,
                        distance_m=dist,
                        avg_speed_mps=dist / elapsed,
                        avg_hr=150.0,
                        intensity=intensity,
                    )
                )
            session.add(workout)

            # 102: easy run, single whole-activity lap, streams present
            easy = _activity(102, name="Easy")
            easy.laps.append(
                Lap(lap_index=0, start_offset_s=0, elapsed_s=999, distance_m=2497.5,
                    avg_speed_mps=2.5)
            )
            session.add(easy)
            session.add(_steady_stream(102))

            # 103: manual laps (not autolap pattern), tagged intervals => workout
            manual = _activity(103, name="Fartlek", tag="intervals")
            for i, (dist, elapsed) in enumerate([(3000, 900), (500, 100), (250, 180), (500, 99)]):
                manual.laps.append(
                    Lap(lap_index=i, start_offset_s=sum(l.elapsed_s for l in manual.laps),
                        elapsed_s=elapsed, distance_m=dist, avg_speed_mps=dist / elapsed)
                )
            session.add(manual)

            # 104: autolap pattern (1 km laps), no streams
            auto = _activity(104, name="Autolap")
            for i, dist in enumerate([1000.0, 1000.3, 999.7, 480.0]):
                auto.laps.append(
                    Lap(lap_index=i, start_offset_s=i * 300.0, elapsed_s=300.0,
                        distance_m=dist, avg_speed_mps=dist / 300.0)
                )
            session.add(auto)

            # 105: non-run
            session.add(_activity(105, name="Ride", sport="cycling"))

            # 106: manual laps on an untagged, non-workout run => plain lap splits
            manual2 = _activity(106, name="Progressive")
            for i, (dist, elapsed) in enumerate([(6896, 1851), (11427, 3163)]):
                manual2.laps.append(
                    Lap(lap_index=i, start_offset_s=sum(l.elapsed_s for l in manual2.laps),
                        elapsed_s=elapsed, distance_m=dist, avg_speed_mps=dist / elapsed)
                )
            session.add(manual2)
        yield test_client


def test_workout_mode_uses_laps_with_intensity(client):
    body = client.get("/api/activities/101/splits").json()
    assert body["mode"] == "workout"
    assert len(body["splits"]) == 5
    assert body["splits"][0]["intensity"] == "warmup"
    assert body["splits"][1]["avg_pace_s_per_km"] == 225.0  # 800 m in 180 s
    assert body["splits"][2]["intensity"] == "rest"


def test_easy_run_gets_km_splits_from_streams(client):
    body = client.get("/api/activities/102/splits").json()
    assert body["mode"] == "km"
    assert len(body["splits"]) == 3  # 2 full km + 497.5 m remainder
    assert body["splits"][0]["distance_m"] == 1000.0
    assert abs(body["splits"][0]["elapsed_s"] - 400.0) < 1.0
    assert body["splits"][0]["avg_hr"] == 145.0
    assert body["splits"][2]["distance_m"] < 1000.0


def test_mile_splits_on_request(client):
    # Activity 102 covers 2497.5 m at 2.5 m/s → 1 full mile + 888 m remainder.
    body = client.get("/api/activities/102/splits?unit=mile").json()
    assert body["mode"] == "km"  # mode means "distance splits", unit-agnostic
    assert len(body["splits"]) == 2
    assert abs(body["splits"][0]["distance_m"] - 1609.344) < 0.1  # stored rounded to 0.1 m
    assert abs(body["splits"][0]["elapsed_s"] - 1609.344 / 2.5) < 1.0
    assert body["splits"][1]["distance_m"] < 1609.344

    assert client.get("/api/activities/102/splits?unit=furlong").status_code == 422


def test_tagged_intervals_session_is_workout_mode(client):
    body = client.get("/api/activities/103/splits").json()
    assert body["mode"] == "workout"
    assert len(body["splits"]) == 4


def test_autolaps_without_streams_fall_back_to_km_mode(client):
    body = client.get("/api/activities/104/splits").json()
    assert body["mode"] == "km"
    assert len(body["splits"]) == 4


def test_non_run_has_no_splits(client):
    body = client.get("/api/activities/105/splits").json()
    assert body["mode"] == "none"
    assert body["splits"] == []


def test_manual_laps_on_plain_run_use_laps_mode(client):
    body = client.get("/api/activities/106/splits").json()
    assert body["mode"] == "laps"
    assert len(body["splits"]) == 2
    assert body["splits"][1]["distance_m"] == 11427.0


def test_unknown_activity_404s(client):
    assert client.get("/api/activities/99999/splits").status_code == 404
