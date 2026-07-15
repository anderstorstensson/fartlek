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
