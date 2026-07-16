"""Command-line entry points.

  uv run python -m backend.cli login       # one-time Garmin authentication
  uv run python -m backend.cli sync        # incremental sync
  uv run python -m backend.cli sync --full # full backfill of all history
  uv run python -m backend.cli recompute   # recompute load metrics
  uv run python -m backend.cli serve       # run the web app
"""

import argparse
import getpass
import sys


def cmd_login() -> int:
    from backend.sync.garmin import interactive_login

    email = input("Garmin Connect email: ").strip()
    password = getpass.getpass("Garmin Connect password: ")
    try:
        interactive_login(email, password, lambda: input("MFA code: ").strip())
    except Exception as exc:
        print(f"Login failed: {exc}", file=sys.stderr)
        if "429" in str(exc):
            print(
                "Garmin is rate limiting this IP. Wait 15-60 minutes and try again "
                "(repeated attempts extend the block).",
                file=sys.stderr,
            )
        return 1
    print("Logged in. Tokens saved — the password is not stored.")
    print("Run 'uv run python -m backend.cli sync --full' to backfill your history.")
    return 0


def cmd_sync(full: bool) -> int:
    from backend.db import init_db
    from backend.sync.service import run_sync

    init_db()
    result = run_sync(full=full)
    print(result)
    return 0 if result.get("status") == "ok" else 1


def cmd_rescan() -> int:
    from backend.db import init_db
    from backend.sync.service import rescan_fit_flags

    init_db()
    count = rescan_fit_flags()
    print(f"Rescanned FIT files for {count} activities.")
    return 0


def cmd_recompute() -> int:
    from backend.db import init_db
    from backend.sync.service import recompute_all_metrics

    init_db()
    count = recompute_all_metrics()
    print(f"Recomputed metrics for {count} activities.")
    return 0


def cmd_rename_workouts() -> int:
    from backend.db import init_db
    from backend.sync.service import rename_workout_activities

    init_db()
    count = rename_workout_activities()
    print(f"Renamed {count} workout activities from their interval structure.")
    return 0


def cmd_weather(limit: int | None) -> int:
    from backend.db import init_db
    from backend.sync.weather import enrich_missing_weather

    init_db()
    count = enrich_missing_weather(limit=limit)
    print(f"Enriched weather for {count} activities.")
    return 0


def cmd_wellness(days: int) -> int:
    from backend.db import init_db
    from backend.sync.garmin import client_from_tokens
    from backend.sync.wellness import sync_wellness

    init_db()
    try:
        client = client_from_tokens()
    except Exception as exc:
        print(f"Garmin login required: {exc}", file=sys.stderr)
        return 1
    count = sync_wellness(client, backfill_days=days)
    print(f"Synced wellness for {count} days.")
    return 0


def cmd_backup() -> int:
    from backend.db import init_db
    from backend.sync.backup import run_backup

    init_db()
    try:
        result = run_backup()
    except Exception as exc:
        print(f"Backup failed: {exc}", file=sys.stderr)
        return 1
    print(f"Snapshot: {result['snapshot']}")
    print("Uploaded to remote." if result["uploaded"] else
          "No FARTLEK_RCLONE_REMOTE configured — local snapshot only.")
    return 0


def cmd_serve() -> int:
    import uvicorn

    from backend.config import config

    uvicorn.run("backend.main:app", host=config.host, port=config.port)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="fartlek")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("login", help="Authenticate with Garmin Connect")
    sync_parser = sub.add_parser("sync", help="Sync activities from Garmin")
    sync_parser.add_argument("--full", action="store_true", help="Backfill all history")
    sub.add_parser("recompute", help="Recompute load metrics for all activities")
    sub.add_parser(
        "rescan", help="Re-extract streams, dynamics and derived metrics from stored FIT files"
    )
    sub.add_parser("rename-workouts", help="Name interval runs after their structure")
    weather_parser = sub.add_parser("weather", help="Backfill weather for activities missing it")
    weather_parser.add_argument("--limit", type=int, default=None, help="Max activities to enrich")
    wellness_parser = sub.add_parser("wellness", help="Backfill Garmin wellness data")
    wellness_parser.add_argument("--days", type=int, default=365, help="Days back to fetch")
    sub.add_parser("backup", help="Snapshot the DB and upload via rclone (if configured)")
    sub.add_parser("serve", help="Run the web application")

    args = parser.parse_args()
    if args.command == "login":
        return cmd_login()
    if args.command == "sync":
        return cmd_sync(args.full)
    if args.command == "recompute":
        return cmd_recompute()
    if args.command == "rescan":
        return cmd_rescan()
    if args.command == "rename-workouts":
        return cmd_rename_workouts()
    if args.command == "weather":
        return cmd_weather(args.limit)
    if args.command == "wellness":
        return cmd_wellness(args.days)
    if args.command == "backup":
        return cmd_backup()
    return cmd_serve()


if __name__ == "__main__":
    sys.exit(main())
