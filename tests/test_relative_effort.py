import os
import tempfile
from datetime import datetime, timedelta

import pytest

from backend.analysis.relative_effort import effort_band, effort_percentile

os.environ["FARTLEK_SCHEDULER_ENABLED"] = "0"
os.environ.setdefault("FARTLEK_DATA_DIR", tempfile.mkdtemp(prefix="fartlek-test-"))

from fastapi.testclient import TestClient  # noqa: E402

from backend.db import session_scope  # noqa: E402
from backend.main import app  # noqa: E402
from backend.models import Activity  # noqa: E402


# --- pure functions ----------------------------------------------------------


def test_percentile_ranks_against_recent_loads():
    recent = [10.0, 20.0, 30.0, 40.0, 50.0]
    assert effort_percentile(60.0, recent) == 100.0
    assert effort_percentile(5.0, recent) == 0.0
    assert effort_percentile(35.0, recent) == 60.0


def test_percentile_uses_midrank_for_ties():
    recent = [10.0, 20.0, 20.0, 30.0, 40.0]
    assert effort_percentile(20.0, recent) == 40.0  # 1 below + half of 2 ties


def test_percentile_needs_minimum_history():
    assert effort_percentile(50.0, [10.0, 20.0]) is None


def test_bands():
    assert effort_band(None) is None
    assert effort_band(10.0) == "easy"
    assert effort_band(55.0) == "moderate"
    assert effort_band(80.0) == "tough"
    assert effort_band(97.0) == "massive"


# --- endpoint ----------------------------------------------------------------


BASE = datetime(2026, 6, 1, 8, 0)


def _activity(id: int, days_ago: int, trimp: float | None, **kwargs) -> Activity:
    start = BASE - timedelta(days=days_ago)
    defaults = dict(
        name=f"Session {id}",
        sport="running",
        start_time_utc=start,
        start_time_local=start,
        elapsed_s=3600,
        moving_s=3500,
        distance_m=10000,
        trimp=trimp,
    )
    defaults.update(kwargs)
    return Activity(id=id, **defaults)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        with session_scope() as session:
            # 10 prior sessions inside the 90-day window, loads 10..100
            for i in range(10):
                session.add(_activity(200 + i, days_ago=5 + i * 7, trimp=(i + 1) * 10.0))
            # a monster session outside the window — must not count
            session.add(_activity(220, days_ago=120, trimp=500.0))
            # the session under test: harder than all 10 in-window sessions
            session.add(_activity(221, days_ago=0, trimp=150.0))
            # a session with no HR/load
            session.add(_activity(222, days_ago=1, trimp=None))
        yield test_client


def test_relative_effort_percentile_and_band(client):
    body = client.get("/api/activities/221/relative-effort").json()
    assert body["load"] == 150.0
    assert body["percentile"] == 100.0
    assert body["band"] == "massive"
    assert body["window_sessions"] == 10  # the 120-days-ago session is excluded


def test_recent_strip_marks_current_session(client):
    body = client.get("/api/activities/221/relative-effort").json()
    days = [r["day"] for r in body["recent"]]
    assert days == sorted(days)  # oldest first
    current = [r for r in body["recent"] if r["current"]]
    assert len(current) == 1
    assert current[0]["activity_id"] == 221
    assert all(r["load"] is not None for r in body["recent"])


def test_activity_without_load(client):
    body = client.get("/api/activities/222/relative-effort").json()
    assert body["load"] is None
    assert body["percentile"] is None
    assert body["band"] is None


def test_relative_effort_unknown_activity_404s(client):
    assert client.get("/api/activities/99999/relative-effort").status_code == 404
