---
name: training-analysis
description: Analyze the user's training data from the local Fartlek database — individual sessions, long-term fitness/load trends, and goal-oriented training plan suggestions. Use whenever the user asks about their running/training data, how a workout went, fitness trends, or wants a training plan.
---

# Training data analysis

The full instructions live in **`docs/coach/training-analysis.md`** (repo root) —
the single source of truth shared with other agent platforms via `AGENTS.md`.
**Read that file now and follow it.**

Claude Code specifics on top of it:

- For the independent plan review step, spawn the `coach-advisor` agent (its
  definition points at `docs/coach/plan-review.md`) rather than self-reviewing.
- Keep any edits to the coaching methodology in `docs/coach/` — this wrapper and
  the agent wrapper carry no knowledge of their own.
