from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend.analysis.pace_zones import pace_zones_for_settings
from backend.analysis.zones import zones_for_settings
from backend.db import get_session
from backend.schemas import (
    PaceZoneOut,
    SettingsIn,
    SettingsResponse,
    SettingsUpdate,
    ZoneOut,
)
from backend.sync.service import get_or_create_settings, recompute_in_background

router = APIRouter(prefix="/api/settings", tags=["settings"])

_SETTINGS_FIELDS = list(SettingsIn.model_fields)


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
        units=settings.units,
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
    payload: SettingsUpdate, session: Session = Depends(get_session)
) -> SettingsResponse:
    """Merge semantics: only fields present in the payload change. Partial
    writers (the AI coach updating threshold pace, an older Settings tab) must
    never silently reset unrelated settings to their defaults."""
    settings = get_or_create_settings(session)
    merged = {field: getattr(settings, field) for field in _SETTINGS_FIELDS}
    merged.update(payload.model_dump(exclude_unset=True))
    try:
        # Full validation (incl. cross-field rules) against the merged state.
        validated = SettingsIn(**merged)
    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail=exc.errors(include_url=False, include_context=False),
        ) from exc

    for field in _SETTINGS_FIELDS:
        setattr(settings, field, getattr(validated, field))
    session.commit()
    # Load metrics depend on these values — refresh them for all activities.
    recompute_in_background()
    return _response(settings)
