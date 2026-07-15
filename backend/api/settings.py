from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.analysis.zones import hr_zones
from backend.db import get_session
from backend.schemas import SettingsIn, SettingsResponse, ZoneOut
from backend.sync.service import get_or_create_settings, recompute_in_background

router = APIRouter(prefix="/api/settings", tags=["settings"])


def _response(settings) -> SettingsResponse:
    zones = [
        ZoneOut(name=z.name, low_bpm=z.low_bpm, high_bpm=z.high_bpm)
        for z in hr_zones(settings.max_hr)
    ]
    return SettingsResponse(
        resting_hr=settings.resting_hr,
        max_hr=settings.max_hr,
        lthr=settings.lthr,
        threshold_pace_s_per_km=settings.threshold_pace_s_per_km,
        sex=settings.sex,
        zones=zones,
    )


@router.get("", response_model=SettingsResponse)
def get_settings(session: Session = Depends(get_session)) -> SettingsResponse:
    settings = get_or_create_settings(session)
    session.commit()
    return _response(settings)


@router.put("", response_model=SettingsResponse)
def update_settings(
    payload: SettingsIn, session: Session = Depends(get_session)
) -> SettingsResponse:
    settings = get_or_create_settings(session)
    settings.resting_hr = payload.resting_hr
    settings.max_hr = payload.max_hr
    settings.lthr = payload.lthr
    settings.threshold_pace_s_per_km = payload.threshold_pace_s_per_km
    settings.sex = payload.sex
    session.commit()
    # Load metrics depend on these values — refresh them for all activities.
    recompute_in_background()
    return _response(settings)
