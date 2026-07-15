import math

from backend.analysis.metrics import (
    banister_trimp,
    hr_reserve_fraction,
    hrtss,
    rtss,
    trimp_from_samples,
)


def test_hr_reserve_fraction_clamps():
    assert hr_reserve_fraction(150, 50, 190) == (150 - 50) / 140
    assert hr_reserve_fraction(40, 50, 190) == 0.0
    assert hr_reserve_fraction(250, 50, 190) == 1.0
    assert hr_reserve_fraction(150, 190, 190) == 0.0  # degenerate settings


def test_banister_trimp_known_value():
    # 60 min at HRr = 0.5: 60 * 0.5 * 0.64 * e^(1.92*0.5)
    expected = 60 * 0.5 * 0.64 * math.exp(0.96)
    assert banister_trimp(60, 120, 50, 190, "male") == expected


def test_banister_trimp_zero_cases():
    assert banister_trimp(0, 150, 50, 190) == 0.0
    assert banister_trimp(60, 0, 50, 190) == 0.0


def test_trimp_from_samples_matches_constant_hr():
    # Constant HR sampled every second should approximate the session formula.
    time_s = list(range(0, 3600))
    hr = [120.0] * 3600
    sampled = trimp_from_samples(time_s, hr, 50, 190)
    session = banister_trimp(3600 / 60, 120, 50, 190)
    assert abs(sampled - session) / session < 0.01


def test_trimp_from_samples_skips_gaps():
    # A 10-minute pause between two samples must not add load.
    time_s = [0, 1, 2, 602, 603]
    hr = [150.0] * 5
    with_gap = trimp_from_samples(time_s, hr, 50, 190)
    without_gap = trimp_from_samples([0, 1, 2, 3, 4], hr, 50, 190)
    assert with_gap < without_gap


def test_rtss_one_hour_at_threshold_is_100():
    # Threshold pace 4:30/km -> 13.333 km covered in one hour at threshold.
    assert abs(rtss(3600, 13333.33, 270) - 100.0) < 0.1


def test_rtss_scales_with_intensity_squared():
    easy = rtss(3600, 10000, 270)  # slower than threshold
    hard = rtss(3600, 13333.33, 270)
    assert easy < hard


def test_hrtss_one_hour_at_lthr_is_100():
    assert hrtss(3600, 170, 170) == 100.0


def test_hrtss_caps_intensity():
    assert hrtss(3600, 250, 170) == (1.15**2) * 100
