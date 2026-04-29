# Domain Constraint: HSC Biology, Cytopenia, and Longevity Adjacency

**This is a hard constraint that applies to every stage of this pipeline.** Every target, candidate protein, assay, experimental plan, IP analysis, and investment thesis must be directly relevant to one of the following, in this order of priority:

## Beachhead (required for any candidate to advance)

1. **Hematopoietic Stem Cell (HSC) engineering** — expansion, engraftment, self-renewal, fate commitment, ex vivo manipulation, transduction efficiency, gene-editing delivery into CD34+ cells, homing/niche retention, conditioning-free transplant enablement.
2. **Cytopenia therapeutics** — anemia (incl. MDS, renal, chemo-induced, hemoglobinopathies), neutropenia (febrile, congenital, chemo-induced), thrombocytopenia (ITP, chemo-induced, aplastic), bone marrow failure syndromes (severe aplastic anemia, Fanconi, DBA), CHIP and clonal hematopoiesis where it drives cytopenia risk.

## Generalization axis (secondary, flag don't prioritize)

3. **Longevity-relevant hematopoiesis** — HSC exhaustion with age, myeloid bias, epigenetic drift, clonal expansion of CHIP mutants, immune aging driven by HSC dysfunction, rejuvenation of aged bone marrow niche.

## Hard rules every stage must enforce

- **Reject** any candidate whose primary use case is unrelated to HSCs, blood, or bone marrow — unless you explicitly argue for a longevity generalization path with a concrete HSC/immune-rejuvenation hypothesis.
- **Prefer** proteins where a 50x–100x directed-evolution improvement could plausibly change a cell therapy or cytopenia outcome. Non-exhaustive examples of the *class* of target we want:
  - HSC expansion factors (UM171-class small-molecule analogs, SR1-class, engineered cytokines: TPO, SCF, FLT3L, IL-3 variants)
  - Gene-editing enzymes optimized for CD34+ cells (Cas variants with better HDR in quiescent cells, base/prime editors with reduced off-target in HSCs)
  - Lentiviral envelope proteins tuned for CD34+ transduction (BaEV, cocal variants)
  - Erythropoiesis-stimulating proteins beyond EPO (activin-trap variants, luspatercept-class)
  - Thrombopoietic agents beyond romiplostim/eltrombopag
  - Conditioning agents that spare non-HSC tissue (anti-CD117 ADC payloads, CD45-SAP variants)
  - Niche-modifying factors (angiopoietin variants, CXCL12, osteolineage targeting)
  - BMF gene therapy payloads (elongation factors, ribosomal protein variants for DBA, telomere maintenance)
- **Benchmark commercial pain points against** allogeneic cell therapy manufacturing (yield/engraftment), gene therapy for hemoglobinopathies (editing efficiency in quiescent HSCs), bone marrow transplant conditioning (non-genotoxic), cytopenia management (durable responses, home administration).

## Longevity pivot flag

For each candidate, add a **Longevity Generalization Score (LGS)** of LOW / MED / HIGH:
- **HIGH** — candidate plausibly rejuvenates aged HSCs or ameliorates age-related clonal hematopoiesis.
- **MED** — candidate is HSC-centric but does not obviously extend beyond disease hematopoiesis.
- **LOW** — pure cytopenia play, no longevity thesis.

The pipeline optimizes for a **cytopenia beachhead first**. LGS is informational — do not let it override the beachhead requirement.
