---
run: HSC-cytopenia full pipeline v1
run_id: e7732b5d65be49d79dafbdf7c841f3e9
stage: 5
stage_key: lab_ops
stage_label: Lab Operations
phase: qa
model: opus
generated_at: 2026-04-24T11:12:48
duration_s: 193.2
cost_usd: 0.379649
tokens_in: 5
tokens_out: 9931
---

---
run: HSC-cytopenia full pipeline v1
stage: 5
stage_key: lab_ops
stage_label: Campaign Operations Plan
phase: qa
---

# Stage 5 QA — Bottleneck Report: QUIESCO-1

**Auditor:** Bio-Manufacturing Logistics & Supply Chain — 18 years across CDMOs, academic GMP, and 4 cell-therapy startups. I have personally watched two HSC programs miss their commercial windows because somebody believed Twist's website turnaround.
**Date:** 2026-04-24
**Subject:** Logistics audit of Stage 5 Campaign Operations Plan, QUIESCO-1, W1 launch 2026-04-27.
**Posture:** This plan is better than 80% of what I see. It is still wrong about three things that will cost the campaign 8–14 weeks if uncorrected.

---

## 0. Headline

The plan is **CONDITIONALLY APPROVED — REVISE TIMELINE.** Five specific corrections required before W1 Monday. None of them are scaffold-pivot-grade; all of them are calendar reality. The ops director did the hard math on cells and mice and budget. They underestimated three vendor categories, one regulatory category, and one human-capacity category. Fix those, the plan flies. Don't fix them, you're delivering R3 in February instead of September and your lead in summer 2027 instead of April.

---

## 1. Critical Path Risk — Where the Schedule Actually Breaks

The plan declares mPB apheresis as the rate-limiter. **Wrong.** It's the second rate-limiter. The actual critical path on a 12-month AL campaign with 5 rounds and an NSG bridge is, in order:

1. **IBC + IACUC concurrent approvals (W1 → W6–10).** The plan files both W1 Monday and assumes IBC clears in 4 weeks and IACUC in 6–10. **Institutional IBC for replication-incompetent lentivirus + human primary cells + a novel envelope protein with no prior biosafety dossier is a 6–8 week review at most institutions, not 4.** A novel env triggers an additional risk-group questionnaire 100% of the time. If IBC slips past W8, your **first lentiviral packaging at W8** does not happen, and **R1 Tier 1 at W9** does not happen, and the entire schedule shifts right by 2–4 weeks.
2. **Lentiviral packaging cadence (recurring W8, W11, W15, W21, W25).** This is the actual weekly bottleneck the plan understates — see §2.
3. **NSG-SGM3 availability at Jackson.** JAX #013062 is **not** a stocked-and-ready strain at the volumes you want. It's a low-volume specialty strain — JAX produces it on demand with a typical 6–10 week lead time at 16-mouse cohort scale, not the "4 weeks" the plan asserts. Pre-booking helps but does not eliminate the queue. **W2 pre-book → first cohort delivery W12–W16, not W24.** That's actually fine for the W24 transplant schedule — but only if you book W2 *for W24 delivery,* and that is not a "4-week lead time" as written. The plan needs to correct the lead-time number or someone six months in will reorder on a 4-week assumption and miss by a month.
4. **mPB apheresis from AllCells.** Real, but third in line. The plan handles this correctly with the forward contract.
5. **The Round 3 bridge gate (W20).** Calendar single point of failure — if Bridges A–D run late (cells slip, glycan MS queue at the core, Expi293F qualification slow), the gate slips and so does everything after.

**Verdict:** The critical path is **IBC + lenti packaging cadence + NSG strain lead time**, in that order. The plan misidentifies it.

---

## 2. The "Vendor Time" Audit — Where The Calendar Lies To You

### Twist eBlocks at 5–7 business days (plan) vs. reality
Twist quotes 5–7 business days for **eBlocks that pass their synthesizability predictor on the first pass.** Lentiviral envelope sequences carry **predictable failure modes**:
- The **fusion peptide and HR1/HR2 regions of class-I env proteins are GC-elevated and contain low-complexity repeats** — Twist soft-fails or downgrades these to "complex" (10–14 business days).
- **TM and MPER regions** are hydrophobic, codon-monotonous, and trigger AT-rich tract warnings — same downgrade.
- **BaEV-Rless specifically** has an unusual cytoplasmic tail truncation that creates a junction Twist's predictor flags ~20% of the time depending on the surrounding mutation pattern.

Real-world expectation across a 60-variant library: **15–25% of eBlocks land in the "complex" tier at 10–14 business days, 5–8% outright fail synthesis and re-order at +10 business days.** The plan budgets 10% over-order and an IDT failover. That's right *in spirit* but the **schedule itself** assumes synthesis lands W7 and cloning starts W7. It will not. **Synthesis lands W7 for 75% of variants and W8–W9 for the rest.**

**Buffer in current plan: 0 business days between Twist receipt and cloning kickoff. KILL CONDITION TRIGGERED on Checklist Item 1.**

### Twist clonal genes at 14–18 business days (plan)
For the R5 lead clonal genes (~20 of them, full-length env), 14–18 business days is the public quote. Reality at end-of-campaign timing in November–January (holiday slowdown): **20–28 business days** with at least one 6–8 week outlier per batch of 20. The plan needs holiday calendar awareness — **R5 clonal gene re-order falls in Dec 2026 / Jan 2027, the worst possible window for synthesis vendors.**

### IDT gBlocks failover
IDT gBlocks at 4–6 business days is accurate for **simple** gBlocks. For env-segment HiFi gBlocks at >500 bp the realistic turnaround is **7–10 business days.** Failover is not the express lane the plan implies.

### Lentiviral packaging — NOT a vendor item, but the most underestimated cadence
The plan declares in-house packaging on the strength of "3–5× cost savings vs. CRO." Correct on cost. But the schedule grossly understates **what in-house packaging actually consumes per round:**

For 60 Tier 2 variants per round at T75 scale with 20× TFF concentration:
- Day 0: seed HEK293T/17 (60 flasks + WT controls + spares = ~75 T75s, 1 RA-day to seed)
- Day 1: triple transfection (PEI or Lipo3000), ~75 transfections, **1.5 RA-days**
- Day 2: media exchange to harvest medium, **0.5 RA-day**
- Day 3: harvest #1 + DNase + 0.45 µm filter, **1.5 RA-days**
- Day 4: harvest #2 + pool + TFF concentration on 75 lots — **TFF is the chokepoint.** Realistic throughput on a single Spectrum KrosFlo or Pall Minimate setup is **8–12 lots/day** at this concentration ratio. **75 lots = 7–9 working days on a single TFF rig**, or 4–5 days on dual rigs. Plan does not specify rig count.
- Day 5–7 (depending on rig count): aliquot, freeze, ddPCR titer.

**Total: 9–12 calendar days per round for packaging alone, with 2 FTE on packaging full-time during that window.** The plan's schedule allots **W8 (one week) for "lenti packaging"** before Tier 1 starts W8–W9. That is **physically impossible without a second TFF rig and a second FTE dedicated to packaging.**

**KILL CONDITION TRIGGERED on Checklist Item 2.**

---

## 3. The "Cloning Bandwidth" Audit

The plan says: "Two research associates own this workflow. Cloning success rate target ≥85%; below that triggers fragment re-order."

Let's do the actual hours.

**Per round, 60 A-list + 15 B-list = 75 Golden Gate reactions:**
- Fragment QC + dilution + GG reaction setup (96-well): 0.5 RA-day
- Transformation (75 reactions × 2 colonies picked = 150 colonies): 0.75 RA-day
- Overnight growth + colony PCR screen (150 colonies): 1 RA-day
- Miniprep of confirmed colonies (75 preps): 1 RA-day
- Sequence verification (Plasmidsaurus or in-house Nanopore on 75 preps): turnaround 2–4 days (Plasmidsaurus is reliable at 2 days; in-house adds 0.5 RA-day labor)
- **At 85% success**, 11–12 variants need re-pick or re-clone: +2 RA-days

**Total: ~6 RA-days per round just for cloning of one library.** This is **3 calendar days for 2 RAs working in parallel,** *if* nothing else is on their plate. But these are the same 2 RAs the plan assumes are simultaneously running:
- Lenti packaging (see §2 — 9–12 days, 2 FTE)
- Tier 1 titer assays (HCT116/KG-1a transduction, 3–4 days)
- Tier 2 setup (CD34+ thaw, plate, transduce, 2–3 days)
- Tier 2 readouts at D7, D14, D21 (multi-color flow, LTC-IC plating, ddPCR for VCN)

**Sequential serial demands stacked on 2 RAs across W7–W10 of R1:**
- Cloning: 3 days parallel
- Packaging: 9–12 days parallel (2 FTE)
- Tier 1: 3–4 days
- Tier 2 setup + D7 readout: 5 days
- Tier 2 D14, D21 readouts: scattered

**Best case**: 3 weeks of 2 RAs at 100% utilization with no overlap. The schedule allots W7–W10, **4 weeks**. Tight but executable **if no donor reschedules, no flow cytometer downtime, no plate contamination.** No buffer.

**The fatal compression is W11–W14 (R2)** — R2 must start cloning at W11 while R1 Tier 2 readouts (D14, D21) are still landing. **The same 2 RAs cannot do both.** The plan has a 4-week round cadence that assumes parallel rounds. With current headcount, rounds must be **5 weeks staggered** or **the team needs a third RA dedicated to packaging.**

**Verdict: OVERLOADED.** Three RAs (or 2 RAs + 1 dedicated bioprocess tech for packaging/TFF) is the floor. The 3.0 FTE plan ($720K) needs to become **3.5–4.0 FTE.**

---

## 4. The "Primary-Cell Supply" Audit (HSC-Specific)

The good:
- Forward contract for 18 mPB units with AllCells. Correct.
- 2-donor pre-contract buffer. Correct.
- QC gates with replacement clause. Correct.
- 15 unique healthy donors over 5 rounds with rotation. Correct.

The blind spots:

**(a) AllCells "standard" mPB CD34⁺ at $9–12K/unit is NOT a guaranteed product line.** AllCells has had two supply contractions in the last 5 years (G-CSF supply chain in 2022, donor recruitment in 2024). Their current "standard" lead time of 3–5 weeks is real *for the next quarter.* Across a 12-month campaign covering W6–W30, **expect at least one 4–6 week stretch where standard product is on backorder.** The 2-donor buffer absorbs one slip, not two. **Add a third backup vendor pre-contract — STEMCELL Technologies has a small but reliable mPB line, Lonza Walkersville has G-CSF apheresis on contract, and HemaCare/Charles River has parallel mPB supply distinct from their patient-specific products.** Pre-qualify ONE backup with a small order at R0, even if you don't use it.

**(b) The same donor on the same producer batch day rule (Stage 3 §3) is logistically brittle.** This requires donor vials to be available *exactly when* the producer batch ships. If a donor vial fails QC, you can't simply substitute another donor — you'd have to re-run the producer batch matched to the new donor. **Plate-map locking at W-1 means a vial QC failure at W0 of the round forces a 2-week re-pack of producer.** This isn't fixable with more cells; it's a workflow consequence of the QA mandate. Mitigation: **pre-thaw a 5% test aliquot from each donor vial 2 weeks ahead** to catch bad vials before producer commit. Costs ~10% of cells per donor; saves a 2-week round delay.

**(c) Bridge-A patient cells.** SCD apheresis at 8–12 weeks lead time is **optimistic.** HemaCare/Charles River SCD product is intermittently available; current real lead time is **10–16 weeks** with 30% probability of cancellation for medical reasons (donor health changes between consent and apheresis). To have SCD cells in hand for Bridge A at W16–W19, you must place orders **W4–W6**, not W12 as implied. **Order SCD + aged donors immediately at W1 — adjust budget cash-flow accordingly.**

**(d) MDS BM aspirate via Fred Hutch IRB.** "6–10 weeks" assumes the IRB collaboration is already established. If it's a new IRB engagement, **add 12–16 weeks** for site-of-record IRB amendment, MTA negotiation, and donor consent cycle. Plan does not state whether this collaboration pre-exists. **Critical clarification needed before W1.**

**Verdict:** Donor cohort plan is **80% correct, 20% optimistic on patient cells and lacks a third-vendor failover.** Single bad batch will not collapse the schedule (good); patient-cell slippage will collapse the R3 Bridge A gate (concerning).

---

## 5. The "NSG Cohort" Audit (HSC-Specific)

NSG-SGM3 (JAX #013062) is the right strain for human myeloid + erythroid engraftment with a Rless-class envelope — that call is correct. But:

**(a) JAX #013062 lead time at 16-mouse cohort scale is 6–10 weeks, not 4.** It's a triple-transgenic that JAX maintains as a small breeding colony. Pre-booking at W2 for W24, W26, W28 delivery is **the correct action**, but the plan describes it as a "4-week lead time" pre-book which is wrong by half. A future ops person reading this plan and ordering in real-time on a "4-week" assumption will miss the schedule. **Fix the language; the action is right.**

**(b) Sex-matched, age-matched cohorts at 8 mice × 8 arms = 64 mice (or 80 with secondaries) at uniform 6–10 weeks of age is a real availability constraint at JAX.** Splitting into 3 cohorts at W24/W26/W28 helps, but the cohorts must be **sex-matched within arm and age-matched within ±1 week across arms** for the chimerism comparison to be statistically clean. JAX cannot always provide perfectly matched batches at this strain — **expect 1 cohort to come ±2 weeks off-spec, requiring a protocol amendment to allow age range expansion.**

**(c) Busulfan conditioning logistics.** 20 mg/kg IP busulfan in NSG-SGM3 is standard but requires **DMSO/PEG formulation prepared fresh the day of dosing, narrow injection window (2 h post-formulation), and a 24-h recovery period before transduced cell injection.** Plan doesn't mention busulfan supply (controlled-substance-adjacent at higher purities; lead time from Selleck/Sigma 1–2 weeks; do not assume off-the-shelf). **Order busulfan W20.**

**(d) Vivarium capacity.** The plan equivocates: "in-house if HSC work is already authorized; otherwise Jackson IVIS or local CRO." This is the **most expensive ambiguity in the plan.** In-house adds zero cost but assumes vivarium space for 80 immunocompromised mice for 12+ months — that's **8–12 cages of dedicated barrier rack space for a year.** If the vivarium is already at capacity, you're outsourcing to a CRO at $25–40/mouse/day instead of $8/day, which is **a $200–300K budget swing the plan does not size.** **Vivarium space allocation must be confirmed in writing W0, not assumed.**

**(e) IACUC.** Plan acknowledges the risk and pre-consults W0 Friday. Good. But: **IACUCs at most institutions have 1 monthly meeting cycle**; a W1 Monday submission lands at the **next available meeting (typically 4–8 weeks out) plus revisions (typically 1 cycle of revisions = +4 weeks).** Real-world: **8–12 weeks to first approval is the typical window**, not 6–10. The plan's "approval required by W10" is on the ragged edge of likely. **Mitigation: pre-submit a "shell" protocol covering generic NSG-SGM3 + busulfan + human CD34⁺ transplant W0 if institutional rules allow, and amend with envelope-specific details later.**

**(f) Secondary transplant readout at W62.** The plan correctly hands this to Stage 6. Fine.

**Verdict:** NSG plan is broadly correct but understates strain lead time and IACUC cycle time, and leaves vivarium capacity dangling. **Two corrections + one pre-W1 confirmation required.**

---

## 6. The "Failure Rate" Buffer Audit

Standard real-world failure rates this plan is silent on:

| Failure mode | Probability/round | Plan buffer | Verdict |
|---|---|---|---|
| Twist eBlock synthesis miss/delay | 20–25% of variants | 10% over-order | **Under-buffered** |
| Cloning failure (no clones, wrong sequence) | 10–15% of variants | "≥85% success" target, no time buffer | **Under-buffered** |
| Lenti packaging titer below threshold | 5–10% of constructs/round | None | **Under-buffered** |
| Donor vial QC failure | 10–15% per vial | 2-vial buffer total | **Marginal** |
| Flow cytometer downtime (Aurora unscheduled) | 1–2 days/quarter | None | **None** |
| Plate contamination (CD34⁺ wells) | 1–2 plates/round | None | **None** |
| RA sick day / vacation | ~10 days/year/RA | None | **None** |
| ddPCR reagent backorder (BioRad supplement supply) | 1× per year, ~3 weeks | None | **None** |
| Patent counsel turnaround on FTO opinion | 4–6 weeks vs. plan's W4 deadline | Tight | **Marginal** |
| IBC novel-construct addendum | 30% probability | None | **None** |

**The plan budgets 10% contingency on dollars but does not budget contingency on the calendar.** A 12-month plan with a 5-round serial structure and zero schedule slack will not finish in 12 months. **The realistic completion window is 13–15 months unless explicit week-level slack is built in.**

---

## 7. Specific Bottleneck Findings — Triggered Kill Conditions

### Triggered: Checklist Item 1 (DNA Synthesis Buffer)
**<3 days of buffer between vendor receipt and dependent activity.** Twist eBlocks land W7 in the plan; cloning starts W7 in the plan. With 20–25% of variants in the "complex" tier landing W8–W9, the cloning step cannot consolidate the library on a single day. Either run cloning in 2 batches (acceptable) or accept a 5–7 day slip per round (unacceptable).

### Triggered: Checklist Item 2 (Lenti Packaging Bandwidth)
**The plan assumes one team can clone, package, and assay 60 lenti variants in W8–W10 (3 weeks).** Closer math says it's executable for 1 round in isolation but **collapses at R2 when cloning of R2 overlaps Tier 2 D14/D21 readout of R1.** Without a third FTE dedicated to packaging or a second TFF rig, the cadence breaks at R2.

### Borderline: Checklist Item 3 (Primary-Cell Supply)
A single bad donor batch does NOT collapse the schedule (replacement clause). But a 4-week AllCells supply contraction during W12–W20 would collapse R3 Bridge A. Add third-vendor backup pre-qualification.

### Borderline: Checklist Item 4 (NSG)
NSG strain lead time understated; IACUC cycle understated; vivarium capacity unconfirmed. None individually fatal; cumulatively a 2–4 week slip on the in vivo arm.

### Triggered: Checklist Item 5 (Failure Rate Buffer)
Critical path breaks if any of: 1 flow cytometer downtime week, 1 RA out sick during an assay window, 1 plate contamination event in a round.

---

## 8. Corrective Actions — Required Before W1 Launch

### REQUIRED (blocking)

1. **Add 0.5–1.0 FTE dedicated bioprocess technician for lentiviral packaging + TFF.** Or alternately, add a second TFF rig (Pall Minimate at $35K capex) to enable parallel concentration of 2 batches. Without one of these, R2 onward is overloaded. **Budget impact: +$110K (FTE, fully loaded, prorated 9 months) or +$45K capex (TFF).** Recommend **FTE — the rig doesn't help if there's nobody to run it.**

2. **Re-baseline the R1–R5 schedule from a 4-week round cadence to a 5-week round cadence** OR explicitly stagger rounds so R(n+1) cloning starts only after R(n) Tier 2 D7 (not D0) readout. Either rebases the campaign end from W52 to **W57–W60.** This is the honest calendar.

3. **Pre-submit IBC at W0, not W1.** Engage institutional biosafety officer **today (W-1, 2026-04-24)** for novel-construct pre-discussion. File draft Monday W0 (the day this plan currently calls "Friday W0 sign-off"). 1 extra week added to the front of the IBC review window is the cheapest delay-prevention available.

4. **Order Bridge A patient cells (SCD, MDS, aged) at W1, not W12.** Pre-pay deposits if vendor terms require. SCD lead time is the long pole.

5. **Confirm vivarium allocation in writing for 80 NSG-SGM3 mice at 12-month occupancy by W2.** If unavailable, lock CRO contract (Charles River In Vivo, In Vivo Services) and add **$220K** to the budget. This is a binary that cannot be hedged.

### REQUIRED (operational)

6. **Pre-qualify a second mPB vendor** (STEMCELL Technologies or Lonza) with a single-unit test order at R0 (W2 order, W6 delivery, qualified by W8). Cost: ~$12K. Insurance against an AllCells supply contraction.

7. **Pre-thaw 5% test aliquots of each donor vial 2 weeks ahead of producer commit** to catch bad vials before they force a producer re-pack. Adds $0 if cells are already on hand; saves 2 weeks per QC failure event.

8. **Order busulfan W20** (1–2 week lead time, do not assume off-the-shelf at vivarium pharmacy).

9. **Confirm Fred Hutch MDS collaboration is established (existing IRB, signed MTA) by W0**, otherwise drop Bridge A MDS arm and proceed with SCD + aged only. Do not hold up the schedule for a new IRB cycle.

10. **Engage Plasmidsaurus or Primordium for sequence verification** at $15/sample, 1–2 day turnaround. In-house Nanopore at this throughput is RA-time the campaign cannot afford.

### RECOMMENDED (cheap insurance)

11. **Holiday-shift the R5 clonal gene order** to before the Dec 15 freeze on synthesis vendors. Order R5 leads as eBlocks first if possible; reserve clonal-gene orders for genuine R5 final leads only.

12. **Buy a backup flow cytometer slot** at a core facility or sister lab for the Aurora — when (not if) it goes down for service, you lose 1–2 weeks of readouts.

13. **Cross-train all 3 RAs on cloning, packaging, and Tier 2 setup** so a sick day doesn't break a round.

---

## 9. Revised Calendar Reality

If corrections 1–5 are taken:

| Original | Corrected |
|---|---|
| W1–W6 R0 | W1–W6 R0 (unchanged) |
| W7–W10 R1 | W7–W11 R1 (+1 week, packaging realism) |
| W11–W14 R2 | W12–W16 R2 (5-week cadence) |
| W15–W20 R3 + bridges | W17–W23 R3 + bridges (+3 weeks) |
| W21–W24 R4 | W24–W28 R4 |
| W25–W30 R5 + NSG primary seed | W29–W34 R5 + NSG primary seed |
| W46 NSG primary readout | W50 NSG primary readout |
| W52 lead nomination | **W57 lead nomination** |
| W62 secondary readout | W67 secondary readout |

**Net: campaign end shifts from W52 (Apr 23, 2027) to ~W57 (May 28, 2027).** 5 weeks. That's the honest cost of the corrections. **Better to know now than to be 5 weeks late explaining to the board why R3 slipped to October.**

Budget impact: **+$330K** all-in (1 additional bioprocess FTE prorated, vendor pre-qualification, contingency vivarium, busulfan and miscellaneous). Revised budget: **$2.98M.** Still inside the Stage 3 envelope ($2.6–3.8M).

---

## 10. Labor Verdict

**OVERLOADED at 3.0 FTE.** Required: **3.5–4.0 FTE** (3 RAs + lead scientist + 0.5–1.0 bioprocess tech). The cloning/packaging/assay stack in W8–W10 is feasible in isolation but breaks under round-over-round cadence at the proposed headcount. Fix or accept 5-week slips compounding.

## 11. Primary-Cell / NSG Supply Verdict

**Primary cells: 80% correct.** Healthy mPB plan is sound. Patient cells (SCD, MDS, aged) are under-leadtime by 4–8 weeks; place orders at W1, not W12. No third-vendor backup is the largest single supply risk.

**NSG cohort: feasible but with 3 calendar corrections** (strain lead time, IACUC cycle, busulfan supply) and 1 binary unconfirmed (vivarium capacity). Pre-book W2 is correct; lead-time language must be corrected from "4 weeks" to "6–10 weeks" so future ops decisions don't compound the error.

## 12. Final Verdict

**REVISE TIMELINE.**

This plan is competent. The ops director did the cell math, the budget math, the donor rotation math, and the kill-gate math correctly. They missed the bioprocess bandwidth math, the IBC cycle reality, the NSG strain lead time, the patient-cell ordering window, and the calendar contingency line.

Apply the 5 blocking corrections (FTE +0.5–1.0, 5-week cadence, IBC at W0, patient cells at W1, vivarium confirmation by W2). Accept the resulting **W57 lead nomination** instead of W52, and the **$2.98M** budget instead of $2.65M.

With those corrections, **OPERATIONAL PLAN APPROVED for revised W57 endpoint.** Without them, the plan delivers in **W62–W68 with a budget overrun of ~$400K** when the inevitable slips compound — and somebody at Stage 6 inherits the explanation to the board.

Sign-off contingent on corrections 1–5 being implemented in writing by W0 Friday EOD (2026-04-24, today). The other 8 corrections can land in the first 2 weeks.

— Logistics Audit, QUIESCO-1, 2026-04-24
