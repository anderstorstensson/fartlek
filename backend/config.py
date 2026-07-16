from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class AppConfig(BaseSettings):
    """Runtime configuration, overridable via FARTLEK_* environment variables."""

    data_dir: Path = BASE_DIR / "data"
    host: str = "127.0.0.1"
    port: int = 8077
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

    model_config = {"env_prefix": "FARTLEK_"}

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
