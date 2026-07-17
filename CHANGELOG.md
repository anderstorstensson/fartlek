# Changelog

All notable changes to Fartlek are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-07-17

First public release. Fartlek is a local, self-hosted training log — Strava-style
activity viewing plus fitness/training-load analytics, synced automatically from
Garmin Connect and coachable by Claude Code. Everything runs in a single process
and all data stays on your machine.

### Sync & ingestion
- Automatic Garmin Connect sync via `garth` / `python-garminconnect`, with MFA-aware
  login that stores OAuth tokens locally (no password kept).
- Background auto-sync every 30 minutes (APScheduler); incremental `sync`, full
  `backfill`, and FIT-only `rescan` paths.
- FIT-file parsing (`fitdecode`) for streams, running dynamics, power and
  respiration; per-activity stream resolution is configurable
  (`FARTLEK_STREAM_MAX_POINTS`).
- Daily Garmin **wellness** sync — sleep, overnight HRV, resting HR, body battery,
  stress and VO2 max.
- The watch's post-run **self-evaluation** (RPE + feel) captured per activity.
- Historical **weather** per activity from the free Open-Meteo API (rounded
  coordinates only; removable if you'd rather send nothing).

### Metrics & analytics
- Banister **TRIMP** (HR) and **rTSS** (grade-adjusted pace) training-load models.
- **CTL / ATL / TSB** fitness, fatigue and freshness curves, with plan-based
  projection to race day.
- **HR zones** with a configurable basis (max HR, LTHR, or manual bounds) and
  weekly intensity distribution.
- **Grade-adjusted pace** (Minetti), aerobic **decoupling** and **efficiency
  index** trends.
- Workout / interval detection, **relative effort** (each session's TRIMP ranked
  against your trailing 90 days), **best efforts** (400 m → marathon) and
  **Riegel** race predictions.
- Running pace (s/km) served alongside every speed field; metric or imperial
  display units.

### Views (web UI)
- **Dashboard** with a readiness flag, next key workout tile, and race countdown.
- **Activity list** with route thumbnails; **activity detail** with map, streams,
  a splits chart and per-split GAP table, and relative effort.
- Strava-style **logbook**, **trends**, **personal records** and **goal races** pages.
- **Training-plan calendar**: planned workouts as dashed chips; a run on a planned
  day auto-marks the workout done and links to it. Type- and order-aware plan
  completion matching.
- Export training plans as **iCalendar** (`.ics`).
- Activity editing (including delete), analysis markers on Activities and Calendar,
  and connected activity tags across list, calendar and edit form.
- Date/time format and unit preferences in Settings; saving athlete parameters
  (max/resting HR, LTHR, threshold pace) triggers a metric recompute.

### AI coach integration
- Platform-neutral coaching instructions in `docs/coach/` (data access, analysis
  methodology, plan design + independent review). Claude Code loads them via
  `.claude/skills/`; other agents pick them up through `AGENTS.md`.
- Claude can query the data, analyze sessions/races/trends, publish goal-oriented
  training plans into the calendar (`POST /api/plan`) and adjust them when life
  happens (missed workouts, illness, fatigue).
- Session analyses are graded against the prescribed workout and stored in the app.
- Plan generation grounded in an endurance-training-science literature review
  (heat, recovery, monitoring), with a `coach-advisor` subagent for independent,
  adversarial plan review.
- **In-app Coach tab** — a headless Claude Code chat inside the app, sharing the
  same skills, data access and methodology as a terminal session. Ships **disabled**
  (`FARTLEK_COACH_ENABLED=1` to enable); guarded by a localhost bind check, a
  `Host`-header loopback check, and a fail-closed tool whitelist (repo reads, the
  app's own loopback API, read-only SQL, and writes limited to
  `data/athlete-profile.md`). Selectable Claude model; resumable conversations with
  persisted chat history; quick links from the Activity and Trends pages with
  pre-filled prompts.

### Backups & operations
- `backup` writes a consistent, gzipped DB snapshot plus the athlete profile to
  `data/backups/` (rotated, 7 kept), with optional off-machine upload via
  [rclone](https://rclone.org) and a nightly 03:30 automatic run.
- Configurable inclusion of raw FIT files (`FARTLEK_BACKUP_INCLUDE_FIT`) and Garmin
  tokens (`FARTLEK_BACKUP_INCLUDE_TOKENS`, off by default); works through an rclone
  crypt remote for end-to-end encryption.
- **Autostart at login** on Linux (systemd user unit), macOS (launchd agent) and
  Windows (Scheduled Task).

### Platform & tooling
- Runs on Linux, macOS and Windows; CI runs the backend test suite on all three
  and builds the frontend.
- FastAPI + SQLite (SQLAlchemy, WAL) backend serving a React + Vite + TypeScript
  frontend (Recharts, Leaflet) as static files — one process runs everything.
- `make` convenience wrapper over every command, with an exFAT / no-symlink venv
  fallback.

### Security & privacy
- No authentication by design; the default `127.0.0.1` bind is the protection —
  the API serves your complete GPS and health history to anyone who can reach it.
- All data stays local except optional weather enrichment (rounded coordinates to
  Open-Meteo). `data/` is gitignored.

[0.1.0]: https://github.com/anderstorstensson/fartlek/releases/tag/v0.1.0
