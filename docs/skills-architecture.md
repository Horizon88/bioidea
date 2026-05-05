# bioidea skills architecture (proposal)

> Status: design v0.1 · written 2026-05-05 to support the pipeline → skills pivot

## Problem

bioidea's 14-stage HSC-locked pipeline is the wrong shape for ad-hoc venture
work, as proven by the muscle/GLP-1 + klotho-FTO + IC-Chair chain we just ran.
Symptoms:

1. **Three distinct ROLES** spawned in one session (Longevity Venture Analyst,
   Senior Patent Counsel, Managing Partner / IC Chair). Each is a hand-rolled
   system prompt + prompt body + invocation flag set. Zero reuse.
2. **The 14 stage prompts in `prompts/stage{0..6}_{main,qa}.md`** are locked to
   HSC/cytopenia by `prompts/focus.md` — useless for muscle, longevity,
   metabolic, CNS programs without rewriting `focus.md`.
3. **Each ROLE is a copy of the same scaffolding**: persona definition,
   confidence flagging discipline, output format spec, claude `-p` invocation
   flags (`--system-prompt`, `--max-turns 1`, `--tools ""`). Same boilerplate
   four times.
4. **No composition.** The IC-Chair v3 prompt had to manually paste the FTO
   opinion's findings into its own context; if either output changes, the
   downstream prompt drifts silently.
5. **No reusability across programs.** The Senior Patent Counsel role is
   exactly the right shape for the next program GGVL discovers (or any
   biotech FTO question). It currently lives as a one-off Markdown file in
   `research/klotho-fto/prompt.md`.

## Design

### Core abstraction: a Skill is an invocable, named, composable unit

A **Skill** is:

```
skills/<name>/
  SKILL.md          # Manifest: persona, inputs, outputs, model, grounding policy
  prompt.md         # The user-prompt body (what gets piped in)
  system.md         # The system prompt (full-replacement, not append)
  schema.json       # (optional) JSON Schema for structured output
  examples/         # (optional) example invocation + expected output
```

Every Skill exposes a single CLI invocation:

```bash
bioidea skill <name> [--input KEY=VALUE ...] [--input-file PATH] \
                    [--model opus|sonnet|haiku] [--out PATH]
```

Internally, `bioidea skill` does:

1. Load `skills/<name>/SKILL.md` (frontmatter manifest).
2. Build the system prompt from `skills/<name>/system.md`, with template
   substitution from `--input` values + program-state context.
3. Build the user prompt from `skills/<name>/prompt.md`, same substitution.
4. Invoke `claude -p --model <model> --output-format json --system-prompt
   "$system" --tools "" --max-turns 1` (the pattern we proved out in v2/v3).
5. If `schema.json` exists, pass `--json-schema "$(cat schema.json)"`.
6. Persist the raw envelope JSON + the `result` text to a versioned location
   under `runs/<run_id>/skills/<skill_name>/<timestamp>.{json,md}`.
7. Update SQLite + Excel CMS as we already do for stages.
8. If the Skill declares `grounding_required: true` in its manifest, route
   through `lib/citation_agent.py` (the harness CitationAgent flow we already
   built) instead of bare `claude -p`.

### Manifest format (SKILL.md frontmatter)

```yaml
---
name: fto-opinion
display_name: "FTO Opinion (Senior Patent Counsel)"
version: 0.1
description: |
  Produce a focused Freedom-to-Operate opinion on a specified mechanism +
  modality, including drafted provisional patent claims with adversarial
  stress tests.
role: senior-patent-counsel
model_default: opus
inputs:
  - name: mechanism
    description: "The therapeutic mechanism (e.g., 'α-klotho × FKBP/FRB conditional control')"
    required: true
  - name: indications
    description: "Co-lead disease anchors (CSV)"
    required: true
  - name: modality_default
    description: "biologic | small-molecule | gene-therapy | cell-therapy"
    default: biologic
  - name: jurisdictions
    description: "us | us+ep | us+ep+jp+cn"
    default: us+ep
outputs:
  format: markdown
  schema: null    # FTO is too text-rich for JSON schema enforcement
  expected_length_words: [4000, 8000]
grounding_required: false   # Patents are PatSnap territory, not our PubMed corpus
red_team_skill: fto-opinion-red-team   # The QA pass (separate skill)
provenance:
  proven_in_run: "klotho-fto/opinion-v1.md (commit ae46c23)"
  cost_typical_usd: 0.59
  duration_typical_seconds: 346
---
```

### The catalog (initial proposal)

Three layers:

**Layer 1 — Roles** (the persona definitions, reusable across skills)

```
roles/
  longevity-venture-analyst.md       # v1, v2 prompts proved this
  senior-patent-counsel.md           # FTO opinion proved this
  managing-partner-ic-chair.md       # v3 sharpening proved this
  ruthless-target-scout.md           # bioidea Stage 0 main
  red-team-auditor.md                # bioidea Stage 0 QA, generalizable
  hostile-patent-litigator.md        # bioidea Stage 1 QA
  assay-development-scientist.md     # bioidea Stage 2 main
  translational-medicine-lead.md     # bioidea Stage 2 QA
  evolutionary-blueprint-scientist.md # bioidea Stage 3 main
  data-science-skeptic.md            # bioidea Stage 3 QA
  computational-chemist.md           # bioidea Stage 4 main
  directed-evolution-scientist.md    # bioidea Stage 4 QA
  lab-operations-director.md         # bioidea Stage 5 main
  biomanufacturing-logistics-pm.md   # bioidea Stage 5 QA
```

**Layer 2 — Skills** (the actual invocable units, can reference roles)

Discovery skills:
- `target-scout` — given a domain, propose ranked candidate targets. Uses role: `ruthless-target-scout`.
- `commercial-quantify` — TAM, named programs, $ pain quantification. Uses role: `longevity-venture-analyst`.
- `competitor-scan` — who's working on this, where in pipeline, BD activity.
- `venture-discovery` — the v1/v2 muscle/GLP-1 discovery shape. Uses role: `longevity-venture-analyst`.

IP skills:
- `fto-opinion` — the focused FTO we just ran. Uses role: `senior-patent-counsel`.
- `fto-red-team` — the hostile-litigator audit. Uses role: `hostile-patent-litigator`.
- `provisional-claim-draft` — extract just the claim-drafting from FTO; useful standalone.

Assay skills:
- `primary-assay-design`
- `bridge-assay-design`
- `assay-reality-gap-audit`

Evolution skills:
- `fitness-equation-design`
- `metric-gaming-audit`
- `chemical-filter-design`
- `chemical-filter-calibrate`

Operations skills:
- `campaign-roadmap`
- `bottleneck-audit`

Decision skills:
- `investment-memo-compose` — the bioidea Stage 6 main, generalized.
- `ic-chair-sharpening` — the v3 sharpening flow we just proved. Uses role: `managing-partner-ic-chair`.
- `ic-final-vote` — the bioidea Stage 6 QA.

**Layer 3 — Workflows** (declarative ordered compositions)

```yaml
# workflows/bioidea-classic.yaml — the original 14-stage HSC pipeline
name: bioidea-classic
description: "The original 14-stage HSC/cytopenia pipeline."
focus: hsc-cytopenia
steps:
  - { skill: target-scout, label: stage-0-main }
  - { skill: target-scout-red-team, label: stage-0-qa }
  - { skill: fto-opinion, label: stage-1-main }
  - { skill: fto-red-team, label: stage-1-qa }
  ... etc
```

```yaml
# workflows/venture-decision.yaml — the muscle/GLP-1 chain we just ran
name: venture-decision
description: "Discovery → broader-frame discovery → focused FTO → IC sharpening → vote."
steps:
  - { skill: venture-discovery, inputs: { framing: narrow }, label: v1 }
  - { skill: venture-discovery, inputs: { framing: broad, contrast_with: v1 }, label: v2 }
  - { skill: fto-opinion, inputs: { mechanism: "{{ v2.top_candidate.mechanism }}" }, label: fto }
  - { skill: ic-chair-sharpening, inputs: { candidates: "{{ v2.top_3 }}", fto: "{{ fto }}" }, label: v3 }
```

### Templating — making composition real

The `{{ v2.top_candidate.mechanism }}` syntax is what makes workflows compose
without hand-pasting. Implementation:

- After each skill runs, its output is parsed (markdown frontmatter + body, or
  JSON schema-validated) and stored in a `WorkflowState` dict.
- Subsequent steps' input values can reference prior steps' outputs via
  Jinja2-style `{{ <step_label>.<field> }}` expressions.
- Skills that produce structured output (via JSON Schema) expose typed fields;
  text-only skills expose `.body` as the entire markdown text.

Run `bioidea workflow run venture-decision --inputs initial_question="muscle ×
GLP-1"` and the four LLM calls execute in sequence, each receiving the
upstream context automatically.

### Migration strategy

**Phase 1 (this session if time):** scaffolding only — `bioidea skill` CLI,
`SKILL.md` parser, dispatcher, persistence to runs/. Zero new content; we
prove the framework with **three skills carved from work we already have**:

1. `venture-discovery` — extracted from `research/muscle-glp1-discovery/prompt-v2-broader.md`
2. `fto-opinion` — extracted from `research/klotho-fto/prompt.md`
3. `ic-chair-sharpening` — extracted from `research/muscle-glp1-discovery/prompt-v3-sharpening.md`

These three skills mean any next program can reproduce the muscle → klotho →
IC-vote chain by name, without copy-pasting prompt files.

**Phase 2 (separate session):** carve the 14 bioidea stage prompts into their
underlying ~20 atomic skills. Build `workflows/bioidea-classic.yaml`. Verify
it produces the same output shape as the old `bioidea run` command.

**Phase 3 (later):** templating, workflow runner, more skills, retire the old
hardcoded pipeline.

## What stays vs. what changes

**Unchanged:**
- The harness fork (`grounded-harness`) with its Validator and Passage store.
  Skills that need grounding declare it in their manifest; the dispatcher
  routes through `lib/citation_agent.py`.
- The Excel export and Obsidian sync. Both already operate on
  `runs/<run_id>/...` artifacts; skills will write into the same directory
  shape with a `skills/` subfolder.
- The 14 bioidea stage prompts, until Phase 2 carves them. The pipeline can
  coexist with the new `bioidea skill` CLI.

**Changes:**
- New `skills/` and `roles/` directories at the repo root.
- New `bioidea skill <name>` CLI command.
- New `SKILL.md` manifest format.
- (Phase 2+) New `workflows/` directory + `bioidea workflow run` command.

**Decisions still open:**
- Should `roles/*.md` be a separate concept or just a section in `SKILL.md`?
  My instinct: separate — same role can serve multiple skills.
- Should grounding-required skills emit a `GroundedOutput` only, or also
  produce the ungrounded markdown alongside? My instinct: both, with the
  grounded version as the primary artifact.
- Should the dispatcher support tool-use skills (e.g., a future skill that
  uses harness tools)? My instinct: not in Phase 1; revisit when needed.
