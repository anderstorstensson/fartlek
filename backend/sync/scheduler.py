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
    _scheduler.start()
    logger.info("Auto-sync scheduled every %d minutes", config.sync_interval_minutes)


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
