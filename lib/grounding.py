"""bioidea grounding validator — lightweight post-pass check on stage outputs.

Implements a deliberately-narrow slice of the Grounding Contract (see
docs/grounding-contract.md). No retrieval corpus, no hash verification, no
passage store — just a markdown post-pass that:

1. Identifies factual-looking bullets (contain a digit or a named acronym).
2. Requires every such bullet to end with a `[src: <tag>, ...]` block.
3. Validates tag syntax against a registry of allowed types.
4. Emits a machine-readable JSON report plus a human-readable summary.

This raises the bar on fabrication far above prompt-only mitigations without
requiring the full Passage/Validator/PassageHash pipeline described in the
Grounding Contract. It is NOT a substitute for that pipeline before any output
reaches a patent provisional, CEO brief, or investor memo.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional

# ---------- tag grammar ----------

# Individual source-tag patterns. Each regex matches one tag inside a [src: ...] list.
TAG_PATTERNS = {
    "PMID": re.compile(r"^PMID:\s*(\d{1,9})$", re.IGNORECASE),
    "DOI": re.compile(r"^DOI:\s*(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)$", re.IGNORECASE),
    "patent": re.compile(r"^patent:\s*([A-Z]{2}\d{4,12}[A-Z0-9]{0,3})$", re.IGNORECASE),
    "biorxiv": re.compile(r"^biorxiv:\s*(\d{4}\.\d{2}\.\d{2}\.\d{6,})$", re.IGNORECASE),
    "arxiv": re.compile(r"^arxiv:\s*(\d{4}\.\d{4,6}(v\d+)?)$", re.IGNORECASE),
    "clinicaltrials": re.compile(r"^clinicaltrials:\s*(NCT\d{8})$", re.IGNORECASE),
    "uniprot": re.compile(r"^uniprot:\s*([OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2})$"),
    "company": re.compile(r"^company:\s*([A-Za-z0-9][A-Za-z0-9_\-\.]{0,64})$"),
    "url": re.compile(r"^url:\s*(https?://\S+)$", re.IGNORECASE),
    "estimate": re.compile(r"^estimate$", re.IGNORECASE),
    "reasoning": re.compile(r"^reasoning$", re.IGNORECASE),
}

# Tags considered "weak" evidence: allowed but flagged in reports.
WEAK_TAG_TYPES = {"company", "url", "estimate", "reasoning"}
# Tags considered "strong" evidence (resolvable to an external record).
STRONG_TAG_TYPES = {"PMID", "DOI", "patent", "biorxiv", "arxiv", "clinicaltrials", "uniprot"}

SRC_BLOCK_RE = re.compile(r"\[src:\s*([^\]]+)\]\s*$")

# Bullet detector: -, *, +, or numbered (1. / 1))
BULLET_RE = re.compile(r"^\s*(?:[-*+]|\d{1,3}[.)])\s+")

# "Looks factual" heuristics on bullet text
DIGIT_RE = re.compile(r"\d")
# Named acronym: 2+ consecutive uppercase letters (CD34, NSG, VSV-G, HSC, MDS...)
ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,}\b")
# Proper-noun-ish: Title Case phrase of 2+ words (weaker signal)
TITLECASE_RUN_RE = re.compile(r"\b(?:[A-Z][a-z]+ ){1,}[A-Z][a-z]+\b")

# Lines that are explicitly non-factual metadata and should be skipped.
# These appear in our stage outputs' YAML frontmatter and directive lines.
SKIP_LINE_PREFIXES = (
    "---",  # YAML frontmatter / section rules
    "```",  # code fence
    "|",  # markdown table row separator
    "#",  # headers
)


@dataclass
class TagParseResult:
    raw: str
    type: Optional[str] = None
    id: Optional[str] = None
    ok: bool = False
    error: Optional[str] = None


@dataclass
class LineFinding:
    line_no: int
    line: str
    classification: str  # "numeric_bullet" | "acronym_bullet" | "numeric_prose" | "ok"
    tagged: bool
    tags: list[TagParseResult] = field(default_factory=list)
    issue: Optional[str] = None  # "untagged" | "malformed_tag" | None
    severity: str = "ok"  # "ok" | "warn" | "fail"


@dataclass
class ValidationReport:
    file: str
    total_lines: int
    scanned_lines: int
    factual_bullet_count: int
    tagged_bullet_count: int
    untagged_bullet_count: int
    malformed_tag_count: int
    numeric_prose_warnings: int
    strong_tag_usage: int
    weak_tag_usage: int
    status: str  # "PASS" | "WARN" | "FAIL"
    findings: list[LineFinding] = field(default_factory=list)
    tag_breakdown: dict = field(default_factory=dict)


# ---------- tag parsing ----------

def parse_tags(raw_list: str) -> list[TagParseResult]:
    """Split comma-separated tag list, validate each against the grammar."""
    out = []
    # Split on commas NOT inside parentheses (DOIs have /, patents have letters, URLs can have commas — rare)
    parts = [p.strip() for p in raw_list.split(",") if p.strip()]
    for raw in parts:
        parsed = TagParseResult(raw=raw)
        # try each pattern
        for tag_type, pattern in TAG_PATTERNS.items():
            m = pattern.match(raw)
            if m:
                parsed.type = tag_type
                parsed.id = m.group(1) if m.groups() else raw
                parsed.ok = True
                break
        if not parsed.ok:
            parsed.error = f"unrecognized tag syntax: {raw!r}"
        out.append(parsed)
    return out


# ---------- markdown walking ----------

def _classify(line: str) -> tuple[str, str]:
    """Return (classification, body_without_src_block).

    classification ∈ {"skip", "ok", "numeric_bullet", "acronym_bullet",
                      "numeric_prose"}.
    """
    raw = line.rstrip("\n")
    stripped = raw.strip()
    if not stripped:
        return "skip", ""
    if any(stripped.startswith(p) for p in SKIP_LINE_PREFIXES):
        return "skip", ""
    # YAML header keys inside frontmatter (e.g., "stage: 0") — skip if short and colon-prefixed
    if re.match(r"^[a-z_]+:\s", stripped) and len(stripped) < 80 and not BULLET_RE.match(raw):
        return "skip", ""

    # detect trailing src block
    m = SRC_BLOCK_RE.search(stripped)
    body = stripped[: m.start()].rstrip() if m else stripped

    is_bullet = bool(BULLET_RE.match(raw))
    has_digit = bool(DIGIT_RE.search(body))
    has_acronym = bool(ACRONYM_RE.search(body))

    if is_bullet and (has_digit or has_acronym):
        return ("numeric_bullet" if has_digit else "acronym_bullet", body)
    if not is_bullet and has_digit and len(body) > 12:
        # prose sentence with a number — warn but do not fail
        return "numeric_prose", body
    return "ok", body


def validate_markdown(path: Path) -> ValidationReport:
    text = path.read_text()
    lines = text.splitlines()

    report = ValidationReport(
        file=str(path),
        total_lines=len(lines),
        scanned_lines=0,
        factual_bullet_count=0,
        tagged_bullet_count=0,
        untagged_bullet_count=0,
        malformed_tag_count=0,
        numeric_prose_warnings=0,
        strong_tag_usage=0,
        weak_tag_usage=0,
        status="PASS",
    )

    in_code_fence = False
    in_front_matter = False
    front_matter_seen = 0

    for i, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        # YAML frontmatter: the first pair of `---` lines enclose metadata
        if stripped == "---" and front_matter_seen < 2:
            front_matter_seen += 1
            in_front_matter = front_matter_seen == 1
            continue
        if in_front_matter:
            continue
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue

        classification, body = _classify(raw)
        if classification == "skip":
            continue
        report.scanned_lines += 1

        src_m = SRC_BLOCK_RE.search(raw.rstrip())
        tagged = src_m is not None
        tags = parse_tags(src_m.group(1)) if tagged else []

        finding = LineFinding(
            line_no=i,
            line=raw.rstrip(),
            classification=classification,
            tagged=tagged,
            tags=tags,
        )

        if classification in ("numeric_bullet", "acronym_bullet"):
            report.factual_bullet_count += 1
            if tagged:
                report.tagged_bullet_count += 1
                # count tag types
                if any(not t.ok for t in tags):
                    finding.issue = "malformed_tag"
                    finding.severity = "fail"
                    report.malformed_tag_count += 1
                else:
                    finding.severity = "ok"
                for t in tags:
                    if t.ok and t.type:
                        report.tag_breakdown[t.type] = report.tag_breakdown.get(t.type, 0) + 1
                        if t.type in STRONG_TAG_TYPES:
                            report.strong_tag_usage += 1
                        elif t.type in WEAK_TAG_TYPES:
                            report.weak_tag_usage += 1
            else:
                finding.issue = "untagged"
                # acronym-only bullets are WARN (lots of false positives); numeric bullets are FAIL
                finding.severity = "fail" if classification == "numeric_bullet" else "warn"
                report.untagged_bullet_count += 1
        elif classification == "numeric_prose":
            if not tagged:
                finding.issue = "untagged_prose"
                finding.severity = "warn"
                report.numeric_prose_warnings += 1
            else:
                finding.severity = "ok"
                for t in tags:
                    if t.ok and t.type:
                        report.tag_breakdown[t.type] = report.tag_breakdown.get(t.type, 0) + 1
                        if t.type in STRONG_TAG_TYPES:
                            report.strong_tag_usage += 1
                        elif t.type in WEAK_TAG_TYPES:
                            report.weak_tag_usage += 1

        if finding.severity != "ok":
            report.findings.append(finding)

    # overall status
    if report.malformed_tag_count > 0 or any(f.severity == "fail" for f in report.findings):
        report.status = "FAIL"
    elif report.numeric_prose_warnings > 0 or any(f.severity == "warn" for f in report.findings):
        report.status = "WARN"
    else:
        report.status = "PASS"

    return report


# ---------- serialization ----------

def report_to_dict(r: ValidationReport) -> dict:
    d = asdict(r)
    return d


def write_json_report(r: ValidationReport, path: Path) -> None:
    path.write_text(json.dumps(report_to_dict(r), indent=2))


def summarize(r: ValidationReport) -> str:
    total = r.factual_bullet_count or 1
    ratio = r.tagged_bullet_count / total
    out = [
        f"file: {r.file}",
        f"status: {r.status}",
        f"factual bullets: {r.factual_bullet_count}  tagged: {r.tagged_bullet_count} "
        f"({ratio*100:.0f}%)  untagged: {r.untagged_bullet_count}  "
        f"malformed: {r.malformed_tag_count}  prose warnings: {r.numeric_prose_warnings}",
        f"strong-tag usages: {r.strong_tag_usage}   weak-tag usages: {r.weak_tag_usage}",
    ]
    if r.tag_breakdown:
        out.append(f"tag breakdown: {r.tag_breakdown}")
    if r.findings:
        out.append("")
        out.append(f"findings ({len(r.findings)} of {r.scanned_lines} scanned lines):")
        for f in r.findings[:50]:
            tag_preview = ""
            if f.tags:
                tag_preview = "  tags=" + ",".join(
                    (t.type or "BAD") + ":" + (t.id or t.raw) for t in f.tags
                )
            out.append(
                f"  L{f.line_no:<4} [{f.severity}] {f.classification:<18} {f.issue or '-':<16} "
                f"{f.line[:100]}{tag_preview}"
            )
        if len(r.findings) > 50:
            out.append(f"  … ({len(r.findings) - 50} more)")
    return "\n".join(out)
