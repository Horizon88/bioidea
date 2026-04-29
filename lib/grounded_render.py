"""Markdown renderer for a GroundedOutput JSON returned by `harness grounding cite`.

Input: the full JSON dict (status / claims / narrative / sources / cost / etc.).
Output: a human-readable markdown document with a YAML front-matter block,
       claims grouped with their citations, the narrative (if PASS), and a
       "Sources cited" table.

Pure function — no I/O, no network. Drop-in for bioidea's per-stage artifact
storage convention (next to stage{N}_{phase}.md).
"""
from __future__ import annotations

from typing import Any


def render(data: dict[str, Any], *, run_name: str = "", stage: int | None = None,
           question: str = "") -> str:
    status = data.get("status", "?")
    claims = data.get("claims") or []
    sources = data.get("sources") or {}
    narrative = (data.get("narrative") or "").strip()
    cost = data.get("cost_usd") or 0.0
    duration = data.get("duration_s") or 0.0
    model = data.get("model", "?")
    validator = data.get("validator_version", "?")
    tokens_in = data.get("tokens_in", 0)
    tokens_out = data.get("tokens_out", 0)

    lines = []
    # Front matter
    lines.append("---")
    if run_name:
        lines.append(f"run: {run_name}")
    if stage is not None:
        lines.append(f"stage: {stage}")
    lines.append("phase: grounded")
    lines.append(f"status: {status}")
    lines.append(f"validator: {validator}")
    lines.append(f"model: {model}")
    lines.append(f"cost_usd: {cost:.4f}")
    lines.append(f"duration_s: {duration:.1f}")
    lines.append(f"tokens_in: {tokens_in}")
    lines.append(f"tokens_out: {tokens_out}")
    lines.append("---")
    lines.append("")

    title = f"Stage {stage} — Grounded Output" if stage is not None else "Grounded Output"
    lines.append(f"# {title}")
    lines.append("")
    if question:
        lines.append("**Question:**")
        lines.append(f"> {question}")
        lines.append("")

    # Failure path
    if status != "PASS":
        lines.append("## ⚠️ Validation FAILED")
        lines.append("")
        for v in data.get("violations") or []:
            inv = v.get("invariant", "?")
            cid = v.get("claim_id", "")
            detail = v.get("detail", "")
            tag = f" (claim={cid})" if cid else ""
            lines.append(f"- **{inv}**{tag}: {detail}")
        lines.append("")
        cand = data.get("candidate") or {}
        cand_claims = cand.get("claims") or []
        if cand_claims:
            lines.append("### Rejected candidate output")
            lines.append("")
            for c in cand_claims:
                lines.append(f"- **{c.get('id','')}**: {c.get('text','')}")
                for cit in c.get("citations") or []:
                    lines.append(f"    - passage_id `{cit.get('passage_id','')}`")
            lines.append("")
        return "\n".join(lines)

    # PASS path
    lines.append(f"## Claims ({len(claims)})")
    lines.append("")
    for c in claims:
        cid = c.get("id", "?")
        text = c.get("text", "")
        lines.append(f"### `{cid}` — {text}")
        for cit in c.get("citations") or []:
            pid = cit.get("passage_id", "")
            quote = (cit.get("verbatim_quote") or "").strip()
            src = sources.get(pid) or {}
            sys = src.get("source_system", "?")
            ext = src.get("external_id", "?")
            url = src.get("url", "")
            stitle = (src.get("title") or "").strip()
            authors = src.get("authors") or []
            year = (src.get("published_at") or "")[:4]
            authorline = ""
            if authors:
                first = authors[0]
                more = f" et al." if len(authors) > 1 else ""
                authorline = f"{first}{more} ({year})" if year else f"{first}{more}"
            srcline = f"**Source:** {sys}:{ext}"
            if authorline:
                srcline += f" — {authorline}"
            if url:
                srcline += f" — [{url}]({url})"
            lines.append(f"- {srcline}")
            if stitle:
                lines.append(f"- **Title:** {stitle}")
            if quote:
                lines.append(f"- **Verbatim:** > {quote}")
            lines.append(f"- **PassageID:** `{pid}`")
        lines.append("")

    if narrative:
        lines.append("## Narrative")
        lines.append("")
        lines.append(narrative)
        lines.append("")

    # Sources table
    if sources:
        lines.append("## Sources cited")
        lines.append("")
        lines.append("| # | Source | Title | URL |")
        lines.append("|---|---|---|---|")
        for i, (pid, src) in enumerate(sources.items(), start=1):
            sys = src.get("source_system", "?")
            ext = src.get("external_id", "?")
            url = src.get("url", "")
            title_ = (src.get("title") or "").replace("|", "\\|")[:140]
            lines.append(f"| {i} | {sys}:{ext} | {title_} | {url} |")
        lines.append("")

    return "\n".join(lines)
