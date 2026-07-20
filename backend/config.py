from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class AppConfig(BaseSettings):
    """Runtime configuration, overridable via FARTLEK_* environment variables."""

    data_dir: Path = BASE_DIR / "data"
    host: str = "127.0.0.1"
    port: int = 8077

    # The in-app Coach runs an AI agent with (whitelisted) shell access on this
    # machine via the Claude CLI. Off by default: opt in deliberately, and only
    # when the app is bound to localhost (see backend/api/coach.py).
    coach_enabled: bool = False
    sync_interval_minutes: int = 30
    scheduler_enabled: bool = True
    # Max number of points kept per stored stream; raw FIT files keep full resolution.
    stream_max_points: int = 3000

    # Backups: rclone destination (e.g. "gdrive:fartlek", or a crypt remote for
    # encryption). Empty = local snapshots only via the backup command, no schedule.
    rclone_remote: str = ""
    backup_keep: int = 7  # rotated local snapshots (mirrored to the remote)
    backup_hour: int = 3  # nightly upload time (local), used when a remote is set
    # FIT files are re-downloadable from Garmin (make backfill) — backing them up
    # is insurance against losing the Garmin account itself. Cheap: incremental.
    backup_include_fit: bool = True
    # Garmin OAuth tokens grant account access — only back them up deliberately.
    backup_include_tokens: bool = False

    # Google Calendar push sync of the training plan. Set the target calendar's
    # id (share the calendar with the service account first — see
    # backend/sync/gcal.py for the full setup). Empty = disabled.
    gcal_calendar_id: str = ""
    gcal_key_file: Path | None = None  # default: data/gcal-service-account.json

    # Real environment variables win over .env — systemd Environment= lines
    # keep working; .env makes the same config reach CLI runs (make gcal-sync).
    model_config = {
        "env_prefix": "FARTLEK_",
        "env_file": BASE_DIR / ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    @property
    def gcal_key_path(self) -> Path:
        return self.gcal_key_file or self.data_dir / "gcal-service-account.json"

    @property
    def gcal_enabled(self) -> bool:
        return bool(self.gcal_calendar_id.strip()) and self.gcal_key_path.exists()

    @property
    def db_path(self) -> Path:
        return self.data_dir / "fartlek.sqlite3"

    @property
    def fit_dir(self) -> Path:
        return self.data_dir / "fit"

    @property
    def garth_dir(self) -> Path:
        return self.data_dir / "garth"

    def ensure_dirs(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.fit_dir.mkdir(parents=True, exist_ok=True)


config = AppConfig()
