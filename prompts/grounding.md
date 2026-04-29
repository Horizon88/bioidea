# Grounding Contract — Output Discipline

This pipeline runs a post-pass validator against every stage output (lightweight slice of `docs/grounding-contract.md`). **You must format output to satisfy the validator**, or your stage will be flagged `FAIL` and re-run.

## The rule

**Every bulleted factual claim that contains a digit or a named acronym MUST end with a source tag block:**

```
- <claim text>  [src: <tag1>, <tag2>, ...]
```

## Allowed source tag types

- `PMID:<digits>` — PubMed ID, e.g. `PMID:31634902`
- `DOI:<doi>` — digital object identifier, e.g. `DOI:10.1038/nbt.3514`
- `patent:<jurisdiction><number>[kind]` — e.g. `patent:US10123456B2`, `patent:EP3456789A1`, `patent:WO2020123456A1`
- `biorxiv:<id>` — bioRxiv, e.g. `biorxiv:2024.01.15.575899`
- `arxiv:<id>` — e.g. `arxiv:2401.12345`
- `clinicaltrials:<NCTid>` — e.g. `clinicaltrials:NCT04819841`
- `uniprot:<accession>` — e.g. `uniprot:Q9WJM2`
- `company:<name>` — company-reported figure (press release, 10-K, investor deck). Accepted but weak.
- `url:<https://…>` — last-resort for regulatory docs, GitHub issues, etc.
- `estimate` — explicitly modeled / back-of-envelope. Use this honestly; do NOT dress an estimate in a fake PMID.
- `reasoning` — derived from earlier tagged claims in this same output. Use sparingly.

## CRITICAL: do not fabricate identifiers

If you do not know the real PMID, DOI, or patent number, **emit `[src: estimate]` or `[src: reasoning]`**. The validator cannot catch a hallucinated PMID by itself, but the downstream human reviewer will, and fabricated identifiers in a memo or provisional are career-ending. The entire point of this contract is to make dishonesty structurally harder than honesty.

When you tag with `PMID`, `DOI`, `patent`, or `biorxiv`, you are asserting you are confident the identifier is real. If you are not, use `estimate` or `reasoning`.

## What needs a tag

- Any bullet containing a number (titer, efficacy %, dollars, patient counts, timelines, Kd, IC50, fold-change, year).
- Any bullet naming a specific product, program, company, patent, protein, or gene with a claimed property.
- Verdicts that cite specific prior stage findings should use `[src: reasoning]`.

## What does NOT need a tag

- Headers and section labels.
- Section transitions and framing sentences.
- Table column labels and table separators.
- Persona/role restatements.
- Pure rhetorical or framing prose (no specific number or entity).

## Multiple sources

Multiple tags can be combined: `[src: PMID:31634902, PMID:35256834, patent:US10123456B2]`.

## Weak vs strong tags

The validator distinguishes `strong` tags (PMID / DOI / patent / biorxiv / arxiv / clinicaltrials / uniprot — externally resolvable) from `weak` tags (company / url / estimate / reasoning). A stage output dominated by weak tags will pass validation but will be flagged in the report for the reviewer. Prefer strong tags; be honest when you can only offer a weak one.

## Example — correctly tagged

```
- WT BaEV-TR transduces unstimulated CD34+CD38-CD90+ LT-HSCs at 10-20% VCN≥1 at MOI 10 [src: DOI:10.1182/blood.2019000941, DOI:10.1038/s41591-019-0601-5]
- Vertex Casgevy list price is $2.2M per patient [src: company:Vertex]
- A ≥50% G0 transduction endpoint is reasonable because WT is ~15% and we are targeting 3-5x gain over 5 evolution rounds [src: reasoning]
- VSV-G-pseudotyped LV requires 48-72h cytokine prestim in standard protocols [src: PMID:31471581]
- Our modeled Round-5 titer of 1e8 TU/mL assumes 10x improvement over the ~1e7 TU/mL Expi293 baseline [src: estimate]
```

## Example — fails validation

```
- WT BaEV-TR transduces quiescent HSCs at 10-20% efficiency.     ← FAIL: numeric bullet, no tag
- Vertex Casgevy list price is $2.2M/patient.                    ← FAIL: numeric bullet, no tag
- ASCT2 is expressed on HSCs [src: PMID:9999999999]              ← FAIL: PMID too long, malformed
```
