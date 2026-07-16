"""Turn a Garmin activity (summary JSON + optional FIT file) into DB rows."""

import io
import logging
from datetime import datetime, timezone

import fitdecode
from sqlalchemy.orm import Session

from backend.analysis.best_efforts import best_efforts
from backend.analysis.decoupling import aerobic_decoupling_pct, efficiency_index
from backend.analysis.gap import average_moving_speed, gap_speed_series
from backend.analysis.metrics import (
    banister_trimp,
    hrtss,
    rtss,
    rtss_from_speed,
    trimp_from_samples,
)
from backend.analysis.spikes import (
    max_plausible_speed,
    remove_gps_spikes,
    sustained_caps_for,
)
from backend.analysis.workout_naming import workout_name
from backend.config import config
from backend.models import Activity, AthleteSettings, BestEffort, Lap, Stream

logger = logging.getLogger(__name__)

_SEMICIRCLE_TO_DEG = 180.0 / 2**31


def _parse_garmin_dt(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def activity_from_summary(summary: dict) -> Activity:
    activity_type = (summary.get("activityType") or {}).get("typeKey", "other")
    return Activity(
        id=summary["activityId"],
        name=summary.get("activityName") or activity_type.replace("_", " ").title(),
        sport=activity_type,
        start_time_utc=_parse_garmin_dt(summary["startTimeGMT"]),
        start_time_local=_parse_garmin_dt(summary["startTimeLocal"]),
        elapsed_s=summary.get("duration") or 0.0,
        moving_s=summary.get("movingDuration") or summary.get("duration") or 0.0,
        distance_m=summary.get("distance") or 0.0,
        avg_hr=summary.get("averageHR"),
        max_hr=summary.get("maxHR"),
        avg_speed_mps=summary.get("averageSpeed"),
        max_speed_mps=summary.get("maxSpeed"),
        ascent_m=summary.get("elevationGain"),
        descent_m=summary.get("elevationLoss"),
        calories=summary.get("calories"),
        avg_cadence=summary.get("averageRunningCadenceInStepsPerMinute")
        or summary.get("averageBikingCadenceInRevPerMinute"),
        has_gps=summary.get("hasPolyline", False),
    )


def parse_fit(fit_bytes: bytes) -> tuple[dict[str, list], list[dict], bool]:
    """Extract record streams, laps and a structured-workout flag from a FIT file."""
    streams: dict[str, list] = {
        k: []
        for k in (
            "time_s", "distance_m", "hr", "speed_mps", "altitude_m", "cadence",
            "lat", "lng", "power", "vertical_oscillation", "vertical_ratio",
            "step_length", "stance_time", "respiration",
        )
    }
    laps: list[dict] = []
    first_ts: datetime | None = None
    workout_steps = 0
    has_rest_lap = False

    with fitdecode.FitReader(io.BytesIO(fit_bytes)) as reader:
        for frame in reader:
            if not isinstance(frame, fitdecode.FitDataMessage):
                continue
            if frame.name == "record":
                ts = _field(frame, "timestamp")
                if ts is None:
                    continue
                if first_ts is None:
                    first_ts = ts
                lat_raw = _field(frame, "position_lat")
                lng_raw = _field(frame, "position_long")
                streams["time_s"].append(round((ts - first_ts).total_seconds(), 1))
                streams["distance_m"].append(_field(frame, "distance"))
                streams["hr"].append(_field(frame, "heart_rate"))
                streams["speed_mps"].append(
                    _field(frame, "enhanced_speed") or _field(frame, "speed")
                )
                streams["altitude_m"].append(
                    _field(frame, "enhanced_altitude") or _field(frame, "altitude")
                )
                streams["cadence"].append(_field(frame, "cadence"))
                streams["lat"].append(
                    round(lat_raw * _SEMICIRCLE_TO_DEG, 6) if lat_raw is not None else None
                )
                streams["lng"].append(
                    round(lng_raw * _SEMICIRCLE_TO_DEG, 6) if lng_raw is not None else None
                )
                streams["power"].append(_field(frame, "power"))
                streams["vertical_oscillation"].append(_field(frame, "vertical_oscillation"))
                streams["vertical_ratio"].append(_field(frame, "vertical_ratio"))
                streams["step_length"].append(_field(frame, "step_length"))
                streams["stance_time"].append(_field(frame, "stance_time"))
                streams["respiration"].append(
                    _field(frame, "enhanced_respiration_rate")
                    or _field(frame, "respiration_rate")
                )
            elif frame.name == "lap":
                lap_start = _field(frame, "start_time")
                intensity = _field(frame, "intensity")
                if intensity == "rest":
                    has_rest_lap = True
                laps.append(
                    {
                        "start_time": lap_start,
                        "elapsed_s": _field(frame, "total_timer_time")
                        or _field(frame, "total_elapsed_time")
                        or 0.0,
                        "distance_m": _field(frame, "total_distance") or 0.0,
                        "avg_hr": _field(frame, "avg_heart_rate"),
                        "max_hr": _field(frame, "max_heart_rate"),
                        "avg_speed_mps": _field(frame, "enhanced_avg_speed")
                        or _field(frame, "avg_speed"),
                        "intensity": intensity if isinstance(intensity, str) else None,
                    }
                )
            elif frame.name == "workout_step":
                workout_steps += 1
    is_workout = workout_steps >= 2 or has_rest_lap
    return streams, laps, is_workout


def _field(frame: "fitdecode.FitDataMessage", name: str):
    try:
        value = frame.get_value(name, fallback=None)
    except Exception:
        return None
    return value


def _downsample(streams: dict[str, list], max_points: int) -> dict[str, list]:
    n = len(streams["time_s"])
    if n <= max_points:
        return streams
    stride = -(-n // max_points)  # ceil division
    indices = list(range(0, n, stride))
    if indices[-1] != n - 1:
        indices.append(n - 1)
    return {key: [values[i] for i in indices] for key, values in streams.items()}


def import_activity(
    session: Session,
    summary: dict,
    fit_bytes: bytes | None,
    settings: AthleteSettings,
) -> Activity:
    """Create/replace one activity with streams, laps, metrics and best efforts."""
    existing = session.get(Activity, summary["activityId"])
    if existing is not None:
        session.delete(existing)
        session.flush()

    activity = activity_from_summary(summary)

    full_streams: dict[str, list] | None = None
    if fit_bytes:
        try:
            full_streams, fit_laps, is_workout = parse_fit(fit_bytes)
            activity.has_fit = True
            activity.is_workout = is_workout
        except Exception as exc:
            logger.warning("FIT parse failed for %s: %s", activity.id, exc)
            full_streams, fit_laps = None, []
    else:
        fit_laps = []

    if full_streams and len(full_streams["time_s"]) >= 2:
        _filter_spikes(activity, full_streams, settings)
        activity.has_gps = any(v is not None for v in full_streams["lat"])
        _attach_laps(activity, fit_laps)
        _attach_best_efforts(activity, full_streams)
        _compute_derived(activity, full_streams)
        _apply_workout_name(activity, fit_laps)
        stored = _downsample(full_streams, config.stream_max_points)
        activity.stream = Stream(**stored)

    _compute_loads(activity, full_streams, settings)
    session.add(activity)
    return activity


def _avg(values: list | None) -> float | None:
    if not values:
        return None
    present = [v for v in values if v is not None]
    if not present:
        return None
    return sum(present) / len(present)


def _compute_derived(activity: Activity, streams: dict[str, list]) -> None:
    """Dynamics averages plus GAP / decoupling / efficiency from full streams."""
    activity.avg_power_w = _round1(_avg(streams.get("power")))
    activity.avg_vertical_oscillation_mm = _round1(_avg(streams.get("vertical_oscillation")))
    activity.avg_vertical_ratio_pct = _round1(_avg(streams.get("vertical_ratio")))
    activity.avg_step_length_mm = _round1(_avg(streams.get("step_length")))
    activity.avg_stance_time_ms = _round1(_avg(streams.get("stance_time")))
    activity.avg_respiration_brpm = _round1(_avg(streams.get("respiration")))

    if not activity.is_run:
        return
    gap_speeds = gap_speed_series(
        streams["time_s"], streams["distance_m"], streams["speed_mps"], streams["altitude_m"]
    )
    avg_gap = average_moving_speed(streams["time_s"], gap_speeds)
    activity.gap_speed_mps = round(avg_gap, 3) if avg_gap is not None else None
    decoupling = aerobic_decoupling_pct(streams["time_s"], gap_speeds, streams["hr"])
    activity.decoupling_pct = _round1(decoupling)

    hr_values = [h for h in streams["hr"] if h is not None]
    avg_stream_hr = sum(hr_values) / len(hr_values) if hr_values else activity.avg_hr
    efficiency = efficiency_index(avg_gap, avg_stream_hr)
    activity.efficiency_index = round(efficiency, 3) if efficiency is not None else None


def _round1(value: float | None) -> float | None:
    return round(value, 1) if value is not None else None


def _filter_spikes(
    activity: Activity, streams: dict[str, list], settings: AthleteSettings
) -> None:
    fixed = remove_gps_spikes(
        streams,
        max_plausible_speed(activity.sport),
        sustained_caps_for(activity.sport, settings.threshold_pace_s_per_km),
    )
    if fixed:
        logger.warning("GPS spike filter: corrected %d samples in activity %s", fixed, activity.id)


def _apply_workout_name(activity: Activity, fit_laps: list[dict]) -> None:
    """Interval runs get named after their structure ("10×3 min / 1 min rest");
    everything else keeps its Garmin name. User-edited titles are never touched."""
    if activity.name_locked or not (activity.is_run and activity.is_workout):
        return
    derived = workout_name(fit_laps)
    if derived:
        activity.name = derived


def refresh_from_fit(activity: Activity, fit_bytes: bytes, settings: AthleteSettings) -> bool:
    """Re-extract streams, workout flags, derived metrics and loads from a stored
    FIT file, in place. Summary fields, laps (except intensity) and best efforts
    are left untouched. Returns False if the file can't be parsed."""
    try:
        streams, fit_laps, is_workout = parse_fit(fit_bytes)
    except Exception as exc:
        logger.warning("FIT re-parse failed for %s: %s", activity.id, exc)
        return False
    if len(streams["time_s"]) < 2:
        return False

    _filter_spikes(activity, streams, settings)
    activity.has_fit = True
    activity.is_workout = is_workout
    intensities = [lap.get("intensity") for lap in fit_laps]
    for lap in activity.laps:
        if lap.lap_index < len(intensities):
            lap.intensity = intensities[lap.lap_index]

    _apply_workout_name(activity, fit_laps)
    # Best efforts were computed from the (possibly spike-polluted) original
    # streams — rebuild them from the filtered ones.
    activity.best_efforts.clear()
    _attach_best_efforts(activity, streams)
    _compute_derived(activity, streams)
    stored = _downsample(streams, config.stream_max_points)
    if activity.stream is not None:
        for key, values in stored.items():
            setattr(activity.stream, key, values)
    else:
        activity.stream = Stream(**stored)
    _compute_loads(activity, streams, settings)
    return True


def compute_loads_for(activity: Activity, settings: AthleteSettings) -> None:
    """Recompute load metrics using the stored (downsampled) stream."""
    streams = None
    if activity.stream is not None:
        streams = {"time_s": activity.stream.time_s, "hr": activity.stream.hr}
    _compute_loads(activity, streams, settings)


def _compute_loads(
    activity: Activity, streams: dict[str, list] | None, settings: AthleteSettings
) -> None:
    if streams and any(h is not None for h in streams.get("hr", [])):
        activity.trimp = round(
            trimp_from_samples(
                streams["time_s"], streams["hr"], settings.resting_hr, settings.max_hr, settings.sex
            ),
            1,
        )
    elif activity.avg_hr:
        activity.trimp = round(
            banister_trimp(
                activity.moving_s / 60.0,
                activity.avg_hr,
                settings.resting_hr,
                settings.max_hr,
                settings.sex,
            ),
            1,
        )
    else:
        activity.trimp = None

    if activity.is_run and activity.gap_speed_mps and settings.rtss_use_gap:
        # Grade-adjusted speed as the NGP approximation, so hills price correctly.
        activity.rtss = round(
            rtss_from_speed(
                activity.moving_s, activity.gap_speed_mps, settings.threshold_pace_s_per_km
            ),
            1,
        )
    elif activity.is_run and activity.distance_m > 0:
        activity.rtss = round(
            rtss(activity.moving_s, activity.distance_m, settings.threshold_pace_s_per_km), 1
        )
    else:
        activity.rtss = None

    activity.hrtss = (
        round(hrtss(activity.moving_s, activity.avg_hr, settings.lthr), 1)
        if activity.avg_hr
        else None
    )


def _attach_laps(activity: Activity, fit_laps: list[dict]) -> None:
    start = activity.start_time_utc.replace(tzinfo=timezone.utc)
    for i, lap in enumerate(fit_laps):
        lap_start = lap["start_time"]
        offset = 0.0
        if lap_start is not None:
            if lap_start.tzinfo is None:
                lap_start = lap_start.replace(tzinfo=timezone.utc)
            offset = max((lap_start - start).total_seconds(), 0.0)
        activity.laps.append(
            Lap(
                lap_index=i,
                start_offset_s=offset,
                elapsed_s=lap["elapsed_s"],
                distance_m=lap["distance_m"],
                avg_hr=lap["avg_hr"],
                max_hr=lap["max_hr"],
                avg_speed_mps=lap["avg_speed_mps"],
                intensity=lap.get("intensity"),
            )
        )


def _attach_best_efforts(activity: Activity, streams: dict[str, list]) -> None:
    if not activity.is_run:
        return
    time_s = [t for t, d in zip(streams["time_s"], streams["distance_m"]) if d is not None]
    dist = [d for d in streams["distance_m"] if d is not None]
    for effort in best_efforts(time_s, dist):
        activity.best_efforts.append(
            BestEffort(
                label=effort.label,
                distance_m=effort.distance_m,
                duration_s=round(effort.duration_s, 1),
                start_time_utc=activity.start_time_utc,
            )
        )
