#!/usr/bin/env python3
"""Pre-report stale-tally sweep (QUALITY 105 draft, round 71 seat SC3Lesson).

Every selftest case-count and label-count figure a round writes is diffed against the
final receipt's own line, before the report is filed.  Scope is the round's added lines
(`git diff -U0 <base>..<head>`), so historical figures in the same files are out of scope
by construction.

Usage:
  sweep-selftest-tally.py --receipt <file> --label <token> --range <A>..<B> -- <path>...
  sweep-selftest-tally.py --receipt <file> --label <token> --diff-file <file>

Exit: 0 when every added figure equals the receipt's figure, 1 on any mismatch, 2 when the
receipt carries no `PASS (N cases, ...)` line.
"""
import re
import subprocess
import sys
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
CASE = re.compile(r"(?<![\w.])(\d{2,4})\s+cases|(\d{2,4})\s*(?:\u2192|->)\s*(\d{2,4})")
LABEL = re.compile(r"(?<![\w.])(\d{1,3})\s+(?:of them\s+)?labelled")
RECEIPT = re.compile(r"PASS \((\d+) cases, (\d+) passed, (\d+) failed\)")


def main(argv):
    if "--receipt" not in argv or "--label" not in argv or "--" not in argv:
        print(__doc__)
        return 2
    receipt = argv[argv.index("--receipt") + 1]
    label = argv[argv.index("--label") + 1]
    paths = argv[argv.index("--") + 1:]

    text = pathlib.Path(receipt).read_text(errors="replace")
    m = RECEIPT.search(text)
    if not m:
        print("SWEEP: no receipt line")
        return 2
    n = int(m.group(1))
    labels = sum(1 for line in text.splitlines() if label in line)

    if "--diff-file" in argv:
        diff = pathlib.Path(argv[argv.index("--diff-file") + 1]).read_text()
    else:
        a, b = argv[argv.index("--range") + 1].split("..")
        diff = subprocess.run(
            ["git", "-C", LANE, "diff", "-U0", a, b, "--", *paths],
            capture_output=True, text=True).stdout

    mism = 0
    f = ln = None
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            f = line[6:]
        elif line.startswith("@@"):
            ln = int(re.search(r"\+(\d+)", line).group(1))
        elif line.startswith("+") and not line.startswith("+++"):
            for mm in CASE.finditer(line):
                v = int(mm.group(1) or mm.group(3))
                ok = v == n
                mism += 0 if ok else 1
                print(f"{'OK  ' if ok else 'MISM'} {f}:{ln} cases_figure={v} receipt={n}")
            for mm in LABEL.finditer(line):
                v = int(mm.group(1))
                ok = v == labels
                mism += 0 if ok else 1
                print(f"{'OK  ' if ok else 'MISM'} {f}:{ln} label_figure={v} receipt={labels}")
            ln += 1
    print(f"SWEEP added_figures_mismatched={mism} receipt_cases={n} receipt_labels={labels}")
    return 1 if mism else 0


sys.exit(main(sys.argv))
