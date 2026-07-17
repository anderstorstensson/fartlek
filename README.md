# Fartlek

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React 18](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-WAL-003B57?logo=sqlite&logoColor=white)
[![CI](https://github.com/anderstorstensson/fartlek/actions/workflows/ci.yml/badge.svg)](https://github.com/anderstorstensson/fartlek/actions/workflows/ci.yml)
![Data: 100% local](https://img.shields.io/badge/data-100%25%20local-e8590c)
![License: MIT](https://img.shields.io/badge/license-MIT-97ca00)

Local, self-hosted training log — Strava-style activity viewing plus
fitness/training-load analytics, synced automatically from Garmin Connect.
Named after the Swedish training method: *fart* (speed) + *lek* (play).

- **Backend**: FastAPI + SQLite (SQLAlchemy), Garmin sync via `garth`/`python-garminconnect`,
  FIT parsing with `fitdecode`, background auto-sync every 30 min (APScheduler).
- **Frontend**: React + Vite + TypeScript, Recharts, Leaflet. Served as static files by the
  backend — one process runs everything.
- **Metrics**: Banister TRIMP (HR) and rTSS (grade-adjusted pace) load models, CTL/ATL/TSB
  fitness & freshness curves (with plan-based projection to race day), HR zones + weekly
  intensity distribution, grade-adjusted pace (Minetti), aerobic decoupling & efficiency
  index trends, running dynamics/power/respiration, workout/interval detection,
  relative effort (each session's TRIMP ranked against your trailing 90 days), best
  efforts (400m → marathon), Riegel race predictions.
- **Wellness & context**: daily Garmin wellness sync (sleep, overnight HRV, resting HR,
  body battery, stress, VO2 max) with a readiness flag on the dashboard; the watch's
  post-run self-evaluation (RPE + feel) per activity; historical weather per activity
  (Open-Meteo).
- **Views**: dashboard (incl. readiness + race countdown), activity list with route
  thumbnails, activity detail with map, streams, splits chart + table (per-split GAP)
  and relative effort, Strava-style logbook, training-plan calendar, trends, personal
  records, goal races.
- **AI-coach integration**: the coaching instructions live in `docs/coach/` (data
  access, analysis methodology, plan design + independent review) and are platform
  neutral — Claude Code loads them via `.claude/skills/`, any other agent platform
  (Codex, Cursor, …) picks them up through `AGENTS.md`. The AI can query the data,
  analyze sessions/races/trends, publish goal-oriented training plans into the
  calendar, and adjust them when life happens (missed workouts, illness, fatigue).

## Setup

Dependencies are defined in `pyproject.toml`. Works on Linux, macOS, and Windows
(CI runs the test suite on all three). `make` is a convenience wrapper — every
target is also a plain command, shown below for Windows.

**Linux / macOS**

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

**Windows (PowerShell, no make needed)**

```powershell
uv sync                                   # 1. Python deps
cd frontend; npm install; npm run build; cd ..   # 2. Frontend build
.venv\Scripts\python -m backend.cli login        # 3. Garmin auth
.venv\Scripts\python -m backend.cli sync --full  # 4. Backfill
.venv\Scripts\python -m backend.cli serve        #    → http://127.0.0.1:8077
```

> **Repo on a filesystem without symlink support (e.g. exFAT)?** Put the venv
> elsewhere — `UV_PROJECT_ENVIRONMENT=~/.venvs/fartlek uv sync` — and run npm with
> `--no-bin-links`. The Makefile falls back to `~/.venvs/fartlek` automatically when
> there is no in-repo `.venv` (override with `make VENV=/path/to/venv <target>`).

## Autostart at login

- **Linux**: `make install-service` — systemd user unit, enabled + started; logs
  via `journalctl --user -u fartlek -f`. Optional `sudo loginctl enable-linger $USER`
  keeps it running without an open session.
- **macOS**: `make install-service` — launchd user agent
  (`~/Library/LaunchAgents/com.fartlek.app.plist`); logs in `~/Library/Logs/fartlek.log`.
- **Windows**: `.\scripts\install-service.ps1` — Scheduled Task started at logon.

The service auto-syncs from Garmin every 30 minutes while running.

## Backups

The database holds things Garmin cannot restore (analysis notes, races, plans,
wellness history, your settings), so back it up. `make backup` (or
`python -m backend.cli backup`) writes a consistent, gzipped DB snapshot plus the
athlete profile to `data/backups/` (rotated, 7 kept). To get them **off the
machine**, install [rclone](https://rclone.org), configure a remote once, and set
one environment variable:

```bash
rclone config                    # one-time: create a "gdrive" Google Drive remote
export FARTLEK_RCLONE_REMOTE=gdrive:fartlek
make backup                      # snapshot + upload
```

With the variable set on the service (see the commented line in
`systemd/fartlek.service` / the launchd plist), a backup runs **automatically
every night at 03:30**. What goes to the remote:

- `snapshots/` — the rotated DB snapshots (mirrored)
- `fit/` — raw FIT files; append-only, so after the one-time ~1 GB seed upload
  only new activities transfer. Skippable with `FARTLEK_BACKUP_INCLUDE_FIT=0`:
  they are re-downloadable from Garmin (`make backfill`), so this is insurance
  against losing the Garmin account itself, at a slow rate-limited re-fetch.
- `athlete-profile.md`
- Garmin tokens (`garth/`) only with `FARTLEK_BACKUP_INCLUDE_TOKENS=1` — they
  grant access to your Garmin account, so leave them out of plain-text remotes
  (after a restore, just run `make login` again).

**Encryption (optional):** back up through an [rclone crypt
remote](https://rclone.org/crypt/) — wrap the Drive remote in a crypt remote and
point `FARTLEK_RCLONE_REMOTE` at that instead; Google then only ever sees
ciphertext. Recommended if you enable token backup.

**Restore:** download the newest snapshot, `gunzip` it to `data/fartlek.sqlite3`,
copy the FIT files back to `data/fit/`, restore `athlete-profile.md`, run
`make login`, done.

## Everyday commands

| Command | Purpose |
|---|---|
| `make sync` | Incremental Garmin sync now (activities + wellness + weather) |
| `make backfill` | Re-scan complete Garmin history |
| `make recompute` | Recompute TRIMP/rTSS after changing athlete settings |
| `make rescan` | Re-extract streams/dynamics/derived metrics from stored FIT files |
| `make wellness` | Backfill Garmin wellness (sleep/HRV/RHR) history |
| `make self-eval` | Backfill watch self-evaluations (RPE/feel) for past activities |
| `make vo2max` | Backfill daily VO2 max history from Garmin |
| `make weather` | Backfill historical weather for activities missing it |
| `make backup` | DB snapshot + rclone upload (see Backups) |
| `make test` | Backend test suite |
| `make dev` | Frontend dev server with hot reload (proxies API to :8077) |
| `make typecheck` | Frontend type checking |

## The Coach tab (in-app Claude Code)

The **Coach** page runs a headless [Claude Code](https://claude.com/claude-code)
session inside the app — same skills, same data access, same coaching
methodology as a terminal session, but as a chat in the browser. Requirements:
the Claude Code CLI installed and logged in on the machine running Fartlek
(uses your Claude subscription, not an API key).

> [!WARNING]
> **The Coach runs an AI agent with shell access on your machine, so it ships
> disabled.** Enable it deliberately with `FARTLEK_COACH_ENABLED=1`, and only when
> the app is bound to `127.0.0.1`. The agent also reads your synced data
> (activity names, notes, the athlete profile) into its context, so treat it as
> exposed to *prompt injection*: content in that data could try to steer it. The
> tool whitelist below limits the blast radius — it does not guarantee the agent
> can't be nudged — so don't enable the Coach on a machine bound to a wider
> interface or fed data you don't trust.

- **Off by default.** Set `FARTLEK_COACH_ENABLED=1` to turn it on; without it the
  Coach tab shows a disabled notice and the endpoint refuses.
- Tool access is a **whitelist** that fails closed: repo reads, the app's own
  loopback API via `scripts/api` (origin pinned to `127.0.0.1` in code),
  **read-only** SQL via `scripts/db` (`mode=ro` + `query_only` — writes fail at
  the SQLite level), and writes limited to `data/athlete-profile.md`. No blanket
  shell, no curl, no arbitrary network, and no subagents (`Task`) — a subagent
  would run with its own broader permissions and escape the whitelist.
- Two guards on top of the localhost bind: the endpoint refuses unless the app
  is bound to localhost (`config.host`), **and** each request's `Host` header
  must be loopback, so a rebound DNS name on another site can't drive the agent.
- Conversations persist (resumable session + chat history in the DB);
  "New conversation" resets both. Activity and Trends pages link straight into
  the Coach with pre-filled prompts ("analyze this session", "review my trends").
- **Model choice** (Settings → Coach model): routine session analyses follow a
  prescriptive methodology (`docs/coach/`), so a fast/economical model handles
  them well and saves subscription quota. Save the most capable model for
  judgment-heavy work — race debriefs and especially training plans. Plans are
  best built in a *terminal* Claude Code session rather than the Coach tab: the
  in-app coach cannot spawn the independent plan-review subagent (its tool
  whitelist forbids it), so only terminal sessions get the adversarial review.

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
`FARTLEK_STREAM_MAX_POINTS` (3000, per-activity stream resolution in the DB),
`FARTLEK_RCLONE_REMOTE` (backup destination, empty = off), `FARTLEK_BACKUP_KEEP` (7),
`FARTLEK_BACKUP_HOUR` (3), `FARTLEK_BACKUP_INCLUDE_FIT` (1),
`FARTLEK_BACKUP_INCLUDE_TOKENS` (0), `FARTLEK_COACH_ENABLED` (0 — the in-app Coach
agent, off by default; see [The Coach tab](#the-coach-tab-in-app-claude-code)).
Athlete parameters (max/resting HR, LTHR, threshold pace) are edited in the web UI
under Settings; saving triggers a metric recompute. Display preferences — metric or
imperial units and date/time format — live there too.

**Privacy note**: all data stays local except weather enrichment, which sends each
outdoor activity's *rounded* start coordinates and date to the free Open-Meteo API
(no key, no account). Remove the `weather` step from sync if that trade-off isn't
acceptable.

**Security model**: the API has no authentication — it serves your complete GPS and
health history to anyone who can reach it, and (when `FARTLEK_COACH_ENABLED=1`) exposes
an AI agent with whitelisted shell access. The default bind to `127.0.0.1` is the
protection; keep it there. Do **not** set `FARTLEK_HOST` to a wider interface without
putting authentication in front of the app, and leave the Coach disabled if you do —
its localhost and `Host`-header guards assume a single trusted local user.

## Data layout

```
data/
  fartlek.sqlite3  # all activities, laps, streams, best efforts, planned workouts
  fit/             # raw FIT files as downloaded from Garmin
  garth/           # Garmin OAuth tokens (no password stored)
```

`data/` is gitignored — it holds your Garmin tokens and full GPS/health history.
Never commit it.

## Acknowledgments

This project was developed in close collaboration with
[Claude Code](https://claude.com/claude-code): the analytics engine (training
load, GAP, decoupling, spike filtering), the Garmin/wellness/weather sync, the
frontend, the backup and cross-platform tooling, and the AI-coach integration
itself were built in pair-programming sessions with Claude — the same assistant
that now serves as the in-app coach through the Coach tab and the instructions
in `docs/coach/`.

## License

[MIT](LICENSE)
