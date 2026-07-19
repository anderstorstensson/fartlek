"""Google Calendar push sync for the training plan (service account, no OAuth flow).

One-time setup:

1. In the Google Cloud console: create a project, enable the "Google Calendar
   API", create a service account (no roles needed), and download its JSON key
   to data/gcal-service-account.json (or point FARTLEK_GCAL_KEY_FILE at it).
2. In Google Calendar: create a dedicated calendar (e.g. "Training") and share
   it with the service account's email address (found in the JSON key) with
   "Make changes to events" permission.
3. Set FARTLEK_GCAL_CALENDAR_ID to that calendar's id (calendar settings →
   "Integrate calendar"; looks like xxx@group.calendar.google.com).

Sync mirrors the planned_workouts table into that calendar. Events carry a
private extended property with a key stable across plan re-imports (see
backend/plan_export.py), so a revised plan updates or removes its existing
events instead of duplicating them. Only events carrying the marker property
are ever touched — anything else in the calendar is left alone.
"""

import logging
import threading
import time
from datetime import timedelta
from urllib.parse import quote

from sqlalchemy import select

from backend.config import config
from backend.db import session_scope
from backend.models import PlannedWorkout
from backend.plan_export import description_text, stable_keys

logger = logging.getLogger(__name__)

API_BASE = "https://www.googleapis.com/calendar/v3"
_SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
_MARKER_PROP = "fartlek"
_MARKER_VALUE = "plan"
_KEY_PROP = "fartlek_key"


class GcalError(RuntimeError):
    pass


class GcalClient:
    """Thin REST client for the events collection of one calendar."""

    def __init__(self, calendar_id: str, key_file) -> None:
        try:
            from google.auth.transport.requests import AuthorizedSession
            from google.oauth2 import service_account
        except ImportError as exc:
            raise GcalError(
                "google-auth is not installed — run 'uv sync' (or pip install google-auth)"
            ) from exc
        try:
            credentials = service_account.Credentials.from_service_account_file(
                str(key_file), scopes=_SCOPES
            )
        except Exception as exc:
            raise GcalError(f"Could not load service account key {key_file}: {exc}") from exc
        self._http = AuthorizedSession(credentials)
        self._events_url = f"{API_BASE}/calendars/{quote(calendar_id)}/events"

    def _send(self, method: str, url: str, action: str, **kwargs):
        """Request with exponential backoff on Google's rate limiting (403
        rateLimitExceeded / 429), which bulk insert bursts reliably trigger."""
        delay = 1.0
        for attempt in range(6):
            response = self._http.request(method, url, timeout=30, **kwargs)
            if response.status_code < 400:
                return response
            retryable = response.status_code == 429 or (
                response.status_code == 403 and "rateLimitExceeded" in response.text
            )
            if retryable and attempt < 5:
                time.sleep(delay)
                delay *= 2
                continue
            detail = response.text[:300]
            if response.status_code == 404 and action == "list":
                detail = (
                    "calendar not found — check FARTLEK_GCAL_CALENDAR_ID and that the "
                    "calendar is shared with the service account"
                )
            if response.status_code in (404, 410) and action == "delete":
                return response  # already gone — the goal state holds
            raise GcalError(f"Google Calendar {action} failed ({response.status_code}): {detail}")
        raise GcalError(f"Google Calendar {action} failed: retries exhausted")

    def list_plan_events(self) -> list[dict]:
        events: list[dict] = []
        page_token: str | None = None
        while True:
            params = {
                "privateExtendedProperty": f"{_MARKER_PROP}={_MARKER_VALUE}",
                "maxResults": 2500,
                "showDeleted": "false",
            }
            if page_token:
                params["pageToken"] = page_token
            payload = self._send("GET", self._events_url, "list", params=params).json()
            events.extend(payload.get("items", []))
            page_token = payload.get("nextPageToken")
            if not page_token:
                return events

    def insert(self, body: dict) -> None:
        self._send("POST", self._events_url, "insert", json=body)

    def patch(self, event_id: str, body: dict) -> None:
        self._send("PATCH", f"{self._events_url}/{quote(event_id)}", "update", json=body)

    def delete(self, event_id: str) -> None:
        self._send("DELETE", f"{self._events_url}/{quote(event_id)}", "delete")


def event_body(workout: PlannedWorkout, key: str) -> dict:
    return {
        "summary": workout.title,
        "description": description_text(workout),
        "start": {"date": workout.day.isoformat()},
        "end": {"date": (workout.day + timedelta(days=1)).isoformat()},
        "transparency": "transparent",
        "extendedProperties": {"private": {_MARKER_PROP: _MARKER_VALUE, _KEY_PROP: key}},
    }


def _needs_update(existing: dict, desired: dict) -> bool:
    return (
        existing.get("summary") != desired["summary"]
        or (existing.get("description") or "") != desired["description"]
        or existing.get("start", {}).get("date") != desired["start"]["date"]
        or existing.get("end", {}).get("date") != desired["end"]["date"]
    )


def plan_diff(
    workouts: list[PlannedWorkout], existing_events: list[dict]
) -> tuple[list[dict], list[tuple[str, dict]], list[str], int]:
    """Diff desired state against the calendar.

    Returns (bodies to insert, (event_id, body) to patch, event_ids to delete,
    count unchanged). Marker-carrying events with a duplicate or missing key
    are deleted — they can only come from interrupted earlier syncs.
    """
    keys = stable_keys(workouts)
    desired = {keys[w.id]: event_body(w, keys[w.id]) for w in workouts}

    existing: dict[str, dict] = {}
    to_delete: list[str] = []
    for event in existing_events:
        key = event.get("extendedProperties", {}).get("private", {}).get(_KEY_PROP)
        if key and key not in existing:
            existing[key] = event
        else:
            to_delete.append(event["id"])

    to_insert: list[dict] = []
    to_patch: list[tuple[str, dict]] = []
    unchanged = 0
    for key, body in desired.items():
        if key not in existing:
            to_insert.append(body)
        elif _needs_update(existing[key], body):
            to_patch.append((existing[key]["id"], body))
        else:
            unchanged += 1
    to_delete.extend(event["id"] for key, event in existing.items() if key not in desired)
    return to_insert, to_patch, to_delete, unchanged


def client_from_config() -> GcalClient:
    calendar_id = config.gcal_calendar_id.strip()
    if not calendar_id:
        raise GcalError("FARTLEK_GCAL_CALENDAR_ID is not set")
    if not config.gcal_key_path.exists():
        raise GcalError(
            f"Service account key not found at {config.gcal_key_path} "
            "(set FARTLEK_GCAL_KEY_FILE to override)"
        )
    return GcalClient(calendar_id, config.gcal_key_path)


def sync_plan(client: GcalClient | None = None) -> dict:
    """Mirror all planned workouts into the configured Google calendar."""
    if client is None:
        client = client_from_config()
    existing_events = client.list_plan_events()
    with session_scope() as session:
        workouts = session.scalars(select(PlannedWorkout)).all()
        to_insert, to_patch, to_delete, unchanged = plan_diff(workouts, existing_events)
    for body in to_insert:
        client.insert(body)
    for event_id, body in to_patch:
        client.patch(event_id, body)
    for event_id in to_delete:
        client.delete(event_id)
    return {
        "status": "ok",
        "created": len(to_insert),
        "updated": len(to_patch),
        "deleted": len(to_delete),
        "unchanged": unchanged,
    }


def sync_quietly() -> None:
    try:
        result = sync_plan()
        logger.info("Google Calendar sync: %s", result)
    except Exception:
        logger.exception("Google Calendar sync failed")


def sync_in_background() -> None:
    """Fire-and-forget sync after a plan mutation. No-op unless configured."""
    if not config.gcal_enabled:
        return
    threading.Thread(target=sync_quietly, daemon=True).start()
