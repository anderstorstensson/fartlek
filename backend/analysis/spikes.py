"""GPS spike filtering.

Bad GPS shows up two ways: single-fix jumps in the cumulative distance stream
(hundreds of meters in a few seconds) and sustained drift where each sample
looks individually possible but a minute of them adds up to an unbelievable
pace and a fabricated record. Both are filtered at ingest:

- per-sample: distance deltas capped at an absolute max speed, absurd speed
  samples nulled;
- rolling windows: for runs, distance gained over any trailing window is
  capped relative to the athlete's threshold speed — no runner sustains
  1.5× threshold speed for 30 s or 1.3× for 2 min (VO2max pace ≈ 1.1–1.15×,
  an all-out 400 m ≈ 1.4×), so drift that builds past these rails is cut
  while real sprints and reps pass.

Everything downstream (best efforts, GAP, decoupling, charts) then works
from sane data.
"""

# Faster than any human sprint (WR ~10.4 m/s average) — above this is GPS error.
_MAX_RUN_SPEED_MPS = 12.0
# Generous cap for cycling/skiing descents.
_MAX_OTHER_SPEED_MPS = 30.0

# (window seconds, multiple of threshold speed) — sustained-speed rails for runs.
SUSTAINED_CAPS = [(30.0, 1.5), (120.0, 1.3)]


def max_plausible_speed(sport: str) -> float:
    if "running" in (sport or "") or "walking" in (sport or "") or "hiking" in (sport or ""):
        return _MAX_RUN_SPEED_MPS
    return _MAX_OTHER_SPEED_MPS


def sustained_caps_for(sport: str, threshold_pace_s_per_km: float | None) -> list[tuple[float, float]]:
    """Rolling-window speed caps (window_s, cap_mps); empty for non-running sports."""
    if "running" not in (sport or "") or not threshold_pace_s_per_km:
        return []
    threshold_speed = 1000.0 / threshold_pace_s_per_km
    return [(window, factor * threshold_speed) for window, factor in SUSTAINED_CAPS]


def remove_gps_spikes(
    streams: dict[str, list],
    max_speed_mps: float,
    sustained_caps: list[tuple[float, float]] | None = None,
) -> int:
    """Clamp cumulative-distance jumps and drift, and null speed spikes, in place.

    Returns the number of corrected samples (0 = stream was clean).
    """
    time_s = streams.get("time_s") or []
    distance = streams.get("distance_m") or []
    speed = streams.get("speed_mps") or []
    caps = sustained_caps or []
    fixed = 0

    fixed += _null_speed_spikes(time_s, speed, max_speed_mps, caps)

    # Rebuild the cumulative distance: each delta capped at max_speed * dt, and
    # distance gained over any trailing window capped at that window's rail.
    # Excess meters from bad fixes are dropped instead of shifting every
    # subsequent sample.
    corrected: list[tuple[float, float]] = []  # (time, corrected distance), valid samples
    window_starts = [0] * len(caps)
    prev_raw: float | None = None
    for i in range(min(len(distance), len(time_s))):
        raw = distance[i]
        if raw is None:
            continue
        if not corrected:
            value = raw
        else:
            prev_time, prev_value = corrected[-1]
            dt = max(time_s[i] - prev_time, 0.0)
            delta = min(max(raw - prev_raw, 0.0), max_speed_mps * dt)
            value = prev_value + delta
            for cap_idx, (window, cap_speed) in enumerate(caps):
                start = window_starts[cap_idx]
                while start < len(corrected) - 1 and time_s[i] - corrected[start + 1][0] >= window:
                    start += 1
                window_starts[cap_idx] = start
                anchor_time, anchor_value = corrected[start]
                if time_s[i] - anchor_time >= window:
                    value = min(value, anchor_value + cap_speed * (time_s[i] - anchor_time))
            if abs(value - (prev_value + (raw - prev_raw))) > 1e-9:
                fixed += 1
        prev_raw = raw
        corrected.append((time_s[i], value))
        distance[i] = round(value, 2)
    return fixed


def _null_speed_spikes(
    time_s: list[float],
    speed: list,
    max_speed_mps: float,
    caps: list[tuple[float, float]],
) -> int:
    """Null instantaneous spikes plus samples whose trailing window sustains
    a speed above the rail. The mask is computed from a snapshot so nulling
    doesn't disturb the rolling sums."""
    fixed = 0
    for i, value in enumerate(speed):
        if value is not None and value > max_speed_mps:
            speed[i] = None
            fixed += 1

    n = min(len(speed), len(time_s))
    segments = []  # (index, end_time, dt, speed) for valid samples
    for i in range(1, n):
        value = speed[i]
        dt = time_s[i] - time_s[i - 1]
        if value is None or dt <= 0 or dt > 30:
            continue
        segments.append((i, time_s[i], dt, value))

    to_null: set[int] = set()
    for window, cap_speed in caps:
        start = 0
        moved = 0.0  # meters over the trailing window
        elapsed = 0.0
        for k, (i, end_time, dt, value) in enumerate(segments):
            moved += value * dt
            elapsed += dt
            while segments[start][1] < end_time - window:
                moved -= segments[start][3] * segments[start][2]
                elapsed -= segments[start][2]
                start += 1
            if elapsed >= window * 0.8 and moved / elapsed > cap_speed:
                to_null.add(i)
    for i in to_null:
        if speed[i] is not None:
            speed[i] = None
            fixed += 1
    return fixed
