---
run: HSC-cytopenia full pipeline v1
run_id: e7732b5d65be49d79dafbdf7c841f3e9
stage: 6
stage_key: investment_memo
stage_label: Greenlight Memo
phase: main
model: opus
generated_at: 2026-04-24T11:14:43
duration_s: 114.9
cost_usd: 0.8285067500000001
tokens_in: 5
tokens_out: 5437
---

---
run: HSC-cytopenia full pipeline v1
stage: 6
stage_key: greenlight
stage_label: Investment Memo
phase: main
---

# Greenlight Memo — Project QUIESCO-1

**To:** Investment Committee
**From:** Biotech Venture Partner / Portfolio Manager
**Date:** 2026-04-24
**Asset class:** Platform + lead reagent (HSC gene therapy delivery)
**Stage:** Pre-seed → Seed bridge

---

## 1. The "Hair-on-Fire" Problem

Every ex vivo HSC gene therapy program on the planet is bleeding margin on the **transduction step**. The bottleneck: no viral envelope transduces quiescent (G0) CD34⁺CD38⁻CD90⁺CD49f⁺ HSCs at clinically useful efficiency without 48–72 h of cytokine prestim that torches long-term repopulating activity.

**Dollar pain, named P&Ls:**
- **bluebird Lyfgenia ($3.1M list, SCD)** and **Zynteglo ($2.8M, β-thal)** — GMP COGS ~$1.5M/dose, ~$400–600K of which is vector + transduction. bluebird's viability depends on this line item.
- **Vertex/CRISPR Casgevy ($2.2M)** — forced into electroporation+AAV6 because lenti of true HSCs is unreliable; 4–6 week vein-to-vein. A G0-competent envelope collapses the timeline and reopens lenti-delivered base/prime editor economics.
- **Orchard/Kyowa Kirin Lenmeldy ($4.25M), Skysona** — same bottleneck, same pipeline attrition (MPS-IIIA, FA).
- **Sana, Ensoma** — the $5–15B **in vivo HSC-GT** optionality is entirely envelope-gated.

**Addressable market captured by fixing this one protein:** $8–12B ex vivo by 2032 + $5–15B in vivo optionality. **Whose P&L we fix:** Vertex, 2seventy, Orchard-Kyowa, Rocket, Editas, Beam, Prime, Sana. Every one of them has an internal slide with "transduction efficiency" as a top-3 risk.

**Our wedge into their P&L:** B2B reagent — sell a 50–100× better envelope as GMP-grade vector. $300K–$1M/dose COGS reduction at industry volume is a ~$500M/yr line item by 2030.

---

## 2. The "Unfair Advantage"

Competitors (Généthon/Cosset/Verhoeyen, Lentigen, Sana fusogens, academic cocal/RDTR labs) optimize empirically — single mutations, small panels, no ML loop, and — critically — **they train on HEK293T or HCT116 indicator cells, not primary G0 CD34⁺.** They have been mining an 11%-ASCT2-expressing surrogate for 12 years.

**We win on four moves none of them combine:**
1. **Fitness function trained on the actual substrate.** Donor-normalized %BFP⁺ *and* absolute count in LT-HSC gate (CD45RA⁻CD49f⁺), n=3–5 mPB donors, serum-free Expi293 producers, 4 h single-cytokine prestim. No HEK293 surrogate, no cord blood, no fresh cells.
2. **EVOLVEpro-class multi-objective AL loop** weighted 0.35/0.30/0.20/0.10 across G0 transduction, producer titer, producer viability, and thermostability — with Ki-67 activation penalty, tightened VCN ≤2 cap, lineage-bias and LTC-IC gates at R3. Hostile-optimizer-proofed at Stage 3 QA.
3. **Chemical filter calibrated for a Class I viral fusion protein** — 5 fast-filter heuristics + AF3/FoldX/Rosetta slow filter with explicit MPER engineering carve-out (where producer-detox winners live), 10% B-list measuring filter false-positive rate every round.
4. **FTO-aware design.** Every variant carries ≥12 non-conservative SU/TM substitutions with ≥4 in high-information residues — engineered to escape the Généthon 80%-identity genus claim by construction.

**Specific competitors we displace:**
- **Généthon / Lentigen-Miltenyi** — own BaEV-TR today; still empirical. Our variants dominate by design and dodge their claims.
- **Sana Biotechnology** — paramyxo fusogens are a different bet on a less mature receptor biology.
- **Magenta Therapeutics (wound down 2023)** — already a cautionary tale on conditioning; we fix the upstream step.
- **ExCellThera, Garuda, Ossium** — HSC expansion plays, adjacent not competing.
- **Academic cocal/RDTR labs (Trobridge, MolMed residual)** — smaller headroom, no ML loop.

---

## 3. The "Defensibility"

**FTO status (verbatim, Stage 1 QA):** `HARD STOP — LEGAL REVIEW REQUIRED` in the as-written Stage 1 memo; remediated to **`CAUTION (License Needed) — path to CLEAR by Stage 3`** conditional on (a) full PAIR/Espacenet pull on Généthon/Verhoeyen/Cosset family including continuations through 2025, (b) pending-application census on Sana, 2seventy, Rocket, Ensoma, Broad, Dyno, Generate, Profluent, (c) method-of-use claim chart, (d) platform-tool FTO vs. ML-protein-design incumbents, (e) receptor-switch optionality analysis, (f) DoE audit on design-around language. Outside-counsel opinion due W4.

**The honest read:** the Généthon 80%-identity + "modified cytoplasmic tail" + ASCT2-binding genus claim is the real threat. Our ≥12 non-conservative SU/TM substitution gate + ASCT1-breadth gate are the designed escape hatches. **ASCT1 breadth is the receptor-switch hedge** if the ASCT2 functional tether bites.

**Filable platform claims (Priority 1 provisionals by W8, 2026-06-22):**
1. Engineered retroviral envelopes with enhanced quiescent-HSC transduction (Markush on SU RBD + TM fusion-peptide positions).
2. ML-guided directed-evolution method for viral envelopes against a G0-HSC fitness function — thin, but real.
3. Producer-detoxified retroviral envelopes (cross-family composition claim).

**Earliest defensible priority date:** **2026-06-22** (provisional). PCT conversion by W30 bundling R5 data.

---

## 4. The "Execution Alpha"

**Budget (revised, post Stage 5 QA):** **$2.98M all-in** over **~14 months** (W1 2026-04-27 → W57 ~2027-05-28 lead nomination). Inside the Stage 3 envelope, corrected for bioprocess FTE, 5-week round cadence, IBC realism, patient-cell lead times, vivarium confirmation.

**Round cadence:** 5 AL rounds @ 60 Tier 2 variants/round + 15 B-list; 15 healthy donors + 3 SCD + 3 MDS + 3 aged + 80 NSG-SGM3. Three hard gates: **R1 (W11)**, **R3 Bridge (W23)**, **R5 (W34)**.

**Proof-of-Concept milestone (W11, R1 kill gate):** top variant ≥1.5× WT on G0 CD34⁺CD38⁻CD45RA⁻CD90⁺CD49f⁺ transduction on donor-normalized Tier 2. Takes asset from seed-stage "platform claim" to **Series A-credible $15–25M post.**

**Value Inflection Milestone (W34, R5 gate):** **A variant hitting ≥50% G0 transduction at MOI ≤10 with ≥1×10⁸ TU/mL raw producer titer, clean Ki-67, VCN ≤2, LTC-IC ≥0.6× untransduced, no LMO2/MDS1-EVI1/HMGA2 integration bias, and ≥12 non-conservative SU/TM substitutions outside R-peptide.** That single data package — composition-of-matter provisional + R3 bridge validation on SCD + MDS + aged donors + Expi293F GMP-line compatibility — takes the asset from **~$3M pre-money seed to $80–150M Series A** on a strategic-led round (Vertex, 2seventy, Orchard-Kyowa, or a pure-platform lead like Arch/Flagship). **10–50× step-up.** NSG primary readout at W50 and secondary at W67 are Stage 6 inheritance that underwrites the Series B, not the inflection itself.

---

## 5. Longevity Optionality

**LGS: MED** (Stage 0 confirmed, Stage 0 QA confirmed). The envelope is a delivery rail, not a rejuvenation agent — but it is **the** rail into aged HSCs. Bridge A explicitly includes aged (>65 y) donors, preserving the option without diluting the beachhead.

**Pivot thesis, ≤5 lines:** Aged HSCs exhibit 3–10× lower ASCT2 surface density and reduced cycling — the same quiescence axis that makes our envelope win on young G0 cells. Variants that dominate on aged-donor CD34⁺ (Bridge A) become the delivery vehicle for CHIP-clone-correcting editors (TET2/DNMT3A base editors) and rejuvenation factors (Lin28b, Sirt3, Ezh2 modulators) in a **second-round aged-HSC gene therapy asset** for clonal hematopoiesis and immune aging. One envelope, two value-creation cycles.

---

## Greenlight Memo — Deliverables

**1. Project Code Name:** **QUIESCO-1**

**2. The Ask:** **$2.98M** for a **14-month, 5-round ML-guided directed evolution campaign + R3 bridge validation on SCD/MDS/aged donors + primary NSG-SGM3 readout + 3 provisional filings by W8 and PCT by W30.**

**3. Value Inflection Milestone:** **R5 lead variant (W34, ~March 2027)** meeting ≥50% G0 CD34⁺ transduction at MOI ≤10, ≥1×10⁸ TU/mL producer titer, VCN ≤2, clean Ki-67/LTC-IC/lineage/integration safety panel, and ≥12 non-conservative SU/TM substitutions outside R-peptide + Bridge-A cross-substrate correlation ρ ≥0.7 + Expi293F GMP-line compatibility. **Step-up: $3M pre-money seed → $80–150M Series A post.** ~30× expected.

**4. Risk Register**

| Category | Top Risk | Concrete Mitigation |
|---|---|---|
| **Technical** | Fitness function rewards G0→G1 activators (Ki-67 cheat) or surrogate-killer variants; AI converges on Graphite-class engraftment-losers by R4. | Ki-67 penalty (−0.25 · log2 ratio) and **min(%BFP⁺, absolute BFP⁺ count)** in primary scalar **from R1, not R5** (Stage 3 QA). LTC-IC binary gate at R3; VCN ≤2 hard cap; lineage CFU ratio at R3; expanded NSG (top 5, n=8/arm) at R5. |
| **Legal** | Généthon/Verhoeyen/Cosset genus claim (≥80% identity + modified tail + ASCT2 binding) catches our variants via doctrine of equivalents; method-of-use claims on the transduction step expose us to §271(b)/(c) inducement on reagent sales. | Outside litigator-grade FTO opinion by W4 (non-negotiable); M_FTO binary gate forcing ≥12 non-cons SU/TM substitutions outside R-peptide with ≥4 in high-info residues **from R1** (Stage 4); ASCT1-breadth gate preserving receptor-switch pivot; Priority-1 provisionals by W8; RD114-TR fallback scaffold cultivated in parallel low-cost track. |
| **Operational** | Bioprocess bandwidth collapse at R2 (cloning + packaging + Tier 2 readout on 2 RAs); IBC novel-env review >8 weeks; SCD/MDS patient cells 10–16 week lead time; NSG-SGM3 strain 6–10 week lead (not 4); vivarium capacity unconfirmed. | +0.5–1.0 bioprocess FTE (+$110K); 5-week round cadence (end W57); IBC pre-submit W0 Friday; SCD+MDS+aged orders at W1 not W12; JAX pre-book W2 with corrected 6–10 week lead-time; vivarium allocation confirmed in writing by W2 or CRO contract locked (+$220K contingency already in revised budget). |

**5. Longevity Pivot Thesis (≤5 lines):**
Aged HSCs downregulate ASCT2 ~3–10× and shift toward deeper quiescence — the **same axis** our envelope is being selected against. Bridge A explicitly tests top variants on aged healthy (>65 y) CD34⁺. A variant dominating on aged substrate becomes the delivery vehicle for CHIP-clone base-editing payloads (TET2, DNMT3A, ASXL1) and rejuvenation cargos (Lin28b, Sirt3) in a second-round longevity asset targeting clonal hematopoiesis and immune aging. **LGS MED; one envelope, two value cycles.**

**6. Final Recommendation: `FUND`.**

The pipeline surfaced exactly the failure modes that kill HSC gene therapy programs — cycling cheat, donor lottery, HEK293 surrogate, Généthon genus claim, bioprocess overload, IBC/IACUC slippage, NSG lead time. **Every one of them was identified and mitigated before W1.** The Stage 1 QA escalated from `CAUTION` to `HARD STOP`; Stage 3 QA escalated from `accept` to `REVISE OBJECTIVE FUNCTION`; Stage 5 QA escalated from `approve` to `REVISE TIMELINE`. Each escalation produced concrete, costed fixes that are now baked into the plan at $2.98M and W57.

The target has documented 50–100× compound headroom on four partially independent axes. The incumbent (Généthon empirical optimization) has not moved the number in a decade. The $8–23B TAM is gated by one protein, and no other well-funded competitor is running an ML-guided deep-mutational scan on it. The B2B reagent model sidesteps the product-level royalty stack if FTO clears, and preserves sublicensing optionality if it doesn't. Risk-adjusted rNPV at the R5 inflection (~30× step-up, P(success) ~25% at R1 conditional on clean baseline, rising to ~55% post-R3 bridge) returns an expected ~8× on the $2.98M ask in ~14 months.

**FUND. Gate hard at R1 (W11), R3 Bridge (W23), R5 (W34). Pre-authorize $350K scaffold-pivot reserve. Do not release W1 launch until the 5 blocking Stage 5 QA corrections and the Stage 1 QA FTO checklist items are signed in writing by W0 Friday EOD.**
