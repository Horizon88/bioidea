---
run: HSC-cytopenia full pipeline v1
run_id: e7732b5d65be49d79dafbdf7c841f3e9
stage: 3
stage_key: evo_blueprint
stage_label: Objective Function
phase: qa
model: opus
generated_at: 2026-04-22T19:44:30
duration_s: 197.3
cost_usd: 0.67089725
tokens_in: 5
tokens_out: 11231
---

---
run: HSC-cytopenia full pipeline v1
stage: 3
stage_key: blueprint
stage_label: Evolutionary Blueprint
phase: qa
---

# Stage 3 QA — Metric Vulnerability Report: How QUIESCO-1 Gets Gamed

**Run:** HSC-cytopenia full pipeline v1
**Date:** 2026-04-22
**Reviewer:** Lead Data Scientist / Systems Biologist
**Subject:** Adversarial audit of the QUIESCO-1 fitness equation. The AI is a hostile optimizer; treat it as such.

---

## 0. Bottom Line

**`REVISE OBJECTIVE FUNCTION.`**

The blueprint is the most thoughtful fitness equation I have seen come out of a Stage 3 in this pipeline. It correctly multiplies by FTO, ASCT1, and immunogenicity gates; it correctly penalizes over-integration; it correctly weights G0 transduction over titer. **It is also gameable in at least seven specific, testable ways**, four of which produce variants that look spectacular on the primary fitness scalar and **fail catastrophically on long-term engraftment, lineage balance, or insertional safety** — exactly the failure modes that killed Graphite Bio, dragged bluebird's MDS/AML signal into a clinical hold, and made FDA stop trusting bulk VCN as a sufficient safety endpoint.

The single biggest unforced error: **the Ki-67 activation guardrail and the engraftment-quality signal are deferred to R5/R6 bridges.** By then the AI has been trained on four rounds of data that systematically reward "variants that mildly cycle G0 cells into G1." That is not a guardrail. That is a four-round delay before you discover the AI has been optimizing the wrong objective the entire time.

Fix the seven loopholes below before Round 1 launches. The cost is one term added to the primary scalar, one term added at R3 not R5, and a tightening of the donor-pairing rule. Total impact: ~$80K incremental assay spend, no schedule slip. Failure to fix them: 18 months and ~$3M into a campaign whose winners will not survive an LTC-IC review at a Vertex BD meeting.

---

## 1. The Loopholes — Seven Specific Ways the AI Cheats

### Loophole #1 — **The Cycling Cheat (CRITICAL)**
**The mechanism:** TXN_G0(v) is %BFP⁺ within the CD34⁺CD38⁻CD45RA⁻CD90⁺CD49f⁺ gate on Day 7. Surface markers are not behavior — they are static phenotype. A variant that modestly activates the cell (G0 → G1 transit) will:
- Transduce 2–3× better (cycling cells admit lentivirus more easily; reverse transcription requires nucleotide pools);
- **Retain the surface marker gate** for at least 5–7 days because CD90/CD49f/CD45RA turnover is slow;
- Score 0.35 · log2(2.5) ≈ +0.46 fitness, which beats almost every other axis.

The blueprint *acknowledges* this in §8.1 and adds a `−0.15 · log2(Ki67_ratio)` term at **R5 onward**. **This is four rounds too late.** Rounds 1–4 generate ~240 variants of training data already biased toward cycling-inducers. The ML model will learn "high Ki-67 = high fitness" because in the early rounds it is true. By R5 the model is path-dependent on the wrong signal.

**Why this is a real risk and not paranoia:** every academic BaEV paper that reported >25% G0 transduction has been independently shown to have cycled the input cells, including the Bernadin 2019 figures the blueprint anchors WT to. The biology *wants* to cheat here.

**Fix:** Move the Ki-67 penalty into the **primary fitness scalar from R1**, with a stronger weight (`−0.25 · log2(Ki67_ratio_v/WT)`). Cost: one extra intracellular flow stain per Tier 2 variant ($8/well × 60 variants × 6 rounds ≈ $3K total). Non-negotiable.

### Loophole #2 — **The Surrogate-Killer Cheat (CRITICAL)**
**The mechanism:** %BFP⁺ is a *fraction*. Fractions can be increased two ways: more numerator, or less denominator. A variant that is mildly cytotoxic to the **non-transduced (BFP⁻)** subset of CD34⁺ — perhaps because residual envelope on the producer-cleared particle binds ASCT2 on bystander cells and triggers low-grade fusion-induced death — inflates the BFP⁺ fraction without transducing more cells.

The blueprint has no absolute-number term. It does not require **BFP⁺ cell count per input CD34⁺** as a separate metric.

**Fix:** Add a co-primary readout — **absolute BFP⁺ LT-HSC count per 10⁴ input CD34⁺** — and require the fitness scalar to use the *minimum* of (a) %BFP⁺ fraction and (b) absolute count, both donor-normalized. This is robust against the surrogate-killer cheat. Already collected by the Stage 2 panel; only the scalar definition needs to change.

### Loophole #3 — **The HCT116 Affinity-Tuning Cheat (HIGH)**
**The mechanism:** TITER(v) is measured by qPCR on **HCT116** indicator cells. HCT116 has a different ASCT2/ASCT1 expression ratio than primary CD34⁺ (HCT116 is ASCT2-dominant, ~10× higher than HSCs; ASCT1 minimal). A variant that affinity-matures specifically against the HCT116 ASCT2 isoform (with HCT116-specific glycosylation) wins the titer term (weight 0.30, easily +1.0 fitness on a 10× improvement) without improving — possibly while *degrading* — primary HSC binding.

The G0 term should pull this back, but the G0 assay has 10–12% CV and runs at MOI 10 (saturating); titer wins are easier and noisier-friendlier.

**Fix:** Cross-validate titer on **two indicator lines** — HCT116 (sensitivity, dynamic range) and a CD34⁺-derived line (KG-1a or primary CD34⁺ MOI calibration). Take the geometric mean. Or: drop the indicator-line titer term to 0.20 and add a 0.10 weight on **MOI-normalized G0 efficiency at MOI 3**, which is sub-saturating and rewards true binding affinity.

### Loophole #4 — **The Late-Cytotoxicity Cheat (MEDIUM)**
**The mechanism:** PRODVIAB(v) is measured at **48 h** post-transfection. GMP harvest is **72–96 h**. A variant that delays cytotoxicity from 36 h (WT) to 60 h scores great on the 48 h readout but still kills producers before harvest at scale. The Bernadin 2019 failure mode the blueprint cites was specifically a 72 h failure mode.

**Fix:** Move PRODVIAB to a **72 h endpoint** (matches GMP harvest) and add a `tox_AUC` parallel readout — area under the cytopathic curve from 24–72 h via Incucyte. Cost: incremental imaging well-time, ~$15K total.

### Loophole #5 — **The Donor Lottery Cheat (CRITICAL)**
**The mechanism:** "Donor-ratio-normalized to same-plate WT Rless" is the right idea, but the blueprint does not specify that **WT and variant must run on the same donor's cells, not just the same plate.** Donor-to-donor BaEV transducibility variance is 1.5–2×. If a variant happens to be tested on three permissive donors and the WT control on three less-permissive donors *on the same plates* (because of how the plate map was filled), the variant is rewarded for donor lottery, not biology.

The published EVOLVEpro work uses a clean isogenic substrate (E. coli, HEK). They never had this problem. The blueprint imported the EVOLVEpro framework without importing the corresponding need for matched substrate.

**Fix mandates (control mandate, see §3 below):**
- WT Rless **on every plate**, **on every donor**, **n=3 wells per donor per plate**. Not "in the same batch."
- Each variant must be normalized to WT on the *same donor*, not the same plate average.
- Donor identity is recorded as a fixed effect in the regression model, not absorbed into a single "donor-normalized" ratio.
- Donor rotation: no donor used in >2 consecutive rounds. Prevents AL loop from over-fitting to donor-specific ASCT2 polymorphisms (SLC1A5 has ≥4 common haplotypes in the population).

This single fix is worth more than every other adjustment combined. Without it, the kill threshold at R1 (top variant ≥1.5× WT) is statistically meaningless — donor lottery alone will produce ≥1.5× ratios in random variants ~15% of the time.

### Loophole #6 — **The FTO-Cheap-Substitution Cheat (MEDIUM)**
**The mechanism:** M_FTO requires ≥12 non-conservative substitutions in SU/TM outside R-peptide. The ML model will preferentially place these in **surface-exposed neutral positions** (loop regions, flexible termini) because those positions tolerate substitution without breaking function. The R5 fix ("4 of 12 must be in RBD contact / heptad / fusion peptide") is too late — by then the model has been trained for four rounds on the cheap-substitution strategy and the design distribution is locked in.

**Fix:** Move the high-information-residue constraint into M_FTO from R1: M_FTO = 1 iff ≥12 non-conservative substitutions outside R-peptide **AND ≥4 of those in {RBD contact residues per AlphaFold3 BaEV-SU/ASCT2, TM heptad repeats, fusion peptide}**. This is a binary gate, not a soft term — easy to enforce, no extra assay cost.

### Loophole #7 — **The Defective-Particle Inflation Cheat (LOW-MEDIUM)**
**The mechanism:** VCN_per_TU is in the equation with weight 0.05 as an "anti-gaming" term. But VCN_per_TU has its own pathology: a variant producing many fusion-defective particles inflates the *physical* particle count (would inflate p24 if measured) and suppresses the *infectious* TU. This *increases* VCN_per_TU artifactually if VCN is measured on bulk and TU on HCT116, because defective particles reduce TU but don't reduce delivered cassette mass.

The 0.05 weight is too low to be diagnostic and too low to penalize. It just adds noise.

**Fix:** Drop VCN_per_TU from the fitness scalar. Move it to a **diagnostic** that is logged but not optimized. If VCN_per_TU drifts >2× across rounds, flag for investigation, but don't let it move the fitness needle.

---

## 2. Sample Size Verdict — `Medium-N is correct, but per-variant donor-N is borderline`

**60 variants per Tier 2 round: ADEQUATE.** The blueprint's Medium-N justification is sound for the AL loop's information needs.

**n=3 donors per variant: BORDERLINE.** With donor-normalized CV of 10–12% and n=3 donors, the 95% CI on a single variant's fitness is approximately ±2.5 · CV/√3 ≈ ±15–17% relative. The R1 kill threshold of "top variant ≥1.5× WT" therefore has a CI that overlaps 1.25–1.75× WT — meaning a variant scoring 1.5× has only ~70% probability of truly being ≥1.3×.

**Fix (cheap):** n=3 donors for the bulk of 60 variants per round, **n=5 donors for the top 10 per round** (re-tested in a confirmation panel before they enter the next-round training data with full weight). Adds ~$20K/round, eliminates the donor-lottery false positives at the top of the rank.

**Epistasis risk:** the BaEV envelope is a multi-pass fusion machine with documented cooperativity between SU RBD, SU/TM cleavage site, TM heptad repeats, and fusion peptide. Single-residue scans will miss the productive epistatic combinations. The blueprint does not specify mutagenesis library design (deferred to Stage 4), but **Medium-N at 60/round is too low for full epistatic coverage if the library is single-residue.** Stage 4 must use **combinatorial libraries (≥2 simultaneous mutations per variant from R2 onward)** or the AI will plateau in a single-mutation local maximum by R4.

**Verdict: Low-N is insufficient. Medium-N (60/round) is the minimum, with confirmation re-test (n=5) on top 10/round.**

---

## 3. Control Mandate — Same-Donor Same-Batch WT, Non-Negotiable

**Required, codified in the assay SOP before Round 0:**

1. **WT BaEV-Rless on every plate, every round.** Minimum 6 wells per plate (one per donor × 2 technical replicates).
2. **Variant-to-WT pairing is by donor identity, not by plate average.** Each variant's TXN_G0(v) is normalized to WT on the same donor. The fitness equation operationally becomes:
   `TXN_G0_norm(v, donor_i) = TXN_G0(v, donor_i) / TXN_G0(WT, donor_i)`
   then geometric mean across donors enters the scalar.
3. **Donor identity recorded as a fixed effect** in any regression-style ML training, not absorbed into a ratio.
4. **Donor rotation:** no single donor used in >2 consecutive rounds; full panel of ≥9 donors over the campaign.
5. **No "historical WT" data.** The blueprint already mandates a Round-0 WT lock-in; that lock-in is the *baseline anchor for power calculations*, not the per-round normalization reference. Per-round normalization uses *that round's* same-donor WT, full stop.
6. **Producer batch matched:** each variant and its same-donor WT control must be produced in the *same transfection day* in the *same producer batch*. Otherwise producer-lot variance (~1.4× across days for BaEV in our experience) confounds the normalization.

This mandate is the single most important addition to the blueprint. Without it, the kill threshold at R1 is arithmetic theater.

---

## 4. Safety Term — Five Penalty Terms the Equation Is Missing

The current equation penalizes over-integration (`λ_sub · max(0, VCN−3)²`) and gates on in silico immunogenicity. **It does not penalize the failure modes that have actually killed HSC gene therapy programs.** Five additions:

### Safety Term 1 — **Activation Penalty (Ki-67), from R1 not R5**
`−0.25 · log2(Ki67_ratio_v / Ki67_ratio_WT)` in BFP⁺ LT-HSC fraction. From R1.
*Failure mode prevented:* Graphite Bio-class loss of long-term repopulating HSC due to G0 → G1 forcing. This is the single most-likely silent killer of the campaign.

### Safety Term 2 — **Lineage Bias Penalty, R3 onward**
At R3, top 10 variants undergo CFU-GEMM at 14 days; compute myeloid:erythroid:lymphoid ratio in BFP⁺ colonies. Add to fitness:
`−0.10 · |log2(myeloid_ratio_v / myeloid_ratio_WT)|`
*Failure mode prevented:* myeloid-skewed reconstitution is both an aging signature and a leukemia signature. A variant that selectively transduces myeloid-biased aged HSCs (which exist in young donors as a small subset, ~5–15%) will look fine on %BFP⁺ but produce a myeloid-skewed clinical reconstitution. This is the bluebird MDS/AML signal that took Lyfgenia into a clinical hold.

### Safety Term 3 — **Engraftment-Quality Surrogate (LTC-IC), R3 onward**
LTC-IC is too noisy and slow for the inner AL loop (5-week readout, CV 18–25%) — but it can enter as a **per-variant binary safety gate** at R3:
`G_LTC = 1 if LTC-IC frequency in BFP⁺ ≥ 0.6 × LTC-IC in untransduced same-donor; else 0.`
Multiplied into the fitness scalar at R3+ for top 20 variants.
*Failure mode prevented:* variants that destroy long-term repopulating activity while preserving Day-7 surface markers.

### Safety Term 4 — **Tightened VCN Cap**
The current penalty `λ · max(0, VCN−3)²` allows VCN=3 unpenalized. **FDA's stated preference is VCN ≤2 in the final drug product.** Tighten to:
`λ_sub · max(0, VCN(v) − 2)²` with `λ_sub = 0.4`.
A variant at VCN=4 now loses 0.4 · 4 = 1.6 fitness points — enough to disqualify any G0 win short of 3.5×.
*Failure mode prevented:* over-integration insertional mutagenesis; this is the lever that distinguishes "Lyfgenia-class clinical hold risk" from "clean integration profile."

### Safety Term 5 — **Class II Immunogenicity + Population Coverage**
Current `M_immuno` checks NetMHCpan-4.1 against four HLA Class I alleles. Inadequate. Required additions:
- **Class II:** NetMHCIIpan against DRB1\*03:01, \*04:01, \*07:01, \*15:01 (covers >80% of US population for CD4 help).
- **Population coverage:** add HLA-A\*03:01, \*11:01, \*23:01, B\*35:01, B\*44:02 to Class I panel (covers Asian, East African, and Hispanic populations relevant to SCD/β-thal markets).
- **Threshold:** ≤2 novel strong binders allowed per variant (not zero), but each one in the immunogenicity panel adds `−0.05` to fitness. Soft penalty, not gate.

*Failure mode prevented:* anti-vector immune responses on second dose (relevant for in vivo HSC-LV optionality) and on retreatment in MDS/aplastic anemia (where patients often need multiple infusions).

---

## 5. Summary of Required Equation Changes

**Original primary fitness scalar:**
```
F(v) = M_FTO · M_ASCT1 · M_immuno · [
         0.35 · log2(TXN_G0_v/WT) + 0.30 · log2(TITER_v/WT)
       + 0.20 · log2(PRODVIAB_v/WT) + 0.10 · log2(THERMO_v/WT)
       + 0.05 · log2(VCN_per_TU_v/WT)
     ] − 0.25 · max(0, VCN−3)²
```

**Revised primary fitness scalar (R1 onward):**
```
F(v) = M_FTO* · M_ASCT1 · M_immuno* · G_LTC(R3+) · [
         0.35 · log2( min(%BFP_frac, abs_BFP_count)_v / WT )    # Loophole #2
       + 0.20 · log2( TITER_geomean(HCT116, KG1a)_v / WT )      # Loophole #3
       + 0.10 · log2( TXN_G0(MOI 3)_v / WT )                    # Loophole #3
       + 0.20 · log2( PRODVIAB(72h)_v / WT )                    # Loophole #4
       + 0.10 · log2( THERMO_v / WT )
     ] 
     − 0.25 · log2(Ki67_v / Ki67_WT)                            # Safety #1, from R1
     − 0.10 · |log2(myeloid_ratio_v / WT)|  (R3+)               # Safety #2
     − 0.40 · max(0, VCN(v) − 2)²                               # Safety #4
     − 0.05 · #(novel_HLA_strong_binders)                       # Safety #5
```

Where:
- `M_FTO*` = original M_FTO + the high-information-residue constraint (Loophole #6) **from R1**.
- `M_immuno*` = expanded HLA panel (Class I + II, broader population coverage) (Safety #5).
- `G_LTC` = LTC-IC binary gate, applied to top 20 variants at R3 forward (Safety #3).
- VCN_per_TU dropped from scalar; logged as diagnostic only (Loophole #7).
- All normalizations are **same-donor, same-producer-batch** (Loophole #5, Control Mandate §3).

---

## 6. Verdict

| Audit Item | Status |
|---|---|
| Fool's Gold trap (cycling, surrogate killer, surface marker drift) | **FAIL** — Loopholes #1, #2 unmitigated in primary scalar |
| Overfitting / N-number risk | **PARTIAL** — Medium-N adequate but per-variant n=3 donors needs n=5 confirmation on top 10 |
| Baseline drift / donor variance | **FAIL** — Donor-pairing not enforced; "same-plate WT" is the wrong control discipline |
| Safety blind spots (immunogenicity breadth, lineage bias, engraftment quality, VCN cap) | **FAIL** — Five safety terms missing or deferred too late |
| FTO gaming (cheap substitutions) | **FAIL** — High-info-residue constraint deferred to R5 |

## **Verdict: `REVISE OBJECTIVE FUNCTION.`**

The blueprint cannot proceed to Stage 4 wet-lab execution as written. Required revisions before R0 lock-in:

1. **Move Ki-67 activation penalty into primary scalar from R1** (Safety #1).
2. **Replace %BFP⁺ with min(fraction, absolute count) in the G0 term** (Loophole #2).
3. **Geometric-mean titer across HCT116 + KG-1a; add MOI-3 sub-saturating G0 term** (Loophole #3).
4. **Move PRODVIAB to 72 h endpoint with AUC** (Loophole #4).
5. **Mandate same-donor, same-producer-batch WT pairing; donor as fixed effect; donor rotation** (Loophole #5, Control Mandate).
6. **Move high-information-residue FTO constraint into M_FTO from R1** (Loophole #6).
7. **Drop VCN_per_TU from scalar; log as diagnostic** (Loophole #7).
8. **Add lineage-bias term at R3, LTC-IC gate at R3, tightened VCN cap (>2 not >3), expanded HLA panel including Class II** (Safety Terms 2–5).
9. **n=5 donor confirmation on top 10 variants per round** (Sample Size Verdict).

Cost of full implementation: ~$80–120K incremental over the 14-month campaign. Schedule slip: zero. Headcount impact: 0.25 FTE for the donor-pairing operational overhead.

Cost of *not* implementing: a campaign that produces beautiful Day-7 BFP numbers, fails LTC-IC at R5, fails NSG secondary at R6, and leaves us with composition-of-matter on a variant that activates HSCs into G1 and induces myeloid skew. That is not a platform. That is a $40M lesson in why you don't trust the scalar.

**Send this back to Stage 3 main for revision. Re-audit before greenlighting Stage 4.**

The AI is not your friend. It is a hostile optimizer that will find every loophole you leave in the equation. Close them now or pay later.
