"""Backup: consistent local snapshots plus optional rclone upload.

The irreplaceable data is the SQLite database (notes, races, plans, wellness,
settings — much of it not recomputable from Garmin) and the athlete profile.
FIT files are the raw source of truth for activities; they are append-only, so
after a one-time seed upload only new files transfer.

Local snapshots go to data/backups/ (rotated). When FARTLEK_RCLONE_REMOTE is
set (e.g. "gdrive:fartlek", or an rclone *crypt* remote for encrypted backups),
each backup also uploads:

- snapshots/  — mirrored with `rclone sync` (remote keeps exactly the rotated set)
- fit/        — `rclone copy` (never deletes remote files; incremental by default)
- athlete-profile.md
- garth/ tokens — only with FARTLEK_BACKUP_INCLUDE_TOKENS=1; they grant Garmin
  account access, so leave them out of plain-text remotes (re-auth with
  `make login` after a restore instead).
"""

import gzip
import logging
import shutil
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

from backend.config import config

logger = logging.getLogger(__name__)

_SNAPSHOT_PREFIX = "fartlek-"
_SNAPSHOT_SUFFIX = ".sqlite3.gz"


def backups_dir() -> Path:
    return config.data_dir / "backups"


def create_snapshot(keep: int | None = None) -> Path:
    """Consistent gzipped DB snapshot (safe against live writers) + rotation."""
    backups_dir().mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = backups_dir() / f"{_SNAPSHOT_PREFIX}{stamp}{_SNAPSHOT_SUFFIX}"

    tmp = target.with_suffix(".tmp")
    source = sqlite3.connect(config.db_path)
    try:
        dest = sqlite3.connect(tmp)
        try:
            source.backup(dest)  # sqlite's online backup API — WAL-safe
        finally:
            dest.close()
    finally:
        source.close()

    with open(tmp, "rb") as raw, gzip.open(target, "wb", compresslevel=6) as packed:
        shutil.copyfileobj(raw, packed)
    tmp.unlink()

    _rotate(keep if keep is not None else config.backup_keep)
    return target


def _rotate(keep: int) -> None:
    snapshots = sorted(backups_dir().glob(f"{_SNAPSHOT_PREFIX}*{_SNAPSHOT_SUFFIX}"))
    for old in snapshots[:-keep] if keep > 0 else []:
        old.unlink()


def _rclone(*args: str) -> None:
    result = subprocess.run(
        ["rclone", *args], capture_output=True, text=True, timeout=3600
    )
    if result.returncode != 0:
        raise RuntimeError(f"rclone {args[0]} failed: {result.stderr.strip()[:500]}")


def run_backup() -> dict:
    """Snapshot locally, then upload to the configured rclone remote (if any)."""
    snapshot = create_snapshot()
    result = {"snapshot": str(snapshot), "uploaded": False}

    remote = config.rclone_remote.strip().rstrip("/")
    if not remote:
        logger.info("Backup snapshot written (no rclone remote configured): %s", snapshot)
        return result

    if shutil.which("rclone") is None:
        raise RuntimeError(
            "FARTLEK_RCLONE_REMOTE is set but rclone is not installed — "
            "see the README's backup section."
        )

    # Mirror the rotated snapshot set; incrementally copy the append-only FIT files.
    _rclone("sync", str(backups_dir()), f"{remote}/snapshots")
    _rclone("copy", str(config.fit_dir), f"{remote}/fit")
    profile = config.data_dir / "athlete-profile.md"
    if profile.exists():
        _rclone("copy", str(profile), remote)
    if config.backup_include_tokens and config.garth_dir.exists():
        _rclone("sync", str(config.garth_dir), f"{remote}/garth")

    result["uploaded"] = True
    logger.info("Backup uploaded to %s", remote)
    return result


def run_backup_quietly() -> None:
    """Scheduler entry point — failures are logged, never raised."""
    try:
        run_backup()
    except Exception:
        logger.exception("Scheduled backup failed")
