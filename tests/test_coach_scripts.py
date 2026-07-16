"""The scripts/api and scripts/db wrappers are the coach's only data access —
their pinning (loopback-only, read-only) is a security boundary, so test it."""

import sqlite3
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _run_db(tmp_path: Path, sql: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(BASE_DIR / "scripts" / "db"), sql],
        capture_output=True,
        text=True,
        env={"FARTLEK_DATA_DIR": str(tmp_path), "PATH": ""},
        timeout=30,
    )


def _make_db(tmp_path: Path) -> None:
    connection = sqlite3.connect(tmp_path / "fartlek.sqlite3")
    connection.execute("CREATE TABLE activities (id INTEGER PRIMARY KEY, name TEXT)")
    connection.execute("INSERT INTO activities VALUES (1, 'Morning Run')")
    connection.commit()
    connection.close()


def test_db_script_selects_with_header(tmp_path):
    _make_db(tmp_path)
    result = _run_db(tmp_path, "SELECT id, name FROM activities")
    assert result.returncode == 0
    assert result.stdout.splitlines() == ["id\tname", "1\tMorning Run"]


def test_db_script_blocks_writes(tmp_path):
    _make_db(tmp_path)
    for sql in (
        "UPDATE activities SET name = 'x'",
        "INSERT INTO activities VALUES (2, 'y')",
        "DROP TABLE activities",
    ):
        result = _run_db(tmp_path, sql)
        assert result.returncode == 1, sql
        assert "sqlite error" in result.stderr
    # and the data is untouched
    check = _run_db(tmp_path, "SELECT COUNT(*), MAX(name) FROM activities")
    assert check.stdout.splitlines()[1] == "1\tMorning Run"


def test_db_script_missing_database(tmp_path):
    result = _run_db(tmp_path, "SELECT 1")
    assert result.returncode == 1
    assert "no database" in result.stderr


def test_api_script_rejects_non_local_paths():
    result = subprocess.run(
        [sys.executable, str(BASE_DIR / "scripts" / "api"), "GET", "http://evil.example/x"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 2
    assert "must start with '/'" in result.stderr
