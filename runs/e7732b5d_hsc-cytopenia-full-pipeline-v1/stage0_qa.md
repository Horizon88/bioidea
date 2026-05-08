---
run: HSC-cytopenia full pipeline v1
run_id: e7732b5d65be49d79dafbdf7c841f3e9
stage: 0
stage_key: visionary
stage_label: Target Scout
phase: qa
model: opus
generated_at: 2026-04-22T19:03:56
duration_s: 71.3
cost_usd: 0.17304049999999999
tokens_in: 5
tokens_out: 3686
---

# Stage 0 QA — Target Viability Audit

**Run:** HSC-cytopenia full pipeline v1
**Date:** 2026-04-22
**Auditor:** Red Team Lead — Target Viability
**Subject:** Stage 0 Scout recommendation — BaEV-Rless envelope glycoprotein

---

## 1. Audit Decision

**ADVANCE CANDIDATE: BaEV-Rless (Baboon Endogenous Retrovirus envelope, cytoplasmic-tail-truncated form; parent UniProt Q9WJT4).**

Conditional on the Stage 1 FTO gauntlet clearing the Lentigen/Généthon/MolMed patent thicket around BaEV-TR pseudotyping (flagged below). This is the right target. The Scout's thesis survives adversarial review.

---

## 2. Selected Candidate Details

### Protein
**BaEV-Rless / BaEV-TR envelope glycoprotein** — tail-truncated *Papio cynocephalus* endogenous retrovirus M7 Env, receptor pair **ASCT1 (SLC1A4) / ASCT2 (SLC1A5)**.

### Survival rationale — criterion by criterion

**(1) Saturation Check — PASS.**
Wild-type BaEV-Rless transduces quiescent CD34+CD38−CD90+ HSCs at **10–20%** (Bernadin 2019; Girard-Gagnepain 2014). Producer titers are **5×10⁶–3×10⁷ TU/mL raw**, roughly 10–30× below VSV-G. Producer viability at 48 h post-transfection is ~30–60%. None of these numbers are anywhere near saturation. A 50% G0-HSC transduction target sits cleanly in the fitness-landscape interior, not at the ceiling — which is also important for EVOLVEpro-class selection to stay informative rather than collapsing into a binary hit/miss assay.

**(2) Assay Check — PASS, with one mandated discipline.**
The relevant primary readouts are quantitative and low-CV when done correctly:
- Producer titer by qPCR on transduced HCT116 or by p24 ELISA — CV 10–15%.
- Transduction efficiency on primary CD34+CD38−CD90+ by flow + reporter (GFP or BFP) — CV 8–12% within a donor.
- VCN by ddPCR on bulk or single-cell — CV <10%.
- Producer syncytia / cytotoxicity by imaging + viability — CV 10–15%.

**Red team mandate:** the "long-term repopulating HSC" phenotype is NOT a training-loop assay — NSG engraftment has CV 25–40% and 16-week readout. Train on G0 transduction + VCN in sorted CD34+CD38−CD90+ as the primary fitness signal; reserve NSG serial transplant for top-N validation only. If the Scout team tries to use NSG engraftment as an inner-loop fitness function, the campaign dies. Lock this in before Stage 2.

**(3) Domain Check — PASS.**
BaEV is the *de facto* envelope for primitive-HSC lentiviral delivery. Every serious HSC gene therapy program (SCD, β-thal, MLD, WAS, Fanconi, ADA-SCID) and every in vivo HSC-lenti program (Sana fusogens, Ensoma's HDAd pivot notwithstanding) either uses or has tried BaEV-class envelopes. Not a forced fit — it is the definitional bottleneck of the field.

**(4) Headroom Check — PASS.**
Four independent axes of documented under-engineering:
- **Producer titer:** 10–30× to reach VSV-G parity; the R-less truncation already proved a single crude edit yields ~10× — the surface is responsive.
- **G0 HSC transduction:** 3–5× to reach ≥50%.
- **Producer cytopathicity:** qualitatively massive — envelope detoxification precedents (HIV Env SOSIP, RSV F DS-Cav1, MeV-H stabilization) routinely achieve it with <10 mutations.
- **Serum/thermostability post-concentration:** 3–10× demonstrated precedent in VSV-G and cocal engineering.

Compounded fitness improvement ceiling (titer × G0 efficiency × producer viability) is comfortably in the 50–100× range. Crucially, *each axis has precedent in homologous viral envelopes*, so this is not a single high-risk bet — it is four partially-independent shots, each with literature support.

**(5) Competition Check — CROWDED, BUT EXPLOITABLE.**
Flag, not kill:
- **Généthon / Anne Galy / Els Verhoeyen (Lyon)** — the original Rless/TR patents and the ongoing academic lead. They optimize empirically, not via directed evolution.
- **Lentigen / Miltenyi** — GMP BaEV-TR vector manufacturing; tied up in the academic licensing chain.
- **Sana Biotechnology** — fusogen engineering, but their focus is HERV-W / paramyxo-derived fusogens for in vivo delivery, not BaEV optimization per se.
- **Cellectis, Flash Therapeutics, Vectalys (Fr)** — incremental BaEV producer line work.
- **2seventy bio / Vertex** — known to have evaluated BaEV but have not, to our knowledge, launched a dedicated directed-evolution campaign.

**No disclosed well-funded program is running a deep-mutational-scan + ML-guided campaign on BaEV Env for quiescent-HSC transduction.** The closest analog is Sana's fusogen work on *different* envelopes. The whitespace is real but narrowing — Stage 1 FTO must confirm we can operate around the Généthon patent family on the R-less truncation itself (likely fine if we mutate SU/TM substantially, not fine if we ship only the tail truncation).

### HSC/cytopenia application unlocked
A BaEV-Rless variant hitting the Hunter's Thesis spec (≥50% G0 CD34+CD38−CD90+ transduction at MOI ≤10, ≥1×10⁸ TU/mL, <10% producer syncytia) unlocks, in order of commercial velocity:
1. **COGS collapse on autologous HSC-GT** (Lyfgenia, Zynteglo, Lenmeldy, Skysona successors) — $300K–$1M/dose saved, 4–6 week → <1 week vein-to-vein.
2. **Lenti-delivered base/prime editors into quiescent HSCs** — breaking the AAV6/electroporation monopoly that Casgevy-class programs depend on.
3. **In vivo HSC gene therapy** via CD117/CD90-retargeted BaEV particles — the $5–15B optionality tier.
4. **Rare inherited BMF programs** (Fanconi, DBA, SDS) that are currently uneconomic under bluebird/Orchard COGS structures.

### LGS re-assessment
**MED.** Confirmed at Scout's level. The envelope is a delivery rail, not a rejuvenation agent; its longevity value is entirely derivative of what payload you ship into aged HSCs (CHIP-clone editors, Lin28b, Sirt3, etc.). Do not upgrade to HIGH — that would require a specific aged-HSC tropism hypothesis (e.g., preferential transduction of myeloid-biased aged LT-HSCs), which the Scout did not make and which is not load-bearing for the beachhead.

---

## 3. Rejected Candidates

**Cocal envelope glycoprotein G (Vesiculovirus cocal).**
**REJECTED — Kill Criterion 4 (Headroom).** Cocal is already 60–80% of the way to VSV-G on titer and only marginally better on true G0 HSCs (~1.5–2×). The improvement ceiling on the axis we actually care about (quiescent-HSC transduction without prestim) is at most 2–3×, well short of the 10× bar. Worth a parallel benchmarking arm; not the lead target.

**Thrombopoietin (TPO, P40225) engineered variants for HSC expansion.**
**REJECTED — Kill Criterion 5 (Competition) + Kill Criterion 1 (partial saturation on platelet axis).** UM171, SR1, ExCellThera OM-LV01, and the Garcia-Prat/Sauvageau axis have mined the HSC-expansion small-molecule/cytokine combinatorial space deeply. The remaining headroom on HSC self-renewal from a better TPO is modest relative to cocktail-level gains, and IP whitespace on engineered cytokines is narrow and heavily litigated (Amgen/Kirin/ExCellThera). Weak moat.

**Anti-CD117 ADC / briquilimab-class conditioning binders.**
**REJECTED — Kill Criterion 4 (Headroom on an evolvable axis).** Magenta MGTA-117 failed on payload/linker biology, not on binder affinity; Jasper briquilimab is already in reasonable depletion range. The "broken" surface is the ADC chemistry and patient-pharmacology, not a single protein with a clean directed-evolution fitness screen. Different engineering problem, wrong tool.

---

## 4. Immediate Next Step

**Proceed to Stage 1: FTO Gauntlet for deep IP analysis.**

Stage 1 must specifically resolve, before any wet-lab spend:
- Scope of the **Généthon / Verhoeyen / Cosset** BaEV-TR / R-less family (priority dates, claim breadth on the tail truncation vs. SU/TM mutations, national phase status).
- Lentigen/Miltenyi GMP manufacturing licenses and whether they encumber non-clinical research use.
- Any Sana/2seventy/Vertex filings referencing BaEV, ASCT2-targeted pseudotypes, or CD90/CD117-retargeted envelopes post-2022.
- Freedom to operate on ASCT2-receptor-binding-domain mutagenesis specifically (less likely to be claimed than the tail truncation).

If Stage 1 returns a clean FTO window on SU/TM mutagenesis + novel producer-detoxifying mutations, proceed to Stage 2 assay design. If the Généthon claims read onto any R-less construct regardless of downstream mutations, the campaign must pivot to a **cocal-BaEV RBD chimera** or a **RD114-TR** backbone as the scaffold — a real but manageable pivot.

**Do not burn a single CD34+ donor sample until FTO is signed off.**
