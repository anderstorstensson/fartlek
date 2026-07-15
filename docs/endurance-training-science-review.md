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
- The app's **ACWR safety rail (0.8–1.3) rests on contested science**: the ratio has been
  shown to have serious statistical and conceptual flaws. It should be treated as a soft
  heuristic, with absolute weekly ramp and consistency given more weight.[^27][^28][^29]

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
periodization and tapering; load monitoring and the ACWR critique; HRV-guided training;
carbohydrate periodization and race fuelling; the female endurance athlete and RED-S.

**Citation integrity.** Every reference's metadata (authors, year, journal, DOI) was retrieved
from CrossRef rather than reproduced from memory, and DOIs were verified to resolve. Author
concept-names were used only as search seeds. 36 references are cited; the majority are
Tier-1/Tier-2 sports-medicine and physiology venues (*Sports Medicine*, *IJSPP*, *BJSM*,
*J Physiol*, *Scand J Med Sci Sports*), most with high citation counts.

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

## 8. Load monitoring and the ACWR critique

**Concept.** Internal (HR-based TRIMP, HR-TSS) and external/pace-based (rTSS) load metrics, integrated
over time into fitness (CTL), fatigue (ATL) and form (TSB), are used to titrate progression and flag
injury risk. The **acute:chronic workload ratio (ACWR)** compares recent (~7-day) to chronic (~28/42-day)
load, with a "sweet spot" (~0.8–1.3) promoted as protective.[^26]

**Evidence.** Consensus supports systematically monitoring load and quantifying both external and
internal load, but stresses that no single metric is definitive and that the internal response (HR, RPE)
is what drives adaptation.[^26] Crucially, **the ACWR has been substantially challenged**: it has
conceptual and statistical flaws — mathematical coupling between numerator and denominator produces
**spurious correlations**, ratio metrics are noisy and create statistical artifacts, the acute/chronic
time windows are arbitrary, and the widely reproduced "sweet-spot" risk figure has been criticised as
methodologically unsound; no study has properly estimated a **causal** effect of manipulating ACWR on
injury.[^27][^28][^29]

**Implication for plan-building.**
- **Keep CTL/ATL/TSB and absolute ramp rate as the primary progression controls** (weekly volume growth
  ≤~10%, CTL ramp ≤~5/week, down week every ~4th). These are more defensible than any ratio.[^26]
- **Demote ACWR (ATL/CTL ~0.8–1.3) to a soft, secondary heuristic** and label it as such in any
  athlete-facing rationale. Do not present the 0.8–1.3 band as a validated injury threshold; the science
  under that rail has moved.[^27][^28][^29]
- Weight **consistency, sudden spikes, and monotony** (many identical-load days) at least as heavily as
  any workload ratio.[^26]
- Never mix load scales (TRIMP vs TSS families) when trending — compare within one model.[^26]

---

## 9. Recovery, HRV-guided load, and monotony

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

## 10. Fuelling: carbohydrate periodization and race intake

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

## 11. The female endurance athlete and RED-S

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

## 12. Synthesis: an evidence map for the plan generator

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
| Readiness | HRV/wellness as a modifier to defer hard days; reduces negative responders | [^30][^31] |
| Taper | 2–3 wk, volume −40–60%, hold intensity & frequency | [^24][^25] |
| Fuelling | Fuel quality/long sessions; race 60–90 g·h⁻¹ rehearsed in training | [^32][^33][^34] |
| Female athlete / REDs | Individualise cycle effects; screen low energy availability first | [^35][^36] |

## 13. Where the evidence has moved under the app's current rails

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

## 14. Limitations

This is a narrative/scoping synthesis, not a formal PRISMA meta-analysis; no formal risk-of-bias scoring
or dual screening was performed. Much elite-training evidence is descriptive/observational (case series of
world-class athletes), and several controlled trials are short (≤16 weeks) with modest samples. Female
athletes remain under-represented and several menstrual-cycle findings rest on low-quality evidence.
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
