---
run: HSC-cytopenia full pipeline v1
run_id: e7732b5d65be49d79dafbdf7c841f3e9
stage: 6
stage_key: investment_memo
stage_label: Greenlight Memo
phase: qa
model: opus
generated_at: 2026-04-24T11:15:55
duration_s: 72.6
cost_usd: 0.173446
tokens_in: 5
tokens_out: 3286
---

---
run: HSC-cytopenia full pipeline v1
stage: 6
stage_key: greenlight
stage_label: Investment Memo
phase: qa
---

# Stage 6 QA — Managing Partner Verdict on QUIESCO-1

**To:** Investment Committee
**From:** Managing Partner (the one who signs the wire)
**Re:** Greenlight Memo, Project QUIESCO-1
**Date:** 2026-04-24

I have read the memo. I have read the QA trail. I have seen this movie before — four times, actually. Généthon BaEV-TR. Magenta. Graphite Bio. Every envelope-engineering pitch that came through this office between 2018 and 2023. Three of the four are dead or zombie. One is a line item in Miltenyi's reagent catalog.

Let me work the checklist.

---

## 1. The "So What?" Test — **PASS the kill condition**

TAM is real and not crowded *at the reagent layer*. bluebird, Vertex/CRISPR, Orchard-Kyowa, Rocket, 2seventy, Beam, Editas, Sana, Ensoma — all of them have the same $400–600K/dose vector+transduction line item on their COGS slide, and none of them have solved G0 transduction. The addressable B2B reagent pull-through at $8–12B ex vivo by 2032 + $5–15B in vivo optionality is not a fiction; the Casgevy 4–6 week vein-to-vein timeline alone is a $500M/yr line item Vertex would pay to erase.

Competitor census is honest: Généthon/Lentigen own the incumbent (BaEV-TR), Sana is a different bet (paramyxo fusogens on a less mature receptor), Magenta is a graveyard, academic cocal/RDTR labs have no ML loop. **Reagent-layer competition is not crowded. Clinical-stage competition is irrelevant because we're not going clinical.** Test passes.

## 2. The "Team/Ops" Doubt — **PASS, but barely**

Stage 5 QA verdict was `REVISE TIMELINE` and the team *did* substantively address it: +$110K bioprocess FTE, 5-week round cadence (W34 → W57 lead nomination), IBC pre-submit W0 Friday, SCD+MDS+aged cells ordered at W1 not W12, JAX NSG-SGM3 6–10 week lead-time corrected (not 4), $220K vivarium/CRO contingency. These are the right fixes, on the right line items.

My residual concern: a 5-week cadence for cloning + packaging + primary G0 CD34⁺ readout on 60 Tier 2 variants/round with 1.5 bioprocess FTEs is still tight. The first round will slip. I'm willing to price that in because the R1 kill gate (W11, 1.5× WT on G0) is cheap to reach and the budget has bioprocess slack now that it didn't before. Not a PASS.

## 3. The "Sunk Cost" Trap — **Risk register is honest, not bloated**

Three risks called, three concrete mitigations, each tied to a specific stage-QA correction with a line item. **Ki-67 penalty from R1 not R5** (Stage 3 QA fix), **M_FTO binary gate from R1** (Stage 4 fix), **JAX lead-time correction** (Stage 5 fix). I count zero unmitigated "High" risks as of this memo. The sunk-cost red flag would be if the team buried a High risk as a footnote; they didn't.

## 4. The "Regulatory" Test — **The strongest single argument for FUND**

This is the point at which 80% of HSC pitches die on my desk, and it is the point at which QUIESCO-1 is strongest. **This is not an IND.** It is a **GMP reagent sold to people who already have INDs.** No genotox package on the reagent itself, no biodistribution (it doesn't circulate in a patient), no insertional mutagenesis IND from us — *the integration safety panel in the Stage 3 gate is a reagent-quality assertion that derisks our customers' IND, not ours.*

Regulatory path is reagent-master-file + drop-in substitution into customer IND amendments. 6–12 months, not 36. If the team can hold the B2B reagent model and resist the temptation to build their own clinical asset on top, the regulatory risk profile is closer to a Miltenyi product launch than an HSC gene therapy. **This is the test that flips my prior from No to Yes.**

## 5. The "Better Alternative" Test — **No derisked modality exists**

Small molecules to transduce G0 HSCs? None. The closest adjacents are cyclosporin H (CsH, IFITM3 inhibition) and prostaglandin E2 / Staurosporine / rapamycin cocktails — all are **cofactors** that boost existing envelopes by 1.5–3×, not replacements. Approved biologics? None. Alternative viral systems — AAV6 (electroporation-gated, payload-limited), foamy (no commercial packaging ecosystem), non-integrating lenti (wrong modality for SCD/β-thal). **There is no shortcut. Directed evolution of the envelope is the path.**

---

## The Vote

# `YES — RELEASE FUNDS`

## The One Thing

**The regulatory profile is reagent, not drug.** A 50–100× improvement on G0 CD34⁺ transduction sold as GMP vector to every company on the Lyfgenia/Zynteglo/Casgevy/Lenmeldy list derisks *their* INDs and ships as a master-file reagent — no genotox/biodistribution/insertional mutagenesis IND package for us, no 36-month preclinical death march, no clinical-stage competitors because we are not in the clinic. Combined with (a) a real ML-loop advantage over empirical incumbents who still train on HEK293, (b) a designed FTO escape via ≥12 non-conservative SU/TM substitutions outside R-peptide, (c) a credible 30× step-up at a W34 R5 inflection, this is the rare HSC pitch where the cell-therapy tailwinds accrue to us without the cell-therapy regulatory anchor.

## Conditions (Blocking, Pre-Wire)

All conditions must be signed in writing by **W0 Friday EOD (2026-04-24 COB)** or the wire does not clear Monday.

1. **Outside-counsel FTO opinion in hand by W4** (not "due W4"). The Stage 1 QA HARD-STOP → CAUTION remediation is contingent on this. No opinion, no R1 synthesis.
2. **B2B reagent charter locked.** No clinical asset, no co-development, no internal IND ambitions for 36 months. Founders sign a board resolution. The instant this becomes a cell-therapy company it becomes a Graphite/Magenta-shaped hole in the portfolio.
3. **Donor batch-matching and lot-tracking SOP** for Tier 2 readouts — same n=3–5 mPB donors across R1→R5 where biologically feasible, with a pre-registered substitution protocol. Donor lottery is how this assay dies quietly.
4. **R1 kill gate is hard, not soft.** If W11 Tier 2 lead does not hit ≥1.5× WT on donor-normalized G0 CD34⁺CD38⁻CD45RA⁻CD90⁺CD49f⁺ with Ki-67 penalty applied and M_FTO gate satisfied, the program terminates and the remaining ~$2.4M returns to the fund. No "one more round." No pivot to cord blood. No HEK293 rescue run.
5. **R3 Bridge (W23) requires LTC-IC ≥0.6× untransduced, VCN ≤2, clean lineage-bias CFU, AND cross-substrate ρ ≥0.7 across healthy/SCD/MDS/aged.** Any one miss forces a committee review before R4 synthesis spend.
6. **Priority-1 provisionals filed by W8 (2026-06-22)** covering (i) Markush on SU RBD + TM fusion-peptide, (ii) ML-guided DE method against G0-HSC fitness function, (iii) producer-detoxified envelope composition. Receipt of filed provisionals to the board.
7. **$350K scaffold-pivot reserve pre-authorized** but ring-fenced — only releasable to an RD114-TR fallback if the Généthon FTO opinion comes back adverse at W4, not as a general slush fund.
8. **Expi293F GMP-line compatibility confirmed by R5**, not assumed. If producer titer only holds in research-grade Expi293, the reagent thesis breaks.

## Longevity Note

**LGS MED justifies a 12-month follow-on option, not a companion bet today.** Bridge A carrying aged (>65 y) donors at R3 costs us nothing incremental and preserves a free call on a CHIP-clone-correcting base-editor delivery asset; if the W34 R5 variant dominates on aged substrate with ρ ≥0.7 to young G0, we write a follow-on term sheet at Series A for a dedicated aged-HSC gene therapy program. Do not fund the longevity asset today. Do not let the founders pitch it to the next round's lead investor as part of the QUIESCO-1 story — it dilutes the reagent narrative that is the entire reason this passes committee.

---

**Signed.** Release $2.98M on satisfaction of Conditions 1–8 by W0 Friday EOD. Gate hard at W11, W23, W34. I want a one-page written update after every gate, not a deck.
