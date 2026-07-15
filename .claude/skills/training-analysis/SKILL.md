---
name: training-analysis
description: Analyze the user's training data from the local Fartlek database — individual sessions, long-term fitness/load trends, and goal-oriented training plan suggestions. Use whenever the user asks about their running/training data, how a workout went, fitness trends, or wants a training plan.
---

# Training data analysis

The Fartlek project stores the user's complete Garmin training history locally.
This skill explains where the data lives, what it means, and how to analyze it.

## Data access

Two options, prefer the API when the app is running (it reuses the app's own math):

1. **HTTP API** (app runs at `http://127.0.0.1:8077`, check with `curl -s http://127.0.0.1:8077/api/health`):
   - `GET /api/activities?limit=50&offset=0&sport=running&q=text` — paged summaries (newest first)
   - `GET /api/activities/{id}` — detail with laps and best efforts
   - `GET /api/activities/{id}/streams` — time/distance/HR/speed/altitude/lat/lng arrays + HR zones + time-in-zones
   - `GET /api/trends/fitness?model=trimp|rtss&days=365` — daily load, CTL, ATL, TSB
   - `GET /api/trends/weekly?weeks=52` — weekly distance/time/load/counts
   - `GET /api/records?top=3` — personal records per standard distance
   - `GET /api/stats/summary` — this week vs last week + current form
   - `GET /api/settings` — athlete parameters (max/resting HR, LTHR, threshold pace)

2. **SQLite directly** (works even when the app is down; DB uses WAL mode, open read-only):
   `sqlite3 "file:data/fartlek.sqlite3?mode=ro" "<query>"` from the project root.

### Schema (SQLite)

- `activities` — one row per activity: `id, name, sport, start_time_utc, start_time_local,
  elapsed_s, moving_s, distance_m, avg_hr, max_hr, avg_speed_mps, max_speed_mps, ascent_m,
  descent_m, calories, avg_cadence, trimp, rtss, hrtss, has_gps, has_fit`.
  Sport values are Garmin type keys (`running`, `trail_running`, `treadmill_running`,
  `cycling`, `strength_training`, …); "is a run" = sport LIKE '%running%'.
- `laps` — `activity_id, lap_index, start_offset_s, elapsed_s, distance_m, avg_hr, max_hr, avg_speed_mps`.
- `streams` — one row per activity, parallel JSON arrays (`time_s, distance_m, hr, speed_mps,
  altitude_m, cadence, lat, lng`), downsampled to ≤3000 points. Use SQLite `json_each` or
  fetch via the API. Raw full-resolution FIT files are in `data/fit/{activity_id}.fit`.
- `best_efforts` — fastest efforts per activity for 400m/1K/1 mile/5K/10K/half/marathon.
- `athlete_settings` — single row: `resting_hr, max_hr, lthr, threshold_pace_s_per_km, sex`.

Units are SI everywhere: meters, seconds, m/s. Pace min/km = (1000/speed_mps)/60.
Timestamps are naive; use `start_time_local` for day/week grouping.

## Load metrics — do not mix scales

- `trimp` — Banister TRIMP from HR (sample-level integration when streams exist).
- `rtss` — pace-based stress score, runs only: 1 h at threshold pace = 100.
- `hrtss` — HR-based TSS approximation (1 h at LTHR = 100); the fallback for
  non-running sports in the rTSS model.
- CTL (fitness) = 42-day exponentially weighted daily load; ATL (fatigue) = 7-day;
  TSB (form) = yesterday's CTL − ATL. Get these from `/api/trends/fitness` rather than
  recomputing. TRIMP-based and TSS-based numbers are different scales — compare within
  one model only.

## Analyzing a single session

1. Pull the activity detail and streams. Establish context: what was it (easy run,
   intervals, long run, race?) — infer from laps structure, pace variance, and name.
2. Splits and pacing: per-lap pace vs average; positive/negative split; for intervals,
   rep consistency (pace and HR per work rep).
3. Aerobic decoupling: compare pace:HR ratio of first vs second half of steady runs;
   >5% drift suggests the effort was above current aerobic fitness, heat, or dehydration.
4. Intensity distribution: time in HR zones vs the session's purpose (easy runs should be
   ~Z1–Z2; if not, flag it).
5. Compare with similar past sessions (same distance range/route/type) — is pace at a
   given HR improving?
6. Place it in context: TSB on the day (was the athlete fresh or fatigued?), contribution
   to the week's load.

## Analyzing long-term trends

- **Ramp rate**: CTL increase per week. Sustainable ≈ 3–5 points/week; >8 is injury risk.
- **Form (TSB)**: > +10 fresh (race-ready), −10…+10 neutral, −10…−25 productive training
  stress, < −30 overreaching risk.
- **ACWR proxy**: ATL/CTL ratio, roughly 0.8–1.3. Treat as a *soft* heuristic only —
  the ratio is statistically and conceptually flawed (review §8, §13); weight absolute
  ramp rate, consistency and monotony above it.
- **Consistency**: runs/week and weekly distance variance matter more than any single week.
- **Monotony**: many identical-load days with no hard/easy polarity is a warning sign.
- **Durability** (review §5): resistance to pace/HR decoupling late in long runs is a
  trainable "fourth determinant". Read it from aerobic-decoupling trends on long runs
  over months — improving decoupling at a given duration = growing resilience.
- **Progress signals**: pace at fixed HR over months, PR trajectory from `best_efforts`,
  weekly distance trend from `/api/trends/weekly`.

## The athlete profile (required before any plan)

A tailored plan requires knowing the athlete, not just their data. The profile lives at
`data/athlete-profile.md` (gitignored — personal data).

- **Before creating or revising a plan, read this file.** If it doesn't exist, conduct
  the interview below and write it. If it exists, confirm it's current ("still true that
  you can train 6 days/week and the long run is Sunday?") and update what changed.
- **Never ask what the database already answers** (weekly volume, fitness trend, PRs,
  pace-at-HR, workout frequency — derive those). Interview only for what data can't show:
  1. Goal: race, distance, date, target time — and a secondary goal if any.
  2. Training availability: days/week, time per day, which day fits the long run,
     access to track/hills/treadmill.
  3. Injury history and current niggles; what has broken them before.
  4. Training history: years of consistent running, highest sustained weekly volume,
     what type of training they've responded well/poorly to.
  5. Life load: sleep quality, work/family stress, other sports.
  6. Age and anything affecting recovery (illness, medication).
  7. Preferences that affect adherence (loves/hates intervals, group runs, doubles).
- Keep the file short and factual; date-stamp updates. Record plan-relevant conclusions
  from check-ins there too ("responds badly to back-to-back quality days").

## Scientific basis — consult the literature review

The repo carries a curated, cited evidence synthesis at
`docs/endurance-training-science-review.md`. It is the authoritative source for the
principles behind plan design — prefer it over general knowledge, and cite it when
explaining choices to the athlete.

- **Read it (at least the relevant sections) before generating or substantially revising
  a plan.** Section 12 is an "app-element → best-supported principle → refs" map; section
  13 lists where the evidence has moved. Pull specific sections by grepping the headings
  (`grep -nE "^#{1,3} " docs/endurance-training-science-review.md`).
- When you justify an emphasis or session design to the athlete, ground it in the review
  (e.g. "sub-threshold controlled intervals rather than all-out tempo, per the review's
  §3 on the Norwegian method") rather than asserting it.
- The guidance below reflects the review's current conclusions; where a specific number
  or distribution matters, verify against the review rather than this summary, since the
  review is versioned and may be updated.

## Suggesting a training plan

Plans are built from the athlete's data + profile, never from generic templates.

1. **Baseline from data**: current CTL and 4–6-week median volume, longest recent run,
   threshold pace estimate (recent best efforts + Riegel exponent 1.06), pace-at-HR
   trend. State these numbers to the user as the plan's foundation.
2. **Demand analysis — what does the goal require?** Compare the race's demand profile
   against the athlete's current state and name the gaps. Race demands, roughly:
   5K ≈ VO2max + speed; 10K ≈ VO2max + threshold; half ≈ threshold + endurance;
   marathon ≈ endurance + threshold + fueling. The plan's emphasis must follow the gap
   analysis (e.g. threshold pace already sufficient for the 10K goal but CTL low →
   endurance-heavy plan), and the plan must say so explicitly.
3. **Every session names its target system.** No session goes in the plan without a
   stated physiological purpose: `endurance` (Z1–Z2 aerobic base, also builds durability
   via long runs + late-run quality — review §5), `threshold` (LT2; prefer controlled,
   interval-based *sub-threshold* / lactate-guided work over all-out tempo — review §3),
   `vo2max` (3–5 min reps at ~3–5K effort, ~1:1 recovery; anchor to critical speed if
   data allow — review §4), `speed` (short neuromuscular reps/strides, full recovery),
   `race-specific` (goal-pace work), `recovery`.
   - **Intensity distribution**: ~80% easy / 20% hard by time is the firm part. The
     *arrangement* of the hard 20% is phase- and level-dependent, not fixed: **pyramidal**
     (substantial threshold) is at least as good as **polarized** for most athletes and
     base/build phases; reserve polarization as a peaking tool (review §2, §13). Don't
     default to "polarized" — justify the choice from phase and athlete level.
   - Typically max 2 quality sessions + 1 long run per week, never hard days back-to-back.
   - **Standing strength element**: include ~2×/week heavy-resistance + plyometric work
     as `cross` sessions — among the best-evidenced, load-free economy gains (review §6).
4. **Training paces from the athlete's numbers** (not tables): easy ≈ threshold pace
   +25–35%, marathon pace ≈ +8–12%, threshold ≈ 100%, VO2max reps ≈ −8–10%, all
   cross-checked against actual recent performances and the athlete's zones.
5. **Progression and safety rails**: volume growth ≤10%/week, down week every 4th
   (~70%), long run ≤30–35% of weekly volume, CTL ramp ≤5/week, intensity volume grows
   before intensity density. Periodize base → build (race-specific emphasis grows) →
   peak → taper (2–3 weeks, volume −40–60%, keep intensity frequency — maintain fitness,
   shed fatigue).
6. **Independent review before the athlete sees it**: spawn the `coach-advisor` agent
   (defined in `.claude/agents/coach-advisor.md`) with the draft plan, the baseline
   numbers, and the goal. It verifies the numbers against the database itself and
   returns a verdict with severity-ranked findings. Fix CRITICAL and HIGH findings and
   re-submit to the advisor until it approves (max 2 iterations — then present with the
   remaining disagreements stated openly). Mention in the presentation that the plan
   passed independent review and what it flagged. Do the same for major revisions
   (regenerated remainder, changed race date) — not for 1–2 workout tweaks.
7. **Present before publishing**: week-by-week table (target km, key sessions with
   paces and their target system, weekly intent), the reasoning ("weeks 1–4 build
   aerobic base because X; threshold block starts week 5 because Y"), stated
   assumptions, and what would trigger a revision. Publish to the calendar only after
   the user approves.
8. Re-analyze against execution after 2–3 weeks (see adjustment section) and update
   both the plan and the athlete profile with what was learned.

## Publishing a training plan into the app

The app has a Calendar page that displays planned workouts next to completed runs
(a run on the same local date automatically marks the workout ✓). After the user
approves a plan, publish it:

```bash
curl -s -X POST http://127.0.0.1:8077/api/plan \
  -H 'Content-Type: application/json' \
  -d '{
    "replace_plan": true,
    "workouts": [
      {"day": "2026-07-20", "title": "Easy 8K", "workout_type": "easy",
       "target_distance_m": 8000,
       "description": "[endurance] Conversational pace, 5:30-5:50 /km, HR Z2",
       "plan_name": "sub-40 10K — Oct 18"},
      {"day": "2026-07-22", "title": "6 × 800m @ 3:55/km", "workout_type": "intervals",
       "description": "[vo2max] 2K warmup, 6x800 w/ 90s jog rest, 2K cooldown",
       "plan_name": "sub-40 10K — Oct 18"},
      {"day": "2026-07-24", "title": "Rest", "workout_type": "rest",
       "plan_name": "sub-40 10K — Oct 18"}
    ]
  }'
```

Rules:
- `workout_type` ∈ easy | long | intervals | tempo | race | rest | cross.
- `description` starts with the session's target system in brackets —
  `[endurance]`, `[threshold]`, `[vo2max]`, `[speed]`, `[race-specific]`, `[recovery]` —
  followed by the concrete prescription (paces/HR, structure). This is mandatory:
  it shows in the calendar tooltip and is how planned intent is audited against
  execution later.
- Use one consistent `plan_name` (include the goal + race date) for the whole plan;
  `replace_plan: true` replaces any previous version of that plan atomically.
- Put paces and structure in `description` — it shows in the calendar tooltip.
- One workout per day unless the plan really has doubles.
- Always show the plan to the user and get their approval BEFORE publishing.
- To revise later: regenerate the full plan and re-POST with `replace_plan: true`;
  to remove: `DELETE /api/plan?plan_name=<name>`. Existing plans: `GET /api/plan/plans`.
- When analyzing execution, compare planned vs actual via `GET /api/plan?start=…&end=…`
  (`completed_activity_id` links to the run) — useful for weekly plan check-ins.

## Adjusting an existing plan (missed workouts, illness, fatigue)

The plan is a living document. When the user reports a missed session, illness,
unusual fatigue, or a schedule conflict:

1. Read the current state: `GET /api/plan?start=<a week ago>&end=<plan end>` plus the
   recent fitness trend (`/api/trends/fitness`) — check TSB before prescribing more load.
2. Decide the adjustment using these defaults:
   - **One missed easy run**: just drop it. Never cram it into the following days.
   - **Missed key session** (intervals/tempo/long): shift it 1–2 days if the week has
     room, otherwise drop it — protect the spacing (no hard sessions on consecutive
     days, long run keeps its recovery buffer).
   - **Illness, no fever** (head cold): easy running only, no intensity until symptoms
     clear; convert planned key sessions that week to easy or rest.
   - **Fever or below-neck symptoms**: full rest. On return: easy running at reduced
     volume for as many days as the illness lasted, then one transition week at
     ~70–80% volume with one moderate session before resuming the plan. If more than
     ~10 days were lost, regenerate the remaining plan from a lower starting point
     rather than patching it.
   - **Persistent fatigue / TSB deeply negative + user reports feeling flat**: insert
     a down week (~60–70% volume, no intensity), push the remaining plan out a week.
   - **Race date moved**: regenerate from the current date with the new taper.
3. Apply mechanically:
   - Edit one workout: `PUT /api/plan/workouts/{id}` (full object; get ids from GET).
   - Remove one: `DELETE /api/plan/workouts/{id}`.
   - Add extras: `POST /api/plan` with `replace_plan: false`.
   - Restructure weeks or regenerate the remainder: re-POST the full plan with
     `replace_plan: true` — cleanest for anything beyond 1–2 workout tweaks. Keep
     past weeks' workouts in the payload so history stays visible in the calendar.
4. As with new plans: present the proposed changes and get the user's approval
   BEFORE writing, and summarize what changed afterwards (e.g. "moved Thursday's
   intervals to Friday, dropped Sunday's long run to 14 km").
5. Record durable lessons in `data/athlete-profile.md` (e.g. "third cold this
   winter during high-volume block — cap ramp rate lower"), so the next plan
   starts smarter.

## Housekeeping commands

- `make sync` — pull latest activities from Garmin now
- `make recompute` — refresh metrics after changing athlete settings
- App/service: `systemctl --user status fartlek`, logs via `journalctl --user -u fartlek`
