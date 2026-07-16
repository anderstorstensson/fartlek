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

        wellness_days = _sync_extras(client, full)

        with session_scope() as session:
            _set_state(
                session,
                status="idle",
                message=f"Synced {imported} new activities",
                last_sync_at=datetime.now(timezone.utc),
                synced_activities=session.query(Activity).count(),
            )
        logger.info(
            "Sync complete: %d new activities, %d wellness days", imported, wellness_days
        )
        return {"status": "ok", "new_activities": imported, "wellness_days": wellness_days}
    except Exception as exc:
        logger.exception("Sync failed")
        with session_scope() as session:
            _set_state(session, status="error", message=f"Sync failed: {exc}")
        return {"status": "error", "message": str(exc), "new_activities": imported}


def _sync_extras(client, full: bool) -> int:
    """Wellness + weather after the activity sync; failures must not fail the sync."""
    wellness_days = 0
    try:
        from backend.sync.wellness import sync_wellness

        wellness_days = sync_wellness(client, backfill_days=365 if full else None)
    except Exception:
        logger.exception("Wellness sync failed")
    try:
        from backend.sync.weather import enrich_missing_weather

        # Capped per cycle: a large backlog must not stall the 30-min sync loop
        # for hours — it drains across successive syncs instead.
        enrich_missing_weather(limit=150)
    except Exception:
        logger.exception("Weather enrichment failed")
    return wellness_days


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


def rename_workout_activities() -> int:
    """Backfill structure-derived names ("10×3 min / 1 min rest") for interval
    runs already in the DB, from their stored laps. New imports and rescans
    name themselves; this is for history imported before the feature existed."""
    from backend.analysis.workout_naming import workout_name

    renamed = 0
    with session_scope() as session:
        workouts = session.scalars(
            select(Activity)
            .where(Activity.is_workout.is_(True))
            .where(Activity.sport.contains("running"))
        ).all()
        for activity in workouts:
            laps = [
                {"elapsed_s": lap.elapsed_s, "distance_m": lap.distance_m,
                 "intensity": lap.intensity}
                for lap in activity.laps
            ]
            derived = workout_name(laps)
            if derived and derived != activity.name:
                activity.name = derived
                renamed += 1
    return renamed


def rescan_fit_flags() -> int:
    """Re-extract streams, workout flags, dynamics and derived metrics from the
    stored FIT files for every activity.

    Needed once after upgrades that add new stream fields or derived metrics;
    new imports compute them automatically. Commits per activity so it can run
    alongside a sync.
    """
    from backend.sync.importer import refresh_from_fit

    # Newest first: recent activities are the ones being looked at while a
    # long backfill grinds through history.
    with session_scope() as session:
        ids = list(
            session.scalars(
                select(Activity.id).order_by(Activity.start_time_utc.desc())
            ).all()
        )

    updated = 0
    for activity_id in ids:
        fit_path = config.fit_dir / f"{activity_id}.fit"
        if not fit_path.exists():
            continue
        fit_bytes = fit_path.read_bytes()
        with session_scope() as session:
            settings = get_or_create_settings(session)
            activity = session.get(Activity, activity_id)
            if activity is None:
                continue
            if refresh_from_fit(activity, fit_bytes, settings):
                updated += 1
    return updated
