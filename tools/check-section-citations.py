#!/usr/bin/env python3
"""Narrow, read-only round-16 section-citation errata gate.

Bounded named-defect conformance, never host truth and never an
update-safety or host-health verdict: the two records of
corpus/knowledge/section-citation-errata-r16.json (schema
tsukuroi-section-citation-errata-v1, source_id S050) must exactly match
the pinned contract values; each record's heading must exist exactly
once outside fenced code in its pinned target file, its row_key must
resolve to exactly one row line under that heading, and its quote must
be a substring of that row. The actual historical wrong locators
"§1 verdict-board row 5" (true §0) and "§7 rank 1" (true §5) are
defects tolerated only inside the preserved ## R15-UPDATE-STATE section
or inside their resolving ## R16-*-SECTION — citation-only erratum
notice; any other occurrence is SECTION-CITATION-WRONG. Every byte
before the appended notice must equal the baseline db68e62… prefix;
the R15 current-use supersession and the no-package/service
authorization must stand untouched. --revision <rev> reads immutable
git objects only (record path fields are compared, never dereferenced);
--selftest is hermetic in-memory fixtures. Exit 0 clean, 1 failed,
2 could-not-evaluate. No writes, no network, no host queries.
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys
from collections import namedtuple
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
ROOT = Path(__file__).resolve().parents[1]
BASE = "db68e62065885b3f7463eb0a436c41f0dc3bcde5"
MD16 = "corpus/knowledge/section-citation-errata-r16.md"
JSON16 = "corpus/knowledge/section-citation-errata-r16.json"
R3 = "corpus/knowledge/host-health-report-r3.md"
V3 = "corpus/knowledge/update-safety-v3.md"
SOURCES = "corpus/SOURCES.md"
SCHEMA = "tsukuroi-section-citation-errata-v1"
BOARD_ID, RANK_ID = "R16-BOARD-SECTION", "R16-RANK-SECTION"
R15_HEAD = "## R15-UPDATE-STATE (2026-10-20) — current-use supersession"
SAFETY = "No agent install, upgrade, downgrade or service action is authorized."
ROUTE = "partial-upgrade-recheck-r15"
REQUIRED = ("id", "source_id", "path", "old_locator", "heading",
            "row_key", "quote", "notice_heading")
PINS = {
    BOARD_ID: {"short": "BOARD", "path": R3, "old_locator": "§1 verdict-board row 5",
               "wrong": "§1 verdict-board row 5", "heading": "## 0. Verdict board",
               "row_key": "| 5 | update-safety |",
               "quote": "`-Syu` now `INERT`; after refresh `UNKNOWN-UPSTREAM`",
               "notice_heading": "## R16-BOARD-SECTION — citation-only erratum"},
    RANK_ID: {"short": "RANK", "path": V3, "old_locator": "§7 rank 1 row",
              "wrong": "§7 rank 1", "heading":
              "## 5. Risk-ordered operations table (recommendation only — nothing here was run)",
              "row_key": "| 1 | Do nothing now |",
              "quote": "`-Syu` would be INERT: 0 candidates by three probes",
              "notice_heading": "## R16-RANK-SECTION — citation-only erratum"}}
REV = re.compile(r"^(?:HEAD|[0-9a-fA-F]{4,64})$")
# Claims that re-supersede the R15 current-use supersession or its routing.
RE_SUPERSEDE = re.compile(
    r"supersed\w*\s+(?:the\s+|this\s+)?(?:r15[\s_-]*update[\s_-]*state"
    r"|r15\s+(?:current-use\s+)?supersession|r15\s+notice|r15\s+routing)", re.I)
SOURCE_ROW = re.compile(r"^\|\s*S050\s*\|")
Finding = namedtuple("Finding", "id site detail")
DocSet = namedtuple("DocSet", "md16 json16 sources targets bases")
Result = namedtuple("Result", "code findings count")


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def norm(text):
    return " ".join(str(text).replace("“", '"').replace("”", '"').split())


def plain(text):
    return norm(str(text).replace("`", ""))


def heading_hits(text, heading):
    """Line indexes where the exact heading appears outside fenced code."""
    out, fence = [], False
    for index, line in enumerate(text.splitlines()):
        stripped = line.strip()
        if stripped.startswith("```"):
            fence = not fence
            continue
        if not fence and line.rstrip() == heading:
            out.append(index)
    return out


def region(lines, start):
    """End index (exclusive) of the section opened at heading line start."""
    fence = False
    for index in range(start + 1, len(lines)):
        stripped = lines[index].strip()
        if stripped.startswith("```"):
            fence = not fence
            continue
        if not fence and stripped.startswith("#"):
            return index
    return len(lines)


def record_checks(cid, obj, text):
    """Per-record pin and resolution findings plus resolved-row lookup.

    Returns (findings, resolved) where resolved means the declared
    binding fields all equal the pins AND resolve in the target text AND
    the notice is valid — the conditions under which the defect is
    tolerated as preserved history.
    """
    pin, out = PINS[cid], []
    short = pin["short"]
    site = f"{JSON16}:{cid}"

    def add(fid, detail):
        out.append(Finding(f"R16-{short}-{fid}", site if fid in ("FIELD", "SOURCE")
                           else pin["path"], detail))

    if not isinstance(obj, dict):
        add("FIELD", "correction record is not an object")
        return out, False
    missing = [f for f in REQUIRED if not isinstance(obj.get(f), str) or not obj[f].strip()]
    extra = sorted(set(obj) - set(REQUIRED))
    if missing or extra:
        add("FIELD", ("missing=" + ",".join(missing) if missing else "")
            + (" extra=" + ",".join(extra) if extra else ""))
    if obj.get("source_id") != "S050":
        add("SOURCE", "source_id must be S050")
    binding = all(isinstance(obj.get(f), str) and obj[f] for f in REQUIRED)
    ok = binding
    if binding and obj["path"] != pin["path"]:
        add("PATH", "declared path differs from the pinned defect file")
        ok = False
    if binding and norm(obj["old_locator"]) != pin["old_locator"]:
        add("OLDLOC", "old_locator differs from the actual historical wrong locator")
        ok = False
    body = text.get(obj["path"] if binding else pin["path"]) if binding else None
    if body is None:
        body = text.get(pin["path"]) if binding else None
    if binding and obj["heading"] != pin["heading"]:
        add("HEADING", "declared heading differs from the pinned contract heading")
        ok = False
    if body is None:
        if binding:
            add("NOTICE", "target text unavailable for notice verification")
            ok = False
        return out, ok
    hits = heading_hits(body, obj["heading"])
    row_line = None
    if len(hits) != 1:
        if obj["heading"] == pin["heading"]:
            add("HEADING", "pinned heading absent, duplicated, or only inside fenced code")
        ok = False
    else:
        lines = body.splitlines()
        start, end = hits[0], region(lines, hits[0])
        rows = [l for l in lines[start + 1:end]
                if l.lstrip().startswith(obj["row_key"])]
        if len(rows) == 1:
            row_line = rows[0]
    if obj["row_key"] != pin["row_key"]:
        add("ROW", "declared row_key differs from the pinned contract row")
        ok = False
    elif len(hits) == 1 and row_line is None:
        add("ROW", "row_key resolves to zero or more than one row under the heading")
        ok = False
    if obj["quote"] != pin["quote"]:
        add("QUOTE", "declared quote differs from the pinned stable row substring")
        ok = False
    elif obj["row_key"] == pin["row_key"] and row_line is not None and obj["quote"] not in row_line:
        add("QUOTE", "quote is not a substring of the uniquely resolved row")
        ok = False
    if obj["notice_heading"] != pin["notice_heading"]:
        add("NOTICE", "declared notice_heading differs from the pinned contract heading")
        ok = False
    elif ok and not notice_valid(body, pin):
        add("NOTICE", "appended notice missing, duplicated, or fails the required links")
        ok = False
    return out, ok


def notice_valid(text, pin):
    hits = heading_hits(text, pin["notice_heading"])
    if len(hits) != 1:
        return False
    lines = text.splitlines()
    body = norm("\n".join(lines[hits[0] + 1:region(lines, hits[0])])).lower()
    return all(token in body for token in (
        pin["old_locator"].lower(), "supersed", "citation only",
        "r15-update-state", ROUTE, SAFETY.lower()))


def supersession_claim(text):
    flat = norm(text)
    out = []
    for match in RE_SUPERSEDE.finditer(flat):
        sent_start = max(flat.rfind(". ", 0, match.start()),
                         flat.rfind("! ", 0, match.start()),
                         flat.rfind("? ", 0, match.start()))
        sent = flat[sent_start + 2:flat.find(".", match.start()) + 1
                    if flat.find(".", match.start()) != -1 else len(flat)]
        if "only" not in sent.split("supersed", 1)[-1][:60]:
            out.append(sent[:100])
    return out


def defect_sites(text, pin, resolved):
    """Unresolved wrong-locator occurrences (normalized, literal-bound)."""
    lines, hits = text.splitlines(), heading_hits(text, pin["notice_heading"])
    r15 = heading_hits(text, R15_HEAD)
    notice_span = ((hits[0], region(lines, hits[0])) if len(hits) == 1 else None)
    r15_span = (r15[0], region(lines, r15[0])) if len(r15) == 1 else None
    wrong = norm(pin["wrong"])
    out = []
    for index, line in enumerate(lines):
        if wrong not in norm(line):
            continue
        in_notice = notice_span and notice_span[0] <= index < notice_span[1]
        in_r15 = r15_span and r15_span[0] <= index < r15_span[1]
        if in_notice:
            continue
        if in_r15 and resolved:
            continue
        out.append(f"line {index + 1}: {pin['wrong']}")
    return out


def target_issues(cid, text, base, resolved):
    """History, supersession, and defect findings for one target file."""
    pin, out = PINS[cid], []
    path = pin["path"]
    if base is None:
        out.append(Finding("R16-HISTORY-REWRITTEN", path,
                           "baseline bytes unavailable for prefix comparison"))
    elif text != base and not text.startswith(base):
        out.append(Finding("R16-HISTORY-REWRITTEN", path,
                           "bytes before the appended notice differ from baseline"))
    r15 = heading_hits(text, R15_HEAD)
    if len(r15) != 1:
        out.append(Finding("R16-SUPERSESSION-REMOVED", path,
                           "R15-UPDATE-STATE heading absent or duplicated"))
    else:
        lines = text.splitlines()
        body = norm("\n".join(lines[r15[0] + 1:region(lines, r15[0])])).lower()
        if ROUTE not in body or SAFETY.lower() not in body:
            out.append(Finding("R16-SUPERSESSION-REMOVED", path,
                               "R15 current-use routing or authorization boundary gutted"))
    for hit in supersession_claim(text):
        out.append(Finding("R16-SUPERSESSION-REMOVED", path, hit))
        break
    for hit in defect_sites(text, pin, resolved):
        out.append(Finding("SECTION-CITATION-WRONG", path, hit))
        break
    return out


def json_issues(doc):
    """Schema, count, and id-structure findings plus per-id unique records."""
    out, records = [], {}
    if not isinstance(doc, dict):
        out.append(Finding("R16-JSON-SCHEMA", JSON16, "top-level object required"))
        return out, records, False
    if doc.get("schema") != SCHEMA:
        out.append(Finding("R16-JSON-SCHEMA", JSON16,
                           "schema tsukuroi-section-citation-errata-v1 required"))
    extra = sorted(set(doc) - {"schema", "corrections"})
    if extra:
        out.append(Finding("R16-JSON-SCHEMA", JSON16, "extra top-level keys=" + ",".join(extra)))
    corrections = doc.get("corrections")
    if not isinstance(corrections, list):
        out.append(Finding("R16-JSON-SCHEMA", JSON16, "corrections array required"))
        return out, records, False
    if len(corrections) != 2:
        out.append(Finding("R16-CORRECTION-COUNT", JSON16,
                           f"corrections={len(corrections)}"))
    structural = not any(f.id == "R16-JSON-SCHEMA" for f in out)
    seen = set()
    for obj in corrections:
        cid = obj.get("id") if isinstance(obj, dict) else None
        if cid in (BOARD_ID, RANK_ID):
            if cid in seen:
                out.append(Finding("R16-CORRECTION-ID", JSON16, f"duplicate id={cid}"))
            else:
                seen.add(cid)
                records[cid] = obj
        elif structural:
            out.append(Finding("R16-CORRECTION-ID", JSON16,
                               "unexpected id=" + (repr(cid)[:40] if cid else "none")))
    for cid in (BOARD_ID, RANK_ID):
        if cid not in records:
            out.append(Finding("R16-CORRECTION-ID", JSON16, f"missing unique id={cid}"))
    return out, records, structural


def md_issues(text):
    out = []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    trio = [line.lower() for line in lines[:3]]
    if not (len(trio) == 3 and trio[0].startswith("source:") and trio[1].startswith("verified-at:")
            and trio[2].startswith("recheck:") and not any(
                line.startswith("#") for line in lines[:3])):
        out.append(Finding("R16-MD-OPENERS", MD16, "source:/verified-at:/recheck: first"))
    heads = ("## R16-BOARD-SECTION", "## R16-RANK-SECTION", "## QUALITY check")
    if not all(any(line.rstrip() == head for line in text.splitlines()) for head in heads):
        out.append(Finding("R16-MD-HEADING", MD16, "named record/QUALITY headings absent"))
    low = plain(text).lower()
    if not all(token in low for token in (
            "s050", R3.lower(), V3.lower(), ROUTE, "citation only")) \
            or supersession_claim(text):
        out.append(Finding("R16-MD-SCOPE", MD16,
                           "citation-only scope, S050/paths/route pins, or supersession leak"))
    return out


def source_issue(text):
    for line in text.splitlines():
        if SOURCE_ROW.match(line) and R3 in line and V3 in line:
            return None
    return Finding("R16-SOURCE-ROW", SOURCES, "S050 row linking both target files absent")


SHARED = {"R16-JSON-MISSING", "R16-JSON-SCHEMA", "R16-CORRECTION-COUNT",
          "R16-CORRECTION-ID", "R16-HISTORY-REWRITTEN",
          "R16-SUPERSESSION-REMOVED", "R16-SOURCE-ROW"}


def evaluate(docs):
    findings = []
    if docs.md16 is None:
        findings.append(Finding("R16-MD-MISSING", MD16, "file absent"))
    if docs.json16 is None:
        findings.append(Finding("R16-JSON-MISSING", JSON16, "file absent"))
    for path in (R3, V3):
        if docs.targets.get(path) is None:
            findings.append(Finding("R16-TARGET-MISSING", path, "file absent"))
    doc = None
    if docs.json16 is not None:
        try:
            doc = json.loads(docs.json16)
        except json.JSONDecodeError as exc:
            return Result(CANNOT, [Finding("E-R16-JSON-PARSE", JSON16, str(exc)[:100])], 0)
    records, structural = {}, False
    if doc is not None:
        issues, records, structural = json_issues(doc)
        findings += issues
    resolved = {cid: False for cid in PINS}
    for cid in PINS:
        obj = records.get(cid)
        if obj is None:
            continue
        issues, ok = record_checks(cid, obj, docs.targets)
        if structural:
            findings += issues
        resolved[cid] = ok
    for cid in PINS:
        path = PINS[cid]["path"]
        text = docs.targets.get(path)
        if text is None:
            continue
        findings += target_issues(cid, text, docs.bases.get(path), resolved[cid])
    if docs.md16 is not None:
        findings += md_issues(docs.md16)
    if docs.sources is None:
        findings.append(Finding("R16-SOURCE-ROW", SOURCES, "SOURCES.md absent"))
    else:
        issue = source_issue(docs.sources)
        if issue:
            findings.append(issue)
    findings = [Finding(*key) for key in sorted({(f.id, f.site, f.detail) for f in findings})]
    count = 0
    for cid, pin in PINS.items():
        prefix = f"R16-{pin['short']}-"
        blocked = any(
            f.id in SHARED or f.id.startswith(prefix)
            or (f.id == "R16-TARGET-MISSING" and f.site == pin["path"])
            or (f.id == "SECTION-CITATION-WRONG" and f.site == pin["path"])
            for f in findings)
        count += int(cid in records and resolved[cid] is not None and not blocked)
    return Result(FAIL if findings else PASS, findings, count)


def emit(result, revision):
    status = {PASS: "PASS", FAIL: "FAIL", CANNOT: "CANNOT_EVALUATE"}[result.code]
    payload = {"status": status, "revision": revision, "correction_count": result.count,
               "scope": "section-citation resolution only; no update-safety or host-health verdict",
               "findings": [{"id": f.id, "site": f.site, "detail": f.detail}
                            for f in result.findings]}
    print(json.dumps(payload, sort_keys=True))
    return result.code


def git(*args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_OPTIONAL_LOCKS": "0", "GIT_PAGER": "cat", "LC_ALL": "C"})
    try:
        return subprocess.run(["git", "--no-pager", "-C", str(ROOT), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=30)
    except subprocess.TimeoutExpired:
        raise Cannot("E-GIT-TIMEOUT", "git", "git command exceeded 30s")
    except OSError as exc:
        raise Cannot("E-GIT-FAILED", "git", str(exc)[:120])


def read_git(commit, path):
    proc = git("show", f"{commit}:{path}")
    if proc.returncode == 0:
        try:
            return proc.stdout.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Cannot("E-READ-FAILED", path, str(exc)[:120])
    error = proc.stderr.decode("utf-8", "replace")
    if re.search(r"does not exist|exists on disk, but not in|not in '", error, re.I):
        return None
    raise Cannot("E-GIT-READ-FAILED", path, error.strip()[:120])


def resolve(rev):
    proc = git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if proc.returncode != 0:
        raise Cannot("E-REVISION-INVALID", "revision", "HEAD or hex commit required")
    return proc.stdout.decode("ascii", "replace").strip()


def build_parser():
    parser = argparse.ArgumentParser(
        description="Narrow read-only round-16 section-citation errata gate.",
        exit_on_error=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision", metavar="REV",
                       help="required: HEAD or a 4-64 hex commit; reads immutable objects only")
    group.add_argument("--selftest", action="store_true", help="in-memory fixture suite")
    return parser


def cli_finding(argv):
    try:
        build_parser().parse_args(argv)
        return None
    except (argparse.ArgumentError, SystemExit):
        return "E-CLI"


def revision_finding(rev):
    return None if REV.fullmatch(rev) else "E-REVISION-INVALID"


BASE_R3 = (
    "# Host-health report — plazir27 (round 3 e2e)\n\n"
    "## 0. Verdict board\n\n"
    "| # | Plane | Verdict | Receipt / pointer |\n"
    "|---|---|---|---|\n"
    "| 4 | journal / boot | `DEGRADED` | `err=251` — detail §2.4 |\n"
    "| 5 | update-safety | `DEGRADED` (arm vocabulary) | `-Syu` now `INERT`; after refresh "
    "`UNKNOWN-UPSTREAM` + `REQUIRES-PREP`; `-Suu`/`-Syyu` `DO-NOT` — detail §2.5 |\n\n"
    "## 1. The gate run (census-v2, four planes)\n\n"
    "Gate prose.\n\n"
    "## 6. Errata (append-only)\n\n"
    "Old errata.\n\n"
    f"{R15_HEAD}\n\n"
    "Appended in round 15. The 2026-10-14 bytes above are preserved and remain\n"
    "historical. The §1 verdict-board row 5 (`update-safety` `DEGRADED`, “`-Syu`\n"
    "now `INERT`”) describes that capture only; it is not a current-use\n"
    "statement.\n\n"
    "For current use on 2026-10-20 read\n"
    "`corpus/knowledge/partial-upgrade-recheck-r15.md` / `.json`.\n\n"
    f"{SAFETY}\n")
BASE_V3 = (
    "# Update safety v3\n\n"
    "## 0. What \"the AUR watch arm\" is — and the one question v3 answers\n\n"
    "v2's §1's own caveat, re-applied.\n\n"
    "## 5. Risk-ordered operations table (recommendation only — nothing here was run)\n\n"
    "v2 §7's table, re-measured today and joined with §3/§4.\n\n"
    "| rank | operation / item | class | reach | measured risk | recommendation |\n"
    "|---:|---|---|---|---|---|\n"
    "| 1 | Do nothing now | official | — | `-Syu` would be INERT: 0 candidates by three probes; "
    "the only effect is the refresh mutation itself, which invalidates the emptiness | gate |\n"
    "| 7 | `-Suu`, `-Syyu`, any downgrade/force verb | official | all | measured | DO-NOT |\n\n"
    "## 7. Appendix\n\n"
    "v2's §7 ranks were the previous numbering.\n\n"
    f"{R15_HEAD}\n\n"
    "Appended in round 15. The 2026-10-14 bytes above are preserved and remain\n"
    "historical. The §7 rank 1 row “Do nothing now” (“`-Syu` would be INERT: 0\n"
    "candidates by three probes”) describes that capture only; it is not a\n"
    "current-use statement.\n\n"
    "For current use on 2026-10-20 read\n"
    "`corpus/knowledge/partial-upgrade-recheck-r15.md` / `.json`.\n\n"
    f"{SAFETY}\n")
NOTICE_R3 = (
    "\n## R16-BOARD-SECTION — citation-only erratum\n\n"
    "Appended in round 16. Every byte above, including the R15-UPDATE-STATE\n"
    "notice, is preserved. That notice's sentence \"The §1 verdict-board row 5\"\n"
    "cites the wrong section: the verdict board is §0 (\"## 0. Verdict board\"),\n"
    "whose row `| 5 | update-safety |` reads \"`-Syu` now `INERT`; after refresh\n"
    "`UNKNOWN-UPSTREAM` + `REQUIRES-PREP`\". The stable citation is §0 row 5.\n\n"
    "This erratum supersedes the citation only. The quoted row content and the\n"
    "R15-UPDATE-STATE current-use supersession routing readers to\n"
    "`corpus/knowledge/partial-upgrade-recheck-r15.md` / `.json` stand\n"
    "unchanged. This note makes no fresh host-health observation and authorizes\n"
    "no package or service action.\n\n"
    f"{SAFETY}\n")
NOTICE_V3 = (
    "\n## R16-RANK-SECTION — citation-only erratum\n\n"
    "Appended in round 16. Every byte above, including the R15-UPDATE-STATE\n"
    "notice, is preserved. That notice's sentence \"The §7 rank 1 row \"Do\n"
    "nothing now\"\" cites the wrong section: in this v3 file the risk-ordered\n"
    "operations table is §5, whose row `| 1 | Do nothing now |` reads \"`-Syu`\n"
    "would be INERT: 0 candidates by three probes\". The stable citation is\n"
    "§5 rank 1, not §7.\n\n"
    "This erratum supersedes the citation only. The quoted row content and the\n"
    "R15-UPDATE-STATE current-use supersession routing readers to\n"
    "`corpus/knowledge/partial-upgrade-recheck-r15.md` / `.json` stand\n"
    "unchanged.\n\n"
    f"{SAFETY}\n")
MD16_CLEAN = (
    "source: S050 — committed target sections at baseline "
    "db68e62065885b3f7463eb0a436c41f0dc3bcde5\n"
    "verified-at: 2026-10-20\n"
    "recheck: on any change to either target file\n\n"
    "This pair resolves only the two citation errata; it authorizes no package\n"
    "or service action and makes no fresh host-health claim.\n\n"
    "## R16-BOARD-SECTION\n\n"
    f"Supersession scope: the section citation only. `{R3}` §0 row 5; R15 routing\n"
    f"to `corpus/knowledge/{ROUTE}.md` stands. S050.\n\n"
    "## R16-RANK-SECTION\n\n"
    f"Supersession scope: the section citation only. `{V3}` §5 rank 1. S050.\n\n"
    "## QUALITY check\n\nBounded conformance over the two records and notices.\n")
RECORD_BOARD = {"id": BOARD_ID, "source_id": "S050", "path": R3,
                "old_locator": "§1 verdict-board row 5",
                "heading": "## 0. Verdict board", "row_key": "| 5 | update-safety |",
                "quote": "`-Syu` now `INERT`; after refresh `UNKNOWN-UPSTREAM`",
                "notice_heading": "## R16-BOARD-SECTION — citation-only erratum"}
RECORD_RANK = {"id": RANK_ID, "source_id": "S050", "path": V3,
               "old_locator": "§7 rank 1 row",
               "heading": "## 5. Risk-ordered operations table (recommendation only "
               "— nothing here was run)",
               "row_key": "| 1 | Do nothing now |",
               "quote": "`-Syu` would be INERT: 0 candidates by three probes",
               "notice_heading": "## R16-RANK-SECTION — citation-only erratum"}
JSON16_CLEAN = {"schema": SCHEMA, "corrections": [RECORD_BOARD, RECORD_RANK]}
SOURCES_CLEAN = ("# Sources\n\n| id | source | scope | tier |\n|---|---|---|---|\n"
                 f"| S050 | committed sections — {R3}; {V3} | own-work | A |\n")


def fixture(**over):
    docs = {"md16": MD16_CLEAN, "json16": json.dumps(JSON16_CLEAN),
            "sources": SOURCES_CLEAN,
            "targets": {R3: BASE_R3 + NOTICE_R3, V3: BASE_V3 + NOTICE_V3},
            "bases": {R3: BASE_R3, V3: BASE_V3}}
    docs.update(over)
    return DocSet(**docs)


def mutate_json(fn):
    doc = json.loads(json.dumps(JSON16_CLEAN))
    fn(doc)
    return json.dumps(doc)


def selftest():
    wr3, wv3 = f"SECTION-CITATION-WRONG:{R3}", f"SECTION-CITATION-WRONG:{V3}"
    cases = [("clean", fixture(), PASS, set(), 2),
             ("baseline", fixture(md16=None, json16=None, sources=SOURCES_CLEAN.replace(
                 "S050", "S049"), targets={R3: BASE_R3, V3: BASE_V3}), FAIL,
              {"R16-MD-MISSING", "R16-JSON-MISSING", "R16-SOURCE-ROW", wr3, wv3}, 0)]
    cases += [
        ("errata-json-missing", fixture(json16=None),
         FAIL, {"R16-JSON-MISSING", wr3, wv3}, 0),
        ("errata-md-missing", fixture(md16=None), FAIL, {"R16-MD-MISSING"}, 2),
        ("target-missing", fixture(targets={R3: None, V3: BASE_V3 + NOTICE_V3}),
         FAIL, {"R16-TARGET-MISSING", "R16-BOARD-NOTICE"}, 1),
        ("source-row-missing", fixture(sources=SOURCES_CLEAN.replace("S050", "S049")),
         FAIL, {"R16-SOURCE-ROW"}, 0)]
    cases.append(("errata-json-malformed", fixture(json16="{"), CANNOT,
                  {"E-R16-JSON-PARSE"}, 0))
    cases.append(("errata-json-wrong-schema",
                  fixture(json16=mutate_json(lambda d: d.update(
                      schema="tsukuroi-locator-clarification-v1"))),
                  FAIL, {"R16-JSON-SCHEMA"}, 0))
    cases.append(("errata-json-extra-key",
                  fixture(json16=mutate_json(lambda d: d.update(notes="x"))),
                  FAIL, {"R16-JSON-SCHEMA"}, 0))
    cases.append(("correction-count-1",
                  fixture(json16=mutate_json(lambda d: d["corrections"].pop(1))),
                  FAIL, {"R16-CORRECTION-COUNT", "R16-CORRECTION-ID", wv3}, 0))
    cases.append(("correction-count-3",
                  fixture(json16=mutate_json(lambda d: d["corrections"].append(
                      {"id": "R16-EXTRA"}))),
                  FAIL, {"R16-CORRECTION-COUNT", "R16-CORRECTION-ID"}, 0))
    cases.append(("duplicate-record-id",
                  fixture(json16=mutate_json(lambda d: d["corrections"][1].update(
                      id=BOARD_ID))),
                  FAIL, {"R16-CORRECTION-ID", wv3}, 0))
    cases.append(("board-field-missing",
                  fixture(json16=mutate_json(lambda d: d["corrections"][0].pop(
                      "old_locator"))),
                  FAIL, {"R16-BOARD-FIELD", wr3}, 1))
    cases.append(("board-field-extra",
                  fixture(json16=mutate_json(lambda d: d["corrections"][0].update(
                      note="x"))),
                  FAIL, {"R16-BOARD-FIELD"}, 1))
    cases.append(("board-source-wrong",
                  fixture(json16=mutate_json(lambda d: d["corrections"][0].update(
                      source_id="S044"))),
                  FAIL, {"R16-BOARD-SOURCE"}, 1))
    cases.append(("board-path-swapped",
                  fixture(json16=mutate_json(lambda d: d["corrections"][0].update(
                      path=V3))),
                  FAIL, {"R16-BOARD-PATH", "R16-BOARD-HEADING", wr3}, 1))
    cases.append(("board-oldloc-mutated",
                  fixture(json16=mutate_json(lambda d: d["corrections"][0].update(
                      old_locator="§2 verdict-board row 5"))),
                  FAIL, {"R16-BOARD-OLDLOC", wr3}, 1))
    cases.append(("rank-oldloc-mutated",
                  fixture(json16=mutate_json(lambda d: d["corrections"][1].update(
                      old_locator="§8 rank 1"))),
                  FAIL, {"R16-RANK-OLDLOC", wv3}, 1))
    cases.append(("board-heading-wrong-section",
                  fixture(json16=mutate_json(lambda d: d["corrections"][0].update(
                      heading="## 1. The gate run (census-v2, four planes)"))),
                  FAIL, {"R16-BOARD-HEADING", "R16-BOARD-ROW", wr3}, 1))
    cases.append(("board-heading-trailing-space",
                  fixture(json16=mutate_json(lambda d: d["corrections"][0].update(
                      heading="## 0. Verdict board "))),
                  FAIL, {"R16-BOARD-HEADING", wr3}, 1))
    cases.append(("rank-heading-emdash",
                  fixture(json16=mutate_json(lambda d: d["corrections"][1].update(
                      heading="## 5. Risk-ordered operations table (recommendation "
                      "only - nothing here was run)"))),
                  FAIL, {"R16-RANK-HEADING", wv3}, 1))
    cases.append(("board-rowkey-mutated",
                  fixture(json16=mutate_json(lambda d: d["corrections"][0].update(
                      row_key="| 4 | update-safety |"))),
                  FAIL, {"R16-BOARD-ROW", wr3}, 1))
    cases.append(("board-rowkey-nonunique",
                  fixture(json16=mutate_json(lambda d: d["corrections"][0].update(
                      row_key="| "))),
                  FAIL, {"R16-BOARD-ROW", wr3}, 1))
    cases.append(("rank-rowkey-other-row",
                  fixture(json16=mutate_json(lambda d: d["corrections"][1].update(
                      row_key="| 7 | `-Suu`, `-Syyu`, any downgrade/force verb |"))),
                  FAIL, {"R16-RANK-ROW", wv3}, 1))
    cases.append(("board-quote-mutated",
                  fixture(json16=mutate_json(lambda d: d["corrections"][0].update(
                      quote="`-Syu` now `INERT` and host is healthy"))),
                  FAIL, {"R16-BOARD-QUOTE", wr3}, 1))
    cases.append(("rank-quote-crossfile",
                  fixture(json16=mutate_json(lambda d: d["corrections"][1].update(
                      quote="`-Syu` now `INERT`; after refresh `UNKNOWN-UPSTREAM`"))),
                  FAIL, {"R16-RANK-QUOTE", wv3}, 1))
    cases.append(("board-notice-heading-decl-mismatch",
                  fixture(json16=mutate_json(lambda d: d["corrections"][0].update(
                      notice_heading="## R16-BOARD-SECTION erratum"))),
                  FAIL, {"R16-BOARD-NOTICE", wr3}, 1))
    cases.append(("board-notice-removed",
                  fixture(targets={R3: BASE_R3, V3: BASE_V3 + NOTICE_V3}),
                  FAIL, {"R16-BOARD-NOTICE", wr3}, 1))
    cases.append(("rank-notice-removed",
                  fixture(targets={R3: BASE_R3 + NOTICE_R3, V3: BASE_V3}),
                  FAIL, {"R16-RANK-NOTICE", wv3}, 1))
    cases.append(("board-notice-unlinked",
                  fixture(targets={R3: BASE_R3 + "\n## R16-BOARD-SECTION — "
                                   "citation-only erratum\n\nAppended in round 16.\n",
                                   V3: BASE_V3 + NOTICE_V3}),
                  FAIL, {"R16-BOARD-NOTICE", wr3}, 1))
    cases.append(("notice-scope-overreach",
                  fixture(targets={R3: BASE_R3 + NOTICE_R3 + "\nThis also supersedes "
                                   "the R15-UPDATE-STATE routing.\n",
                                   V3: BASE_V3 + NOTICE_V3}),
                  FAIL, {"R16-SUPERSESSION-REMOVED"}, 0))
    cases.append(("r15-supersession-deleted",
                  fixture(targets={R3: BASE_R3[:BASE_R3.index(R15_HEAD)]
                                   + NOTICE_R3.lstrip("\n"),
                                   V3: BASE_V3 + NOTICE_V3}),
                  FAIL, {"R16-HISTORY-REWRITTEN", "R16-SUPERSESSION-REMOVED"}, 0))
    laundered = BASE_R3.replace("The §1 verdict-board row 5 (`update-safety`", "The row")
    cases.append(("defect-text-laundered",
                  fixture(targets={R3: laundered + NOTICE_R3, V3: BASE_V3 + NOTICE_V3}),
                  FAIL, {"R16-HISTORY-REWRITTEN"}, 0))
    cases.append(("history-prefix-rewritten",
                  fixture(targets={R3: BASE_R3.replace("Gate prose.", "Changed prose.")
                                   + NOTICE_R3, V3: BASE_V3 + NOTICE_V3}),
                  FAIL, {"R16-HISTORY-REWRITTEN"}, 0))
    cases.append(("restored-defect-elsewhere",
                  fixture(targets={R3: BASE_R3 + NOTICE_R3 + "\n## Trailing note\n\n"
                                   "see §1 verdict-board row 5 for the current arm state\n",
                                   V3: BASE_V3 + NOTICE_V3}),
                  FAIL, {wr3}, 1))
    cases.append(("md-openers-missing",
                  fixture(md16="# Title\n" + MD16_CLEAN), FAIL, {"R16-MD-OPENERS"}, 2))
    cases.append(("md-headings-missing",
                  fixture(md16=MD16_CLEAN.replace("## R16-RANK-SECTION", "## renamed")),
                  FAIL, {"R16-MD-HEADING"}, 2))
    cases.append(("md-scope-supersede",
                  fixture(md16=MD16_CLEAN + "\nThis also supersedes the R15-UPDATE-STATE "
                              "routing.\n"),
                  FAIL, {"R16-MD-SCOPE"}, 2))
    passed, failures = 0, []
    for name, docs, code, want, count in cases:
        result = evaluate(docs)
        want_ids = {w.split(":")[0] if w.startswith("SECTION-CITATION-WRONG") else w
                    for w in want}
        want_sites = {w for w in want if w.startswith("SECTION-CITATION-WRONG")}
        problems = []
        if result.code != code:
            problems.append(f"exit={result.code}/{code}")
        got_ids = {f.id for f in result.findings}
        if got_ids != want_ids:
            problems.append("ids=" + ",".join(sorted(got_ids))
                            + " want=" + ",".join(sorted(want_ids)))
        got_wrong = {f"{f.id}:{f.site}" for f in result.findings
                     if f.id == "SECTION-CITATION-WRONG"}
        if got_wrong != want_sites:
            problems.append("wrong-sites=" + ",".join(sorted(got_wrong)))
        if result.count != count:
            problems.append(f"count={result.count}/{count}")
        if problems:
            failures.append(f"{name}: " + "; ".join(problems))
        else:
            passed += 1
    for name, got, want in (
            ("invalid-revision", revision_finding("not-a-rev!!"), "E-REVISION-INVALID"),
            ("invalid-revision-dash", revision_finding("--exec"), "E-REVISION-INVALID"),
            ("invalid-cli", cli_finding(["--bogus"]), "E-CLI"),
            ("cli-no-mode", cli_finding([]), "E-CLI"),
            ("cli-both-modes", cli_finding(["--selftest", "--revision", "HEAD"]), "E-CLI")):
        if got == want:
            passed += 1
        else:
            failures.append(f"{name}: id={got}/{want}")
    total = len(cases) + 5
    if failures:
        print(f"CHECK_SECTION_CITATIONS_SELFTEST: FAIL ({total} cases, {passed} passed)")
        print("\n".join("  " + item for item in failures))
        return FAIL
    print(f"CHECK_SECTION_CITATIONS_SELFTEST: PASS ({total} cases, {passed} passed, 0 failed)")
    return PASS


def main(argv=None):
    try:
        args = build_parser().parse_args(argv)
    except (argparse.ArgumentError, SystemExit) as exc:
        if isinstance(exc, SystemExit) and not exc.code:
            return 0
        return emit(Result(CANNOT, [Finding("E-CLI", "cli",
                                            "--revision REV or --selftest required")], 0),
                    "worktree")
    if args.selftest:
        return selftest()
    revision = "worktree"
    try:
        if not REV.fullmatch(args.revision):
            raise Cannot("E-REVISION-INVALID", "revision", "HEAD or hex commit required")
        revision = resolve(args.revision)
        base_rev = resolve(BASE)
        docs = DocSet(
            read_git(revision, MD16), read_git(revision, JSON16),
            read_git(revision, SOURCES),
            {path: read_git(revision, path) for path in (R3, V3)},
            {path: read_git(base_rev, path) for path in (R3, V3)})
    except Cannot as exc:
        return emit(Result(CANNOT, [Finding(exc.fid, exc.site, exc.detail)], 0), revision)
    except Exception as exc:  # no traceback exit 1: unreadable input is CANNOT
        return emit(Result(CANNOT, [Finding("E-INTERNAL", "gate", str(exc)[:120])], 0),
                    revision)
    try:
        result = evaluate(docs)
    except Exception as exc:
        return emit(Result(CANNOT, [Finding("E-INTERNAL", "gate", str(exc)[:120])], 0),
                    revision)
    return emit(result, revision)


if __name__ == "__main__":
    sys.exit(main())
