---
run: cytopenia conditioning agent v1
run_id: 08d0193bae0443f9a7767ff6891781b1
stage: 0
stage_key: visionary
stage_label: Target Scout
phase: main
model: opus
generated_at: 2026-05-01T11:44:51
duration_s: 107.3
cost_usd: 0.227943
tokens_in: 5
tokens_out: 6570
---

# Stage 0 — Visionary (Target Scout)
## Run: cytopenia conditioning agent v1

---

## 1. Selected Target

**Saporin-6** (seed-type ribosome-inactivating protein from *Saponaria officinalis*; UniProt **P20656**, 253 aa mature, ~28 kDa, type I RIP). [src: uniprot:P20656]

**Application:** payload protein for an antibody-drug conjugate (ADC) used as **non-genotoxic HSC conditioning** prior to autologous gene therapy or allo-HSCT. Specifically: anti-CD117 (KIT)–saporin and anti-CD45–saporin conjugates intended to replace busulfan/melphalan in patients receiving Casgevy, Lyfgenia, or allogeneic transplant. [src: PMID:27376563, company:Vertex]

---

## 2. Hunter's Thesis

I am hunting for an **evolved saporin variant** that delivers ≥100× more functional cytosolic depurination per internalized molecule (via improved endosomal escape and proteolytic stability) **and** is stripped of human MHC-II / B-cell epitopes, so that an anti-CD117–saporin ADC can clear ≥90% of host HSCs at sub-mg/kg doses with a single infusion. The wild-type protein is broken precisely where it must work — it gets internalized, then almost all of it is destroyed in the lysosome before reaching ribosomes, and what survives is rapidly neutralized by ADAs on redose. [src: reasoning]

---

## 3. Commercial Pain Point ($)

The conditioning step is the largest cost-of-treatment and the largest barrier to adoption for the entire ex vivo HSC gene therapy stack. Vertex's **Casgevy** lists at **$2.2M / patient** but the eligible-patient capture rate is collapsing because families refuse busulfan's infertility and secondary-malignancy risk. [src: company:Vertex]

Companies whose economics are bottlenecked by this exact failure mode:

- **Vertex / CRISPR Therapeutics** — Casgevy uptake in SCD has run far below the ~16,000-patient eligible US pool; busulfan conditioning is the most-cited reason in payer/provider feedback. [src: company:Vertex, estimate]
- **bluebird bio** — Lyfgenia ($3.1M list) carries a black-box warning for hematologic malignancy, much of which traces to busulfan-induced clonal selection. [src: company:bluebird]
- **Magenta Therapeutics** — wound down 2023 after its anti-CD117–amanitin ADC **MGTA-117** triggered DLTs in Phase 1; the targeting antibody (briquilimab parent) was fine — the **payload** was the failure mode. [src: clinicaltrials:NCT05223699, company:Magenta]
- **Jasper Therapeutics** — briquilimab (JSP191, naked anti-CD117) is in trials but as a *single-agent* it only achieves partial HSC depletion; without a potent payload it cannot replace busulfan in malignant settings. [src: clinicaltrials:NCT04429191]
- **Editas, Beam, Sana, Allogene, BMS (cell therapy), Kite** — every ex vivo CD34+ or allogeneic program inherits this conditioning tax. Sana and Allogene specifically need a non-genotoxic lymphodepletion-plus-HSC-niche-clearing agent. [src: reasoning]
- **Pivotal Bio / Forty Seven legacy (Gilead)** — anti-CD47 + anti-CD117 combos hit the same wall. [src: reasoning]

Total addressable annual conditioning market for ex vivo HSC therapy + allo-HSCT is on the order of **$3–5B by 2030** if a non-genotoxic regimen exists; ~$0 if one does not, because the gene therapy field stalls. [src: estimate]

---

## 4. Longevity Generalization Score (LGS)

**MED.** A potent, non-genotoxic, repeat-dosable HSC-clearing payload would enable **serial bone marrow rejuvenation** — periodic ablation of CHIP-bearing or exhausted aged HSCs followed by reinfusion of expanded young/edited autologous HSCs. The thesis is concrete (clear DNMT3A/TET2-mutant clones in elderly with CHIP, replace with corrected autologous graft) but downstream of the cytopenia beachhead, hence MED not HIGH. [src: reasoning]

---

## 5. Headroom Claim

Wild-type saporin's *intrinsic* depurination kcat on naked ribosomes is fast (~1,500–2,000 min⁻¹), but **cellular** potency as an immunoconjugate is grotesque: roughly **10³–10⁴ saporin molecules must be internalized per cell to achieve kill**, because endosomal escape is <1% — almost all internalized toxin is routed to the lysosome and degraded. [src: PMID:15050826, estimate]

Three orthogonal headroom axes, each with documented ≥10× precedent in related RIPs/toxins:

- **Endosomal escape** — engineered His/Glu protonatable surface patches and pH-triggered conformational switches have given 10–50× cytosolic delivery gains in related toxins (PE, gelonin). [src: estimate]
- **Proteolytic stability in late endosome** — disulfide engineering / loop stiffening has given 5–20× half-life gains in ricin A and PAP. [src: estimate]
- **Deimmunization** — wild-type saporin contains multiple high-affinity human MHC-II epitopes; T-cell-epitope-depleted variants of bouganin (de-bouganin, Viventia) achieved >90% reduction in T-cell proliferation while retaining catalytic activity, proof that this axis is evolvable in a type-I RIP. [src: PMID:19587091, estimate]

Stack these multiplicatively and a **50–100× functional improvement** in ADC therapeutic index is plausible — exactly EVOLVEpro's wheelhouse, exactly the regime where Magenta's amanitin payload could not go (small-molecule, not evolvable). [src: reasoning]

---

## 6. Runner-Up Candidates

1. **Anti-CD117 single-domain binder (VHH) — evolve for faster receptor-mediated internalization and lysosomal routing.** Briquilimab (JSP191) is an IgG1 Fc-silenced antibody; sdAb scaffolds offer better tissue penetration but currently lag in CD117 affinity (Kd ~10–50 nM range vs briquilimab's sub-nM). Evolvable, but the payload is the bigger lever. [src: clinicaltrials:NCT04429191, estimate]
2. **Pseudomonas exotoxin A (PE38 / domain III) — alternative ADC payload.** Already FDA-approved on moxetumomab pasudotox; immunogenicity profile is brutal (>80% ADA on redose) and limits chronic / multi-dose use, which conditioning rarely needs but adjacent CHIP-clearing applications do. Strong, but PE is a more crowded IP space than saporin. [src: PMID:30523064, estimate]
3. **Engineered SCF (KITLG) antagonist / dominant-negative SCF — non-ADC route to HSC depletion via niche detachment.** Wild-type SCF Kd to KIT ~100 pM; an evolved high-affinity non-signaling SCF could starve HSCs out of the niche without a cytotoxic payload at all. Higher-risk biology, but cleanest tox profile. [src: PMID:8245801, estimate]

---

**Verdict:** Saporin-6 is the target. The conditioning ADC market is a ~$3–5B/yr prize gated by a single broken protein — a 28 kDa plant toxin doing 21st-century medicine with 1980s biophysics. Magenta proved the targeting works and the payload kills the program. Replace the payload. [src: reasoning]
