"""Markdown extractors — pull structured fields out of stage outputs.

Each function takes a markdown string and returns a small dict of fields. All
extractors are tolerant: if a field can't be found they return None or an
empty string. Designed to be cheap (regex only, no LLM) so the auto-exporter
can run after every stage completion.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


# ---------- helpers ----------

def _strip_frontmatter(md: str) -> str:
    """Remove the YAML frontmatter block we inject in stage outputs."""
    if md.startswith("---"):
        # find the second ---
        m = re.search(r"\n---\s*\n", md[3:])
        if m:
            return md[3 + m.end():]
    return md


def _trim(s: Optional[str], n: int = 240) -> str:
    if not s:
        return ""
    s = s.strip()
    if len(s) > n:
        return s[: n - 1].rstrip() + "…"
    return s


def _first_match(pattern: str, text: str, group: int = 1, flags: int = re.IGNORECASE) -> Optional[str]:
    m = re.search(pattern, text, flags)
    if m:
        try:
            return m.group(group).strip()
        except IndexError:
            return m.group(0).strip()
    return None


def _first_paragraph_after(heading_pattern: str, text: str) -> Optional[str]:
    """Return the prose text immediately following a heading or labeled line."""
    m = re.search(heading_pattern, text, re.IGNORECASE)
    if not m:
        return None
    rest = text[m.end():]
    # take everything until the next blank line or next heading
    para = re.split(r"\n\s*\n|\n#+\s", rest, maxsplit=1)[0]
    return para.strip()


def _strip_md(s: str) -> str:
    """Strip simple markdown formatting for cell display."""
    if not s:
        return ""
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", s)
    s = re.sub(r"\[src:[^\]]+\]", "", s)  # drop grounding tags
    return s.strip()


# ---------- per-stage extractors ----------

def stage0_main(md: str) -> dict:
    md = _strip_frontmatter(md)
    # Selected Target — try multiple patterns:
    # (a) **Protein:** **<TARGET>** — common form
    # (b) Selected Target heading then **<TARGET>** on next non-empty line
    target = _first_match(r"\*\*Protein:\*\*\s*\*\*([^\*]{3,300})\*\*", md)
    if not target:
        target = _first_match(
            r"Selected\s+Target[^\n]*\n+(?:\s*\n)*\s*\*\*([^\*]{3,300})\*\*", md
        )
    if not target:
        target = _first_match(r"Selected\s+Target[:\*\s]+\**\s*([^\n*]{3,200})", md)
    if target:
        target = _strip_md(target)
    # Hunter's Thesis — paragraph after the heading
    thesis = _first_paragraph_after(r"Hunter['\u2019]s\s+Thesis[:\*\s]*\n", md)
    thesis = _strip_md(thesis) if thesis else None
    # LGS
    lgs = _first_match(r"LGS[\)\s\*:]*\**\s*(LOW|MED|MEDIUM|HIGH)", md)
    if lgs and lgs.upper() == "MEDIUM":
        lgs = "MED"
    # TAM / pain dollar — broaden to any "$X.X[BMK]" near "TAM" or "pain"
    pain = _first_match(
        r"(?:TAM|Pain Point|pain[^\n]{0,40}|Commercial)[^\n]{0,80}?\$([\d\.,]+\s*[\-–]?\s*[\d\.,]*\s*[BMmKk])",
        md,
    )
    if not pain:
        pain = _first_match(r"\$(\d{1,3}(?:[\.,]\d+)?\s*[\-–]\s*\d{1,3}(?:[\.,]\d+)?\s*[BMmKk])", md)
    return {
        "stage0_target": _trim(target, 120),
        "stage0_thesis": _trim(thesis, 320),
        "stage0_LGS": (lgs or "").upper(),
        "stage0_pain_point_$": _trim(pain, 40),
    }


def stage0_qa(md: str) -> dict:
    md = _strip_frontmatter(md)
    decision = _first_match(r"\b(ADVANCE\s+CANDIDATE[^\.\n]*?)(?:\.|\n|$)", md)
    if not decision:
        decision = _first_match(r"\b(TERMINATE\s+ALL)\b", md)
    return {"stage0_qa_decision": _trim(_strip_md(decision or ""), 120)}


def stage1_main(md: str) -> dict:
    md = _strip_frontmatter(md)
    # Legal verdict — handle backtick-wrapped form: VERDICT: `CAUTION (...)`
    verdict = _first_match(
        r"VERDICT[:\*\s]*[`\"\*]*\s*(CLEAR|CAUTION[^`\"\*\n]{0,80}|BLOCKED[^`\"\*\n]{0,80})",
        md,
    )
    if not verdict:
        verdict = _first_match(
            r"(?:Legal\s+)?Verdict[:\*\s]+[`\"\*]*\s*(CLEAR|CAUTION[^`\"\*\n]{0,80}|BLOCKED[^`\"\*\n]{0,80})",
            md,
        )
    if not verdict:
        verdict = _first_match(r"\b(CLEAR|CAUTION\s*\([^)]+\)|BLOCKED\s*\([^)]+\))\b", md)
    blocker = _first_match(
        r"Blocking\s+(?:Patent\s+)?Holder[s]?[:\*\s]+\**\s*([^\n*]{3,180})", md
    )
    if not blocker:
        # alternative: "Threat: <entity>"
        blocker = _first_match(r"(?:Threat|Patentee|Assignee)[:\*\s]+\**\s*([^\n*]{3,180})", md)
    cost = _first_match(r"(?:Estimated\s+)?Licensing\s+Cost[:\*\s]+\**\s*(Low|Med(?:ium)?|High)", md)
    return {
        "stage1_fto_verdict": _trim(_strip_md(verdict or ""), 80),
        "stage1_blocker": _trim(_strip_md(blocker or ""), 100),
        "stage1_license_cost": (cost or "").title(),
    }


def stage1_qa(md: str) -> dict:
    md = _strip_frontmatter(md)
    score = _first_match(r"Litigation\s+Risk\s+Score[^\n]*?(\d{1,2})", md)
    verdict = _first_match(
        r"(?:Final\s+)?QA\s+Verdict[:\*\s]+\**\s*(SAFE\s+TO\s+PROCEED|HARD\s+STOP[^.\n]{0,80})",
        md,
    )
    if not verdict:
        verdict = _first_match(r"\b(SAFE\s+TO\s+PROCEED|HARD\s+STOP[^\n.]{0,80})", md)
    return {
        "stage1_qa_litigation_risk": score or "",
        "stage1_qa_verdict": _trim(_strip_md(verdict or ""), 80),
    }


def stage2_main(md: str) -> dict:
    md = _strip_frontmatter(md)
    decision = _first_match(
        r"(?:Final\s+)?Stage\s*2\s+Decision[:\*\s]+\**\s*(PROCEED\s+TO\s+BLUEPRINT|ABORT)",
        md,
    )
    if not decision:
        decision = _first_match(r"\b(PROCEED\s+TO\s+BLUEPRINT|ABORT)\b", md)
    assay = _first_match(r"Recommended\s+Primary\s+Assay[:\*\s]+\**\s*([^\n*]{3,180})", md)
    return {
        "stage2_decision": _trim(_strip_md(decision or ""), 60),
        "stage2_assay": _trim(_strip_md(assay or ""), 140),
    }


def stage2_qa(md: str) -> dict:
    md = _strip_frontmatter(md)
    verdict = _first_match(
        r"\b(SAFE\s+TO\s+PROCEED|BRIDGE\s+ASSAY\s+REQUIRED)\b", md
    )
    return {"stage2_qa_verdict": _trim(_strip_md(verdict or ""), 80)}


def stage3_main(md: str) -> dict:
    md = _strip_frontmatter(md)
    throughput = _first_match(r"\b(Low-N|Medium-N)\b[^\n]{0,60}", md)
    name = _first_match(r"Campaign\s+Name[:\*\s]+\**\s*([^\n*]{3,120})", md)
    kill = _first_match(r"Kill\s+Threshold[:\*\s]+\**\s*([^\n*]{3,160})", md)
    return {
        "stage3_throughput": _trim(_strip_md(throughput or ""), 40),
        "stage3_campaign_name": _trim(_strip_md(name or ""), 80),
        "stage3_kill_threshold": _trim(_strip_md(kill or ""), 160),
    }


def stage3_qa(md: str) -> dict:
    md = _strip_frontmatter(md)
    verdict = _first_match(
        r"\b(ROBUST\s+BLUEPRINT|REVISE\s+OBJECTIVE\s+FUNCTION)\b", md
    )
    return {"stage3_qa_verdict": _trim(_strip_md(verdict or ""), 80)}


def stage4_main(md: str) -> dict:
    return {}  # no specific verdict to extract beyond the protocol body


def stage4_qa(md: str) -> dict:
    md = _strip_frontmatter(md)
    verdict = _first_match(
        r"\b(APPROVE\s+PROTOCOL|APPROVE\s+AS-?IS|APPROVE\s+WITH\s+CALIBRATION\s+NOTES|"
        r"RECOMMEND\s+CALIBRATION|RECOMMEND\s+REVISION|LOOSEN\s+HEURISTICS)\b",
        md,
    )
    return {"stage4_qa_verdict": _trim(_strip_md(verdict or ""), 80)}


def stage5_main(md: str) -> dict:
    md = _strip_frontmatter(md)
    # Budget: try multiple patterns
    # (a) markdown table row: **TOTAL** | **$X.XXM**
    budget = _first_match(r"\*\*TOTAL\*\*\s*\|\s*\*\*\$([\d\.,]+\s*[MmBbKk]?)", md)
    # (b) "$X.XXM all-in" or "$X.XXM total"
    if not budget:
        budget = _first_match(r"\$([\d\.,]+\s*[MmBb])\s+(?:all-in|total)", md)
    # (c) "Budget $X.XXM" near top
    if not budget:
        budget = _first_match(
            r"(?:Total\s+Budget|All[-\s]in|Budget(?:\s+impact)?)[^\n]{0,40}?\$([\d\.,]+\s*[MmBbKk]?)",
            md,
        )
    if not budget:
        # fallback: largest $X.XM mention
        candidates = re.findall(r"\$([\d\.]+\s*M)", md)
        if candidates:
            def _to_num(s):
                try:
                    return float(re.sub(r"[^\d\.]", "", s))
                except Exception:
                    return 0
            candidates.sort(key=_to_num, reverse=True)
            budget = candidates[0]
    # Timeline: look for "X weeks" or "Wn" max with "lead nomination" or "POC"
    weeks_m = re.findall(r"\b(\d{1,3})\s*[-–]?\s*week", md, re.IGNORECASE)
    weeks = max(weeks_m, key=lambda w: int(w)) if weeks_m else ""
    return {
        "stage5_budget_$": _trim(budget or "", 30),
        "stage5_timeline_weeks": weeks or "",
    }


def stage5_qa(md: str) -> dict:
    md = _strip_frontmatter(md)
    verdict = _first_match(
        r"\b(OPERATIONAL\s+PLAN\s+APPROVED|REVISE\s+TIMELINE|REJECT\s+PLAN)\b", md
    )
    return {"stage5_qa_verdict": _trim(_strip_md(verdict or ""), 80)}


def stage6_main(md: str) -> dict:
    md = _strip_frontmatter(md)
    code = _first_match(r"(?:Project\s+)?Code\s+Name[:\*\s]+\**\s*([^\n*]{2,80})", md)
    if not code:
        # "**Project Code Name:** **QUIESCO-1**"
        code = _first_match(r"Project[^\n]*?\*\*([A-Z][A-Z0-9\-]{1,30})\*\*", md)
    ask = _first_match(
        r"(?:The\s+)?Ask[:\*\s]+[`\"\*]*\s*\$?([\d\.,]+\s*[MmBbKk]?)",
        md,
    )
    if not ask:
        ask = _first_match(r"(?:Ask|Funding\s+Request)[^\n]{0,40}?\$([\d\.,]+\s*[MmBbKk])", md)
    # inflection: prefer paragraph after "Inflection Milestone" heading
    inflection = _first_paragraph_after(r"(?:Value\s+)?Inflection(?:\s+Milestone)?[:\*\s]+", md)
    if not inflection:
        inflection = _first_match(r"Inflection[^\n]*?:\s*\*\*([^\*]{10,400})", md)
    rec = _first_match(r"(?:Final\s+)?Recommendation[^\n]*?\b(FUND|PASS)\b", md)
    if not rec:
        rec = _first_match(r"^\s*\**\s*(FUND|PASS)\b", md, flags=re.MULTILINE | re.IGNORECASE)
    return {
        "stage6_code_name": _trim(_strip_md(code or ""), 60),
        "stage6_ask_$": _trim(_strip_md(ask or ""), 30),
        "stage6_inflection": _trim(_strip_md(inflection or ""), 240),
        "stage6_recommendation": (rec or "").upper(),
    }


def stage6_qa(md: str) -> dict:
    md = _strip_frontmatter(md)
    vote = _first_match(
        r"\b(YES\s*[—\-–]?\s*RELEASE\s+FUNDS|NO\s*[—\-–]?\s*KILL\s+PROJECT)\b", md
    )
    one = _first_paragraph_after(r"(?:^|\n)#{1,3}\s*The\s+One\s+Thing\s*\n+", md)
    if not one:
        one = _first_paragraph_after(r"One\s+Thing[:\*\s]+", md)
    return {
        "stage6_qa_vote": _trim(_strip_md(vote or ""), 60),
        "stage6_qa_one_thing": _trim(_strip_md(one or ""), 320),
    }


# ---------- aggregator ----------

EXTRACTORS = {
    (0, "main"): stage0_main,
    (0, "qa"): stage0_qa,
    (1, "main"): stage1_main,
    (1, "qa"): stage1_qa,
    (2, "main"): stage2_main,
    (2, "qa"): stage2_qa,
    (3, "main"): stage3_main,
    (3, "qa"): stage3_qa,
    (4, "main"): stage4_main,
    (4, "qa"): stage4_qa,
    (5, "main"): stage5_main,
    (5, "qa"): stage5_qa,
    (6, "main"): stage6_main,
    (6, "qa"): stage6_qa,
}


def extract_run(stage_paths: dict[tuple[int, str], Path]) -> dict:
    """Given a mapping of (stage, phase) -> markdown file path, return a flat dict
    of extracted fields for that run."""
    out: dict = {}
    for (stage, phase), path in stage_paths.items():
        fn = EXTRACTORS.get((stage, phase))
        if not fn or not path or not Path(path).exists():
            continue
        try:
            md = Path(path).read_text()
            out.update(fn(md))
        except Exception as e:
            out[f"stage{stage}_{phase}_extract_error"] = str(e)[:120]
    return out
