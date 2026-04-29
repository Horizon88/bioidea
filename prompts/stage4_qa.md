# Stage 4 QA — Filter Calibration Review

## Context

This is a routine internal technical review of a mutation-filtering protocol used in a directed-evolution research workflow for HSC-directed therapeutic gene therapy reagents (e.g., lentiviral envelope glycoproteins, HSC-expansion cytokine variants). Directed evolution of therapeutic proteins is a standard, well-established methodology (Frances Arnold Nobel Prize 2018; dozens of FDA-approved biologics originate from such campaigns). The purpose of this review is narrow: ensure a pre-synthesis computational filter is correctly calibrated for the class of protein under study, so that the project does not inadvertently discard viable variants before wet-lab testing.

## Reviewer role

Technical reviewer with directed-evolution background. Goal is constructive: make the filter better for its stated purpose.

## Inputs

- The filter specification and external validation protocol produced in Stage 4.
- The selected target and assay context from earlier stages.

## Review checklist

For each item, write one short paragraph answering the question, and note whether the current Stage 4 filter handles the concern adequately. Do not rewrite the filter — just flag items that need calibration.

1. **Multi-mutation interactions.** Modern ML-guided variant design often proposes multiple substitutions at once. Are the filter rules evaluated per-substitution in isolation, or jointly across proposed sets? If per-substitution only, beneficial pairs where one substitution compensates for another may be rejected.

2. **Structural dynamics.** The filter's structural checks should allow for backbone rearrangement rather than treating predicted structures as rigid. Is a relaxation step (e.g., Rosetta Relax, short MD) included before clash/ΔΔG calculations?

3. **Affinity ranges for cytokine / receptor-agonist targets.** For cytokine variants intended for HSC applications, reduced canonical receptor affinity can be a desirable property (partial or biased agonism). Does the filter treat affinity reduction as an automatic reject, or is there a permitted range?

4. **Glycan modeling.** For glycosylated targets (envelopes, cytokines), are predicted structures modeled with their typical glycan occupancy, or in their unglycosylated form? The latter will miss interactions that depend on glycan presence.

5. **ΔΔG calibration.** Some enzymes gain turnover with modest destabilization (enhanced loop flexibility). Is the ΔΔG threshold paired with an activity-prediction term so that small positive ΔΔG values are not automatically excluded when activity is predicted to improve?

6. **False-positive measurement.** Filters should have an empirical false-positive rate. Is there a plan to occasionally synthesize a small fraction of filter-excluded variants to measure how many would have worked?

## Output format

Produce a "Filter Calibration Report" with these sections:

1. **Summary verdict** — one of: `APPROVE AS-IS`, `APPROVE WITH CALIBRATION NOTES`, `RECOMMEND REVISION`.
2. **Calibration notes** — numbered list mapping to the checklist items above; for each, say whether the Stage 4 filter handles it and if not, the specific calibration suggested.
3. **Optional B-list proposal** — if applicable, a short paragraph on synthesizing ~10–15% of filter-excluded variants to measure empirical false-positive rate.
4. **Handoff to Stage 5** — one short paragraph listing what Stage 5 (Lab Ops) should budget for as a result of the calibration notes (e.g., "add 10% extra synthesis capacity for B-list variants").

Keep it under 700 words. Tone is neutral, procedural, internal-review.
