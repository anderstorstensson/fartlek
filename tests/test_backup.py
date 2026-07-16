import gzip
import sqlite3

import pytest

from backend.sync import backup


@pytest.fixture()
def data_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(backup.config, "data_dir", tmp_path, raising=False)
    con = sqlite3.connect(tmp_path / "fartlek.sqlite3")
    con.execute("CREATE TABLE t (v TEXT)")
    con.execute("INSERT INTO t VALUES ('hello')")
    con.commit()
    con.close()
    return tmp_path


def _restore_and_read(snapshot_path, tmp_path):
    restored = tmp_path / "restored.sqlite3"
    with gzip.open(snapshot_path, "rb") as packed:
        restored.write_bytes(packed.read())
    con = sqlite3.connect(restored)
    try:
        return con.execute("SELECT v FROM t").fetchone()[0]
    finally:
        con.close()


def test_snapshot_roundtrip(data_dir):
    snapshot = backup.create_snapshot(keep=5)
    assert snapshot.exists()
    assert _restore_and_read(snapshot, data_dir) == "hello"


def test_rotation_keeps_newest(data_dir):
    made = [backup.create_snapshot(keep=3) for _ in range(5)]
    remaining = sorted(backup.backups_dir().glob("fartlek-*.sqlite3.gz"))
    assert len(remaining) <= 3
    assert made[-1] in remaining


def test_run_backup_without_remote_is_local_only(data_dir, monkeypatch):
    monkeypatch.setattr(backup.config, "rclone_remote", "", raising=False)
    result = backup.run_backup()
    assert result["uploaded"] is False
    assert backup.backups_dir().exists()


def test_run_backup_uploads_via_rclone(data_dir, monkeypatch):
    monkeypatch.setattr(backup.config, "rclone_remote", "gdrive:fartlek", raising=False)
    monkeypatch.setattr(backup.config, "backup_include_tokens", False, raising=False)
    monkeypatch.setattr(backup.shutil, "which", lambda _: "/usr/bin/rclone")
    (data_dir / "fit").mkdir()
    (data_dir / "athlete-profile.md").write_text("# profile")
    (data_dir / "garth").mkdir()

    calls = []
    monkeypatch.setattr(backup, "_rclone", lambda *args: calls.append(args))

    result = backup.run_backup()
    assert result["uploaded"] is True
    commands = [(c[0], c[-1]) for c in calls]
    assert ("sync", "gdrive:fartlek/snapshots") in commands
    assert ("copy", "gdrive:fartlek/fit") in commands
    assert ("copy", "gdrive:fartlek") in commands  # profile
    # tokens excluded by default
    assert not any(dest.endswith("/garth") for _, dest in commands)


def test_fit_skipped_when_opted_out(data_dir, monkeypatch):
    monkeypatch.setattr(backup.config, "rclone_remote", "gdrive:fartlek", raising=False)
    monkeypatch.setattr(backup.config, "backup_include_fit", False, raising=False)
    monkeypatch.setattr(backup.shutil, "which", lambda _: "/usr/bin/rclone")
    (data_dir / "fit").mkdir()

    calls = []
    monkeypatch.setattr(backup, "_rclone", lambda *args: calls.append(args))
    backup.run_backup()
    assert not any(c[-1].endswith("/fit") for c in calls)


def test_tokens_only_when_opted_in(data_dir, monkeypatch):
    monkeypatch.setattr(backup.config, "rclone_remote", "crypt:fartlek", raising=False)
    monkeypatch.setattr(backup.config, "backup_include_tokens", True, raising=False)
    monkeypatch.setattr(backup.shutil, "which", lambda _: "/usr/bin/rclone")
    (data_dir / "fit").mkdir()
    (data_dir / "garth").mkdir()

    calls = []
    monkeypatch.setattr(backup, "_rclone", lambda *args: calls.append(args))
    backup.run_backup()
    assert any(c[-1] == "crypt:fartlek/garth" for c in calls)


def test_missing_rclone_binary_errors(data_dir, monkeypatch):
    monkeypatch.setattr(backup.config, "rclone_remote", "gdrive:fartlek", raising=False)
    monkeypatch.setattr(backup.shutil, "which", lambda _: None)
    with pytest.raises(RuntimeError, match="rclone is not installed"):
        backup.run_backup()
