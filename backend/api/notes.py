from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db import get_session
from backend.models import AnalysisNote
from backend.schemas import NoteIn, NoteOut

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.get("", response_model=list[NoteOut])
def list_notes(
    activity_id: int | None = None,
    kind: str | None = None,
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_session),
) -> list[NoteOut]:
    query = select(AnalysisNote)
    if activity_id is not None:
        query = query.where(AnalysisNote.activity_id == activity_id)
    if kind:
        query = query.where(AnalysisNote.kind == kind)
    return session.scalars(
        query.order_by(AnalysisNote.created_at.desc()).limit(min(limit, 200)).offset(offset)
    ).all()


@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: int, session: Session = Depends(get_session)) -> NoteOut:
    note = session.get(AnalysisNote, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("", response_model=NoteOut)
def create_note(payload: NoteIn, session: Session = Depends(get_session)) -> NoteOut:
    note = AnalysisNote(**payload.model_dump())
    session.add(note)
    session.commit()
    return note


@router.put("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int, payload: NoteIn, session: Session = Depends(get_session)
) -> NoteOut:
    note = session.get(AnalysisNote, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    for field, value in payload.model_dump().items():
        setattr(note, field, value)
    session.commit()
    return note


@router.delete("/{note_id}", response_model=dict)
def delete_note(note_id: int, session: Session = Depends(get_session)) -> dict:
    note = session.get(AnalysisNote, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return {"deleted": note_id}
