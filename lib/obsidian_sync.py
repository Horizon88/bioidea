"""bioidea → Obsidian sync.

Idempotent one-way push from bioidea's SQLite + run artifacts into an Obsidian
vault subfolder. Re-running over the same vault updates files in place and
recomputes source-backlink registries — never duplicates.

Vault layout written under <vault>/Bioidea/:

    _index.md                       — dashboard with Dataview queries
    <run-slug>.md                   — run hub
    <run-slug>/                     — per-run subfolder
        stage{N}_main.md            — stage artifact, with backlinks + frontmatter
        stage{N}_qa.md
        stage{N}_grounded.md        — if `bioidea ground` was run
    Sources/
        <source_system>-<external_id>.md   — one per cited source, deduped

Constraint: this module never writes outside <vault>/Bioidea/. The user's
other Obsidian content is untouched.
"""
from __future__ import annotations

import json
import re
import shutil
import sqlite3
from pathlib import Path
from typing import Any

ROOT_DIR_NAME = "Bioidea"
SOURCES_DIR_NAME = "Sources"


# ---------- helpers ----------

def _slugify(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.strip().lower()).strip("-")
    return s or "run"


def _safe_filename(s: str, max_len: int = 80) -> str:
    """Make a string safe for use as a filename across platforms + Obsidian."""
    s = re.sub(r'[<>:"/\\|?*]', "-", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:max_len].strip("-. ") or "untitled"


def _yaml_block(d: dict[str, Any]) -> str:
    """Tiny YAML emitter — handles flat dicts of scalars + list-of-strings."""
    lines = ["---"]
    for k, v in d.items():
        if v is None:
            continue
        if isinstance(v, list):
            if not v:
                continue
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {_yaml_scalar(item)}")
        else:
            lines.append(f"{k}: {_yaml_scalar(v)}")
    lines.append("---")
    return "\n".join(lines)


def _yaml_scalar(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    # Quote if contains anything YAML-significant
    if any(c in s for c in ":#\n\"'") or s.strip() != s or s == "":
        return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return s


def _strip_existing_frontmatter(md: str) -> str:
    """If a stage markdown already has its own '---' frontmatter, strip it so
    we can write fresh frontmatter without nesting."""
    if md.startswith("---"):
        m = re.search(r"\n---\s*\n", md[3:])
        if m:
            return md[3 + m.end():]
    return md


def _source_key(source_system: str, external_id: str) -> str:
    s = _safe_filename(f"{source_system}-{external_id}", max_len=120)
    return s


# ---------- core ----------

def _fetch_runs(db_path: Path) -> list[dict]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    runs = conn.execute(
        "SELECT id, name, slug, created_at, focus_profile, current_stage, status "
        "FROM runs ORDER BY created_at DESC"
    ).fetchall()
    out = []
    for r in runs:
        execs = conn.execute(
            "SELECT stage, phase, output_path, cost_usd, completed_at, model, "
            "grounding_status, grounding_tagged, grounding_untagged, "
            "grounding_strong, grounding_weak "
            "FROM stage_executions WHERE run_id = ? ORDER BY stage, phase",
            (r["id"],),
        ).fetchall()
        out.append({"run": dict(r), "execs": [dict(e) for e in execs]})
    conn.close()
    return out


def _scan_grounded(run_dir: Path) -> list[dict]:
    """Return list of {stage, json_path, data} for each stage*_grounded.json."""
    out = []
    if not run_dir.exists():
        return out
    for p in sorted(run_dir.glob("stage*_grounded.json")):
        try:
            data = json.loads(p.read_text())
        except Exception:
            continue
        try:
            stage_n = int(p.stem.split("_")[0].replace("stage", ""))
        except Exception:
            continue
        out.append({"stage": stage_n, "json_path": p, "data": data})
    return out


def sync_run(
    repo_root: Path,
    db_path: Path,
    vault: Path,
    run_id: str | None = None,
) -> dict:
    """Sync one run (by id or short prefix) or — if run_id is None — all runs.

    Returns a summary dict for the caller to print.
    """
    bioidea_root = vault / ROOT_DIR_NAME
    sources_dir = bioidea_root / SOURCES_DIR_NAME
    bioidea_root.mkdir(parents=True, exist_ok=True)
    sources_dir.mkdir(parents=True, exist_ok=True)

    records = _fetch_runs(db_path)
    if run_id:
        # short-id prefix match
        candidates = [r for r in records if r["run"]["id"].startswith(run_id)]
        if len(candidates) != 1:
            raise SystemExit(f"Run id prefix {run_id!r} matched {len(candidates)} runs")
        records = candidates

    # Source registry — accumulated across all synced runs so we can write
    # deduped Sources/*.md with full backlink lists at the end.
    source_registry: dict[str, dict] = {}

    runs_written = 0
    stages_written = 0
    grounded_written = 0

    for rec in records:
        run = rec["run"]
        execs = rec["execs"]
        run_slug = _safe_filename(run["name"], max_len=80)
        run_subdir = bioidea_root / run_slug
        run_subdir.mkdir(exist_ok=True)

        # --- per-stage files ---
        stage_links: list[tuple[int, str, str]] = []  # (stage, phase, link)
        local_run_dir = repo_root / "runs" / f"{run['id'][:8]}_{run['slug']}"
        for e in execs:
            if not e.get("output_path"):
                continue
            src = Path(e["output_path"])
            if not src.exists():
                continue
            stage_n = e["stage"]
            phase = e["phase"]
            target_name = f"stage{stage_n}_{phase}.md"
            target = run_subdir / target_name
            body = _strip_existing_frontmatter(src.read_text())
            fm = {
                "type": "bioidea-stage",
                "run": run["name"],
                "run_id": run["id"][:8],
                "stage": stage_n,
                "phase": phase,
                "model": e.get("model") or "",
                "cost_usd": e.get("cost_usd") or 0,
                "completed_at": e.get("completed_at") or "",
                "grounding_status": e.get("grounding_status") or "",
                "tags": ["bioidea", "bioidea-stage", f"stage-{stage_n}", f"phase-{phase}"],
            }
            content = (
                _yaml_block(fm)
                + f"\n\n# Stage {stage_n} {phase.upper()} — {run['name']}\n\n"
                + f"⤴︎ Run hub: [[{run_slug}]]\n\n"
                + body.lstrip("\n")
            )
            target.write_text(content)
            stage_links.append((stage_n, phase, f"{run_slug}/{target.stem}"))
            stages_written += 1

        # --- per-stage grounded artifacts ---
        grounded_records = _scan_grounded(local_run_dir)
        grounded_links: list[tuple[int, str, str]] = []  # (stage, status, link)
        for g in grounded_records:
            stage_n = g["stage"]
            data = g["data"]
            status = data.get("status", "?")
            target_name = f"stage{stage_n}_grounded.md"
            target = run_subdir / target_name

            sources = data.get("sources") or {}
            cited_keys: list[str] = []
            for pid, src in sources.items():
                ssys = src.get("source_system") or "?"
                ext = src.get("external_id") or "?"
                key = _source_key(ssys, ext)
                cited_keys.append(key)
                # Accumulate into registry for later dedup write
                entry = source_registry.setdefault(key, {
                    "source_system": ssys,
                    "external_id": ext,
                    "url": src.get("url") or "",
                    "title": src.get("title") or "",
                    "authors": src.get("authors") or [],
                    "published_at": src.get("published_at") or "",
                    "status": src.get("status") or "Active",
                    "cited_by": set(),
                })
                # backlink: which run/stage cited this source
                entry["cited_by"].add(f"{run_slug}/stage{stage_n}_grounded")
                # Keep the longest title we've seen
                if (src.get("title") or "") and len(src.get("title", "")) > len(entry["title"]):
                    entry["title"] = src.get("title", "")

            fm = {
                "type": "bioidea-grounded",
                "run": run["name"],
                "run_id": run["id"][:8],
                "stage": stage_n,
                "status": status,
                "validator": data.get("validator_version") or "",
                "model": data.get("model") or "",
                "cost_usd": data.get("cost_usd") or 0,
                "claims": len(data.get("claims") or []),
                "sources": len(sources),
                "tags": ["bioidea", "bioidea-grounded", f"stage-{stage_n}",
                         f"grounded-{status.lower()}"],
            }
            # Render the body using the existing renderer (avoid drift)
            from . import grounded_render as _gr
            body = _gr.render(data, run_name=run["name"], stage=stage_n,
                              question=data.get("question", ""))
            # Strip the renderer's own frontmatter
            body = _strip_existing_frontmatter(body)
            # Add Obsidian-style backlinks to the source notes
            backlinks_block = ""
            if cited_keys:
                seen = []
                for k in cited_keys:
                    if k not in seen:
                        seen.append(k)
                backlinks_block = "\n## Source backlinks\n\n" + "\n".join(
                    f"- [[{SOURCES_DIR_NAME}/{k}]]" for k in seen
                ) + "\n"
            content = (
                _yaml_block(fm)
                + f"\n\n# Stage {stage_n} GROUNDED — {run['name']}\n\n"
                + f"⤴︎ Run hub: [[{run_slug}]]\n\n"
                + body.lstrip("\n")
                + backlinks_block
            )
            target.write_text(content)
            grounded_links.append((stage_n, status, f"{run_slug}/{target.stem}"))
            grounded_written += 1

        # --- run hub ---
        total_cost = sum(e.get("cost_usd") or 0 for e in execs)
        hub_path = bioidea_root / f"{run_slug}.md"
        hub_fm = {
            "type": "bioidea-run",
            "run_id": run["id"][:8],
            "run_id_full": run["id"],
            "name": run["name"],
            "created_at": run["created_at"],
            "focus_profile": run["focus_profile"],
            "current_stage": run["current_stage"],
            "status": run["status"],
            "total_cost_usd": round(total_cost, 4),
            "tags": ["bioidea", "bioidea-run", run["focus_profile"]],
        }
        # Build hub body
        body_lines: list[str] = []
        body_lines.append(f"# {run['name']}")
        body_lines.append("")
        body_lines.append(f"**Run id:** `{run['id'][:8]}` &nbsp;&nbsp;**Status:** {run['status']} &nbsp;&nbsp;"
                          f"**Stage:** {run['current_stage']} &nbsp;&nbsp;**Cost:** ${total_cost:.2f}")
        body_lines.append("")
        body_lines.append(f"_Created: {run['created_at']} · Focus: {run['focus_profile']}_")
        body_lines.append("")
        body_lines.append("## Stages")
        body_lines.append("")
        # Group stage_links by stage number
        by_stage: dict[int, dict[str, str]] = {}
        for stage_n, phase, link in stage_links:
            by_stage.setdefault(stage_n, {})[phase] = link
        grounded_by_stage: dict[int, tuple[str, str]] = {}
        for stage_n, status, link in grounded_links:
            grounded_by_stage[stage_n] = (status, link)
        for stage_n in sorted(by_stage.keys() | grounded_by_stage.keys()):
            row = by_stage.get(stage_n, {})
            ground = grounded_by_stage.get(stage_n)
            parts = [f"- **Stage {stage_n}**:"]
            if "main" in row:
                parts.append(f"[[{row['main']}|main]]")
            if "qa" in row:
                parts.append(f"[[{row['qa']}|QA]]")
            if ground:
                gstatus, glink = ground
                marker = "✅" if gstatus == "PASS" else "⚠️" if gstatus == "WARN" else "❌"
                parts.append(f"{marker} [[{glink}|grounded]]")
            body_lines.append(" ".join(parts))
        body_lines.append("")
        body_lines.append("## Cited sources")
        body_lines.append("")
        run_sources = sorted({k for k, v in source_registry.items()
                              if any(b.startswith(f"{run_slug}/") for b in v["cited_by"])})
        if run_sources:
            for k in run_sources:
                meta = source_registry[k]
                title = meta.get("title") or k
                body_lines.append(f"- [[{SOURCES_DIR_NAME}/{k}|{meta['source_system']}:{meta['external_id']}]] — {title}")
        else:
            body_lines.append("_No grounded outputs yet for this run. "
                              "Run `bioidea ground <run_id> --stage N --question \"...\" --search \"...\"`._")
        body_lines.append("")
        hub_path.write_text(_yaml_block(hub_fm) + "\n\n" + "\n".join(body_lines))
        runs_written += 1

    # --- write deduped Sources/*.md ---
    for key, meta in source_registry.items():
        target = sources_dir / f"{key}.md"
        cited_by_links = sorted(meta["cited_by"])
        fm = {
            "type": "bioidea-source",
            "source_system": meta["source_system"],
            "external_id": meta["external_id"],
            "url": meta["url"],
            "published_at": meta["published_at"],
            "status": meta["status"],
            "tags": ["bioidea", "bioidea-source", meta["source_system"]],
        }
        lines = [_yaml_block(fm), "", f"# {meta['title'] or key}", ""]
        if meta["authors"]:
            lines.append("**Authors:** " + ", ".join(meta["authors"]))
        if meta["url"]:
            lines.append(f"**URL:** {meta['url']}")
        lines.append(f"**Source:** `{meta['source_system']}:{meta['external_id']}` · status: {meta['status']}")
        if meta["published_at"]:
            lines.append(f"**Published:** {meta['published_at']}")
        lines.append("")
        lines.append("## Cited by")
        lines.append("")
        for link in cited_by_links:
            lines.append(f"- [[{link}]]")
        target.write_text("\n".join(lines) + "\n")

    # --- _index.md (dashboard) ---
    index_path = bioidea_root / "_index.md"
    index_fm = {
        "type": "bioidea-index",
        "tags": ["bioidea", "bioidea-index"],
    }
    index_body = """
# Bioidea — runs dashboard

## Runs

```dataview
TABLE
  status AS "Status",
  current_stage AS "Stage",
  total_cost_usd AS "$",
  focus_profile AS "Focus",
  created_at AS "Created"
FROM "Bioidea"
WHERE type = "bioidea-run"
SORT created_at DESC
```

## Grounded outputs

```dataview
TABLE
  run AS "Run",
  stage AS "Stage",
  status AS "Status",
  claims AS "Claims",
  sources AS "Sources",
  cost_usd AS "$",
  validator AS "Validator"
FROM "Bioidea"
WHERE type = "bioidea-grounded"
SORT status DESC, stage ASC
```

## Sources cited

```dataview
TABLE
  source_system AS "System",
  external_id AS "ID",
  status AS "Status",
  length(file.inlinks) AS "Cited by"
FROM "Bioidea/Sources"
WHERE type = "bioidea-source"
SORT length(file.inlinks) DESC
```

## Stage failures (grounding FAIL)

```dataview
LIST
FROM "Bioidea"
WHERE type = "bioidea-grounded" AND status = "FAIL"
SORT file.mtime DESC
```
""".strip()
    index_path.write_text(_yaml_block(index_fm) + "\n\n" + index_body + "\n")

    return {
        "vault_root": str(bioidea_root),
        "runs": runs_written,
        "stages": stages_written,
        "grounded": grounded_written,
        "sources": len(source_registry),
    }
