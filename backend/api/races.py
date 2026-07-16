"""Goal races: CRUD plus a Riegel prediction from recent best efforts."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.analysis.prediction import predict
from backend.db import get_session
from backend.models import Race
from backend.schemas import RaceIn, RaceOut

router = APIRouter(prefix="/api/races", tags=["races"])


def _fmt_hms(seconds: float) -> str:
    s = int(round(seconds))
    h, rest = divmod(s, 3600)
    m, sec = divmod(rest, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"


def _to_out(race: Race, session: Session) -> RaceOut:
    out = RaceOut.model_validate(race)
    out.days_until = (race.day - date.today()).days
    prediction = predict(session, race.distance_m)
    if prediction is not None:
        out.predicted_time_s = round(prediction.time_s, 0)
        out.predicted_from = (
            f"{prediction.anchor_label} {_fmt_hms(prediction.anchor_duration_s)}"
            f" ({prediction.anchor_date})"
        )
    return out


@router.get("", response_model=list[RaceOut])
def list_races(
    upcoming: bool = False, session: Session = Depends(get_session)
) -> list[RaceOut]:
    query = select(Race).order_by(Race.day)
    if upcoming:
        query = query.where(Race.day >= date.today())
    return [_to_out(race, session) for race in session.scalars(query).all()]


@router.post("", response_model=RaceOut)
def create_race(payload: RaceIn, session: Session = Depends(get_session)) -> RaceOut:
    race = Race(**payload.model_dump())
    session.add(race)
    session.commit()
    return _to_out(race, session)


@router.put("/{race_id}", response_model=RaceOut)
def update_race(
    race_id: int, payload: RaceIn, session: Session = Depends(get_session)
) -> RaceOut:
    race = session.get(Race, race_id)
    if race is None:
        raise HTTPException(status_code=404, detail="Race not found")
    for key, value in payload.model_dump().items():
        setattr(race, key, value)
    session.commit()
    return _to_out(race, session)


@router.delete("/{race_id}", response_model=dict)
def delete_race(race_id: int, session: Session = Depends(get_session)) -> dict:
    race = session.get(Race, race_id)
    if race is None:
        raise HTTPException(status_code=404, detail="Race not found")
    session.delete(race)
    session.commit()
    return {"deleted": race_id}
