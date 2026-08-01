"""Injury and niggle episodes: CRUD over the athlete's injury history.

The coach writes here instead of into prose in data/athlete-profile.md, because
previous injury is the strongest known risk factor for a new one and the history
is only useful if it can be queried against training load. Methodology lives in
docs/coach/physio-guidance.md; the evidence in docs/running-injury-review.md.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db import get_session
from backend.models import Niggle
from backend.schemas import NiggleIn, NiggleOut

router = APIRouter(prefix="/api/niggles", tags=["niggles"])


@router.get("", response_model=list[NiggleOut])
def list_niggles(
    active_only: bool = False,
    site: str | None = None,
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_session),
) -> list[NiggleOut]:
    query = select(Niggle)
    if active_only:
        query = query.where(Niggle.resolved_date.is_(None))
    if site:
        query = query.where(Niggle.site == site)
    return session.scalars(
        query.order_by(Niggle.onset_date.desc()).limit(min(limit, 200)).offset(offset)
    ).all()


@router.get("/{niggle_id}", response_model=NiggleOut)
def get_niggle(niggle_id: int, session: Session = Depends(get_session)) -> NiggleOut:
    niggle = session.get(Niggle, niggle_id)
    if niggle is None:
        raise HTTPException(status_code=404, detail="Niggle not found")
    return niggle


@router.post("", response_model=NiggleOut)
def create_niggle(payload: NiggleIn, session: Session = Depends(get_session)) -> NiggleOut:
    niggle = Niggle(**payload.model_dump())
    session.add(niggle)
    session.commit()
    return niggle


@router.put("/{niggle_id}", response_model=NiggleOut)
def update_niggle(
    niggle_id: int, payload: NiggleIn, session: Session = Depends(get_session)
) -> NiggleOut:
    niggle = session.get(Niggle, niggle_id)
    if niggle is None:
        raise HTTPException(status_code=404, detail="Niggle not found")
    for field, value in payload.model_dump().items():
        setattr(niggle, field, value)
    session.commit()
    return niggle


@router.delete("/{niggle_id}", response_model=dict)
def delete_niggle(niggle_id: int, session: Session = Depends(get_session)) -> dict:
    niggle = session.get(Niggle, niggle_id)
    if niggle is None:
        raise HTTPException(status_code=404, detail="Niggle not found")
    session.delete(niggle)
    session.commit()
    return {"deleted": niggle_id}
