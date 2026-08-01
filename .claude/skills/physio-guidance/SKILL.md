---
name: physio-guidance
description: Guide the athlete through niggles, pain, and injuries — triage, red-flag referral, load modification, and return-to-running. Use whenever the user reports something hurting, asks about an injury or niggle, asks whether they should run through something, or wants injury-prevention advice.
---

# Physio guidance

The full instructions live in **`docs/coach/physio-guidance.md`** (repo root) —
the single source of truth shared with other agent platforms via `AGENTS.md`.
**Read that file now and follow it.**

Claude Code specifics on top of it:

- Its §2 (red flags) is a hard boundary: when one applies, stop coaching and refer.
  Do not produce or revise a training plan for that athlete until it is resolved.
- When a niggle forces a plan change, the revised plan goes through the normal review —
  spawn the `coach-advisor` agent (rubric item 11 covers injury-awareness) rather than
  self-reviewing.
- Keep any edits to the methodology in `docs/coach/`, and its evidence base in
  `docs/running-injury-review.md` — this wrapper carries no knowledge of its own.
