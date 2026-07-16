from backend.analysis.best_efforts import best_efforts
from backend.analysis.spikes import (
    max_plausible_speed,
    remove_gps_spikes,
    sustained_caps_for,
)

# threshold pace 224 s/km → threshold speed ≈ 4.46 m/s
CAPS = sustained_caps_for("running", 224.0)


def _streams(time_s, distance, speed):
    return {"time_s": time_s, "distance_m": distance, "speed_mps": speed}


def test_clean_stream_untouched():
    time_s = [float(i) for i in range(10)]
    distance = [i * 3.0 for i in range(10)]
    speed = [3.0] * 10
    streams = _streams(time_s, list(distance), list(speed))
    assert remove_gps_spikes(streams, 12.0) == 0
    assert streams["distance_m"] == [round(d, 2) for d in distance]
    assert streams["speed_mps"] == speed


def test_distance_jump_is_clamped():
    # 286 m "travelled" in 3 s mid-run (real spike shape from activity 20087123148)
    time_s = [0.0, 3.0, 6.0, 9.0, 12.0]
    distance = [0.0, 9.0, 295.0, 304.0, 313.0]
    streams = _streams(time_s, distance, [3.0] * 5)
    fixed = remove_gps_spikes(streams, 12.0)
    assert fixed == 1
    # jump capped at 12 m/s * 3 s = 36 m; subsequent deltas preserved
    assert streams["distance_m"] == [0.0, 9.0, 45.0, 54.0, 63.0]


def test_speed_spike_is_nulled():
    streams = _streams([0.0, 1.0, 2.0], [0.0, 3.0, 6.0], [3.0, 55.0, 3.0])
    assert remove_gps_spikes(streams, 12.0) == 1
    assert streams["speed_mps"] == [3.0, None, 3.0]


def test_negative_distance_delta_clamped_to_zero():
    streams = _streams([0.0, 1.0, 2.0], [0.0, 100.0, 6.0], [3.0, 3.0, 3.0])
    remove_gps_spikes(streams, 12.0)
    d = streams["distance_m"]
    assert d[0] <= d[1] <= d[2]  # cumulative distance stays monotonic


def test_spike_no_longer_fabricates_best_efforts():
    # steady 3 m/s run with one 400 m GPS jump — unfiltered this "runs" 400 m in 3 s
    time_s = [float(i * 3) for i in range(400)]
    distance = []
    d = 0.0
    for i in range(400):
        d += 9.0 if i != 200 else 409.0
        distance.append(d)
    streams = _streams(time_s, list(distance), [3.0] * 400)

    dirty = {e.label: e.duration_s for e in best_efforts(time_s, distance)}
    assert dirty["400m"] < 60  # the fabricated impossible effort

    remove_gps_spikes(streams, 12.0)
    clean = {e.label: e.duration_s for e in best_efforts(time_s, streams["distance_m"])}
    # 400 m at 3 m/s ≈ 133 s; the clamp leaves a small fast patch at the jump
    assert clean["400m"] >= 400 / 12.0
    assert clean["400m"] > 100


def test_sport_caps():
    assert max_plausible_speed("running") == 12.0
    assert max_plausible_speed("trail_running") == 12.0
    assert max_plausible_speed("cycling") == 30.0
    assert sustained_caps_for("cycling", 224.0) == []
    assert sustained_caps_for("running", None) == []


def test_sustained_drift_is_capped():
    """9 m/s for 90 s — every delta under the 12 m/s cap, but the buildup would
    fake a ~1:51 1K. The rolling rails must cut it."""
    time_s = [float(i) for i in range(300)]
    distance, speed = [], []
    d = 0.0
    for i in range(300):
        v = 9.0 if 100 <= i < 190 else 3.0
        d += v
        distance.append(d)
        speed.append(v)
    streams = _streams(time_s, distance, speed)
    fixed = remove_gps_spikes(streams, 12.0, CAPS)
    assert fixed > 0

    clean = {e.label: e.duration_s for e in best_efforts(time_s, streams["distance_m"])}
    # fastest 400 m must respect the 30s rail (1.5 × 4.46 ≈ 6.7 m/s)
    assert clean["400m"] >= 400 / 6.8
    # drifted speed samples nulled so GAP/decoupling don't ingest them
    assert all(v is None for v in streams["speed_mps"][135:190])


def test_real_interval_speeds_survive_the_rails():
    """10×3 min at 4.55 m/s (2% over threshold speed) with 1-min slow rests —
    a genuine hard session must pass untouched."""
    time_s, distance, speed = [], [], []
    t, d = 0.0, 0.0
    for _rep in range(10):
        for _ in range(180):
            t += 1; d += 4.55
            time_s.append(t); distance.append(d); speed.append(4.55)
        for _ in range(60):
            t += 1; d += 1.5
            time_s.append(t); distance.append(d); speed.append(1.5)
    streams = _streams(time_s, list(distance), list(speed))
    assert remove_gps_spikes(streams, 12.0, CAPS) == 0
    assert all(v is not None for v in streams["speed_mps"])
