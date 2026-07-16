import json

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
