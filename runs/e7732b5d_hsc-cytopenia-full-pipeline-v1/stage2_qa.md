---
run: HSC-cytopenia full pipeline v1
run_id: e7732b5d65be49d79dafbdf7c841f3e9
stage: 2
stage_key: scientist
stage_label: Assay Audit
phase: qa
model: opus
generated_at: 2026-04-22T19:38:54
duration_s: 155.3
cost_usd: 0.52012825
tokens_in: 5
tokens_out: 9094
---

---
run: HSC-cytopenia full pipeline v1
stage: 2
stage_key: assay
stage_label: Technical Pre-Mortem
phase: qa
---

# Stage 2 QA — Reality Gap Report: The Translational Gauntlet

**Run:** HSC-cytopenia full pipeline v1
**Date:** 2026-04-22
**Reviewer:** Translational Medicine Lead / Clinical Pharmacologist
**Subject:** Does the Stage 2 assay stack actually predict clinical performance in the patient populations we intend to dose? Or are we teaching EVOLVEpro to win in a petri dish?

---

## 0. Bottom Line

**`BRIDGE ASSAY REQUIRED.`**

The Stage 2 memo is the best assay design I have seen in an HSC-GT campaign memo in five years. It correctly forces serum-free Expi293, cryopreserved mPB, 4h single-cytokine prestim, LT-HSC gating to CD45RA⁻CD49f⁺, and donor-normalized n=3. It correctly excludes NSG from the AL loop. These are all real, and I will not relitigate them.

**But it has blind spots the author was too close to see.** The fitness function is a reporter-LV on healthy adult mPB from a Miltenyi apheresis vendor, transduced in atmospheric oxygen, with a ~700 bp BFP cassette, on HEK293T producers. **The commercial product is a 7–9 kb therapeutic cassette on Expi293F GMP producers, transduced into plerixafor-mobilized SCD or G-CSF-mobilized aged MDS CD34⁺, in a hypoxic bone marrow niche post-infusion, cleared by human serum complement if we ever pivot in vivo.** Five of those six axes are unaddressed.

The AI will find what the AI is asked to find. If we ask it to optimize reporter-BFP transduction of healthy young mPB in 21% O₂, that is exactly what we will get — and there is a credible mechanistic story for why the winners underperform on the actual clinical substrate. The bridge is not optional; it is the difference between a platform and a $50M postmortem.

---

## 1. The Mismatch List — Screen vs. Commercial Reality

| Axis | Stage 2 Screen | Commercial HSC-GT Reality | Delta |
|---|---|---|---|
| **Donor age** | Healthy adults (likely 18–40, typical apheresis vendor demographic) | SCD: median 20s–30s + oxidative stress; β-thal: children + transfusion iron overload; MDS: median 70s; Fanconi: pediatric with DDR defects; aplastic: heterogeneous | Large; aged/diseased HSCs have ↓ASCT2, ↑p16/p21, altered cycling |
| **Mobilization** | Unspecified — almost certainly G-CSF±plerixafor from commercial vendor | **SCD: plerixafor-only** (G-CSF contraindicated — triggers crisis, sometimes fatal); β-thal: G-CSF+plerixafor; aplastic: BM harvest, not mPB | Plerixafor-mobilized CD34⁺ have distinct transcriptome, more primitive, more G0 |
| **Oxygen tension** | 21% O₂ (standard incubator) | BM niche **1–4% O₂**; post-transplant homing into hypoxic niche | Hypoxic HSCs have altered surface proteome; ASCT2 is nutrient/hypoxia-regulated |
| **Payload size** | ~700 bp BFP under EF1α | **7–9 kb** therapeutic cassette (β-globin LCR, BCL11A shRNA, ARSA, FANCA, γc) | Envelope-dependent packaging efficiency is payload-size-sensitive; BaEV titer drops ~2–5× at full clinical payload size |
| **Producer cell line** | HEK293T/17 (SV40 large T, forbidden by several GMP frameworks) | **Expi293F / HEK293F / CAP-T** (GMP-compliant, different glycosylation machinery) | Envelope glycosylation patterns change; thermostability and complement sensitivity shift |
| **Transduction vessel** | 96-well static, <1 mL | 1–4 L gas-permeable bag (Saint-Gobain / G-Rex) or CliniMACS Prodigy cassette, **1–4×10⁶ CD34⁺/mL** | Particle diffusion, shear, sedimentation, and cell-surface encounter kinetics all differ |
| **Cytokine context** | SCF 50 ng/mL alone, 4 h | Multiple programs add **UM171, SR1, PGE2, or 16,16-dmPGE2** for engraftment benefit | Variants evolved in SCF-only may lose function when co-dosed with UM171 (alters HSC fate) |
| **Vector post-processing** | Unconcentrated supernatant (thermostability proxy only) | TFF concentration (100–500×), benzonase, chromatography, 0.22 µm filter, –80°C storage | Sheer/concentration stress differentially inactivates envelope variants |
| **Serum exposure** | None (in vitro) | Autologous serum during infusion; complement active | **BaEV is complement-sensitive**; variants never tested here |
| **Integration-site biology** | Ignored | Integration site profile drives safety (LMO2 history) and expression durability | Not in training loop |
| **Readout** | Day 7 %BFP⁺ in CD34⁺CD38⁻CD45RA⁻CD90⁺CD49f⁺ + VCN | 16-week NSG secondary engraftment, multilineage; in humans, durable VCN 1–2+ years | Top 2 NSG variants cannot rank-order 60–100 Tier 2 hits |

**Count of axes differing ≥1 variable without a validation bridge in the current plan: 8 of 11.** The Stage 2 memo's kill criterion (>2 mismatched variables without a bridge = NO-GO) is breached by a factor of 4.

---

## 2. The "Artifact" Risk — Five Named Failure Modes

### Artifact #1 — **The "Young Healthy Donor" Variant**
**High risk.** The AL loop trains exclusively on healthy adult mPB. Aged and diseased HSCs have **3–10× lower ASCT2 surface expression** (confirmed in MDS and SCD proteomics), higher CDKN2A/p16, and a shifted lipid raft composition. A variant optimized for young healthy ASCT2-high cells may rank-invert on the actual patient substrate. **The LGS=MED aged-HSC optionality is entirely unsupported by the current assay** — zero aged-donor cells enter the loop.

### Artifact #2 — **The "Reporter Cassette Cheat"**
**High risk.** A 700 bp BFP cassette packages easily in any envelope, and a strong EF1α promoter masks modest integration/expression defects. The clinical 7–9 kb payload reveals **payload-size-dependent envelope defects** that the screen cannot see. BaEV specifically has shown ~2–5× titer loss at full clinical cassette size in published data. We could evolve variants that win on BFP and lose on β-globin.

### Artifact #3 — **The "21% O₂ ASCT2 Artifact"**
**Medium-high risk.** ASCT2 is a **glutamine/nutrient transporter regulated by mTOR and hypoxia.** CD34⁺ cells cultured at 21% O₂ upregulate ASCT2 within hours — artificially boosting BaEV transducibility relative to the hypoxic BM niche the HSC came from (and the niche it must home back to post-infusion). Variants optimized for normoxic ASCT2-high cells may fail on the cells that actually matter in vivo. The memo does not mention oxygen tension once.

### Artifact #4 — **The "HEK293T Glycan Shadow"**
**Medium risk.** HEK293T is disallowed or disfavored by many GMP frameworks (SV40 large T). Scale-up will require **HEK293F / Expi293F / CAP-T** producer lines. These lines have measurably different N-glycosylation (α2,6- vs. α2,3-sialic acid ratios; core fucosylation). Envelope glycans drive (a) complement recognition, (b) DC-SIGN/L-SIGN off-target capture, and (c) serum half-life. A variant selected on HEK293T glycans may be **immunogenic or complement-sensitive** on the GMP line. This is a classic pre-CMC artifact — we see it every 18 months in the antibody world, and the envelope world is worse because nobody is looking.

### Artifact #5 — **The "Plerixafor Gap"**
**Medium risk.** SCD — our flagship beachhead indication — **cannot receive G-CSF** (vaso-occlusive crisis risk). Every SCD program uses **plerixafor-only mobilization**, which produces a more primitive, more G0-enriched, transcriptionally distinct CD34⁺ population versus G-CSF mPB. The commercial vendors who supply healthy donor mPB use G-CSF±plerixafor. We are training on the wrong mobilization agent for our highest-velocity market. Vertex and bluebird both learned this the hard way in 2018–2020.

### Artifact #6 — **The NSG Rank-Order Failure (already half-acknowledged)**
**Medium risk.** The memo explicitly pulls NSG out of the AL loop — correct — but then runs **only top 2 variants** in NSG at 16+16 weeks. **Rank order within the top 10 Tier 2 hits is not established before platform filing.** If Tier 2 %BFP⁺ correlates with NSG repopulation at r≈0.5 (optimistic for this class of assay), the probability that "best Tier 2 hit" = "best NSG hit" among 10 candidates is ~30%. We could file composition-of-matter on the wrong lead.

---

## 3. Bridge Assay Requirement — The R3/R4 Stress Gate

**Non-negotiable additions to the plan, gated at Round 3 (mid-campaign), before any platform filing or GMP transfer:**

### Bridge A — The Aged/Diseased Substrate Panel (R3 gate)
- **Top 10 Tier 2 variants** re-tested on three orthogonal patient substrates:
  1. **Plerixafor-only mobilized SCD patient CD34⁺** (n=3 donors, commercial vendor — HemaCare, AllCells, or Bio-IVT have SCD apheresis product).
  2. **MDS patient CD34⁺** from BM aspirate (n=3 donors, age >60; focus on low-risk MDS to avoid cytogenetic confounders).
  3. **Aged healthy mPB CD34⁺** (n=3 donors, age >65) — proxy for the CHIP/clonal hematopoiesis longevity axis and the LGS=MED claim.
- **Kill criterion:** if Spearman rank correlation between healthy-mPB fitness and aged/SCD-mPB fitness < 0.7 on top-10 variants, **the training loop is generating a biased winner.** Pause; retrain with aged-donor data weighted into the scalar.

### Bridge B — The Clinical Cassette Swap (R3 gate)
- **Top 10 Tier 2 variants** re-tested with a **full-size 7.5 kb therapeutic-proxy cassette** (e.g., β-globin mini-LCR + γ-globin transgene + WPRE, or a stuffer cassette matched to Lyfgenia payload dimensions).
- **Readout:** titer drop ratio (full-cassette / BFP-cassette) and transduction efficiency on mPB CD34⁺.
- **Kill criterion:** any variant showing >3× titer drop at full cassette size is disqualified from lead nomination regardless of BFP performance.

### Bridge C — The Hypoxic Assay Arm (R3 gate)
- **Top 10 variants** transduced in **3% O₂ hypoxia chamber** (hypoxic workstation — Baker Ruskinn or similar) with the full Tier 2 protocol otherwise unchanged.
- **Readout:** same LT-HSC-gated %BFP⁺, plus ASCT2 surface density (αASCT2 flow) as a covariate.
- **Kill criterion:** >2× fold-change in rank order between 21% O₂ and 3% O₂ top-10 → add a hypoxic arm to the AL loop from R4 onward.

### Bridge D — GMP Producer Line Sanity Check (R3 gate)
- **Top 5 variants** produced in **Expi293F suspension** alongside HEK293T adherent.
- **Readouts:** titer (qPCR), thermostability (same protocol), and **complement stability** (30 min incubation in 50% human serum from pooled donors, then titer on HCT116). Add a simple **mass-spec N-glycan profile** on concentrated vector from both lines.
- **Kill criterion:** >3× titer drop on Expi293F, OR >50% complement inactivation, OR a glycan profile shift that matches known immunogenic motifs (terminal Gal-α-1,3-Gal, Neu5Gc) → disqualify from lead nomination.

### Bridge E — Small-Molecule Cocktail Compatibility (R4 gate)
- **Top 5 variants** tested at MOI 10 in Tier 2 ± **UM171 (35 nM)** ± **PGE2 (10 µM)**. These are the clinical cocktail elements our customers (Vertex, Orchard-Kyowa, Rocket) will be using.
- **Kill criterion:** any variant that rank-inverts in presence of UM171 is a no-ship — UM171 is the dominant stem-retention small molecule in the clinical workflow.

### Bridge F — Expanded NSG Rank Validation (R5/R6)
- **Top 5 Tier 2 variants** (not top 2) in NSG **secondary transplant**, 16-week primary + 16-week secondary, n=8 mice/variant per arm, multilineage chimerism as endpoint.
- **Kill criterion:** if rank-order between Tier 2 %BFP⁺ and NSG secondary chimerism has Spearman ρ < 0.6 among the top 5, **pause platform filing** until a Tier 2.5 LTC-IC-plus-hypoxia assay is validated as an NSG surrogate.

### Bridge G — Integration Site Sanity (once, R5)
- **Top 2 variants** deep-sequenced for integration site distribution on bulk transduced CD34⁺ (LAM-PCR + Illumina). Compare to VSV-G and canonical BaEV-Rless controls.
- **Kill criterion:** enrichment for LMO2/MDS1-EVI1/HMGA2 hotspot loci vs. VSV-G baseline → regulatory red flag, disqualify.

---

## 4. What the Stage 2 Memo Got Right (for the record)

- Forcing Expi293 serum-free from R1 — correct.
- Rejecting p24 ELISA as the training signal — correct.
- n=3 biological donors, donor-normalized — correct.
- Cryopreserved-only, 4h single-cytokine — correct.
- CD45RA⁻CD49f⁺ gate, not just CD38⁻CD90⁺ — correct.
- FTO distance as binary multiplier — correct, and ties cleanly to Stage 1 QA mandate.

The gaps above are additions, not replacements. The core design stands.

---

## 5. Cost and Timeline Impact of the Bridge

- **Bridge A (diseased/aged substrate):** +$180–250K per R3 gate (SCD apheresis units are $15–25K each and limited supply; MDS aspirate access via Hematologic Malignancy Research Consortium or direct IRB).
- **Bridge B (full cassette):** +$40–60K (vector prep + titer runs).
- **Bridge C (hypoxia):** +$80K capex for workstation if not available, +$30K consumables/round.
- **Bridge D (GMP line + complement + glycan):** +$60K one-time.
- **Bridge E (UM171/PGE2):** +$20K consumables.
- **Bridge F (expanded NSG):** +$150–200K (48 additional mice + serial transplant cost).
- **Bridge G (integration sites):** +$40K.
- **Total bridge spend:** **~$600K–$800K** across the 12-month campaign, load of ~25% on top of the baseline $2–3M assay consumables.
- **Timeline impact:** R3 gate adds ~3 weeks. R5 gate adds ~6 weeks for expanded NSG. **Net: campaign extends from 12 months to ~14 months.** Acceptable.

---

## 6. Final QA Verdict

| Gauntlet item | Status |
|---|---|
| Buffer / reagent mismatch (producer media, cassette, cytokines, O₂) | **FAIL** — 3 unbridged variables |
| Host cell trap (donor age, disease state, mobilization agent, tissue O₂) | **FAIL** — 4 unbridged variables |
| Downstream trap (NSG bridge, integration, complement, cassette size) | **PARTIAL FAIL** — NSG planned but underpowered at n=2 variants; no integration, complement, or full-cassette arm |
| Patient heterogeneity (SCD, MDS, aged donors) | **FAIL** — zero patient substrate in current plan |

## **Verdict: `BRIDGE ASSAY REQUIRED`.**

Stage 2 assay design is fundamentally sound but must be amended with **Bridges A–G before Round 3 data is allowed to feed the AL loop or support a platform filing.** Specifically, Bridges A, B, C, and D are **gating for lead nomination**; Bridges E, F, G are gating for platform IP filing and GMP transfer.

**Do not proceed to Stage 3 (blueprint) without the bridge plan codified into the assay SOP and budget.** The baseline memo optimizes a reporter for healthy young donors in normoxic plastic. The commercial product has to work on a 65-year-old MDS patient's bone marrow cells, delivering a 9 kb payload, under complement attack, on a GMP producer line nobody on the scientific team has touched yet. We will not find out which gap killed us for 18 months and $40M — unless we bridge now.

**Proceed to Stage 3 conditional on bridge incorporation.**
