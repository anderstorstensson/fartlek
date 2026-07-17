---
title: "Current Concepts in Endurance Training Science for Running"
subtitle: "An evidence synthesis for building science-backed running plans"
author: "Fartlek project — literature review"
date: "2026-07-15"
---

# Current Concepts in Endurance Training Science for Running

**A scoping synthesis to inform science-backed running training plans**

## Executive summary

This review synthesises the current evidence on endurance training as it applies to
prescribing running plans. It is organised so that each concept is followed by the
**evidence** and its **implication for plan-building**, mapping directly onto the
training systems the Fartlek app already uses (`endurance`, `threshold`, `vo2max`,
`speed`, `race-specific`, `recovery`) and its load model (TRIMP / rTSS / CTL–ATL–TSB).

Headline conclusions:

- **A large majority of running volume should be low-intensity** (~80% by time). Whether
  the remaining hard work is arranged in a *polarised* (little threshold) or *pyramidal*
  (substantial threshold) pattern is **not settled**; real-world elite distance runners
  more often train pyramidally, and the best pattern appears to depend on athlete level and
  training phase.[^1][^2][^3][^4][^5]
- **The "Norwegian" double-threshold method** — high volume plus frequent *lactate-guided
  sub-threshold* interval sessions (blood lactate ~2–4.5 mmol·L⁻¹) — is the most influential
  current model in elite distance running, and formalises "controlled" threshold work.[^6][^7]
- **Durability / physiological resilience** — resistance to the decline of VO₂max, economy
  and thresholds late in prolonged exercise — is now treated as a **fourth performance
  determinant** beyond VO₂max, threshold and economy, and is trainable mainly through
  accumulated low-intensity volume and long runs.[^13][^14][^15][^16]
- **Running economy is trainable off the run**: heavy-resistance and plyometric strength
  training yield small-to-moderate economy gains, and **advanced footwear technology
  ("super shoes")** improves economy ~2–4% on road, worth roughly ~1% in marathon time.[^17][^18][^19][^20][^21][^22]
- **Tapering** works best as a **~2-week** progressive **volume** cut of **41–60%**, holding
  intensity and (largely) frequency.[^24][^25]
- **Interruptions cost less than athletes fear, and intensity is what defends against them.** VO₂max falls ~7%
  in three weeks off and the early loss is mostly **blood volume**, not "fitness"; capillarisation and much of
  the aerobic base persist for months. Fitness can be *maintained* for up to 15 weeks on as little as 2 sessions
  a week — **provided intensity is held** — which is the taper finding (cut volume, keep intensity) in a
  different costume.[^57][^59][^60]
- The app's **ACWR safety rail (0.8–1.3) rests on contested science**: the ratio has been
  shown to have serious statistical and conceptual flaws. It should be treated as a soft
  heuristic, with absolute weekly ramp and consistency given more weight.[^27][^28][^29]
- **Sleep is the cheapest lever the app already measures, and the sensor is weakest where it matters.** Consumer
  trackers detect sleep well (sensitivity ≥0.93) but detect *wake* poorly (specificity 0.18–0.54), assess stages
  inconsistently, and degrade on disrupted nights — so `deep_sleep_s` should not drive decisions. Meanwhile
  **subjective athlete report tracks training load better than the objective markers** and does not correlate
  with them, making the athlete's own voice the more sensitive channel rather than a courtesy.[^69][^71][^72]
- **Heat is the largest environmental modifier of running performance** and the app already
  stores the data to model it. Marathon times slow progressively as wet-bulb globe temperature
  rises from 5 → 25 °C, and **slower runners lose disproportionately more**.[^42] **Heat
  acclimation** (1–2 weeks of repeated exercise-heat exposure) reliably improves performance
  *in the heat*, decays at ~2.5%/day, and is re-induced 8–12× faster than it is lost.[^37][^39][^40]
  Whether heat training transfers to **cool-condition** performance — the "poor man's altitude"
  claim — is **not settled**.[^43][^44][^45][^46][^47]

---

## 1. Scope and method

**Objective.** Summarise the most current, defensible concepts in endurance training science
that bear on prescribing running plans, and state the practical implication of each for
automated plan generation.

**Type.** Narrative / scoping synthesis (not a PRISMA clinical meta-analysis), appropriate
for a mature applied field where the goal is usable concepts rather than a single pooled
effect estimate.

**Search.** Targeted per-theme web searches (July 2026) across scholarly sources, prioritising
recent high-citation systematic reviews and meta-analyses plus landmark primary papers.
Themes: intensity distribution; the Norwegian double-threshold method; interval prescription
(VO₂max, critical speed/power); durability; running economy (strength, plyometrics, footwear);
periodization and tapering; detraining, illness and the minimal maintenance dose; load monitoring
(including session-RPE) and the ACWR critique; HRV-guided training; sleep and readiness monitoring;
carbohydrate periodization and race fuelling; heat acclimation, environmental heat stress, cooling
and post-exercise immersion; the female endurance athlete and RED-S.

**Citation integrity.** Every reference's metadata (authors, year, journal, DOI) was retrieved
from CrossRef rather than reproduced from memory, and DOIs were verified to resolve. Author
concept-names were used only as search seeds. 74 references are cited; the majority are
Tier-1/Tier-2 sports-medicine and physiology venues (*Sports Medicine*, *IJSPP*, *BJSM*,
*J Physiol*, *Scand J Med Sci Sports*, *Physiol Rev*, *Sleep*), most with high citation counts.

**How to read each theme.** *Concept → Evidence → Implication for plan-building.*

---

## 2. Training intensity distribution (the 80/20 question)

**Concept.** *Training intensity distribution* (TID) describes how running time is split across
a low/moderate/high three-zone scheme (Zone 1 below the first lactate/ventilatory threshold;
Zone 2 between thresholds; Zone 3 above the second threshold). The two dominant models are
**polarised** (a large Z1 base + meaningful Z3, with little Z2) and **pyramidal** (a large
Z1 base with progressively less Z2 then Z3).[^1][^3]

**Evidence.** Seiler's foundational analysis established that highly trained endurance athletes
converge on roughly **80% of sessions/time at low intensity and ~20% at moderate-to-high
intensity** regardless of the exact model.[^1] Early controlled work suggested a polarised
distribution improved VO₂max and related variables more than threshold-dominant training over
short blocks.[^2] However, **descriptive studies of elite distance runners more often find a
pyramidal pattern**, especially in high-volume base phases, with the distribution becoming more
polarised nearer competition.[^3] A 16-week RCT in well-trained runners found **both pyramidal
and polarised TID improved performance, with no clear overall winner**.[^4] The most recent
systematic review with meta-analysis found that **polarised training confers only a small
advantage, and only for VO₂peak** (SMD ≈ 0.24) — concentrated in **highly-trained/national-level
athletes and shorter training blocks** (SMD ≈ 0.46) — with **no superiority for actual
performance (time trial), time-to-exhaustion, or threshold**, and **no difference in
trained/recreational athletes**.[^5] In other words, neither pattern is universally superior;
polarisation buys a modest, phase-specific aerobic-power gain rather than a general performance
edge.

**Implication for plan-building.**
- Keep the **~80/20 easy:hard split by time** as the backbone constraint (the app already does
  this). This is the single most robust TID finding.[^1]
- **Do not hard-code "polarised" as universally optimal.** For most recreational users and in
  base phases, a **pyramidal** distribution (a real threshold presence, less Z3) is at least as
  good and often more practical.[^3][^4][^5] Shift *toward* polarised (more Z3/VO₂max, less Z2)
  in the sharpening/peak phase.
- Enforce the existing rails: **≤2 quality sessions + 1 long run per week, never on consecutive
  days**, so that "20% hard" does not silently inflate.

---

## 3. The Norwegian double-threshold method

**Concept.** The dominant current elite model pairs **high low-intensity volume** with frequent
**lactate-guided threshold interval training (LGTIT)** — intervals held at a *controlled*
sub-threshold intensity defined by a blood-lactate target (typically **~2.0–4.5 mmol·L⁻¹**),
often performed as **two threshold sessions in one day ("double threshold")** on selected days.[^6][^7]

**Evidence.** A 2023 systematic review characterises the method as 3–4 LGTIT sessions plus ~1
VO₂max session per week within 150–180 km/week of mostly low-intensity running, allowing ~20% of
volume near threshold while keeping each rep controlled and repeatable.[^6] Best-practice profiling
of Olympic-level endurance athletes confirms very high volumes, disciplined easy running, and large
amounts of *threshold/moderate* work delivered as intervals rather than continuous efforts —
consistent with a pyramidal, threshold-rich structure.[^7] The key mechanistic idea is that
**splitting threshold work into intervals below the maximal lactate steady state lets an athlete
accumulate more time near threshold at a lower physiological cost** than a single hard continuous
effort would allow.[^6]

**Implication for plan-building.**
- Model `threshold` sessions as **controlled, interval-based sub-threshold work** (e.g.
  5–6 × 6–8 min, or 10–15 min reps at ~LT2 effort with short jog rests), *not* as all-out tempo.
  This is safer, more repeatable, and better supported for accumulating threshold volume.[^6]
- **Double-threshold days are an elite tool**, not a default. They require the volume base and
  recovery capacity most recreational users lack; only surface them for high-volume, experienced
  athletes and never as back-to-back hard days for others.[^6][^7]
- Where the athlete has lactate or reliable HR/pace anchors, define threshold reps by a **target
  effort band** rather than a single pace, echoing the lactate-guided principle.

---

## 4. Interval training: VO₂max and the critical-speed model

**Concept.** High-intensity intervals develop VO₂max and the ability to sustain a high fraction of
it. The **critical speed / critical power (CS/CP)** model formalises the boundary between the
*heavy* and *severe* intensity domains: CS is the highest sustainable steady-state speed, and *D′*
(or *W′*) is a finite "tank" of work available above it.[^10][^11][^12]

**Evidence.** Classic work established interval formats (including ~3–5 min reps at ~vVO₂max with
roughly 1:1 recovery) that maximise time spent near VO₂max.[^8][^9] The maximal metabolic steady
state (near CS/CP) is a sharper physiological boundary than fixed %-based zones for defining "hard"
vs "sustainable".[^12] The CS concept has been applied directly to **interval prescription and race
strategy**: intervals above CS deplete D′, and recovery duration/intensity governs how fast D′
reconstitutes, which predicts how long a given interval session can be sustained.[^10][^11]

**Implication for plan-building.**
- Anchor `vo2max` sessions to **~3–5 min reps at ~3K–5K effort with ~1:1 recovery** (already in the
  skill) — this is the best-supported format for time-at-VO₂max.[^8][^9]
- Where enough race/best-effort data exist, **estimate critical speed** (from two or more maximal
  efforts of differing duration) and prescribe severe-domain intervals relative to CS rather than to
  a lone threshold estimate; use recovery length to control total sustainable rep volume.[^10][^11]
- Keep `speed` (short neuromuscular reps, full recovery) distinct from VO₂max work: its purpose is
  economy/mechanics, not aerobic power.[^17][^23]

---

## 5. Durability / physiological resilience — the "fourth determinant"

**Concept.** The three textbook determinants (VO₂max, lactate/ventilatory threshold, running
economy) are all measured **fresh**. **Durability** (a.k.a. physiological resilience) is the
resistance of these variables to deterioration **late in prolonged exercise** — and it differs
markedly between athletes with similar fresh profiles.[^13][^14]

**Evidence.** Maunder and colleagues argued durability should be added to physiological profiling
because economy, thresholds and even the power–duration relationship drift adversely after
prolonged work.[^13] Jones framed physiological resilience as an **independent, fourth determinant**
of endurance performance, particularly decisive in the marathon where the last third is run in a
fatigued state.[^14] Recent methodological work shows durability profiles depend heavily on the
fatiguing protocol (relative intensity and duration), so the construct must be measured
carefully.[^15] Resilience appears **trainable primarily through accumulated low-intensity volume,
long runs, and time-on-feet**, i.e. the same base that builds the aerobic system, with fuelling and
substrate factors modulating late-race decline.[^16]

**Implication for plan-building.**
- Treat the **long run and total easy volume as durability training**, not merely "endurance base."
  For half/marathon goals, progress long-run duration and add **fatigued quality** (e.g. goal-pace
  segments *late* in a long run) to train resilience specifically.[^14][^16]
- When analysing sessions, **aerobic decoupling** (pace:HR drift >~5% in the second half) is a
  practical, data-available proxy for poor durability on the day — already computed by the app; use
  a persistent trend as a signal to add long-run volume.[^13]
- The demand analysis should weight durability by event: it matters little for 5K, substantially for
  the marathon.[^14]

---

## 6. Running economy: strength, plyometrics and footwear

**Concept.** **Running economy** (energy cost at a given submaximal speed) is a strong predictor of
distance performance and, unlike VO₂max, keeps improving in trained runners through **non-running
stimuli**.[^17][^23]

**Evidence.**
- **Strength training.** Meta-analyses show **heavy (high-load) resistance training and plyometric
  training produce small-to-moderate improvements in running economy** in middle- and long-distance
  runners, with effects varying by method and by the speed at which economy is measured; certainty of
  evidence is moderate.[^18][^19][^20] Explosive and heavy strength are both effective and do not
  compromise (and may aid) performance.[^19]
- **Advanced footwear technology (AFT / "super shoes").** Combining compliant resilient foam with a
  stiff (often carbon) plate, AFT improves running economy by **~2–4% on flat road**, translating to
  roughly a **~1% improvement in marathon performance** — but the benefit is terrain-dependent and can
  disappear or reverse on trails/uphill, and arises from the whole shoe system, not the plate
  alone.[^21][^22]

**Implication for plan-building.**
- **Include 2×/week strength work** (heavy resistance and/or plyometrics) as a standing, non-negotiable
  component for runners without contraindication — it is one of the few well-evidenced ways to improve
  economy without adding running load.[^18][^20] Schedule it to avoid clashing with hard running days.
- Provide **short strides / neuromuscular `speed` reps** year-round for economy/mechanics.[^17][^23]
- **Footwear guidance:** recommend AFT for road races and key road workouts, set expectations at a few
  percent (not transformative), and note it does not substitute for training. Because AFT shifts the
  pace–effort relationship, **verify goal paces against effort/HR** rather than assuming shoe-aided
  paces reflect fitness.[^21][^22]

---

## 7. Periodization and tapering

**Concept.** Organise training into phases (base → build/specific → peak → taper) that progressively
shift emphasis toward race-specific demands, then shed fatigue before competition.[^23]

**Evidence.** Training to enhance the determinants of distance performance requires phase-appropriate
emphasis (aerobic base, then threshold/VO₂max, then race-specificity).[^23] For the **taper**, two
independent meta-analyses converge: the most effective strategy is a **~2-week (≤21-day) progressive
reduction in training *volume* of 41–60%, while maintaining intensity and largely maintaining session
frequency**; large volume cuts with preserved intensity restore the stress–recovery balance and yield
small but meaningful performance gains (typically ~2–3%).[^24][^25] Reducing frequency too far can cost
performance via lost "feel"/technical proficiency.[^25]

**Implication for plan-building.**
- Keep the app's periodised structure and a **2–3 week taper with volume −40–60%, intensity frequency
  maintained** — this matches the evidence exactly.[^24][^25]
- During the taper, **do not drop the hard sessions**; drop easy volume. Preserve session frequency
  (shorten sessions rather than removing days).[^24][^25]
- Grow **intensity volume before intensity density**, and shift the easy:hard *character* (not the
  ~80/20 ratio) from pyramidal-base toward polarised-sharpening across the macrocycle.[^3][^5]

---

## 8. Detraining, illness, and interrupted training

**Concept.** Every real training year contains interruptions — a cold, a work trip, a niggle, a missed
week. Where the taper (§7) is a *planned* reduction in load, detraining is an **unplanned** one: the
partial or complete loss of training-induced adaptations in response to an insufficient training
stimulus, conventionally split at ~4 weeks into **short-term** (<4 weeks) and **long-term** (>4 weeks)
insufficient stimulus.[^57][^58] Rebuilding a plan after an interruption requires three numbers: what is
actually lost, how fast, and the **minimum dose** that holds on to it.

**Evidence.**

- **The early loss is central (blood volume), not peripheral.** In the classic detraining study, endurance-
  trained subjects who stopped training entirely lost **7% of VO₂max in the first 21 days**, with the decline
  stabilising after 56 days at **16% below trained values**. The *early* fall tracked a reduced **stroke
  volume**; the *later* fall tracked a reduced a-vO₂ difference.[^59] Short-term detraining in highly trained
  athletes is characterised by exactly this pattern — a rapid decline in VO₂max **and blood volume**, with
  heart rate failing to rise enough to offset the lost stroke volume, so maximal cardiac output falls.[^57]
- **But the floor is far higher than athletes fear.** After **84 days** of complete inactivity, the same
  subjects still had a substantially higher VO₂max than never-trained controls (**50.8 vs 43.3 mL·kg⁻¹·min⁻¹**);
  **muscle capillarisation did not decline at all**, remaining 50% above sedentary; and oxidative enzyme
  activity fell with a **~12-day half-life** but stabilised 50% above sedentary.[^59] Over the long term,
  VO₂max declines markedly yet stays above untrained values, while **recently acquired gains are lost
  completely** — the newest fitness is the most fragile, the deep base is remarkably durable.[^58]
- **Intensity is what preserves fitness; volume and frequency are negotiable.** A narrative review of the
  *minimal maintenance dose* found endurance performance can be maintained for **up to 15 weeks** with training
  frequency cut to as little as **2 sessions per week**, or volume cut by **33–66%** (as little as 13–26 min per
  session) — **provided exercise intensity is maintained**. Strength and muscle size can be held for up to
  32 weeks on **1 session per week and 1 set per exercise** at maintained relative load. The authors' primary
  conclusion is that **intensity is the key variable** for maintaining performance despite large reductions in
  frequency and volume — though they note the data come from general populations and are explicitly
  **insufficient to make athlete-specific recommendations**.[^60]
- **Illness: the symptom pattern predicts the timeline better than the calendar.** Acute respiratory infections
  are common in athletes and now have an IOC consensus framework covering diagnosis, management and return to
  sport.[^61] The most directly useful evidence is symptom-based: in symptomatic athletes with acute respiratory
  illness, the symptoms associated with prolonged return-to-play were **excessive fatigue (75%), chills (65%),
  fever (64%), headache (56%), loss of smell (51%), chest pain/pressure (48%), difficulty breathing (48%) and
  loss of appetite (47%)** — and **"excessive fatigue" was the only one that survived multivariate analysis**.[^62]
  A systematic review by the same consensus subgroup confirms that the performance effects of acute respiratory
  infection, while real, remain poorly quantified.[^63]

**Implication for plan-building.**

- **Reduced training beats no training, and the reduction should be in volume — not intensity.** When life
  compresses a week, cut frequency and volume hard but **keep one quality session**: that is what the maintenance
  evidence says preserves fitness.[^60] This is the same shape as the taper rail (§7) — cut volume, hold
  intensity — which means the app already implements the right instinct for the wrong reason, and can reuse it.
- **Do not regenerate a plan for a short break.** A week off costs little, and most of what it costs is **plasma
  volume** — the fastest-returning adaptation, not "fitness."[^57][^59] The app's CTL will drop faster than the
  athlete's actual capacity, so trust the physiology over the model: **up to ~10 days lost, resume rather than
  rebuild; beyond that, regenerate from a lower starting point** — which is exactly where the skill already draws
  the line, and the evidence supports keeping it there.
- **Distinguish recent gains from deep base when deciding how far to regress.** Newly acquired fitness is lost
  first and most completely; a long-standing aerobic base is not.[^58][^59] An athlete with years of volume
  returning from three weeks off should restart nearer their prior level than a first-year runner would.
- **Ground the illness rule and sharpen it.** The skill's "below the neck / fever → full rest" heuristic is
  directionally supported — systemic symptoms do predict prolonged return — but the evidence points at
  **excessive fatigue as the single strongest predictor**, ahead of fever.[^62] Ask about it explicitly, and treat
  a report of excessive fatigue as at least as disqualifying as a temperature.
- **Return progressively and expect the timeline to be symptom-driven, not fixed.** Symptom clusters, not the
  calendar, should pace the return; and because the performance effects of infection are poorly quantified,[^63]
  err toward the athlete's report over any table — which is exactly where the readiness and wellness evidence
  points too (§11).

---

## 9. Load monitoring and the ACWR critique

**Concept.** Internal (HR-based TRIMP, HR-TSS) and external/pace-based (rTSS) load metrics, integrated
over time into fitness (CTL), fatigue (ATL) and form (TSB), are used to titrate progression and flag
injury risk. The **acute:chronic workload ratio (ACWR)** compares recent (~7-day) to chronic (~28/42-day)
load, with a "sweet spot" (~0.8–1.3) promoted as protective.[^26] A third family — **session-RPE (sRPE)** —
quantifies internal load as *perceived effort × duration*, requiring no sensor at all.[^64]

**Evidence.** Consensus supports systematically monitoring load and quantifying both external and
internal load, but stresses that no single metric is definitive and that the internal response (HR, RPE)
is what drives adaptation.[^26] Crucially, **the ACWR has been substantially challenged**: it has
conceptual and statistical flaws — mathematical coupling between numerator and denominator produces
**spurious correlations**, ratio metrics are noisy and create statistical artifacts, the acute/chronic
time windows are arbitrary, and the widely reproduced "sweet-spot" risk figure has been criticised as
methodologically unsound; no study has properly estimated a **causal** effect of manipulating ACWR on
injury.[^27][^28][^29]

**Session-RPE deserves separate treatment**, because it is the cheapest validated internal-load tool and it
fails in different places than HR does. Foster's method multiplies a session's RPE by its duration to yield a
single internal-load figure, explicitly designed to quantify training during **non-steady-state and prolonged
exercise** — the conditions where HR-based quantification is weakest.[^64] The same line of work is the origin
of the **monotony** and **strain** constructs this review already leans on.[^65] Subsequent validation supports
sRPE's validity, reliability and internal consistency across many sports, both sexes, and all age and
expertise levels; it can stand alone, though it is often better paired with a physiological measure.[^66]

**Implication for plan-building.**
- **Compute sRPE — the data now exists.** The app stores `perceived_exertion` and `feel` per activity, so
  `RPE × minutes` is available for free. Its value is that it survives precisely the cases where the app's other
  metrics break: **intervals** (non-steady-state, where HR lags) and **heat** (§13, where HR-derived load inflates
  while pace-derived rTSS deflates for the same session).[^64][^66] A third, independent opinion is exactly what
  a disagreement between TRIMP and rTSS needs.
- Treat sRPE as **its own scale** — the rule against mixing load families (below) applies to it too; trend it
  against itself, never against TRIMP or TSS.
- **Keep CTL/ATL/TSB and absolute ramp rate as the primary progression controls** (weekly volume growth
  ≤~10%, CTL ramp ≤~5/week, down week every ~4th). These are more defensible than any ratio.[^26]
- **Demote ACWR (ATL/CTL ~0.8–1.3) to a soft, secondary heuristic** and label it as such in any
  athlete-facing rationale. Do not present the 0.8–1.3 band as a validated injury threshold; the science
  under that rail has moved.[^27][^28][^29]
- Weight **consistency, sudden spikes, and monotony** (many identical-load days) at least as heavily as
  any workload ratio.[^26] Monotony and strain now have their original source and definition rather than
  being inherited as folklore.[^65]
- Never mix load scales (TRIMP vs TSS vs sRPE families) when trending — compare within one model.[^26]

---

## 10. Recovery, HRV-guided load, and monotony

**Concept.** Autonomic recovery status — indexed by **resting heart-rate variability (HRV)** — can be
used to decide *when* to schedule hard sessions, adjusting the plan to the athlete's day-to-day
readiness rather than following a fixed template.[^30][^31]

**Evidence.** Meta-analyses find **HRV-guided training performs at least as well as, and modestly better
than, pre-planned training** for aerobic outcomes, with the clearest benefit being **fewer negative
responders** (fewer athletes who fail to improve or regress) rather than large mean performance gains;
effects on maximal aerobic capacity are small and often non-significant, and results are sensitive to
methodology (measurement standardisation, decision rules).[^30][^31]

**Implication for plan-building.**
- HRV-guidance is a **reasonable readiness modifier, not a plan replacement**: use a suppressed
  multi-day HRV trend (with subjective wellness) to **defer or downgrade a hard session**, keeping the
  weekly structure intact.[^30][^31]
- Its strongest value is **damage-avoidance** (catching non-functional overreaching) — align this with
  the app's existing TSB / overreaching flags and the "no hard days back-to-back" rule.[^30]
- Avoid **training monotony**: preserve hard/easy polarity day-to-day, which the app already monitors.[^26]

---

## 11. Sleep and the readiness synthesis

**Concept.** §10 asks whether *autonomic* status should schedule hard days. This section asks the two questions
either side of it: **sleep**, the largest single recovery input and the one the athlete actually controls; and
the **readiness synthesis** — how sleep, HRV, resting HR and the athlete's own report should be combined into a
single "train or back off" judgement, given that the app collects all of them.

**Evidence.**

- **Sleep loss degrades performance; sleep extension improves it.** The mechanisms and magnitude of sleep loss on
  exercise performance and the physiological and cognitive responses to exercise are well reviewed.[^67] The
  landmark intervention remains sleep *extension*: collegiate basketball players who spent a minimum of 10 h in
  bed for 5–7 weeks increased objectively measured nightly sleep by **111 minutes**, and improved a timed sprint
  (**16.2 → 15.5 s**), free-throw accuracy (**+9%**) and 3-point accuracy (**+9.2%**).[^68] The caveats matter for a
  running app: **n = 11**, no control group, and the outcomes are basketball-specific skills, not endurance —
  this is a direction, not an effect size to quote at a runner.
- **Chronic short sleep tracks injury.** In 112 adolescent athletes, sleeping **<8 h per night** was associated
  with **1.7× the odds of injury** (95% CI 1.0–3.0, p = 0.04).[^69] Again read it carefully: adolescents,
  retrospective survey, and a confidence interval whose lower bound touches 1.0 — suggestive, not decisive.
- **A consensus exists** synthesising sleep assessment, the prevalence of poor sleep in athletes, and practical
  recommendations for improving it.[^70]
- **Wearable sleep data is not polysomnography — and its failures are systematic.** Seven consumer devices plus
  research actigraphy were tested against **polysomnography** in 34 adults across three nights including a
  deliberately disrupted-sleep condition. Epoch-by-epoch **sensitivity was high (all ≥0.93)** — the devices are
  good at recognising sleep — but **specificity was low-to-medium (0.18–0.54)**, meaning they are poor at
  recognising *wake* and therefore **overestimate sleep**. **Sleep-stage assessment was inconsistent**, devices
  performed **worse on nights with poorer/disrupted sleep**, and — directly relevant here — the **Garmin devices
  performed worse than actigraphy** on sleep/wake measures, while most other brands matched or beat it.[^71]
- **Subjective report outperforms the sensors.** A systematic review found subjective and objective measures of
  athlete well-being **generally did not correlate**, and that **subjective measures reflected acute and chronic
  training load with superior sensitivity and consistency** than objective ones. Subjective well-being was
  impaired by an acute load increase *and* by chronic training, and improved when load was acutely reduced.[^72]

**Implication for plan-building.**

- **Treat sleep as a training variable, not a lifestyle footnote.** It is the cheapest available adaptation and
  injury lever, and it belongs in the athlete profile alongside volume. Before adding load to a stalled athlete,
  check whether the plan is competing with their sleep — and for a goal race, deliberate sleep *extension* is a
  legitimate, essentially risk-free intervention.[^68]
- **The app's sleep gate is right in kind, soft in number.** `/api/wellness/readiness` already flags a low
  `sleep_score`, which the evidence supports in principle — but no study licenses the specific threshold, so it
  should be labelled a heuristic, exactly as ACWR now is (§9).
- **Trust duration, distrust stages.** Because consumer devices overestimate sleep (specificity 0.18–0.54) and
  assess stages inconsistently, **`deep_sleep_s` is the least defensible field the app stores** — do not coach
  off sleep stages, and do not let an athlete's "poor deep sleep" reading drive a plan change.[^71] The
  Garmin-specific underperformance makes this stricter here, not looser.
- **The device is least reliable exactly when it looks most alarming.** Accuracy degrades on disrupted nights,[^71]
  so a single bad reading is the *least* trustworthy kind. Require a multi-day trend before acting — the same
  discipline §10 already applies to HRV.
- **Weight the athlete's own report at least as heavily as the sensors.** The app stores `perceived_exertion` and
  `feel`; per the monitoring evidence these track training load *better* than objective markers and **do not
  correlate with them**, which means they are not redundant — they are the more sensitive channel.[^72] This
  upgrades the skill's existing "confirm with the athlete, treat it as one signal not a verdict" from courtesy
  to method.
- **Combine, don't rank.** No single measure is definitive (§9): use sleep, HRV, RHR and subjective report as
  converging evidence, and act when they agree. A suppressed HRV *with* poor sleep *and* an athlete reporting
  flatness is a real signal; any one alone is noise.

---

## 12. Fuelling: carbohydrate periodization and race intake

**Concept.** Two distinct questions: (a) **training-diet periodization** — whether deliberately training
with *low* carbohydrate availability ("train low") boosts adaptation; and (b) **race-day fuelling** —
how much carbohydrate to ingest during prolonged competition.[^32][^33][^34]

**Evidence.**
- **"Fuel for the work required"** frames carbohydrate availability as something to match to each
  session's demand (high for quality, lower for some easy sessions), and "train-low" models
  (fasted, twice-a-day, sleep-low) up-regulate molecular signalling (AMPK, p38MAPK).[^32] However, a
  **systematic review/meta-analysis found periodized carbohydrate restriction does not improve endurance
  performance over high-carbohydrate diets in trained athletes**, and low-glycogen states impair the
  quality of hard sessions.[^33]
- **Race-day carbohydrate intake** scales with duration: guidance rises toward **~60 g·h⁻¹**, and up to
  **~90 g·h⁻¹** using multiple transportable carbohydrates (glucose:fructose) for events >2.5–3 h, with
  gut tolerance being trainable.[^34]

**Implication for plan-building.**
- Keep hard/quality and long sessions **well-fuelled**; reserve any "train-low" stimulus for selected
  *easy* sessions only, and never before or during key quality work.[^32][^33]
- For marathon plans, **build a fuelling plan (~60–90 g·h⁻¹) and rehearse it in long runs** — treat gut
  training as part of `race-specific` preparation.[^34]
- Do not present carbohydrate periodization as a performance enhancer; its rationale is
  adaptation/body-composition, and it carries a session-quality cost.[^33]

---

## 13. Heat: acclimation, transfer, and racing warm

**Concept.** Heat degrades endurance performance through a well-described chain: skin blood flow
competes with working muscle for cardiac output, plasma volume falls, heart rate rises at any given
pace, and core temperature climbs — so **pace at a fixed effort falls, and effort at a fixed pace
rises**.[^41] **Heat acclimation (HA)** is the adaptation to repeated exercise-heat exposure that
blunts this chain. A separate and more contested claim is that heat is *ergogenic in its own right* —
that a heat block improves performance even in **cool** conditions, making it a logistically cheap
substitute for altitude.[^43][^49]

**Evidence.**

- **What heat costs.** The definitive dose–response comes from seven marathons over up to 36 years:
  performance slows **progressively as wet-bulb globe temperature (WBGT) rises from 5 to 25 °C**.
  Top male finishers were slower than the course record by **1.7 / 2.5 / 3.3 / 4.5%** across WBGT
  quartiles (5–10, 10–15, 15–20, 20–25 °C); top women trended the same way. Critically, the **25th-,
  50th-, 100th- and 300th-place finishers slowed *more* than the leaders as WBGT rose** — heat is
  not a uniform tax, it is regressive with respect to ability.[^42]
- **Acclimation: dose and adaptations.** HA produces earlier and greater sweating, increased skin
  blood flow, **plasma volume expansion**, lower resting and exercising core temperature, reduced
  cardiovascular strain, and enhanced cellular protection; the magnitude is set by the **intensity,
  duration, frequency and number** of exposures and by whether the heat is dry or humid.[^37] A
  meta-analysis of 96 studies found HA has a **moderate** beneficial effect on exercise performance
  and capacity in the heat *regardless of regimen*, with **moderate-to-large** effects on lowering
  core temperature and maintaining cardiovascular stability — and that **longer regimens beat shorter
  ones**, with adaptations greatest beyond 14 days.[^39] The consensus recommendation is **repeated
  exercise-heat exposures across 1–2 weeks**, beginning each session euhydrated.[^38]
- **Decay and re-induction.** Adaptations are perishable but cheap to refresh: **~2.5% of the heart-rate
  and core-temperature adaptation is lost per day** without heat exposure (2.3%/day HR, 2.6%/day core
  temp), **≥5 days** of exposure suffices to induce them, and **re-acclimation is 8–12× faster than
  decay** — which makes brief top-ups, rather than a full second block, the efficient way to hold
  adaptation into a race.[^40]
- **Transfer to cool conditions — contested.** The influential claim rests on Lorenzo et al., where 10
  days of HA improved cycling time-trial performance in **cool (13 °C)** as well as hot conditions.[^43]
  A mechanistic cross-over study failed to reproduce it: after 10 days of heat training, VO₂max and
  30-min time-trial performance rose by **9.6% and 10.4% at 38 °C but were *unchanged* at 18 °C**. The same
  study weakened the leading candidate mechanism: acutely expanding blood volume with albumin (+538 mL) before
  testing in the heat **failed to rescue performance**, so acclimation-induced hypervolaemia — the adaptation
  most often invoked to explain a cool-condition carry-over — does not by itself explain even the *hot*-condition
  gain.[^44] The disagreement was staged as a
  *Journal of Physiology* **CrossTalk**: the case *for* transfer,[^45] against the counter-argument that
  apparent cool-condition gains reflect a **training-load confound** — heat raises relative intensity,
  so the "heat effect" is partly just a harder training stimulus.[^46] The most recent controlled
  crossover splits the difference: 3 weeks of HA raised time-trial power in **hot (+20 W)** *and*
  **cool (+12 W)** but not hypoxic conditions, while VO₂peak rose **only in the heat**, with the authors
  concluding the mechanisms for any cool-condition benefit **remain unclear**.[^47]
- **The haematological route.** Heat expands plasma volume within days, and prolonged heat training
  raises haemoglobin mass: 5 weeks of 1 h heat sessions 5×/week increased **Hbmass by 42 g** in elite
  cyclists (vs +6 g in controls). Notably this did **not** yield a greater VO₂max improvement, with only
  small-to-moderate effect sizes favouring heat for lactate-threshold power, fatigued economy and 15-min
  power.[^48] Whether heat is a genuine alternative to altitude for Hbmass and *performance* — as opposed
  to for Hbmass alone — is exactly what remains open.[^49]
- **Passive and practical methods.** Chambers are rare; heat is not. Six days of **post-exercise hot-water
  immersion** (40 °C, 40 min) after temperate running induced HA and improved time-trial performance by
  **4.9% in 33 °C — but not in temperate conditions**.[^50] Three weeks of **post-exercise sauna** (~28 min,
  3×/week) in middle-distance runners lowered peak core temperature, skin temperature and heart rate, and
  *did* improve temperate-condition markers (**VO₂max +0.27 L·min⁻¹**, speed at 4 mmol·L⁻¹ **+0.6 km·h⁻¹**).[^51]
  Pooled, however, the picture is sober: a meta-analysis of post-exercise heat exposure (10 studies, 199
  participants) found a **trivial** effect on performance in the heat (ratio of means 1.04, 95% CI 0.94–1.15),
  **trivial** effects in thermoneutral conditions, only small effects on VO₂max — all at **low-to-very-low
  GRADE certainty**.[^52] Passive methods are accessible and low-risk, but should be sold modestly.
- **Cold immersion is the mirror image — and it is not neutral.** Because this section recommends *hot* immersion,
  the *cold* case has to be stated alongside it, or the athlete will simply hear "immersion good." Regular
  post-exercise **cold-water immersion (CWI)** attenuates acute anabolic signalling and long-term muscle
  adaptation to strength training,[^73] and the pooled effect is **selective**: CWI alongside **resistance**
  training harms gains in one-repetition maximum, maximal isometric strength and strength endurance
  (**SMD −0.60**, 95% CI −0.87 to −0.33) and ballistic performance (**SMD −0.61**), whereas CWI alongside
  **endurance** training has **no detectable effect** on time-trial performance or maximal aerobic power
  (SMD −0.07 and 0.00, both p ≥ 0.71).[^74] Cold blunts the adaptation you build with weights, not the one you
  build with running.
- **Females are under-represented.** HA guidelines derive mostly from male cohorts. A female-specific
  meta-analysis (30 studies, 22 pooled) confirms HA works in women — reducing **resting core temperature
  (ES −0.45)** and **exercising core temperature (ES −0.81)** — while noting that male-derived dose
  guidance may not be optimal given biological and phenotypical differences.[^53]
- **Cooling and safety.** Pre- and per-cooling attenuate the performance decline in the heat, but the benefit
  is **larger for constant-workload exercise (ES 0.62) than for self-paced exercise (ES 0.30)** — and racing
  is self-paced, because athletes spontaneously redistribute effort rather than bank the cooling.[^54]
  Above all, heat is a **medical** issue before it is a performance one: exertional heat stroke is defined by
  **extreme hyperthermia (>40.5 °C) accompanied by central nervous system dysfunction** (irrational behaviour,
  altered or lost consciousness), it is a leading cause of sudden death in sport, and survival turns on time-to-
  cooling — hence the explicit rule that patients are **"cooled first and transported second"**, with whole-body
  **cold-water immersion** the most effective modality (ice packs and towels are not a substitute).[^55][^56]
  Notably, the IOC consensus **declines to set a universal WBGT cut-off**, observing that the same WBGT (30.6 °C)
  is graded *orange* by the Tokyo 2020 organisers, *red* by World Triathlon and *black* by modern pentathlon, and
  recommending **sport-specific** extreme-heat policies instead.[^55]

**Implication for plan-building.**

- **Treat heat as a confounder before it is a training tool.** The app already stores `weather_temp_c`,
  `weather_humidity_pct` and `weather_wind_mps` per activity — enough to derive an **approximate WBGT**
  (solar load unmodelled) rather than reasoning from dry-bulb temperature alone. This matters: the
  marathon dose–response is indexed to **WBGT, not air temperature**, and the two diverge sharply with
  humidity.[^42] Humidity is not a modifier to mention in passing — it is part of the independent variable.
- **Keep the existing "~1–2% per 5 °C above ~12–15 °C" heuristic, but scale it by ability.** It is
  well-calibrated against the elite end of the evidence (Ely's top men lose ~1% per 5 °C WBGT) and should
  sit at the **upper** end, or beyond, for slower runners, who demonstrably lose more.[^42] A 4:30 marathoner
  is not paying a 3:00 marathoner's heat tax.
- **Do not read heat-driven decoupling as poor durability.** Aerobic decoupling is the app's durability
  readout (§5), but heat inflates HR drift directly.[^41] Check WBGT before logging a decoupling trend as a
  resilience deficit — otherwise the fix (more long-run volume) is prescribed for a problem that was weather.
- **Heat distorts the load model asymmetrically.** Elevated HR in the heat inflates **HR-derived** load
  (TRIMP, HR-TSS) while pace-derived **rTSS** falls with the slower pace — the same session lands very
  differently depending on the metric. This compounds the existing rule never to mix load scales when
  trending (§9), and argues for flagging hot sessions rather than silently letting them ramp CTL — and it is
  the clearest case for reading session-RPE (§9) as a third opinion when TRIMP and rTSS disagree.
- **Heat blocks are athlete-requested, not coach-initiated — and a plan without one is not
  deficient.** Everything below describes what heat training *can* do once an athlete chooses it;
  none of it is a licence to add heat work unbidden. The characteristic failure mode of an
  automated coach is **over-prescription** — a modality that is genuinely useful in a narrow case
  gets bolted onto every warm-weather plan, and the athlete pays the recovery cost for a benefit
  that, outside the heat, is unproven. Prescribe only on request, always with the standing
  disclaimer (reliable **in the heat**, unsettled for **cool**), and **never review a plan as
  deficient for omitting heat preparation** (§16).
- **"A hot race" is the wrong trigger — thermal strain is, and it scales with duration.** The marathon
  dose–response declines *continuously* from ~5 °C WBGT upward,[^42] so a **marathon is heat-sensitive far
  below any temperature a runner would call hot**, while a 5K in the same conditions is barely touched. The
  decision variable is **temperature × humidity × duration × ability**, never a threshold word. A 2:45
  marathon at ~16 °C and ~60% humidity carries real thermal strain; a 17-minute 5K on that day does not.
- **Two protocols, two evidence bases — do not conflate them.**
  - *Thermoregulatory acclimation* — **1–2 weeks** of repeated exercise-heat exposure, ≥5 days minimum,
    finishing near the race.[^38][^39] This is the **well-supported** one, and it pays in any race carrying
    real thermal strain. Because decay runs ~2.5%/day while re-induction is 8–12× faster, hold it with
    **short top-ups every ~5 days** rather than a second full block — which also resolves the taper conflict,
    since a full block is disruptive precisely when the taper (§7) wants fatigue shed.[^40]
  - *Haematological ("altitude alternative")* — a different and much longer dose: **~5 weeks at ~5
    sessions/week**, the protocol that raised Hbmass by 42 g.[^48] This is the **speculative** one: Hbmass
    rises, but the same study found **no** accompanying VO₂max advantage,[^48] and whether it converts into
    cool-race performance is exactly the open question.[^45][^46][^47][^49] A bet, never a promise.
- **Protocol *design* decides how hard the main criticism bites.** The strongest objection to cool-transfer
  findings is the **training-load confound** — heat raises relative intensity, so the "heat effect" is partly
  just a harder stimulus.[^46] That objection lands hardest where heat **replaces** normal training (everything
  performed hot).[^44] It lands far more weakly where heat is **added to easy volume while quality stays
  cool** — post-session hot baths, overdressed easy cross-training — which is the design of the study that
  *did* find cool-condition gains.[^43] A protocol that costs no session quality is a low-risk bet even under
  genuine uncertainty, and should be judged on that basis rather than on the unsettled transfer alone.
- **Offer sauna or hot-water immersion as the accessible option, with honest expectations.** For an athlete
  without a chamber, post-exercise heat is the realistic route to acclimation for a hot race.[^50][^51]
  Do **not** present it — or heat training generally — as a validated way to get faster in *cool* races;
  the transfer question is unsettled and the pooled passive-heat evidence is trivial-to-small at low
  certainty.[^45][^46][^47][^52] This is the same "not settled" posture the review takes on polarised
  vs pyramidal (§2), and it should read that way in any athlete-facing rationale.
- **Never let "immersion" collapse into a single recommendation.** This review now prescribes *hot* immersion for
  acclimation (above) and 2×/week strength for economy (§6). Habitual post-session **ice baths would leave the
  running adaptation intact but blunt precisely the strength adaptation the plan is buying** — a contradiction the
  athlete would never spot on their own.[^73][^74] Reserve CWI for acute recovery between congested efforts
  (multi-day racing, doubles in the heat), keep it away from strength blocks, and never present hot and cold
  immersion as interchangeable "recovery."
- **Race guidance in heat is pacing guidance.** Since cooling helps self-paced exercise least,[^54] the
  first-line intervention is a **downward goal-pace adjustment** scaled to forecast WBGT and athlete
  ability, set *before* the gun — not a mid-race rescue. Pre-cooling and fluid strategy are adjuncts.
- **Safety rails outrank the plan.** At high WBGT, downgrade or move hard sessions and races rather than
  negotiating with them. There is **no universal WBGT number** to encode — the consensus is explicitly that
  thresholds are sport-specific and federations disagree — so treat WBGT as an escalating risk gradient, not a
  bright line, and surface exertional-heat-stroke recognition (**>40.5 °C + CNS dysfunction → cool first with
  cold-water immersion, transport second**) for anyone racing in the heat.[^55][^56] Pair heat guidance
  with the fuelling section's hydration advice (§12) — the consensus is to **start euhydrated and limit,
  not eliminate, dehydration**,[^38] and over-drinking carries its own risk.

---

## 14. The female endurance athlete and RED-S

**Concept.** Two practically important, historically neglected topics: whether the **menstrual cycle**
should reshape training, and **Relative Energy Deficiency in Sport (REDs)** — the syndrome of impaired
physiological function caused by **low energy availability**.[^35][^36]

**Evidence.** A large meta-analysis reports the **menstrual cycle has, on average, only a trivial effect
on exercise performance**, with a possible small reduction in the early-follicular phase — but the
evidence base is of generally low quality and inter-individual variation is high, so **individualised
tracking beats population rules**.[^35] The **2023 IOC consensus on REDs** reframes and expands the older
"female athlete triad": chronic **low energy availability** impairs endurance performance and health
(bone, endocrine, metabolic, immune) in **both sexes**, and is a leading, under-recognised driver of
under-performance and injury in distance runners.[^36]

**Implication for plan-building.**
- **Do not impose generic menstrual-phase periodization**; instead allow **symptom/performance tracking**
  and adjust individually where an athlete reports consistent phase effects.[^35]
- Screen for **REDs / low energy availability** as a first-line explanation when volume rises but
  performance, recovery, mood, or (for some) menstrual regularity deteriorate — an energy-availability
  problem cannot be out-trained, and adding load makes it worse.[^36]
- Record such findings in the athlete profile so future plans start from a corrected energy baseline.[^36]

---

## 15. Synthesis: an evidence map for the plan generator

| App element | Best-supported principle | Key refs |
|---|---|---|
| Easy:hard split | ~80/20 by time; low-intensity dominant | [^1] |
| Polarised vs pyramidal | Not settled; pyramidal at least as good for recreational/base; polarising gives only a small VO₂peak gain, mainly elite/short blocks — reserve for peaking | [^3][^4][^5] |
| `threshold` sessions | Controlled, interval-based sub-threshold ("lactate-guided") work, not all-out tempo | [^6][^7] |
| `vo2max` sessions | ~3–5 min reps at ~3–5K effort, ~1:1 recovery; anchor to critical speed if data allow | [^8][^9][^10][^11] |
| Long run / easy volume | Builds durability (4th determinant); add late-run quality for resilience | [^13][^14][^16] |
| `speed` | Short neuromuscular reps for economy/mechanics | [^17][^23] |
| Off-run work | 2×/week heavy-resistance + plyometrics improves economy | [^18][^19][^20] |
| Footwear | AFT ~2–4% economy on road (~1% marathon); verify fitness by effort/HR | [^21][^22] |
| Progression | Absolute ramp (≤~10%/wk vol, ≤~5 CTL/wk), down week q4; consistency > ratios | [^26] |
| ACWR rail | Soft heuristic only — statistically/conceptually flawed | [^27][^28][^29] |
| Session-RPE | `RPE × minutes` as a third internal-load channel; survives intervals and heat where HR fails; own scale | [^64][^66] |
| Missed time | Don't rebuild for <~2 wk off; early loss is blood volume, not base; newest gains go first | [^57][^58][^59] |
| Reduced training | Maintain fitness up to 15 wk on ~2 sessions/wk **if intensity held** — cut volume, not quality | [^60] |
| Illness | Symptom-driven return; *excessive fatigue* is the strongest predictor of prolonged return, ahead of fever | [^61][^62][^63] |
| Readiness | HRV/wellness as a modifier to defer hard days; reduces negative responders | [^30][^31] |
| Sleep | Training variable, not lifestyle; extension is a free race-prep lever; short sleep tracks injury | [^67][^68][^69][^70] |
| Wearable sleep | Trust duration, distrust stages (`deep_sleep_s`); worst on bad nights; Garmin underperformed | [^71] |
| Subjective report | `feel`/RPE track load better than objective markers and don't correlate with them — not redundant | [^72] |
| Cold immersion | Habitual CWI blunts strength adaptation (SMD −0.60), not endurance (~0.00) — never a default | [^73][^74] |
| Taper | 2–3 wk, volume −40–60%, hold intensity & frequency | [^24][^25] |
| Fuelling | Fuel quality/long sessions; race 60–90 g·h⁻¹ rehearsed in training | [^32][^33][^34] |
| Female athlete / REDs | Individualise cycle effects; screen low energy availability first | [^35][^36] |
| Weather as confounder | Check WBGT (not air temp) before blaming fitness; cost ~1%/5 °C WBGT for elites, more for slower runners | [^41][^42] |
| When heat prep is indicated | Gate on thermal strain (temp × humidity × duration × ability), not the word "hot" — a marathon is heat-sensitive well below it, a 5K is not | [^42] |
| Thermoregulatory block | 1–2 wk exercise-heat exposure, ≥5 d minimum, longer is better; ~2.5%/day decay, re-induction 8–12× faster → short top-ups. The well-supported protocol | [^37][^38][^39][^40] |
| Haematological block | A *different* dose: ~5 wk at ~5 sessions/wk → Hbmass +42 g — but no VO₂max advantage alongside it. The speculative protocol | [^48][^49] |
| Heat → cool transfer | Not settled; don't sell heat blocks as an altitude substitute or a cool-race enhancer. Heat added to *easy* volume (quality kept cool) is the design least exposed to the training-load confound | [^43][^44][^45][^46][^47] |
| Passive heat (sauna/HWI) | Accessible route to acclimation; pooled effects trivial-to-small at low certainty — modest claims only | [^50][^51][^52] |
| Racing in heat | Adjust goal pace to forecast WBGT pre-race; cooling helps self-paced exercise least | [^54] |
| Heat safety | WBGT is a risk gradient, not a universal cut-off (thresholds are sport-specific); EHS = >40.5 °C + CNS dysfunction → cool first (cold-water immersion), transport second | [^55][^56] |

## 16. Where the evidence has moved under the app's current rails

1. **ACWR (0.8–1.3).** The app trusts this band as a safety rail; the underlying ratio is now widely
   regarded as statistically and conceptually flawed. **Action:** keep it visible but explicitly
   secondary to absolute ramp rate, consistency and monotony.[^27][^28][^29]
2. **"Polarised" as the default distribution.** The skill cites polarised/pyramidal and Seiler 80/20;
   current evidence says **pyramidal is at least as good for most users and phases**, with polarisation a
   peaking tool. **Action:** make distribution phase- and level-dependent rather than fixed.[^3][^4][^5]
3. **Durability is missing as an explicit target.** The app names endurance/threshold/VO₂max/speed but
   not resilience. **Action:** treat long-run volume + late-run quality as durability work and surface
   decoupling trends as its readout.[^13][^14][^16]
4. **Off-run strength is under-weighted.** Economy gains from strength/plyometrics are among the
   best-evidenced, load-free improvements available. **Action:** make 2×/week strength a standing plan
   element.[^18][^20]
5. **Heat is collected but not modelled.** The app stores temperature, humidity and wind per activity and
   the coach skill uses heat only as a qualitative caveat ("check before blaming fitness"). Two gaps
   follow. First, the evidence is indexed to **WBGT, not dry-bulb temperature**, and the app has the
   inputs to approximate it — humidity is part of the independent variable, not a footnote.[^42] Second,
   the heat penalty is **larger for slower runners**, so a single flat "1–2% per 5 °C" understates it for
   much of the field.[^42] **Action:** derive an approximate WBGT, scale the pace adjustment by ability,
   and treat hot sessions as load-model outliers (heat inflates HR-based TRIMP/HR-TSS while deflating
   pace-based rTSS) and as decoupling confounders before they are read as durability deficits.[^41]
6. **Heat acclimation is absent as a training modality — but "hot race only" is the wrong gate.** For a race
   carrying real thermal strain, thermoregulatory acclimation is one of the best-evidenced preparations
   available, and its decay kinetics (~2.5%/day, fast re-induction) make it schedulable around a taper.
   Two corrections matter. First, **strain scales with duration**: the marathon dose–response declines
   continuously from ~5 °C WBGT up,[^42] so a marathon is heat-sensitive well below "hot" while a 5K is not —
   gating on the word rather than on temperature × humidity × duration × ability gets the marathon case
   wrong. Second, the **1–2 week thermoregulatory block and the ~5-week haematological block are different
   interventions**;[^48] prescribing one and claiming the other's benefit is a category error.
   **Action:** treat heat blocks as **athlete-requested, never volunteered** — the risk here is
   over-prescription — and when requested, match dose to purpose, default to sauna/hot-water immersion
   for athletes without a chamber, and attach the standing disclaimer: reliable **in the heat**, unsettled
   for **cool** races.[^38][^39][^40][^45][^46][^47][^50][^51]
7. **The plan-adjustment rules were unsourced.** The coach skill prescribes precise numbers for missed time
   (return volume, regenerate thresholds, down weeks) that had no evidence base in this review. They are now
   broadly defensible, but with two corrections: the reduction should protect **intensity** rather than trim it
   evenly,[^60] and the illness rule should key on **excessive fatigue**, the strongest predictor of prolonged
   return — ahead of fever, which the skill currently treats as the trigger.[^62] **Action:** cite §8 from the
   adjustment rules, keep one quality session in compressed weeks, and ask about fatigue explicitly.
8. **Sleep was collected and discarded.** `DailyWellness` stores sleep duration, deep sleep and a sleep score,
   and the readiness endpoint already gates on the score — with no cited basis for the threshold and no guidance
   on which fields to believe. **Action:** treat sleep as a training variable in the profile, label the score
   threshold a heuristic (as ACWR now is), stop using `deep_sleep_s` for decisions (stage assessment is
   inconsistent and Garmin specifically underperformed), and require a multi-day trend since accuracy is worst on
   disrupted nights.[^69][^71]
9. **The athlete's own voice is under-weighted relative to the sensors.** The app now stores `perceived_exertion`
   and `feel`, and the monitoring evidence says subjective measures track load *better* than objective ones and
   **do not correlate** with them. **Action:** compute session-RPE from data already held,[^64] and treat athlete
   report as a primary channel — not a confirmation step — when it disagrees with HRV or sleep scores.[^72]
10. **Cold-water immersion could contradict the review's own strength advice.** The review prescribes 2×/week
   strength (§6) and now hot immersion (§13); habitual ice baths would blunt the former (SMD −0.60) while leaving
   running untouched. **Action:** never present immersion as one undifferentiated "recovery" tool.[^73][^74]

## 17. Limitations

This is a narrative/scoping synthesis, not a formal PRISMA meta-analysis; no formal risk-of-bias scoring
or dual screening was performed. Much elite-training evidence is descriptive/observational (case series of
world-class athletes), and several controlled trials are short (≤16 weeks) with modest samples. Female
athletes remain under-represented and several menstrual-cycle findings rest on low-quality evidence.
The heat literature carries its own caveats: the field is methodologically heterogeneous enough that the
principal meta-analysis flags persistent uncertainty about the magnitude and time course of adaptation;[^39]
much of the transfer-to-cool and haematological evidence comes from **cyclists** in small samples (n ≈ 7–23)
rather than runners;[^44][^48] the pooled passive-heat evidence is graded **low-to-very-low certainty**;[^52]
and the marathon dose–response, while large-scale, is **observational** and cannot separate weather from
the pacing decisions it provokes.[^42]
The newer sections inherit similar limits. The **maintenance-dose** figures come from general populations, and
their authors state explicitly that the data are insufficient for athlete-specific recommendations.[^60] The
**detraining** kinetics rest on small classic studies of complete cessation (n = 7), which is not what a busy
week looks like.[^59] The headline **sleep-extension** result is n = 11, uncontrolled, and measured on
basketball skills rather than endurance,[^68] while the sleep–injury association comes from a retrospective
adolescent survey whose confidence interval touches 1.0.[^69] **Device-validation** data come from a
non-athlete laboratory sample.[^71] These support a direction of travel, not precise prescriptions — which is
again why plans should be built from the individual athlete's data.
Effect sizes for many interventions are small and individually variable — reinforcing the app's core
design principle of **building plans from the individual athlete's data and profile, not generic tables.**

---

## References

[^1]: Seiler S. What is best practice for training intensity and duration distribution in endurance athletes? *Int J Sports Physiol Perform.* 2010;5(3):276–291. https://doi.org/10.1123/ijspp.5.3.276

[^2]: Stöggl T, Sperlich B. Polarized training has greater impact on key endurance variables than threshold, high intensity, or high volume training. *Front Physiol.* 2014;5:33. https://doi.org/10.3389/fphys.2014.00033

[^3]: Kenneally M, Casado A, Santos-Concejero J. The effect of periodization and training intensity distribution on middle- and long-distance running performance: a systematic review. *Int J Sports Physiol Perform.* 2018;13(9):1114–1121. https://doi.org/10.1123/ijspp.2017-0327

[^4]: Filipas L, Bonato M, Gallo G, Codella R. Effects of 16 weeks of pyramidal and polarized training intensity distributions in well-trained endurance runners. *Scand J Med Sci Sports.* 2022;32(3):498–511. https://doi.org/10.1111/sms.14101

[^5]: Silva Oliveira R, et al. Comparison of polarized versus other types of endurance training intensity distribution on athletes' endurance performance: a systematic review with meta-analysis. *Sports Med.* 2024;54(11):2817–2839. https://doi.org/10.1007/s40279-024-02034-z

[^6]: Kelemen B, et al. The Norwegian double-threshold method in distance running: systematic literature review. *Sci J Sport Perform.* 2023. https://doi.org/10.55860/nbxv4075

[^7]: Sandbakk Ø, et al. Best-practice training characteristics within Olympic endurance sports. *Sports Med Open.* 2025;11:35. https://doi.org/10.1186/s40798-025-00848-3

[^8]: Billat LV. Interval training for performance: a scientific and empirical practice. *Sports Med.* 2001;31(1):13–31. https://doi.org/10.2165/00007256-200131010-00002

[^9]: Buchheit M, Laursen PB. High-intensity interval training, solutions to the programming puzzle: Part I. *Sports Med.* 2013;43(5):313–338. https://doi.org/10.1007/s40279-013-0029-x

[^10]: Pettitt RW. Applying the critical speed concept to racing strategy and interval training prescription. *Int J Sports Physiol Perform.* 2016;11(7):842–847. https://doi.org/10.1123/ijspp.2016-0001

[^11]: Jones AM, Vanhatalo A, Burnley M, Morton RH, Poole DC. Critical power: implications for determination of VO₂max and exercise tolerance. *Med Sci Sports Exerc.* 2010;42(10):1876–1890. https://doi.org/10.1249/mss.0b013e3181d9cf7f

[^12]: Jones AM, Burnley M, Black MI, Poole DC, Vanhatalo A. The maximal metabolic steady state: redefining the "gold standard". *Physiol Rep.* 2019;7(10):e14098. https://doi.org/10.14814/phy2.14098

[^13]: Maunder E, Seiler S, Mildenhall MJ, Kilding AE, Plews DJ. The importance of "durability" in the physiological profiling of endurance athletes. *Sports Med.* 2021;51(8):1619–1628. https://doi.org/10.1007/s40279-021-01459-0

[^14]: Jones AM. The fourth dimension: physiological resilience as an independent determinant of endurance exercise performance. *J Physiol.* 2024;602(17):4113–4128. https://doi.org/10.1113/jp284205

[^15]: Hunter B, Maunder E, Jones AM. Durability as an index of endurance exercise performance: methodological considerations. *Exp Physiol.* 2025. https://doi.org/10.1113/ep092120

[^16]: Jones AM, et al. Physiological resilience: what is it and how might it be trained? *Scand J Med Sci Sports.* 2025;35(1):e70032. https://doi.org/10.1111/sms.70032

[^17]: Barnes KR, Kilding AE. Running economy: measurement, norms, and determining factors. *Sports Med Open.* 2015;1:8. https://doi.org/10.1186/s40798-015-0007-y

[^18]: Blagrove RC, Howatson G, Hayes PR. Effects of strength training on the physiological determinants of middle- and long-distance running performance: a systematic review. *Sports Med.* 2018;48(5):1117–1149. https://doi.org/10.1007/s40279-017-0835-7

[^19]: Denadai BS, de Aguiar RA, de Lima LCR, Greco CC, Caputo F. Explosive training and heavy weight training are effective for improving running economy in endurance athletes: a systematic review and meta-analysis. *Sports Med.* 2017;47(3):545–554. https://doi.org/10.1007/s40279-016-0604-z

[^20]: Llanos-Lagos C, Ramirez-Campillo R, Moran J, Sáez de Villarreal E. Effect of strength training programs in middle- and long-distance runners' economy at different running speeds: a systematic review with meta-analysis. *Sports Med.* 2024;54(4):895–932. https://doi.org/10.1007/s40279-023-01978-y

[^21]: Hoogkamer W, Kipp S, Frank JH, Farina EM, Luo G, Kram R. A comparison of the energetic cost of running in marathon racing shoes. *Sports Med.* 2018;48(4):1009–1019. https://doi.org/10.1007/s40279-017-0811-2

[^22]: Kobayashi EN, de Toledo RRF, de Almeida MO, Sprey JWC, Jorge PB. Metabolic effects of carbon-plated running shoes: a systematic review and meta-analysis. *Front Sports Act Living.* 2026;7:1710224. https://doi.org/10.3389/fspor.2025.1710224

[^23]: Midgley AW, McNaughton LR, Jones AM. Training to enhance the physiological determinants of long-distance running performance. *Sports Med.* 2007;37(10):857–880. https://doi.org/10.2165/00007256-200737100-00003

[^24]: Bosquet L, Montpetit J, Arvisais D, Mujika I. Effects of tapering on performance: a meta-analysis. *Med Sci Sports Exerc.* 2007;39(8):1358–1365. https://doi.org/10.1249/mss.0b013e31806010e0

[^25]: Wang Z, et al. Effects of tapering on performance in endurance athletes: a systematic review and meta-analysis. *PLoS One.* 2023;18(5):e0282838. https://doi.org/10.1371/journal.pone.0282838

[^26]: Bourdon PC, Cardinale M, Murray A, et al. Monitoring athlete training loads: consensus statement. *Int J Sports Physiol Perform.* 2017;12(s2):S2-161–S2-170. https://doi.org/10.1123/ijspp.2017-0208

[^27]: Impellizzeri FM, Woodcock S, Coutts AJ, Fanchini M, McCall A, Vigotsky AD. Acute:chronic workload ratio: conceptual issues and fundamental pitfalls. *Int J Sports Physiol Perform.* 2020;15(6):907–913. https://doi.org/10.1123/ijspp.2019-0864

[^28]: Impellizzeri FM, Tenan MS, Kempton T, Novak A, Coutts AJ. What role do chronic workloads play in the acute to chronic workload ratio? Time to dismiss ACWR and its underlying theory. *Sports Med.* 2020;50(3):581–592. https://doi.org/10.1007/s40279-020-01378-6

[^29]: Lolli L, Batterham AM, Hawkins R, et al. Mathematical coupling causes spurious correlation within the conventional acute-to-chronic workload ratio calculations. *Br J Sports Med.* 2019;53(15):921–922. https://doi.org/10.1136/bjsports-2017-098110

[^30]: Manresa-Rocamora A, Sarabia JM, Sánchez-Meca J, et al. Heart rate variability-guided training for enhancing cardiac-vagal modulation, aerobic fitness, and endurance performance: a systematic review with meta-analysis. *Int J Environ Res Public Health.* 2021;18(19):10299. https://doi.org/10.3390/ijerph181910299

[^31]: Düking P, Zinner C, Reed JL, Holmberg HC, Sperlich B. Monitoring and adapting endurance training on the basis of heart rate variability monitored by wearable technologies: a systematic review with meta-analysis. *J Sci Med Sport.* 2021;24(11):1180–1192. https://doi.org/10.1016/j.jsams.2021.04.012

[^32]: Impey SG, Hearris MA, Hammond KM, et al. Fuel for the work required: a theoretical framework for carbohydrate periodization and the glycogen threshold hypothesis. *Sports Med.* 2018;48(5):1031–1048. https://doi.org/10.1007/s40279-018-0867-7

[^33]: Gejl KD, Nybo L. Performance effects of periodized carbohydrate restriction in endurance trained athletes: a systematic review and meta-analysis. *J Int Soc Sports Nutr.* 2021;18(1):37. https://doi.org/10.1186/s12970-021-00435-3

[^34]: Jeukendrup AE. A step towards personalized sports nutrition: carbohydrate intake during exercise. *Sports Med.* 2014;44(Suppl 1):S25–S33. https://doi.org/10.1007/s40279-014-0148-z

[^35]: McNulty KL, Elliott-Sale KJ, Dolan E, et al. The effects of menstrual cycle phase on exercise performance in eumenorrheic women: a systematic review and meta-analysis. *Sports Med.* 2020;50(10):1813–1827. https://doi.org/10.1007/s40279-020-01319-3

[^36]: Mountjoy M, Ackerman KE, Bailey DM, et al. 2023 International Olympic Committee's (IOC) consensus statement on Relative Energy Deficiency in Sport (REDs). *Br J Sports Med.* 2023;57(17):1073–1098. https://doi.org/10.1136/bjsports-2023-106994

[^37]: Périard JD, Racinais S, Sawka MN. Adaptations and mechanisms of human heat acclimation: applications for competitive athletes and sports. *Scand J Med Sci Sports.* 2015;25(Suppl 1):20–38. https://doi.org/10.1111/sms.12408

[^38]: Racinais S, Alonso JM, Coutts AJ, et al. Consensus recommendations on training and competing in the heat. *Scand J Med Sci Sports.* 2015;25(Suppl 1):6–19. https://doi.org/10.1111/sms.12467

[^39]: Tyler CJ, Reeve T, Hodges GJ, Cheung SS. The effects of heat adaptation on physiology, perception and exercise performance in the heat: a meta-analysis. *Sports Med.* 2016;46(11):1699–1724. https://doi.org/10.1007/s40279-016-0538-5

[^40]: Daanen HAM, Racinais S, Périard JD. Heat acclimation decay and re-induction: a systematic review and meta-analysis. *Sports Med.* 2018;48(2):409–430. https://doi.org/10.1007/s40279-017-0808-x

[^41]: Cramer MN, Gagnon D, Laitano O, Crandall CG. Human temperature regulation under heat stress in health, disease, and injury. *Physiol Rev.* 2022;102(4):1907–1989. https://doi.org/10.1152/physrev.00047.2021

[^42]: Ely MR, Cheuvront SN, Roberts WO, Montain SJ. Impact of weather on marathon-running performance. *Med Sci Sports Exerc.* 2007;39(3):487–493. https://doi.org/10.1249/mss.0b013e31802d3aba

[^43]: Lorenzo S, Halliwill JR, Sawka MN, Minson CT. Heat acclimation improves exercise performance. *J Appl Physiol.* 2010;109(4):1140–1147. https://doi.org/10.1152/japplphysiol.00495.2010

[^44]: Keiser S, Flück D, Hüppin F, Stravs A, Hilty MP, Lundby C. Heat training increases exercise capacity in hot but not in temperate conditions: a mechanistic counter-balanced cross-over study. *Am J Physiol Heart Circ Physiol.* 2015;309(5):H750–H761. https://doi.org/10.1152/ajpheart.00138.2015

[^45]: Minson CT, Cotter JD. CrossTalk proposal: heat acclimatization does improve performance in a cool condition. *J Physiol.* 2016;594(2):241–243. https://doi.org/10.1113/JP270879

[^46]: Nybo L, Lundby C. CrossTalk opposing view: heat acclimatization does not improve exercise performance in a cool condition. *J Physiol.* 2016;594(2):245–247. https://doi.org/10.1113/JP270880

[^47]: Périard JD, Nichols D, Travers G, Cocking S, Townsend N, Brown H, Racinais S. Impact of exercise heat acclimation on performance in hot, cool and hypoxic conditions. *J Sci Sport Exerc.* 2024;6(3):275–287. https://doi.org/10.1007/s42978-024-00300-0

[^48]: Rønnestad BR, Hamarsland H, Hansen J, et al. Five weeks of heat training increases haemoglobin mass in elite cyclists. *Exp Physiol.* 2021;106(1):316–327. https://doi.org/10.1113/EP088544

[^49]: Lundby C, Robach P. Altitude or heat training to increase haemoglobin mass and endurance exercise performance in elite sport. *J Physiol.* 2025. https://doi.org/10.1113/JP287700

[^50]: Zurawlew MJ, Walsh NP, Fortes MB, Potter C. Post-exercise hot water immersion induces heat acclimation and improves endurance exercise performance in the heat. *Scand J Med Sci Sports.* 2016;26(7):745–754. https://doi.org/10.1111/sms.12638

[^51]: Kirby NV, Lucas SJE, Armstrong OJ, Weaver SR, Lucas RAI. Intermittent post-exercise sauna bathing improves markers of exercise capacity in hot and temperate conditions in trained middle-distance runners. *Eur J Appl Physiol.* 2021;121(2):621–635. https://doi.org/10.1007/s00421-020-04541-z

[^52]: Solomon TPJ, Laye MJ. The effect of post-exercise heat exposure (passive heat acclimation) on endurance exercise performance: a systematic review and meta-analysis. *BMC Sports Sci Med Rehabil.* 2025;17(1):4. https://doi.org/10.1186/s13102-024-01038-6

[^53]: Kelly MK, Bowe SJ, Jardine WT, et al. Heat adaptation for females: a systematic review and meta-analysis of physiological adaptations and exercise performance in the heat. *Sports Med.* 2023;53(7):1395–1421. https://doi.org/10.1007/s40279-023-01831-2

[^54]: van de Kerkhof TM, Bongers CCWG, Périard JD, Eijsvogels TMH. Performance benefits of pre- and per-cooling on self-paced versus constant workload exercise: a systematic review and meta-analysis. *Sports Med.* 2024;54(2):447–471. https://doi.org/10.1007/s40279-023-01940-y

[^55]: Racinais S, Hosokawa Y, Akama T, et al. IOC consensus statement on recommendations and regulations for sport events in the heat. *Br J Sports Med.* 2023;57(1):8–25. https://doi.org/10.1136/bjsports-2022-105942

[^56]: Casa DJ, DeMartini JK, Bergeron MF, et al. National Athletic Trainers' Association position statement: exertional heat illnesses. *J Athl Train.* 2015;50(9):986–1000. https://doi.org/10.4085/1062-6050-50.9.07

[^57]: Mujika I, Padilla S. Detraining: loss of training-induced physiological and performance adaptations. Part I: short term insufficient training stimulus. *Sports Med.* 2000;30(2):79–87. https://doi.org/10.2165/00007256-200030020-00002

[^58]: Mujika I, Padilla S. Detraining: loss of training-induced physiological and performance adaptations. Part II: long term insufficient training stimulus. *Sports Med.* 2000;30(3):145–154. https://doi.org/10.2165/00007256-200030030-00001

[^59]: Coyle EF, Martin WH, Sinacore DR, Joyner MJ, Hagberg JM, Holloszy JO. Time course of loss of adaptations after stopping prolonged intense endurance training. *J Appl Physiol.* 1984;57(6):1857–1864. https://doi.org/10.1152/jappl.1984.57.6.1857

[^60]: Spiering BA, Mujika I, Sharp MA, Foulis SA. Maintaining physical performance: the minimal dose of exercise needed to preserve endurance and strength over time. *J Strength Cond Res.* 2021;35(5):1449–1458. https://doi.org/10.1519/JSC.0000000000003964

[^61]: Schwellnus M, Adami PE, Bougault V, et al. International Olympic Committee (IOC) consensus statement on acute respiratory illness in athletes part 1: acute respiratory infections. *Br J Sports Med.* 2022;56(19):1066–1088. https://doi.org/10.1136/bjsports-2022-105759

[^62]: Schwellnus M, Sewry N, Snyders C, et al. Symptom cluster is associated with prolonged return-to-play in symptomatic athletes with acute respiratory illness (including COVID-19): a cross-sectional study — AWARE study I. *Br J Sports Med.* 2021;55(20):1144–1152. https://doi.org/10.1136/bjsports-2020-103782

[^63]: Kaulback K, Pyne DB, Hull JH, Snyders C, Sewry N, Schwellnus M. The effects of acute respiratory illness on exercise and sports performance outcomes in athletes — a systematic review by a subgroup of the IOC consensus group on "acute respiratory illness in the athlete". *Eur J Sport Sci.* 2023;23(7):1356–1374. https://doi.org/10.1080/17461391.2022.2089914

[^64]: Foster C, Florhaug JA, Franklin J, et al. A new approach to monitoring exercise training. *J Strength Cond Res.* 2001;15(1):109–115. https://doi.org/10.1519/00124278-200102000-00019

[^65]: Foster C. Monitoring training in athletes with reference to overtraining syndrome. *Med Sci Sports Exerc.* 1998;30(7):1164–1168. https://doi.org/10.1097/00005768-199807000-00023

[^66]: Haddad M, Stylianides G, Djaoui L, Dellal A, Chamari K. Session-RPE method for training load monitoring: validity, ecological usefulness, and influencing factors. *Front Neurosci.* 2017;11:612. https://doi.org/10.3389/fnins.2017.00612

[^67]: Fullagar HHK, Skorski S, Duffield R, Hammes D, Coutts AJ, Meyer T. Sleep and athletic performance: the effects of sleep loss on exercise performance, and physiological and cognitive responses to exercise. *Sports Med.* 2015;45(2):161–186. https://doi.org/10.1007/s40279-014-0260-0

[^68]: Mah CD, Mah KE, Kezirian EJ, Dement WC. The effects of sleep extension on the athletic performance of collegiate basketball players. *Sleep.* 2011;34(7):943–950. https://doi.org/10.5665/sleep.1132

[^69]: Milewski MD, Skaggs DL, Bishop GA, et al. Chronic lack of sleep is associated with increased sports injuries in adolescent athletes. *J Pediatr Orthop.* 2014;34(2):129–133. https://doi.org/10.1097/BPO.0000000000000151

[^70]: Walsh NP, Halson SL, Sargent C, et al. Sleep and the athlete: narrative review and 2021 expert consensus recommendations. *Br J Sports Med.* 2021;55(7):356–368. https://doi.org/10.1136/bjsports-2020-102025

[^71]: Chinoy ED, Cuellar JA, Huwa KE, et al. Performance of seven consumer sleep-tracking devices compared with polysomnography. *Sleep.* 2021;44(5):zsaa291. https://doi.org/10.1093/sleep/zsaa291

[^72]: Saw AE, Main LC, Gastin PB. Monitoring the athlete training response: subjective self-reported measures trump commonly used objective measures: a systematic review. *Br J Sports Med.* 2016;50(5):281–291. https://doi.org/10.1136/bjsports-2015-094758

[^73]: Roberts LA, Raastad T, Markworth JF, et al. Post-exercise cold water immersion attenuates acute anabolic signalling and long-term adaptations in muscle to strength training. *J Physiol.* 2015;593(18):4285–4301. https://doi.org/10.1113/JP270570

[^74]: Malta ES, Dutra YM, Broatch JR, Bishop DJ, Zagatto AM. The effects of regular cold-water immersion use on training-induced changes in strength and endurance performance: a systematic review with meta-analysis. *Sports Med.* 2021;51(1):161–174. https://doi.org/10.1007/s40279-020-01362-0
