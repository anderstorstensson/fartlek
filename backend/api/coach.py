"""In-app coach: a headless Claude Code session driven from the browser.

Each user message spawns `claude -p … --output-format stream-json` in the repo
root, so the training-analysis instructions, CLAUDE.md, and the coach-advisor
agent all apply exactly as in a terminal session. Authentication is the CLI's
own login (subscription) — no Anthropic API key is involved.

Tool access is a whitelist tuned to what the coach methodology needs (local
API via curl, read-only SQLite, repo reads, the athlete profile file, the
review subagent). Anything else is denied by the CLI itself; headless mode has
no way to ask for permission interactively.

Security: this endpoint lets the browser run an agent with (whitelisted) shell
access. It refuses to operate unless the app is bound to localhost.
"""

import asyncio
import json
import logging
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
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
ALLOWED_TOOLS = [
    "Read",
    "Grep",
    "Glob",
    "Task",  # coach-advisor plan review (inherits these same rules)
    "TodoWrite",
    "Bash(curl:*)",  # the app's own API — how analyses/notes/plans are written
    "Bash(sqlite3:*)",  # read-only DB queries per the methodology
    "Bash(grep:*)",
    "Bash(make sync:*)",
    "Bash(make recompute:*)",
    "Write(data/athlete-profile.md)",
    "Edit(data/athlete-profile.md)",
]


# Keeps first turns from fumbling: the CLI only pulls in the full coaching
# instructions when a question triggers the skill.
_SYSTEM_HINT = (
    "You are the athlete's in-app coach, embedded in the Fartlek web app which is "
    "already running at http://127.0.0.1:8077 (do not try to start it). For any "
    "training question, follow docs/coach/training-analysis.md. Replies render as "
    "markdown in a chat bubble — keep them conversational and compact."
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


def _require_localhost() -> None:
    if config.host not in ("127.0.0.1", "localhost", "::1"):
        raise HTTPException(
            status_code=403,
            detail="The coach endpoint is disabled when the app is not bound to localhost.",
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


@router.get("/messages", response_model=list[CoachMessageOut])
def list_messages(
    limit: int = 200, session: Session = Depends(get_session)
) -> list[CoachMessageOut]:
    rows = session.scalars(
        select(CoachMessage).order_by(CoachMessage.id.desc()).limit(limit)
    ).all()
    return list(reversed(rows))


@router.post("/reset", response_model=dict)
def reset_conversation(session: Session = Depends(get_session)) -> dict:
    """Start over: clear the chat history and drop the CLI session."""
    session.execute(delete(CoachMessage))
    session.commit()
    _session_file().unlink(missing_ok=True)
    return {"reset": True}


@router.post("/messages")
async def send_message(payload: CoachMessageIn) -> StreamingResponse:
    _require_localhost()
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

        args = [
            "claude", "-p", text,
            "--output-format", "stream-json", "--verbose",
            "--append-system-prompt", _SYSTEM_HINT,
            "--allowedTools", *ALLOWED_TOOLS,
        ]
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
