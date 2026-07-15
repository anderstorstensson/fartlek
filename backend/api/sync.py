from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.db import get_session
from backend.models import Activity, SyncState
from backend.schemas import SyncStatus
from backend.sync import garmin
from backend.sync.service import run_sync_in_background

router = APIRouter(prefix="/api/sync", tags=["sync"])


@router.post("", response_model=dict)
def trigger_sync(full: bool = False) -> dict:
    run_sync_in_background(full=full)
    return {"started": True, "full": full}


@router.get("/status", response_model=SyncStatus)
def sync_status(session: Session = Depends(get_session)) -> SyncStatus:
    state = session.get(SyncState, 1)
    total = session.scalar(select(func.count()).select_from(Activity)) or 0
    return SyncStatus(
        status=state.status if state else "idle",
        message=state.message if state else "",
        last_sync_at=state.last_sync_at if state else None,
        logged_in=garmin.is_logged_in(),
        total_activities=total,
    )
