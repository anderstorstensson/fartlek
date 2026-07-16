# Agent instructions — Fartlek

Fartlek is a local, self-hosted training log: FastAPI + SQLite backend, React
frontend, synced from Garmin Connect. The user's complete GPS/health history
lives in `data/` (gitignored — never commit or exfiltrate it).

## Acting as the AI coach

If the user asks about their training — analyzing a run or race, fitness trends,
building or adjusting a training plan — **read and follow
`docs/coach/training-analysis.md`**. It documents the data (HTTP API + SQLite
schema), the analysis methodology, the plan-design protocol, and the coaching
tone setting. Draft training plans must pass the independent review in
`docs/coach/plan-review.md` before the athlete sees them (spawn a subagent for
it if your platform has them; otherwise self-review per that document).

The scientific basis for plan design is `docs/endurance-training-science-review.md`
— prefer it over general knowledge and cite its sections.

## Development

- Backend: Python 3.11+, FastAPI + SQLAlchemy + SQLite (WAL). Deps via `uv sync`
  (venv falls back to `~/.venvs/fartlek` on filesystems without symlinks).
- Frontend: React + Vite + TypeScript in `frontend/` (`npm ci`, `npm run
  typecheck`, `npm run build`).
- Tests: `pytest -q` from the repo root (or `make test`). Add tests for new
  backend behavior; the suite must pass before committing.
- Run the app: `python -m backend.cli serve` (or `make serve`) →
  http://127.0.0.1:8077. The API is unauthenticated — keep it bound to localhost.
- Commit style: conventional commits (`feat:`, `fix:`, `docs:`, …), imperative
  subject, body explaining what and why. No AI attribution trailers.

## Layout

- `backend/analysis/` — pure computation (training load, GAP, zones, spikes, …)
- `backend/sync/` — Garmin sync, FIT import, wellness, weather, scheduler
- `backend/api/` — FastAPI routers; `backend/models.py` + `backend/schemas.py`
- `frontend/src/pages/` + `frontend/src/components/`
- `.claude/` — Claude Code wrappers around `docs/coach/` (keep knowledge there,
  not in the wrappers)
