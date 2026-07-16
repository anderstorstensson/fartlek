from backend.analysis.plan_projection import estimated_tss
from backend.models import AthleteSettings, PlannedWorkout


def _settings():
    return AthleteSettings(id=1, threshold_pace_s_per_km=270.0)


def test_duration_based_easy_workout():
    workout = PlannedWorkout(day=None, title="Easy hour", workout_type="easy",
                             target_duration_s=3600)
    # 1 h at IF 0.68 → 0.68² * 100 ≈ 46
    assert 44 < estimated_tss(workout, _settings()) < 48


def test_distance_based_workout_uses_type_speed():
    workout = PlannedWorkout(day=None, title="Easy 10K", workout_type="easy",
                             target_distance_m=10000)
    # threshold speed 3.7 m/s * 0.68 ≈ 2.52 m/s → ~66 min → ~51 TSS
    tss = estimated_tss(workout, _settings())
    assert 45 < tss < 58


def test_rest_day_is_zero():
    workout = PlannedWorkout(day=None, title="Rest", workout_type="rest",
                             target_duration_s=3600)
    assert estimated_tss(workout, _settings()) == 0.0


def test_no_targets_is_zero():
    workout = PlannedWorkout(day=None, title="Easy", workout_type="easy")
    assert estimated_tss(workout, _settings()) == 0.0
