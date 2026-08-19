---
title: "Running Injury Prevention and Management for Recreational Distance Runners"
subtitle: "An evidence synthesis, tiered by certainty, for a coaching agent that is not a clinician"
author: "Fartlek project — literature review"
date: "2026-07-31"
---

# Running Injury Prevention and Management

**A tiered evidence synthesis for the physio-guidance side of the coaching agent**

## Executive summary

This review is the third in the Fartlek project's evidence base, alongside
`endurance-training-science-review.md` (training design) and `sports-nutrition-review.md` (fuelling and
supplements). Those two tell the coach how to make an athlete faster. This one covers what to do when
something hurts — and, more importantly, where the coach must stop and hand over.

Every claim carries an explicit **certainty label**, because this field's evidence is systematically
weaker than the sports-nutrition literature and an automated coach that speaks about a rehabilitation
protocol in the same confident register as a well-established one can do real harm.

Headline conclusions:

- **Previous injury is the strongest known risk factor** — roughly a doubling of risk — and it is the
  single most valuable thing the app can know about an athlete.[^3][^5][^7] This is the evidence-based
  case for storing structured injury history rather than leaving it in free-text notes.
- **No metric predicts injury in an individual, and none ever will.** Risk estimation and prediction are
  different things; screening tests do not have the properties required.[^18] The app may manage load;
  it must never present a risk score as a forecast.
- **The 10% rule failed its randomised trial** (20.8% vs 20.3% injured).[^10] The threshold with actual
  data behind it is **>30% weekly-distance change over 2 weeks**.[^9] And progressing volume versus
  progressing intensity made no difference to injury risk in a direct RCT.[^11]
- **The ACWR safety rail is not a safety rail.** Its associations arise even when no true relationship
  exists, no protective 0.8–1.3 "sweet spot" is supported, and the one large study in *runners* found the
  opposite curve shape to the model's prediction.[^13][^14][^15][^16] This matches endurance §9's
  conclusion and must not be presented to athletes as a validated threshold.
- **Overuse injuries may not be gradual at all.** The Garmin-RUNSAFE cohort traced a majority of them to
  a **single session**.[^17] If that holds, catching the one bad run matters more than smoothing the
  four-week ramp — the strongest argument for a niggle-reporting feature.
- **Progressive tendon loading is the best-evidenced protocol in this document** — eccentric or heavy
  slow resistance, 12 weeks, first-line, with **no adjunct beating exercise alone** and shockwave
  explicitly not routine.[^44][^46][^47][^49] Mid-portion and insertional Achilles tendinopathy need
  *different* protocols.[^39]
- **The Silbernagel pain-monitoring model is the most operationally useful rule here**: pain up to 5/10
  is acceptable during loading, may reach 5/10 afterwards but must settle to baseline by the following
  morning, and baseline must not rise week to week.[^43] It is what allows an athlete to keep running
  through a tendinopathy, and it maps directly onto a daily check-in — but these three numbers carry
  secondary-source provenance and must be verified at source before being hard-coded (§8, §18).
- **Strength training is the best-evidenced prevention in sport generally (RR 0.315) — but the
  runner-specific pooled evidence is null.**[^68][^69][^70][^71] What separated effective from
  ineffective trials was **supervision**, not programme content.[^70] For an app, the analogue of
  supervision is scheduling, reminders and follow-up — a software problem, and the most actionable
  finding in this review.
- **Several popular interventions do not survive contact with the evidence**: static stretching for
  injury prevention (RR 0.963),[^68][^74] shock-absorbing insoles (null on every outcome),[^81]
  pronation- and arch-based shoe prescription (>7000 recruits, no effect),[^76] and cadence retraining as
  injury prevention (37 studies, only 2 measured injury).[^75] Changing biomechanics is not the same
  claim as preventing injury.
- **Bone stress injury is where the coach must get out of the way.** High-risk sites — anterior tibial
  cortex, femoral neck, navicular — risk non-union; the "dreaded black line" showed 93% non-union with
  conservative management.[^25][^26] Focal bone tenderness is a referral, not a training adjustment.
- **The binding constraint on this whole document is §15 (red flags).** The coach recognises patterns,
  manages load, and refers. It does not diagnose.

---

## 1. Scope, method, and boundaries with the sibling reviews

**Objective.** Summarise the defensible evidence on why recreational distance runners get hurt, what
actually reduces that risk, and how a coaching agent should modify training when an athlete reports a
niggle or an injury — tiered so that the coach can distinguish "this is well established" from "this is
plausible but unproven" from "this is popular and wrong".

**Type.** Narrative / scoping synthesis, not a PRISMA meta-analysis — as with its two sibling reviews, the
goal is usable, gradeable guidance rather than a pooled effect estimate.

**The boundary this review must not cross.** The other two reviews advise a coach. This one borders on
advising a *clinician*, and it does not cross that line. Nothing here is a diagnosis, and the coach that
cites it must not offer one. What this document licenses is: recognising patterns, managing **load**
around them, applying published self-monitoring rules, and knowing when to stop and refer. §15 (red flags)
is the binding constraint on everything else in the document.

**Boundary with `endurance-training-science-review.md` and `sports-nutrition-review.md`.** This review
overlaps both siblings more than they overlap each other. It declares and cross-references rather than
restating:

| Topic | Lives in |
|---|---|
| Load metrics themselves (TRIMP, rTSS, sRPE, CTL/ATL/TSB), and the ACWR critique | endurance §9 |
| Load *as a modifiable injury risk factor*, and ramp rules written for injury rather than adaptation | **here** |
| Strength training for **running economy** | endurance §6 |
| Strength training for **injury prevention** — different evidence base, same intervention | **here** |
| Sleep, readiness monitoring, and the athlete's subjective report | endurance §11 |
| Energy availability and REDs as a performance/health syndrome | endurance §14 |
| Low energy availability as a **bone stress injury** risk factor | **here** |
| Iron, vitamin D, calcium as nutrition topics | nutrition §16 |
| Vitamin D/calcium as **stress-fracture prevention** | **here** |
| Collagen/gelatin for connective tissue | nutrition §17 |
| Detraining and the cost of interrupted training | endurance §8 |
| Return-to-running progressions after injury | **here** |
| Footwear for **economy** ("super shoes") | endurance §6 |
| Footwear for **injury prevention** (cushioning, pronation, minimalism) | **here** |

Where the two overlap, the sibling is authoritative for its own framing and this document
cross-references it rather than duplicating numbers.

**Search.** Targeted per-theme searches (July 2026) across scholarly sources, prioritising clinical
practice guidelines and consensus statements, then systematic reviews and meta-analyses, then landmark
primary trials and prospective cohorts where no synthesis exists.

**Citation integrity.** Same protocol as the nutrition review: every reference was first located in live
literature search, then its metadata retrieved from CrossRef — no citation was reconstructed from memory
and no DOI was guessed. The retrieval script is `docs/sources/fetch_injury_bib.py` and the resolution
result is `running-injury-review_citation_report.json`.

**What that verification does and does not cover.** DOI resolution confirms a citation points at a real
paper with the stated authors, journal and year. It does *not* confirm that a quoted number appears in
that paper. This matters more here than in either sibling review, because this field is unusually full of
famous, frequently-misquoted numbers — protocol parameters, risk-reduction percentages, incidence rates.
Numbers that were checked against the source abstract rather than a search summary are marked as such in
the text.

**How to read each theme.** *Concept → Evidence → Certainty → Implication for coaching.*

---

## 2. The certainty scheme — read this before advising anything

**Concept.** The failure mode for an automated coach in this domain is not being wrong about a
supplement, it is speaking about a *rehabilitation protocol* with a confidence the evidence does not
carry, and thereby delaying care. Musculoskeletal rehabilitation evidence is systematically weaker than
the sports-nutrition evidence in the sibling review: trials are small, rarely blinded, control conditions
are inconsistent, and the outcome (pain) is subjective. A tier scheme copied from the AIS supplement
framework would flatter it. This review therefore uses a GRADE-flavoured certainty label.

| Certainty | Meaning | How the coach should speak about it |
|---|---|---|
| **High** | Consistent evidence from multiple good syntheses; further research unlikely to overturn the direction of effect | State it as established; may act on it directly |
| **Moderate** | Reasonable synthesis-level support, but limited by trial quality, small samples, or population mismatch | Recommend, while naming the uncertainty |
| **Low** | Sparse, conflicting, or indirect evidence; widely practised on rationale more than proof | Offer as a reasonable option, explicitly flagged as not well proven |
| **Very low / contested** | Evidence is absent, or good evidence points the other way | Do not recommend; say plainly the evidence does not support it |
| **Referral** | Not an evidence question — a safety boundary | Stop advising and direct the athlete to a clinician |

Per `AGENTS.md`'s convention for the nutrition review, **the certainty label must be stated whenever the
recommendation is named** to the athlete. "Do heavy slow resistance work for that tendon" and "try
shockwave" are not the same claim and must not sound alike.

An additional caveat applies to every certainty label in this document: most of it is **borrowed
evidence**. Much of the prevention literature is drawn from military recruits and team-sport athletes,
and much of the rehabilitation literature from mixed clinical populations rather than recreational
distance runners specifically. Where a recommendation rests on borrowed evidence, that is stated, and it
caps the certainty at Moderate regardless of how good the original trial was.

---

## 3. How often runners get hurt — and why every number disagrees

**Concept.** Before the coach can say anything useful about risk, it has to know how big the risk is.
The literature's headline numbers range from "one runner in five" to "four runners in five", which
looks like disagreement about reality but is mostly disagreement about **definition**.

**Evidence.**

- **The definition problem is the dominant source of variance.** The seminal systematic review of
  long-distance runners found lower-extremity injury incidence ranging from **19.4% to 79.3%** across
  studies — a spread driven largely by whether "injury" meant any ache, a training interruption, or a
  medical consultation.[^3] A modified Delphi process closed this by producing a consensus definition:
  *running-related musculoskeletal pain in the lower limbs causing a restriction of or stoppage of
  running (distance, speed, duration, or training) for at least 7 days or 3 consecutive scheduled
  training sessions, or requiring the runner to consult a physician or other health professional*.[^1]
- **Exposure-normalised incidence is the more stable currency.** Meta-analysis of 13 prospective studies
  gives **7.7 injuries per 1000 h of running (95% CI 6.9–8.7) in recreational runners** and **17.8 per
  1000 h (95% CI 16.7–19.1) in novice runners** — novices are hurt at roughly **2.3× the rate** of
  established recreational runners.[^2] Expressed per distance, the pooled estimate is **1.07 injuries
  per 1000 km (95% CI 1.01–1.13)**.[^2]
- **Annual risk for a recreational runner is roughly one-in-two.** A one-year prospective cohort of 224
  recreational runners found a cumulative incidence of **45.9% (95% CI 38.4–54.2)**.[^5]
- **Injuries concentrate below the knee, plus the knee itself.** Across ~3500 runners, the most common
  specific diagnoses were **medial tibial stress syndrome (incidence 13.6–20.0%)**, **Achilles
  tendinopathy (9.1–10.9%)** and **plantar fasciitis (4.5–10.0%)**; the knee is consistently the single
  most-affected region.[^4][^3]

**Certainty. High** for the qualitative claims (novices are at higher risk; injuries cluster at knee,
shin, Achilles and foot; definition drives the numbers). **Moderate** for any specific incidence figure,
because it is definition- and population-bound.

**Implication for coaching.**

- **Never quote a bare incidence number to the athlete.** "About half of recreational runners have a
  running-interrupting injury in a year"[^5] is defensible; "80% of runners get injured" is a definition
  artefact.[^3]
- **Normalise risk talk to exposure, not calendar time.** The app already stores duration and distance
  per activity, so per-1000-h and per-1000-km framings are directly computable and are what the
  literature actually supports.[^2]
- **Treat a returning or beginning runner as a distinct risk class.** The novice/recreational gap is one
  of the largest and best-replicated effects in this literature.[^2] The same logic applies to a runner
  restarting after a layoff — see endurance §8 on how little fitness is actually lost, which is the
  argument for restarting conservatively rather than at the old volume.
- **Use the consensus definition internally.** If the app ever logs "injury", it should mean the Delphi
  definition — 7 days or 3 sessions of restriction, or a clinical consultation — so its own history is
  comparable to published risk data.[^1]

---

## 4. Risk factors: what actually predicts trouble

**Concept.** Which athlete-level and training-level factors raise risk, and — separately — whether any
of them can be used to *predict* an injury in an individual. These are different questions and the
literature answers them very differently.

**Evidence.**

- **Previous injury is the strongest and most consistent risk factor.** Recreational runners with a
  history of injury were **twice as likely** to sustain a running-related injury over one year.[^5]
  Systematic reviews across cohorts agree that previous injury is the recurring, strongest
  predictor.[^3][^7]
- **The wider risk-factor literature is real but weak.** A 2024 umbrella review of 13 systematic reviews
  (207 outcomes, 148 primary studies) found that **every included review was rated low or critically low
  quality** — 8 critically low, 5 low, none moderate or high.[^6] Of 131 associations with a reported
  effect measure, 23% were large, 29% medium, 37% small and 11% null.[^6] That is the honest state of the
  field: many associations, little methodological confidence.
- **Body mass and age matter in novices.** In 930 novice runners, **BMI >30 kg·m⁻²**, **age 45–65**, and
  previous non-running injuries were associated with increased risk, while **BMI <20 kg·m⁻²** was
  protective.[^8]
- **Sex differences exist but are not simple.** A review of 15 longitudinal cohorts found women at lower
  overall risk than men, with different risk profiles by sex.[^7] It also found **orthotics/inserts use
  associated with increased risk** — almost certainly confounding by indication (people with problems buy
  orthotics), which is a good illustration of why this literature should not be read causally.[^7]
- **Screening cannot predict injury in an individual.** The decisive critique shows there is no screening
  test with adequate test properties, because even a statistically significant risk marker produces
  massive overlap between the athletes who do and do not get hurt; no intervention study has shown that
  targeting "high-risk" athletes beats treating everyone the same.[^18] **Risk estimation and prediction
  are not the same thing.**[^18]

**Certainty. High** that previous injury is the dominant risk factor.[^3][^5][^7] **High** that
individual-level prediction does not work.[^18] **Low** for essentially every other single risk
factor, given the umbrella review's quality findings.[^6]

**Implication for coaching.**

- **Injury history is the single most valuable thing the app can know about an athlete** — more valuable
  than any biomechanical or wellness metric.[^3][^5][^7] This is the strongest argument for storing
  structured injury history rather than leaving it in free-text notes.
- **Never present a risk factor as a prediction.** The coach may say "runners with your injury history
  are at roughly double the population risk, so we'll progress conservatively";[^5] it must not say "you
  are likely to get injured."[^18]
- **Do not build a screening or risk-score feature and present its output as predictive.** The evidence
  says that cannot work at the individual level.[^18] Load *management* is defensible; risk *scoring* is
  not.
- **Treat a previously injured site as a standing constraint** on how fast that tissue's specific loading
  (impact, hills, speed) is progressed, rather than as a general reason to train less.

---

## 5. Training load as a modifiable risk factor

**Concept.** Load is the one risk factor a coaching app actually controls. The question is what the
evidence licenses it to do with it. Load *metrics* themselves — TRIMP, rTSS, sRPE, CTL/ATL/TSB — and the
statistical critique of the acute:chronic workload ratio are owned by **endurance §9**; this section
covers only load as a cause of injury and the rules that follow.

**Evidence.**

- **The consensus position is that load matters and that rapid change is the risk.** The IOC consensus
  statement on load and injury frames the problem as one of *rapid changes* in load rather than absolute
  load, and recommends systematic monitoring.[^12]
- **The "10% rule" failed its randomised test.** In the GRONORUN trial, 532 novice runners were randomised
  to a standard 8-week programme or a graded 13-week programme built on the 10% rule. Injury incidence was
  **20.8% in the graded group versus 20.3% in the standard group** — no benefit.[^10]
- **The observational signal sits far above 10%.** In 874 novice runners with GPS-verified training,
  progression groups of <10%, 10–30% and >30% weekly-distance change showed **no significant overall
  difference**; only the **>30%** group showed excess *distance-related* injuries (patellofemoral pain,
  ITBS and similar).[^9] So the defensible threshold is "don't jump by a third", not "never exceed 10%".
- **Progressing volume and progressing intensity carry similar risk.** The Run Clever RCT randomised 447
  recreational runners after preconditioning to intensity-focused or volume-focused 16-week progression:
  **16% vs 19% injured**, risk difference −14.0% (95% CI −36.9 to 8.9, p = 0.23) — no difference.[^11]
- **ACWR does not deliver what it promised, and in runners it does not even reproduce.** Simulation shows
  ACWR–injury associations arise even when no true relationship exists,[^13] the analytical degrees of
  freedom are enormous (one review counted 350 hazard ratios from varying windows and metrics),[^13] and
  reviews conclude the limitations "should discourage its use".[^14] A 2021 editorial found **no evidence
  for a protective 0.8–1.3 sweet spot**.[^15] The one large study in *runners* found an **inverse,
  L-shaped** association — the opposite shape to the U-curve the sweet-spot model assumes.[^16] This
  review's conclusion is the same as endurance §9's: **ACWR is a soft heuristic at best and must not be
  presented to the athlete as a validated injury threshold.**
- **The gradual-overload model itself is now contested.** The Garmin-RUNSAFE cohort reports that a
  majority of "overuse" running injuries were **traced to a single session** rather than accumulating
  invisibly over weeks.[^17] If that holds, the highest-value intervention is not smoothing the 4-week
  ramp but **catching the one session that was too much** — and acting on the athlete's report of it
  immediately.

**Certainty. High** that abrupt load increases carry risk and that gradual progression is sensible.[^12]
**High** that the specific 10% rule has no randomised support.[^10] **Moderate** for the >30% threshold
(single observational cohort, novices).[^9] **Very low / contested** for ACWR as an injury-management
tool.[^13][^14][^15][^16]

**Implication for coaching.**

- **Do not defend a plan with the 10% rule.** It failed an RCT.[^10] Use it, if at all, as a loose
  planning convention — never as a safety claim to the athlete.
- **Make >30% weekly-distance change the actual alarm line**, evaluated over a 2-week window as in the
  source cohort.[^9] That is the threshold with data behind it.
- **Do not tell the athlete that shifting from volume to intensity is the safer path** (or vice versa) —
  the direct RCT found no difference.[^11] Both progressions need the same restraint.
- **Never present the ACWR band as a safety threshold in athlete-facing text.**[^13][^14][^15][^16]
  Weight absolute ramp rate, consistency, and the athlete's own report far more heavily, exactly as
  endurance §9 already prescribes.
- **Treat a single bad session as a first-class event.** Given the RUNSAFE finding,[^17] a report of
  "something went wrong in that run" deserves an immediate response, not a note to watch the weekly
  trend. This is the strongest evidence-based argument for the whole niggle-reporting feature.

---

## 6. Bone stress injuries — where the coach must be most conservative

**Concept.** Bone stress injury (BSI) sits on a continuum from stress *reaction* to stress *fracture* to
complete fracture, arising when microdamage accumulates faster than remodelling repairs it.[^19] It is the
injury class where "train through it sensibly" is most dangerous, and where the coach's job is largely to
recognise it and get out of the way.

**Evidence.**

- **Site determines everything.** BSIs divide into **high-risk** sites — femoral neck (tension side),
  patella, **anterior tibial cortex**, medial malleolus, talus, tarsal navicular, proximal fifth
  metatarsal, great toe sesamoids — sharing high tensile load and poor blood supply, and **low-risk**
  sites, chiefly the posteromedial tibia and metatarsal shafts.[^25] High-risk sites carry real danger of
  delayed union, non-union or progression to complete fracture and need aggressive imaging and specialist
  management.[^25] Low-risk tibial and metatarsal diaphyseal injuries account for **more than half of
  BSIs in runners** and are the ones that respond to load management.[^24]
- **The anterior tibial cortex is the sharpest illustration.** The "dreaded black line" — a transverse
  radiolucent line on the tension side of the anterior mid-tibia — represents **5–15% of tibial stress
  fractures**; in one case series conservative management was associated with **93% non-union versus 53%
  with surgery**, and it is easily missed because the usual periosteal reaction is absent.[^26] Shin pain
  is not one entity, and the coach cannot separate these by chat.
- **MRI grading (Fredericson) defines severity but predicts timelines poorly.** The original system runs
  grade 1 (periosteal oedema only) → 2 (marrow oedema on T2) → 3 (marrow oedema on T1 and T2) → 4a/4b
  (intracortical signal abnormality / a linear cortical fracture line).[^20] It has been validated
  against outcomes in 142 tibial stress injuries.[^21] But a cohort of 42 tibial stress fractures found
  **no difference between grades in time to recovery** (mean time to pain resolution 55.6 ± 5.0
  days).[^22] Grade informs severity; it does **not** license the coach to quote a return date.
- **Return to running has usable published criteria.** A scoping review of 50 studies found: complete
  resolution of localised bony tenderness recommended before running by ~40% of sources; radiological
  healing required only for **high-risk** injuries, not low-risk posteromedial tibial ones (clinical
  healing outpaces radiological healing); the **single-leg hop test** described as the most sensitive
  readiness test; and a walk–run progression on alternate days from 30–60 s running intervals,
  **progressing distance before speed**, guided by symptoms.[^23] Required pain-free walking before
  running ranged from 1 mile to 45 minutes across sources.[^23]
- **A concrete trigger exists for low-risk BSI.** Loading should not produce symptoms during, after, or
  **the day following**; a return-to-run programme may begin once the athlete is **pain-free during daily
  activities for 5 consecutive days**.[^24]
- **Energy availability is a modifiable driver.** The 2023 IOC REDs consensus places low energy
  availability on a spectrum from adaptable to problematic and supplies a screening tool (REDs
  CAT2);[^27] the Female Athlete Triad Coalition's cumulative risk assessment offers the older
  point-based stratification linking menstrual dysfunction, energy availability and bone health.[^28]
- **Calcium and vitamin D reduce stress fractures — in a military cohort.** 5201 female Navy recruits
  randomised to 2000 mg calcium + 800 IU vitamin D₃ daily versus placebo across 8 weeks of basic training
  showed a **20% lower stress fracture incidence** in the supplemented group.[^29]

**Certainty. High** for the high-risk/low-risk distinction and its consequences.[^25][^26] **High** that
low energy availability is a modifiable BSI risk factor.[^27][^28] **Moderate** for the return-to-run
criteria — consensus- and cohort-derived, not trial-derived.[^23][^24] **Moderate** for calcium/vitamin D
(one large RCT, military recruits — borrowed evidence).[^29] **Low** for grade-based timeline prediction,
which a cohort directly contradicts.[^22]

**Implication for coaching.**

- **Suspected bone stress injury is a referral, not a coaching problem.** Focal pinpoint bone tenderness,
  pain on hopping, or pain worsening through a run should stop the coach load-managing and send the
  athlete for assessment (§15). This is absolute for **high-risk sites**, where being wrong risks a
  non-union or complete fracture.[^25][^26]
- **Never estimate a return date from an MRI grade the athlete reports.** The grade indicates severity;
  evidence that it predicts recovery time is contradicted.[^22] Explain what it means and defer timing to
  the treating clinician.
- **Once a clinician has cleared a low-risk BSI, the app can run the progression** — 5 consecutive
  pain-free days of daily activity as the entry gate,[^24] alternate-day walk–run from 30–60 s intervals,
  **distance before speed**, and the rule that loading must not cause symptoms during, after, or the next
  day.[^23][^24] This structured, dated progression is exactly what a training app is good at.
- **Screen for energy availability whenever a BSI appears**, especially a repeat one, routing to
  endurance §14 and nutrition §16 rather than duplicating that advice.[^27][^28]
- **Do not prescribe calcium/vitamin D on the Navy trial alone** — nutrition §16 owns supplementation.
  What this review licenses is *raising* bone-health nutrition as a topic once a BSI has occurred.[^29]

---

## 7. Medial tibial stress syndrome — common, poorly treated, easily confused with something worse

**Concept.** MTSS ("shin splints") is diffuse exercise-induced pain along the posteromedial tibial border.
It matters to the app twice over: it is among the most common running injuries, and its differential
diagnosis includes tibial bone stress injury.

**Evidence.**

- **Very common, with a wide reported range.** Incidence 13.6–20.0% across runner cohorts;[^4] a 2025
  scoping review of 37 studies reports prevalence in runners from **5.4% to 69.5%** and incidence from
  **16.1% to 35.7%**, depending on population and definition.[^35]
- **Risk factors are reasonably quantified.** Meta-analysis in active individuals: **female sex OR 2.35
  (95% CI 1.58–3.50)**, greater navicular drop **SMD 0.44 (0.21–0.67)**, previous running injury **OR
  2.18 (1.00–4.72)**, increased weight **SMD 0.24 (0.03–0.45)**; ankle dorsiflexion range and Q-angle were
  **clearly not** risk factors.[^30] A runner-specific meta-analysis adds **previous MTSS history RR 3.74
  (1.17–11.91)** and **fewer years of running experience SMD −0.74 (−1.26 to −0.23)**.[^31]
- **No treatment has good evidence.** A systematic review concluded the evidence base was of
  **insufficient methodological quality to recommend any specific treatment**, with no study sufficiently
  free of bias. Stretching and strengthening, compression stockings, braces, laser and pulsed
  electromagnetic fields were not proven effective; shockwave was judged the most promising avenue for
  research, on level 3–4 evidence.[^32]
- **Prevention has better evidence than treatment.** A 2025 meta-analysis (12 studies, 8197 participants)
  found **neuromuscular training effective (OR 95% CI 0.13–0.64, high certainty)** and
  **overpronation-specific insoles effective (OR 95% CI 0.10–1.0, moderate certainty)**, while
  **shock-absorbing insoles showed no significant effect (95% CI 0.28–1.08)**.[^33] The null for
  shock-absorbing insoles is corroborated by a 1205-recruit RCT: 18.5% versus 18.0% withdrawal for
  lower-limb injury, OR 1.04 (0.75–1.44), p = 0.87.[^34]

**Certainty. Moderate** for the risk factors — consistent estimates, wide intervals, mostly
non-modifiable.[^30][^31] **High** that no MTSS *treatment* has good supporting evidence.[^32]
**Moderate** for neuromuscular training as prevention.[^33] **High** that generic shock-absorbing insoles
do not prevent lower-limb injury.[^33][^34]

**Implication for coaching.**

- **The first job with shin pain is triage, not treatment.** Diffuse pain over several centimetres of the
  posteromedial border fits MTSS; **focal pinpoint tenderness, night pain, or pain on hopping points
  toward bone stress injury** and requires referral (§6, §15).[^25][^26]
- **Be honest that there is no evidence-backed MTSS treatment to offer.**[^32] The coach can manage load
  and address history — which is defensible — rather than name a modality it cannot support.
- **Offer neuromuscular/strength work as prevention rather than cure**, with the certainty label
  attached.[^33]
- **Do not recommend shock-absorbing insoles**; two independent lines of evidence say they do not
  work.[^33][^34]
- **Weight previous MTSS heavily** — a history of it carries the largest single effect in this
  literature.[^31]

---

## 8. Achilles and patellar tendinopathy — the best-evidenced loading protocols in this document

**Concept.** Tendinopathy is persistent tendon pain and loss of function under load. The **continuum
model** frames it in three stages — reactive tendinopathy, tendon dysrepair, degenerative tendinopathy —
each implying different management.[^36] The ICON international consensus fixed **"tendinopathy"** as the
preferred clinical term, retiring "tendinitis" and "tendinosis".[^37] The app should use that word.

**Evidence.**

- **Eccentric loading is the historical anchor.** Alfredson's original trial treated 15 recreational
  athletes with chronic Achilles tendinosis unresponsive to other treatment; after 12 weeks **all 15 were
  back at pre-injury running**.[^38] The dosage usually attributed to it — **3 × 15 repetitions, twice
  daily, 7 days a week, for 12 weeks** — is stated in that form by Alfredson's own later
  paper.[^39] *(See §18: this specific dosage string was corroborated through the 2008 paper and a
  secondary clinical guideline, not read in the paywalled 1998 full text.)*
- **Insertional Achilles tendinopathy needs a modified protocol.** The same group's pilot study ran the
  eccentric regimen **without loading into dorsiflexion** — flat ground rather than off a step — because
  compression at the insertion is the problem; **18/27 patients (67%) were satisfied and back to previous
  tendon-loading activity** at ~4 months, with VAS falling from 69.9 to 21.[^39] Mid-portion and
  insertional presentations are not interchangeable.
- **Heavy slow resistance (HSR) is at least as good and more tolerable.** The originating patellar
  tendinopathy trial randomised 39 patients to corticosteroid injection, eccentric decline squat, or HSR
  for 12 weeks; the HSR protocol was **leg press, squat and hack squat, every other day, 3–4 sets,
  progressing from 15RM to 6RM, with a 3 s eccentric and 3 s concentric phase**.[^40] In Achilles
  tendinopathy, a head-to-head RCT of 58 patients found **eccentric and HSR equally effective at 52
  weeks**, with **greater patient satisfaction for HSR at 12 weeks**.[^41]
- **Isometrics relieve pain acutely, but the effect has not replicated cleanly.** The original crossover
  study — **5 × 45 s at 70% MVC** — reduced single-leg decline squat pain from 7.0 to 0.17 immediately and
  sustained it at 45 minutes, versus a smaller, non-sustained reduction from isotonic work.[^42] That
  study had **six participants**, and the patellar tendinopathy network meta-analysis later found
  isometric and isotonic exercise equivalent for immediate pain relief across three RCTs.[^45] Useful
  tool; not the reliable analgesic it is often sold as.
- **The pain-monitoring model licenses continued running during rehab.** In 38 patients with Achilles
  tendinopathy randomised to continue tendon-loading activity under a pain-monitoring model versus 6
  weeks of active rest, there were **no significant between-group differences and no negative effect of
  continuing to load**.[^43] The model's rules: **pain up to 5/10 is acceptable during the exercise;
  pain after the session may reach 5/10 but must subside to baseline by the following morning; and
  baseline pain must not increase week to week.**[^43] *(See §18 on the provenance of these three
  numbers.)* A meta-analysis of eccentric exercise likewise found continuous tendon loading did not
  adversely affect outcomes.[^50]
- **Be honest about certainty: no active treatment clearly beats another.** The Achilles living network
  meta-analysis of 29 RCTs found **no trial at low risk of bias**, certainty **low to very low**, and
  **"no clinically relevant difference in effectiveness between different active treatments"** at 3 or 12
  months — while recommending starting with a calf-muscle exercise programme for accessibility, cost and
  safety.[^44] The living review across lower-limb tendinopathies reaches the same place and recommends
  **progressive eccentric or heavy slow resistance exercise for 12 weeks as first-line**, concluding
  there is **no convincing evidence that any adjunct beats exercise alone**.[^46] The 2024 JOSPT clinical
  practice guideline for midportion Achilles tendinopathy likewise places tendon-loading exercise and
  education first-line.[^49]
- **Shockwave should not be routine.** A 2026 meta-analysis found **no clinically meaningful benefit** of
  shockwave for either midportion or insertional Achilles tendinopathy and concluded it "should not be
  considered a routine treatment".[^47] The patellar network meta-analysis similarly recommends against
  shockwave added to eccentric exercise (moderate strength evidence of no superiority).[^45]
- **Timelines are long.** The proposed return-to-sport framework for midportion Achilles tendinopathy is
  **criteria-based rather than time-based**, recommends treating with exercise for **at least 3 months**
  before considering alternatives, and notes recovery **can take up to a year** with high recurrence risk
  during the return-to-sport phase.[^48]

**Certainty. High** that progressive tendon loading is first-line and that adjuncts add nothing over
it.[^44][^46][^49] **High** that shockwave is not indicated routinely.[^45][^47] **Moderate** for the
specific eccentric/HSR dosages — they come from small originating trials, and syntheses find no clear
superiority between them.[^38][^40][^41][^44] **Moderate** for the pain-monitoring model (a single
RCT of 38 patients, but its conclusion is corroborated by meta-analysis).[^43][^50] **Low** for
isometrics as a dependable analgesic.[^42][^45]

**Implication for coaching.**

- **This is the one area where the coach can offer a concrete, evidence-based protocol.** Progressive
  tendon loading — eccentric or HSR — for **12 weeks**, stated at Moderate-to-High certainty depending on
  the claim.[^44][^46]
- **Branch on location.** Mid-portion Achilles work loads through dorsiflexion off a step; **insertional
  Achilles must not**.[^39] Getting this backwards makes an insertional presentation worse.
- **Adopt the pain-monitoring model as the app's core pain-gating rule** — 5/10 acceptable during, back
  to baseline by next morning, baseline not rising week to week.[^43] It is the single most
  operationally useful rule in this review, it is what lets the athlete keep running, and it maps
  directly onto a daily check-in. **⚠ These three numeric thresholds were corroborated through a
  secondary clinical guideline citing the 2007 trial, not read in the paywalled primary text — verify
  them at source before hard-coding them into the app (§18).**
- **Set expectations at months, not weeks**, and warn that the return-to-running phase is when
  recurrence happens.[^48]
- **Do not offer shockwave, injections or other adjuncts** as coach-level suggestions; the evidence does
  not support them over exercise, and they are clinician decisions regardless.[^45][^46][^47]
- **Say "tendinopathy", never "tendinitis".**[^37]

---

## 9. Plantar fasciopathy

**Concept.** Plantar heel pain, characteristically worst on the first steps in the morning and after
inactivity. Incidence in runners is 4.5–10.0%.[^4]

**Evidence.** The current JOSPT clinical practice guideline recommends manual therapy, **plantar
fascia-specific and gastrocnemius/soleus stretching**, and **therapeutic exercise including resistance
training for the foot and ankle musculature**.[^52] The landmark trial randomised 48 patients with
ultrasound-verified plantar fasciitis to shoe inserts plus stretching versus shoe inserts plus **high-load
progressive strength training — unilateral heel raises with a towel under the toes, performed every other
day**. At 3 months the strength group had a **29-point better Foot Function Index (95% CI 6–52,
p = 0.016)**, above the minimal clinically important difference; by 6 and 12 months the groups had
converged.[^51]

**Certainty. High** for exercise and stretching as first-line (clinical practice guideline).[^52]
**Moderate** for high-load strength training specifically — one RCT, n = 48, and its advantage is speed of
improvement rather than a better endpoint.[^51]

**Implication for coaching.** Offer high-load progressive heel raises with the toes extended, every other
day, framed accurately: **it gets you comfortable faster, not better in the end**.[^51] Combine with
calf and plantar fascia stretching.[^52] This is one of the few running injuries where a simple,
prescribable home exercise has direct trial support.

---

## 10. Patellofemoral pain — the most common, and more persistent than runners expect

**Concept.** Retropatellar or peripatellar pain reproduced by squatting, stair climbing, prolonged
sitting, or other activities loading the joint in flexion — with other causes of anterior knee pain
excluded.[^53] The knee is the most commonly affected region in runners.[^3][^4]

**Evidence.**

- **Exercise therapy is the core, and hip work matters.** The international consensus recommends
  **exercise therapy — especially combined hip- and knee-focused exercise** — plus combined interventions
  and foot orthoses; it recommends **against** patellofemoral, knee or lumbar mobilisations in isolation
  and against electrophysical agents; and it rates patellar taping/bracing, dry needling, manual soft
  tissue techniques and **gait retraining** as uncertain.[^54] A meta-analysis of 14 trials (673
  participants) found **hip and knee strengthening superior to knee strengthening alone** for pain and
  activity — notably **without a between-group difference in measured strength gains**.[^55]
- **It often does not simply resolve.** In a multicentre cohort followed 5–8 years after diagnosis,
  **57% reported unfavourable recovery** — though on a **19.3% response rate (60 of 310)**, which
  plausibly skews toward those still symptomatic.[^56] Reassuringly, **98% of those imaged showed no
  radiographic knee osteoarthritis**.[^56] Baseline pain duration over 12 months predicted worse
  outcome.[^56]

**Certainty. High** for exercise therapy, combining hip and knee work, as first-line.[^54][^55]
**High** for what to avoid — isolated mobilisations and electrophysical agents.[^54] **Low** for the
precise long-term persistence figure, given the response rate.[^56]

**Implication for coaching.**

- **Prescribe hip-focused strength alongside knee-focused work**, not quadriceps work alone.[^55]
- **Set honest expectations**: patellofemoral pain frequently persists longer than runners assume, and
  duration of symptoms before starting treatment predicts a worse outcome — which is an argument for
  addressing it early rather than waiting.[^56] But do not quote "57% never recover" as a fact; the
  response rate does not support that precision.[^56]
- **Reassure on the osteoarthritis question** if the athlete raises it — the cohort found essentially no
  radiographic OA at 5–8 years.[^56]
- **Do not offer taping, bracing or gait retraining as established treatment** — the consensus rates them
  uncertain.[^54]

---

## 11. Iliotibial band syndrome — the mechanism most often explained wrongly

**Concept.** Lateral knee pain, typically arising at a repeatable point in a run.

**Evidence.** The friction model — the band "rubbing" over the lateral femoral epicondyle — was
challenged by anatomical and MRI work showing the ITB is a thickened part of the fascia lata rather than
a discrete structure that rolls over the epicondyle; the apparent movement is an illusion created by
changing anterior/posterior fibre tension, and the structure being compressed is a **highly innervated,
vascularised fat pad**, not a bursa.[^57] That work concluded ITBS relates to impaired hip muscle
function.[^57] Prospective and cross-sectional biomechanical evidence associates ITBS in female runners
with **increased peak hip adduction and increased peak knee internal rotation**, from 13 studies of
moderate quality but only one prospective.[^59] A runner-specific systematic review of conservative
treatment found **hip abductor strengthening the cornerstone intervention**, used in 60% of combination
strategies, with pain reduction of 27–100% and functional improvement of 10–57% over 2–8 weeks — but
across only **13 studies and 201 participants, mostly case series**, with heterogeneity so large that
meta-analysis was impossible.[^58]

**Certainty. Moderate** that the compression/fat-pad model supersedes the friction model.[^57]
**Low** for any specific ITBS treatment — the runner-specific evidence base is small and
low-design.[^58] **Low** for the biomechanical risk factors, which are near-entirely
cross-sectional.[^59]

**Implication for coaching.** Offer **hip abductor strengthening and load modification** as the most
reasonable option, labelled Low certainty.[^58] Do not describe ITBS as a friction or "rubbing" problem,
and do not prescribe IT-band stretching or foam rolling on the theory of "loosening the band" — the
anatomy does not support it.[^57] Because ITBS is distance-sensitive rather than pace-sensitive,[^9] cut
long-run distance first when it flares.

---

## 12. Calf and hamstring muscle injuries — and a large external-validity warning

**Concept.** Muscle strain injuries. For distance runners the calf — particularly the **soleus**, the
dominant plantarflexor in steady-state running — matters more than the hamstring, which is the opposite
of the emphasis in the published literature.

**Evidence.**

- **Almost all high-quality strain-injury evidence comes from team sport.** The Nordic hamstring and calf
  strain literature is dominated by football and Australian Rules football cohorts.[^60][^62][^63] The
  one large dataset specific to collegiate track and field shows a different injury profile: distance
  running events had a significantly higher proportion of **overuse** injuries and **168% more time loss
  (95% CI 78–304%)** than other track and field events, with the greatest proportion of **lower-leg**
  injuries.[^66] Distance runners are not sprinters, and the hamstring evidence transfers poorly.
- **Calf strains recur, and recurrences cluster early.** Over a decade of elite Australian football data,
  2-year recurrence ranged **13.0% to 21.3%** depending on definition; individual recurrences averaged
  **35.6 ± 25.6 days** lost; **over 50% of recurrences occurred within 6 months** of the index injury,
  and **20% of subsequent injuries occurred before full recovery from the first**.[^60] There are no
  universally accepted management or return-to-sport guidelines based on grading or imaging.[^67]
- **Calf capacity is measurable, and normative values now exist.** In 500 asymptomatic participants, the
  median single-leg heel-raise count was **25 repetitions (dominant leg)**, with total work 1374 J and
  peak height 9.3 cm; female sex, higher BMI and lower activity were associated with lower
  performance.[^61]
- **The Nordic hamstring effect is smaller and less certain than commonly claimed.** The famous
  meta-analysis of 15 studies and 8459 athletes reported programmes including the Nordic hamstring
  exercise **reduced hamstring injuries by up to 51%**.[^62] A methodological reappraisal restricted to
  RCTs found only 5 of those 15 studies were randomised, giving **RR 0.56 (95% CI 0.20–1.52)**, and
  **0.59 (0.27–1.29)** with an additional RCT — **both confidence intervals crossing 1.0** — and
  concluded the protective effect "remains inconclusive".[^63] Where an effect is found, it is
  compliance-dependent: benefit was associated with **compliance above ~50%**.[^64]
- **Return-to-sport criteria have process consensus but no agreed numbers.** The London international
  consensus reached agreement on exercise selection and dosage (78.8–96.3%), progression criteria
  (73–92.7%), running and sprinting progression (83–100%) and return-to-sport criteria (78.3–98.3%) — but
  **failed to reach consensus on flexibility (40%) or strength (66.1%) benchmarks**.[^65]

**Certainty. High** that calf strain recurrence is common and front-loaded in the first 6
months.[^60] **Moderate** for heel-raise normative values as a capacity benchmark.[^61] **Low /
contested** for the Nordic hamstring exercise's protective effect once restricted to RCTs.[^63]
**Moderate** for the process of return-to-running progression; **Very low** for any specific numeric
strength benchmark, which consensus explicitly failed to agree.[^65] All of this is **borrowed evidence**
from team sport and is capped at Moderate for distance runners.[^66]

**Implication for coaching.**

- **Prioritise calf capacity for runners, not hamstring work.** The soleus is the runner's problem
  muscle; the hamstring literature is imported from sprint-dominant sports.[^66]
- **Use the heel-raise test as a trackable capacity benchmark** — roughly 25 single-leg repetitions is
  population-median, so a runner well under that on the injured side has an actionable
  deficit.[^61] Present it as a benchmark, not a validated return-to-run threshold.
- **Extend monitoring for a full 6 months after a calf strain**, because that is when recurrences
  land — and note that a fifth of subsequent injuries happen before full recovery, i.e. from returning
  too early.[^60]
- **Present the Nordic hamstring exercise honestly**: worth doing, cheap, safe, but the RCT-only estimate
  is not statistically significant, and it only works if actually performed.[^62][^63][^64] Do not quote
  "halves hamstring injuries" as established fact.
- **Do not invent numeric return-to-run strength thresholds.** International consensus could not agree on
  them; the app must not manufacture false precision.[^65]

---

## 13. Prevention: strength training, and the adherence problem that swallows everything else

**Concept.** What can a runner do *before* anything hurts? This is the section a coaching app most wants
to be able to act on, and it is where the gap between the famous headline and the actual evidence is
widest.

**Evidence.**

- **The famous strength-training result is real but narrower than it is quoted.** The 2014 meta-analysis
  (25 trials, 26 610 participants, 3464 injuries) found **strength training RR 0.315 (95% CI
  0.207–0.480)**, **proprioception training RR 0.550 (0.347–0.869)**, multiple-exposure programmes **RR
  0.655 (0.520–0.826)**, and — critically — **stretching RR 0.963 (0.846–1.095), i.e. no effect**. By
  injury type: **acute RR 0.647 (0.502–0.836)**, **overuse RR 0.527 (0.373–0.746)**. Its own summary:
  *"Strength training reduced sports injuries to less than 1/3 and overuse injuries could be almost
  halved."*[^68]
- **The 2018 follow-up is stronger in wording and thinner in data.** It reported **RR 0.338
  (0.238–0.480)** with high strength of evidence and no publication bias, and that **"a 10% increase in
  strength training volume reduced the risk of injury by more than four percentage points"** — but from
  **six studies, 7738 participants and only 177 injuries**.[^69] That is a small evidence base behind a
  very confident sentence, and it is drawn from mixed sports, not runners.
- **In runners specifically, prevention programmes have not worked.** The runner-specific meta-analysis
  (9 studies, 1904 participants) found a **null pooled effect — log RR −0.21 (95% CI −0.46 to 0.047),
  p = 0.110** for injury risk and **log IRR −0.15 (−0.45 to 0.15), p = 0.329** for injury rate. **Seven of
  nine studies were at high risk of bias.** The one thing that separated effective from ineffective
  trials was not programme content but **supervision**: the supervised-only subgroup gave **log RR −0.77
  (−1.18 to −0.37), p < 0.001**.[^70]
- **The largest runner prevention RCT was null.** INSPIRE randomised 2378 recreational runners to an
  online multifactorial prevention programme or control: **37.5% versus 36.7% injured, OR 1.08 (95% CI
  0.90–1.30)**. Roughly **63% read the content and 44% applied the recommendations**.[^71]
- **Adherence is the recurring explanation, and it is usually not even measured.** Of 100
  injury-prevention RCTs, 51.4% reported compliance data and **only 19.3% analysed its effect on
  outcomes** — and those that did found compliance significantly affected results.[^72] In football, the
  FIFA 11+ warm-up programme reduces injuries by roughly **30–46%**, with adherence named as the primary
  determinant of success.[^73] **No equivalently validated warm-up programme exists for distance
  runners** — a genuine gap, not an oversight in this review.

**Certainty. High** that strength training reduces sports injury risk **in mixed athletic
populations**.[^68][^69] **Moderate at best** that it does so in recreational distance runners, where the
direct pooled evidence is null.[^70][^71] **High** that adherence and supervision dominate programme
content as determinants of effect.[^70][^71][^72][^73]

**Implication for coaching.**

- **Recommend strength training — but state the certainty correctly.** The defensible sentence is
  something like: *"Strength training is the best-evidenced injury-prevention intervention in sport
  generally; in runners specifically the trials have been null, and the strongest predictor of whether it
  helps is whether you actually do it."*[^68][^69][^70] Do not quote "cuts injuries by two-thirds" as a
  fact about runners.
- **This dovetails with endurance §6**, which already prescribes 2×/week strength work for *running
  economy* on independent evidence. The practical recommendation is the same; the injury-prevention
  justification is weaker than the economy justification, and the coach should lead with the stronger
  one.
- **Design for adherence over sophistication.** The evidence says a simple programme actually completed
  beats an elaborate one abandoned, and that supervision is what separates success from
  failure.[^70][^72] For an app, the analogue of supervision is scheduling, reminders, logging and
  follow-up — which is squarely a software problem the app can solve. **This is the single most
  actionable finding in the section.**
- **Track completion and use it.** Compliance above ~50% is where benefits appeared in the hamstring
  literature;[^64] an app that knows the athlete did 3 of 12 prescribed sessions should say so rather
  than assume the programme failed.
- **Do not promise prevention.** The honest framing is risk reduction with uncertain magnitude in this
  population, alongside benefits (economy, durability) that are better established.

---

## 14. What is oversold

Both sibling reviews carry a section like this; here is what runners are most often sold that the
evidence does not support.

- **Static stretching to prevent injury.** Direct meta-analytic estimate **RR 0.963 (0.846–1.095) — no
  effect**;[^68] a dedicated systematic review found **moderate-to-strong evidence that routine static
  stretching does not reduce overall injury rates**, with only preliminary evidence for specific
  soft-tissue injuries.[^74] **Certainty: High that it does not work for this purpose.** Stretching may
  still be prescribed where a guideline supports it for a *specific* condition — plantar heel pain,
  for example[^52] — but not as general injury prophylaxis.
- **Cadence and gait retraining as injury prevention.** The systematic review found **37 studies, of
  which only 2 addressed injury**. There is strong evidence that increasing step rate reduces peak knee
  flexion angle and moderate evidence for reduced step length, peak hip adduction and knee extensor
  moment — but the authors conclude there is **"insufficient evidence to conclusively determine the
  effects of altering running step rate on injury and performance"**.[^75] The consensus on
  patellofemoral pain likewise rates gait retraining **uncertain**.[^54] **Certainty: Low.** Changed
  biomechanics is not a demonstrated injury reduction, and the coach must not present it as one.
- **Pronation-based shoe prescription.** Three coordinated military RCTs across the US Army, Air Force
  and Marine Corps (>7000 recruits) found that assigning shoes by **foot arch height had no effect on
  injury rates**.[^76] The picture is not uniformly negative — a blinded RCT in recreational runners
  found motion-control shoes reduced overall injury risk **HR 0.55 (0.36–0.85)**, with the effect
  concentrated in the **pronated-foot subgroup (HR 0.34, 0.13–0.84)** and absent in neutral and supinated
  feet;[^77] a secondary analysis found the benefit specific to **pronation-related** pathologies (HR
  0.41, 0.17–0.98) and not to other running injuries (HR 0.68, 0.41–1.10).[^78] **Certainty: High that
  the mass-market "get your gait analysed and buy the matching shoe" model is not supported;
  Low-to-Moderate that motion-control footwear helps a narrow pronation-related subgroup.**
- **Minimalist and barefoot running as protective.** The RCT randomising 103 runners across traditional,
  partial-minimalist and full-minimalist shoes recorded **4, 7 and 12 injuries** respectively over 12
  weeks — the wrong direction for the claim, though the sample is far too small to be decisive.[^80]
  Separately, a double-blinded RCT of 848 recreational runners found **more** cushioning associated with
  **lower** injury risk (sub-hazard rate ratio 1.52, 95% CI 1.07–2.16 for the harder shoe), modified by
  body mass.[^79] **Certainty: Low that minimalism does not reduce injury risk** — that verdict rests on
  a single trial with 23 injuries in total, which is the same evidentiary thinness this review labels Low
  elsewhere. **Moderate that softer cushioning is not harmful and may help**, from the n = 848 RCT.[^79]
- **Shock-absorbing insoles.** Meta-analysis: overall injuries **RR 0.92 (0.73–1.16)**, stress fractures
  **RR 1.15 (0.57–2.32)**, soft-tissue injuries **RR 0.92 (0.74–1.15)** — null on every outcome.[^81]
  Corroborated by the 1205-recruit RCT[^34] and the MTSS prevention meta-analysis.[^33] **Certainty:
  High that they do not work.** Note the contrast with *prescribed foot orthoses*, which in the same
  meta-analysis did reduce overall injuries **RR 0.72 (0.55–0.94)** and stress fractures **RR 0.59
  (0.45–0.76)** — but from largely military trials, so this is borrowed evidence.[^81]
- **Foam rolling as injury prevention.** This review found no trial evidence that foam rolling reduces
  running injury incidence — the literature on it addresses range of motion, soreness and perceived
  recovery, which are different claims and were outside this review's search. **Certainty: absent for
  injury prevention** — the coach should not present it as prevention, though there is no reason to
  discourage it.

The unifying pattern: **interventions that change biomechanics or feel are consistently better evidenced
for changing biomechanics or feel than for preventing injury.** The coach should keep those two claims
apart.

---

## 15. Red flags — the boundary this document exists to enforce

**Concept.** Not an evidence question but a safety boundary. When these appear, the coach stops managing
load and directs the athlete to a clinician. This section overrides every other recommendation in the
document.

**Evidence and reasoning.** Individual red flags have weak diagnostic accuracy taken alone — the
international framework for serious spinal pathology is explicit that **"there is an absence of
high-quality evidence for the diagnostic accuracy of most red flags"** and advocates a clinical-reasoning
pathway over naive checklists, noting only around **1% of musculoskeletal presentations in primary care**
reflect serious pathology.[^82] That cuts both ways for an automated coach: it means a red flag is a
*trigger for human assessment*, not a diagnosis the app has made — which is exactly the right framing,
because the app is not the clinician either way. It also means the app should escalate on pattern, not
panic on a single word.

**Referral triggers.**

| Pattern | Why it matters |
|---|---|
| **Focal, pinpoint bone tenderness**; pain on hopping; pain that worsens through a run rather than warming up | Bone stress injury, including high-risk sites where delay risks non-union or complete fracture[^25][^26] |
| Pain over the **anterior tibia**, femoral neck/groin, navicular, or base of the fifth metatarsal | High-risk BSI sites specifically[^25][^26] |
| **Night pain**, rest pain, or pain unrelated to loading | Does not fit a mechanical overload pattern[^25][^82] |
| **Neurological symptoms** — numbness, pins and needles, weakness, and especially saddle anaesthesia or bladder/bowel change | Serious spinal pathology; saddle/bladder symptoms are an emergency[^82] |
| **Calf pain with swelling, warmth, or redness**, particularly after travel, immobilisation or surgery | Possible deep vein thrombosis — a medical emergency, not a muscle strain |
| **Reproducible, distance-dependent bilateral leg pain with tightness, paraesthesia or weakness that resolves on stopping** | Chronic exertional compartment syndrome, commonly misdiagnosed as shin splints and requiring compartment pressure testing[^83] |
| **Chest pain, exertional syncope, palpitations, or disproportionate breathlessness** | Cardiac — outside this document's scope entirely and always urgent |
| Systemic features: **fever, unexplained weight loss, night sweats**, or a history of cancer | Infection or malignancy[^82] |
| Pain that is **rapidly worsening** session on session despite load reduction | The load-management approach is failing and the working assumption is wrong |
| Any injury **not improving after ~4 weeks** of appropriate load management | Time to reassess the assumption, not to persist |

**Implication for coaching.**

- **The coach's referral message should be plain, non-alarming and non-diagnostic.** It says what pattern
  it noticed and that a clinician should look at it — never a named diagnosis and never a probability.
- **Escalate on pattern, not keyword.** A single mention of "numb feet" after a long run in tight shoes is
  not cauda equina. The framework's own conclusion is that red flags are reasoning prompts rather than
  triggers.[^82]
- **Never let a red flag be silently overridden** by the athlete insisting they are fine or by a race on
  the calendar. This is the one place where the coach should decline to produce a training plan at all.
- **The app has no emergency channel.** For the emergency-tier items (neurological deficit, suspected
  DVT, cardiac symptoms), the message must direct to urgent care rather than implying the app will follow
  up.

---

## 16. Return to running: the common structure

Across the injury-specific sections, the return-to-running literature converges on a shared shape, even
though the numbers differ by tissue:

1. **Entry gate is symptom-based, not calendar-based.** For low-risk BSI the published gate is **5
   consecutive pain-free days of normal daily activity**;[^24] tendinopathy uses the pain-monitoring
   thresholds instead.[^43] Consensus in hamstring rehabilitation is explicitly criteria-based, and
   deliberately declined to set numeric strength benchmarks.[^65]
2. **A capacity check before running**, where one exists: **single-leg hop** for tibial BSI,[^23]
   **single-leg heel raise** for calf, against a population median of about 25 repetitions.[^61]
3. **Walk–run intervals on alternate days**, beginning around **30–60 s of running** per interval.[^23]
4. **Distance before speed.**[^23] Hills, intervals and long runs return last.
5. **The next-day rule as the progression gate** — loading must not provoke symptoms during, after, or
   the following morning, and baseline pain must not creep up week to week.[^24][^43]
6. **Extended monitoring after clearance**, because recurrence clusters early: over half of calf strain
   recurrences fall within 6 months,[^60] and the return-to-sport phase is the high-risk window for
   Achilles tendinopathy.[^48]

**Certainty: Moderate.** This structure is consistent across consensus statements and scoping reviews but
is largely expert-derived rather than trial-derived, and the specific numbers are tissue-specific rather
than general.

---

## 17. Synthesis: an evidence map for the coach

| Claim the coach might make | Certainty | Source |
|---|---|---|
| Previous injury roughly doubles risk; it is the strongest known risk factor | High | [^3][^5][^7] |
| Novice runners are hurt at ~2.3× the rate of established recreational runners | High | [^2] |
| No metric can predict an individual's injury; risk estimation ≠ prediction | High | [^18] |
| Progressive tendon loading (eccentric or HSR), 12 weeks, is first-line for tendinopathy | High | [^44][^46][^49] |
| No adjunct beats exercise alone for tendinopathy; shockwave is not routine | High | [^45][^46][^47] |
| Exercise therapy combining hip and knee work is first-line for patellofemoral pain | High | [^54][^55] |
| Static stretching does not prevent injury | High | [^68][^74] |
| Shock-absorbing insoles do not prevent injury | High | [^33][^34][^81] |
| Pronation/arch-based shoe prescription does not reduce injury | High | [^76] |
| Suspected bone stress injury at a high-risk site needs referral, not load management | High (safety) | [^25][^26] |
| Strength training reduces injury risk in sport generally | High | [^68][^69] |
| ...and in recreational runners specifically | Moderate at best — pooled effect is null | [^70][^71] |
| Adherence/supervision matters more than programme content | High | [^70][^72] |
| Weekly distance jumps >30% raise distance-related injury risk | Moderate | [^9] |
| The 10% rule prevents injury | **Very low — failed its RCT** | [^10] |
| Progressing volume is safer than progressing intensity (or vice versa) | **Very low — RCT found no difference** | [^11] |
| The ACWR 0.8–1.3 band is a validated injury threshold | **Very low / contested** | [^13][^14][^15][^16] |
| Pain up to 5/10, settling to baseline by next morning, is acceptable during tendon rehab | Moderate | [^43][^50] |
| Return to run after low-risk BSI: 5 pain-free days, walk–run, distance before speed | Moderate | [^23][^24] |
| High-load heel raises speed recovery in plantar fasciopathy | Moderate | [^51][^52] |
| Nordic hamstring exercise halves hamstring injuries | **Low — RCT-only estimate is not significant** | [^62][^63] |
| Hip abductor strengthening helps ITBS | Low | [^58] |
| Increasing cadence prevents injury | **Low — changes biomechanics, injury effect unproven** | [^75] |
| Isometrics reliably relieve tendon pain | Low | [^42][^45] |
| Foam rolling prevents injury | **Very low / absent** | — |

---

## 18. Limitations, and what this review does not license

- **This document does not license diagnosis.** Every management recommendation here assumes the
  diagnosis is already established or the presentation is being managed conservatively pending
  assessment. The coach recognises patterns and manages load; it does not name conditions with
  confidence, and §15 overrides everything else.
- **Most of the evidence is borrowed.** Prevention evidence comes disproportionately from military
  recruits and team sports;[^69][^73][^76][^81] muscle-strain evidence comes almost entirely from
  football codes;[^60][^62][^63] rehabilitation trials use mixed clinical populations. Where the
  runner-specific evidence exists it is frequently **weaker or null** compared with the mixed-population
  result — the strength-training case is the clearest example.[^70][^71]
- **The underlying quality is low and this review cannot fix that.** The risk-factor umbrella review
  rated **every** included systematic review low or critically low quality;[^6] the Achilles network
  meta-analysis found **no trial at low risk of bias**;[^44] the runner prevention meta-analysis found 7
  of 9 studies at high risk of bias.[^70] The certainty labels in this document reflect that ceiling.
- **The injury-definition problem propagates into every incidence number quoted here.**[^1][^3]
- **Citation-integrity caveats specific to this review.** Every DOI was resolved against CrossRef; that
  proves the paper exists as described, not that a quoted number appears in it. Two heavily-quoted
  numeric items deserve explicit flagging:
  - The **Alfredson eccentric dosage** (3 × 15, twice daily, 7 days a week, 12 weeks) is quoted here from
    Alfredson's own 2008 paper, which states it in that form, rather than from the paywalled 1998
    original.[^38][^39]
  - The **Silbernagel pain-monitoring thresholds** (5/10 acceptable; settling to baseline by the
    following morning; baseline not rising week to week) were confirmed against a secondary clinical
    guideline that cites the 2007 trial, not against the paywalled primary text.[^43] Given this is the
    most operationally important rule in the document, it should be verified at source before being
    hard-coded into the app.
  - **Year convention.** References here carry the **issue** year, which is how these papers are cited
    in the literature. CrossRef's `published` field often reports the earlier online-first date, so
    running `fetch_injury_bib.py` shows a one-year difference for about a dozen entries (Lauersen 2014,
    Cook & Purdam 2009, ICON 2020 and others). Volume and page numbers match exactly in every case,
    which is what confirms the right paper.
  - Numbers checked directly against source abstracts include the Lauersen risk ratios,[^68][^69] the
    Videbæk incidence figures,[^2] the Nielsen progression cohort,[^9] the GRONORUN and Run Clever
    trials,[^10][^11] the INSPIRE trial,[^71] the Nordic hamstring reappraisal,[^63] and the MTSS
    risk-factor meta-analyses.[^30][^31]
- **What is missing.** No good runner-specific evidence exists for: a validated warm-up programme
  analogous to FIFA 11+;[^73] numeric return-to-run strength benchmarks;[^65] MTSS treatment of any
  kind;[^32] and ITBS management beyond small case series.[^58] The coach should say so rather than
  improvise.

---

## References

[^1]: Yamato TP, Saragiotto BT, Lopes AD. A consensus definition of running-related injury in recreational runners: a modified Delphi approach. *J Orthop Sports Phys Ther.* 2015;45(5):375–380. https://doi.org/10.2519/jospt.2015.5741

[^2]: Videbæk S, Bueno AM, Nielsen RO, Rasmussen S. Incidence of running-related injuries per 1000 h of running in different types of runners: a systematic review and meta-analysis. *Sports Med.* 2015;45(7):1017–1026. https://doi.org/10.1007/s40279-015-0333-8

[^3]: van Gent RN, Siem D, van Middelkoop M, van Os AG, Bierma-Zeinstra SMA, Koes BW. Incidence and determinants of lower extremity running injuries in long distance runners: a systematic review. *Br J Sports Med.* 2007;41(8):469–480. https://doi.org/10.1136/bjsm.2006.033548

[^4]: Lopes AD, Hespanhol Júnior LC, Yeung SS, Costa LOP. What are the main running-related musculoskeletal injuries? A systematic review. *Sports Med.* 2012;42(10):891–905. https://doi.org/10.1007/BF03262301

[^5]: Desai P, Jungmalm J, Börjesson M, Karlsson J, Grau S. Recreational runners with a history of injury are twice as likely to sustain a running-related injury as runners with no history of injury: a 1-year prospective cohort study. *J Orthop Sports Phys Ther.* 2021;51(3):144–150. https://doi.org/10.2519/jospt.2021.9673

[^6]: Correia CK, Machado JM, Dominski FH, de Castro MP, de Brito Fontana H, Ruschel C. Risk factors for running-related injuries: an umbrella systematic review. *J Sport Health Sci.* 2024;13(6):793–804. https://doi.org/10.1016/j.jshs.2024.04.011

[^7]: van der Worp MP, ten Haaf DSM, van Cingel R, de Wijer A, Nijhuis-van der Sanden MWG, Staal JB. Injuries in runners; a systematic review on risk factors and sex differences. *PLoS One.* 2015;10(2):e0114937. https://doi.org/10.1371/journal.pone.0114937

[^8]: Nielsen RO, Buist I, Parner ET, Nohr EA, Sørensen H, Lind M, Rasmussen S. Predictors of running-related injuries among 930 novice runners: a 1-year prospective follow-up study. *Orthop J Sports Med.* 2013;1(1). https://doi.org/10.1177/2325967113487316

[^9]: Nielsen RO, Parner ET, Nohr EA, Sørensen H, Lind M, Rasmussen S. Excessive progression in weekly running distance and risk of running-related injuries: an association which varies according to type of injury. *J Orthop Sports Phys Ther.* 2014;44(10):739–747. https://doi.org/10.2519/jospt.2014.5164

[^10]: Buist I, Bredeweg SW, van Mechelen W, Lemmink KAPM, Pepping GJ, Diercks RL. No effect of a graded training program on the number of running-related injuries in novice runners: a randomized controlled trial. *Am J Sports Med.* 2008;36(1):33–39. https://doi.org/10.1177/0363546507307505

[^11]: Ramskov D, Rasmussen S, Sørensen H, Parner ET, Lind M, Nielsen RO. Run Clever – no difference in risk of injury when comparing progression in running volume and running intensity in recreational runners: a randomised trial. *BMJ Open Sport Exerc Med.* 2018;4(1):e000333. https://doi.org/10.1136/bmjsem-2017-000333

[^12]: Soligard T, Schwellnus M, Alonso JM, et al. How much is too much? (Part 1) International Olympic Committee consensus statement on load in sport and risk of injury. *Br J Sports Med.* 2016;50(17):1030–1041. https://doi.org/10.1136/bjsports-2016-096581

[^13]: Impellizzeri FM, McCall A, Ward P, Bornn L, Coutts AJ. Training load and its role in injury prevention, part 2: conceptual and methodologic pitfalls. *J Athl Train.* 2020;55(9):893–901. https://doi.org/10.4085/1062-6050-501-19

[^14]: Wang C, Vargas JT, Stokes T, Steele R, Shrier I. Analyzing activity and injury: lessons learned from the acute:chronic workload ratio. *Sports Med.* 2020;50(7):1243–1254. https://doi.org/10.1007/s40279-020-01280-1

[^15]: Zouhal H, Boullosa D, Ramirez-Campillo R, Ali A, Granacher U. Editorial: acute:chronic workload ratio: is there scientific evidence? *Front Physiol.* 2021;12:669687. https://doi.org/10.3389/fphys.2021.669687

[^16]: Nakaoka GB, Barboza SD, Verhagen E, van Mechelen W, Hespanhol L. The association between the acute:chronic workload ratio and running-related injuries in Dutch runners: a prospective cohort study. *Sports Med.* 2021;51(11):2437–2447. https://doi.org/10.1007/s40279-021-01483-0

[^17]: Frandsen JJ, Simonsen MB, Hulme A, et al. A paradigm shift in understanding overuse running-related injuries: findings from the Garmin-RUNSAFE study point to a sudden not gradual onset. *JOSPT Open.* 2025;3(1):85–92. https://doi.org/10.2519/josptopen.2024.0075

[^18]: Bahr R. Why screening tests to predict injury do not work—and probably never will…: a critical review. *Br J Sports Med.* 2016;50(13):776–780. https://doi.org/10.1136/bjsports-2016-096256

[^19]: Warden SJ, Davis IS, Fredericson M. Management and prevention of bone stress injuries in long-distance runners. *J Orthop Sports Phys Ther.* 2014;44(10):749–765. https://doi.org/10.2519/jospt.2014.5334

[^20]: Fredericson M, Bergman AG, Hoffman KL, Dillingham MS. Tibial stress reaction in runners: correlation of clinical symptoms and scintigraphy with a new magnetic resonance imaging grading system. *Am J Sports Med.* 1995;23(4):472–481. https://doi.org/10.1177/036354659502300418

[^21]: Kijowski R, Choi J, Shinki K, Del Rio AM, De Smet A. Validation of MRI classification system for tibial stress injuries. *AJR Am J Roentgenol.* 2012;198(4):878–884. https://doi.org/10.2214/AJR.11.6826

[^22]: Ditmars FS, Ruess L, Young CM, Hu HH, MacDonald JP, Ravindran R, Thompson BP. MRI of tibial stress fractures: relationship between Fredericson classification and time to recovery in pediatric athletes. *Pediatr Radiol.* 2020;50(12):1735–1741. https://doi.org/10.1007/s00247-020-04760-8

[^23]: George ERM, Sheerin KR, Reid D. Criteria and guidelines for returning to running following a tibial bone stress injury: a scoping review. *Sports Med.* 2024;54(9):2247–2265. https://doi.org/10.1007/s40279-024-02051-y

[^24]: Warden SJ, Edwards WB, Willy RW. Optimal load for managing low-risk tibial and metatarsal bone stress injuries in runners: the science behind the clinical reasoning. *J Orthop Sports Phys Ther.* 2021;51(7):322–330. https://doi.org/10.2519/jospt.2021.9982

[^25]: McInnis KC, Ramey LN. High-risk stress fractures: diagnosis and management. *PM R.* 2016;8(3 Suppl):S113–S124. https://doi.org/10.1016/j.pmrj.2015.09.019

[^26]: Al-Janabi MJM, Gupta N, Döring S. The dreaded black line. *J Belg Soc Radiol.* 2023;107(1). https://doi.org/10.5334/jbsr.3050

[^27]: Mountjoy M, Ackerman KE, Bailey DM, et al. 2023 International Olympic Committee's (IOC) consensus statement on Relative Energy Deficiency in Sport (REDs). *Br J Sports Med.* 2023;57(17):1073–1098. https://doi.org/10.1136/bjsports-2023-106994

[^28]: Joy E, De Souza MJ, Nattiv A, et al. 2014 Female Athlete Triad Coalition consensus statement on treatment and return to play of the female athlete triad. *Curr Sports Med Rep.* 2014;13(4):219–232. https://doi.org/10.1249/jsr.0000000000000077

[^29]: Lappe J, Cullen D, Haynatzki G, Recker R, Ahlf R, Thompson K. Calcium and vitamin D supplementation decreases incidence of stress fractures in female navy recruits. *J Bone Miner Res.* 2008;23(5):741–749. https://doi.org/10.1359/jbmr.080102

[^30]: Reinking MF, Austin TM, Richter RR, Krieger MM. Medial tibial stress syndrome in active individuals: a systematic review and meta-analysis of risk factors. *Sports Health.* 2016;9(3):252–261. https://doi.org/10.1177/1941738116673299

[^31]: Newman P, Witchalls J, Waddington G, Adams R. Risk factors associated with medial tibial stress syndrome in runners: a systematic review and meta-analysis. *Open Access J Sports Med.* 2013;4:229–241. https://doi.org/10.2147/OAJSM.S39331

[^32]: Winters M, Eskes M, Weir A, Moen MH, Backx FJG, Bakker EWP. Treatment of medial tibial stress syndrome: a systematic review. *Sports Med.* 2013;43(12):1315–1333. https://doi.org/10.1007/s40279-013-0087-0

[^33]: Marques TBT, Rangel RPS, Martins LV, Vidal APC. Preventive interventions for medial tibial stress syndrome: systematic review and meta-analysis. *Gait Posture.* 2025;122:92–98. https://doi.org/10.1016/j.gaitpost.2025.07.312

[^34]: Withnall R, Eastaugh J, Freemantle N. Do shock absorbing insoles in recruits undertaking high levels of physical activity reduce lower limb injury? A randomized controlled trial. *J R Soc Med.* 2006;99(1):32–37. https://doi.org/10.1177/014107680609900113

[^35]: Saad MA, Jamal JM, Aldhafiri AT, Alkandari SA. Medial tibial stress syndrome: a scoping review of epidemiology, biomechanics, and risk factors. *Cureus.* 2025. https://doi.org/10.7759/cureus.81463

[^36]: Cook JL, Purdam CR. Is tendon pathology a continuum? A pathology model to explain the clinical presentation of load-induced tendinopathy. *Br J Sports Med.* 2009;43(6):409–416. https://doi.org/10.1136/bjsm.2008.051193

[^37]: Scott A, Squier K, Alfredson H, et al. ICON 2019: International Scientific Tendinopathy Symposium consensus: clinical terminology. *Br J Sports Med.* 2020;54(5):260–262. https://doi.org/10.1136/bjsports-2019-100885

[^38]: Alfredson H, Pietilä T, Jonsson P, Lorentzon R. Heavy-load eccentric calf muscle training for the treatment of chronic Achilles tendinosis. *Am J Sports Med.* 1998;26(3):360–366. https://doi.org/10.1177/03635465980260030301

[^39]: Jonsson P, Alfredson H, Sunding K, Fahlström M, Cook J. New regimen for eccentric calf-muscle training in patients with chronic insertional Achilles tendinopathy: results of a pilot study. *Br J Sports Med.* 2008;42(9):746–749. https://doi.org/10.1136/bjsm.2007.039545

[^40]: Kongsgaard M, Kovanen V, Aagaard P, et al. Corticosteroid injections, eccentric decline squat training and heavy slow resistance training in patellar tendinopathy. *Scand J Med Sci Sports.* 2009;19(6):790–802. https://doi.org/10.1111/j.1600-0838.2009.00949.x

[^41]: Beyer R, Kongsgaard M, Hougs Kjær B, Øhlenschlæger T, Kjær M, Magnusson SP. Heavy slow resistance versus eccentric training as treatment for Achilles tendinopathy: a randomized controlled trial. *Am J Sports Med.* 2015;43(7):1704–1711. https://doi.org/10.1177/0363546515584760

[^42]: Rio E, Kidgell D, Purdam C, Gaida J, Moseley GL, Pearce AJ, Cook J. Isometric exercise induces analgesia and reduces inhibition in patellar tendinopathy. *Br J Sports Med.* 2015;49(19):1277–1283. https://doi.org/10.1136/bjsports-2014-094386

[^43]: Silbernagel KG, Thomeé R, Eriksson BI, Karlsson J. Continued sports activity, using a pain-monitoring model, during rehabilitation in patients with Achilles tendinopathy: a randomized controlled study. *Am J Sports Med.* 2007;35(6):897–906. https://doi.org/10.1177/0363546506298279

[^44]: van der Vlist AC, Winters M, Weir A, et al. Which treatment is most effective for patients with Achilles tendinopathy? A living systematic review with network meta-analysis of 29 randomised controlled trials. *Br J Sports Med.* 2021;55(5):249–256. https://doi.org/10.1136/bjsports-2019-101872

[^45]: Challoumas D, Pedret C, Biddle M, et al. Management of patellar tendinopathy: a systematic review and network meta-analysis of randomised studies. *BMJ Open Sport Exerc Med.* 2021;7(4):e001110. https://doi.org/10.1136/bmjsem-2021-001110

[^46]: Challoumas D, Crosbie G, O'Neill S, Pedret C, Millar NL. Effectiveness of exercise treatments with or without adjuncts for common lower limb tendinopathies: a living systematic review and network meta-analysis. *Sports Med Open.* 2023;9(1). https://doi.org/10.1186/s40798-023-00616-1

[^47]: Korakakis V, Kotsifaki R, Sotiralis Y, Malliaras P. Shockwave therapy for midportion and insertional Achilles tendinopathy: a nail in the coffin? A systematic review with meta-analysis. *J Orthop Sports Phys Ther.* 2026;56(5):282–299. https://doi.org/10.2519/jospt.2026.13985

[^48]: Grävare Silbernagel K, Crossley KM. A proposed return-to-sport program for patients with midportion Achilles tendinopathy: rationale and implementation. *J Orthop Sports Phys Ther.* 2015;45(11):876–886. https://doi.org/10.2519/jospt.2015.5885

[^49]: Chimenti RL, Neville C, Houck J, et al. Achilles pain, stiffness, and muscle power deficits: midportion Achilles tendinopathy revision – 2024. *J Orthop Sports Phys Ther.* 2024;54(12):CPG1–CPG32. https://doi.org/10.2519/jospt.2024.0302

[^50]: Prudêncio DA, Maffulli N, Migliorini F, Serafim TT, Nunes LF, Sanada LS, Okubo R. Eccentric exercise is more effective than other exercises in the treatment of mid-portion Achilles tendinopathy: systematic review and meta-analysis. *BMC Sports Sci Med Rehabil.* 2023;15(1). https://doi.org/10.1186/s13102-023-00618-2

[^51]: Rathleff MS, Mølgaard CM, Fredberg U, Kaalund S, Andersen KB, Jensen TT, Aaskov S, Olesen JL. High-load strength training improves outcome in patients with plantar fasciitis: a randomized controlled trial with 12-month follow-up. *Scand J Med Sci Sports.* 2015;25(3). https://doi.org/10.1111/sms.12313

[^52]: Koc TA, Bise CG, Neville C, Carreira D, Martin RL, McDonough CM. Heel pain – plantar fasciitis: revision 2023. *J Orthop Sports Phys Ther.* 2023;53(12):CPG1–CPG39. https://doi.org/10.2519/jospt.2023.0303

[^53]: Willy RW, Hoglund LT, Barton CJ, et al. Patellofemoral pain: clinical practice guidelines linked to the International Classification of Functioning, Disability and Health. *J Orthop Sports Phys Ther.* 2019;49(9):CPG1–CPG95. https://doi.org/10.2519/jospt.2019.0302

[^54]: Collins NJ, Barton CJ, van Middelkoop M, et al. 2018 Consensus statement on exercise therapy and physical interventions (orthoses, taping and manual therapy) to treat patellofemoral pain. *Br J Sports Med.* 2018;52(18):1170–1178. https://doi.org/10.1136/bjsports-2018-099397

[^55]: Nascimento LR, Teixeira-Salmela LF, Souza RB, Resende RA. Hip and knee strengthening is more effective than knee strengthening alone for reducing pain and improving activity in individuals with patellofemoral pain: a systematic review with meta-analysis. *J Orthop Sports Phys Ther.* 2018;48(1):19–31. https://doi.org/10.2519/jospt.2018.7365

[^56]: Lankhorst NE, van Middelkoop M, Crossley KM, Bierma-Zeinstra SMA, Oei EHG, Vicenzino B, Collins NJ. Factors that predict a poor outcome 5–8 years after the diagnosis of patellofemoral pain: a multicentre observational analysis. *Br J Sports Med.* 2016;50(14):881–886. https://doi.org/10.1136/bjsports-2015-094664

[^57]: Fairclough J, Hayashi K, Toumi H, Lyons K, Bydder G, Phillips N, Best TM, Benjamin M. Is iliotibial band syndrome really a friction syndrome? *J Sci Med Sport.* 2007;10(2):74–76. https://doi.org/10.1016/j.jsams.2006.05.017

[^58]: Sanchez-Alvarado A, Bokil C, Cassel M, Engel T. Effects of conservative treatment strategies for iliotibial band syndrome on pain and function in runners: a systematic review. *Front Sports Act Living.* 2024;6. https://doi.org/10.3389/fspor.2024.1386456

[^59]: Aderem J, Louw QA. Biomechanical risk factors associated with iliotibial band syndrome in runners: a systematic review. *BMC Musculoskelet Disord.* 2015;16(1). https://doi.org/10.1186/s12891-015-0808-7

[^60]: Green B, Schache AG, Pizzari T. What is a recurrence? The onset, frequency and time loss impact of recurrent calf muscle strain injuries in elite male Australian football players over a decade. *BMJ Open Sport Exerc Med.* 2025;11(3):e002865. https://doi.org/10.1136/bmjsem-2025-002865

[^61]: Sleeswijk Visser TSO, O'Neill S, Hébert-Losier K, Eygendaal D, de Vos RJ. Normative values for calf muscle strength-endurance in the general population assessed with the Calf Raise Application: a large international cross-sectional study. *Braz J Phys Ther.* 2025;29(3):101188. https://doi.org/10.1016/j.bjpt.2025.101188

[^62]: van Dyk N, Behan FP, Whiteley R. Including the Nordic hamstring exercise in injury prevention programmes halves the rate of hamstring injuries: a systematic review and meta-analysis of 8459 athletes. *Br J Sports Med.* 2019;53(21):1362–1370. https://doi.org/10.1136/bjsports-2018-100045

[^63]: Impellizzeri FM, McCall A, van Smeden M. Why methods matter in a meta-analysis: a reappraisal showed inconclusive injury preventive effect of Nordic hamstring exercise. *J Clin Epidemiol.* 2021;140:111–124. https://doi.org/10.1016/j.jclinepi.2021.09.007

[^64]: Ripley NJ, Cuthbert M, Ross S, Comfort P, McMahon JJ. The effect of exercise compliance on risk reduction for hamstring strain injury: a systematic review and meta-analyses. *Int J Environ Res Public Health.* 2021;18(21):11260. https://doi.org/10.3390/ijerph182111260

[^65]: Paton BM, Read P, van Dyk N, et al. London International Consensus and Delphi study on hamstring injuries part 3: rehabilitation, running and return to sport. *Br J Sports Med.* 2023;57(5):278–291. https://doi.org/10.1136/bjsports-2021-105384

[^66]: Hopkins C, Williams J, Rauh MJ, Zhang L. Epidemiology of NCAA track and field injuries from 2010 to 2014. *Orthop J Sports Med.* 2022;10(1). https://doi.org/10.1177/23259671211068079

[^67]: Pagan-Rosado R, Troyer W, Rosario-Concepcion R, et al. Calf strains in athletes: a narrative review of management, injury grading, and return to sport. *Sports Med Open.* 2025;11(1). https://doi.org/10.1186/s40798-025-00960-4

[^68]: Lauersen JB, Bertelsen DM, Andersen LB. The effectiveness of exercise interventions to prevent sports injuries: a systematic review and meta-analysis of randomised controlled trials. *Br J Sports Med.* 2014;48(11):871–877. https://doi.org/10.1136/bjsports-2013-092538

[^69]: Lauersen JB, Andersen TE, Andersen LB. Strength training as superior, dose-dependent and safe prevention of acute and overuse sports injuries: a systematic review, qualitative analysis and meta-analysis. *Br J Sports Med.* 2018;52(24):1557–1563. https://doi.org/10.1136/bjsports-2018-099078

[^70]: Wu H, Brooke-Wavell K, Fong DTP, Paquette MR, Blagrove RC. Do exercise-based prevention programs reduce injury in endurance runners? A systematic review and meta-analysis. *Sports Med.* 2024;54(5):1249–1267. https://doi.org/10.1007/s40279-024-01993-7

[^71]: Fokkema T, de Vos RJ, van Ochten JM, et al. Online multifactorial prevention programme has no effect on the number of running-related injuries: a randomised controlled trial. *Br J Sports Med.* 2019;53(23):1479–1485. https://doi.org/10.1136/bjsports-2018-099744

[^72]: van Reijen M, Vriend I, van Mechelen W, Finch CF, Verhagen EALM. Compliance with sport injury prevention interventions in randomised controlled trials: a systematic review. *Sports Med.* 2016;46(8):1125–1139. https://doi.org/10.1007/s40279-016-0470-8

[^73]: Patel P, Shah M. The impact of the FIFA 11+ injury prevention program on injury incidence in football athletes: a systematic review of randomized controlled trials. *Cureus.* 2025. https://doi.org/10.7759/cureus.100463

[^74]: Small K, Mc Naughton L, Matthews M. A systematic review into the efficacy of static stretching as part of a warm-up for the prevention of exercise-related injury. *Res Sports Med.* 2008;16(3):213–231. https://doi.org/10.1080/15438620802310784

[^75]: Anderson LM, Martin JF, Barton CJ, Bonanno DR. What is the effect of changing running step rate on injury, performance and biomechanics? A systematic review and meta-analysis. *Sports Med Open.* 2022;8(1). https://doi.org/10.1186/s40798-022-00504-0

[^76]: Knapik JJ, Trone DW, Tchandja J, Jones BH. Injury-reduction effectiveness of prescribing running shoes on the basis of foot arch height: summary of military investigations. *J Orthop Sports Phys Ther.* 2014;44(10):805–812. https://doi.org/10.2519/jospt.2014.5342

[^77]: Malisoux L, Chambon N, Delattre N, Gueguen N, Urhausen A, Theisen D. Injury risk in runners using standard or motion control shoes: a randomised controlled trial with participant and assessor blinding. *Br J Sports Med.* 2016;50(8):481–487. https://doi.org/10.1136/bjsports-2015-095031

[^78]: Willems TM, Ley C, Goetghebeur E, Theisen D, Malisoux L. Motion-control shoes reduce the risk of pronation-related pathologies in recreational runners: a secondary analysis of a randomized controlled trial. *J Orthop Sports Phys Ther.* 2021;51(3):135–143. https://doi.org/10.2519/jospt.2021.9710

[^79]: Malisoux L, Delattre N, Urhausen A, Theisen D. Shoe cushioning influences the running injury risk according to body mass: a randomized controlled trial involving 848 recreational runners. *Am J Sports Med.* 2020;48(2):473–480. https://doi.org/10.1177/0363546519892578

[^80]: Ryan M, Elashi M, Newsham-West R, Taunton J. Examining injury risk and pain perception in runners using minimalist footwear. *Br J Sports Med.* 2014;48(16):1257–1262. https://doi.org/10.1136/bjsports-2012-092061

[^81]: Bonanno DR, Landorf KB, Munteanu SE, Murley GS, Menz HB. Effectiveness of foot orthoses and shock-absorbing insoles for the prevention of injury: a systematic review and meta-analysis. *Br J Sports Med.* 2017;51(2):86–96. https://doi.org/10.1136/bjsports-2016-096671

[^82]: Finucane LM, Downie A, Mercer C, et al. International framework for red flags for potential serious spinal pathologies. *J Orthop Sports Phys Ther.* 2020;50(7):350–372. https://doi.org/10.2519/jospt.2020.9971

[^83]: Tarabishi MM, Almigdad A, Almonaie S, Farr S, Mansfield C. Chronic exertional compartment syndrome in athletes: an overview of the current literature. *Cureus.* 2023. https://doi.org/10.7759/cureus.47797
