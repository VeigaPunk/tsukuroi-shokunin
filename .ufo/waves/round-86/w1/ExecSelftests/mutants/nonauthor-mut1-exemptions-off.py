#!/usr/bin/env python3
"""Non-author seat-label check (round 85).

Round-84 spot-check routed defect 2: the round-84 report and entry called seat
`ReviewEntry` a "named non-author reviewer". LEARNING.md §Discernment says the
opposite — a seat the lane dispatched is still the lane; only the hyaku closure is
non-author. A frozen claim can therefore be "verified" by the same lane that wrote
it, with no gate able to notice.

Rule (frozen for round 85): with the wave's results file as the seat census, every
line of every FILE is a finding when it (a) contains the token `non-author`
(case-insensitive), (b) also names a seat from the census as a whole word
(case-insensitive), and (c) carries neither exemption on the same line:

    EXEMPT-LANE       the line says the seat is the lane
                      (`is the lane`, `was the lane`, `the lane, not ...`)
    EXEMPT-NEGATION   the line negates the label
                      (`not a non-author`, `not the non-author`, `not non-author`)

The exemptions exist because the round-85 correction lands exactly such a line
(`seat ReviewEntry is the lane, not a non-author reviewer`); a gate that flagged
the correction would punish the repair. Both checks are line-local: a negation two
lines later does not clear a label on this line.

Exit: 0 no findings; 1 at least one finding; 2 could-not-evaluate (results file
unreadable/malformed, census empty, a FILE unreadable, malformed CLI). JSON on
stdout, sorted keys. Read-only: plain file reads, nothing written.

`--selftest` runs this file as a subprocess over fixtures it writes itself (a
two-seat census, a red file with two labeled lines and two exempt/decoy lines, a
green file, three broken results files, an unreadable FILE and two malformed CLIs)
and asserts the rc, the finding id and the site of every case; it exits 0 only if
all of them match, 1 otherwise.

Usage:
    python3 check-nonauthor-label-r85.py --results WAVE-results.json FILE [FILE ...]
    python3 check-nonauthor-label-r85.py --selftest
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

PASS, FAIL, CANNOT = 0, 1, 2
LABEL = "NONAUTHOR-SEAT-LABEL"
NON_AUTHOR = re.compile(r"non[- ]?author", re.I)
EXEMPT_LANE = re.compile(r"\b(?:is|was|are|were)\s+the\s+lane\b", re.I)
EXEMPT_NEGATION = re.compile(
    r"\bnot\s+(?:a\s+|an\s+|the\s+)?non[- ]?author\b", re.I)
TOKEN = r"(?<![\w.-]){}(?![\w.-])"


class Cannot(Exception):
    def __init__(self, fid, site, detail):
        super().__init__(detail)
        self.fid, self.site, self.detail = fid, site, detail


def seat_names(results_path):
    try:
        raw = Path(results_path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise Cannot("E-RESULTS-UNREADABLE", str(results_path), str(exc)[:160])
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise Cannot("E-RESULTS-MALFORMED", str(results_path), str(exc)[:160])
    rows = payload.get("results") if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        raise Cannot("E-RESULTS-MALFORMED", str(results_path),
                     "no `results` list")
    names = []
    for row in rows:
        name = row.get("name") if isinstance(row, dict) else None
        if isinstance(name, str) and name.strip() and name.strip() not in names:
            names.append(name.strip())
    if not names:
        raise Cannot("E-RESULTS-EMPTY", str(results_path),
                     "no seat `name` in results; an empty census cannot pass")
    return names


def evaluate(results_path, files):
    names = seat_names(results_path)
    patterns = [(name, re.compile(TOKEN.format(re.escape(name)), re.I))
                for name in names]
    findings, notes = [], []
    for path in files:
        try:
            text = Path(path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise Cannot("E-FILE-UNREADABLE", str(path), str(exc)[:160])
        hits, exempt = 0, 0
        for number, line in enumerate(text.split("\n"), 1):
            if not NON_AUTHOR.search(line):
                continue
            seats = [name for name, pattern in patterns if pattern.search(line)]
            if not seats:
                continue
            if False:  # MUTANT: exemptions disabled
                exempt += 1
                continue
            hits += 1
            findings.append({
                "id": LABEL,
                "site": f"{path}:{number}",
                "detail": (f"seat {seats[0]} named on a `non-author` line with no "
                           "lane/negation exemption: " + line.strip()[:140]),
                "seats": seats,
                "line": number,
            })
        notes.append({"path": str(path), "labeled_lines": hits,
                      "exempt_lines": exempt})
    return names, findings, notes


def emit(status, payload):
    payload = dict(payload)
    payload["status"] = status
    print(json.dumps(payload, sort_keys=True))
    return {"PASS": PASS, "FAIL": FAIL, "CANNOT_EVALUATE": CANNOT}[status]


def build_parser():
    parser = argparse.ArgumentParser(
        description="Read-only non-author seat-label check (round 85).",
        exit_on_error=False)
    parser.add_argument("--results", metavar="WAVE-results.json",
                        help="wave results file carrying the seat census")
    parser.add_argument("--selftest", action="store_true",
                        help="self-invocation over isolated fixtures (no FILE/--results)")
    parser.add_argument("files", nargs="*", metavar="FILE",
                        help="file(s) to scan")
    return parser


SELFTEST_RED = """# red fixture: two labeled lines, one decoy, two exempt lines
seat ReviewEntry is a named non-author reviewer here.
the lane notes that non-author review is a useful fiction.
seat ExecSelftests is the lane, not a non-author reviewer.
seat ExecSelftests is not a non-author reviewer, and says so.
seat ReviewEntry is a named non-author reviewer again.
"""
SELFTEST_GREEN = """# green fixture: decoys and exemptions only
non-author review is a fiction; this line names no seat.
seat ExecSelftests is the lane, not a non-author reviewer.
seat ReviewEntry is not a non-author reviewer for this claim.
"""


def _probe(argv):
    proc = subprocess.run([sys.executable, os.path.abspath(__file__), *argv],
                          capture_output=True, text=True, timeout=30)
    try:
        payload = json.loads(proc.stdout)
    except ValueError:
        payload = None
    return proc.returncode, payload


def _write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def selftest():
    """Self-invocation: run this file on each fixture; assert rc, finding id and site."""
    work = tempfile.mkdtemp(prefix="nonauthor-label-selftest-")
    bad = []
    try:
        results = os.path.join(work, "results.json")
        empty = os.path.join(work, "empty.json")
        broken = os.path.join(work, "broken.json")
        red = os.path.join(work, "red.md")
        green = os.path.join(work, "green.md")
        absent_results = os.path.join(work, "absent.json")
        absent_file = os.path.join(work, "absent.md")
        _write(results, json.dumps({"results": [{"name": "ReviewEntry"},
                                                 {"name": "ExecSelftests"}]}))
        _write(empty, json.dumps({"results": []}))
        _write(broken, "{not json")
        _write(red, SELFTEST_RED)
        _write(green, SELFTEST_GREEN)
        cases = [
            # (name, argv, expected rc, expected payload fields)
            ("red-and-green", ["--results", results, red, green], 1,
             {"status": "FAIL", "seats": ["ReviewEntry", "ExecSelftests"],
              "seat_count": 2, "file_count": 2, "finding_count": 2,
              "clean_count": 1, "ids": [LABEL, LABEL],
              "sites": [f"{red}:2", f"{red}:6"]}),
            ("green-only", ["--results", results, green], 0,
             {"status": "PASS", "finding_count": 0, "clean_count": 1,
              "ids": [], "sites": []}),
            ("results-unreadable", ["--results", absent_results, green], 2,
             {"status": "CANNOT_EVALUATE", "ids": ["E-RESULTS-UNREADABLE"]}),
            ("results-malformed", ["--results", broken, green], 2,
             {"status": "CANNOT_EVALUATE", "ids": ["E-RESULTS-MALFORMED"]}),
            ("results-empty", ["--results", empty, green], 2,
             {"status": "CANNOT_EVALUATE", "ids": ["E-RESULTS-EMPTY"]}),
            ("file-unreadable", ["--results", results, green, absent_file], 2,
             {"status": "CANNOT_EVALUATE", "ids": ["E-FILE-UNREADABLE"]}),
            ("cli-no-files", ["--results", results], 2,
             {"status": "CANNOT_EVALUATE", "ids": ["E-CLI"]}),
            ("cli-selftest-with-files", ["--selftest", "--results", results, green], 2,
             {"status": "CANNOT_EVALUATE", "ids": ["E-CLI"]}),
        ]
        for name, argv, want_rc, want in cases:
            rc, payload = _probe(argv)
            findings = payload.get("findings") if isinstance(payload, dict) else None
            got = {
                "status": payload.get("status") if isinstance(payload, dict) else None,
                "ids": [f.get("id") for f in findings] if isinstance(findings, list) else None,
                "sites": [f.get("site") for f in findings] if isinstance(findings, list) else None,
            }
            for key in ("seats", "seat_count", "file_count", "finding_count",
                        "clean_count"):
                if key in want:
                    got[key] = payload.get(key) if isinstance(payload, dict) else None
            mismatched = sorted(k for k, v in want.items() if got.get(k) != v)
            ok = rc == want_rc and not mismatched
            print(json.dumps({"case": name, "rc": rc, "want_rc": want_rc,
                              "mismatched": mismatched, "pass": ok}, sort_keys=True))
            if not ok:
                bad.append(name)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(json.dumps({"selftest": "PASS" if not bad else "FAIL",
                      "cases": 8, "failed": bad}, sort_keys=True))
    return 0 if not bad else 1


def _cannot_cli(detail):
    return emit("CANNOT_EVALUATE", {
        "scope": "none: malformed CLI",
        "findings": [{"id": "E-CLI", "site": "argv", "detail": detail[:160]}]})


def main(argv=None):
    try:
        args = build_parser().parse_intermixed_args(argv)
    except (argparse.ArgumentError, SystemExit) as exc:
        return _cannot_cli(str(exc))

    if args.selftest:
        if args.results is not None or args.files:
            return _cannot_cli("--selftest takes no --results or FILE")
        return selftest()

    if args.results is None or not args.files:
        return _cannot_cli("--results and at least one FILE are required")

    try:
        names, findings, notes = evaluate(args.results, args.files)
    except Cannot as exc:
        return emit("CANNOT_EVALUATE", {
            "scope": "none: could-not-evaluate",
            "findings": [{"id": exc.fid, "site": exc.site, "detail": exc.detail}]})

    return emit("FAIL" if findings else "PASS", {
        "results": str(args.results),
        "seat_count": len(names),
        "seats": names,
        "file_count": len(notes),
        "finding_count": len(findings),
        "clean_count": sum(1 for note in notes if not note["labeled_lines"]),
        "scope": ("whole file, line-local: `non-author` + a census seat name on the "
                  "same line, unless the line says the seat is the lane or negates "
                  "the label; read-only"),
        "findings": findings,
        "notes": notes,
    })


if __name__ == "__main__":
    sys.exit(main())
