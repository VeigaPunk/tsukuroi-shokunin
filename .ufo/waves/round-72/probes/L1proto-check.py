#!/usr/bin/env python3
"""Pre-report stale-tally sweep (QUALITY 105 draft, round 71 seat SC3Lesson).

Every selftest case-count and label-count figure a round writes is diffed against the
final receipt's own line, before the report is filed.  Scope is the round's added lines
(`git diff -U0 <base>..<head>`), so historical figures in the same files are out of scope
by construction.

Usage:
  check-selftest-tally.py --receipt <file> --label <token> --range <A>..<B> -- <path>...
  check-selftest-tally.py --receipt <file> --label <token> --diff-file <file>
  check-selftest-tally.py --selftest

Exit: 0 when every added figure equals the receipt's figure, 1 on any mismatch, 2 when the
receipt carries no `PASS (N cases, ...)` line.

Only lines that name the census selftest or carry the receipt's own "cases, " phrasing are
scored: a battery's "11 cases", a registry row's historical count or any other instrument's
figure is out of scope by construction. An added line that explicitly marks its figure as superseded (it contains "superseded",
"stays as written" or "stays visible as filed") is printed as SKIP: a correction block must
quote the figure it supersedes, and quoting it is not filing it as current.
"""
import os
import re
import subprocess
import sys
import tempfile
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
CASE = re.compile(r"(?<![\w.])(\d{2,4})\s+cases|(\d{2,4})\s*(?:\u2192|->)\s*(\d{2,4})")
LABEL = re.compile(r"(?<![\w.])(\d{1,3})\s+(?:of them\s+)?labelled")
RECEIPT = re.compile(r"PASS \((\d+) cases, (\d+) passed, (\d+) failed\)")


def sweep(receipt_text, diff_text, label, out, use_git=True):
    """Score one receipt/diff pair. Writes lines through `out`; returns (rc, mism, skipped)."""
    m = RECEIPT.search(receipt_text)
    if not m:
        out("SWEEP: no receipt line")
        return 2, None, None
    n = int(m.group(1))
    labels = sum(1 for line in receipt_text.splitlines() if label in line)

    mism = 0
    skipped = 0
    SUPERSEDED = ("superseded", "stays as written", "stays visible as filed")
    f = ln = None
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            f = line[6:]
        elif line.startswith("@@"):
            ln = int(re.search(r"\+(\d+)", line).group(1))
        elif line.startswith("+") and not line.startswith("+++"):
            if ("selftest" not in line.lower()) and ("cases, " not in line):
                ln += 1
                continue
            if any(marker in line for marker in SUPERSEDED):
                skipped += 1
                out(f"SKIP {f}:{ln} superseded-figure quote (the correction block names it as such)")
                ln += 1
                continue
            for mm in CASE.finditer(line):
                v = int(mm.group(1) or mm.group(3))
                ok = v == n
                mism += 0 if ok else 1
                out(f"{'OK  ' if ok else 'MISM'} {f}:{ln} cases_figure={v} receipt={n}")
            for mm in LABEL.finditer(line):
                v = int(mm.group(1))
                ok = v == labels
                mism += 0 if ok else 1
                out(f"{'OK  ' if ok else 'MISM'} {f}:{ln} label_figure={v} receipt={labels}")
            ln += 1
    out(f"SWEEP added_figures_mismatched={mism} skipped_superseded={skipped} receipt_cases={n} receipt_labels={labels}")
    return (1 if mism else 0), mism, skipped


def selftest():
    root = pathlib.Path(tempfile.mkdtemp(prefix="selftest-tally-", dir=os.environ.get("TMPDIR") or None))
    receipt = "TSUKUROI_CENSUS_SELFTEST: PASS (218 cases, 218 passed, 0 failed)\n" + "R72-C2 line\n" * 4
    cases = []
    try:
        cases.append(("match", receipt,
                      "+++ b/A.md\n@@ -1,0 +1,1 @@\n+the selftest now reads PASS (218 cases, 218 passed, 0 failed)", 0, "added_figures_mismatched=0"))
        cases.append(("mismatch", receipt,
                      "+++ b/A.md\n@@ -1,0 +1,1 @@\n+the selftest reads 217 cases", 1, "MISM A.md:1 cases_figure=217 receipt=218"))
        cases.append(("label-mismatch", receipt,
                      "+++ b/A.md\n@@ -1,0 +1,1 @@\n+the selftest emitted 3 labelled arms", 1, "MISM A.md:1 label_figure=3 receipt=4"))
        cases.append(("superseded-skip", receipt,
                      "+++ b/A.md\n@@ -1,0 +1,1 @@\n+the selftest figure 217 cases is superseded by this correction", 0, "SKIP A.md:1"))
        cases.append(("out-of-scope", receipt,
                      "+++ b/A.md\n@@ -1,0 +1,1 @@\n+the battery ran 11 cases", 0, "added_figures_mismatched=0"))
        cases.append(("no-receipt-line", "no summary here\n",
                      "+++ b/A.md\n@@ -1,0 +1,1 @@\n+the selftest reads 218 cases", 2, "SWEEP: no receipt line"))
        cases.append(("green-control", receipt, "", 0, "added_figures_mismatched=0"))
        passed = 0
        for name, rtext, dtext, want_rc, want_tok in cases:
            lines = []
            rc, _, _ = sweep(rtext, dtext, "R72-C2", lines.append)
            ok = rc == want_rc and any(want_tok in l for l in lines)
            passed += ok
            print(f"{'PASS' if ok else 'FAIL'} (SELFTEST-{name}) rc={rc} want={want_rc}")
        total = len(cases)
        print(f"SELFTEST: {'PASS' if passed == total else 'FAIL'} ({total} cases, {passed} passed, {total - passed} failed)")
        return 0 if passed == total else 1
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--receipt" not in argv or "--label" not in argv or "--" not in argv:
        print(__doc__)
        return 2
    receipt = argv[argv.index("--receipt") + 1]
    label = argv[argv.index("--label") + 1]
    paths = argv[argv.index("--") + 1:]

    rtext = pathlib.Path(receipt).read_text(errors="replace")
    if "--diff-file" in argv:
        dtext = pathlib.Path(argv[argv.index("--diff-file") + 1]).read_text()
    else:
        a, b = argv[argv.index("--range") + 1].split("..")
        dtext = subprocess.run(
            ["git", "-C", LANE, "diff", "-U0", a, b, "--", *paths],
            capture_output=True, text=True).stdout
    rc, _, _ = sweep(rtext, dtext, label, print)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
