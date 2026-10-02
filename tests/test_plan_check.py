"""scripts/plan-check re-derives every workout's distance from its description's
Total line — the deterministic guard against the drafting coach's mental
arithmetic (published targets have been up to 2.3 km off their own descriptions)."""

import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _run(payload) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(BASE_DIR / "scripts" / "plan-check")],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
    )


def _workout(**overrides) -> dict:
    workout = {
        "day": "2026-09-01",
        "title": "3x4K @ MP",
        "workout_type": "intervals",
        "target_distance_m": 19000,
        "description": (
            "[race-specific] 3K wu, 3x4K @ MP 3:52-3:55, 2x1K float @ 4:20, 2K cd. "
            "Total: 3 wu + 3×4 MP + 2×1 float + 2 cd = 19 km"
        ),
    }
    return {**workout, **overrides}


def test_consistent_plan_passes():
    result = _run({"workouts": [_workout()]})
    assert result.returncode == 0, result.stderr
    assert "1 running workout checked" in result.stdout


def test_accepts_bare_list_as_from_get_api_plan():
    result = _run([_workout()])
    assert result.returncode == 0, result.stderr


def test_target_description_mismatch_fails():
    # The original bug: float counted once, target published as 18K.
    result = _run({"workouts": [_workout(target_distance_m=18000)]})
    assert result.returncode == 1
    assert "18000" in result.stderr
    assert "19" in result.stderr
    assert "description wins" in result.stderr


def test_total_line_internal_arithmetic_error_fails():
    workout = _workout(
        description="[endurance] 3K wu, 3x4K, 2x1K float, 2K cd. "
        "Total: 3 wu + 3×4 MP + 2×1 float + 2 cd = 18 km",
        target_distance_m=18000,
    )
    result = _run({"workouts": [workout]})
    assert result.returncode == 1
    assert "sum to 19" in result.stderr


def test_missing_total_line_fails():
    workout = _workout(description="[endurance] Easy conversational running.")
    result = _run({"workouts": [workout]})
    assert result.returncode == 1
    assert "Total" in result.stderr


def test_missing_target_distance_fails():
    workout = _workout()
    del workout["target_distance_m"]
    result = _run({"workouts": [workout]})
    assert result.returncode == 1
    assert "target_distance_m" in result.stderr


def test_rest_and_cross_are_skipped():
    workouts = [
        {"day": "2026-09-02", "title": "Rest", "workout_type": "rest"},
        {
            "day": "2026-09-03",
            "title": "Strength",
            "workout_type": "cross",
            "target_duration_s": 3600,
            "description": "Squats 4x5",
        },
    ]
    result = _run({"workouts": workouts})
    assert result.returncode == 0
    assert "0 running workouts checked" in result.stdout


def test_race_without_total_line_passes():
    workout = _workout(
        workout_type="race",
        title="Goal 10K",
        target_distance_m=10000,
        description="[race-specific] Even splits at 3:58, contingency plan-B 4:05.",
    )
    result = _run({"workouts": [workout]})
    assert result.returncode == 0, result.stderr


def test_timed_recovery_converted_to_decimal_km():
    workout = _workout(
        title="6x800",
        target_distance_m=9700,
        description="[vo2max] 2K wu, 6x800 w/ 90s jog (~0.15K), 2K cd. "
        "Total: 2 wu + 6×0.8 + 5×0.18 + 2 cd = 9.7 km",
    )
    result = _run({"workouts": [workout]})
    assert result.returncode == 0, result.stderr


def test_unparseable_total_line_fails():
    workout = _workout(
        description="[endurance] stuff. Total: 3 wu + about four + 2 cd = 9 km"
    )
    result = _run({"workouts": [workout]})
    assert result.returncode == 1
    assert "unparseable" in result.stderr


def test_bad_json_is_usage_error():
    result = subprocess.run(
        [sys.executable, str(BASE_DIR / "scripts" / "plan-check")],
        input="not json",
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 2
