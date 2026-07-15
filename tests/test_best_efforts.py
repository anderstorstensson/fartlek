from backend.analysis.best_efforts import best_efforts, _fastest_window


def _steady_run(speed_mps: float, duration_s: int):
    time_s = [float(t) for t in range(duration_s + 1)]
    dist = [speed_mps * t for t in time_s]
    return time_s, dist


def test_steady_run_efforts():
    # 5 km at exactly 3:20/km (5 m/s) -> 1K in 200 s, 5K in 1000 s.
    time_s, dist = _steady_run(5.0, 1000)
    efforts = {e.label: e.duration_s for e in best_efforts(time_s, dist)}
    assert abs(efforts["1K"] - 200.0) < 0.5
    assert abs(efforts["5K"] - 1000.0) < 0.5
    assert "10K" not in efforts  # run too short


def test_negative_split_finds_fast_segment():
    # 1 km slow (10 min) then 1 km fast (3 min): best 1K should be ~180 s.
    time_s = [float(t) for t in range(0, 781)]
    dist = []
    for t in time_s:
        if t <= 600:
            dist.append(t * (1000 / 600))
        else:
            dist.append(1000 + (t - 600) * (1000 / 180))
    efforts = {e.label: e.duration_s for e in best_efforts(time_s, dist)}
    assert abs(efforts["1K"] - 180.0) < 2.0


def test_short_or_empty_input():
    assert best_efforts([], []) == []
    assert best_efforts([0.0], [0.0]) == []
    assert best_efforts([0.0, 1.0], [0.0, 1.0]) == []  # only 1 m covered


def test_fastest_window_interpolates():
    # 2 samples spanning the target exactly halfway.
    time_s = [0.0, 100.0, 200.0]
    dist = [0.0, 500.0, 1000.0]
    assert abs(_fastest_window(time_s, dist, 750.0) - 150.0) < 1e-6
