#!/usr/bin/env python3
"""bioidea — HSC/cytopenia biotech idea-generation workflow.

7-stage pipeline (Visionary → FTO → Scientist → Evo Blueprint → Chemical Logic
→ Lab Ops → Investment Memo), each with a main pass + QA red-team pass.

Each stage shells out to `claude -p` using the user's logged-in Max plan.
Runs are persisted to SQLite + markdown artifacts under runs/<run_id>/.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os  # noqa
import re
import sqlite3
import subprocess
import sys
import uuid
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent
PROMPTS = ROOT / "prompts"
RUNS = ROOT / "runs"
DB_PATH = ROOT / "bioidea.db"

sys.path.insert(0, str(ROOT))
from lib import grounding as _grounding  # noqa: E402
from lib import excel_export as _excel_export  # noqa: E402
from lib import grounded_render as _grounded_render  # noqa: E402

DEFAULT_EXPORT_PATH = ROOT / "bioidea_export.xlsx"

# Path to the grounded-harness binary. Override with $BIOIDEA_HARNESS_BIN.
HARNESS_BIN_DEFAULT = Path.home() / "grounded-harness" / "bin" / "harness"

STAGES = [
    (0, "visionary", "Target Scout"),
    (1, "fto", "IP Gauntlet"),
    (2, "scientist", "Assay Audit"),
    (3, "evo_blueprint", "Objective Function"),
    (4, "chemical_logic", "Chemical Filter"),
    (5, "lab_ops", "Lab Operations"),
    (6, "investment_memo", "Greenlight Memo"),
]
STAGE_NUMS = {n for n, _, _ in STAGES}
STAGE_BY_NUM = {n: (key, label) for n, key, label in STAGES}


# ---------- db ----------

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate_db():
    """Add grounding_* columns to stage_executions if missing (old DBs)."""
    with db() as conn:
        cols = {r["name"] for r in conn.execute("PRAGMA table_info(stage_executions)").fetchall()}
        needed = {
            "grounding_status": "TEXT",
            "grounding_tagged": "INTEGER",
            "grounding_untagged": "INTEGER",
            "grounding_malformed": "INTEGER",
            "grounding_strong": "INTEGER",
            "grounding_weak": "INTEGER",
        }
        for col, ctype in needed.items():
            if col not in cols:
                conn.execute(f"ALTER TABLE stage_executions ADD COLUMN {col} {ctype}")


def init_db():
    with db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS runs (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT NOT NULL,
                created_at TEXT NOT NULL,
                focus_profile TEXT NOT NULL DEFAULT 'hsc_cytopenia',
                current_stage INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'active',
                notes TEXT
            );
            CREATE TABLE IF NOT EXISTS stage_executions (
                run_id TEXT NOT NULL,
                stage INTEGER NOT NULL,
                phase TEXT NOT NULL CHECK (phase IN ('main','qa')),
                started_at TEXT NOT NULL,
                completed_at TEXT,
                model TEXT,
                duration_s REAL,
                cost_usd REAL,
                tokens_in INTEGER,
                tokens_out INTEGER,
                output_path TEXT,
                grounding_status TEXT,
                grounding_tagged INTEGER,
                grounding_untagged INTEGER,
                grounding_malformed INTEGER,
                grounding_strong INTEGER,
                grounding_weak INTEGER,
                PRIMARY KEY (run_id, stage, phase),
                FOREIGN KEY (run_id) REFERENCES runs(id) ON DELETE CASCADE
            );
            """
        )


# ---------- helpers ----------

def slugify(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.strip().lower()).strip("-")
    return s or "run"


def now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def today_stamp() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d")


def run_dir(run_id: str, slug: str) -> Path:
    return RUNS / f"{run_id[:8]}_{slug}"


def load_prompt(name: str) -> str:
    return (PROMPTS / name).read_text()


def get_run(run_id: str):
    with db() as conn:
        row = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
        if row is None:
            # try short-id prefix match
            rows = conn.execute(
                "SELECT * FROM runs WHERE id LIKE ?", (run_id + "%",)
            ).fetchall()
            if len(rows) == 1:
                return rows[0]
            if len(rows) > 1:
                sys.exit(f"Ambiguous run id prefix {run_id!r}. Use `bioidea list`.")
            sys.exit(f"No run matching {run_id!r}. Use `bioidea list`.")
        return row


def find_output_path(run_id: str, stage: int, phase: str):
    with db() as conn:
        row = conn.execute(
            "SELECT output_path FROM stage_executions WHERE run_id=? AND stage=? AND phase=?",
            (run_id, stage, phase),
        ).fetchone()
        return Path(row["output_path"]) if row and row["output_path"] else None


def prior_outputs_context(run_id: str, up_to_stage: int) -> str:
    """Concatenate markdown outputs from all prior stages (main + qa) as context."""
    parts = []
    with db() as conn:
        rows = conn.execute(
            "SELECT stage, phase, output_path FROM stage_executions "
            "WHERE run_id=? AND stage<? AND output_path IS NOT NULL "
            "ORDER BY stage, CASE phase WHEN 'main' THEN 0 ELSE 1 END",
            (run_id, up_to_stage),
        ).fetchall()
    for r in rows:
        p = Path(r["output_path"])
        if not p.exists():
            continue
        key, label = STAGE_BY_NUM[r["stage"]]
        tag = f"Stage {r['stage']} — {label} — {r['phase'].upper()}"
        parts.append(f"\n\n<<<BEGIN {tag}>>>\n\n{p.read_text()}\n\n<<<END {tag}>>>")
    return "".join(parts)


# ---------- claude invocation ----------

def invoke_claude(system_prompt: str, user_prompt: str, model: str = "opus") -> dict:
    """Call `claude -p` non-interactively and return {result, cost_usd, duration_s, ...}.

    Uses --output-format json so we get metadata. The user's stdin gets the user_prompt.
    --append-system-prompt injects the persona/focus.
    """
    cmd = [
        "claude",
        "-p",
        "--model", model,
        "--output-format", "json",
        "--append-system-prompt", system_prompt,
        "--permission-mode", "bypassPermissions",
        "--tools", "",  # disable tools; we just want model reasoning output
    ]
    t0 = dt.datetime.now()
    proc = subprocess.run(
        cmd,
        input=user_prompt,
        capture_output=True,
        text=True,
        timeout=1800,
    )
    duration = (dt.datetime.now() - t0).total_seconds()
    if proc.returncode != 0:
        raise RuntimeError(
            f"claude -p exited {proc.returncode}\nstderr:\n{proc.stderr}\nstdout head:\n{proc.stdout[:2000]}"
        )
    # stdout is a single JSON object
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Non-JSON stdout from claude:\n{proc.stdout[:2000]}") from e
    return {
        "result": data.get("result", ""),
        "cost_usd": data.get("total_cost_usd") or data.get("cost_usd"),
        "tokens_in": (data.get("usage") or {}).get("input_tokens"),
        "tokens_out": (data.get("usage") or {}).get("output_tokens"),
        "duration_s": duration,
        "raw": data,
    }


# ---------- stage execution ----------

SYSTEM_BASE = dedent(
    """\
    You are participating in a structured biotech-idea-generation pipeline focused
    on hematopoietic stem cells (HSCs), cytopenia therapeutics, and longevity-adjacent
    hematopoiesis. Each stage has a distinct persona and a specific deliverable.
    Stay in-persona. Produce markdown. Be concrete, numerate, and adversarial.
    Do not hedge. If the stage prompt asks for a verdict, deliver one.

    A post-pass grounding validator will check your output. You must follow the
    source-tagging rules in the Grounding Contract section below. Unsourced
    numeric bullets will FAIL the stage and force a rerun.
    """
)


def run_stage(run_id: str, stage: int, phase: str, model: str = "opus", force: bool = False) -> Path:
    run = get_run(run_id)
    rdir = run_dir(run["id"], run["slug"])
    rdir.mkdir(parents=True, exist_ok=True)

    out_file = rdir / f"stage{stage}_{phase}.md"
    if out_file.exists() and not force:
        print(f"[skip] {out_file} already exists. Use --force to overwrite.", file=sys.stderr)
        return out_file

    focus = load_prompt("focus.md")
    grounding = load_prompt("grounding.md")
    stage_prompt = load_prompt(f"stage{stage}_{phase}.md")

    # system prompt = base + focus + grounding contract
    system_prompt = f"{SYSTEM_BASE}\n\n---\n\n{focus}\n\n---\n\n{grounding}"

    # user prompt = context from prior stages + this stage's instructions
    # For the QA phase: ONLY show the stage's own MAIN output (keeps context small
    # and avoids dual-use classifier false-positives from cumulative prior context).
    # For the MAIN phase: show all prior stages (main + QA) so later stages can synthesize.
    context_blocks = []
    if phase == "qa":
        main_path = find_output_path(run["id"], stage, "main")
        if not main_path or not main_path.exists():
            sys.exit(f"Stage {stage} main output not found; run main phase first.")
        context_blocks.append(
            f"\n<<<BEGIN Stage {stage} MAIN output to audit>>>\n\n"
            f"{main_path.read_text()}\n\n"
            f"<<<END Stage {stage} MAIN>>>\n"
        )
    else:
        context_blocks.append(prior_outputs_context(run["id"], up_to_stage=stage))

    prior_context = "\n".join(b for b in context_blocks if b)

    user_prompt = dedent(
        f"""\
        # Pipeline run: {run['name']}

        {('## Prior stage outputs (context)\n' + prior_context) if prior_context.strip() else '## No prior stage outputs yet.'}

        ---

        # Current task — Stage {stage} ({phase.upper()})

        {stage_prompt}

        ---

        Produce your deliverable now, in markdown. Stay in-persona.
        """
    )

    with db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO stage_executions "
            "(run_id, stage, phase, started_at, model) VALUES (?,?,?,?,?)",
            (run["id"], stage, phase, now_iso(), model),
        )

    key, label = STAGE_BY_NUM[stage]
    print(f"[run] Stage {stage} {label} — {phase.upper()} (model={model}) …", file=sys.stderr)

    try:
        result = invoke_claude(system_prompt, user_prompt, model=model)
    except Exception as e:
        print(f"[fail] {e}", file=sys.stderr)
        raise

    # Write output markdown
    header = dedent(
        f"""\
        ---
        run: {run['name']}
        run_id: {run['id']}
        stage: {stage}
        stage_key: {key}
        stage_label: {label}
        phase: {phase}
        model: {model}
        generated_at: {now_iso()}
        duration_s: {result['duration_s']:.1f}
        cost_usd: {result['cost_usd']}
        tokens_in: {result['tokens_in']}
        tokens_out: {result['tokens_out']}
        ---

        """
    )
    out_file.write_text(header + (result["result"] or "") + "\n")

    # Run grounding validator post-pass
    vreport = _grounding.validate_markdown(out_file)
    vjson = out_file.with_suffix(".validation.json")
    _grounding.write_json_report(vreport, vjson)

    with db() as conn:
        conn.execute(
            "UPDATE stage_executions SET completed_at=?, duration_s=?, cost_usd=?, "
            "tokens_in=?, tokens_out=?, output_path=?, "
            "grounding_status=?, grounding_tagged=?, grounding_untagged=?, "
            "grounding_malformed=?, grounding_strong=?, grounding_weak=? "
            "WHERE run_id=? AND stage=? AND phase=?",
            (
                now_iso(),
                result["duration_s"],
                result["cost_usd"],
                result["tokens_in"],
                result["tokens_out"],
                str(out_file),
                vreport.status,
                vreport.tagged_bullet_count,
                vreport.untagged_bullet_count,
                vreport.malformed_tag_count,
                vreport.strong_tag_usage,
                vreport.weak_tag_usage,
                run["id"],
                stage,
                phase,
            ),
        )
        # advance current_stage only after both main and qa complete for that stage
        both = conn.execute(
            "SELECT COUNT(*) as c FROM stage_executions WHERE run_id=? AND stage=? AND completed_at IS NOT NULL",
            (run["id"], stage),
        ).fetchone()["c"]
        if both >= 2 and run["current_stage"] <= stage:
            conn.execute("UPDATE runs SET current_stage=? WHERE id=?", (stage + 1, run["id"]))
        if stage == 6 and phase == "qa" and both >= 2:
            conn.execute("UPDATE runs SET status='completed' WHERE id=?", (run["id"],))

    cost = f"${result['cost_usd']:.4f}" if result['cost_usd'] is not None else "?"
    print(
        f"[ok] Stage {stage} {phase} → {out_file.relative_to(ROOT)} "
        f"({result['duration_s']:.1f}s, {cost})  "
        f"grounding={vreport.status} "
        f"[{vreport.tagged_bullet_count}✓/{vreport.untagged_bullet_count}✗/{vreport.malformed_tag_count}!]  "
        f"strong={vreport.strong_tag_usage} weak={vreport.weak_tag_usage}",
        file=sys.stderr,
    )

    # Auto-export to XLSX (idempotent rebuild from DB + disk)
    if not os.environ.get("BIOIDEA_NO_EXPORT"):
        try:
            _excel_export.export_to_xlsx(ROOT, DB_PATH, DEFAULT_EXPORT_PATH)
            print(f"[export] {DEFAULT_EXPORT_PATH.relative_to(ROOT)}", file=sys.stderr)
        except Exception as e:
            print(f"[export-warn] {e}", file=sys.stderr)
    return out_file


# ---------- commands ----------

def cmd_new(args):
    init_db(); migrate_db()
    name = args.name or f"run-{today_stamp()}"
    slug = slugify(name)
    run_id = uuid.uuid4().hex
    rdir = run_dir(run_id, slug)
    rdir.mkdir(parents=True, exist_ok=True)
    with db() as conn:
        conn.execute(
            "INSERT INTO runs (id, name, slug, created_at, focus_profile) VALUES (?,?,?,?,?)",
            (run_id, name, slug, now_iso(), "hsc_cytopenia"),
        )
    # write a run.json for easy navigation
    (rdir / "run.json").write_text(
        json.dumps(
            {"id": run_id, "name": name, "slug": slug, "created_at": now_iso(),
             "focus_profile": "hsc_cytopenia"},
            indent=2,
        )
    )
    print(f"Created run {run_id[:8]} ({name})")
    print(f"  dir: {rdir.relative_to(ROOT)}")
    print(f"\nNext: bioidea run {run_id[:8]} --stage 0")


def cmd_list(args):
    init_db(); migrate_db()
    with db() as conn:
        rows = conn.execute(
            "SELECT id, name, created_at, current_stage, status FROM runs ORDER BY created_at DESC"
        ).fetchall()
    if not rows:
        print("No runs. Start one with `bioidea new --name <name>`.")
        return
    print(f"{'ID':<10}{'CREATED':<22}{'STAGE':<8}{'STATUS':<12}NAME")
    for r in rows:
        print(f"{r['id'][:8]:<10}{r['created_at']:<22}{r['current_stage']:<8}{r['status']:<12}{r['name']}")


def cmd_show(args):
    init_db(); migrate_db()
    run = get_run(args.run_id)
    with db() as conn:
        execs = conn.execute(
            "SELECT * FROM stage_executions WHERE run_id=? ORDER BY stage, phase DESC",
            (run["id"],),
        ).fetchall()
    print(f"Run {run['id'][:8]}  {run['name']}")
    print(f"  created:   {run['created_at']}")
    print(f"  focus:     {run['focus_profile']}")
    print(f"  status:    {run['status']}")
    print(f"  current:   stage {run['current_stage']}")
    print(f"  dir:       {run_dir(run['id'], run['slug']).relative_to(ROOT)}")
    print()
    print(f"{'STAGE':<28}{'MAIN':<24}{'QA':<24}{'$':<10}")
    by_stage = {}
    for e in execs:
        by_stage.setdefault(e["stage"], {})[e["phase"]] = e
    total_cost = 0.0

    def cell(e):
        if not e:
            return "—"
        if not e["completed_at"]:
            return "pending"
        gs = e["grounding_status"]
        if gs is None:
            return "done"
        tagged = e["grounding_tagged"] or 0
        untagged = e["grounding_untagged"] or 0
        malf = e["grounding_malformed"] or 0
        return f"done  {gs}[{tagged}/{untagged}/{malf}]"

    for n, key, label in STAGES:
        row = by_stage.get(n, {})
        main = row.get("main")
        qa = row.get("qa")
        cost = (main["cost_usd"] if main and main["cost_usd"] else 0) + (qa["cost_usd"] if qa and qa["cost_usd"] else 0)
        total_cost += cost
        print(f"{n:<3}{label:<25}{cell(main):<24}{cell(qa):<24}${cost:.4f}")
    print(f"\nTotal cost: ${total_cost:.4f}")
    print("\nGrounding cells read:  status [tagged/untagged/malformed].  Status: PASS / WARN / FAIL.")


def cmd_run(args):
    init_db(); migrate_db()
    if getattr(args, "no_export", False):
        os.environ["BIOIDEA_NO_EXPORT"] = "1"
    run = get_run(args.run_id)
    if args.stage is None:
        # run all remaining stages
        for n, _, _ in STAGES:
            if n < run["current_stage"]:
                continue
            for phase in ("main", "qa"):
                if find_output_path(run["id"], n, phase) and not args.force:
                    continue
                run_stage(run["id"], n, phase, model=args.model, force=args.force)
        return
    if args.stage not in STAGE_NUMS:
        sys.exit(f"Invalid stage {args.stage}. Valid: {sorted(STAGE_NUMS)}")
    phases = (args.phase,) if args.phase != "both" else ("main", "qa")
    for phase in phases:
        run_stage(run["id"], args.stage, phase, model=args.model, force=args.force)


def cmd_view(args):
    init_db()
    run = get_run(args.run_id)
    p = find_output_path(run["id"], args.stage, args.phase)
    if not p or not p.exists():
        sys.exit(f"No output yet for stage {args.stage} {args.phase}")
    print(p.read_text())


def cmd_prompts(args):
    """Print the assembled prompt that would be sent for a given stage/phase (dry run)."""
    init_db()
    run = get_run(args.run_id)
    focus = load_prompt("focus.md")
    stage_prompt = load_prompt(f"stage{args.stage}_{args.phase}.md")
    system_prompt = f"{SYSTEM_BASE}\n\n---\n\n{focus}"
    if args.phase == "qa":
        main_path = find_output_path(run["id"], args.stage, "main")
        main_ctx = main_path.read_text() if main_path and main_path.exists() else "(main not yet run)"
        prior = f"\n<<<BEGIN Stage {args.stage} MAIN>>>\n{main_ctx}\n<<<END>>>\n" + prior_outputs_context(run["id"], args.stage)
    else:
        prior = prior_outputs_context(run["id"], args.stage)
    print("### SYSTEM PROMPT ###\n")
    print(system_prompt)
    print("\n\n### USER PROMPT ###\n")
    print(f"# Run: {run['name']}\n\n{prior}\n\n---\n\n{stage_prompt}")


def _harness_bin() -> str:
    return os.environ.get("BIOIDEA_HARNESS_BIN") or str(HARNESS_BIN_DEFAULT)


def cmd_ground(args):
    """Run a grounded synthesis pass for a stage and persist the artifact.

    Calls `harness grounding cite` (the CitationAgent loop in the
    grounded-harness fork) and writes:
      runs/<id>/stage{N}_grounded.json   — raw GroundedOutput JSON
      runs/<id>/stage{N}_grounded.md     — human-readable rendering

    Existing ungrounded artifacts are NOT touched. Compare side by side.
    """
    init_db(); migrate_db()
    run = get_run(args.run_id)
    rdir = run_dir(run["id"], run["slug"])
    rdir.mkdir(parents=True, exist_ok=True)

    out_json = rdir / f"stage{args.stage}_grounded.json"
    out_md = rdir / f"stage{args.stage}_grounded.md"

    if out_json.exists() and not args.force:
        sys.exit(f"{out_json} exists. Use --force to overwrite.")

    cmd = [
        _harness_bin(),
        "grounding", "cite",
        "--question", args.question,
        "--model", args.model,
        "--limit", str(args.limit),
    ]
    if args.search:
        cmd += ["--search", args.search]
    elif args.passage_ids:
        cmd += ["--passage-ids", args.passage_ids]
    else:
        sys.exit("--search or --passage-ids required")
    if args.db:
        cmd += ["--db", args.db]
    if args.timeout:
        cmd += ["--timeout", args.timeout]

    print(f"[ground] stage {args.stage} — {args.model} — {' '.join(cmd[2:])}", file=sys.stderr)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)

    raw = proc.stdout.strip() or "{}"
    out_json.write_text(raw)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Persist whatever we got; surface the harness's stderr.
        sys.stderr.write(proc.stderr or "")
        sys.exit(f"[fail] non-JSON from harness; saved raw to {out_json.relative_to(ROOT)}")

    md = _grounded_render.render(
        data, run_name=run["name"], stage=args.stage, question=args.question
    )
    out_md.write_text(md)

    status = data.get("status", "?")
    nclaims = len(data.get("claims") or [])
    cost = data.get("cost_usd") or 0.0
    sources = data.get("sources") or {}
    print(
        f"[ground] {status}  claims={nclaims}  sources={len(sources)}  "
        f"${cost:.4f}  → {out_md.relative_to(ROOT)}",
        file=sys.stderr,
    )

    # auto-export Excel unless suppressed
    if not os.environ.get("BIOIDEA_NO_EXPORT"):
        try:
            _excel_export.export_to_xlsx(ROOT, DB_PATH, DEFAULT_EXPORT_PATH)
        except Exception as e:
            print(f"[export-warn] {e}", file=sys.stderr)

    if proc.returncode != 0 or status != "PASS":
        sys.exit(2)


def cmd_export(args):
    """Build / rebuild the Excel CMS file from current DB state."""
    init_db(); migrate_db()
    out = Path(args.out) if args.out else DEFAULT_EXPORT_PATH
    path = _excel_export.export_to_xlsx(ROOT, DB_PATH, out)
    print(f"Exported → {path}")


def cmd_validate(args):
    """Run the grounding validator against existing stage outputs (no LLM calls)."""
    init_db(); migrate_db()
    run = get_run(args.run_id)
    targets = []
    with db() as conn:
        if args.stage is not None:
            phases = (args.phase,) if args.phase != "both" else ("main", "qa")
            for ph in phases:
                row = conn.execute(
                    "SELECT stage, phase, output_path FROM stage_executions "
                    "WHERE run_id=? AND stage=? AND phase=?",
                    (run["id"], args.stage, ph),
                ).fetchone()
                if row and row["output_path"]:
                    targets.append(row)
        else:
            rows = conn.execute(
                "SELECT stage, phase, output_path FROM stage_executions "
                "WHERE run_id=? AND output_path IS NOT NULL ORDER BY stage, phase",
                (run["id"],),
            ).fetchall()
            targets.extend(rows)
    if not targets:
        print("No stage outputs found to validate.")
        return

    any_fail = False
    for row in targets:
        p = Path(row["output_path"])
        if not p.exists():
            print(f"[missing] {p}")
            continue
        r = _grounding.validate_markdown(p)
        vjson = p.with_suffix(".validation.json")
        _grounding.write_json_report(r, vjson)
        with db() as conn:
            conn.execute(
                "UPDATE stage_executions SET grounding_status=?, grounding_tagged=?, "
                "grounding_untagged=?, grounding_malformed=?, grounding_strong=?, grounding_weak=? "
                "WHERE run_id=? AND stage=? AND phase=?",
                (
                    r.status,
                    r.tagged_bullet_count,
                    r.untagged_bullet_count,
                    r.malformed_tag_count,
                    r.strong_tag_usage,
                    r.weak_tag_usage,
                    run["id"],
                    row["stage"],
                    row["phase"],
                ),
            )
        print("=" * 80)
        print(f"Stage {row['stage']} — {row['phase'].upper()}")
        print("=" * 80)
        print(_grounding.summarize(r))
        print()
        if r.status == "FAIL":
            any_fail = True
    if any_fail and args.strict:
        sys.exit(1)


def cmd_delete(args):
    init_db()
    run = get_run(args.run_id)
    rdir = run_dir(run["id"], run["slug"])
    if not args.yes:
        ans = input(f"Delete run {run['id'][:8]} ({run['name']}) and {rdir}? [y/N] ")
        if ans.strip().lower() != "y":
            print("aborted")
            return
    with db() as conn:
        conn.execute("DELETE FROM runs WHERE id=?", (run["id"],))
    if rdir.exists():
        import shutil
        shutil.rmtree(rdir)
    print(f"Deleted {run['id'][:8]}")


# ---------- argparse ----------

def build_parser():
    p = argparse.ArgumentParser(prog="bioidea", description="HSC/cytopenia biotech idea-generation workflow.")
    sub = p.add_subparsers(dest="cmd", required=True)

    new = sub.add_parser("new", help="Create a new run")
    new.add_argument("--name", help="Human-readable name for this run (e.g., 'BaEV envelope for quiescent CD34+').")
    new.set_defaults(func=cmd_new)

    ls = sub.add_parser("list", help="List runs")
    ls.set_defaults(func=cmd_list)

    sh = sub.add_parser("show", help="Show run status and stage progress")
    sh.add_argument("run_id")
    sh.set_defaults(func=cmd_show)

    r = sub.add_parser("run", help="Execute one or more stages of a run")
    r.add_argument("run_id")
    r.add_argument("--stage", type=int, help="0..6; if omitted, runs all remaining stages")
    r.add_argument("--phase", choices=["main", "qa", "both"], default="both")
    r.add_argument("--model", default="opus", help="Claude model alias/id (default: opus)")
    r.add_argument("--force", action="store_true", help="Overwrite existing stage output")
    r.add_argument("--no-export", action="store_true", help="Skip auto-export to XLSX")
    r.set_defaults(func=cmd_run)

    ex = sub.add_parser("export", help="Rebuild the Excel CMS (bioidea_export.xlsx)")
    ex.add_argument("--out", help="Output path (default: bioidea_export.xlsx)")
    ex.set_defaults(func=cmd_export)

    g = sub.add_parser("ground",
                       help="Run a grounded synthesis pass via the harness CitationAgent")
    g.add_argument("run_id")
    g.add_argument("--stage", type=int, required=True, help="0..6")
    g.add_argument("--question", required=True, help="Research question to ground")
    g.add_argument("--search", help="Free-text query for harness passage retrieval")
    g.add_argument("--passage-ids", help="Comma-separated PassageIDs (alt to --search)")
    g.add_argument("--limit", type=int, default=5, help="Max passages to feed the agent")
    g.add_argument("--model", default="opus", help="Claude model (opus/sonnet/haiku)")
    g.add_argument("--db", help="Path to grounding SQLite DB (default: harness's default)")
    g.add_argument("--timeout", help="Harness LLM timeout, e.g. '5m'")
    g.add_argument("--force", action="store_true", help="Overwrite existing grounded artifact")
    g.set_defaults(func=cmd_ground)

    v = sub.add_parser("view", help="Print a stage output")
    v.add_argument("run_id")
    v.add_argument("stage", type=int)
    v.add_argument("phase", choices=["main", "qa"])
    v.set_defaults(func=cmd_view)

    pr = sub.add_parser("prompts", help="Dry-run: print the exact prompts that would be sent")
    pr.add_argument("run_id")
    pr.add_argument("stage", type=int)
    pr.add_argument("phase", choices=["main", "qa"])
    pr.set_defaults(func=cmd_prompts)

    va = sub.add_parser("validate", help="Run the grounding validator on existing stage outputs")
    va.add_argument("run_id")
    va.add_argument("--stage", type=int, help="0..6; if omitted, validates all stages")
    va.add_argument("--phase", choices=["main", "qa", "both"], default="both")
    va.add_argument("--strict", action="store_true", help="Exit non-zero if any FAIL")
    va.set_defaults(func=cmd_validate)

    d = sub.add_parser("delete", help="Delete a run")
    d.add_argument("run_id")
    d.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")
    d.set_defaults(func=cmd_delete)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
