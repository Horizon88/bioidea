---
run: HSC-cytopenia full pipeline v1
run_id: e7732b5d65be49d79dafbdf7c841f3e9
stage: 5
stage_key: lab_ops
stage_label: Lab Operations
phase: main
model: opus
generated_at: 2026-04-24T11:09:34
duration_s: 253.4
cost_usd: 0.8760062500000001
tokens_in: 5
tokens_out: 13256
---

---
run: HSC-cytopenia full pipeline v1
stage: 5
stage_key: lab_ops
stage_label: Campaign Operations Plan
phase: main
---

# Stage 5 — Campaign Operations Plan: QUIESCO-1

**Run:** HSC-cytopenia full pipeline v1
**Date:** 2026-04-24
**Author:** Director, Laboratory Operations & Program Management
**Subject:** Execution roadmap, 5-round AL campaign against BaEV-Rless envelope. Week-by-week. Vendor-locked. Budget-capped.

---

## 0. Preamble — What This Plan Assumes I Was Handed

Stage 4 QA signed off 2026-04-24 (Friday). Week 1 begins **Monday 2026-04-27**. The blueprint (Stage 3) specified 6–8 rounds at 60 Tier 2 variants/round; Stage 3 QA revised the objective function and added safety terms; Stage 4 QA appended a FastRelax step, a 15 Å glycan-check trigger, and a "functional-rescue override" schema. **I am compressing the blueprint to 5 AL rounds inside a 12-month campaign** because (a) mPB donor apheresis is the rate-limiter, not liquid handling, and (b) the Round-3 bridge gate (Bridges A–D) is the real decision point — if we survive it, 2 more rounds of refinement are enough; if we don't, a 6th round doesn't save us.

Anything that cannot be ordered, scheduled, or staffed in this plan is out of scope. I will flag it explicitly when it happens.

---

## 1. The Schedule — Week-by-Week

**Week 1 = Mon 2026-04-27. Campaign end = Fri 2027-04-23 (Week 52).** NSG secondary transplant endpoint falls Week 52 ± 2.

| Weeks | Dates | Activity | Gate / Deliverable |
|---|---|---|---|
| **W1–W2** | Apr 27 – May 8 | Stage 4 QA calibration: implement FastRelax, 15 Å glycan trigger, functional-rescue override schema; finalize Tier 1/2 SOPs; IACUC + IBC submissions filed Mon W1 | SOP lock; IACUC + IBC filed |
| **W1–W6** | Apr 27 – Jun 5 | **R0 — WT baseline lock-in + assay qualification.** 20-rep Tier 1 WT + 9-donor Tier 2 WT across 3 producer batches. CHO-ASCT1/ASCT2 counter-screen lines qualified. Hypoxia workstation commissioned (Baker Ruskinn). Platform provisional drafts on Stage 1 §5 filings. | Baseline numbers locked; Priority-1 provisionals filed **by W8 (Jun 22)** per Stage 1 deadline |
| **W3–W6** | May 11 – Jun 5 | Seed library design (AI sampler + Fast Filter + Slow Filter). Twist order placed end of W5. | Seed library: 80 variants ordered |
| **W7–W10** | Jun 8 – Jul 3 | **R1.** Synthesis lands W7; cloning W7–W8; lenti packaging W8; Tier 1 W8–W9; Tier 2 W9–W10 (3 donors × 60 variants). | **R1 kill-threshold review, W11 Mon.** Hard stop if top variant <1.5× WT OR top-10 mean F <+0.25 OR FTO pass rate <40% OR Tier 1↔Tier 2 ρ outside [−0.2, +0.5] OR CV >12%. |
| **W11–W14** | Jul 6 – Jul 31 | **R2.** ML retrain on R1 data; library order W11; Tier 1 W13; Tier 2 W13–W14. Donor rotation: no overlap with R1 panel. | Monotonicity check: top F(v) must advance ≥+0.2 log2 over R1. Soft hold if fails. |
| **W15–W20** | Aug 3 – Sep 11 | **R3 + Bridge gate.** R3 Tier 1/2 as normal (W15–W17). In parallel W16–W19: **Bridge A** (SCD + MDS + aged CD34⁺ on top 10); **Bridge B** (7.5 kb cassette swap); **Bridge C** (3% O₂ hypoxia arm); **Bridge D** (Expi293F producer + complement + N-glycan MS). Week 20 = decision week. | **R3 HARD GATE.** Spearman ρ(healthy ↔ SCD/aged) ≥0.7; no >3× titer drop at full cassette; no >2× rank inversion on hypoxia; Expi293F titer within 3× of HEK293T; pass complement; clean glycan profile. Failure → retrain with bridge data weighted and extend R3 by 2 weeks. |
| **W21–W24** | Sep 14 – Oct 9 | **R4.** Bridge A/C data integrated into training with 25% sample weight. Bridge E (UM171 + PGE2 co-dose on top 5) runs parallel W22–W24. | Rank-inversion under UM171 disqualifies variants from lead candidacy. |
| **W25–W30** | Oct 12 – Nov 20 | **R5.** Final AL round; narrow from ~150 cumulative top variants to top 20 globally. Bridge F (expanded NSG, n=8/arm, top 5 variants) **initiated W27** — primary transplant. Bridge G (LAM-PCR integration site) on top 2 W29–W30. | Platform PCT conversion by W30 (Priority-1 12-month deadline = Jun 2027, but we convert early to bundle R5 data). |
| **W31–W46** | Nov 23 – Mar 12 | **NSG primary transplant — 16-week engraftment readout.** Biweekly peripheral bleeds (chimerism flow). Lab capacity shifts to lead characterization: thermostability panels, serum-stability, cross-species ASCT2 binding (cyno homolog for tox studies). Lead composition-of-matter provisional filings drafted and filed (target W36, Feb 2027). | Primary chimerism readout W46. Ranks top 5 variants. |
| **W47–W52** | Mar 15 – Apr 23 | **NSG secondary transplant seeded W46; 6-week partial readout only** (full 16-week secondary lands W62, outside the nominal campaign window — that data is the Stage 6 handoff deliverable). Campaign closeout: lead selected, 2 backups designated, full regulatory-grade VCN/integration/tox prep for Stage 6. | **Lead variant nominated W52.** Secondary transplant continuation budgeted into Stage 6. |

**Known schedule risks:**
- **Donor apheresis slippage** (AllCells/HemaCare reschedules): 1–2 weeks/occurrence, ~30% probability per round. Mitigation: 2-donor pre-contract buffer.
- **IACUC resubmission** if protocol needs amendment (probability ~40% on first submit): 3–4 week delay. Mitigation: pre-consultation with IACUC chair W0.
- **Twist clonal gene failures** (repeat-rich env sequences fail synthesis ~8–12% of the time): re-order at +10 business days. Mitigation: budget 10% over-order; split to IDT for failed sequences.

---

## 2. The N-Number Plan

**Total Tier 2 variants over 5 rounds: 300. Plus ~150 B-list on Tier 1 only. Plus WT replicates. Plus confirmation n=5 donor panels on top 10/round.**

| Round | Tier 2 N (A-list) | Tier 1-only N (B-list) | Donor panel (Tier 2) | Rationale |
|---|---|---|---|---|
| R0 | — (WT only) | — | 9 donors × 20 reps WT | Baseline lock-in. Non-negotiable per Stage 3 blueprint. |
| R1 | 60 | 15 | 3 fresh donors + re-test top 10 on +2 donors | **Exploration-weighted library.** Library design favors diversity over predicted fitness: ~40 high-diversity variants (broad RBD + TM sampling) + 20 ML-ranked top predictions. First AL round — model has no task-specific data yet. |
| R2 | 60 | 15 | 3 fresh donors + top-10 n=5 | Shift to 50/50 exploration/exploitation. Incorporate combinatorial (≥2 mutations) library members. |
| R3 | 60 | 15 | 3 fresh donors + top-10 n=5 + **Bridge A**: top 10 on 3 SCD + 3 MDS + 3 aged donors | Exploitation-weighted; first round where bridge data gates advancement. |
| R4 | 60 | 15 | 3 fresh donors (weighted inclusion of bridge-A donor classes) + top-5 n=5 + **Bridge E**: top 5 ± UM171 | Bridge data folds into training; continue combinatorial diversity in TM/MPER. |
| R5 | 60 | 15 | 3 fresh donors + top-5 n=5 + **Bridge F**: top 5 × 8 NSG mice × 2 arms | Refinement; narrow from cumulative 300 to top 20 to top 5. |
| **Totals** | **300 Tier 2** | **75 B-list** | ~24 mPB donors + 3 SCD + 3 MDS + 3 aged + 48 NSG mice | — |

**Why Medium-N (60) not Low-N (~20):** Low-N at n=3 donors × 20 variants = 60 data points/round is below the stable regime for regression-style AL on a scalar with 10–12% CV and multi-term objective. EVOLVEpro T7 RNAP plateau is at ~50 variants/round. Going lower trades $400K/year in assay savings for 2 extra AL rounds (~12 weeks) of slower convergence — bad math on a 12-month clock.

**Why 5 rounds not 7:** Round 3 is the bridge gate. If R3 passes, diminishing returns on the AL loop set in by R5 — the protein is a ~600 aa target, and by R5 the model has seen ~300 labeled variants + bridge data, enough to converge. If R3 fails, we don't run rounds 4–7; we pivot scaffold. Budgeting for 7 rounds invites scope creep.

---

## 3. Vendor Strategy

**Lock-in decisions made W0; change orders after W4 require PI sign-off.**

### DNA Synthesis
| Vendor | Role | Turnaround | Cost |
|---|---|---|---|
| **Twist Bioscience** | Primary. eBlock/gene fragments for RBD + TM + MPER mutagenesis cassettes (~200–600 bp each). Full-length clonal env genes (~1.9 kb) for R5 lead candidates only. | eBlocks: 5–7 business days. Clonal genes: 14–18 business days. | eBlocks ~$40–80/variant at campaign volumes (Twist Enterprise tier). Clonal genes ~$280–350/variant. |
| **IDT** | Backup for Twist failures. gBlocks HiFi when synthesizability fails Twist's predictor (AT-rich or repeat-rich TM regions do this ~10% of the time). All primers for Golden Gate junctions. | gBlocks: 4–6 business days. | ~$70–120/gBlock. Primers negligible. |
| **GenScript** | NOT used for R1–R5. Reserved for Stage 6 GMP-grade lead reconfirmation. | 18–25 business days. | Irrelevant for R1–R5. |
| **Aldevron** | Stage 6 GMP plasmid. Not engaged before W48. | — | — |

**Assembly strategy:** **Golden Gate (BsaI/BsmBI) with a pre-qualified acceptor backbone** holding Gag-Pol + transfer plasmid + BFP reporter. Each variant = one Golden Gate reaction from 3–4 eBlock fragments. In-house, 2-day turnaround from fragment receipt to sequence-verified clone at 96-well scale. Two research associates own this workflow. Cloning success rate target ≥85%; below that triggers fragment re-order.

### Lentiviral Packaging (Tier 1/2 scale only — NOT GMP)
**In-house.** HEK293T/17 transient triple transfection in serum-free Expi293 medium (per Stage 2 mandate). 24-well adherent for Tier 1 (~2 mL supernatant); T75 flask for Tier 2 (~15 mL, concentrated 20× by TFF to ~5×10⁸ particles/mL concentrated). Outsourcing LV packaging at this volume is 3–5× our unit cost and adds 2-week CRO lag per round. No.

### Structural / In Silico (Slow Filter)
**Primary: in-house GPU cluster** (4× A100 nodes, already budgeted). AF3 multimer, ESMFold, FoldX, Rosetta FastRelax + ddg_monomer + InterfaceAnalyzer. **Backup / overflow: Cradle or Charm** on a per-variant basis ($40–80/variant) for round-end surges where in-house queue >48 h. Budget $150K overflow.

### CD34⁺ Cells
| Vendor | Product | Unit size | Lead time | Cost |
|---|---|---|---|---|
| **AllCells** | Healthy mPB CD34⁺ apheresis, G-CSF+plerixafor, cryopreserved | 1–2×10⁸ cells/vial | 3–5 weeks standard; 2 weeks expedited (+30%) | $9–12K/unit |
| **HemaCare (now Charles River)** | SCD patient apheresis (plerixafor-only) for Bridge A | 2–5×10⁷ cells/vial | 8–12 weeks, limited supply | $18–25K/unit |
| **STEMCELL Technologies** | Cord blood CD34⁺ | 1–2×10⁶ cells/vial | 2 weeks | $1.2–1.8K/vial; NOT used in AL loop (per Stage 2 NO-GO); reserved for methods development only |
| **Fred Hutch IRB / HMRC** | MDS BM aspirate CD34⁺ (Bridge A) | Variable | 6–10 weeks (IRB + donor consent) | $3–6K/donor via established collaboration |
| **AllCells** | Aged healthy mPB (>65 y, Bridge A) | 5×10⁷–1×10⁸ | 6–8 weeks, rare | $14–18K/unit |

**Donor pre-commitment:** **Contract AllCells for 18 standard mPB units across W6–W30 on a forward calendar** with 4-week cancellation window. This is critical — mPB donors are booked on a first-come basis and a last-minute 2-week delay blows a round cadence.

### NSG Mice (Bridge F)
**Jackson Laboratory NSG-SGM3** (stock #013062, supports human myeloid engraftment) — 48 mice total, ordered in 3 cohorts of 16 at W24, W26, W28 to match R5 readout. 4-week lead time from Jackson at this volume; pre-book W8. Vivarium: in-house if HSC work is already authorized; otherwise The Jackson Laboratory IVIS or local ABSL-2 CRO (In Vivo Services, Charles River ABSL-2). Budget $350/mouse purchase + $8/day husbandry × 140 days avg × 48 mice = ~$56K husbandry + $17K purchase = **$73K total**, plus flow reagents and IHC.

---

## 4. Primary-Cell Plan — The Rate-Limiter

**Substrate: cryopreserved mobilized peripheral blood CD34⁺ (AllCells) as the Tier 2 AL training substrate. Cord blood is BANNED from the training loop per Stage 2 NO-GO list.** Patient substrates (SCD, MDS, aged) enter at Bridge A only.

**Cells-per-variant math:**
- Tier 2 primary assay: 1×10⁴ CD34⁺/well, 96-well plate format, n=3 wells/donor, 3 donors = **9×10⁴ cells/variant**.
- Top-10 confirmation panel: +2 donors × 3 wells × 1×10⁴ = +6×10⁴/variant, applied to top 10 only.
- Per round: 60 variants × 9×10⁴ + 10 × 6×10⁴ = **6×10⁶ cells + controls/WT reps + bridge spillover ≈ 1×10⁷ cells**.
- **One AllCells mPB unit (1.5×10⁸ CD34⁺) covers ~12 rounds of Tier 2 at that density**, but because of donor rotation rules (no donor in >2 consecutive rounds) and n=3 donors/round, we consume units faster — budget **3 fresh AllCells units per round** × 5 rounds = **15 units**, plus the R0 qualification consuming 3 units, plus 3 bridge-A units (SCD + aged), plus a 2-unit buffer. **Total: ~22 AllCells units + 3 SCD + 3 MDS + 3 aged.**

**QC gates (on every vial before use):**
- Post-thaw viability ≥80% (7-AAD flow).
- CD34⁺ purity ≥92% after 2 h rest.
- Colony-forming assay on a 5% aliquot: CFU-GEMM frequency ≥1/2000 CD34⁺.
- Mycoplasma negative.
- Any vial failing any gate: **returned to AllCells for replacement** (typically honored within 2 weeks).

**Donor batching rule:** a given AL round uses 3 donors, each donor run on the **same producer batch day** as its matched same-donor WT control (per Stage 3 QA Control Mandate §3). Plate maps are locked by the biostats lead W-1 of each round; no last-minute reshuffling.

**Donor panel rotation:** 9 unique donors across R1–R3 (no overlap), 6 additional unique donors across R4–R5 (no overlap with R1–R3). **Total unique healthy-donor identities: 15**, plus 3 SCD, 3 MDS, 3 aged at Bridge A. This is what kills the donor-lottery cheat.

---

## 5. In-Vivo Plan — Bridge F (NSG)

**IACUC submission: W1 (Mon 2026-04-27). Pre-submission consultation with IACUC chair: W0 Friday 2026-04-24.** Anticipated approval window: 6–10 weeks. Approval **required by W10** to protect the W24+ transplant schedule — any slip and the NSG bridge moves out of the campaign window.

**Study design:**
- **Strain:** NSG-SGM3 (NOD.Cg-PrkdcˢᶜⁱᵈIl2rg^tm1Wjl Tg(CMV-IL3,CSF2,KITLG)1Eav/MloySzJ, JAX #013062). Supports myeloid and erythroid reconstitution, which VSV-G-transduced human CD34⁺ typically fails to produce robustly in plain NSG — relevant for the lineage-bias safety term (Stage 3 QA Safety #2).
- **Conditioning:** sublethal busulfan 20 mg/kg IP (age-matched cohorts).
- **Cells/mouse:** 5×10⁵ transduced human mPB CD34⁺ (pooled from 2 donors to reduce donor-specific engraftment variance), injected retro-orbitally or tail-vein.
- **Arms:** 5 candidate variants + 1 WT Rless + 1 VSV-G positive control + 1 untransduced negative = **8 arms × 8 mice = 64 mice.** We budget 48 earlier because not all arms go to secondary; revised to **56 mice** for primary + 24 for secondary = **80 total**. (This is a budget upward revision from Stage 3's ~48; the lineage-bias term and multi-arm positive/negative controls force it. Documented.)
- **Primary readout W46** (16 weeks post-transplant): human CD45⁺ chimerism in peripheral blood, bone marrow, spleen; lineage breakdown (CD3, CD19, CD33, CD71/GPA, CD41); VCN in sorted BFP⁺ bone marrow CD34⁺; integration site profile (Bridge G, top 2 only).
- **Secondary transplant W46–W47:** bone marrow from top 3 primary arms (5 donors → 5 recipients per arm = 15 secondary mice + 5 WT controls = 20 secondary). 16-week readout lands **W62**, outside campaign closeout — that's a Stage 6 deliverable.

**Protocol amendments budgeted** for lineage analysis expansion — file as addendum at W12 to avoid resubmission delay.

---

## 6. Kill Criteria — Go/No-Go at R1, R3, R5

### R1 Gate (W11, Mon 2026-07-06)
**HARD STOP if any TWO of the following:**
- Top variant TXN_G0 fold-change <1.5× WT on donor-normalized Tier 2.
- Top-10 mean F(v) <+0.25 log2.
- FTO gate pass rate across R1 library <40%.
- Tier 1 titer ↔ Tier 2 G0 Spearman ρ outside [−0.2, +0.5].
- Tier 2 CV on WT technical controls >12% donor-normalized.

**SOFT HOLD (one failing):** 4-week diagnostic pause, no R2 library order, root-cause analysis.

**HARD STOP action:** scaffold pivot to **cocal-BaEV RBD chimera** (Stage 1 QA fallback). Campaign restart from R0 with new seed library. **Budget impact: +8 weeks, +$350K.** Decision locked by PI + board within 2 weeks of gate.

### R3 Gate (W20, Mon 2026-09-14)
**HARD STOP if any of:**
- Spearman ρ(healthy-donor fitness ↔ SCD-donor fitness) <0.7 on top 10 AND retraining with bridge-A sample weights at 25% does not rescue to ρ ≥0.7 within 2 weeks.
- Top variant shows >3× titer drop when packaged with 7.5 kb therapeutic-proxy cassette (Bridge B).
- Top 10 rank-inverts (Spearman ρ <0.5) between 21% and 3% O₂ (Bridge C) AND a hypoxia arm cannot be integrated into R4.
- Expi293F producer line (Bridge D): titer drops >3× vs. HEK293T/17 OR complement inactivation >50% in 50% human serum OR N-glycan MS shows Gal-α-1,3-Gal or Neu5Gc motifs.

**HARD STOP action:** redesign is not a rescue — these are structural biology failures. Pivot scaffold OR pivot to reagent-only (non-clinical) business model. Board decision.

### R5 Gate (W30, Mon 2026-11-23) — gating platform PCT conversion and lead nomination
**HARD STOP if any of:**
- No variant achieves **TXN_G0 ≥50% on donor-normalized Tier 2** OR **composite F(v) ≥+2.0 log2** (i.e., ~4× composite improvement).
- Top 5 variants show Ki-67 ratio >1.3× WT in BFP⁺ LT-HSC fraction (activation-biased false winners; Stage 3 QA Safety #1).
- Any top-5 variant shows myeloid:erythroid:lymphoid CFU ratio |log2 fold-change| >1 vs. WT (lineage bias; Safety #2).
- LTC-IC frequency in BFP⁺ fraction <0.6× untransduced same-donor (engraftment-quality gate; Safety #3).
- VCN per cell >2 at MOI 10 across top 5 (FDA safety threshold; Safety #4).
- Bridge G integration site enrichment at LMO2/MDS1-EVI1/HMGA2 hotspots >2× VSV-G baseline.

**HARD STOP action:** do not file lead composition-of-matter; do not transfer to Stage 6. Extend campaign by 1 refinement round with revised fitness weighting. Budget impact: +6 weeks, +$280K, one-shot.

---

## 7. Total Budget

**All-in campaign budget, W1–W52:**

| Line item | Amount | Notes |
|---|---|---|
| **DNA synthesis** (Twist + IDT) | $95K | ~500 variants triaged; eBlocks + ~20 clonal genes for R5 leads. Includes 10% overorder for failed syntheses. |
| **Cloning consumables** (enzymes, competent cells, selection) | $35K | Golden Gate NEB Max, Stbl3 cells, prep kits. |
| **Lentiviral packaging reagents** (transfection, DNase, TFF) | $180K | Serum-free Expi293 medium is the single largest line. |
| **CD34⁺ cells — healthy mPB (AllCells)** | $220K | 22 standard units × ~$10K avg. |
| **CD34⁺ cells — bridges (SCD, MDS, aged)** | $105K | 3 SCD @ $22K + 3 MDS @ $5K + 3 aged @ $16K. |
| **Flow/spectral cytometry reagents** | $190K | 13-color panel, LT-HSC-gated, 60 var × n=3 × 6 rounds. Aurora spectral acquisition time included. |
| **ddPCR + qPCR consumables** | $85K | VCN, titer on HCT116/KG-1a. |
| **CHO-ASCT1/ASCT2 counter-screen lines + maintenance** | $25K | Qualified at R0; maintained thereafter. |
| **Structural compute (cluster depreciation + Cradle/Charm overflow)** | $150K | Slow Filter bucket. |
| **NSG mice + husbandry + readout reagents** | $225K | 80 mice, 1-year vivarium, IHC, LAM-PCR for Bridge G, sequencing. |
| **Bridge A/B/C/D/E/G reagents and compute** (beyond cells already accounted) | $180K | Hypoxia workstation ($85K capex if not available; otherwise $0), Expi293F line qualification, UM171/PGE2 (small molecule), glycan MS, LAM-PCR sequencing. |
| **FTE — 3.0 FTE for 12 months** | $720K | 1 lead scientist ($280K loaded), 1 senior RA ($220K), 1 RA ($220K). Excludes structural biologist (0.3 FTE at $150K/yr loaded = $45K, folded into compute overhead). |
| **Ops / PM / biosafety / IACUC / IBC** (0.3 FTE me + admin) | $90K | — |
| **Patent filings** (3 provisionals + PCT conversion) | $85K | Per Stage 1 §5 schedule; outside counsel. |
| **Contingency (10%)** | $270K | Standard. |
| **TOTAL** | **$2.65M** | 12-month campaign. Does **not** include Stage 6 GMP transfer or secondary NSG continuation beyond W52. |

**Budget vs. Stage 3 prediction:** Stage 3 estimated $2–3M assay + $600–800K bridge = $2.6–3.8M. We land at **$2.65M all-in**, favorably inside the envelope. The FTE line is the swing variable — if the company already has an HSC gene therapy team, the FTE line drops to $0 incremental and campaign comes in at $1.9M.

**Cap on variant synthesis: 500 variants total across R0–R5 (300 Tier 2 + 150 B-list + 50 WT/qualification/reorder).** Any ask above this requires board re-authorization.

---

## 8. What This Plan Cannot Do (Honest Risk Inventory)

- **If mPB apheresis supply chain fails** (AllCells production issue, pandemic-class disruption): campaign stalls. No good mitigation beyond a secondary vendor contract with StemExpress as backup — their supply for mPB is less reliable than AllCells. Tagged as program-level single point of failure.
- **If IACUC takes >10 weeks**: NSG bridge (Bridge F) moves out of campaign window. Mitigation: file draft W-1 with pre-consultation; nothing else we can do.
- **If Stage 3 QA weights were themselves wrong** (objective function still has a loophole we didn't see): we find out at Stage 6 when the lead variant fails in a Vertex PD lab. This plan does not protect against that; Stage 3 QA's job was to close it and mine is to execute what was approved.
- **Secondary NSG endpoint at W62** falls outside the campaign window. Stage 6 inherits it; lead nomination at W52 is conditional on primary 16-week data only.
- **The 5-round compression** (from 6–8 in Stage 3 to 5 here) bets that R3 bridge pass + 2 refinement rounds is enough. If R3 passes marginally, we may wish we had booked R6. The board-approval gate at R5 can extend +1 round (§6 R5 action) but that's a one-shot, not a standing reserve.

---

## 9. Sign-Off Requirements

Before W1 Monday launch:
- **IACUC** draft W0 Thursday, pre-consult W0 Friday, submit W1 Monday.
- **IBC** (BSL-2+ for lentivirus + human primary cells) submit W1 Monday. Institutional turnaround ~4 weeks.
- **Outside patent counsel** engaged W0 Friday, FTO opinion on Généthon family due W4.
- **Board approval** of budget, kill gates, and scaffold-pivot contingency fund ($350K held in reserve): required W0.
- **AllCells forward contract** for 18 mPB units signed W1 Tuesday.
- **Jackson Lab NSG-SGM3 cohort pre-book** (3× 16 mice at W24/W26/W28) signed W2.
- **Twist Enterprise pricing tier** confirmed W1.

---

## 10. Verdict

**Roadmap locked. W1 launch 2026-04-27 is feasible conditional on Section 9 sign-offs by W0 Friday (2026-04-24 EOD).** Budget $2.65M; 5 AL rounds + 3 bridge-gate reviews + NSG primary readout inside 52 weeks; 300 variants in Tier 2, 500 total synthesized; 15 healthy donors + 9 patient donors + 80 NSG mice.

The schedule has two real single points of failure (mPB supply, IACUC) and one structural-biology-dependent kill gate at R3. Everything else is executable. Proceed to Stage 6 on R5 success.
