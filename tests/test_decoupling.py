from backend.analysis.decoupling import aerobic_decoupling_pct, efficiency_index


def _run(n_s: int, speed: float, hr_first: float, hr_second: float):
    time_s = [float(i) for i in range(n_s)]
    speeds = [speed] * n_s
    hr = [hr_first if i < n_s / 2 else hr_second for i in range(n_s)]
    return time_s, speeds, hr


def test_no_drift_is_zero():
    time_s, speeds, hr = _run(2400, 3.0, 150, 150)
    assert abs(aerobic_decoupling_pct(time_s, speeds, hr)) < 0.5


def test_hr_drift_is_positive():
    time_s, speeds, hr = _run(2400, 3.0, 150, 160)
    drift = aerobic_decoupling_pct(time_s, speeds, hr)
    assert 5.0 < drift < 8.0  # 160/150 - 1 = 6.7%


def test_too_short_returns_none():
    time_s, speeds, hr = _run(600, 3.0, 150, 160)  # 10 min < 2x10 min minimum
    assert aerobic_decoupling_pct(time_s, speeds, hr) is None


def test_missing_hr_returns_none():
    time_s = [float(i) for i in range(2400)]
    assert aerobic_decoupling_pct(time_s, [3.0] * 2400, [None] * 2400) is None


def test_efficiency_index():
    # 3 m/s at 150 bpm = 180 m/min / 150 = 1.2
    assert abs(efficiency_index(3.0, 150.0) - 1.2) < 1e-9
    assert efficiency_index(None, 150.0) is None
    assert efficiency_index(3.0, 0) is None
