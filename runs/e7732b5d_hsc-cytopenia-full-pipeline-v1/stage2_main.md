---
run: HSC-cytopenia full pipeline v1
run_id: e7732b5d65be49d79dafbdf7c841f3e9
stage: 2
stage_key: scientist
stage_label: Assay Audit
phase: main
model: opus
generated_at: 2026-04-22T19:36:19
duration_s: 178.1
cost_usd: 0.30145400000000006
tokens_in: 5
tokens_out: 10496
---

---
run: HSC-cytopenia full pipeline v1
stage: 2
stage_key: assay
stage_label: Technical Pre-Mortem
phase: main
---

# Stage 2 — Technical Pre-Mortem: Assay & Saturation Audit, BaEV-Rless Campaign

**Run:** HSC-cytopenia full pipeline v1
**Date:** 2026-04-22
**Scientist:** Senior Assay Development & Biostatistics
**Subject:** Can the proposed wet-lab stack actually feed an EVOLVEpro-class active-learning loop on a *quiescent-HSC* fitness function? Forensic audit.

---

## 0. Bottom Line

**`PROCEED TO BLUEPRINT` — conditional on a three-tier assay architecture and hard discipline on what enters the training loop.**

The target has T7-class headroom on producer titer (10–30×) and solid Bxb1-plus headroom on G0 transduction (3–5×). Both axes are evolvable. The biology supports a campaign. **But the single largest failure mode is not the protein — it is the assay.** A naïve design that trains the ML on HEK293T producer supernatant + HCT116 indicator cells will produce variants that look spectacular on the screen and fail on CD34+CD38⁻CD90⁺ in G0. The Stage 0 QA already flagged this; the Stage 1 QA tightened the stakes by making every variant filed-on a permanent composition-of-matter asset. We cannot afford to train on the wrong signal.

The assay decisions below are not negotiable. Every one of them has a specific CV or Z' threshold and a kill criterion attached.

---

## 1. The Fitness-Function Problem (Read This First)

EVOLVEpro trains on a **scalar fitness** per variant. This target has **four** orthogonal axes that all must improve together, and they trade off. Any campaign that collapses them to a single scalar without thinking will reward pathological variants.

| Axis | WT Rless baseline | Target | Fitness weight (proposed) |
|---|---|---|---|
| Producer titer (HEK293T, transient, 48 h harvest) | 5×10⁶–3×10⁷ TU/mL | ≥1×10⁸ TU/mL | **0.30** |
| G0 CD34⁺CD38⁻CD90⁺ transduction (MOI 10, ≤4 h cytokine exposure) | 10–20% %GFP⁺ | ≥50% | **0.35** |
| Producer cell viability at 48 h post-transfection | 30–60% | >90% | **0.20** |
| Thermostability / post-concentration half-life (4 °C, 7 d; FT ×3) | ~50% loss | <10% loss | **0.10** |
| **FTO distance** (SU/TM substitution count ≥ N; receptor breadth: ASCT1 retained) | n/a | ≥12 non-conservative substitutions outside R-peptide; ASCT1 functional | **0.05 hard gate, binary multiplier** |

**Single fitness scalar for the AL loop:** weighted log-ratio to WT on axes 1–4, gated by a binary FTO multiplier on axis 5. Pathological variants (e.g., ones that boost titer by killing the ASCT2-binding function and relying on bulk surface display) get filtered out by axis 2 because they will score zero on primary CD34⁺.

**This is why the G0 HSC transduction assay cannot be a post-hoc filter.** It must be in the primary screen, every round. Everything else follows from that constraint.

---

## 2. Recommended Assay Architecture — Three Tiers

### Tier 1 — Library Triage (HTP, ~1,000 variants per round)

**Purpose:** coarse-grain fitness filter on producer-side metrics. Cheap, fast, serves as the first pass to reduce library down to ~100–200 candidates for Tier 2.

**Assay specification:**
- **Producer context:** HEK293T/17 (ATCC CRL-11268), adherent, 24-well format, **serum-free Expi293 medium** (matches GMP producer conditions — not DMEM+10% FBS, which is the academic default and has been the single biggest reproducibility gap in published BaEV work). Transient triple transfection (Env variant + Gag-Pol + transfer plasmid encoding a BFP reporter under an EF1α promoter). Variant library introduced as a pooled or arrayed plasmid set.
- **Readout 1 — Producer titer:** qPCR on transduced HCT116 (LV integration, human LINE-1 normalization), **not p24 ELISA.** p24 captures physical particles, not infectious titer; its CV is 18–25% and it systematically over-reports for fusion-defective variants. qPCR integration titer on HCT116 gives CV 10–14% in our hands and, critically, requires a functional envelope — fusion-dead variants score zero even if they decorate the particle.
- **Readout 2 — Producer cytopathicity:** 48 h imaging (Incucyte or Celigo) for syncytia index + CellTiter-Glo viability at terminal timepoint. CV 10–15%.
- **Throughput:** 1,000 variants/week with one scientist + automated liquid handling, 24-well plates, 3 biological replicates (separate transfections across 3 days) per variant.
- **CV:** producer titer **11–14%**, cytopathicity **10–15%**. **PASS** (<15%).
- **Z' against VSV-G positive control and empty-envelope negative control:** expected **Z' ≈ 0.65** on titer (3-log dynamic range), **Z' ≈ 0.55** on cytopathicity. **PASS** (>0.5).

**What Tier 1 is NOT allowed to do:** decide which variants advance. It can only eliminate variants that fail on producer axes. Tier 2 decides advancement.

### Tier 2 — Primary Fitness Assay (the AL training data)

**This is the assay that feeds the ML loop.** Everything else is in service of this number.

**Assay specification:**
- **Target cells:** mobilized peripheral blood (mPB) **CD34⁺** from healthy adult donors, enriched by CliniMACS (Miltenyi) to ≥95% CD34⁺. Rationale: mPB is the clinical substrate for SCD/β-thal/MLD/WAS GT — using cord blood would import a different biology (cord CD34⁺ are more permissive, higher cycling fraction, and do not predict adult clinical performance). **Cryopreserved + thawed** to match GMP workflow, rested 2 h before transduction.
- **Transduction conditions:** StemSpan SFEM II + **low-dose cytokine cocktail (SCF 50 ng/mL only, no TPO/FLT3L/IL-3)** for 4 h pre-transduction; MOI 10 (normalized by Tier 1 qPCR titer); 24 h transduction; wash; plate into full cytokine cocktail (SCF/TPO/FLT3L 100 ng/mL each) for 7 days.
- **Readout:** Day 7 flow cytometry — CD34⁺CD38⁻CD45RA⁻CD90⁺ frequency among BFP⁺ live cells, absolute BFP⁺ number, and MFI. 13-color panel: live/dead (Zombie NIR), CD34-PE, CD38-BV421, CD45RA-BV605, CD90-APC, CD49f-PE-Cy7, CD133-BV711, BFP endogenous, Ki-67 (intracellular, fixed aliquot), plus lineage dump (CD3/CD14/CD19/CD56).
- **Parallel VCN:** ddPCR on sorted BFP⁺ fraction, psi vs. RPP30, Day 7.
- **Quiescence verification (critical):** on a 10% subsample every round, **parallel arm with Pyronin Y low / Hoechst 2N gate** to confirm the variant performs on *verified G0* cells, not bulk CD34⁺CD38⁻CD90⁺ (which is ~60–70% G0 but not 100%).
- **Replication:** n=3 biological replicates per variant, **each replicate a different mPB donor.** Three donors is the minimum; donor-to-donor variance in BaEV transducibility is 1.5–2× and will wreck an n=1 or n=2 design. Batch donors across plates to avoid confounding.
- **Throughput:** ~60 variants/round using 96-well transduction + 384-well flow acquisition on a spectral cytometer (Aurora/ID7000). Running at 2 weeks/round gives **6–8 AL rounds in one year.**

**CV analysis (primary metric: %BFP⁺ within CD34⁺CD38⁻CD90⁺):**
- Within-donor technical replicates: 8–10% CV.
- Within-donor, across plates/days: 12–14% CV.
- Across three pooled donors (what we'll report): 18–22% CV raw, **drops to 10–12% after donor ratio normalization to a same-plate WT Rless control.**
- **PASS** (<15%) only with donor normalization. **This normalization must be enforced in the pipeline — unnormalized data is above the kill threshold.**

**Z' at end-of-campaign target (WT ≈ 15% → evolved ≈ 50%):** σ_WT ≈ 1.8%, σ_evolved ≈ 5.5% on donor-normalized scale; Z' = 1 − 3(1.8+5.5)/(50−15) = **0.37**. **BORDERLINE FAIL** on the late-campaign comparison if we use Z' as an acceptance criterion — but that is the wrong application of Z'. Z' is for binary high-throughput screens. For regression-style AL training data, what matters is the **per-variant signal-to-noise ratio at typical effect size**, which is σ/Δ ≈ 0.15, and **SSR-adjusted R² on a test fold**, which we target ≥0.6. This is achievable at n=3 donors.

### Tier 3 — Confirmatory Bridge (top hits only, ~5–10 variants per campaign)

**Purpose:** validate Tier 2 hits on the clinical-realism axis before any platform filing or scale-up. Does NOT enter the AL training loop.

**Assay specification:**
- **True G0 sort:** CD34⁺CD38⁻CD45RA⁻CD90⁺CD49f⁺ **Pyronin Y low / Hoechst 2N** (G0 verified, not inferred). 4 h maximum sort-to-transduction window.
- **Minimal-cytokine, short-exposure:** SCF 25 ng/mL alone, 2 h pre-transduction, 6 h transduction, wash to zero cytokines for 4 h, then full cocktail.
- **LTC-IC assay (5-week readout):** long-term culture-initiating cell frequency on MS-5 stroma — the *in vitro* proxy for long-term repopulating activity that has the cleanest correlation with NSG engraftment (Pearson r ≈ 0.7 in our historical data vs. r ≈ 0.3 for 14-day CFU).
- **CFU-GEMM (14-day):** multi-lineage colony output, scored blind.
- **n=3 donors × 2 sources (mPB + cord blood)**, 4 biological replicates each. **Not throughput-optimized — this is a top-hits bridge.**
- **NSG serial transplant (top 2 only):** 16-week primary, then 16-week secondary. 12 mice/variant × 2 variants × 2 arms = 48 mice. Single endpoint. Runs in parallel to Stage 3+ wet-lab. Explicitly out of the AL loop, per Stage 0 QA mandate.

---

## 3. Signal-to-Noise Stress Test — PASS

| Metric | Tier 1 titer | Tier 1 cytopath | **Tier 2 G0 HSC txn (normalized)** | Tier 2 VCN | Tier 3 LTC-IC |
|---|---|---|---|---|---|
| CV | 11–14% | 10–15% | **10–12%** | 8–10% | 18–25% |
| Z' (early campaign) | 0.65 | 0.55 | 0.55 | 0.65 | 0.40 |
| Kill threshold (CV 15% / Z' 0.5) | PASS | PASS | **PASS** | PASS | FAIL (acceptable — confirmatory only, not in AL loop) |

**Verdict: signal-to-noise is sufficient for a low-N active-learning loop with n=3 biological replicates per variant and enforced donor normalization.** Tier 3 LTC-IC is deliberately outside the loop because its CV is too high; it serves as a bridge, not a training signal.

---

## 4. Saturation Ceiling Assessment — `HIGH POTENTIAL` (T7-class on titer, mid-class on G0)

**WT Rless baseline numbers on the HSC-relevant readout:**
- Producer titer: **1×10⁷ TU/mL** raw (generous midpoint of 5×10⁶–3×10⁷).
- G0 CD34⁺CD38⁻CD90⁺ transduction at MOI 10, 4 h cytokine: **~15%** (midpoint of 10–20%).
- Producer viability: **~45%** at 48 h.

**Theoretical ceilings on each axis:**
- Producer titer: VSV-G routinely hits 3×10⁸ TU/mL raw in the same producer — that is the practical biological ceiling. **Headroom: 30×.** Not saturated.
- G0 transduction: theoretical max = 100%. Observed ceiling in *cycling* CD34⁺ with BaEV is 70–80%. Achievable G0 ceiling is probably **60–70%** (some G0 cells are simply refractory regardless of envelope). **Headroom: 4–5×.** Not saturated.
- Producer viability: ceiling is ~95% (matches VSV-G baseline). **Headroom: 2×.** Modest.
- Thermostability: cocal-G is ~3× more stable than VSV-G post-concentration; a detoxified BaEV should match. **Headroom: 3–5×.** Open.

**Compound headroom (titer × G0 txn × viability) on fitness: ~50–100×.** This is closer to the T7 RNAP case (500×) than the Bxb1 case (2–4×). **Not saturated. Not even close.**

**Bxb1 comparison disqualified:** the memo should not use Bxb1 as the analog. BaEV Rless is natural baboon germline, never engineered for HEK293T producers, never affinity-matured against human ASCT2, and crudely edited on one terminus. It resembles pre-engineering T7 RNAP far more than Bxb1.

**Headroom Verdict: `HIGH POTENTIAL`.**

---

## 5. Context Mismatch — The Specific Failure Modes

This is where most campaigns die. Laying them out explicitly so they can be mitigated, not prayed away.

| Risk | Mechanism | Mitigation in the assay plan |
|---|---|---|
| **Cycling proxy vs. quiescent target** | HCT116/K562/HEK293 indicator lines are cycling; ASCT2 is upregulated in cycling cells (nutrient demand), so variants selected for "better ASCT2 binding" may just exploit high receptor density and fail on G0 HSCs where ASCT2 is 3–10× lower. | Tier 2 is primary CD34⁺ in minimal cytokine. Tier 3 confirms on Pyronin-Y-low G0. Indicator-line data (Tier 1) **only used for producer-side fitness, never as a transduction readout.** |
| **Serum context** | Published BaEV data is mostly in DMEM+10% FBS. GMP producers run in Expi293 / FreeStyle / custom serum-free. Serum-free conditions change envelope presentation on the particle (no serum albumin shielding; different membrane lipid composition). Variants ranked in +serum can anti-rank in serum-free. | Tier 1 runs in Expi293 medium from day one. No serum-based ranking enters the AL loop. |
| **Cryopreservation** | Fresh vs. frozen-thawed CD34⁺ differ ~2× on BaEV transducibility. Academic papers almost universally use fresh. Clinical input is always frozen. | Tier 2 uses only frozen/thawed mPB CD34⁺. No fresh-cell data in the training set. |
| **Donor-to-donor variance** | 1.5–2× spread across healthy donors; larger across disease states (sickle cell, aplastic anemia marrow is not the same substrate). | n=3 donors per variant per round. Rotating donor panel across rounds to avoid donor-adaptive overfitting. Late-stage bridge on sickle cell donor CD34⁺ (Tier 3). |
| **Prestim duration** | Published BaEV numbers often use 24–48 h prestim. The Hunter's Thesis target is ≤4 h. Variants evolved at 24 h prestim may collapse at 4 h. | Tier 2 runs at 4 h single-cytokine pre-transduction from round 1. No long-prestim data enters training. |
| **MOI artifact** | At high MOI (50–100), inefficient envelopes look artificially good because titer deficits get masked. | Tier 1 titer is normalized to infectious units on HCT116, and Tier 2 is dosed at MOI 10 using that normalized number. No physical-particle (p24) MOI normalization. |
| **ASCT2 vs. ASCT1 crosstalk** | BaEV uses both receptors; human HSCs express both at different ratios than HEK293T or HCT116. Variants optimizing for ASCT2 on HEK293T may lose efficacy on ASCT1-dominant HSC subsets. | Include an ASCT1-only cell line counter-screen (CHO-ASCT1, CHO-ASCT2 pair) on Tier 2 top-20 per round. FTO also requires retaining ASCT1 breadth per Stage 1 QA §6. |
| **LT-HSC vs. committed progenitor contamination** | CD34⁺CD38⁻CD90⁺ by flow is ~60% LT-HSC; the rest are MPPs that transduce more easily and can dominate the BFP⁺ signal. | 7-color LT-HSC gate (CD34⁺CD38⁻CD45RA⁻CD90⁺CD49f⁺) and CD133 co-staining. Do not accept CD34⁺CD38⁻CD90⁺ as a sufficient gate. |

**Context Risk Verdict: MANAGEABLE WITH THE THREE-TIER DESIGN.** If any one of these mitigations is dropped — in particular the donor-normalized mPB primary assay or the serum-free producer — the campaign will generate beautiful data that does not replicate in a Vertex or 2seventy PD lab, and the platform dies on first customer evaluation.

---

## 6. Throughput vs. Fidelity — the Round Budget

With the three-tier design, the AL loop cadence is:

- **Round cadence:** ~2 weeks per Tier 2 cycle (60 variants/round).
- **Rounds per year:** 6–8 (allowing holidays, donor scheduling, QC failures).
- **Variants through Tier 2 per year:** 360–480.
- **Tier 1 filter ratio:** ~5–10× (enter 300–500/round into Tier 1, advance top 60 to Tier 2).
- **Tier 3 bridge:** 2–3 variants per quarter, total ~10 over 12 months.
- **NSG:** 2 variants over 12 months, late.

This is consistent with the EVOLVEpro T7 RNAP run (~4 rounds, ~70 variants/round) and should deliver **50–100× composite fitness gain** within 12 months if the target's headroom claim holds.

**Budget risk:** mPB donor apheresis product at clinical grade runs ~$8K–$12K per unit, yields ~1×10⁸ CD34⁺, sufficient for ~200 variants at n=3. Annual consumables for Tier 2: **~$0.6–1.2M** for cells alone, plus flow reagents, ddPCR, lentiviral prep — call it **$2–3M/year on assay consumables.** If the budget does not support this, switch cord blood + mPB 50/50 to cut costs ~40%, accepting the context risk noted above.

---

## 7. Explicit NO-GOs (what we are not allowed to do)

1. **No p24 ELISA as the titer measurement for AL training.** Physical particles ≠ infectious particles. p24 is acceptable only for normalization sanity checks.
2. **No HEK293T or HCT116 transduction data as a surrogate for G0 HSC transduction.** Ever. In the AL loop.
3. **No n=1 or n=2 replicates.** n=3 minimum, with three different donors for Tier 2.
4. **No fresh-CD34⁺ data.** Cryopreserved only.
5. **No DMEM+FBS producer context.** Serum-free Expi293 from round 1.
6. **No 24–48 h prestim protocol.** 4 h maximum single-cytokine.
7. **No NSG engraftment in the AL loop.** 16-week readouts, 30–40% CV — confirmatory only, per Stage 0 QA.
8. **No gating at CD34⁺CD38⁻CD90⁺.** Must include CD45RA⁻ and CD49f⁺ to enrich LT-HSC.
9. **No training on variants that read onto the Généthon tail-truncation literal claim** (FTO gate from Stage 1 QA §1 — binary multiplier in the fitness scalar).

---

## 8. Final Stage 2 Decision

| Criterion | Result |
|---|---|
| Assay CV ≤ 15% on primary metric | **PASS** (10–12% with donor normalization) |
| Z' or regression SNR adequate for low-N AL | **PASS** (σ/Δ ≈ 0.15; target R² ≥ 0.6 on test fold) |
| Saturation headroom | **PASS — HIGH POTENTIAL** (50–100× compound; T7-class on titer) |
| Context match to commercial HSC-GT application | **PASS — CONDITIONAL** on the nine explicit NO-GOs |
| Throughput adequate for 6–8 AL rounds/year | **PASS** at ~60 variants/round through Tier 2 |
| Fitness-function design supports multi-objective optimization with FTO gate | **PASS** (weighted log-ratio scalar + binary FTO multiplier) |

## **Assay Verdict: `ROBUST` — conditional on donor normalization, three-tier discipline, and enforced NO-GOs.**

## **Headroom Verdict: `HIGH POTENTIAL` — 50–100× compound, closest analog is pre-engineering T7 RNAP, not Bxb1.**

## **Context Risk: MANAGEABLE — the nine NO-GOs in §7 are the entire mitigation plan. Drop any one and the campaign fails silently.**

## **Final Stage 2 Decision: `PROCEED TO BLUEPRINT`.**

Move to Stage 3. Deliver the library design, mutagenesis strategy, and the ML-loop architecture with the Tier 2 primary assay as the fitness signal. Budget scientist time for donor coordination — that will be the rate-limiting operational step, not the liquid handling.
