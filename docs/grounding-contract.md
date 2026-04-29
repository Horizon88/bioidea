# Grounding Contract — GGVL Autonomous Research Agent

> Status: Draft v0.1 · Owner: Ed · Handoff target: Joonas, Andre
> Location: docs/grounding-contract.md

## Purpose

Every factual claim emitted by the research agent must be traceable to a specific passage in a specific retrieved document. The agent must be structurally incapable of emitting an unsourced claim. This is not a prompt-engineering target — it is a compile-time and runtime contract enforced at the type boundary between synthesis and emission.

If you take nothing else from this document, take this: **there is no code path from raw LLM output to user-facing text. All LLM output goes through the Validator. The Validator rejects or releases. Nothing else ships.**

## Motivation

GGVL operates on a cockroach/licensing model where scientific rigor is the primary asset. A single fabricated citation in a patent provisional, a CEO brief, or a target discovery memo creates catastrophic downstream risk: patent invalidation, regulatory challenge, investor trust collapse, team erosion. We have already observed this failure mode in human-authored work on the team — it was caught by chance. Autonomous agents hallucinate at rates orders of magnitude higher than humans and produce output faster than any reviewer can keep up with.

Prompt-based mitigations ("please only cite real sources", "do not make up references") have been demonstrated to fail repeatedly in agentic systems. The only robust defense is structural: the pipeline rejects any claim for which citation validation fails, before the claim reaches human eyes.

## Threat model

The contract defends against:

- **Fabricated identifiers** — DOIs, PMIDs, patent numbers that look plausible but do not exist
- **Misattributed claims** — real paper, does not say what the agent claims it says
- **Hallucinated quotes** — text presented as extracted that does not appear in source
- **Stale claims** — source was retracted, corrected, or superseded after ingestion
- **Scope drift** — claim generalizes beyond what the source actually supports
- **Synthetic fabrication** — agent invents a coherent but fictional study

It does not defend against:

- Factually wrong claims correctly cited to factually wrong sources (handled by source curation and downstream review)
- Correct citations to papers with flawed methodology (handled by source quality scoring)
- Semantic misinterpretation by the human reader

## Core types

```go
package grounding

import (
    "context"
    "time"
)

// SourceDocument is an immutable record of content retrieved from a trusted
// source. Once ingested, its ContentHash is the canonical identifier; any
// mutation creates a new SourceDocument.
type SourceDocument struct {
    ID            string    // UUIDv7, generated at ingestion
    SourceSystem  string    // "pubmed", "openalex", "uspto", "epo", "biorxiv", ...
    ExternalID    string    // PMID, DOI, patent number, etc.
    URL           string    // canonical URL for human verification
    Title         string
    Authors       []string
    PublishedAt   time.Time
    RetrievedAt   time.Time
    ContentHash   [32]byte  // sha256 of normalized full text
    ContentLength int       // bytes of normalized text
    Status        DocStatus // Active | Retracted | Superseded | Withdrawn
}

type DocStatus int

const (
    DocActive DocStatus = iota
    DocRetracted
    DocSuperseded
    DocWithdrawn
)

// Passage is a contiguous span of text within a SourceDocument. Passages are
// the atomic unit of citation — every Citation points to exactly one Passage.
type Passage struct {
    ID          string    // UUIDv7
    DocumentID  string    // FK -> SourceDocument.ID
    StartByte   int       // inclusive, into normalized text
    EndByte     int       // exclusive
    Text        string    // redundant with doc[start:end], stored for fast access
    PassageHash [32]byte  // sha256(doc.ContentHash || start || end || Text)
    Embedding   []float32 // populated by retrieval layer
}

// Citation is a claim's link to evidence. It is NEVER constructed directly by
// the LLM — citations are emitted by the retrieval layer with opaque
// PassageIDs, and the LLM references them back by ID only.
type Citation struct {
    PassageID     string    // FK -> Passage.ID; must resolve at validation
    PassageHash   [32]byte  // copy of Passage.PassageHash at synthesis time
    RelevanceSpan *Span     // optional narrower span within Passage.Text
}

type Span struct {
    StartOffset int // relative to Passage.Text
    EndOffset   int
}

// Claim is a single atomic assertion produced by the agent. Claims are not
// emitted directly to downstream consumers; they are emitted to the Validator,
// which rejects or releases them.
type Claim struct {
    ID          string     // UUIDv7
    Text        string     // the claim, in the agent's words
    Citations   []Citation // MUST be non-empty
    Confidence  float32    // agent's self-reported confidence; advisory only
    GeneratedAt time.Time
}

// GroundedOutput is the ONLY type the agent is permitted to return to
// downstream consumers (digest writer, Slack notifier, patent brief composer).
// Constructing a GroundedOutput requires passing the Validator.
type GroundedOutput struct {
    Claims           []Claim
    Narrative        string // prose; every factual sentence contains a [[claim:UUID]] marker
    ValidatedAt      time.Time
    ValidatorVersion string
}
```

`GroundedOutput` is deliberately unexported-constructor — the only way to obtain one is through `Validator.Validate()`. Enforce this via package boundaries (keep the struct field-exported but the constructor unexported, and have the Validator live in the same package).

## Invariants

These MUST hold for every `GroundedOutput` emitted by the system. Each has a corresponding test in `internal/grounding/grounding_test.go`.

- **I1 — No unsourced claims.** For every `Claim c` in `output.Claims`, `len(c.Citations) >= 1`.
- **I2 — Citations resolve.** For every `Citation c`, there exists a `Passage p` in the retrieval store such that `p.ID == c.PassageID`.
- **I3 — Hashes match.** For every resolved Citation, `stored_passage.PassageHash == citation.PassageHash`. Mismatch indicates either corpus drift (serious bug) or the LLM fabricating a plausible-looking hash.
- **I4 — Narrative grounding.** Every factual sentence in `output.Narrative` contains at least one `[[claim:UUID]]` marker referencing a `Claim.ID` present in `output.Claims`. Non-factual sentences (transitions, framing) must be explicitly tagged `[[nonfactual]]`.
- **I5 — Passage text unchanged.** The Passage text referenced by any Citation is byte-identical to the text present at ingestion (verified via PassageHash).
- **I6 — Source document still valid.** The `SourceDocument` referenced transitively by every Citation is `DocActive` — not Retracted, Superseded, or Withdrawn since synthesis.

Violating any invariant causes the Validator to reject the entire `GroundedOutput`. Partial outputs are never released.

## The Validator

```go
type Validator interface {
    // Validate checks a candidate output against all invariants. It returns
    // a GroundedOutput on success or a ValidationError describing every
    // invariant violated. Validation is deterministic and fast — NO LLM calls.
    Validate(ctx context.Context, candidate CandidateOutput) (*GroundedOutput, error)
}

type CandidateOutput struct {
    Claims    []Claim
    Narrative string
}

type ValidationError struct {
    Violations []InvariantViolation
}

type InvariantViolation struct {
    Invariant string // "I1", "I2", ...
    ClaimID   string // which claim triggered it (may be empty for I4)
    Detail    string
}
```

Canonical implementation in `internal/grounding/validator.go`. Requirements:

- Pure function of `(CandidateOutput, PassageStore)`. No LLM calls.
- Deterministic. Given same inputs, same output.
- Fast. Target <50ms for typical 20-claim output. No external API calls.
- Versioned. `ValidatorVersion` in output is the git SHA of the validator package.

## Emission pipeline

The agent's synthesis loop is structured so unsourced emission is impossible by construction:

1. **Retrieval.** Retrieval layer returns a set of Passages from Qdrant. Each Passage is stored with its PassageHash precomputed. The LLM receives passages with opaque `PassageID`s and `PassageHash`es visible in the prompt context. The LLM does not see raw DOIs, PMIDs, or URLs — only opaque IDs. This removes the temptation to fabricate a plausible identifier.

2. **Constrained synthesis.** The LLM is invoked with a JSON schema that requires every Claim to include ≥1 Citation with `PassageID` and `PassageHash`. Schema enforcement path depends on backend:
   - vLLM / SGLang local: XGrammar or outlines — decoder cannot produce output violating schema.
   - Frontier APIs (Claude, GPT) without native grammar: tool-call schema + post-hoc parser rejection (belt and suspenders). Any output that doesn't parse against the schema triggers immediate retry with the parse error in the retry prompt.

3. **Validation.** Validator runs all invariants. On violation, retry or drop per failure-handling rules below.

4. **Emission.** Only `GroundedOutput` (validated) is passed to downstream composers. The digest writer, Slack notifier, and patent brief composer accept only `GroundedOutput`, not `CandidateOutput`. This is enforced at the type level.

The schema used for constrained synthesis is versioned at `schemas/claim_v1.json` and is the source of truth. The Go types above are generated from the schema via `go generate`.

## Failure handling

When validation fails, agent behavior is governed by a retry policy:

- **I1, I4** (unsourced claim / unsourced narrative sentence): retry synthesis once with an explicit instruction listing the violating claim. On second failure, drop the offending claim and emit the remainder with a structured warning appended.
- **I2** (unresolved PassageID): treat as fabrication. Drop the claim. Increment `fabrication_counter` metric with source-system label. If rate exceeds threshold (default: 1% of claims over 1h window), page on-call.
- **I3** (hash mismatch): halt the workflow. Page ops. This indicates either corpus mutation (serious bug) or model misbehavior worth investigating offline before further runs.
- **I5** (passage text drift): same as I3.
- **I6** (retracted source): drop the claim, emit a `source_retracted` event to the source-curation team's inbox, and add the source to the force-refresh queue for re-ingestion.

All validation failures logged with full context (prompt, response, invariant, passages considered) to the eval store for offline analysis. This log is the ground truth for the regression eval tier (see below).

## Eval spec

The grounding contract is only as good as its test suite. Four required tiers:

- **Tier 1 — Unit tests** (`internal/grounding/`). Deterministic tests of each invariant with hand-crafted inputs. Every invariant has ≥3 passing cases and ≥3 violation cases. Run on every PR. Blocks merge on red.

- **Tier 2 — Golden set** (`eval/golden/`). 30 curated queries spanning GGVL domains: CLU/CHIP, p53 circuits, FKBP/FRB switches, synthetic auxotrophy, senolytics, longevity Mendelian randomization, competitive patent monitoring. Each query has: expected claims, expected citations, expected narrative structure. Agent output compared claim-by-claim. Target: 100% invariant compliance, ≥90% claim recall vs. human expert. Run nightly. Regression blocks deploy to prod.

- **Tier 3 — Adversarial set** (`eval/adversarial/`). 20 queries designed to induce hallucination: questions about fictional genes, questions with no good evidence in the corpus, questions that mix real and fake premises, questions that name real researchers but fabricate their conclusions. Agent output MUST either emit only validated claims or return "insufficient evidence" — never fabricate. Target: zero hallucinations over 100 runs. Run nightly. Regression blocks deploy to prod.

- **Tier 4 — Regression set** (`eval/regressions/`). Every production failure that makes it past validation is added as a permanent test case. Never shrinks.

Eval results tracked in Postgres and visualized in Grafana. Model or prompt changes that regress any tier block merge.

## Non-goals

This contract does not:

- Judge the scientific correctness of cited claims (handled by source quality scoring + human review)
- Prevent the agent from citing a correctly-extracted claim from a flawed paper
- Guarantee exhaustive literature coverage (handled by retrieval recall metrics)
- Police narrative style, tone, or framing (handled separately)
- Replace domain expert review for patent filings, regulatory submissions, or CEO briefs — a grounded output is a floor, not a ceiling

## Open questions for Joonas / Andre

1. Should `PassageHash` include the `SourceDocument.ContentHash` transitively, to detect whole-document mutation? Currently drafted as yes. Implementation cost minor. Confirm.
2. For patent claims specifically, should we require two independent citations (different assignees or different source systems) for every legal-status assertion? Argues yes given downstream IP consequences. Decide before first patent workflow ships.
3. Eval compute budget — nightly golden (30q) + adversarial (20q) × 3 model configs × 365 days. Estimate TBD. Budget sign-off from Ed needed before wiring nightly.
4. Do we want a `claim_confidence_threshold` below which claims are dropped even if validated? Model-reported confidence is unreliable but not useless. Proposal: log but don't gate on it until we have calibration data. Agree?
5. For long-horizon autonomous runs (Temporal workflows lasting days), should re-validation fire periodically against the live `SourceDocument.Status` to catch retractions mid-run? Argues yes for anything that touches patents. Confirm pattern.

## Changelog

- **v0.1** (2026-04-23): Initial draft by Ed.
