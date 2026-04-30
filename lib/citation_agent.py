"""Python-side CitationAgent — synthesizes a CandidateOutput from retrieved
passages by shelling out to `claude -p --json-schema`, then pipes the
candidate JSON to `harness grounding validate` for the seven-invariant check.

Lives here (not in the Go harness) because Go's exec.Command for `claude -p`
gets SIGKILLed by the macOS sandbox when the harness binary runs as a
grandchild of a Claude Code agent session, while Python's subprocess.run
does not. Same prompt + same JSON Schema + same Validator semantics.

Architecture:

    bioidea Python                    harness (Go)
    ┌──────────────────┐              ┌────────────────────────┐
    │  cmd_ground      │              │  grounding search      │
    │     │            │ ───────────▶ │  (pure-Go retrieval)   │
    │     ▼            │              └────────────────────────┘
    │  build system    │
    │  prompt with     │              ┌────────────────────────┐
    │  passages        │              │  claude -p             │
    │     │            │ ───────────▶ │  --json-schema         │
    │     ▼            │              │  (the only LLM call)   │
    │  parse candidate │              └────────────────────────┘
    │     │            │
    │     ▼            │              ┌────────────────────────┐
    │  pipe to         │ ───────────▶ │  grounding validate    │
    │  validate        │              │  (pure-Go 7 invariants)│
    │     │            │              └────────────────────────┘
    │     ▼            │
    │  GroundedOutput  │
    └──────────────────┘
"""
from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any


# JSON Schema enforced via `claude -p --json-schema`. Identical shape to the
# harness Go-side schema in cite.go.
CITATION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["claims"],
    "properties": {
        "claims": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "text", "citations"],
                "properties": {
                    "id": {"type": "string", "minLength": 1, "maxLength": 64},
                    "text": {"type": "string", "minLength": 1},
                    "citations": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["passage_id", "passage_hash"],
                            "properties": {
                                "passage_id": {"type": "string", "minLength": 1},
                                "passage_hash": {
                                    "type": "string",
                                    "pattern": "^[0-9a-fA-F]{64}$",
                                },
                                "verbatim_quote": {"type": "string"},
                            },
                        },
                    },
                },
            },
        },
        "narrative": {"type": "string"},
    },
}


CITATION_SYSTEM = """You are the CitationAgent in a grounded research harness.

Your task: answer the user's question by emitting a CandidateOutput with one
or more atomic Claims, where every Claim is supported by at least one Citation
referencing one of the Passages provided to you.

OUTPUT FORMAT — STRICT:
- Output ONLY a single JSON object. No prose. No commentary. No markdown
  fences. The first character of your output MUST be '{' and the last MUST
  be '}'.

Strict content rules — every output is post-validated by a 7-invariant
Validator; violations are rejected wholesale:

1. You may ONLY cite Passages from the "Available passages" block in this
   prompt. If a Passage is not listed there, you do not have it.
2. Every passage_hash you emit MUST be the exact hex hash shown for that
   PassageID in the prompt. Do NOT invent or modify hashes.
3. If you include a verbatim_quote, it MUST be a literal substring of the
   passage text shown.
4. If the available passages do not support a claim, OMIT the claim. Returning
   a partial-but-grounded answer is correct; fabricating a citation is failure.
5. Keep each Claim atomic — one assertion per claim.
6. Use opaque PassageIDs only. Do NOT include DOIs, PMIDs, URLs, or author
   names in claim text.
7. NARRATIVE IS OPTIONAL. If you include a "narrative" field, every factual
   sentence in it MUST end with at least one [[claim:ID]] marker that points
   to a Claim.id you defined above. Pure framing/transition sentences MUST
   end with [[nonfactual]]. If you cannot reliably tag every sentence, OMIT
   the narrative — return only "claims" and skip "narrative" entirely.

Begin output with '{' now."""


def _harness_bin() -> str:
    return os.environ.get("BIOIDEA_HARNESS_BIN") or str(
        Path.home() / "grounded-harness" / "bin" / "harness"
    )


def search(query: str, *, limit: int = 5, db: str | None = None) -> list[dict]:
    """Call `harness grounding search --json` and return parsed hits."""
    cmd = [
        _harness_bin(), "grounding", "search",
        "--query", query,
        "--limit", str(limit),
        "--json",
    ]
    if db:
        cmd += ["--db", db]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError(f"harness search failed: {proc.stderr}")
    return json.loads(proc.stdout)


def _build_system_prompt(hits: list[dict]) -> str:
    lines = [CITATION_SYSTEM, "", "Available passages (you may only cite from these):", ""]
    for h in hits:
        pid = h.get("passage_id", "")
        phash = h.get("passage_hash", "")
        text = (h.get("text") or "").replace("\n", " ")
        lines.append(f"[{pid}] hash={phash}")
        lines.append(f"text: {text}")
        lines.append("")
    return "\n".join(lines)


def _invoke_claude(question: str, system_prompt: str, *, model: str = "opus",
                   timeout_s: int = 300) -> dict:
    """Call `claude -p --json-schema` and return the envelope dict."""
    schema_str = json.dumps(CITATION_SCHEMA)
    cmd = [
        "claude", "-p",
        "--model", model,
        "--output-format", "json",
        "--json-schema", schema_str,
        "--append-system-prompt", system_prompt,
        "--permission-mode", "bypassPermissions",
        "--tools", "",
    ]
    user = (
        f"Question: {question}\n\n"
        "Produce a JSON CandidateOutput now. Cite only the passages listed above."
    )
    t0 = time.monotonic()
    proc = subprocess.run(
        cmd, input=user, capture_output=True, text=True, timeout=timeout_s
    )
    duration = time.monotonic() - t0
    if not proc.stdout:
        raise RuntimeError(
            f"claude -p returned no stdout (exit={proc.returncode})\n"
            f"stderr: {proc.stderr[:600]}"
        )
    env = json.loads(proc.stdout)
    env["_duration_s"] = duration
    return env


def _validate(candidate: dict, *, db: str | None = None) -> dict:
    """Pipe a CandidateOutput JSON through `harness grounding validate`."""
    cmd = [_harness_bin(), "grounding", "validate"]
    if db:
        cmd += ["--db", db]
    proc = subprocess.run(
        cmd, input=json.dumps(candidate), capture_output=True, text=True, timeout=30
    )
    return json.loads(proc.stdout) if proc.stdout else {"status": "ERROR", "detail": proc.stderr}


def _hits_to_sources(hits: list[dict]) -> dict[str, dict]:
    """Build a passage_id -> source-metadata map for downstream rendering."""
    out: dict[str, dict] = {}
    for h in hits:
        pid = h.get("passage_id", "")
        if not pid:
            continue
        out[pid] = {
            "source_system": h.get("source_system", ""),
            "external_id": h.get("external_id", ""),
            "url": h.get("url", ""),
            "title": h.get("title", ""),
        }
    return out


def cite(
    question: str,
    *,
    search_query: str | None = None,
    passage_ids: list[str] | None = None,
    limit: int = 5,
    model: str = "opus",
    db: str | None = None,
    timeout_s: int = 300,
) -> dict:
    """End-to-end CitationAgent flow.

    Returns a dict with the same shape as `harness grounding cite` so the
    bioidea renderer doesn't care which path produced it. Always includes
    a "sources" field keyed by passage_id (built from search hits).
    """
    if search_query and passage_ids:
        raise ValueError("provide search_query or passage_ids, not both")
    if not search_query and not passage_ids:
        raise ValueError("provide search_query or passage_ids")

    if search_query:
        hits = search(search_query, limit=limit, db=db)
    else:
        # Build hits directly from passage_ids using harness query.
        hits = []
        for pid in passage_ids or []:
            cmd = [_harness_bin(), "grounding", "query", "--passage-id", pid]
            if db:
                cmd += ["--db", db]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if proc.returncode != 0:
                continue
            d = json.loads(proc.stdout)
            p, s = d["passage"], d["source"]
            hits.append({
                "passage_id": p["id"],
                "passage_hash": p["passage_hash"],
                "text": p["text"],
                "score": 1.0,
                "source_system": s["source_system"],
                "external_id": s["external_id"],
                "url": s["url"],
                "title": s["title"],
            })

    if not hits:
        return {
            "status": "ERROR",
            "detail": "no passages retrieved (try a different --search or ingest more)",
            "model": model,
        }

    system_prompt = _build_system_prompt(hits)

    try:
        env = _invoke_claude(question, system_prompt, model=model, timeout_s=timeout_s)
    except Exception as e:
        return {"status": "ERROR", "detail": str(e), "model": model}

    if env.get("is_error"):
        return {
            "status": "ERROR",
            "detail": f"claude error stop_reason={env.get('stop_reason')} api_status={env.get('api_error_status')}",
            "raw": env.get("result", "")[:600],
            "model": model,
        }

    # The schema-enforced output lives in structured_output; result may be empty.
    candidate = env.get("structured_output")
    if isinstance(candidate, str):
        candidate = json.loads(candidate)
    if not candidate or candidate == {}:
        # Fallback: parse `result` text as JSON
        try:
            candidate = json.loads(env.get("result") or "{}")
        except json.JSONDecodeError:
            return {
                "status": "ERROR",
                "detail": "claude returned no structured_output and result was non-JSON",
                "raw": (env.get("result") or "")[:600],
                "model": model,
            }

    # Pipe through the harness validator (pure Go, no claude).
    val = _validate(candidate, db=db)

    out: dict[str, Any] = {
        "model": model,
        "cost_usd": env.get("total_cost_usd", 0.0),
        "duration_s": env.get("_duration_s", 0.0),
        "tokens_in": (env.get("usage") or {}).get("input_tokens", 0),
        "tokens_out": (env.get("usage") or {}).get("output_tokens", 0),
        "question": question,
        "sources": _hits_to_sources(hits),
    }

    status = val.get("status", "?")
    if status == "PASS":
        out.update({
            "status": "PASS",
            "validator_version": val.get("validator_version", "?"),
            "claims": candidate.get("claims") or [],
            "narrative": candidate.get("narrative", ""),
        })
    else:
        out.update({
            "status": status,
            "violations": val.get("violations") or [],
            "candidate": candidate,
        })
    return out
