# Fartlek

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React 18](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-WAL-003B57?logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)
![Data: 100% local](https://img.shields.io/badge/data-100%25%20local-e8590c)
![License: MIT](https://img.shields.io/badge/license-MIT-97ca00)

Local, self-hosted training log — Strava-style activity viewing plus
fitness/training-load analytics, synced automatically from Garmin Connect.
Named after the Swedish training method: *fart* (speed) + *lek* (play).

- **Backend**: FastAPI + SQLite (SQLAlchemy), Garmin sync via `garth`/`python-garminconnect`,
  FIT parsing with `fitdecode`, background auto-sync every 30 min (APScheduler).
- **Frontend**: React + Vite + TypeScript, Recharts, Leaflet. Served as static files by the
  backend — one process runs everything.
- **Metrics**: Banister TRIMP (HR) and rTSS (pace) load models, CTL/ATL/TSB fitness &
  freshness curves, HR zones, workout/interval detection, best efforts (400m → marathon).
- **Views**: dashboard, activity list with route thumbnails, Strava-style logbook,
  training-plan calendar, trends, personal records.
- **Claude Code integration**: `.claude/skills/training-analysis/` teaches Claude how to
  query the data, analyze sessions and trends, publish goal-oriented training plans into
  the calendar, and adjust them when life happens (missed workouts, illness, fatigue).

## Setup

Dependencies are defined in `pyproject.toml`.

```bash
# 1. Python deps (creates .venv/)
uv sync

# 2. Frontend build
cd frontend && npm install && cd ..
make build-frontend

# 3. Garmin authentication (one time; supports MFA, stores tokens in data/garth/)
make login

# 4. Backfill your full history, then start the app
make backfill
make serve            # → http://127.0.0.1:8077
```

> **Repo on a filesystem without symlink support (e.g. exFAT)?** Put the venv
> elsewhere — `UV_PROJECT_ENVIRONMENT=~/.venvs/fartlek uv sync` — and run npm with
> `--no-bin-links`. The Makefile falls back to `~/.venvs/fartlek` automatically when
> there is no in-repo `.venv` (override with `make VENV=/path/to/venv <target>`).

## Autostart at login

```bash
make install-service          # systemd user unit, enabled + started
journalctl --user -u fartlek -f
```

The service auto-syncs from Garmin every 30 minutes while running.
Optional `sudo loginctl enable-linger $USER` keeps it running without an open session.

## Everyday commands

| Command | Purpose |
|---|---|
| `make sync` | Incremental Garmin sync now |
| `make backfill` | Re-scan complete Garmin history |
| `make recompute` | Recompute TRIMP/rTSS after changing athlete settings |
| `make rescan` | Re-detect workout flags from stored FIT files |
| `make test` | Backend test suite |
| `make dev` | Frontend dev server with hot reload (proxies API to :8077) |
| `make typecheck` | Frontend type checking |

## Training plans

Plans live in the app, not in documents. Ask Claude Code (in this project) for a plan —
e.g. *"build me a plan for a sub-40 10K on October 18"* — and after your approval it is
published to the **Calendar** page via `POST /api/plan`. Planned workouts appear as
dashed chips next to completed activities; a run on a planned day automatically marks
the workout done and links to it. Adjustments go the same way: tell Claude you were
sick or missed a session, approve its proposal, and it edits the calendar through the
plan API (`GET/POST/PUT/DELETE /api/plan…`). Plans can also be deleted from the
Calendar page directly.

## Configuration

Environment variables (prefix `FARTLEK_`): `FARTLEK_PORT` (8077), `FARTLEK_HOST`,
`FARTLEK_DATA_DIR`, `FARTLEK_SYNC_INTERVAL_MINUTES` (30), `FARTLEK_SCHEDULER_ENABLED`,
`FARTLEK_STREAM_MAX_POINTS` (3000, per-activity stream resolution in the DB).
Athlete parameters (max/resting HR, LTHR, threshold pace) are edited in the web UI
under Settings; saving triggers a metric recompute.

**Security model**: the API has no authentication — it serves your complete GPS and
health history to anyone who can reach it. The default bind to `127.0.0.1` is the
protection; keep it there, or put the app behind a reverse proxy with auth before
setting `FARTLEK_HOST` to anything wider.

## Data layout

```
data/
  fartlek.sqlite3  # all activities, laps, streams, best efforts, planned workouts
  fit/             # raw FIT files as downloaded from Garmin
  garth/           # Garmin OAuth tokens (no password stored)
```

`data/` is gitignored — it holds your Garmin tokens and full GPS/health history.
Never commit it.

## License

[MIT](LICENSE)
