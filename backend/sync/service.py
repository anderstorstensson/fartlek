"""Sync orchestration: pull new activities from Garmin into the local DB."""

import logging
import threading
from datetime import datetime, timezone

from sqlalchemy import select

from backend.config import config
from backend.db import session_scope
from backend.models import Activity, AthleteSettings, SyncState
from backend.sync import garmin
from backend.sync.importer import compute_loads_for, import_activity

logger = logging.getLogger(__name__)

_PAGE_SIZE = 50
_sync_lock = threading.Lock()


def get_or_create_settings(session) -> AthleteSettings:
    settings = session.get(AthleteSettings, 1)
    if settings is None:
        settings = AthleteSettings(id=1)
        session.add(settings)
        session.flush()
    return settings


def _set_state(session, **kwargs) -> None:
    state = session.get(SyncState, 1)
    if state is None:
        state = SyncState(id=1)
        session.add(state)
    for key, value in kwargs.items():
        setattr(state, key, value)


def run_sync(full: bool = False) -> dict:
    """Fetch activities newer than what we have (or everything, if full=True)."""
    if not _sync_lock.acquire(blocking=False):
        return {"status": "already_running", "new_activities": 0}

    try:
        return _run_sync_locked(full)
    finally:
        _sync_lock.release()


def _run_sync_locked(full: bool) -> dict:
    with session_scope() as session:
        _set_state(session, status="running", message="Connecting to Garmin…")

    try:
        client = garmin.client_from_tokens()
    except garmin.GarminAuthError as exc:
        with session_scope() as session:
            _set_state(session, status="error", message=str(exc))
        return {"status": "error", "message": str(exc), "new_activities": 0}

    imported = 0
    try:
        with session_scope() as session:
            known_ids = set(session.scalars(select(Activity.id)).all())

        start = 0
        while True:
            summaries = garmin.list_activities(client, start, _PAGE_SIZE)
            if not summaries:
                break
            new_summaries = [s for s in summaries if s["activityId"] not in known_ids]
            for summary in new_summaries:
                try:
                    _import_one(client, summary)
                except Exception:
                    logger.exception(
                        "Skipping activity %s", summary.get("activityId")
                    )
                    continue
                imported += 1
                if imported % 10 == 0:
                    with session_scope() as session:
                        _set_state(
                            session, message=f"Imported {imported} activities…"
                        )
            if not full and not new_summaries:
                break  # a full page of already-known activities: we're caught up
            start += _PAGE_SIZE

        with session_scope() as session:
            _set_state(
                session,
                status="idle",
                message=f"Synced {imported} new activities",
                last_sync_at=datetime.now(timezone.utc),
                synced_activities=session.query(Activity).count(),
            )
        logger.info("Sync complete: %d new activities", imported)
        return {"status": "ok", "new_activities": imported}
    except Exception as exc:
        logger.exception("Sync failed")
        with session_scope() as session:
            _set_state(session, status="error", message=f"Sync failed: {exc}")
        return {"status": "error", "message": str(exc), "new_activities": imported}


def _import_one(client, summary: dict) -> None:
    activity_id = summary["activityId"]
    fit_bytes = garmin.download_fit(client, activity_id)
    if fit_bytes:
        fit_path = config.fit_dir / f"{activity_id}.fit"
        fit_path.write_bytes(fit_bytes)
    with session_scope() as session:
        settings = get_or_create_settings(session)
        import_activity(session, summary, fit_bytes, settings)


def run_sync_in_background(full: bool = False) -> None:
    thread = threading.Thread(target=run_sync, kwargs={"full": full}, daemon=True)
    thread.start()


def recompute_all_metrics() -> int:
    """Recompute TRIMP/rTSS/hrTSS after athlete settings change."""
    count = 0
    with session_scope() as session:
        settings = get_or_create_settings(session)
        for activity in session.scalars(select(Activity)).all():
            compute_loads_for(activity, settings)
            count += 1
    return count


def recompute_in_background() -> None:
    thread = threading.Thread(target=recompute_all_metrics, daemon=True)
    thread.start()


def rescan_fit_flags() -> int:
    """Re-parse stored FIT files to (re)detect workout flags and lap intensities.

    Needed once for activities imported before those fields existed; new imports
    detect them automatically. Commits per activity so it can run alongside a sync.
    """
    from backend.sync.importer import parse_fit

    with session_scope() as session:
        ids = list(session.scalars(select(Activity.id)).all())

    updated = 0
    for activity_id in ids:
        fit_path = config.fit_dir / f"{activity_id}.fit"
        if not fit_path.exists():
            continue
        try:
            _streams, fit_laps, is_workout = parse_fit(fit_path.read_bytes())
        except Exception:
            logger.warning("Rescan: FIT parse failed for %s", activity_id)
            continue
        intensities = [lap.get("intensity") for lap in fit_laps]
        with session_scope() as session:
            activity = session.get(Activity, activity_id)
            if activity is None:
                continue
            activity.is_workout = is_workout
            for lap in activity.laps:
                if lap.lap_index < len(intensities):
                    lap.intensity = intensities[lap.lap_index]
        updated += 1
    return updated
