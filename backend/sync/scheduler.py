"""Background auto-sync using APScheduler (runs inside the web process)."""

import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from backend.config import config
from backend.sync.service import run_sync

logger = logging.getLogger(__name__)

_scheduler: BackgroundScheduler | None = None


def start_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        return
    _scheduler = BackgroundScheduler()
    _scheduler.add_job(
        run_sync,
        "interval",
        minutes=config.sync_interval_minutes,
        next_run_time=datetime.now() + timedelta(seconds=15),
        max_instances=1,
        coalesce=True,
        id="garmin_sync",
    )
    if config.rclone_remote.strip():
        from backend.sync.backup import run_backup_quietly

        _scheduler.add_job(
            run_backup_quietly,
            "cron",
            hour=config.backup_hour,
            minute=30,
            max_instances=1,
            coalesce=True,
            id="nightly_backup",
        )
        logger.info("Nightly backup scheduled at %02d:30", config.backup_hour)
    if config.gcal_enabled:
        from backend.sync.gcal import sync_quietly

        # Plan mutations already trigger a sync; this nightly pass reconciles
        # anything missed (app restarts, transient Google API failures).
        _scheduler.add_job(
            sync_quietly,
            "cron",
            hour=4,
            minute=15,
            max_instances=1,
            coalesce=True,
            id="gcal_plan_sync",
        )
        logger.info("Nightly Google Calendar plan sync scheduled at 04:15")
    _scheduler.start()
    logger.info("Auto-sync scheduled every %d minutes", config.sync_interval_minutes)


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
