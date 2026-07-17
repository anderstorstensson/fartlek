from backend.analysis.splits import elevation_gain, is_autolap, km_splits


def _streams(n=700, speed=3.0, dt=1.0):
    """Steady run: `n` samples at `speed` m/s, one per `dt` seconds."""
    time_s = [i * dt for i in range(n)]
    distance = [i * dt * speed for i in range(n)]
    return time_s, distance


# --- km_splits ---------------------------------------------------------------


def test_steady_run_produces_even_km_splits():
    time_s, dist = _streams(n=1000, speed=2.5)  # 2 497.5 m over 999 s
    splits = km_splits(time_s, dist, altitude_m=None, hr=None)
    assert len(splits) == 3
    full = splits[:2]
    for s in full:
        assert abs(s.distance_m - 1000.0) < 1e-6
        assert abs(s.elapsed_s - 400.0) < 0.5  # 1000 m at 2.5 m/s
        assert abs(s.avg_speed_mps - 2.5) < 0.01
    assert splits[2].distance_m < 1000.0


def test_boundary_time_is_interpolated_between_samples():
    # 5 m/s with samples every 3 s: km boundary falls between samples.
    time_s = [i * 3.0 for i in range(150)]
    dist = [t * 5.0 for t in time_s]
    splits = km_splits(time_s, dist, altitude_m=None, hr=None)
    assert abs(splits[0].elapsed_s - 200.0) < 0.01


def test_short_trailing_remainder_is_dropped():
    time_s, dist = _streams(n=361, speed=3.0)  # 1 080 m: remainder 80 m < 200 m
    splits = km_splits(time_s, dist, altitude_m=None, hr=None)
    assert len(splits) == 1


def test_pause_gaps_are_excluded_from_split_time():
    # 1 000 m at 2.5 m/s with a ~320 s standing pause (a single long sample gap).
    time_s = [float(i) for i in range(200)] + [float(i + 320) for i in range(200, 401)]
    dist = [i * 2.5 for i in range(200)] + [i * 2.5 for i in range(200, 401)]
    splits = km_splits(time_s, dist, altitude_m=None, hr=None)
    assert abs(splits[0].elapsed_s - 400.0) <= 2.0
    assert abs(splits[0].avg_speed_mps - 2.5) < 0.05


def test_split_avg_hr_is_computed_per_split():
    time_s, dist = _streams(n=801, speed=2.5)  # 2 000 m
    hr = [140.0] * 400 + [160.0] * 401
    splits = km_splits(time_s, dist, altitude_m=None, hr=hr)
    assert abs(splits[0].avg_hr - 140.0) < 1.0
    assert abs(splits[1].avg_hr - 160.0) < 1.0


def test_split_elevation_gain_only_counts_real_climbs():
    time_s, dist = _streams(n=801, speed=2.5)
    # First km flat with ±0.5 m noise; second km climbs 20 m.
    alt = [100.0 + (0.5 if i % 2 else -0.5) for i in range(400)]
    alt += [100.0 + (i - 400) * 0.05 for i in range(400, 801)]
    splits = km_splits(time_s, dist, altitude_m=alt, hr=None)
    assert splits[0].elevation_gain_m < 3.0
    assert 15.0 < splits[1].elevation_gain_m < 25.0


def test_none_and_missing_streams_are_tolerated():
    assert km_splits([], [], altitude_m=None, hr=None) == []
    time_s, dist = _streams(n=500)
    dist = list(dist)
    dist[100] = None  # dropout mid-stream
    splits = km_splits(time_s, dist, altitude_m=None, hr=None)
    assert len(splits) >= 1


# --- elevation_gain ----------------------------------------------------------


def test_elevation_gain_ignores_altimeter_noise():
    time_s = [float(i) for i in range(600)]
    alt = [50.0 + (0.6 if i % 2 else -0.6) for i in range(600)]
    assert elevation_gain(time_s, alt) < 2.0


def test_elevation_gain_counts_steady_climb():
    time_s = [float(i) for i in range(600)]
    alt = [50.0 + i * 0.05 for i in range(600)]  # +30 m
    gain = elevation_gain(time_s, alt)
    assert 25.0 < gain < 32.0


def test_elevation_gain_handles_missing_altitude():
    assert elevation_gain([0.0, 1.0], [None, None]) is None
    assert elevation_gain([], []) is None


# --- is_autolap --------------------------------------------------------------


def test_km_autolaps_detected():
    assert is_autolap([1000.0, 1000.2, 999.8, 1000.1, 614.0]) is True


def test_mile_autolaps_detected():
    assert is_autolap([1609.3, 1609.4, 1609.2, 800.0]) is True


def test_manual_interval_laps_are_not_autolap():
    assert is_autolap([3969.0, 502.0, 236.0, 500.0, 241.0, 1860.0]) is False


def test_single_lap_is_not_autolap():
    assert is_autolap([8042.0]) is False
    assert is_autolap([]) is False


def test_two_long_manual_laps_are_not_autolap():
    assert is_autolap([6896.0, 11427.0]) is False
