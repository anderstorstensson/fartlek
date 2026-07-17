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


def rpe_from_garmin(value) -> int | None:
    """Garmin stores the watch's 1-10 RPE as directWorkoutRpe = rating × 10."""
    if not isinstance(value, (int, float)) or not 10 <= value <= 100:
        return None
    return round(value / 10)


def feel_from_garmin(value) -> int | None:
    """Garmin stores the five feel smileys as directWorkoutFeel 0/25/50/75/100;
    map to 1 (very weak) … 5 (very strong)."""
    if not isinstance(value, (int, float)) or not 0 <= value <= 100:
        return None
    return round(value / 25) + 1


def fetch_self_evaluation(client: Garmin, activity_id: int) -> tuple[int | None, int | None]:
    """(perceived_exertion 1-10, feel 1-5) from the activity detail endpoint —
    the self-evaluation is not in the list summary or the FIT file. (None, None)
    when the athlete skipped the prompt or the fetch fails."""
    try:
        detail = client.get_activity(activity_id) or {}
    except Exception as exc:
        logger.warning("Self-evaluation fetch failed for activity %s: %s", activity_id, exc)
        return None, None
    summary = detail.get("summaryDTO") or {}
    return (
        rpe_from_garmin(summary.get("directWorkoutRpe")),
        feel_from_garmin(summary.get("directWorkoutFeel")),
    )


def fetch_vo2max_by_day(client: Garmin, start_iso: str, end_iso: str) -> dict[str, float]:
    """Daily running VO2 max (precise value, ml/kg/min) for a date span, keyed by
    ISO date. One request per span; days without a value are simply absent."""
    try:
        rows = client.connectapi(
            f"{client.garmin_connect_metrics_url}/{start_iso}/{end_iso}"
        ) or []
    except Exception as exc:
        logger.warning("VO2 max fetch failed for %s..%s: %s", start_iso, end_iso, exc)
        return {}
    result: dict[str, float] = {}
    for row in rows:
        generic = row.get("generic") or {}
        day = generic.get("calendarDate")
        value = generic.get("vo2MaxPreciseValue") or generic.get("vo2MaxValue")
        if day and isinstance(value, (int, float)):
            result[day] = float(value)
    return result


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
