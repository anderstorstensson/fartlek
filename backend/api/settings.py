from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.analysis.pace_zones import pace_zones_for_settings
from backend.analysis.zones import zones_for_settings
from backend.db import get_session
from backend.schemas import PaceZoneOut, SettingsIn, SettingsResponse, ZoneOut
from backend.sync.service import get_or_create_settings, recompute_in_background

router = APIRouter(prefix="/api/settings", tags=["settings"])


def _response(settings) -> SettingsResponse:
    zones = [
        ZoneOut(name=z.name, low_bpm=z.low_bpm, high_bpm=z.high_bpm)
        for z in zones_for_settings(settings)
    ]
    return SettingsResponse(
        resting_hr=settings.resting_hr,
        max_hr=settings.max_hr,
        lthr=settings.lthr,
        threshold_pace_s_per_km=settings.threshold_pace_s_per_km,
        sex=settings.sex,
        zone_mode=settings.zone_mode,
        manual_zone_bounds=settings.manual_zone_bounds,
        rtss_use_gap=settings.rtss_use_gap,
        pace_zone_mode=settings.pace_zone_mode,
        manual_pace_zone_bounds=settings.manual_pace_zone_bounds,
        coaching_tone=settings.coaching_tone,
        display_locale=settings.display_locale,
        coach_model=settings.coach_model,
        zones=zones,
        pace_zones=[
            PaceZoneOut(
                name=z.name, low_speed_mps=z.low_speed_mps, high_speed_mps=z.high_speed_mps
            )
            for z in pace_zones_for_settings(settings)
        ],
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
    settings.zone_mode = payload.zone_mode
    settings.manual_zone_bounds = payload.manual_zone_bounds
    settings.rtss_use_gap = payload.rtss_use_gap
    settings.pace_zone_mode = payload.pace_zone_mode
    settings.manual_pace_zone_bounds = payload.manual_pace_zone_bounds
    settings.coaching_tone = payload.coaching_tone
    settings.display_locale = payload.display_locale
    settings.coach_model = payload.coach_model
    session.commit()
    # Load metrics depend on these values — refresh them for all activities.
    recompute_in_background()
    return _response(settings)
