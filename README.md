# bioidea

A 7-stage biotech idea-generation workflow, hard-constrained to **HSC engineering, cytopenia therapeutics, and longevity-adjacent hematopoiesis**.

Each stage has a distinct persona, a main deliverable, and a red-team QA pass that audits the deliverable. Execution is routed through `claude -p` using your logged-in Claude Max plan (no API keys). Runs are persisted to SQLite + markdown artifacts.

The pipeline design is adapted from the "EVOLVEpro-style" workflow in `Biotech Workflow Evolve [GG].xlsx`, with every stage rewritten to hard-constrain candidates to the HSC/cytopenia beachhead. Longevity is a flagged generalization axis, not a first-class output.

## Stages

| # | Stage | Persona (main) | Red Team (QA) |
|---|---|---|---|
| 0 | **Target Scout (Visionary)** | Ruthless Biotech Venture Scout | Technical Auditor / Kill Criteria |
| 1 | **FTO (IP Gauntlet)** | Senior Patent Counsel | Hostile Patent Litigator |
| 2 | **Assay Audit (Scientist)** | Assay Dev + Biostatistician | Translational Medicine Lead |
| 3 | **Objective Function (Evo Blueprint)** | Principal Scientist / AI Strategy | Lead Data Scientist (metric gaming) |
| 4 | **Chemical Logic Filter** | Senior Computational Chemist | Radical Evolutionist (Arnold-school) |
| 5 | **Lab Ops (Low-N Campaign)** | Lab Operations Director | Manufacturing Logistics |
| 6 | **Investment Memo (Greenlight)** | Biotech Venture Partner | Managing Partner (Final Boss) |

## Install

No install step. Requires Python 3.10+, `openpyxl` not required at runtime, and the `claude` CLI on PATH (logged into Max plan).

```bash
cd /Users/fujipeanutbutter/bioidea
python3 bioidea.py --help
```

## Usage

### Start a run

```bash
python3 bioidea.py new --name "BaEV envelope for quiescent CD34+"
# → Created run abcd1234 (BaEV envelope for quiescent CD34+)
```

### Execute stages

```bash
# Run one stage (main + QA)
python3 bioidea.py run abcd1234 --stage 0

# Run just the main phase of a stage
python3 bioidea.py run abcd1234 --stage 0 --phase main

# Run all remaining stages end-to-end
python3 bioidea.py run abcd1234

# Re-run a stage (overwrite existing output)
python3 bioidea.py run abcd1234 --stage 0 --force

# Use a different Claude model alias
python3 bioidea.py run abcd1234 --stage 0 --model sonnet
```

### Inspect

```bash
python3 bioidea.py list                      # all runs
python3 bioidea.py show abcd1234             # stage-by-stage progress + cost
python3 bioidea.py view abcd1234 0 main      # print a stage output
python3 bioidea.py view abcd1234 0 qa
python3 bioidea.py prompts abcd1234 1 main   # dry-run: show what would be sent
```

### Delete

```bash
python3 bioidea.py delete abcd1234 -y
```

## How it works

- **Domain constraint.** `prompts/focus.md` defines the HSC/cytopenia hard constraint plus the longevity flag. It is loaded into the system prompt of every stage so the model cannot drift into industrial enzymes or unrelated modalities.
- **Per-stage prompts.** `prompts/stage{0..6}_{main,qa}.md` hold the persona + task for each of the 14 individual LLM calls. Edit these freely — they're just markdown.
- **Context accumulation.** Each stage receives the full text of every prior stage's main + QA output, concatenated in order. Stage 6 (memo) therefore synthesizes Stages 0–5. QA of stage N gets stage N's main output as its audit target.
- **System prompt.** `SYSTEM_BASE` in `bioidea.py` + the focus preamble. The persona for each stage lives inside the stage markdown, so you can iterate on persona without restarting.
- **Execution.** `claude -p --model opus --output-format json --append-system-prompt <…> --tools ""` — tools are disabled so the stage is a pure reasoning call. Cost + tokens are captured from the JSON result.
- **Persistence.** `bioidea.db` (SQLite) tracks runs + per-stage executions (started/completed timestamps, model, duration, cost). `runs/<short-id>_<slug>/stage{N}_{phase}.md` holds the actual output as YAML-fronted markdown.

## Grounding (lightweight slice of the Grounding Contract)

Every stage output is post-validated by `lib/grounding.py` against the source-tag convention defined in [prompts/grounding.md](prompts/grounding.md) and the broader spec at [docs/grounding-contract.md](docs/grounding-contract.md). Every bulleted factual claim containing a digit or a named acronym must end with a source-tag block:

```
- WT BaEV-TR transduces unstimulated CD34+CD38- HSCs at 10-20% [src: DOI:10.1182/blood.2019000941]
- Vertex Casgevy list price is $2.2M/patient [src: company:Vertex]
- Our R5 titer target of 1e8 TU/mL is a 10x gain over the Expi293 baseline [src: estimate]
```

Supported tag types: `PMID`, `DOI`, `patent`, `biorxiv`, `arxiv`, `clinicaltrials`, `uniprot`, `company` (weak), `url` (weak), `estimate` (weak), `reasoning` (weak).

**Commands:**

```bash
# Validate all stage outputs of a run (also re-runs on every `bioidea run` automatically)
python3 bioidea.py validate <run_id>

# Validate one stage
python3 bioidea.py validate <run_id> --stage 0 --phase main

# Validate and fail the shell on any FAIL (for CI)
python3 bioidea.py validate <run_id> --strict
```

**Output status:**
- `PASS` — every numeric/acronym bullet has a well-formed tag, no warnings.
- `WARN` — all bullets tagged, but some prose sentences with numbers are not tagged (soft signal).
- `FAIL` — at least one numeric bullet is untagged or at least one tag is malformed.

Validation results are stored in:
- `runs/<id>/stage{N}_{phase}.validation.json` — full report with line numbers and findings.
- SQLite columns `grounding_status`, `grounding_tagged`, `grounding_untagged`, `grounding_malformed`, `grounding_strong`, `grounding_weak` on `stage_executions`.

**What this gives you.** A measurable gap between model output and the grounding target, per stage. Baseline pre-contract runs fail with 0% tag coverage; post-contract runs currently land at ~30% on first pass, which is the empirical cost of prompt-only grounding (exactly the failure mode the Grounding Contract was designed to defeat structurally).

**What this does not give you.** Real source verification. The validator checks tag *syntax*, not tag *truth* — a hallucinated PMID with valid format passes. Real verification requires the retrieval-and-validator pipeline described in `docs/grounding-contract.md` (Passage store, PassageHash, schema-constrained synthesis). That is a separate build.

## Excel CMS export

Every `bioidea run` auto-rebuilds `bioidea_export.xlsx` at the repo root — a single-tab "Ideas" sheet with one row per run and ~35 columns covering identity, cost, all 7 stage verdicts, the Stage 6 memo headline (code name, ask, recommendation, VC vote, inflection, the One Thing), grounding status, and a clickable hyperlink to the run's markdown directory.

```bash
# Manual export / backfill (rebuild from current DB state)
python3 bioidea.py export

# Custom output path
python3 bioidea.py export --out /path/to/somewhere.xlsx

# Skip auto-export on a single run
python3 bioidea.py run <id> --no-export

# Skip auto-export globally
BIOIDEA_NO_EXPORT=1 python3 bioidea.py run <id>
```

**Color coding:**
- Green: positive verdicts (FUND, YES, ADVANCE, CLEAR, PROCEED, ROBUST, APPROVE, SAFE TO PROCEED, OPERATIONAL PLAN APPROVED, grounding PASS).
- Amber: cautions / revisions (CAUTION, BRIDGE, REVISE, RECOMMEND CALIBRATION, grounding WARN).
- Red: blocks / kills (PASS-the-deal, NO, TERMINATE, BLOCKED, ABORT, HARD STOP, grounding FAIL).

**Atomic write** — exports go to a temp file in the same directory, then `os.rename`'d into place. Safe to leave the spreadsheet open in Excel during a run; the open handle gets a stale view but won't corrupt.

**Extractor caveats.** Verdicts are pulled by regex from the markdown outputs. Headline fields (target, code name, ask, recommendation, vote, the One Thing, all QA verdicts) extract reliably. A few fields (S1 blocker, S2 assay) are best-effort and will sometimes show table fragments — fixable via prompt convention or a structured-output JSON schema in a later iteration. See `lib/extract.py`.

## Obsidian sync (CMS view in your knowledge base)

Push runs into an Obsidian vault as a self-contained `Bioidea/` subfolder. One-way push, idempotent — re-running over the same vault updates files in place, never duplicates.

```bash
# All runs:
python3 bioidea.py sync-obsidian --vault ~/Documents/MyVault

# One run (id or short prefix):
python3 bioidea.py sync-obsidian e7732b5d --vault ~/Documents/MyVault
```

**Vault layout** under `<vault>/Bioidea/`:

```
_index.md                     ← Dashboard (Dataview tables of runs, grounded outputs, sources)
<run-name>.md                 ← Run hub: summary, links to stages, cited-source list
<run-name>/
  stage{N}_{main,qa}.md       ← Stage artifacts with frontmatter + backlinks to run hub
  stage{N}_grounded.md        ← Grounded outputs (if `bioidea ground` ran)
Sources/
  pubmed-41591869.md          ← One per cited source, deduped across runs
                                "Cited by" backlinks auto-generated
```

**Frontmatter is Dataview-aware** — `_index.md` ships with prebuilt queries:

```dataview
TABLE status, current_stage AS "Stage", total_cost_usd AS "$", focus_profile AS "Focus"
FROM "Bioidea"
WHERE type = "bioidea-run"
SORT created_at DESC
```

Plus tables for grounded outputs (sortable by status), source citation counts, and grounding failures. Treat the vault as a real CMS over your runs.

**Constraint:** the sync only writes inside `<vault>/Bioidea/`. Your other Obsidian content is untouched.

## Tuning

- **Change persona or constraints** → edit `prompts/stage{N}_{phase}.md` or `prompts/focus.md`.
- **Change model** → `--model sonnet` or `--model haiku` per run invocation.
- **Broaden to longevity** → loosen `prompts/focus.md` or author a new focus file and swap it in via a trivial edit to `load_prompt("focus.md")`.
- **Add a multi-provider backend later** → replace `invoke_claude()` in `bioidea.py` with a dispatcher that routes by model string to Anthropic/Gemini/Grok clients. The rest of the pipeline doesn't care.

## Project layout

```
bioidea/
├── bioidea.py                    # CLI
├── prompts/
│   ├── focus.md                  # HSC/cytopenia domain constraint (loaded every stage)
│   ├── stage0_main.md  stage0_qa.md
│   ├── stage1_main.md  stage1_qa.md
│   ├── …
│   └── stage6_main.md  stage6_qa.md
├── runs/
│   └── <short-id>_<slug>/
│       ├── run.json
│       ├── stage0_main.md  stage0_qa.md
│       ├── stage1_main.md  stage1_qa.md
│       ├── …
│       └── stage6_main.md  stage6_qa.md
├── bioidea.db                    # SQLite (runs + stage_executions)
└── README.md
```

## Cost reference (Opus 4, observed on the smoke test)

Stage 0 end-to-end: ~$0.30 (main $0.15 + QA $0.17), ~2.5 min wall time. Extrapolating to all 7 stages (14 calls, growing context): expect **$3–$6 and 25–40 minutes for a full run**. Use `--model sonnet` to cut cost by ~5x at a fidelity tradeoff.
