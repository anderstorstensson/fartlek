---
title: "Sports Nutrition for Endurance Runners: Permitted Ergogenic Aids and Recovery Nutrition"
subtitle: "An evidence synthesis, tiered by strength of evidence, for a coaching agent"
author: "Fartlek project — literature review"
date: "2026-07-19"
---

# Sports Nutrition for Endurance Runners

**Permitted ergogenic aids and recovery nutrition — a tiered evidence synthesis**

## Executive summary

This review is the companion to `endurance-training-science-review.md`. That document covers
training design; this one covers what the athlete eats and ingests **around** that training —
specifically (a) legal ergogenic aids and (b) recovery nutrition.

Its purpose is narrow and practical: the coaching agent cites this document when it prescribes
something to an athlete, so every claim here carries an explicit **evidence tier**. Two agents
with identical mechanisms of action can sit three tiers apart, and the coach must not present
them with equal confidence.

Headline conclusions:

- **Caffeine is the only ergogenic aid in this review with strong, consistent evidence for
  distance running**, at 3–6 mg·kg⁻¹ roughly 60 min pre-race, with meaningful effects on both
  time-trial performance and time to exhaustion.[^4][^5][^6]
- **Dietary nitrate works, but mostly in the athletes who need it least.** Benefits are
  reasonably established in recreational-to-moderately-trained runners and are attenuated or
  absent in highly trained endurance athletes.[^11][^12]
- **Sodium bicarbonate and beta-alanine are Tier-A supplements for the wrong events.** Both act
  on the buffering of high-intensity acidosis and are established for efforts of roughly 30 s to
  12 min — relevant to 800 m–3000 m, largely irrelevant to half-marathon and marathon.[^15][^16]
- **Creatine's evidence is strong but its use case in distance running is narrow**, limited to
  race-defining surges and end-spurts, and offset by a 0.5–1.5 kg body-mass increase that is a
  direct penalty in a weight-bearing sport.[^13][^14]
- **Ketone esters do not improve endurance performance.** Meta-analysis found no effect
  (Hedges' *g* = 0.14, *p* = .42).[^17]
- **Sulforaphane / broccoli sprouts are emerging at best**, with one promising training study and
  one null acute trial — not a basis for prescription.[^22][^23]
- **Tart cherry has modest, low-to-moderate-certainty support for recovery** — and, being an
  anti-inflammatory polyphenol, belongs in race week and competition blocks rather than in
  adaptation-seeking training blocks.[^18][^19][^20]
- **The adaptation-blunting problem is the key cross-cutting caveat.** High-dose antioxidants
  blunt the molecular signalling that drives endurance adaptation; the coach should treat any
  antioxidant/anti-inflammatory aid as a *competition* tool, not a *training* tool.[^24][^25]
- **Recovery nutrition beats supplements in effect size.** Daily protein around
  1.6–1.8 g·kg⁻¹·d⁻¹ distributed across the day, and post-exercise carbohydrate near
  1.0 g·kg⁻¹·h⁻¹ when sessions are closely spaced, are the highest-yield interventions
  here.[^26][^27][^28][^29]
- **Two things reliably make an athlete slower**: alcohol after a hard session (24–37% suppression
  of post-exercise myofibrillar protein synthesis) and untreated iron deficiency.[^32][^33]
- **Supplements carry a real contamination risk.** Roughly a quarter of analytical anti-doping
  cases in one national programme involved a claimed supplement source; only third-party-tested
  products should ever be named.[^2][^3]

---

## 1. Scope, method, and boundary with the training-science review

**Objective.** Summarise the defensible evidence on legal ergogenic aids and recovery nutrition
for endurance runners, tiered so that a coaching agent can distinguish "prescribe this" from
"mention as experimental" from "do not recommend".

**Type.** Narrative / scoping synthesis, not a PRISMA meta-analysis — the goal is usable,
gradeable guidance rather than a pooled effect estimate.

**Boundary with `endurance-training-science-review.md` (important).** That review's **§12
(Fuelling)** owns two topics and this document does **not** restate them:

| Topic | Lives in |
|---|---|
| Carbohydrate *during* exercise, race-day intake (~60–90 g·h⁻¹), gut training | training-science review §12 |
| Carbohydrate periodization / "train low" / fuel-for-the-work-required | training-science review §12 |
| Carbohydrate *after* exercise for glycogen resynthesis | **here, §13** |
| Heat, sweat rate, and racing-warm fluid strategy | training-science review §13 |
| Hydration, sodium and hyponatremia as a general rule | **here, §14** |
| Energy availability and RED-S | training-science review §14 |
| Protein, ergogenic aids, alcohol, micronutrients, connective tissue | **here** |

Where the two overlap, the training-science review is authoritative for the during-exercise case
and this document cross-references it rather than duplicating numbers.

**Search.** Targeted per-theme web searches (July 2026) across scholarly sources, prioritising
consensus statements and position stands (IOC, ACSM/Academy of Nutrition and Dietetics/Dietitians
of Canada, ISSN), then systematic reviews, meta-analyses and umbrella reviews, then landmark
primary trials where no synthesis exists. Themes: caffeine; dietary nitrate; creatine; sodium
bicarbonate; beta-alanine; ketone esters; tart cherry and polyphenols; sulforaphane / broccoli
sprouts; antioxidant interference with adaptation; protein requirement, dose and distribution;
post-exercise glycogen resynthesis; hydration and exercise-associated hyponatremia; alcohol; iron
and vitamin D; collagen/gelatin; supplement contamination and anti-doping risk.

**Citation integrity.** Every reference here was first located in live literature search and then
its metadata (authors, year, journal, volume, pages, DOI) retrieved from CrossRef — no citation
was reconstructed from memory, and no DOI was guessed. Where a search surfaced a title but no
DOI, the DOI was resolved by bibliographic query and the returned title checked against the seed
before use. 36 references are cited; the retrieval script is `docs/sources/fetch_nutrition_bib.py`,
and all 35 DOIs resolve (`sports-nutrition-review_citation_report.json`).

**What that verification does and does not cover.** DOI resolution confirms a citation points at a
real paper with the stated authors, journal and year. It does *not* confirm that a quoted number
appears in that paper. The specific effect sizes quoted below were drawn from literature-search
summaries; the three most quotable — the ketone meta-analysis pooled effect, the tart cherry effect
sizes, and the alcohol protein-synthesis percentages — were additionally checked against the source
abstracts and matched exactly. The remaining numeric claims carry search-summary provenance, so
treat any figure the coach is about to quote to an athlete as worth confirming at source first.

**How to read each theme.** *Concept → Evidence → Tier → Implication for coaching.*

---

## 2. The tiering scheme — read this before prescribing anything

**Concept.** Sports supplements differ enormously in evidence quality, and the failure mode for
an automated coach is presenting a weakly-supported compound in the same confident register as a
well-supported one. This review therefore labels every agent with a tier, adapted from the
structure of the Australian Institute of Sport Sports Supplement Framework's ABCD system[^36] and
the graded approach of the IOC consensus statement on dietary supplements.[^2]

| Tier | Meaning | How the coach should speak about it |
|---|---|---|
| **A** | Strong evidence of benefit in a relevant context; safe at recommended doses | May prescribe with a specific protocol |
| **A‑mismatch** | Strong evidence, but for events or demands this athlete does not race | Mention only if the athlete races the relevant distance |
| **B** | Emerging or context-dependent; effect real but small, inconsistent, or population-limited | Offer as optional and explicitly experimental; never in a race plan the athlete depends on |
| **C** | Insufficient evidence, or good evidence of *no* benefit | Do not recommend; say plainly that the evidence does not support it |

**Evidence.** Nutrition makes a small but real contribution to elite performance, and supplements
a minor contribution within that — while supplement use is near-universal across all levels of
sport, which is precisely the gap this tiering is meant to close.[^2] The foundational position
statements are consistent that food-first strategies and adequate energy availability dominate
the effect sizes available from any pill.[^1][^2]

**The risk side is not optional.** Supplement contamination is a documented and substantial route
to anti-doping rule violations: in one national anti-doping programme covering 2003–2020, 26% of
analytical violation cases involved an athlete claiming a dietary supplement as the source, with
supporting evidence in roughly 14% of all cases.[^3]

**Implication for coaching.**
- State the tier whenever an aid is named. A Tier-B suggestion phrased like a Tier-A prescription
  is a defect, not a stylistic choice.
- Never introduce a new supplement in race week that has not been rehearsed in training —
  the same "nothing new on race day" rule the training-science review applies to fuelling.
- If the athlete competes under anti-doping jurisdiction, name only third-party-tested products
  and say why.[^2][^3]
- Food first. If daily protein, carbohydrate, iron status or sleep are unaddressed, fix those
  before discussing any Tier-A supplement — the effect sizes are not comparable.[^1]

---

## 3. Caffeine — Tier A

**Concept.** An adenosine-receptor antagonist that reduces perception of effort and pain and
increases central drive; the most consistently ergogenic legal compound in endurance sport.

**Evidence.**
- An **umbrella review of 21 published meta-analyses** found caffeine ergogenic across aerobic
  endurance, muscular endurance, strength, power and speed, with the effects on aerobic endurance
  supported by *moderate* quality of evidence.[^5]
- The **ISSN position stand** concludes that caffeine acutely enhances many aspects of exercise
  performance, with the well-supported dose range at **3–6 mg·kg⁻¹ body mass**, typically taken
  ~60 min before exercise; lower doses (~200 mg) are also effective for some outcomes, and doses
  above ~9 mg·kg⁻¹ add side effects without adding benefit.[^4]
- **Running-specific meta-analysis** confirms the effect in this modality: a medium-sized
  ergogenic effect on time to exhaustion and a smaller effect on running time-trial performance,
  across doses of 3–9 mg·kg⁻¹.[^6]
- **Genotype does not currently justify individualised dosing.** A systematic review of *CYP1A2*
  (rs762551) found that where genotype differences reached significance the AA ("fast metaboliser")
  group responded more favourably, but the evidence overall is inconsistent and not a basis for
  withholding caffeine from any athlete.[^7]

**The sleep cost is the real constraint.** Caffeine's downside for a training athlete is not
performance but recovery, and this interacts directly with the training-science review's §11
(sleep and readiness):
- Meta-analysis: caffeine reduced total sleep time by **~45 min**, cut sleep efficiency by ~7%,
  and increased sleep-onset latency (+9 min) and wake-after-sleep-onset (+12 min).[^8]
- A dose–timing randomised crossover trial gives usable thresholds: **100 mg can be taken up to
  4 h before bed** without significant effect, whereas **400 mg delays sleep onset and alters
  sleep architecture when taken within 12 h of bedtime**, with markedly greater fragmentation
  inside 8 h.[^9]
- Meta-analysis specific to **caffeine taken before late-afternoon or evening training or
  competition** confirms measurable subsequent sleep disruption in athletes — the exact scenario
  of an evening race or a late quality session.[^10]

**Implication for coaching.**
- **Race day**: 3–6 mg·kg⁻¹ ~60 min before the start is a defensible default for any race
  distance. For a 70 kg athlete that is roughly 210–420 mg. Rehearse the dose in at least one
  key session before racing it — GI tolerance and jitteriness are individual.[^4]
- **Key workouts**: the same dose is legitimate for a hard session the athlete wants to hit, but
  weigh it against the sleep cost if the session is in the afternoon or evening.[^8][^9][^10]
- **Timing rule to apply**: for an evening race or session, expect a sleep debt and plan the next
  day as recovery. Do not schedule a demanding session the morning after evening caffeine.
- Do not manipulate habitual intake ("caffeine deloading") as part of a plan; the evidence for
  withdrawal protocols is not strong enough to justify the disruption.[^4]

---

## 4. Dietary nitrate / beetroot — Tier B for trained runners

**Concept.** Dietary nitrate is reduced to nitrite and then nitric oxide, improving vasodilation,
muscle oxygen delivery and mitochondrial efficiency — mechanistically, a reduction in the oxygen
cost of submaximal exercise.

**Evidence.**
- An **umbrella review** of beetroot juice in professional athletes and healthy individuals
  concluded that benefits are clearest in individuals of **low-to-moderate training status** and
  that highly trained endurance athletes derive fewer or no significant performance
  benefits — plausibly because their baseline NO bioavailability and efficiency are already
  high.[^11]
- A **systematic review and meta-analysis specific to high-intensity endurance time-trial
  performance** likewise reports mixed results, with effectiveness varying by training status and
  protocol.[^12]
- Where protocols do work, they cluster around **8.3–16.4 mmol nitrate** taken **2–3 h before**
  exercise, or **chronic loading for ≥3 days**; single small doses are unreliable.[^11]

**Tier B, explicitly.** The mechanism is sound and the compound is safe and legal, but the
population in which it is best supported is not the well-trained runner, and the individual
response is variable.

**Implication for coaching.**
- Offer to a **recreational or moderately trained** athlete as an optional, clearly experimental
  addition for a goal race: ~2–3 h pre-race, or a 3–6 day loading block ending on race day.[^11]
- For a **well-trained** athlete, state honestly that the expected benefit is small and may be
  absent, and do not build a race plan that assumes it.[^11][^12]
- If tried, it must be rehearsed — beetroot juice commonly causes GI discomfort and always
  discolours urine and stool, which will alarm an unprepared athlete.
- Note that antibacterial mouthwash abolishes the oral-bacteria nitrate-reduction step; an athlete
  supplementing nitrate should not use it in that window.

---

## 5. Creatine — Tier A for the mechanism, narrow use in distance running

**Concept.** Creatine monohydrate loads muscle phosphocreatine, buffering ATP resynthesis during
short, high-intensity efforts. Its endurance relevance is not steady-state pace but the ability to
repeat and sustain surges.

**Evidence.**
- The **ISSN position stand** calls creatine monohydrate the most effective ergogenic supplement
  available for increasing high-intensity exercise capacity and lean mass, and finds it safe and
  well tolerated in healthy people over short and long-term use.[^13]
- A **review focused specifically on endurance performance** concludes creatine's promise for
  endurance athletes lies in **surges in intensity and end-spurts** — the race-defining moments —
  rather than in average pace, alongside possible secondary effects on glycogen storage, calcium
  handling and reduced oxidative stress.[^14]
- The countervailing fact for runners: creatine reliably increases body mass by roughly
  **0.5–1.5 kg**, largely intramuscular water, which is a direct cost in a weight-bearing
  sport.[^13][^14]

**Implication for coaching.**
- **Do not recommend as a default for half-marathon or marathon athletes.** The mass penalty is
  certain, and the benefit — surge capacity — is not what limits those events.
- **Reasonable to raise** for a middle-distance runner (800 m–5000 m) whose races are decided by
  end-spurts and mid-race surges, or for an athlete doing meaningful concurrent strength work.[^14]
- If used: 3–5 g·d⁻¹ maintenance is sufficient; a 20 g·d⁻¹ loading week only accelerates
  saturation.[^13]
- Never start creatine inside a taper — the acute mass gain arrives exactly when the athlete is
  weighing themselves and reading meaning into it.

---

## 6. Sodium bicarbonate — Tier A‑mismatch

**Concept.** An extracellular buffer that raises blood bicarbonate and pH, delaying the
performance consequences of high-intensity acidosis.

**Evidence.** The **ISSN position stand** finds bicarbonate improves performance in high-intensity
running, cycling, swimming and rowing at doses of **0.2–0.5 g·kg⁻¹**, with the **optimal dose
around 0.3 g·kg⁻¹** taken **60–180 min** before exercise. Crucially, the ergogenic effects are
established for exercise **lasting roughly 30 s to 12 min**.[^15]

**Implication for coaching.**
- **Relevant to 800 m–3000 m racing and to sessions of repeated maximal intervals.** Not relevant
  to half-marathon or marathon pace, and the coach should say so rather than staying silent.
- GI distress is the limiting side effect and is common at the top of the dose range; if raised at
  all, it must be trialled in training well before any race.[^15]

---

## 7. Beta-alanine — Tier A‑mismatch

**Concept.** Chronic beta-alanine supplementation raises muscle carnosine, an intracellular pH
buffer — the intramuscular counterpart to bicarbonate's extracellular action.

**Evidence.** The **ISSN position stand** reports that **4–6 g·d⁻¹ for at least 2–4 weeks**
significantly increases muscle carnosine and improves exercise performance, **most pronounced in
open-endpoint tasks and time trials lasting 1–4 min**. It appears safe at recommended doses; the
only commonly reported side effect is paraesthesia (tingling), attenuated by splitting into
smaller (~1.6 g) doses or using sustained-release forms.[^16]

**Implication for coaching.**
- Same verdict as bicarbonate: the supported effect window (1–4 min) maps onto **1500 m–3000 m**,
  not to the long-distance events most recreational goal races target.
- Unlike caffeine or bicarbonate, this is a **chronic loading** protocol — it must begin weeks
  before the target race, which makes it a planning item, not a race-week decision.[^16]

---

## 8. Ketone esters — Tier C

**Concept.** Exogenous ketone monoesters and precursors were proposed as an alternative fuel that
spares glycogen and improves efficiency.

**Evidence.** A **systematic review and meta-analysis** of acute ketone monoester and precursor
ingestion found **no significant effect on endurance performance** (Hedges' *g* = 0.136,
95% CI −0.195 to 0.467, *p* = .419).[^17] The compounds are also expensive and frequently cause GI
distress.

**Implication for coaching.** Do not recommend. If an athlete raises them, state plainly that
meta-analysis shows no performance benefit, and redirect the attention (and money) to
carbohydrate intake during racing, which is well supported — see training-science review §12.[^17]

---

## 9. Tart cherry and polyphenols — Tier B, and competition-phase only

**Concept.** Montmorency tart cherry is rich in anthocyanins with antioxidant and
anti-inflammatory action, proposed to accelerate recovery from muscle-damaging exercise. Its
mechanism is precisely why its timing matters (see §11).

**Evidence.**
- **Meta-analysis (14 studies)** found a **small** beneficial effect on muscle soreness
  (ES = −0.44) and a **moderate** effect on recovery of muscular strength (ES = −0.78).[^18]
- A **2026 systematic review and meta-analysis (19 trials)** found tart cherry juice significantly
  improved recovery of maximal voluntary contraction across time points, but explicitly noted the
  findings are **heterogeneous and supported by low-to-moderate certainty of evidence, warranting
  cautious interpretation**.[^19]
- A conceptual review argues the mechanism is better understood as **"precovery"** —
  supplementation *before* the damaging bout, priming the athlete — than as post-hoc repair,
  which changes when it would be taken.[^20]
- **Sleep** claims are weaker than commonly presented: a randomised controlled trial in elite
  athletes found tart cherry juice **did not change melatonin or cortisol**, though some
  actigraphy sleep-quality measures improved.[^21]

**Implication for coaching.**
- Tier B: mention as optional for a **congested competition period or a multi-day race block**,
  where recovering fast between efforts outranks adapting.
- **Do not prescribe through a training block.** As an anti-inflammatory antioxidant it falls
  under the adaptation-blunting caveat in §11 — blunting the very inflammatory signal the training
  is meant to provoke.[^24][^25]
- If used, the "precovery" framing means starting **several days before** the target
  event rather than only after it.[^20]
- Do not sell it as a sleep aid; the objective hormonal evidence did not support that.[^21]

---

## 10. Sulforaphane / broccoli sprouts — Tier C (genuinely emerging)

**Concept.** Glucosinolates in broccoli sprouts yield sulforaphane, an activator of the Nrf2
pathway — which, unlike direct antioxidants, upregulates the body's *endogenous* antioxidant
defences. That mechanistic distinction is the reason it is interesting rather than merely another
antioxidant.

**Evidence.**
- A **randomised training study** found glucosinolate-rich broccoli sprout supplementation
  protected against oxidative stress and improved adaptations to intense exercise training —
  a genuinely promising result, and notably one where the antioxidant action did *not* appear to
  blunt adaptation.[^22]
- An **acute crossover trial** (17 healthy men, broccoli powder vs. spinach placebo over 2 weeks)
  found that although urinary sulforaphane output rose markedly, confirming bioavailability, there
  was **no effect on exercise-induced oxidative stress markers, blood lactate dynamics, exercise
  test performance, or functional recovery**. The authors attributed the null result partly to the
  mild exercise stimulus used.[^23]

**Implication for coaching.**
- **Tier C — do not prescribe.** Two small studies pointing in different directions, in small
  mostly-male samples, with no dose-response consensus and no runner-specific outcome data.
- If the athlete asks (this is a fashionable supplement), the honest answer is: mechanistically
  interesting, one encouraging training study, one null acute trial, not enough to recommend.
- Whole broccoli sprouts as *food* are harmless and need no discouraging — the Tier-C verdict is
  about prescribing a supplement and expecting a performance effect.

---

## 11. The adaptation-blunting problem — the cross-cutting caveat

**Concept.** Endurance adaptation is driven in part by exercise-induced reactive oxygen species
and inflammatory signalling. Suppressing that signal with high-dose antioxidants can suppress the
adaptation along with it. This section governs how §9 and §10 must be applied, and is the single
most important nuance in this document.

**Evidence.**
- **Paulsen et al.**, a double-blind randomised controlled trial, found that high-dose vitamin C
  and E supplementation **blunted the training-induced increase in mitochondrial markers**: COX4
  rose 59% and PGC-1α 19% in the placebo group, with **no increase in the supplemented group**.
  Notably, training-induced improvements in V̇O₂max and running performance were **not detectably
  affected** over the trial period — the effect was demonstrated at the molecular level.[^24]
- A **review of the broader question** concludes that antioxidant supplementation may blunt
  adaptations such as training-induced mitochondrial biogenesis, while noting human studies remain
  sparse and results conflicting.[^25]

**Read this honestly.** The molecular evidence is solid; the performance evidence is not yet.
The defensible position is therefore precautionary rather than alarmist: there is no demonstrated
performance benefit from high-dose antioxidant supplementation, and a plausible mechanistic cost,
so the risk-reward favours not taking them during adaptation-seeking training.

**Implication for coaching.**
- **Rule of thumb: antioxidant and anti-inflammatory aids are competition tools, not training
  tools.** Use them when the goal is to recover fast between efforts (race week, multi-day
  competition, congested racing). Avoid them when the goal is to adapt (base, build, any block
  where the training stimulus is the point).[^24][^25]
- **This is one principle with two instances, not a nutrition-only quirk.** The training-science
  review reaches the same conclusion from a completely different literature: habitual
  post-session **cold-water immersion** blunts the adaptation it is meant to aid, so it too is
  reserved for congested racing and kept out of adaptation blocks (training-science review §13).
  The general rule the coach should carry is that **any intervention which suppresses the
  post-session stress signal trades adaptation for short-term recovery** — which is a good trade
  in competition and a bad one in a training block.
- **But the two are not interchangeable, and the difference matters.** Cold-water immersion's
  blunting is *selective*: it harms strength adaptation (SMD −0.60) while leaving endurance
  adaptation essentially untouched (SMD ≈ 0.00). High-dose antioxidants blunt the *endurance*
  side — the mitochondrial signalling running training exists to provoke. So an athlete doing
  2×/week strength work for economy has a cold-water problem, and the same athlete in a base
  block has an antioxidant problem. Do not collapse them into a single "avoid recovery
  modalities" message.
- This applies directly to tart cherry (§9) and to high-dose vitamin C/E; it does **not** clearly
  apply to Nrf2-pathway compounds like sulforaphane, which upregulate endogenous defences rather
  than swamping the signal — one reason that line of research is interesting.[^22]
- Do not recommend routine high-dose vitamin C or E supplementation to a training runner at
  all.[^24][^25]
- Nothing here argues against dietary antioxidants from ordinary food; the concern is
  supra-physiological supplement doses.

---

## 12. Protein: daily requirement, per-dose, and distribution

**Concept.** Endurance runners are routinely under-advised on protein, which is framed as a
strength-sport concern. It is not: protein supports mitochondrial and structural remodelling and
attenuates the muscle damage of high-volume running.

**Evidence.**
- **Requirement is higher than the standard advice.** Using the indicator amino acid oxidation
  method in endurance-trained adults after a 20 km run, the estimated average requirement was
  **1.65 g·kg⁻¹·d⁻¹** and the recommended intake **1.83 g·kg⁻¹·d⁻¹** — above the RDA
  (0.8) and above the then-current endurance guidance of 1.2–1.4 g·kg⁻¹·d⁻¹.[^27]
- **Per-dose and distribution.** The ISSN position stand recommends **~0.25 g·kg⁻¹ per serving**
  (or an absolute 20–40 g), ideally containing 700–3000 mg leucine, **distributed every 3–4 h
  across the day**. The anabolic response to exercise persists for at least 24 h, so exact timing
  matters less than total intake and distribution.[^26]
- **Endurance-specific synthesis** confirms the metabolic focus for endurance athletes is
  promoting recovery and training adaptation rather than hypertrophy, which reframes protein as a
  recovery-and-remodelling nutrient rather than a mass-gain one.[^28]

**Implication for coaching.**
- Target **1.6–1.8 g·kg⁻¹·d⁻¹** on training days for a runner in a meaningful block — for a
  70 kg athlete, roughly 112–126 g·d⁻¹.[^27]
- Prescribe **distribution, not timing panic**: ~4 doses of 25–35 g spread across the day beats
  one large dose plus a "recovery window" scramble.[^26]
- A protein dose within an hour or two of hard sessions and long runs is sensible practice, but
  the coach should not present a narrow anabolic window as established — it is not.[^26]
- Protein intake interacts with energy availability (training-science review §14): in an athlete
  who may be under-fuelling, raising protein without raising total energy is the wrong first move.

---

## 13. Post-exercise carbohydrate and glycogen resynthesis

**Concept.** Refilling muscle glycogen after a session. Distinguish this sharply from
during-exercise carbohydrate, which is training-science review §12's territory.

**Evidence.**
- A **systematic review and meta-analysis** found that carbohydrate ingestion during recovery
  (**~1.0 g·kg⁻¹·h⁻¹**) improved the rate of muscle glycogen resynthesis compared with water,
  and — the important negative finding — that **co-ingesting protein with carbohydrate neither
  enhanced nor impeded** the rate of glycogen resynthesis compared to carbohydrate alone.[^29]
- The practical corollary from the same work: athletes with limited recovery time between
  consecutive sessions should prioritise **regular carbohydrate intake** rather than optimising
  the protein-to-carbohydrate ratio.[^29]
- A **narrative review of post-exercise recovery nutrition** places this in context: carbohydrate
  is essential for glycogen replenishment particularly in the first hours post-exercise, with
  effects depending on type, timing and amount.[^30]

**Implication for coaching.**
- **Aggressive post-exercise carbohydrate only matters when recovery time is short** — two
  sessions in a day, back-to-back quality days, or a multi-day race. In those cases prescribe
  ~1.0 g·kg⁻¹·h⁻¹ for the first few hours (≈70 g·h⁻¹ for a 70 kg athlete).[^29]
- **When the next hard session is 24 h away or more, this is a non-issue** — total daily
  carbohydrate does the work and the athlete does not need a stopwatch. Do not manufacture
  urgency the evidence does not support.
- Still recommend protein alongside, but for the §12 reasons (remodelling), **not** because it
  speeds glycogen resynthesis — it does not.[^29]

---

## 14. Hydration, sodium, and exercise-associated hyponatremia

**Concept.** The failure mode that actually kills endurance runners is not dehydration but
overdrinking. This section covers the general rule; heat-specific fluid and cooling strategy is
training-science review §13.

**Evidence.** The **Third International Exercise-Associated Hyponatremia Consensus** concluded
that **overdrinking beyond thirst**, together with non-osmotic arginine vasopressin release, is
the most common cause of exercise-associated hyponatremia, and that using the innate thirst
mechanism to guide fluid intake both limits excess drinking and prevents excessive
dehydration.[^31]

**Implication for coaching.**
- The default prescription is **drink to thirst**. Do not give a runner a fixed
  millilitres-per-hour target to hit regardless of sensation, and never advise pre-emptive
  drinking "to stay ahead".[^31]
- Marathon and ultra plans should say this explicitly, because race-day advice from other sources
  frequently contradicts it.
- Sodium-containing drinks are reasonable for long, hot efforts and heavy sweaters, but sodium
  does not license overdrinking — the volume rule is the one that matters.[^31]
- Athletes who *gain* weight over a long race were drinking too much; that is the flag to look for
  in a post-race debrief.

---

## 15. Alcohol

**Concept.** The most commonly ingested substance that measurably degrades recovery, and the one
athletes least expect to see in a training plan.

**Evidence.** In a randomised crossover trial, alcohol ingested after a bout of concurrent
exercise **reduced rates of myofibrillar protein synthesis by 24% when co-ingested with protein
and by 37% when co-ingested with carbohydrate**, relative to protein alone — that is, protein does
not rescue the effect.[^32]

**Implication for coaching.**
- Where an athlete's check-ins mention regular post-session drinking, it is legitimate and
  evidence-based to raise it as a recovery issue, not a lifestyle judgement.[^32]
- The highest-value specific advice: avoid alcohol **after key sessions and long runs**, and in
  the days before a goal race — the sessions the athlete most wants to convert into adaptation.
- Note the compounding effect with sleep (training-science review §11); alcohol degrades sleep
  architecture as well as protein synthesis.

---

## 16. Micronutrients worth actually checking: iron and vitamin D

**Concept.** Most micronutrient supplementation in athletes is unnecessary. Two are exceptions
because deficiency is common in runners *and* has a demonstrable performance or injury cost.

**Evidence.**
- **Iron.** A systematic review of iron deficiency, supplementation and sports performance in
  female athletes documents both the elevated prevalence in this population and the performance
  relevance of correcting it — distance runners are among the most affected groups, via
  foot-strike hemolysis, sweat and GI losses, and (in female athletes) menstrual losses.[^33]
- **Vitamin D.** A review focused on physical performance and musculoskeletal injuries in athletes
  finds the most consistent association is with **impaired bone health and increased bone stress
  injury risk**, while the evidence for a direct performance effect remains inconclusive.
  Deficiency is more common in winter and in athletes with limited sun exposure.[^34]

**Implication for coaching.**
- These are **testing recommendations, not supplement recommendations**. The correct coaching move
  is to suggest the athlete get ferritin (and, at northern latitudes in winter, 25(OH)D) checked by
  a clinician — never to prescribe a dose.[^33][^34]
- **Raise iron testing when the data justifies it**: unexplained decoupling of pace and heart
  rate, persistent fatigue despite adequate load and sleep, or a plateau that training-side
  explanations do not cover. The training-science review's durability and load sections should be
  ruled out first.
- **Raise vitamin D** in the context of a bone stress injury or a history of them, and at Nordic
  latitudes through winter — the athlete in this project trains in Sweden, where winter status is
  a live concern.[^34]
- Iron supplementation without a documented deficiency is not benign; iron overload is harmful.
  Defer to the clinician on dose and duration.

---

## 17. Connective tissue: collagen and gelatin — Tier B

**Concept.** Tendon and ligament collagen synthesis may be stimulated by ingesting collagen
precursors with vitamin C shortly before loading the tissue — relevant to runners because
Achilles and patellar tendon problems are among the most common training-limiting injuries.

**Evidence.** In a randomised trial, **vitamin C-enriched gelatin taken ~1 h before intermittent
activity increased circulating markers of collagen synthesis**, supporting a role for timed
supplementation around connective-tissue loading.[^35] The typical protocol derived from this line
of work is ~15 g gelatin or hydrolysed collagen plus ~50 mg vitamin C, taken 30–60 min before
loading.

**Implication for coaching.**
- Tier B: the biomarker evidence is real, but the leap from circulating collagen markers to fewer
  tendon injuries in runners is not yet demonstrated.
- Reasonable to mention to an athlete with a **history of tendinopathy** who is also doing the
  loading rehabilitation that actually has the evidence behind it — as an adjunct, never a
  substitute.
- The timing is the whole intervention: taken 30–60 min **before** the loading session, not after.

---

## 18. Synthesis: an evidence map for the coach

| Agent | Tier | Best-supported use | Protocol if used | Refs |
|---|---|---|---|---|
| **Caffeine** | A | Any race distance; key sessions | 3–6 mg·kg⁻¹, ~60 min pre; mind evening sleep cost | [^4][^5][^6][^8][^9] |
| **Dietary nitrate** | B | Recreational/moderately trained, goal race | 8.3–16.4 mmol, 2–3 h pre or ≥3 d loading | [^11][^12] |
| **Creatine** | A (narrow) | 800 m–5 000 m surges; concurrent strength work | 3–5 g·d⁻¹; expect +0.5–1.5 kg mass | [^13][^14] |
| **Sodium bicarbonate** | A‑mismatch | 30 s–12 min efforts (800 m–3 000 m) | 0.3 g·kg⁻¹, 60–180 min pre; GI risk | [^15] |
| **Beta-alanine** | A‑mismatch | 1–4 min efforts (1 500 m–3 000 m) | 4–6 g·d⁻¹ for 2–4+ weeks; split doses | [^16] |
| **Ketone esters** | C | — (no effect on endurance performance) | Do not recommend | [^17] |
| **Tart cherry** | B | Congested racing / multi-day competition only | Start days before; avoid in training blocks | [^18][^19][^20] |
| **Sulforaphane / broccoli sprouts** | C | — (emerging, conflicting) | Do not prescribe; food is fine | [^22][^23] |
| **High-dose vitamin C/E** | C (avoid) | — (blunts adaptation signalling) | Do not recommend to a training runner | [^24][^25] |
| **Protein** | Foundational | Every training block | 1.6–1.8 g·kg⁻¹·d⁻¹, ~0.25 g·kg⁻¹ every 3–4 h | [^26][^27][^28] |
| **Post-exercise carbohydrate** | Foundational | Only when recovery <24 h | ~1.0 g·kg⁻¹·h⁻¹ for first hours | [^29][^30] |
| **Fluid** | Foundational | All endurance racing | Drink to thirst; never a fixed forced volume | [^31] |
| **Alcohol** | Avoid | — | Avoid after key sessions and pre-race | [^32] |
| **Iron / vitamin D** | Test, don't dose | Suspected deficiency; bone stress injury | Refer for blood test; clinician prescribes | [^33][^34] |
| **Collagen + vitamin C** | B | Tendinopathy history, alongside loading rehab | ~15 g + ~50 mg vit C, 30–60 min *before* loading | [^35] |

**Phase mapping.** The distinction that matters most operationally:

- **Base / build blocks** — adaptation is the goal. Protein, total carbohydrate, iron status,
  sleep and alcohol avoidance. **No antioxidant or anti-inflammatory aids.**[^24][^25]
- **Race-specific block** — rehearse what will be used on race day: caffeine dose, nitrate if
  chosen, and the during-race fuelling protocol from training-science review §12.
- **Race week / competition period** — the only window where recovery-focused anti-inflammatory
  aids (tart cherry) are defensible, and where nothing new should be introduced.[^2]
- **Multi-day or congested racing** — post-exercise carbohydrate timing becomes genuinely
  important; adaptation concerns are temporarily secondary.[^29]

---

## 19. Limitations, and what this review does not license

- **Narrative, not systematic.** No PRISMA screening, no formal risk-of-bias scoring, no pooled
  effect estimates of our own. Tiers reflect the weight and consistency of the cited syntheses,
  not a formal GRADE assessment.
- **Sex bias in the underlying literature is substantial.** Several key trials here are
  male-only or male-dominated (the alcohol trial, the acute broccoli trial, and much of the
  ketone literature). Recommendations for female athletes carry more uncertainty than the tiers
  alone suggest, and should be read alongside training-science review §14.
- **Individual variation is large and largely unpredictable.** Caffeine, nitrate and every GI-active
  compound here vary substantially between people. Rehearsal in training is not a nicety; it is the
  only individualisation mechanism available.
- **Effect sizes are small relative to training.** Nothing in this document competes with
  consistency, adequate energy availability, sleep and a well-designed plan. If the coach finds
  itself discussing supplements with an athlete whose sleep or fuelling is unaddressed, the
  priority ordering is wrong.[^1][^2]
- **Not medical advice.** Iron, vitamin D and any clinical question belong to a clinician. The
  coach's role is to notice the pattern and recommend testing.
- **Anti-doping status changes.** Everything covered here is permitted as of the search date
  (July 2026), but the coach should not assert current WADA status from this document alone.
- **Recency and drift.** This review reflects searches conducted in July 2026. Tart cherry,
  sulforaphane and ketone research are all active; the Tier-B and Tier-C verdicts here are the
  ones most likely to move.

---

## References

[^1]: Thomas DT, Erdman KA, Burke LM. Position of the Academy of Nutrition and Dietetics, Dietitians of Canada, and the American College of Sports Medicine: nutrition and athletic performance. *J Acad Nutr Diet.* 2016;116(3):501–528. https://doi.org/10.1016/j.jand.2015.12.006

[^2]: Maughan RJ, Burke LM, Dvorak J, et al. IOC consensus statement: dietary supplements and the high-performance athlete. *Br J Sports Med.* 2018;52(7):439–455. https://doi.org/10.1136/bjsports-2018-099027

[^3]: Lauritzen F. Dietary supplements as a major cause of anti-doping rule violations. *Front Sports Act Living.* 2022;4:868228. https://doi.org/10.3389/fspor.2022.868228

[^4]: Guest NS, VanDusseldorp TA, Nelson MT, et al. International Society of Sports Nutrition position stand: caffeine and exercise performance. *J Int Soc Sports Nutr.* 2021;18(1):1. https://doi.org/10.1186/s12970-020-00383-4

[^5]: Grgic J, Grgic I, Pickering C, Schoenfeld BJ, Bishop DJ, Pedisic Z. Wake up and smell the coffee: caffeine supplementation and exercise performance — an umbrella review of 21 published meta-analyses. *Br J Sports Med.* 2019;54(11):681–688. https://doi.org/10.1136/bjsports-2018-100278

[^6]: Wang Z, Qiu B, Gao J, Del Coso J. Effects of caffeine intake on endurance running performance and time to exhaustion: a systematic review and meta-analysis. *Nutrients.* 2022;15(1):148. https://doi.org/10.3390/nu15010148

[^7]: Grgic J, Pickering C, Del Coso J, Schoenfeld BJ, Mikulic P. CYP1A2 genotype and acute ergogenic effects of caffeine intake on exercise performance: a systematic review. *Eur J Nutr.* 2020;60(3):1181–1195. https://doi.org/10.1007/s00394-020-02427-6

[^8]: Gardiner C, Weakley J, Burke LM, et al. The effect of caffeine on subsequent sleep: a systematic review and meta-analysis. *Sleep Med Rev.* 2023;69:101764. https://doi.org/10.1016/j.smrv.2023.101764

[^9]: Gardiner CL, Weakley J, Burke LM, et al. Dose and timing effects of caffeine on subsequent sleep: a randomized clinical crossover trial. *Sleep.* 2024;48(4):zsae230. https://doi.org/10.1093/sleep/zsae230

[^10]: Kocak A, Georgousopoulou E, Knight-Agarwal CR, Matthews R, et al. The effect of consuming caffeine before late afternoon/evening training or competition on sleep: a systematic review with meta-analysis. *Sports.* 2025;13(9):317. https://doi.org/10.3390/sports13090317

[^11]: Tian C, Jiang Q, Han M, et al. Effects of beetroot juice on physical performance in professional athletes and healthy individuals: an umbrella review. *Nutrients.* 2025;17(12):1958. https://doi.org/10.3390/nu17121958

[^12]: Wong TH, Sim A, Burns SF. The effects of nitrate ingestion on high-intensity endurance time-trial performance: a systematic review and meta-analysis. *J Exerc Sci Fit.* 2022;20(4):305–316. https://doi.org/10.1016/j.jesf.2022.06.004

[^13]: Kreider RB, Kalman DS, Antonio J, et al. International Society of Sports Nutrition position stand: safety and efficacy of creatine supplementation in exercise, sport, and medicine. *J Int Soc Sports Nutr.* 2017;14(1):18. https://doi.org/10.1186/s12970-017-0173-z

[^14]: Forbes SC, Candow DG, Neto JHF, et al. Creatine supplementation and endurance performance: surges and sprints to win the race. *J Int Soc Sports Nutr.* 2023;20(1):2204071. https://doi.org/10.1080/15502783.2023.2204071

[^15]: Grgic J, Pedisic Z, Saunders B, et al. International Society of Sports Nutrition position stand: sodium bicarbonate and exercise performance. *J Int Soc Sports Nutr.* 2021;18(1):61. https://doi.org/10.1186/s12970-021-00458-w

[^16]: Trexler ET, Smith-Ryan AE, Stout JR, et al. International Society of Sports Nutrition position stand: beta-alanine. *J Int Soc Sports Nutr.* 2015;12(1):30. https://doi.org/10.1186/s12970-015-0090-y

[^17]: Brooks E, Lamothe G, Nagpal TS, Imbeault P, et al. Acute ingestion of ketone monoesters and precursors do not enhance endurance exercise performance: a systematic review and meta-analysis. *Int J Sport Nutr Exerc Metab.* 2022;32(3):214–225. https://doi.org/10.1123/ijsnem.2021-0280

[^18]: Hill JA, Keane KM, Quinlan R, Howatson G. Tart cherry supplementation and recovery from strenuous exercise: a systematic review and meta-analysis. *Int J Sport Nutr Exerc Metab.* 2021;31(2):154–167. https://doi.org/10.1123/ijsnem.2020-0145

[^19]: Daab W, Bouzid MA, Nassis GP, Arumugam A, et al. Effects of tart cherry juice supplementation on recovery from exercise-induced muscle damage in athletes: a systematic review and meta-analysis. *Sports Med Open.* 2026;12(1). https://doi.org/10.1186/s40798-026-00993-3

[^20]: McHugh MP. "Precovery" versus recovery: understanding the role of cherry juice in exercise recovery. *Scand J Med Sci Sports.* 2022;32(6):940–950. https://doi.org/10.1111/sms.14141

[^21]: Chung J, Choi M, Lee K. Effects of short-term intake of Montmorency tart cherry juice on sleep quality after intermittent exercise in elite female field hockey players: a randomized controlled trial. *Int J Environ Res Public Health.* 2022;19(16):10272. https://doi.org/10.3390/ijerph191610272

[^22]: Flockhart M, Nilsson L, Tillqvist E, Vinge F, et al. Glucosinolate-rich broccoli sprouts protect against oxidative stress and improve adaptations to intense exercise training. *Redox Biol.* 2023;67:102873. https://doi.org/10.1016/j.redox.2023.102873

[^23]: Cesanelli L, Venckunas T, Minderis P, Maconyte V, et al. Effects of short-term broccoli powder supplementation on acute oxidative stress and recovery following a metabolically demanding exercise session. *Antioxidants.* 2026;15(3):379. https://doi.org/10.3390/antiox15030379

[^24]: Paulsen G, Cumming KT, Holden G, et al. Vitamin C and E supplementation hampers cellular adaptation to endurance training in humans: a double-blind, randomised, controlled trial. *J Physiol.* 2014;592(8):1887–1901. https://doi.org/10.1113/jphysiol.2013.267419

[^25]: Merry TL, Ristow M. Do antioxidant supplements interfere with skeletal muscle adaptation to exercise training? *J Physiol.* 2016;594(18):5135–5147. https://doi.org/10.1113/JP270654

[^26]: Jäger R, Kerksick CM, Campbell BI, et al. International Society of Sports Nutrition position stand: protein and exercise. *J Int Soc Sports Nutr.* 2017;14(1):20. https://doi.org/10.1186/s12970-017-0177-8

[^27]: Kato H, Suzuki K, Bannai M, Moore DR. Protein requirements are elevated in endurance athletes after exercise as determined by the indicator amino acid oxidation method. *PLoS One.* 2016;11(6):e0157406. https://doi.org/10.1371/journal.pone.0157406

[^28]: Witard OC, Hearris M, Morgan PT. Protein nutrition for endurance athletes: a metabolic focus on promoting recovery and training adaptation. *Sports Med.* 2025;55(6):1361–1376. https://doi.org/10.1007/s40279-025-02203-8

[^29]: Craven J, Desbrow B, Sabapathy S, Bellinger P, et al. The effect of consuming carbohydrate with and without protein on the rate of muscle glycogen re-synthesis during short-term post-exercise recovery: a systematic review and meta-analysis. *Sports Med Open.* 2021;7(1):9. https://doi.org/10.1186/s40798-020-00297-0

[^30]: Naderi A, Rothschild JA, Santos HO, Hamidvand A, et al. Nutritional strategies to improve post-exercise recovery and subsequent exercise performance: a narrative review. *Sports Med.* 2025;55(7):1559–1577. https://doi.org/10.1007/s40279-025-02213-6

[^31]: Hew-Butler T, Rosner MH, Fowkes-Godek S, et al. Statement of the Third International Exercise-Associated Hyponatremia Consensus Development Conference, Carlsbad, California, 2015. *Clin J Sport Med.* 2015;25(4):303–320. https://doi.org/10.1097/JSM.0000000000000221

[^32]: Parr EB, Camera DM, Areta JL, Burke LM, et al. Alcohol ingestion impairs maximal post-exercise rates of myofibrillar protein synthesis following a single bout of concurrent training. *PLoS One.* 2014;9(2):e88384. https://doi.org/10.1371/journal.pone.0088384

[^33]: Pengelly M, Pumpa K, Pyne DB, Etxebarria N. Iron deficiency, supplementation, and sports performance in female athletes: a systematic review. *J Sport Health Sci.* 2025;14:101009. https://doi.org/10.1016/j.jshs.2024.101009

[^34]: Yoon S, Kwon O, Kim J. Vitamin D in athletes: focus on physical performance and musculoskeletal injuries. *Phys Act Nutr.* 2021;25(2):20–25. https://doi.org/10.20463/pan.2021.0011

[^35]: Shaw G, Lee-Barthel A, Ross ML, Wang B, Baar K. Vitamin C-enriched gelatin supplementation before intermittent activity augments collagen synthesis. *Am J Clin Nutr.* 2017;105(1):136–143. https://doi.org/10.3945/ajcn.116.138594

[^36]: Australian Institute of Sport. AIS Sports Supplement Framework — ABCD Classification System. Australian Sports Commission. https://www.ausport.gov.au/ais/nutrition/supplements
