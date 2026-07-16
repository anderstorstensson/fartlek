from backend.analysis.gap import average_moving_speed, gap_speed_series, grade_cost_factor


def test_flat_grade_costs_nothing_extra():
    assert grade_cost_factor(0.0) == 1.0


def test_uphill_costs_more_downhill_less():
    assert grade_cost_factor(0.10) > 1.3
    assert grade_cost_factor(-0.10) < 0.8


def test_extreme_grades_are_clamped():
    assert grade_cost_factor(2.0) == grade_cost_factor(0.30)
    assert grade_cost_factor(-2.0) == grade_cost_factor(-0.30)


def _steady_streams(n=60, speed=3.0, climb_per_s=0.0):
    time_s = [float(i) for i in range(n)]
    distance = [i * speed for i in range(n)]
    altitude = [100.0 + i * climb_per_s for i in range(n)]
    speeds = [speed] * n
    return time_s, distance, speeds, altitude


def test_flat_run_gap_equals_speed():
    time_s, dist, speeds, alt = _steady_streams()
    gap = gap_speed_series(time_s, dist, speeds, alt)
    assert all(abs(g - 3.0) < 1e-6 for g in gap)


def test_uphill_run_gap_exceeds_speed():
    # 3 m/s with 0.15 m/s climb = 5% grade
    time_s, dist, speeds, alt = _steady_streams(climb_per_s=0.15)
    gap = gap_speed_series(time_s, dist, speeds, alt)
    # skip edges where the smoothing window is one-sided
    assert all(g > 3.0 for g in gap[10:-10])


def test_missing_altitude_falls_back_to_raw_speed():
    time_s, dist, speeds, _ = _steady_streams()
    gap = gap_speed_series(time_s, dist, speeds, [None] * len(time_s))
    assert gap == speeds


def test_average_moving_speed_skips_pauses():
    time_s = [0.0, 1.0, 2.0, 100.0, 101.0]  # 98 s gap = auto-pause
    speeds = [3.0, 3.0, 3.0, 3.0, 3.0]
    assert average_moving_speed(time_s, speeds) == 3.0


def test_average_moving_speed_empty():
    assert average_moving_speed([], []) is None
