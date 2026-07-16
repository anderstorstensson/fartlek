import json
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from backend.api import coach


def test_events_from_assistant_line():
    line = json.dumps({
        "type": "assistant",
        "message": {"content": [
            {"type": "text", "text": "Looking at your run…"},
            {"type": "tool_use", "name": "Bash",
             "input": {"command": "curl -s http://127.0.0.1:8077/api/stats/summary"}},
        ]},
    })
    events = coach.events_from_line(line)
    assert events[0] == {"type": "text", "text": "Looking at your run…"}
    assert events[1]["type"] == "tool"
    assert events[1]["name"] == "Bash"
    assert "stats/summary" in events[1]["summary"]


def test_events_from_result_line():
    line = json.dumps({"type": "result", "subtype": "success", "session_id": "abc"})
    assert coach.events_from_line(line) == [
        {"type": "done", "session_id": "abc", "is_error": False}
    ]


def test_junk_lines_ignored():
    assert coach.events_from_line("not json") == []
    assert coach.events_from_line(json.dumps({"type": "system", "subtype": "init"})) == []


def test_whitelist_has_no_unrestricted_shell():
    # The whole point of the whitelist: no blanket Bash/Write/Edit.
    assert "Bash" not in coach.ALLOWED_TOOLS
    assert "Write" not in coach.ALLOWED_TOOLS
    assert "Edit" not in coach.ALLOWED_TOOLS
    assert "WebFetch" not in coach.ALLOWED_TOOLS


def test_whitelist_excludes_task_and_scopes_shell():
    # Task is barred: a subagent runs with its own broader tool grants and would
    # escape this whitelist. Data access goes through the repo's pinned scripts;
    # raw curl/sqlite3 rules are gone (colon-in-prefix rules never match anyway).
    assert "Task" not in coach.ALLOWED_TOOLS
    assert "Bash(scripts/api:*)" in coach.ALLOWED_TOOLS
    assert "Bash(scripts/db:*)" in coach.ALLOWED_TOOLS
    assert not any("curl" in t for t in coach.ALLOWED_TOOLS)
    assert not any("sqlite3" in t for t in coach.ALLOWED_TOOLS)
    # No allow rule may contain a colon in its prefix — the CLI matcher breaks
    # on it and the rule silently never matches (verified empirically).
    for tool in coach.ALLOWED_TOOLS:
        if tool.startswith("Bash(") and tool.endswith(":*)"):
            assert ":" not in tool[len("Bash("):-len(":*)")], tool


def test_coach_disabled_by_default(monkeypatch):
    # Ships off: the agent surface must be opt-in.
    assert coach.config.coach_enabled is False
    with pytest.raises(HTTPException) as exc:
        coach._require_coach_enabled()
    assert exc.value.status_code == 403
    monkeypatch.setattr(coach.config, "coach_enabled", True, raising=False)
    coach._require_coach_enabled()  # no raise once enabled


def _request(host: str) -> SimpleNamespace:
    return SimpleNamespace(headers={"host": host})


def test_local_host_guard_allows_loopback():
    coach._require_local_host(_request(f"127.0.0.1:{coach.config.port}"))
    coach._require_local_host(_request("localhost"))


def test_local_host_guard_rejects_foreign_host():
    # DNS rebinding lands here: the request still carries the attacker's hostname.
    for host in ("evil.example.com", "attacker.test", "fartlek.internal:8077"):
        with pytest.raises(HTTPException) as exc:
            coach._require_local_host(_request(host))
        assert exc.value.status_code == 403
