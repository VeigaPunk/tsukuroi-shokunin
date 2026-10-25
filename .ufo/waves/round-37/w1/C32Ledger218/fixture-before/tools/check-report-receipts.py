#!/usr/bin/env python3
"""Check that revision-cited report gates have committed receipts in a lane snapshot.

The report is read as a plain file and the lane is read through immutable Git
objects. Every Git child follows the round-30 Git child environment contract.
Usage: python3 tools/check-report-receipts.py --report PATH --lane REPO --revision REV
       python3 tools/check-report-receipts.py --selftest
Output: one JSON line per cited revision/tool pair and a summary JSON line.
Exit 0 when all citations are receipted, 1 when any are not, and 2 when the
report or lane revision cannot be read.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HEX = r"[0-9a-fA-F]{4,40}"
GATES_RE = re.compile(r"\bGates\s+at\s+`?(" + HEX + r")`?", re.IGNORECASE)
BEFORE_AFTER_RE = re.compile(r"\bBefore\s*(?:→|->|to)\s*after\b", re.IGNORECASE)
HASH_RE = re.compile(r"(?<![0-9a-fA-F])(" + HEX + r")(?![0-9a-fA-F])")
AT_REV_RE = re.compile(r"\bat\s+`?(" + HEX + r")`?", re.IGNORECASE)
DECLARATION_REV_RE = re.compile(
    r"\bdeclaration(?:\s+commit)?\s+`?(" + HEX + r")`?", re.IGNORECASE)
TABLE_ROW_RE = re.compile(r"^\s*\|")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")
TOOL_PATH_RE = re.compile(r"(?<![A-Za-z0-9_.-])tools/[A-Za-z0-9_.-]+\.(?:py|sh)(?![A-Za-z0-9_.-])")
TOOL_NAME_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])((?:check|probe|mutants|measure|kernel|adjacency|freshness|"
    r"memory|storage|registry|sources|census)-[A-Za-z0-9][A-Za-z0-9_-]*)(?![A-Za-z0-9_-])",
    re.IGNORECASE,
)
RECEIPT_SUFFIXES = {
    ".csv", ".json", ".jsonl", ".log", ".md", ".out", ".txt", ".xml", ".yaml", ".yml"
}


def table_cells(line: str) -> list[str] | None:
    if not TABLE_ROW_RE.match(line):
        return None
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def add_pair(pairs: list[tuple[str, str]], seen: set[tuple[str, str]],
             revision: str, tool: str | None) -> None:
    if tool is None:
        return
    pair = (revision.lower(), tool)
    if pair not in seen:
        seen.add(pair)
        pairs.append(pair)


def tool_from_cell(cell: str) -> str | None:
    path = TOOL_PATH_RE.search(cell)
    if path:
        return path.group(0)
    plain = re.sub(r"[`*_]", "", cell).strip()
    if re.fullmatch(r"sources\s+census", plain, re.IGNORECASE):
        return "sources census"
    name = TOOL_NAME_RE.search(plain)
    if name:
        return name.group(1)
    return None


def gate_tool_label(cell: str) -> str | None:
    tool = tool_from_cell(cell)
    if tool:
        return tool
    plain = re.sub(r"[`*_]", "", cell).strip()
    if plain.lower() in {"", "gate", "gate name", "tool", "tool name", "command", "result",
                         "claim", "test", "name"}:
        return None
    return re.sub(r"\s+", " ", plain)


def tool_from_row(cells: list[str], command_columns: set[int] | None = None) -> str | None:
    columns = command_columns or set()
    for index in sorted(columns):
        if index < len(cells):
            tool = tool_from_cell(cells[index])
            if tool:
                return tool
    for cell in cells:
        tool = tool_from_cell(cell)
        if tool:
            return tool
    return None


def is_table_header(cells: list[str]) -> bool:
    normalized = [re.sub(r"[`*_]", "", cell).strip().lower() for cell in cells]
    return any(cell in {"gate", "tool", "command", "claim", "result", "before", "after"}
               or "measured at" in cell for cell in normalized)


def gate_citations(lines: list[str], pairs: list[tuple[str, str]],
                   seen: set[tuple[str, str]]) -> None:
    pending_revisions: list[str] = []
    active_revisions: list[str] = []
    last_gate_tools: list[str] = []
    for line in lines:
        matches = [match.group(1).lower() for match in GATES_RE.finditer(line)]
        if matches:
            pending_revisions = matches
            active_revisions = []
            last_gate_tools = []
            continue
        cells = table_cells(line)
        if cells is not None and (pending_revisions or active_revisions):
            if TABLE_SEPARATOR_RE.match(line) or is_table_header(cells):
                active_revisions = pending_revisions or active_revisions
                pending_revisions = []
                continue
            active_revisions = pending_revisions or active_revisions
            pending_revisions = []
            tool = gate_tool_label(cells[0]) if cells else None
            if tool and tool not in last_gate_tools:
                last_gate_tools.append(tool)
            for revision in active_revisions:
                add_pair(pairs, seen, revision, tool)
            continue
        sentence_revision = re.search(r"\bAt\s+`?(" + HEX + r")`?", line, re.IGNORECASE)
        if sentence_revision and "same gates" in line.lower():
            revision = sentence_revision.group(1).lower()
            for tool in last_gate_tools:
                add_pair(pairs, seen, revision, tool)
            for match in TOOL_NAME_RE.finditer(line):
                add_pair(pairs, seen, revision, match.group(1))
        if not line.strip() and pending_revisions and not active_revisions:
            continue
        pending_revisions = []
        active_revisions = []


def measurement_citations(lines: list[str], pairs: list[tuple[str, str]],
                          seen: set[tuple[str, str]]) -> None:
    in_section = False
    header: list[str] = []
    declaration_revisions: list[str] = []
    measured_columns: set[int] = set()
    command_columns: set[int] = set()
    for line in lines:
        if BEFORE_AFTER_RE.search(line):
            in_section = True
            header = []
            declaration_revisions = []
            measured_columns = set()
            command_columns = set()
            continue
        if in_section and re.match(r"^\s*#{1,6}\s", line):
            in_section = False
            continue
        if not in_section:
            continue
        cells = table_cells(line)
        if cells is None:
            if not line.strip():
                header = []
                declaration_revisions = []
                measured_columns = set()
                command_columns = set()
            continue
        if TABLE_SEPARATOR_RE.match(line):
            continue
        if is_table_header(cells):
            header = cells
            declaration_revisions = [match.group(1).lower()
                                     for cell in header
                                     for match in DECLARATION_REV_RE.finditer(cell)]
            measured_columns = {index for index, cell in enumerate(header)
                                if "measured at" in cell.lower()}
            command_columns = {index for index, cell in enumerate(header)
                               if any(label in cell.lower() for label in ("command", "tool", "gate"))}
            continue
        tool = tool_from_row(cells, command_columns)
        if tool is None:
            continue
        revisions = list(declaration_revisions)
        for index, cell in enumerate(cells):
            if index in measured_columns:
                revisions.extend(match.group(1).lower() for match in HASH_RE.finditer(cell))
            else:
                revisions.extend(match.group(1).lower() for match in AT_REV_RE.finditer(cell))
                revisions.extend(match.group(1).lower() for match in DECLARATION_REV_RE.finditer(cell))
        for revision in revisions:
            add_pair(pairs, seen, revision, tool)


def extract_citations(report: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    lines = report.splitlines()
    gate_citations(lines, pairs, seen)
    measurement_citations(lines, pairs, seen)
    return pairs


def tool_aliases(tool: str) -> tuple[str, ...]:
    if tool.lower() == "sources census":
        return ("sources census", "sources-census", "sources-census.sh", "tools/sources-census.sh")
    aliases = [tool]
    if tool.startswith("tools/"):
        basename = tool.rsplit("/", 1)[-1]
        aliases.extend((basename, basename.rsplit(".", 1)[0]))
    else:
        aliases.extend(("tools/" + tool + ".py", "tools/" + tool + ".sh",
                        tool + ".py", tool + ".sh"))
    return tuple(dict.fromkeys(alias.lower() for alias in aliases))


def contains_token(text: str, token: str) -> bool:
    pattern = r"(?<![A-Za-z0-9_.-])" + re.escape(token) + r"(?![A-Za-z0-9_.-])"
    return re.search(pattern, text, re.IGNORECASE) is not None


def contains_revision(text: str, cited: str) -> bool:
    cited = cited.lower()
    return any(token.lower().startswith(cited) for token in HASH_RE.findall(text))


COMMAND_LINE_RE = re.compile(
    r"^\s*(?:command|cmd)\s*[:=]|^\s*(?:env|python(?:[0-9]+(?:\.[0-9]+)*)?|bash|sh)\s+",
    re.IGNORECASE,
)
TOOL_FIELD_RE = re.compile(
    r"^\s*[\"']?(?:tool|tool_name|command|cmd)[\"']?\s*[:=]\s*(.+)$",
    re.IGNORECASE,
)


def receipt_matches(text: str, revision: str, tool: str) -> bool:
    aliases = tool_aliases(tool)

    def record_matches(record: object) -> bool:
        if isinstance(record, dict):
            identity_fields = ("tool", "tool_name", "command", "cmd", "argv", "args")
            names_tool = False
            for key in identity_fields:
                value = record.get(key)
                if value is None:
                    continue
                if isinstance(value, (list, tuple)):
                    value_text = " ".join(str(item) for item in value)
                elif isinstance(value, dict):
                    value_text = json.dumps(value, ensure_ascii=False)
                else:
                    value_text = str(value)
                if any(contains_token(value_text, alias) for alias in aliases):
                    names_tool = True
                    break
            if names_tool and contains_revision(json.dumps(record, ensure_ascii=False), revision):
                return True
            return any(record_matches(value) for value in record.values())
        if isinstance(record, list):
            return any(record_matches(value) for value in record)
        return False

    try:
        parsed = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        parsed = None
    if parsed is not None and record_matches(parsed):
        return True
    if parsed is None:
        for line in text.splitlines():
            try:
                record = json.loads(line)
            except (json.JSONDecodeError, TypeError):
                continue
            if record_matches(record):
                return True
    has_named_tool = any(
        (match := TOOL_FIELD_RE.match(line))
        and any(contains_token(match.group(1), alias) for alias in aliases)
        for line in text.splitlines()
    )
    has_command = any(
        COMMAND_LINE_RE.search(line)
        and any(contains_token(line, alias) for alias in aliases)
        for line in text.splitlines()
    )
    return contains_revision(text, revision) and (has_named_tool or has_command)



def receipt_path_matches(path: str) -> bool:
    if re.match(r"^\.ufo/waves/round-[^/]+/.+", path) is None:
        return False
    basename = path.rsplit("/", 1)[-1].lower()
    if re.search(r"(?:^|[-_])(?:dispatch|draft|spec|manifest)(?:[-_.]|$)", basename):
        return False
    suffix = Path(basename).suffix.lower()
    parts = path.lower().split("/")
    # round-30 wave-2 RevReportReceipts: seat reports and any path segment merely containing
    # "receipt" (seat names such as ExecReceiptsR29) self-satisfied every citation; a receipt
    # is now only a non-Markdown file under a `measure/` directory of a round's wave evidence.
    if "measure" not in parts or suffix == ".md":
        return False
    return suffix in RECEIPT_SUFFIXES


def find_receipts(lane: str, revision: str, pairs: list[tuple[str, str]],
                  temp_dir: str) -> dict[tuple[str, str], str]:
    home = os.path.join(temp_dir, "home")
    os.mkdir(home)
    env = {
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "HOME": home,
        "XDG_CONFIG_HOME": os.path.join(home, ".config"),
        "PATH": "/usr/bin:/bin",
        "LC_ALL": "C",
        "GIT_CEILING_DIRECTORIES": os.path.dirname(os.path.abspath(temp_dir)),
    }

    def run_git(*args: str) -> subprocess.CompletedProcess[bytes]:
        command = ["git", "-c", "user.name=tsukuroi-round30-receipt-check",
                   "-c", "user.email=receipt-check@example.invalid", "-C", lane, *args]
        return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              stdin=subprocess.DEVNULL, env=env, check=False)

    resolved = run_git("rev-parse", "--verify", revision + "^{commit}")
    if resolved.returncode != 0:
        raise RuntimeError("lane revision cannot be resolved")
    commit = resolved.stdout.decode("ascii", "replace").strip()
    listing = run_git("ls-tree", "-rz", "--full-tree", commit, "--", ".ufo/waves/")
    if listing.returncode != 0:
        raise RuntimeError("lane wave tree cannot be read")

    unresolved = {pair for pair in pairs}
    found: dict[tuple[str, str], str] = {}
    candidates = []
    for record in listing.stdout.split(b"\0"):
        if not record:
            continue
        metadata, separator, raw_path = record.partition(b"\t")
        if not separator:
            continue
        fields = metadata.split()
        if len(fields) != 3 or fields[1] != b"blob":
            continue
        path = raw_path.decode("utf-8", "surrogateescape")
        if receipt_path_matches(path):
            candidates.append(path)

    for path in candidates:
        if not unresolved:
            break
        shown = run_git("show", f"{commit}:{path}")
        if shown.returncode != 0:
            raise RuntimeError("committed wave file cannot be read: " + path)
        text = shown.stdout.decode("utf-8", "replace")
        for pair in tuple(unresolved):
            cited_revision, tool = pair
            if receipt_matches(text, cited_revision, tool):
                found[pair] = path
                unresolved.remove(pair)
    return found


def fixture_check(report: str, receipts: dict[str, str], expected: list[tuple[str, str, str | None]]) -> bool:
    pairs = extract_citations(report)
    observed = []
    for revision, tool in pairs:
        path = next((path for path, text in receipts.items()
                     if receipt_matches(text, revision, tool)), None)
        observed.append((revision, tool, path))
    return observed == expected


def selftest() -> int:
    positive_report = (
        "Gates at `feedcafe`:\n\n"
        "| Gate | Result |\n|---|---|\n"
        "| `check-example` | PASS |\n"
    )
    negative_report = (
        "## Before → after measurements\n\n"
        "| Claim | Command | Before (declaration `deadbeef`) | After | Measured at |\n"
        "|---|---|---|---|---|\n"
        "| C1 | `python3 tools/check-example.py --revision <REV>` | absent | present | `decafbad` |\n"
    )
    positive_receipts = {
        ".ufo/waves/round-1/measure/gate.jsonl":
            '{"revision":"feedcafedeadbeef","tool":"tools/check-example.py","status":"PASS"}'
    }
    negative_receipts = {
        ".ufo/waves/round-1/measure/before.jsonl":
            '{"revision":"deadbeef","tool":"tools/other-check.py"}'
    }
    cases = [
        ("gates-with-committed-receipt",
         fixture_check(positive_report, positive_receipts,
                       [("feedcafe", "check-example", ".ufo/waves/round-1/measure/gate.jsonl")])),
        ("before-after-unreceipted-citations",
         fixture_check(negative_report, negative_receipts,
                       [("deadbeef", "tools/check-example.py", None),
                        ("decafbad", "tools/check-example.py", None)])),
    ]
    failures = [name for name, passed in cases if not passed]
    print(json.dumps({"selftest": "PASS" if not failures else "FAIL",
                      "cases": len(cases), "passed": len(cases) - len(failures),
                      "failures": failures}, sort_keys=True))
    return 0 if not failures else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--selftest", action="store_true", help="run report and receipt fixtures")
    parser.add_argument("--report", help="round report Markdown file (read as plain text)")
    parser.add_argument("--lane", help="lane repository to inspect with read-only Git")
    parser.add_argument("--revision", help="lane commit revision to inspect")
    args = parser.parse_args(argv)
    if args.selftest:
        if args.report or args.lane or args.revision:
            parser.error("--selftest cannot be combined with --report, --lane or --revision")
        return selftest()
    if not args.report or not args.lane or not args.revision:
        parser.error("--report PATH --lane REPO --revision REV or --selftest is required")
    try:
        report = Path(args.report).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(json.dumps({"error": "report cannot be read", "detail": str(exc)}))
        return 2
    pairs = extract_citations(report)
    try:
        with tempfile.TemporaryDirectory(prefix="check-report-receipts-") as temp_dir:
            found = find_receipts(args.lane, args.revision, pairs, temp_dir)
    except (OSError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc), "revision": args.revision}))
        return 2
    unreceipted = 0
    for revision, tool in pairs:
        receipt = found.get((revision, tool))
        receipted = receipt is not None
        unreceipted += not receipted
        print(json.dumps({"revision": revision, "tool": tool, "receipted": receipted,
                          "receipt": receipt}, sort_keys=True))
    print(json.dumps({"cited": len(pairs), "unreceipted": unreceipted}, sort_keys=True))
    return 1 if unreceipted else 0


if __name__ == "__main__":
    sys.exit(main())
