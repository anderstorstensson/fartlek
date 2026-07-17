"""Self-evaluation (RPE/feel) and VO2 max ingestion from Garmin."""

from backend.sync.garmin import (
    feel_from_garmin,
    fetch_self_evaluation,
    fetch_vo2max_by_day,
    rpe_from_garmin,
)


class _StubClient:
    """Stands in for the garminconnect client in fetch tests."""

    garmin_connect_metrics_url = "/metrics-service/metrics/maxmet/daily"

    def __init__(self, detail=None, maxmet=None, raise_on_call=False):
        self._detail = detail
        self._maxmet = maxmet
        self._raise = raise_on_call

    def get_activity(self, activity_id):
        if self._raise:
            raise RuntimeError("boom")
        return self._detail

    def connectapi(self, url):
        if self._raise:
            raise RuntimeError("boom")
        return self._maxmet


def test_rpe_mapping():
    # Garmin stores the 1-10 rating × 10.
    assert rpe_from_garmin(10) == 1
    assert rpe_from_garmin(70) == 7
    assert rpe_from_garmin(100) == 10
    assert rpe_from_garmin(None) is None
    assert rpe_from_garmin(0) is None
    assert rpe_from_garmin(110) is None
    assert rpe_from_garmin("70") is None


def test_feel_mapping():
    # Five smileys at 0/25/50/75/100 → 1..5.
    assert feel_from_garmin(0) == 1
    assert feel_from_garmin(25) == 2
    assert feel_from_garmin(50) == 3
    assert feel_from_garmin(100) == 5
    assert feel_from_garmin(None) is None
    assert feel_from_garmin(-1) is None
    assert feel_from_garmin(101) is None


def test_fetch_self_evaluation_reads_summary_dto():
    client = _StubClient(
        detail={"summaryDTO": {"directWorkoutRpe": 70, "directWorkoutFeel": 50}}
    )
    assert fetch_self_evaluation(client, 1) == (7, 3)


def test_fetch_self_evaluation_handles_missing_and_errors():
    assert fetch_self_evaluation(_StubClient(detail={}), 1) == (None, None)
    assert fetch_self_evaluation(_StubClient(detail={"summaryDTO": {}}), 1) == (None, None)
    assert fetch_self_evaluation(_StubClient(raise_on_call=True), 1) == (None, None)


def test_fetch_vo2max_by_day_prefers_precise_value():
    client = _StubClient(
        maxmet=[
            {"generic": {"calendarDate": "2026-07-15", "vo2MaxPreciseValue": 65.4,
                         "vo2MaxValue": 65.0}},
            {"generic": {"calendarDate": "2026-07-16", "vo2MaxPreciseValue": None,
                         "vo2MaxValue": 65.0}},
            {"generic": None},
            {"generic": {"calendarDate": "2026-07-17"}},  # no value that day
        ]
    )
    assert fetch_vo2max_by_day(client, "2026-07-15", "2026-07-17") == {
        "2026-07-15": 65.4,
        "2026-07-16": 65.0,
    }


def test_fetch_vo2max_by_day_swallows_errors():
    assert fetch_vo2max_by_day(_StubClient(raise_on_call=True), "a", "b") == {}
