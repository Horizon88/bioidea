---
run: HSC-cytopenia full pipeline v1
run_id: e7732b5d65be49d79dafbdf7c841f3e9
stage: 3
stage_key: evo_blueprint
stage_label: Objective Function
phase: main
model: opus
generated_at: 2026-04-22T19:41:13
duration_s: 138.7
cost_usd: 0.532304
tokens_in: 5
tokens_out: 7746
---

---
run: HSC-cytopenia full pipeline v1
stage: 3
stage_key: blueprint
stage_label: Evolutionary Blueprint
phase: main
---

# Stage 3 — Campaign Blueprint: Project **QUIESCO-1**

**Run:** HSC-cytopenia full pipeline v1
**Date:** 2026-04-22
**Author:** Principal Scientist, Protein Engineering & AI Strategy Lead
**Target:** BaEV-Rless envelope glycoprotein (parent UniProt Q9WJT4) — directed evolution for quiescent-HSC lentiviral transduction

---

## 1. Campaign Name

**Project QUIESCO-1** — *QUIescent-HSC Envelope Specification & Commercial Optimization, Round 1.*

Mandate: deliver a BaEV-derived envelope variant achieving ≥50% transduction of true-G0 CD34⁺CD38⁻CD45RA⁻CD90⁺CD49f⁺ mPB HSCs at MOI ≤10, with ≥1×10⁸ TU/mL raw producer titer in serum-free Expi293, <10% producer syncytia, and ≥12 non-conservative substitutions in SU/TM outside the R-peptide, within 14 months and ≤$4M all-in.

---

## 2. The Fitness Equation

The AL loop optimizes a **single scalar** `F(v)` per variant `v`, computed per round on Tier 2 data (donor-normalized), with Tier 1 serving as a pre-gate filter and Bridge assays (Stage 2 QA) serving as rank-validators at specified rounds.

### 2.1 Primary Fitness Scalar (Rounds 1–6, default)

```
F(v) = M_FTO(v) · M_ASCT1(v) · M_immuno(v) · [
           0.35 · log2( TXN_G0(v)     / TXN_G0(WT)     )    # G0 HSC transduction
         + 0.30 · log2( TITER(v)      / TITER(WT)      )    # producer infectious titer
         + 0.20 · log2( PRODVIAB(v)   / PRODVIAB(WT)   )    # producer viability @48h
         + 0.10 · log2( THERMO(v)     / THERMO(WT)     )    # post-concentration stability
         + 0.05 · log2( VCN_per_TU(v) / VCN_per_TU(WT) )    # integration efficiency per infectious unit
       ]  −  λ_sub · max(0, VCN(v) − 3)²                    # over-integration penalty
```

Each additive term is a **log2 fold-change** on a donor-normalized, WT-Rless-anchored basis — not a raw fraction. Log-space keeps the gradient well-behaved across 30× dynamic range on titer and 4× on G0, and makes the weights commensurable.

### 2.2 Binary Multiplicative Gates

Any variant scoring zero on any of the following multiplies the entire fitness to zero and is dropped from training:

| Gate | Definition | Reason |
|---|---|---|
| `M_FTO(v)` | 1 if variant carries ≥12 non-conservative substitutions in SU/TM outside the R-peptide region **AND** Hamming distance to WT Rless tail ≥6 positions in residues 1–20 of cytoplasmic tail; else 0 | Stage 1 QA §1 — escape the Généthon 80%-identity + modified-tail genus claim by forcing meaningful SU/TM engineering, not cosmetic tail edits |
| `M_ASCT1(v)` | 1 if transduction on CHO-ASCT1 counter-screen is ≥50% of WT Rless CHO-ASCT1 baseline; else 0 | Stage 1 QA §1 — receptor breadth optionality; prevents the campaign from collapsing onto pure ASCT2, which would eliminate a key future receptor-switch design-around |
| `M_immuno(v)` | 1 if NetMHCpan-4.1 predicts **no** novel strong-binder (IC50 <50 nM) 9-mer to HLA-A\*02:01, A\*24:02, B\*07:02, DRB1\*15:01 spanning any mutated residue set; AND AggreScan3D ΔAggregation Score <+10% vs. WT; else 0 | Anti-vector immunogenicity and aggregation control; published BaEV already has pre-existing immunity concerns from HERV homology, we do not add to it |

### 2.3 Penalty Term (Soft)

`λ_sub = 0.25`; VCN per cell >3 on Tier 2 bulk is penalized quadratically. This blocks the "mutate the genome to win" pathological regime where a variant achieves high %BFP⁺ by delivering 5–10 integrations per cell — clinically disqualifying (insertional mutagenesis risk, bluebird-Lyfgenia-class AML concern).

### 2.4 Term Definitions (Stage 2 units)

| Term | Definition | Stage 2 assay |
|---|---|---|
| `TXN_G0(v)` | %BFP⁺ within CD34⁺CD38⁻CD45RA⁻CD90⁺CD49f⁺ gate on Day 7, donor-ratio-normalized to same-plate WT Rless | Tier 2 primary |
| `TITER(v)` | Infectious titer (TU/mL) by qPCR on HCT116, serum-free Expi293 producer, 48 h transient transfection | Tier 1 |
| `PRODVIAB(v)` | % live HEK293T/17 at 48 h post-transfection by CellTiter-Glo, corrected for syncytia index | Tier 1 |
| `THERMO(v)` | Fraction of Day-0 titer retained after 7 days at 4°C + 3 freeze-thaw cycles | Tier 1 (batch subset) |
| `VCN_per_TU(v)` | ddPCR VCN in bulk CD34⁺ BFP⁺ fraction / delivered infectious MOI | Tier 2 secondary |
| `VCN(v)` | Mean integrated copies per BFP⁺ cell | Tier 2 secondary |

---

## 3. Weight Justification (Each Weight = One Failure Mode)

| Weight | Term | Failure mode it prevents |
|---|---|---|
| 0.35 | G0 HSC transduction | **The Scout's thesis.** If we do not move this number from 15% → 50%, nothing else matters. Every clinical customer (Vertex, 2seventy, Rocket, Orchard-Kyowa) pays us for this number. Heaviest weight. |
| 0.30 | Producer titer | **COGS collapse.** Each 10× on titer = ~$300K/dose saved and collapses GMP batch size from 20 L → 2 L. Lentigen underbids us at sticker price unless we win here. |
| 0.20 | Producer viability | **Manufacturability gate.** A variant that triples titer but lyses producers in 24 h cannot be manufactured at >100 L scale — the supernatant fills with intracellular protease and inactivates the product. This is the Bernadin 2019 failure mode. |
| 0.10 | Thermostability | **Supply-chain enabler.** Cold-chain robustness differentiates us vs. VSV-G (notoriously labile) — directly enables decentralized HSC-GT manufacturing, which is the next-gen business model. |
| 0.05 | VCN per TU | **Efficiency check.** Catches titer inflation from defective particles. Small weight, but present to prevent gaming. |

Weights were chosen so that **any single axis doubling (log2 = 1)** contributes to fitness in proportion to its commercial value; a 10× titer improvement contributes +1.0 to F, a 3× G0 improvement contributes +0.55. This keeps the easiest-to-move axis (titer) from dominating the scalar and starving the hardest-to-move axis (G0 HSC).

---

## 4. WT Baseline (Ground Truth, Stage 2 Tier 1+2)

To be locked before Round 1 begins, via a **20-replicate Tier 1 run + 9-donor Tier 2 run on parental WT BaEV-Rless** across three independent manufacturing days. Current best-estimates from literature + internal historical (to be confirmed and treated as provisional until the lock-in run):

| Term | WT Rless baseline | SD | Source / confidence |
|---|---|---|---|
| `TXN_G0(WT)` on CD34⁺CD38⁻CD45RA⁻CD90⁺CD49f⁺, MOI 10, 4 h SCF-only prestim | **15.0%** BFP⁺ | 2.5% (abs) | Bernadin 2019 extrapolation + Tier 2 lock-in run required |
| `TITER(WT)`, HEK293T/17, serum-free Expi293, 48 h, qPCR on HCT116 | **1.0×10⁷ TU/mL** | 0.3×10⁷ (~30% rel) | Girard-Gagnepain 2014 + serum-free adjustment factor ~0.6× |
| `PRODVIAB(WT)` at 48 h | **45%** live | 8% (abs) | Historical + literature |
| `THERMO(WT)` (titer retained 7d@4°C + 3 FT) | **50%** of Day 0 | 10% (abs) | Literature |
| `VCN_per_TU(WT)` on bulk CD34⁺ | **1.2×10⁻⁷** integrations / TU delivered | 30% rel | Internal proxy; lock-in required |

**Rule:** the Round-0 WT characterization run is a **hard gate**. If measured WT `TXN_G0` is <8% or >25% on our Tier 2 SOP, the SOP is not ready — do not start the AL loop. This has bitten every academic BaEV campaign that skipped the baseline-lock step.

---

## 5. Throughput Strategy

### **Medium-N Mode — ~60 variants per Tier 2 round, 300–600 pre-screened in Tier 1.**

Justification:

- **Tier 2 cost per variant:** ~$1,800 (mPB CD34⁺ allocation + cytokines + flow + ddPCR + labor). 60 variants/round × 6–8 rounds = 360–480 variants/year @ ~$650K–$870K in Tier 2 alone, plus Tier 1 (~$200/variant × ~3,000/year ≈ $600K).
- **Tier 2 CV 10–12% donor-normalized** is adequate for regression-style AL training at **n=3 donor biological replicates**. Dropping to Low-N (~16/round) saves ~$400K/year but **starves the ML model** — EVOLVEpro and ESM-based AL models show monotonic performance gains up to ~50 variants/round and then plateau; 16/round sits on the unstable left flank of that curve.
- **Time per round:** 2 weeks including Tier 1 triage (Days 1–5), Tier 2 transduction (Days 6–8), Day 7 readout (Day 15), ML retraining + next-round library design (Days 15–20). Achieves **6–8 rounds in 14 months** including bridge gates.
- **Not Medium-High (~96/round):** primary bottleneck is mPB donor apheresis scheduling, not liquid handling. Three donors per round at n=3 donors × 60 variants × 1–2×10⁴ cells/well consumes ~3×10⁷ CD34⁺, which is one apheresis unit at 30% of yield. Going to 96/round requires 2 apheresis units/round → donor scheduling risk dominates.

**Medium-N is the point at which the AL loop is information-rich, the donor pipeline is tractable, and the burn rate is defensible to a board.**

---

## 6. Kill Threshold (Round 1 Gate)

The campaign is killed — or the seed library is scrapped and rebuilt — if **any** of the following is true after Round 1:

| Metric | Round 1 requirement | Rationale |
|---|---|---|
| Top variant `TXN_G0` fold-change vs. WT | **≥1.5×** (i.e., ≥22.5% on G0) | EVOLVEpro against a non-saturated target like T7 RNAP hit 3–5× on R1; BaEV headroom is comparable. <1.5× at R1 means either the library is too conservative or the fitness signal is too noisy to train on. |
| Top-10 variants mean `F(v)` | **≥+0.25** over WT (log2-scalar) | Confirms the signal is above the noise floor of n=3-donor Tier 2. |
| Fraction of Round 1 variants passing `M_FTO` gate | **≥40%** | If fewer, the seed library leans too close to Rless — redesign with more SU/TM diversity. |
| Spearman ρ between Tier 1 titer rank and Tier 2 G0 rank on R1 candidates | **−0.2 ≤ ρ ≤ +0.5** | Pure positive correlation means Tier 1 predicts Tier 2 (we could drop Tier 2 — good). Strong negative ρ (<−0.2) means titer-winners are G0-losers → fitness function is fighting itself and weights need re-tuning before R2. |
| Round 1 variant-level Tier 2 CV on WT technical controls | **≤12% donor-normalized** | If CV has crept above Stage 2 spec, the assay drifted; fix before R2. |

Any two of these failing → **HARD ABORT**, library redesign, 4–6 week timeout. Any one failing → **SOFT HOLD**, single-round diagnostic before R2 launches.

---

## 7. Bridge Points (Stage 2 QA Bridges Mapped to Rounds)

The Stage 2 QA added seven bridges (A–G). Integration into QUIESCO-1 cadence:

| Round | Primary activity | Bridges gated at this round | Gate type |
|---|---|---|---|
| R0 | WT baseline lock-in; assay qualification | — | Internal SOP sign-off |
| R1 | First AL round, 60 variants | — | Kill threshold (§6) |
| R2 | Second AL round | — | Monotonicity check: top `F(v)` must advance ≥0.2 log2 over R1 |
| **R3** | Mid-campaign gate | **Bridges A, B, C, D** on top 10 R1–R3 variants | **Hard — retrains if ρ(healthy↔SCD/aged) <0.7 OR titer drop >3× at 7.5 kb cassette OR Expi293F glycan/complement fail** |
| R4 | Incorporate bridge-A/C data (aged, hypoxia) into training set with 25% sample weight | **Bridge E (UM171/PGE2)** on top 5 R4 variants | Hard — rank-inversion under UM171 disqualifies |
| R5 | Narrow to top 20 globally | **Bridge F (expanded NSG, n=8/arm, 5 variants, secondary transplant)** initiated | Hard on platform filing — Spearman ρ(Tier 2 ↔ NSG secondary) ≥0.6 required before composition-of-matter PCT |
| R6 | Final refinement round, top 20 → top 5 leads | **Bridge G (integration site LAM-PCR)** on top 2 | Hard — LMO2/MDS1-EVI1/HMGA2 hotspot enrichment = disqualified |
| R7 (optional) | Confirmation and polish on lead + 2 backups | Final Bridge F readout | Platform + lead composition claims locked |

**Total rounds:** 6–7. **Total duration:** 14 months (12 AL + 2 bridge timeline). **Platform provisional filing target:** 2026-06-22 (before R1 data), anchored on position classes + ML method disclosure per Stage 1 §5. **Lead composition provisional filing:** 2027-02 (post-R5, pre-NSG readout).

---

## 8. Counter-Selection / Penalty Terms — HSC-Specific Guardrails

Beyond the fitness equation gates, four structural counter-selections are built into the campaign:

### 8.1 The Engraftment-Killer Trap
Classic HSC failure: a variant that transduces G0 cells better because it mildly activates them (pushing G0 → G1). This **kills long-term repopulation** — the Graphite Bio and early bluebird failure mode.

**Guardrail:** Bridge A (aged/SCD substrate) and Bridge F (NSG secondary transplant) both include a **Day 7 Ki-67 intracellular flow measurement on BFP⁺ HSCs**. Any variant pushing Ki-67⁺ fraction >1.3× WT in its BFP⁺ fraction is flagged as an **activation-biased false winner** and dropped from lead nomination regardless of F(v) score. Additionally, R5 introduces an explicit term `−0.15 · log2(Ki67_ratio_v/WT)` into F for the last two rounds.

### 8.2 The Over-Integration Trap
Addressed by the `λ_sub · max(0, VCN−3)²` penalty in §2.1. A variant hitting VCN=6 loses ~2.25 fitness points — more than enough to wipe a 4× G0 win.

### 8.3 The Immunogenicity Trap
`M_immuno` gate (§2.2) runs in silico on every variant **before** it enters the wet lab — cost is negligible, filter is permissive enough to not dominate library design. Stage 5/6 will add ex vivo PBMC assays on final leads, but these are too expensive/slow for the AL inner loop.

### 8.4 The FTO-Gaming Trap
`M_FTO` forces ≥12 non-conservative SU/TM substitutions. To prevent the ML from satisfying this with 12 cheap surface-exposed neutral mutations, the R5 fitness function adds a secondary constraint: **at least 4 of the 12 required substitutions must fall in high-information-content regions** — RBD contact residues (per AlphaFold3 BaEV-SU/ASCT2 complex prediction), TM heptad repeats, or the fusion peptide. This aligns FTO escape with functional engineering.

---

## 9. Deliverable Summary

| Item | Spec |
|---|---|
| **Campaign name** | Project QUIESCO-1 |
| **Fitness equation** | Weighted log2-fold-change scalar, §2.1, gated by three binary multipliers and softened by a VCN over-integration penalty |
| **Primary weights** | G0 txn 0.35 / titer 0.30 / prod viab 0.20 / thermo 0.10 / VCN-per-TU 0.05 |
| **WT baseline (to be locked in R0)** | G0 txn 15±2.5%; titer 1×10⁷ ± 0.3×10⁷ TU/mL; prod viab 45±8%; thermo 50±10%; VCN/TU 1.2×10⁻⁷ ± 30% |
| **Throughput** | Medium-N: 60 Tier 2 variants/round, 6–8 rounds in 14 months, ~$2.6M all-in assay + ~$600–800K bridge spend |
| **Kill threshold (R1)** | Top variant `TXN_G0` ≥1.5× WT; top-10 mean F ≥+0.25; FTO pass ≥40%; Tier 1↔Tier 2 ρ in [−0.2, +0.5]; CV ≤12% |
| **Bridge gates** | R3: Bridges A/B/C/D (aged, full cassette, hypoxia, Expi293F); R4: Bridge E (UM171); R5: Bridge F (expanded NSG); R6: Bridge G (integration sites) |
| **Counter-selections** | Ki-67 activation trap; VCN quadratic penalty; in silico NetMHCpan + AggreScan gates; FTO-gaming constraint on high-information residues |
| **LGS** | MED (confirmed; aged-donor Bridge A keeps the option alive without diluting the cytopenia beachhead) |

---

## 10. Verdict to Next Stage

**Proceed to Stage 4 (wet-lab execution: library design, producer infrastructure, assay SOPs, AL orchestration).** The blueprint above is the full specification needed to build the seed library and start R0. Do not deviate from the fitness equation between rounds without a board-level re-weighting decision — mid-campaign weight drift is the single most common way these loops silently optimize the wrong thing.

The equation is written. The AI will maximize it. Make sure we wrote it right, because in 14 months we will have exactly what we asked for.
