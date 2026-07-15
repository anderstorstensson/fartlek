"""Thin wrapper around python-garminconnect (garth-based auth).

Tokens are persisted in data/garth/ after an interactive login, so the
background sync never needs the password again (tokens auto-refresh).
"""

import io
import logging
import zipfile
from collections.abc import Callable

from garminconnect import Garmin

from backend.config import config

logger = logging.getLogger(__name__)


class GarminAuthError(Exception):
    pass


def is_logged_in() -> bool:
    return config.garth_dir.exists() and any(config.garth_dir.iterdir())


def client_from_tokens() -> Garmin:
    if not is_logged_in():
        raise GarminAuthError(
            "No Garmin tokens found. Run: uv run python -m backend.cli login"
        )
    try:
        client = Garmin()
        client.login(str(config.garth_dir))
        return client
    except Exception as exc:
        raise GarminAuthError(f"Garmin token login failed: {exc}") from exc


def interactive_login(email: str, password: str, prompt_mfa: Callable[[], str]) -> None:
    """Log in with credentials (asking for an MFA code if needed) and persist tokens.

    Passing the token directory to login() makes garminconnect (>= 0.3) dump the
    tokens there itself after a successful credential login.
    """
    config.garth_dir.mkdir(parents=True, exist_ok=True)
    client = Garmin(email=email, password=password, prompt_mfa=prompt_mfa)
    client.login(str(config.garth_dir))
    if not any(config.garth_dir.iterdir()):
        # Fallback for library versions that don't auto-dump.
        client.client.dump(str(config.garth_dir))


def list_activities(client: Garmin, start: int, limit: int) -> list[dict]:
    return client.get_activities(start, limit) or []


def download_fit(client: Garmin, activity_id: int) -> bytes | None:
    """Download the original upload (a zip usually containing one .fit file)."""
    try:
        raw = client.download_activity(
            activity_id, dl_fmt=Garmin.ActivityDownloadFormat.ORIGINAL
        )
    except Exception as exc:
        logger.warning("Download failed for activity %s: %s", activity_id, exc)
        return None
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            fit_names = [n for n in zf.namelist() if n.lower().endswith(".fit")]
            if not fit_names:
                return None
            return zf.read(fit_names[0])
    except zipfile.BadZipFile:
        # Some uploads come back as a bare FIT file rather than a zip.
        return raw if b".FIT" in raw[:12] else None
