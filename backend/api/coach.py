"""In-app coach: a headless Claude Code session driven from the browser.

Each user message spawns `claude -p … --output-format stream-json` in the repo
root, so the training-analysis instructions, CLAUDE.md, and the coach-advisor
agent all apply exactly as in a terminal session. Authentication is the CLI's
own login (subscription) — no Anthropic API key is involved.

Tool access is a whitelist tuned to what the coach methodology needs: repo
reads, the app's own loopback API via scripts/api, read-only SQL via scripts/db,
and writes to the athlete profile file only. It grants no subagents (Task) — a
subagent runs with its own, broader tool permissions and would escape this
whitelist. Anything else is denied by the CLI itself; headless mode has no way
to ask interactively.

Security: this endpoint lets the browser run an agent with (whitelisted) shell
access, so it is gated three ways. It is off unless FARTLEK_COACH_ENABLED is set
(config.coach_enabled); it refuses to operate unless the app is bound to
localhost (config.host); and every request's Host header must be loopback — so a
rebound DNS name on some other site the user is visiting cannot reach in and
drive the agent (the JSON preflight blocks classic CSRF; this blocks the
rebinding path the preflight can't).

Even so, the agent reads synced data (activity names, notes, the athlete
profile) into its context, so treat it as exposed to prompt injection: the
whitelist is the blast-radius limit, not a guarantee the agent won't be steered.
"""

import asyncio
import json
import logging
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from backend.config import BASE_DIR, config
from backend.db import get_session, session_scope
from backend.models import CoachMessage
from backend.schemas import CoachMessageIn, CoachMessageOut

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/coach", tags=["coach"])

_turn_lock = asyncio.Lock()
_STREAM_LIMIT = 10 * 1024 * 1024  # stream-json lines can carry whole messages
_TURN_TIMEOUT_S = 15 * 60

# What the coach may do without asking (headless mode cannot ask).
#
# No `Task`: a spawned subagent runs with its own tool grants (coach-advisor,
# for one, has unrestricted Bash), which would escape everything below — so the
# in-app coach reasons on its own and never delegates.
#
# Data access goes through two repo scripts instead of raw curl/sqlite3: the
# CLI's Bash allow rules are prefix matches that break on colons, so a rule
# containing a URL (`Bash(curl http://127.0.0.1:8077/:*)`) silently never
# matches. scripts/api pins the origin to 127.0.0.1 in code, and scripts/db
# opens the DB read-only (mode=ro + query_only) — the constraint lives where
# the matcher can't lose it, and anything else is denied rather than widened.
ALLOWED_TOOLS = [
    "Read",
    "Grep",
    "Glob",
    "TodoWrite",
    "Bash(scripts/api:*)",  # loopback API only — how analyses/notes/plans are written
    "Bash(scripts/db:*)",  # read-only SQL per the methodology
    "Bash(python scripts/api:*)",  # Windows invocation of the same scripts
    "Bash(python scripts/db:*)",
    "Bash(grep:*)",
    "Bash(make sync:*)",
    "Bash(make recompute:*)",
    # Read-only glue so compound commands and JSON crunching don't get denied
    # (every segment of a pipe/&&-chain must match a rule). Deliberately absent:
    # python/awk/sed (arbitrary exec or file writes would escape the whitelist).
    "Bash(echo:*)",
    "Bash(jq:*)",
    "Bash(head:*)",
    "Bash(tail:*)",
    "Bash(wc:*)",
    "Bash(sort:*)",
    "Bash(uniq:*)",
    "Bash(cut:*)",
    "Bash(tr:*)",
    "Bash(paste:*)",
    "Write(data/athlete-profile.md)",
    "Edit(data/athlete-profile.md)",
]


# Keeps first turns from fumbling: the CLI only pulls in the full coaching
# instructions when a question triggers the skill.
_SYSTEM_HINT = (
    "You are the athlete's in-app coach, embedded in the Fartlek web app which is "
    "already running at http://127.0.0.1:8077 (do not try to start it). For any "
    "training question, follow docs/coach/training-analysis.md. All data access goes "
    "through two repo scripts — other forms (curl, sqlite3, WebFetch) are blocked: "
    "`scripts/api GET|POST|PUT|DELETE /api/... ['<json>' | -]` for the app's API, and "
    "`scripts/db \"<sql>\"` for read-only SQL against data/fartlek.sqlite3. "
    "For number crunching, pipe into `jq` (allowed, and installed) or push the math "
    "into SQL — python/awk/sed and writing temp files are blocked and retrying them "
    "wastes turns. echo/head/tail/wc/sort/uniq/cut/tr are allowed as glue; every "
    "segment of a pipe or && chain must be an allowed tool or the whole command is "
    "denied. Replies render as markdown in a chat bubble — keep them conversational "
    "and compact."
)


def _session_file() -> Path:
    return config.data_dir / "coach-session.json"


def _load_session_id() -> str | None:
    try:
        return json.loads(_session_file().read_text()).get("session_id")
    except (OSError, ValueError):
        return None


def _store_session_id(session_id: str) -> None:
    _session_file().write_text(json.dumps({"session_id": session_id}))


def _require_coach_enabled() -> None:
    if not config.coach_enabled:
        raise HTTPException(
            status_code=403,
            detail="The Coach is off. Set FARTLEK_COACH_ENABLED=1 to enable it (localhost only).",
        )


def _require_localhost() -> None:
    if config.host not in ("127.0.0.1", "localhost", "::1"):
        raise HTTPException(
            status_code=403,
            detail="The coach endpoint is disabled when the app is not bound to localhost.",
        )


# Exact Host-header values we accept — loopback only, with and without the port.
_ALLOWED_HTTP_HOSTS = frozenset(
    {"127.0.0.1", "localhost", "[::1]"}
    | {f"{h}:{config.port}" for h in ("127.0.0.1", "localhost", "[::1]")}
)


def _require_local_host(request: Request) -> None:
    """Reject cross-origin driving of the agent (e.g. via DNS rebinding).

    A rebound hostname is same-origin to the attacker's page, so the JSON
    preflight won't stop it — but the request still carries that hostname in the
    Host header. Pinning Host to loopback closes the gap.
    """
    if (request.headers.get("host") or "").strip().lower() not in _ALLOWED_HTTP_HOSTS:
        raise HTTPException(
            status_code=403,
            detail="Coach requests must originate from localhost.",
        )


def _sse(event: dict) -> str:
    return f"data: {json.dumps(event)}\n\n"


def _summarize_tool(name: str, tool_input: dict) -> str:
    if name == "Bash":
        return str(tool_input.get("command", ""))[:160]
    if name in ("Read", "Write", "Edit"):
        return str(tool_input.get("file_path", ""))[:160]
    if name == "Task":
        return str(tool_input.get("description", ""))[:160]
    return json.dumps(tool_input)[:160]


def events_from_line(line: str) -> list[dict]:
    """Translate one stream-json line into UI events (pure, unit-tested)."""
    try:
        payload = json.loads(line)
    except ValueError:
        return []
    kind = payload.get("type")
    if kind == "assistant":
        events = []
        for block in (payload.get("message") or {}).get("content") or []:
            if block.get("type") == "text" and block.get("text"):
                events.append({"type": "text", "text": block["text"]})
            elif block.get("type") == "tool_use":
                events.append({
                    "type": "tool",
                    "name": block.get("name", "?"),
                    "summary": _summarize_tool(block.get("name", ""), block.get("input") or {}),
                })
        return events
    if kind == "result":
        return [{
            "type": "done",
            "session_id": payload.get("session_id"),
            "is_error": payload.get("subtype") != "success",
        }]
    return []


@router.get("/status", response_model=dict)
def coach_status() -> dict:
    """Whether the Coach is enabled and usable — lets the UI show a clear state."""
    return {
        "enabled": config.coach_enabled,
        "cli_available": shutil.which("claude") is not None,
    }


@router.get("/messages", response_model=list[CoachMessageOut])
def list_messages(
    request: Request, limit: int = 200, session: Session = Depends(get_session)
) -> list[CoachMessageOut]:
    _require_coach_enabled()
    _require_localhost()
    _require_local_host(request)
    rows = session.scalars(
        select(CoachMessage).order_by(CoachMessage.id.desc()).limit(limit)
    ).all()
    return list(reversed(rows))


@router.post("/reset", response_model=dict)
def reset_conversation(
    request: Request, session: Session = Depends(get_session)
) -> dict:
    """Start over: clear the chat history and drop the CLI session."""
    _require_coach_enabled()
    _require_localhost()
    _require_local_host(request)
    session.execute(delete(CoachMessage))
    session.commit()
    _session_file().unlink(missing_ok=True)
    return {"reset": True}


@router.post("/messages")
async def send_message(request: Request, payload: CoachMessageIn) -> StreamingResponse:
    _require_coach_enabled()
    _require_localhost()
    _require_local_host(request)
    if shutil.which("claude") is None:
        raise HTTPException(
            status_code=503,
            detail="Claude Code CLI not found on this machine — install it and run 'claude' once to log in.",
        )
    if _turn_lock.locked():
        raise HTTPException(status_code=409, detail="The coach is already working on a message.")

    return StreamingResponse(
        _stream_turn(payload.text),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


async def _stream_turn(text: str):
    async with _turn_lock:
        with session_scope() as db:
            db.add(CoachMessage(role="user", content=text, session_id=_load_session_id()))
            from backend.sync.service import get_or_create_settings

            coach_model = get_or_create_settings(db).coach_model.strip()

        args = [
            "claude", "-p", text,
            "--output-format", "stream-json", "--verbose",
            "--append-system-prompt", _SYSTEM_HINT,
            "--allowedTools", *ALLOWED_TOOLS,
        ]
        if coach_model:
            args += ["--model", coach_model]
        resume_id = _load_session_id()
        if resume_id:
            args += ["--resume", resume_id]

        process = await asyncio.create_subprocess_exec(
            *args,
            cwd=BASE_DIR,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=_STREAM_LIMIT,
        )

        assistant_parts: list[str] = []
        final_session: str | None = None
        try:
            async with asyncio.timeout(_TURN_TIMEOUT_S):
                while True:
                    line = await process.stdout.readline()
                    if not line:
                        break
                    for event in events_from_line(line.decode("utf-8", "replace")):
                        if event["type"] == "text":
                            assistant_parts.append(event["text"])
                        if event["type"] == "done" and event.get("session_id"):
                            final_session = event["session_id"]
                        yield _sse(event)
                await process.wait()
        except TimeoutError:
            process.kill()
            yield _sse({"type": "error", "message": "The coach timed out after 15 minutes."})
        except asyncio.CancelledError:
            process.kill()
            raise
        finally:
            if process.returncode is None:
                process.kill()

        if process.returncode not in (0, None):
            stderr = (await process.stderr.read()).decode("utf-8", "replace")[-500:]
            logger.error("coach turn failed (rc=%s): %s", process.returncode, stderr)
            yield _sse({"type": "error", "message": stderr.strip() or "Claude CLI failed."})

        content = "\n\n".join(part for part in assistant_parts if part.strip())
        if content:
            with session_scope() as db:
                db.add(CoachMessage(
                    role="assistant", content=content,
                    session_id=final_session or resume_id,
                ))
        if final_session:
            _store_session_id(final_session)
