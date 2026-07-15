from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from backend.analysis.zones import time_in_zones, zones_for_settings
from backend.db import get_session
from backend.models import Activity, Stream
from backend.schemas import ActivityDetail, ActivityList, StreamsOut, ZoneOut
from backend.sync.service import get_or_create_settings

router = APIRouter(prefix="/api/activities", tags=["activities"])


@router.get("", response_model=ActivityList)
def list_activities(
    limit: int = 50,
    offset: int = 0,
    sport: str | None = None,
    q: str | None = None,
    session: Session = Depends(get_session),
) -> ActivityList:
    query = select(Activity)
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
    return ActivityList(items=items, total=total)


@router.get("/sports", response_model=list[str])
def list_sports(session: Session = Depends(get_session)) -> list[str]:
    rows = session.scalars(select(Activity.sport).distinct().order_by(Activity.sport)).all()
    return list(rows)


@router.get("/{activity_id}", response_model=ActivityDetail)
def get_activity(activity_id: int, session: Session = Depends(get_session)) -> ActivityDetail:
    activity = session.get(Activity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


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
    return StreamsOut(
        time_s=stream.time_s,
        distance_m=stream.distance_m,
        hr=stream.hr,
        speed_mps=stream.speed_mps,
        altitude_m=stream.altitude_m,
        cadence=stream.cadence,
        lat=stream.lat,
        lng=stream.lng,
        zones=[ZoneOut(name=z.name, low_bpm=z.low_bpm, high_bpm=z.high_bpm) for z in zones],
        time_in_zones_s=tiz,
    )
