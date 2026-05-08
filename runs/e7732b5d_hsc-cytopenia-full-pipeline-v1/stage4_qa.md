---
run: HSC-cytopenia full pipeline v1
run_id: e7732b5d65be49d79dafbdf7c841f3e9
stage: 4
stage_key: chemical_logic
stage_label: Chemical Filter
phase: qa
model: sonnet
generated_at: 2026-04-24T11:05:16
duration_s: 60.5
cost_usd: 0.10055454999999999
tokens_in: 2
tokens_out: 2451
---

# Filter Calibration Report — QUIESCO-1 Stage 4 QA
**Reviewer role:** Technical reviewer, directed-evolution background
**Date:** 2026-04-24
**Subject:** Stage 4 mutation-filtering protocol, BaEV-Rless envelope campaign

---

## 1. Summary Verdict

**APPROVE WITH CALIBRATION NOTES**

The filter architecture is sound. The five fast-filter heuristics are specific to the structural biology of a Class I viral fusion protein and the B-list safety net (§5) is correctly designed. Four calibration gaps are identified below; none requires a protocol rewrite, but two require explicit procedural amendments before R1 execution.

---

## 2. Calibration Notes

**Item 1 — Multi-mutation interactions.** The five fast-filter heuristics are evaluated per-substitution in isolation. FoldX `BuildModel` in the slow filter operates on the full variant sequence and does capture epistatic effects on stability, but the hard-veto rules (heuristics 1, 2, 5) can kill a variant for a single substitution that would be rescued by a co-occurring stabilizing mutation elsewhere. This is the most consequential gap: a charge reversal at a semi-buried RBD position (heuristic 1) may be precisely compensated by an adjacently proposed hydrophobic packing mutation in the same variant. **Calibration needed:** add a conditional pass for multi-mutant variants where a per-substitution fast-filter veto fires — if the co-mutations in the same variant are predicted by the AI to be compensatory (i.e., the variant's composite FoldX ΔΔG passes the slow-filter threshold), escalate to slow filter rather than hard-veto. Implement as a "multi-mutant override" flag in the variant record; do not widen the heuristic threshold globally.

**Item 2 — Structural dynamics / relaxation.** The slow filter runs `RepairPDB` before FoldX, which repacks side chains but does not perform backbone relaxation. Clash checks (§3.2) and interface ΔΔG calculations (§3.4) are therefore performed on a semi-rigid structure. For mutations in flexible linker regions (VRA-VRB, ~210–260) and MPER (~570–600), which are engineering hot zones for this campaign, backbone rigidity will produce spurious clash rejections. **Calibration needed:** add a brief Rosetta `FastRelax` (5 cycles, coordinate-constrained backbone) before the heavy-atom distance check in §3.2 and before `InterfaceAnalyzerMover` in §3.4. This is standard practice; cost is approximately 10–20 additional GPU-minutes per variant and does not materially change throughput.

**Item 3 — Affinity ranges.** For a lentiviral envelope, this is a transduction-efficiency target, not a cytokine agonist, so the biased-agonism framing does not apply directly. However, the question is relevant to the dual-receptor gate (§4.2): the filter permits ASCT1 ΔΔG_binding degradation up to +3 kcal/mol while ASCT2 is gated at +2 kcal/mol. This asymmetry is intentional and correctly documented. **No calibration required** for this item given the target class.

**Item 4 — Glycan modeling.** The primary structural prediction (§3.1, used as input to §3.2 clash checks and §3.4 ΔΔG_binding) is run on the unglycosylated sequence. The dedicated glycan consistency check (§3.6) is only triggered for mutations within 10 Å of a predicted glycan site and uses a separate AF3 run. This means side-chain clash calculations for variants near but outside the 10 Å threshold are run without glycan context — a glycan-mediated steric effect can be missed entirely. **Calibration needed:** extend the glycan-consistency trigger from 10 Å to 15 Å Cα distance from any predicted N-glycan sequon. The incremental AF3 calls are low volume (only ~30% of SU residues fall in the expanded radius).

**Item 5 — ΔΔG calibration vs. activity.** The FoldX ΔΔG hard-reject threshold (+3 kcal/mol) is not paired with a functional-geometry or activity-prediction term. For BaEV Env, functional proxies exist in the slow filter (fusion-peptide RSA, HR1/HR2 heptad register, furin cleavage RSA), but a variant with FoldX ΔΔG = +2.8 kcal/mol that passes all functional-site geometry checks is currently at risk of B-list relegation with no pathway to direct promotion. **Calibration needed:** variants in the [+2, +3] kcal/mol FoldX range that pass all five functional-site geometry checks should be auto-promoted to A-list rather than defaulting to B-list. Document as "functional-rescue override" in the variant record.

**Item 6 — False-positive measurement.** Fully addressed in §5. B-list composition, measurement protocol, cost, and 15% FPR recalibration trigger are all specified. **No calibration required.**

---

## 3. B-List Note

The existing B-list design (§5) is adequate. The only amendment following item 5 above: variants promoted via "functional-rescue override" should be tracked as a distinct sub-cohort within the A-list so their Tier 1 hit rate can be compared to the main A-list, providing an ongoing calibration signal for the ΔΔG threshold independently of the B-list.

---

## 4. Handoff to Stage 5

Stage 5 (Lab Ops) should budget for: (a) approximately 10–15% additional Rosetta compute time per variant from the FastRelax amendment (item 2); (b) a modest increase in AF3 glycan-check calls from the expanded 15 Å trigger (item 4) — estimated +5–8% slow-filter GPU cost; (c) a "functional-rescue override" tracking column in the variant database schema before R1 data ingestion. No additional synthesis capacity is required beyond what the existing B-list allocation covers.
