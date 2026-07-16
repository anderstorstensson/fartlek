from backend.analysis.workout_naming import workout_name


def _laps(*specs):
    return [
        {"intensity": intensity, "elapsed_s": elapsed, "distance_m": distance}
        for intensity, elapsed, distance in specs
    ]


def test_time_based_intervals():
    """Watch-controlled 3-min reps: exact durations, distances drift with pace."""
    laps = _laps(("warmup", 600, 2000))
    distances = [797, 820, 809, 817, 818, 847, 819, 818, 796, 806]
    for dist in distances:
        laps += _laps(("active", 180, dist), ("rest", 60, 80))
    laps += _laps(("cooldown", 300, 900))
    assert workout_name(laps) == "10×3 min / 1 min rest"


def test_distance_based_intervals():
    """Watch-controlled 800m reps: exact distances, durations drift with pace."""
    laps = _laps(("warmup", 600, 2000))
    for elapsed in (185, 182, 188, 184, 187, 190):
        laps += _laps(("active", elapsed, 800), ("rest", 90, 150))
    assert workout_name(laps) == "6×800 m / 1:30 rest"


def test_km_reps():
    laps = []
    for elapsed in (240, 244, 238, 246, 242):
        laps += _laps(("active", elapsed, 1002), ("rest", 120, 200))
    assert workout_name(laps) == "5×1 km / 2 min rest"


def test_pyramid_returns_none():
    laps = _laps(
        ("active", 60, 250), ("rest", 60, 80),
        ("active", 120, 500), ("rest", 60, 80),
        ("active", 240, 1000), ("rest", 60, 80),
    )
    assert workout_name(laps) is None


def test_no_structure_returns_none():
    assert workout_name(_laps(("active", 1800, 6000))) is None
    assert workout_name([]) is None


def test_continuous_reps_without_rest_laps():
    laps = _laps(("active", 600, 2410), ("active", 600, 2385), ("active", 600, 2402))
    assert workout_name(laps) == "3×10 min"
