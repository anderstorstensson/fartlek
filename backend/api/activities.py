from datetime import date, datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from backend.analysis.gap import gap_speed_series
from backend.analysis.pace_zones import pace_zones_for_settings, time_in_pace_zones
from backend.analysis.relative_effort import WINDOW_DAYS, effort_band, effort_percentile
from backend.analysis.splits import (
    is_autolap,
    km_splits,
    window_elevation_gains,
    window_gap_means,
)
from backend.analysis.zones import time_in_zones, zones_for_settings
from backend.db import get_session
from backend.models import Activity, AnalysisNote, Lap, Stream
from backend.schemas import (
    ActivityDetail,
    ActivityList,
    ActivitySummary,
    ActivityUpdate,
    PaceZoneOut,
    RecentEffort,
    RelativeEffortOut,
    SplitOut,
    SplitsOut,
    StreamsOut,
    ZoneOut,
)
from backend.sync.service import get_or_create_settings

router = APIRouter(prefix="/api/activities", tags=["activities"])


@router.get("", response_model=ActivityList)
def list_activities(
    limit: int = 50,
    offset: int = 0,
    sport: str | None = None,
    q: str | None = None,
    start: date | None = None,
    end: date | None = None,
    session: Session = Depends(get_session),
) -> ActivityList:
    query = select(Activity)
    if start:
        query = query.where(Activity.start_time_local >= datetime.combine(start, time.min))
    if end:
        query = query.where(Activity.start_time_local < datetime.combine(end + timedelta(days=1), time.min))
    if sport:
        if sport == "running":
            query = query.where(Activity.sport.contains("running"))
        else:
            query = query.where(Activity.sport == sport)
    if q:
        query = query.where(or_(Activity.name.icontains(q), Activity.sport.icontains(q)))

    total = session.scalar(select(func.count()).select_from(query.subquery())) or 0
    items = session.scalars(
        query.order_by(Activity.start_time_utc.desc()).limit(min(limit, 500)).offset(offset)
    ).all()
    analyzed = _analyzed_ids(session, [a.id for a in items])
    summaries = []
    for activity in items:
        summary = ActivitySummary.model_validate(activity)
        summary.has_analysis = activity.id in analyzed
        summaries.append(summary)
    return ActivityList(items=summaries, total=total)


def _analyzed_ids(session: Session, ids: list[int]) -> set[int]:
    if not ids:
        return set()
    return set(
        session.scalars(
            select(AnalysisNote.activity_id).where(AnalysisNote.activity_id.in_(ids))
        ).all()
    )


@router.get("/sports", response_model=list[str])
def list_sports(session: Session = Depends(get_session)) -> list[str]:
    rows = session.scalars(select(Activity.sport).distinct().order_by(Activity.sport)).all()
    return list(rows)


@router.get("/{activity_id}", response_model=ActivityDetail)
def get_activity(activity_id: int, session: Session = Depends(get_session)) -> ActivityDetail:
    activity = session.get(Activity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    detail = ActivityDetail.model_validate(activity)
    detail.has_analysis = bool(_analyzed_ids(session, [activity_id]))
    return detail


@router.patch("/{activity_id}", response_model=ActivityDetail)
def update_activity(
    activity_id: int, payload: ActivityUpdate, session: Session = Depends(get_session)
) -> ActivityDetail:
    """Edit title, session tag, or the athlete's note. A user-set title is locked
    against automatic workout naming."""
    activity = session.get(Activity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    if payload.name is not None and payload.name != activity.name:
        activity.name = payload.name
        activity.name_locked = True
    if payload.tag is not None:
        activity.tag = payload.tag or None  # empty string clears the tag
    if payload.user_note is not None:
        activity.user_note = payload.user_note
    session.commit()
    return activity


@router.delete("/{activity_id}", status_code=204)
def delete_activity(activity_id: int, session: Session = Depends(get_session)) -> Response:
    """Permanently remove an activity and its streams, laps and best efforts (ORM
    cascade). Analysis notes are intentionally left intact — they carry no foreign
    key so they survive re-imports, and the same rule applies to a manual delete.

    Note: a real Garmin activity deleted here reappears on the next sync, which
    recreates rows by activity id; only manually-added or stray rows stay gone."""
    activity = session.get(Activity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    session.delete(activity)
    session.commit()
    return Response(status_code=204)


# Tags whose sessions get the interval-style splits chart even without the
# auto-detected structured-workout flag.
_WORKOUT_TAGS = {"intervals", "tempo"}


def _lap_splits(laps: list[Lap], stream: Stream | None) -> list[SplitOut]:
    windows = [(lap.start_offset_s, lap.start_offset_s + lap.elapsed_s) for lap in laps]
    if stream is not None:
        gains = window_elevation_gains(stream.time_s, stream.altitude_m, windows)
        gap_means = window_gap_means(
            stream.time_s, stream.distance_m, stream.speed_mps, stream.altitude_m, windows
        )
    else:
        gains = [None] * len(laps)
        gap_means = [None] * len(laps)
    return [
        SplitOut(
            index=lap.lap_index,
            distance_m=lap.distance_m,
            elapsed_s=lap.elapsed_s,
            avg_speed_mps=lap.avg_speed_mps,
            avg_gap_speed_mps=gap_mean,
            elevation_gain_m=round(gain, 1) if gain is not None else None,
            avg_hr=lap.avg_hr,
            intensity=lap.intensity,
        )
        for lap, gain, gap_mean in zip(laps, gains, gap_means)
    ]


_MILE_M = 1609.344


@router.get("/{activity_id}/splits", response_model=SplitsOut)
def get_splits(
    activity_id: int,
    unit: str = Query("km", pattern="^(km|mile)$"),
    session: Session = Depends(get_session),
) -> SplitsOut:
    """Splits for the activity page chart. Structured/tagged workouts serve
    their laps; manual lap-button sessions serve those laps; everything else
    gets per-distance splits cut from the streams (runs only) — km by default,
    miles with ?unit=mile (mode stays "km", meaning "distance splits")."""
    activity = session.get(Activity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    if not activity.is_run:
        return SplitsOut(mode="none")

    stream = session.get(Stream, activity_id)
    laps = activity.laps
    if len(laps) > 1:
        if activity.is_workout or activity.tag in _WORKOUT_TAGS:
            return SplitsOut(mode="workout", splits=_lap_splits(laps, stream))
        if not is_autolap([lap.distance_m for lap in laps]):
            return SplitsOut(mode="laps", splits=_lap_splits(laps, stream))

    if stream is not None:
        splits = km_splits(
            stream.time_s,
            stream.distance_m,
            stream.altitude_m,
            stream.hr,
            split_m=_MILE_M if unit == "mile" else 1000.0,
            speed_mps=stream.speed_mps,
        )
        if splits:
            return SplitsOut(
                mode="km",
                splits=[
                    SplitOut(
                        index=s.index,
                        distance_m=s.distance_m,
                        elapsed_s=s.elapsed_s,
                        avg_speed_mps=s.avg_speed_mps,
                        avg_gap_speed_mps=s.avg_gap_speed_mps,
                        elevation_gain_m=s.elevation_gain_m,
                        avg_hr=round(s.avg_hr, 1) if s.avg_hr is not None else None,
                    )
                    for s in splits
                ],
            )
    if len(laps) > 1:  # autolap km laps, no usable streams
        return SplitsOut(mode="km", splits=_lap_splits(laps, stream))
    return SplitsOut(mode="none")


_RECENT_STRIP_SESSIONS = 30


@router.get("/{activity_id}/relative-effort", response_model=RelativeEffortOut)
def get_relative_effort(
    activity_id: int, session: Session = Depends(get_session)
) -> RelativeEffortOut:
    """This session's TRIMP ranked against every loaded session (any sport —
    TRIMP is comparable across them) in the trailing window, as seen from the
    session's own date, plus the recent sessions for a context strip."""
    activity = session.get(Activity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    if activity.trimp is None:
        return RelativeEffortOut(load=None, window_days=WINDOW_DAYS, window_sessions=0)

    window_start = activity.start_time_local - timedelta(days=WINDOW_DAYS)
    others = session.scalars(
        select(Activity)
        .where(Activity.trimp.is_not(None))
        .where(Activity.start_time_local >= window_start)
        .where(Activity.start_time_local <= activity.start_time_local)
        .where(Activity.id != activity.id)
        .order_by(Activity.start_time_local)
    ).all()
    loads = [a.trimp for a in others]
    percentile = effort_percentile(activity.trimp, loads)
    strip = (list(others) + [activity])[-_RECENT_STRIP_SESSIONS:]
    return RelativeEffortOut(
        load=activity.trimp,
        percentile=percentile,
        band=effort_band(percentile),
        window_days=WINDOW_DAYS,
        window_sessions=len(loads),
        recent=[
            RecentEffort(
                activity_id=a.id,
                day=a.start_time_local.date(),
                name=a.name,
                load=a.trimp,
                current=a.id == activity.id,
            )
            for a in strip
        ],
    )


@router.get("/{activity_id}/track", response_model=list[list[float]])
def get_track(
    activity_id: int,
    max_points: int = 80,
    session: Session = Depends(get_session),
) -> list[list[float]]:
    """Compact [lat, lng] polyline for thumbnails; [] when there is no GPS."""
    stream = session.get(Stream, activity_id)
    if stream is None:
        return []
    points = [
        [lat, lng]
        for lat, lng in zip(stream.lat, stream.lng)
        if lat is not None and lng is not None
    ]
    if len(points) < 2:
        return []
    stride = max(len(points) // max(max_points, 2), 1)
    sampled = points[::stride]
    if sampled[-1] != points[-1]:
        sampled.append(points[-1])
    return [[round(lat, 5), round(lng, 5)] for lat, lng in sampled]


@router.get("/{activity_id}/streams", response_model=StreamsOut)
def get_streams(activity_id: int, session: Session = Depends(get_session)) -> StreamsOut:
    stream = session.get(Stream, activity_id)
    if stream is None:
        raise HTTPException(status_code=404, detail="No streams for this activity")
    settings = get_or_create_settings(session)
    zones = zones_for_settings(settings)
    tiz = time_in_zones(
        [t for t in stream.time_s if t is not None], stream.hr, zones
    )
    # GAP series is derived, not stored: compute from the downsampled arrays so it
    # is available for every activity with speed + altitude, rescanned or not.
    gap = gap_speed_series(stream.time_s, stream.distance_m, stream.speed_mps, stream.altitude_m)
    p_zones = pace_zones_for_settings(settings)
    # Classify on GAP so hills land in the effort-equivalent zone (raw when disabled).
    zone_speeds = gap if settings.rtss_use_gap else stream.speed_mps
    time_s_clean = [t for t in stream.time_s if t is not None]
    tipz = time_in_pace_zones(time_s_clean, zone_speeds, p_zones)
    return StreamsOut(
        time_s=stream.time_s,
        distance_m=stream.distance_m,
        hr=stream.hr,
        speed_mps=stream.speed_mps,
        gap_speed_mps=gap,
        altitude_m=stream.altitude_m,
        cadence=stream.cadence,
        lat=stream.lat,
        lng=stream.lng,
        # Rows imported before the dynamics columns existed hold NULL, not [].
        power=stream.power or [],
        vertical_oscillation=stream.vertical_oscillation or [],
        vertical_ratio=stream.vertical_ratio or [],
        step_length=stream.step_length or [],
        stance_time=stream.stance_time or [],
        respiration=stream.respiration or [],
        zones=[ZoneOut(name=z.name, low_bpm=z.low_bpm, high_bpm=z.high_bpm) for z in zones],
        time_in_zones_s=tiz,
        pace_zones=[
            PaceZoneOut(
                name=z.name, low_speed_mps=z.low_speed_mps, high_speed_mps=z.high_speed_mps
            )
            for z in p_zones
        ],
        time_in_pace_zones_s=tipz,
    )
