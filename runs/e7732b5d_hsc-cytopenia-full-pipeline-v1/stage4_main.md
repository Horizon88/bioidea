---
run: HSC-cytopenia full pipeline v1
run_id: e7732b5d65be49d79dafbdf7c841f3e9
stage: 4
stage_key: chemical_logic
stage_label: Chemical Filter
phase: main
model: opus
generated_at: 2026-04-22T19:47:45
duration_s: 195.1
cost_usd: 0.7367412499999999
tokens_in: 5
tokens_out: 11465
---

---
run: HSC-cytopenia full pipeline v1
stage: 4
stage_key: chem_filter
stage_label: Chemical Logic Filter & Validation Protocol
phase: main
---

# Stage 4 — Mutation Filtering Protocol: Project QUIESCO-1

**Run:** HSC-cytopenia full pipeline v1
**Date:** 2026-04-22
**Author:** Senior Computational Chemist
**Subject:** Fast-and-slow filter stack for BaEV-Rless envelope variants before they consume Tier 1 producer runs or Tier 2 CD34⁺ apheresis product.

---

## 0. Bottom Line

The AI will propose ~3,000 variants per round pre-triage. At a Tier 1 unit cost of ~$200/variant and Tier 2 cost of ~$1,800/variant (plus irreplaceable mPB apheresis allocation), **every chemically nonsensical variant that reaches wet-lab is a direct tax on the campaign budget and a theft of donor cells.** The objective of this filter is to reduce the AI's raw output by ~70% **without removing non-intuitive winners** — including the bulky, charge-switched, or structurally surprising variants that have historically dominated the top of EVOLVEpro-class campaigns (the T7 RNAP paper's top hit was an E→K in a solvent-accessible loop, which a naive filter would have killed).

The filter below is structured as a **two-stage sieve** (fast AI heuristics, then slow structural validation) with a **10% B-list escape hatch** so we measure our own false-positive rate every round. All thresholds are numeric, defensible, and target-specific to a Class I viral fusion protein binding a neutral amino acid transporter.

---

## 1. The BaEV Envelope Structural Landscape (what the filter must respect)

Before I write heuristic thresholds, the filter must encode what is actually sensitive on this protein. Summary of the structural map QUIESCO-1 operates against:

| Region (approximate residue numbering, BaEV Env Q9WJT4) | Function | Mutational sensitivity |
|---|---|---|
| Signal peptide (~1–30) | Secretion | Do not touch |
| SU N-terminal receptor-binding domain, RBD (~30–210) | ASCT2/ASCT1 contact surface; ~6 residues form the primary receptor interface per AlphaFold3 prediction vs. SLC1A5 ectodomain | **Hot — intentional engineering zone**, but with interface-distance checks |
| SU proline-rich region / VRA-VRB linker (~210–260) | Flexibility between RBD and C-terminal SU | Moderately tolerant |
| SU C-terminal domain (~260–390) | Trimer interface, furin cleavage site presentation | Conserved — disulfides, interface residues |
| Furin cleavage site (R|X|K|R near residue ~390) | Essential maturation | **Never mutate** |
| TM fusion peptide (~395–420) | Membrane insertion; amphipathic | Responsive to engineering but small changes can abolish fusion |
| TM heptad repeat 1 (HR1, ~420–470) | Six-helix bundle core | Highly sensitive to register-breaking mutations |
| TM heptad repeat 2 (HR2, ~520–570) | Six-helix bundle core | Same |
| Membrane-proximal external region (MPER, ~570–600) | Lipid-proximal stability; complement epitopes | Engineering hot-spot for producer detoxification |
| Transmembrane helix (~600–625) | Membrane anchor | Do not disrupt helix register |
| Cytoplasmic tail / R-peptide (~625–end) | R-peptide cleavage regulates fusion; Rless truncation lives here | **FTO-forbidden zone per Stage 1 QA** — no literal Rless motif; substitutions OK but bounded |
| N-linked glycan sites (~11 predicted NxS/T) | Shield immunogenic epitopes; receptor-access gating; complement evasion | Any change requires structural review |
| Disulfide bonds (~8 predicted Cys pairs in SU-TM) | Fold integrity | **Never remove without documented compensation** |

Every heuristic below maps to one of these regions.

---

## 2. The AI "Fast Filter" — Five Hard-Veto Heuristics

These rules run **inside the ML sampler**, before a variant is added to the Tier 1 queue. They are cheap, deterministic, and conservative. Each rule includes a numeric threshold and an explicit carve-out for the cases where the rule would destroy a real winner.

### Heuristic 1 — **Core Hydrophobic Pocket Charge Reversal (HARD VETO)**

**Rule:** Reject any substitution that places a formally charged residue (D, E, R, K, H) at a position where:
- (a) the WT residue is hydrophobic (A, V, L, I, M, F, W, Y, C);
- (b) relative solvent accessibility (RSA) < 20% in the WT AlphaFold3 model;
- (c) the position is within a high-information region (RBD contact, HR1, HR2, fusion peptide, TM helix).

**Numeric threshold:** RSA < 20% *and* side-chain polarity change magnitude > 1.5 on the Kyte-Doolittle scale.

**Rationale:** Burying a charge desolvates the backbone and costs 3–6 kcal/mol of folding stability per unpaired charge. This is the T7 RNAP-class failure where a single charge reversal near the active site abolishes all activity.

**Carve-out:** If the AI flags the position as deliberately interface-facing (i.e., AI attempts a charge-complementarity pairing with a known charged residue on human ASCT2), the variant survives the Fast Filter and is escalated to the Slow Filter for ΔΔG_binding evaluation.

**Expected kill rate:** ~8–12% of naive AI output.

### Heuristic 2 — **Side-Chain Volume Catastrophe (HARD VETO)**

**Rule:** Reject any substitution where:
- (a) |ΔVolume| > 50 Å³ (Zamyatnin volumes);
- (b) RSA < 30% (buried or semi-buried);
- (c) the position is within the SU β-barrel core, TM helix, or HR1/HR2 six-helix bundle.

**Numeric threshold:** ΔVolume > +50 Å³ in a buried core position (e.g., G→W, S→F at RSA<30%) or ΔVolume < −60 Å³ (creating an unfilled cavity, e.g., W→A at RSA<30%).

**Rationale:** Large volume increases in cores force backbone rearrangement; large volume decreases leave cavities that destabilize by 1.5–4 kcal/mol per 50 Å³. Catalytic-site analog: the T7 RNAP E643K failure in the EVOLVEpro paper placed a bulky residue near the NTP-binding pocket; the analog here is introducing W, F, or Y in the fusion peptide core or HR1.

**Carve-out:** Surface-exposed positions (RSA ≥ 30%) are permitted any volume change. This is where most real winners live (the T7 RNAP top-hit position was surface-accessible).

**Expected kill rate:** ~10–15%.

### Heuristic 3 — **Disulfide Bookkeeping (HARD VETO, NO CARVE-OUT)**

**Rule:** Never mutate a cysteine engaged in a documented or high-confidence predicted disulfide unless the partner cysteine is mutated in the *same variant* in a compensatory Cys→Cys shift.

**Numeric threshold:** BaEV SU-TM has 8 predicted disulfide pairs per AlphaFold3 (to be confirmed by R0 structural pipeline). Any Cys removal in these pairs without matched partner handling = reject.

**Rationale:** Retroviral Class I envelopes are notoriously sensitive to disulfide bookkeeping. Loss of a single SU–TM disulfide causes spontaneous SU shedding and abolishes infectivity. This is non-negotiable and has no productive design-space carve-out.

**Expected kill rate:** ~1–2% (AI rarely proposes Cys mutations spontaneously, but language-model samplers can occasionally suggest them).

### Heuristic 4 — **N-Glycan Relocation Without Review (HARD VETO)**

**Rule:** Reject any substitution that:
- (a) **removes** a canonical N-glycosylation consensus site (NxS/T, x≠P) on SU; or
- (b) **introduces** a new NxS/T sequon within the RBD (residues 30–210) or within 8 Å of the predicted ASCT2 interface.

**Numeric threshold:** BaEV has ~11 predicted N-glycan sites on SU; knockout of any one = reject; creation of a novel sequon inside the RBD contact zone (AlphaFold3 interface residues ± 8 Å Cα distance to SLC1A5) = reject.

**Rationale:** Glycan shield composition drives three clinically relevant behaviors the QUIESCO-1 spec locks in:
1. **Complement resistance** — loss of the MPER-proximal glycan makes BaEV complement-sensitive; this is a known failure mode from RDTR/cocal comparative work.
2. **Receptor access** — the RBD glycan cluster gates ASCT2 contact kinetics; moving a glycan into the interface sterically abolishes transduction *and* scores fine on simple affinity metrics because the glycan is post-translational.
3. **Immunogenicity** — glycan knockouts expose subsurface peptide epitopes that NetMHCpan cannot anticipate because the WT glycan shielded them from T-cell surveillance in the natural env.

**Carve-out:** Glycan **repositioning** (removing one site AND adding a compensating site within 6 Å Cα) may be escalated to the Slow Filter with an explicit "intentional glycan engineering" flag. This is a Stage 5/6 handle we want to keep alive, not kill at Stage 4.

**Expected kill rate:** ~5–7%.

### Heuristic 5 — **Register-Breaking Prolines and Glycines in Helices (HARD VETO)**

**Rule:** Reject any substitution that:
- (a) introduces a proline into HR1, HR2, the TM helix, or any α-helix of the SU core with >4 residues of flanking helical character per AlphaFold3 DSSP assignment;
- (b) introduces a glycine at an i, i+3, or i+4 position flanking an existing proline or helix-cap in the same regions.

**Numeric threshold:** Any X→P in a DSSP-H-assigned residue within HR1 (res ~420–470), HR2 (res ~520–570), or TM (~600–625) = reject.

**Rationale:** Proline breaks backbone φ,ψ in helices by ~4 kcal/mol and abolishes the six-helix bundle that drives membrane fusion. Glycine adds flexibility that destabilizes the register. Both fail silently on small-molecule structure metrics but kill fusion dead.

**Carve-out:** X→P at helix caps (first or last residue of DSSP-H run) is permitted — these are positions where proline is stabilizing and several engineered env stabilization efforts (HIV SOSIP, RSV F DS-Cav1 analogs) exploit precisely this placement.

**Expected kill rate:** ~3–5%.

### Total Fast-Filter Kill Rate

**~25–35% of raw AI output** — substantial enough to materially reduce Tier 1 load, conservative enough that the surviving distribution still contains non-intuitive winners. Critically, **no surface-exposed variant is killed by Heuristics 1, 2, or 5** — the filter protects core integrity and ignores surface loop diversity, which is where real winners have historically lived.

---

## 3. The "Slow Filter" — External Computational Validation Spec

**To be executed by the outsourced computational biology team (recommended: in-house if ≥1 FTE structural biologist available; otherwise Cradle, Charm, Atomic, or comparable CRO).** Each surviving variant (~65–75% of pre-filter) runs through the following pipeline. Target turnaround: 48 h per variant at 100–200 GPU-hours/variant on A100-equivalent.

### 3.1 Structural Prediction — AlphaFold3 (PRIMARY) + ESMFold (RAPID)

**Task:** Predict the variant's SU-TM trimer in complex with the SLC1A5 ectodomain (ASCT2) model.

**Tool:** AlphaFold3 (multimer mode). ESMFold used as a pre-screen — if ESMFold pLDDT <70 in the RBD or <75 globally on WT, upgrade immediately to AF3.

**Inputs:**
- BaEV SU-TM sequence, variant-substituted.
- Human SLC1A5 extracellular face (templated from PDB 7G12 or best available).
- Template bias off (we want the model to predict WT fold integrity de novo).

**Outputs required per variant:**
- Global pLDDT
- RBD region pLDDT (res 30–210)
- Interface pTM (ipTM) score against SLC1A5
- PAE matrix for mutated residue vs. all interface residues
- Superposition RMSD to WT prediction over Cα

**Thresholds (REJECT if):**
- Global pLDDT < 75.
- RBD pLDDT < 80.
- ipTM drops >0.15 vs. WT prediction on same hardware.
- Cα RMSD of any mutated residue > 2.5 Å vs. WT prediction *and* that residue is within 8 Å of the ASCT2 interface.

### 3.2 Side-Chain Proximity Check — The "T7 RNAP E643K Analog" Test

**This is the specific guardrail the EVOLVEpro paper's failure mode demands.** In T7 RNAP, the failed variant placed a bulky side chain within 2 Å of the DNA substrate — the AI found a high-fitness fold but a sterically impossible enzyme-substrate complex.

**Task:** For every mutated side chain, measure the minimum heavy-atom distance to:
- (a) any ASCT2 (SLC1A5) atom in the complex prediction;
- (b) any glycan NAG (to catch clashes with modeled N-glycans);
- (c) any neighboring subunit in the trimer (clash with symmetry-related protomer);
- (d) the lipid bilayer plane (for TM/MPER residues; use COM of TM helix as reference).

**Tool:** PyMOL scripted (`get_distance` on heavy atoms) or Biopython on the PDB. Scripted, not manual — run on every variant.

**Thresholds (REJECT if):**
- Any mutated heavy atom < 2.0 Å from a partner atom (this is the literal T7 RNAP failure threshold).
- Any mutated heavy atom 2.0–2.5 Å from a partner atom **AND** ΔΔG_binding prediction (§3.4) is worse than WT → flag as "likely clash" and demote to B-list only.

### 3.3 Stability Prediction — FoldX (DEFAULT) + Rosetta ΔΔG (CONFIRMATORY)

**Task:** Predict ΔΔG of folding stability for each variant vs. WT.

**Tool:**
- **FoldX 5.1** — primary, fast (~1 min/variant). Use `BuildModel` with `RepairPDB` on the WT first.
- **Rosetta `ddg_monomer` (or `cartesian_ddg`)** — on any variant where FoldX predicts ΔΔG in [+2, +4] kcal/mol (the ambiguous zone). Rosetta is slower but more accurate in marginal cases.

**Thresholds:**
- **REJECT if FoldX ΔΔG > +3 kcal/mol** (aligns with blueprint-stage guidance; corresponds to ~20× reduction in folded fraction at 37°C).
- **Flag for B-list** (synthesize anyway, measure false-positive rate) if +2 < ΔΔG ≤ +3 kcal/mol — these are borderline destabilizing and sometimes compensated by epistatic partners in multi-mutant variants.
- **REJECT if Rosetta confirms ΔΔG > +3 kcal/mol** on FoldX-flagged cases.
- **Bonus flag:** variants with ΔΔG < −1.5 kcal/mol (stabilizing) are promoted as *a priori* interesting and tagged for thermostability prioritization.

### 3.4 Binding Interface ΔΔG — Rosetta Interface Analyzer

**Task:** For variants with mutations within 8 Å of the ASCT2 interface, compute ΔΔG_binding.

**Tool:** Rosetta `InterfaceAnalyzerMover` on the AF3-predicted complex, WT vs. variant. Sample 50 decoys per variant; report median.

**Thresholds:**
- **REJECT if ΔΔG_binding > +2 kcal/mol** (loss of ~30× binding affinity) — unless flagged as intentional affinity-tuning or receptor-switching.
- **Promote** variants with ΔΔG_binding in [−2, −0.5] kcal/mol — productive tightening without affinity-maturation runaway.
- **Flag for review** variants with ΔΔG_binding < −3 kcal/mol — suspiciously tight; verify not an artifact of glycan clash or buried-hot-spot overfitting. Very tight binders can also reduce cell-surface detachment kinetics and paradoxically reduce productive fusion.

### 3.5 Active-Site / Functional-Site Geometry Check

Not a traditional active site for an envelope, but three functional sites on BaEV Env must be geometrically preserved:

**a) Furin cleavage site (RNKR-like motif near residue ~390):**
- Solvent accessibility (RSA) of the scissile bond must remain ≥ 40% in the variant prediction.
- No substitutions within a 6 Å sphere of the P4–P4' residues.
- Any variant violating this: **REJECT**.

**b) Fusion peptide exposure (post-cleavage):**
- The fusion peptide N-terminal residues (first 20 after the cleavage site) must remain sterically accessible for insertion into the target membrane. Check that no introduced side chain creates a buried occlusion (RSA of the fusion peptide N-terminus must remain ≥ 25% in the post-cleavage modeled state).
- Any variant violating this: **REJECT**.

**c) Six-helix bundle competence (post-fusion state):**
- For variants with mutations in HR1 or HR2, predict the post-fusion six-helix bundle (AF3 with two copies of TM ectodomain as symmetric input). Compute the register integrity by measuring i/i+7 hydrophobic face residue identity (leucine/valine/isoleucine content at a/d positions).
- **REJECT** if the i/i+7 hydrophobic face identity drops below 70% of WT.

### 3.6 Glycan Model Consistency Check

**Task:** For every variant whose mutation is within 10 Å of a predicted N-glycan site, re-run AF3 with a GlcNAc-attached sequon and check that the glycan position does not:
- Clash (<2.0 Å) with the ASCT2 interface;
- Invade the fusion peptide exposure zone;
- Clash with the i/i+7 hydrophobic face of HR1/HR2.

**Tool:** AF3 with glycan ligand input (or post-hoc modeling via GLYCAM-web if the structural team lacks AF3 ligand capability).

**Threshold:** **REJECT** if glycan heavy atom enters any of the three forbidden zones above. Otherwise **pass**.

### 3.7 Summary Output per Variant

The Slow Filter returns a 12-field record per variant:

| Field | Value | Pass/Fail |
|---|---|---|
| AF3 global pLDDT | float | ≥75 |
| AF3 RBD pLDDT | float | ≥80 |
| AF3 ipTM (complex) | float | ≥ (WT − 0.15) |
| Mutated-residue min heavy-atom distance | float Å | ≥2.0 |
| FoldX ΔΔG | float kcal/mol | ≤+3.0 |
| Rosetta ΔΔG (if invoked) | float kcal/mol | ≤+3.0 |
| Rosetta ΔΔG_binding | float kcal/mol | ≤+2.0 (unless intentional) |
| Furin cleavage site RSA | float | ≥40% |
| Fusion peptide N-term RSA (post-cleavage) | float | ≥25% |
| HR1/HR2 heptad register integrity | % | ≥70% of WT |
| Glycan consistency | pass/fail | pass |
| Mutation count & regional distribution | int & zones | ≥12 non-cons, ≥4 high-info (per Stage 3 FTO) |

Any single FAIL → **REJECT** (with the B-list escape hatch in §5 catching a defined fraction for validation).

---

## 4. HSC-Specific Notes — BaEV Envelope Particulars

Target-class-specific warnings beyond the generic physical chemistry:

### 4.1 Preserve RBD Glycosylation Pattern Unless Explicitly Repositioning
BaEV RBD has ~3 predicted N-glycan sites in the 30–210 region that shield immunogenic peptide epitopes. Heuristic 4 kills any knockout; Slow Filter §3.6 catches relocation hazards. **Any glycan-engineering variant must be explicitly labeled `glycan_engineered=true` in the variant record and reviewed by the lead scientist, not auto-advanced.** Glycan engineering is a legitimate long-term axis (complement resistance, serum half-life) but not one the AI should explore in R1–R3.

### 4.2 ASCT1/ASCT2 Dual-Receptor Competence (Stage 3 M_ASCT1 Gate)
The Stage 3 QA hard-gate requires retention of ASCT1 transduction. The Slow Filter must therefore run a **second ΔΔG_binding calculation against SLC1A4 (ASCT1)** using the homology model. **Reject** any variant with ASCT1 ΔΔG_binding > +3 kcal/mol (moderate threshold — we want ASCT1 competence preserved, not maximized). This is the receptor-switch optionality the FTO strategy depends on (Stage 1 QA §6).

### 4.3 MPER Engineering for Producer Detoxification — Permitted but Bounded
The membrane-proximal external region (~570–600) is the highest-value zone for reducing producer syncytia without killing transduction (RSV F DS-Cav1 precedent). The filter must **permit aggressive MPER engineering** — do not accidentally veto these variants via Heuristic 2 (volume) or Heuristic 5 (helix breakers) at surface-exposed MPER positions. **Explicit carve-out:** for residues 570–600 with RSA ≥ 25%, raise the volume threshold to 70 Å³ and permit proline introduction. MPER is where producer-detoxification winners live.

### 4.4 The R-Peptide Adjacent Zone (FTO-Critical)
The cytoplasmic tail immediately adjacent to the R-peptide cleavage site (residues ~620–640) is where the Stage 1 QA genus-claim trap lives. The filter must **enforce ≥6 position Hamming distance from WT Rless in this region for any variant that carries any tail modification** (Stage 3 M_FTO gate). **This is not a chemical check; it is a binary legal check that runs in the Fast Filter.** Any variant with <6 position distance = reject with reason code `FTO_TAIL_CLAIM_COLLISION`.

### 4.5 Complement Epitope Avoidance
Published work on RDTR and BaEV shows that MPER-proximal glycan loss creates a linear complement-binding epitope. The Fast Filter's Heuristic 4 catches the glycan loss case; the Slow Filter should additionally **flag any variant that introduces or removes charged residues in residues 560–600** for PBMC complement assay prioritization at Stage 5. Not a reject — a flag for downstream testing.

### 4.6 Trimer Interface Sensitivity
BaEV Env is a trimer. AF3 multimer prediction should be run with three copies; any variant where the inter-protomer interface RMSD > 2.0 Å or where the trimer pTM drops >0.1 vs. WT is suspect for trimer dissociation — which gives high apparent titer (monomers pseudotype particles) and zero transduction. **Reject** variants with trimer pTM drop > 0.15.

### 4.7 Do NOT Filter on "Conservative" Substitution Intuition Alone
A caution to the team, not a rule: BaEV Env has been under essentially no selective pressure for HEK293T compatibility or human ASCT2 affinity. **Conservative substitutions (I→V, L→M) in "conserved-looking" positions may already be near-optimal and not move fitness; non-conservative substitutions (F→D on the surface, G→W in a loop) are the most likely winners.** The filter above preserves this — it only vetoes chemically catastrophic changes, not chemically surprising ones. Review anyone trying to add "conservativeness" thresholds to the filter.

---

## 5. B-List Safety Net — Measuring the Filter's False-Positive Rate

**The filter is a hypothesis, not a ground truth.** To measure and correct its false-positive rate, we synthesize and test a defined fraction of filter-rejected variants in parallel.

### 5.1 B-List Composition

Every round, **10% of the Tier 1 batch (~30–60 variants of the ~300–600 triaged) is drawn from the rejected pool**, stratified as follows:

| Stratum | Fraction of B-list | Rationale |
|---|---|---|
| Fast Filter Heuristic 1 rejects (core charge reversals) | 20% | Most likely to surprise; Heuristic 1 is strict by design |
| Fast Filter Heuristic 2 rejects (volume catastrophes) | 20% | Surface-exposed edge cases and MPER-proximal cases likely false positives |
| Fast Filter Heuristic 4 rejects (glycan relocation) | 15% | Glycan engineering space deliberately suppressed; B-list keeps the option measured |
| Slow Filter FoldX ΔΔG reject [+2.5, +4.5] kcal/mol | 25% | Borderline destabilizers are the highest-information B-list — epistatic partners can rescue |
| Slow Filter ΔΔG_binding reject [+2, +4] kcal/mol (ASCT2) | 10% | Interface reshuffle cases |
| Slow Filter clash reject (min distance 1.5–2.0 Å) | 10% | AF3 prediction has ~0.3 Å positional error; some "clashes" are model noise |

### 5.2 B-List Measurement Protocol

- B-list variants run Tier 1 only (producer titer, producer viability). They do NOT consume Tier 2 apheresis allocation — the rejected pool is too large to risk donor cells on.
- At end of round, compute: for each heuristic, what fraction of rejected variants scored in the top-quartile of Tier 1 among B-list?
- If any single heuristic has a **false-positive rate (top-Tier-1-quartile fraction) > 15%**, the heuristic is recalibrated before the next round. Specifically:
  - Loosen the threshold by the distance that would have admitted the observed false positives;
  - Document the change in the R&D changelog;
  - Re-run the Slow Filter calibration on the next batch.

### 5.3 B-List Cost

- 30–60 variants × Tier 1 unit cost $200 = **$6K–12K per round**, ~$40K–$85K over the 6–8 round campaign. ~1–3% of the assay budget. **Trivial cost for a measured filter.**

### 5.4 What We Do with B-List Winners

Any B-list variant that scores in the top quartile of Tier 1 in its round is **promoted to the Tier 2 queue of the following round** (not the same round — by that time Tier 2 is already provisioned), with the filter heuristic that killed it marked in its record. If the variant also wins Tier 2, we have a clean documented case study for filter recalibration and a genuinely non-intuitive winner. These are expected to appear 1–3 times over the campaign; if they do not appear at all, the filter is too loose (losing winners we would never catch) or the AI is too conservative.

---

## 6. Filter Integration into the QUIESCO-1 AL Loop

The filter sits between AI variant generation and Tier 1 execution, as follows:

```
AI sampler → ~3000 raw variants
  ↓
[FAST FILTER: 5 heuristics + FTO checks]
  ↓ ~2000–2250 survivors (~25–35% kill)
  ↓
[SLOW FILTER: AF3 → distance/clash → FoldX → (Rosetta if needed) → ΔΔG_binding → functional-site geometry → glycan consistency]
  ↓ ~600–900 survivors (~30% kill of Fast survivors)
  ↓
[ML ranking on predicted fitness using EVOLVEpro-class model + filter survivor pool]
  ↓
Top ~500 A-list → Tier 1 (producer titer + viability)
  +
~30–60 B-list sampled from rejected pool → Tier 1 (filter calibration)
  ↓
Top 60 A-list → Tier 2 (primary HSC fitness assay)
  ↓
Fitness scalar F(v) feeds back to AI sampler
```

Filter is re-calibrated **every round** from B-list data. Tightening or loosening is a documented decision, not a drift.

---

## 7. Deliverable Summary

| Layer | Contents |
|---|---|
| **Fast Filter (AI-side)** | 5 hard-veto heuristics with numeric thresholds and explicit carve-outs: (1) buried charge reversal, (2) buried volume catastrophe, (3) disulfide bookkeeping, (4) glycan knockout/RBD introduction, (5) register-breaking proline/glycine in helices |
| **Slow Filter (external)** | AF3+ESMFold structural prediction; scripted side-chain proximity check (<2.0 Å reject); FoldX ΔΔG >+3 reject; Rosetta ΔΔG ambiguous zone confirmation; Rosetta interface ΔΔG_binding >+2 reject; furin/fusion-peptide/six-helix-bundle geometry checks; glycan consistency check |
| **HSC-specific notes** | RBD glycan pattern preservation; ASCT1 dual-receptor gate; MPER engineering carve-out; R-peptide-adjacent FTO gate; complement epitope flagging; trimer interface sensitivity; caution against "conservative-substitution-only" intuition |
| **B-List safety net** | 10% of Tier 1 drawn from rejected pool, stratified by heuristic; false-positive rate measured every round; threshold recalibration >15% FPR trigger; ~$6–12K/round cost |

**Projected triage efficiency:** ~3000 AI proposals → ~600–900 entering Tier 1 → top 60 into Tier 2. Donor cells protected; non-intuitive winners preserved via B-list; filter is self-correcting.

**Proceed to Stage 5** with this protocol codified as SOP. Next stages will stress this filter against real R1 data; expect at least one heuristic to require recalibration within the first two rounds, which is why the B-list is not optional.
