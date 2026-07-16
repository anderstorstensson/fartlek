from backend.analysis.pace_zones import (
    pace_zones,
    pace_zones_from_paces,
    time_in_pace_zones,
)


def test_zones_from_threshold_pace():
    zones = pace_zones(270.0)  # 4:30/km → 3.704 m/s
    assert len(zones) == 5
    assert zones[0].low_speed_mps == round(3.7037 * 0.60, 3)
    assert zones[4].high_speed_mps is None
    # contiguous: each zone's high is the next zone's low
    for a, b in zip(zones, zones[1:]):
        assert a.high_speed_mps == b.low_speed_mps


def test_invalid_threshold_gives_no_zones():
    assert pace_zones(0) == []


def test_manual_zones_from_paces():
    # slowest→fastest bounds: 7:30, 5:40, 5:00, 4:38, 4:15 per km
    zones = pace_zones_from_paces([450, 340, 300, 278, 255])
    assert len(zones) == 5
    assert zones[0].low_speed_mps == round(1000 / 450, 3)
    assert zones[0].high_speed_mps == zones[1].low_speed_mps
    assert zones[4].high_speed_mps is None


def test_time_in_pace_zones_classifies_threshold_running():
    zones = pace_zones(270.0)
    threshold_speed = 1000.0 / 270.0
    n = 600
    time_s = [float(i) for i in range(n)]
    speeds = [threshold_speed] * n  # exactly threshold → Z4 (0.97–1.06)
    totals = time_in_pace_zones(time_s, speeds, zones)
    assert totals[3] == n - 1
    assert sum(totals) == n - 1


def test_walking_below_z1_floor_is_ignored():
    zones = pace_zones(270.0)
    time_s = [0.0, 1.0, 2.0]
    speeds = [1.0, 1.0, 1.0]  # ~16:40/km walk, below 60% of threshold speed
    assert sum(time_in_pace_zones(time_s, speeds, zones)) == 0
