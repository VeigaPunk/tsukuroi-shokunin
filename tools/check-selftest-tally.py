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
receipt carries no `PASS (N cases, ...)` line or on usage.
`--selftest` runs ten hermetic cases.  Every receipt/diff fixture is written, and read back,
under ONE temp root created in `$TMPDIR` (never a hardcoded `/tmp`; the platform default is
used only when `TMPDIR` is unset).  One named `PASS (SELFTEST-<ID>)` / `FAIL (SELFTEST-<ID>)`
line per case, then `SELFTEST: PASS (N cases, N passed, 0 failed)`; exit 0 only when every
case passes, 1 when one fails.  Findings carry stable ids: a figure mismatch is
`SWEEP-MISMATCH`, a label-count mismatch `SWEEP-LABEL`, a receipt with no PASS line
`SWEEP-NO-RECEIPT`.  `SELFTEST-CASES` compares the executed case ids with the pinned
`DECLARED` manifest, so deleting a case row is itself a failure.

Only lines that name the census selftest or carry the receipt's own "cases, " phrasing are
scored: a battery's "11 cases", a registry row's historical count or any other instrument's
figure is out of scope by construction. An added line that explicitly marks its figure as superseded (it contains "superseded",
"stays as written" or "stays visible as filed") is printed as SKIP: a correction block must
quote the figure it supersedes, and quoting it is not filing it as current.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
CASE = re.compile(r"(?<![\w.])(\d{2,4})\s+cases|(\d{2,4})\s*(?:\u2192|->)\s*(\d{2,4})")
LABEL = re.compile(r"(?<![\w.])(\d{1,3})\s+(?:of them\s+)?labelled")
RECEIPT = re.compile(r"PASS \((\d+) cases, (\d+) passed, (\d+) failed\)")
FINDING = {"cases": "SWEEP-MISMATCH", "labels": "SWEEP-LABEL", "receipt": "SWEEP-NO-RECEIPT"}
DECLARED = ("MATCH", "MISMATCH", "LABEL", "SUPERSEDED", "OUT-OF-SCOPE",
            "NO-RECEIPT", "GREEN-DIFF", "MIXED", "HERMETIC")


def sweep(receipt_text, diff_text, label, out):
    """Score one receipt/diff pair. Writes lines through `out`; returns (rc, mism, skipped)."""
    m = RECEIPT.search(receipt_text)
    if not m:
        out(f"SWEEP: no receipt line [{FINDING['receipt']}]")
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
                out(f"{'OK  ' if ok else 'MISM'} {f}:{ln} cases_figure={v} receipt={n} [{FINDING['cases']}]")
            for mm in LABEL.finditer(line):
                v = int(mm.group(1))
                ok = v == labels
                mism += 0 if ok else 1
                out(f"{'OK  ' if ok else 'MISM'} {f}:{ln} label_figure={v} receipt={labels} [{FINDING['labels']}]")
            ln += 1
    out(f"SWEEP added_figures_mismatched={mism} skipped_superseded={skipped} receipt_cases={n} receipt_labels={labels}")
    return (1 if mism else 0), mism, skipped


def score_files(receipt_path, diff_path, label, out):
    """Read one receipt file and one `git diff -U0` file, then score them through `sweep`."""
    return sweep(pathlib.Path(receipt_path).read_text(errors="replace"),
                 pathlib.Path(diff_path).read_text(), label, out)


def selftest():
    """Run every hermetic case over fixtures written under one temp root and report."""
    tmpdir = os.environ.get("TMPDIR")
    base = pathlib.Path(tmpdir) if tmpdir else pathlib.Path(tempfile.gettempdir())
    if not base.is_dir():
        print(f"FAIL (SELFTEST-TMPDIR) TMPDIR={base} is not a directory")
        print("SELFTEST: FAIL (1 cases, 0 passed, 1 failed)")
        return 2
    base = base.resolve()
    root = pathlib.Path(tempfile.mkdtemp(prefix="selftest-tally-", dir=str(base)))
    label = "R72-C2"
    receipt = ("TSUKUROI_CENSUS_SELFTEST: PASS (218 cases, 218 passed, 0 failed)\n"
               + "R72-C2 line\n" * 4)
    # (case id, receipt text, diff text, expected rc, tokens required, tokens forbidden)
    cases = [
        ("MATCH", receipt,
         "+++ b/tally-fixture.md\n@@ -1,0 +1,1 @@\n"
         "+the census selftest now reads PASS (218 cases, 218 passed, 0 failed)",
         0, ["cases_figure=218 receipt=218", "added_figures_mismatched=0"], ["MISM tally", "SKIP"]),
        ("MISMATCH", receipt,
         "+++ b/tally-fixture.md\n@@ -1,0 +2,1 @@\n+the census selftest reads 217 cases",
         1, ["SWEEP-MISMATCH", "tally-fixture.md:2 cases_figure=217 receipt=218"],
         ["added_figures_mismatched=0"]),
        ("LABEL", receipt,
         "+++ b/tally-fixture.md\n@@ -1,0 +1,1 @@\n+the census selftest emitted 3 labelled arms",
         1, ["SWEEP-LABEL", "label_figure=3 receipt=4"], ["added_figures_mismatched=0"]),
        ("SUPERSEDED", receipt,
         "+++ b/tally-fixture.md\n@@ -1,0 +1,1 @@\n"
         "+the census selftest figure 217 cases is superseded by this correction",
         0, ["SKIP tally-fixture.md:1", "skipped_superseded=1"], ["cases_figure"]),
        ("OUT-OF-SCOPE", receipt,
         "+++ b/tally-fixture.md\n@@ -1,0 +1,1 @@\n+the modprobe battery ran 11 cases",
         0, ["added_figures_mismatched=0"], ["cases_figure", "label_figure"]),
        ("NO-RECEIPT", "no summary here\n",
         "+++ b/tally-fixture.md\n@@ -1,0 +1,1 @@\n+the census selftest reads 218 cases",
         2, ["SWEEP-NO-RECEIPT", "no receipt line"], ["added_figures_mismatched"]),
        ("GREEN-DIFF", receipt,
         "+++ b/tally-fixture.md\n@@ -1,0 +1,2 @@\n"
         "+the census selftest now reads 218 cases in one run\n"
         "+the census selftest rollup keeps 4 labelled",
         0, ["SWEEP added_figures_mismatched=0 skipped_superseded=0 "
             "receipt_cases=218 receipt_labels=4"], ["MISM tally"]),
        ("MIXED", receipt,
         "+++ b/tally-fixture.md\n@@ -1,0 +1,2 @@\n"
         "+the census selftest reads 218 cases\n"
         "+the census selftest also reads 220 cases",
         1, ["SWEEP-MISMATCH", "cases_figure=220", "added_figures_mismatched=1"], []),
    ]
    written = []
    results = []

    def fixture(name, text):
        path = root / name
        path.write_text(text)
        written.append(path)
        return path

    try:
        for cid, receipt_text, diff_text, want_rc, want, forbid in cases:
            receipt_path = fixture(f"receipt-{cid}.txt", receipt_text)
            diff_path = fixture(f"diff-{cid}.diff", diff_text)
            lines = []
            rc, mism, skipped = score_files(receipt_path, diff_path, label, lines.append)
            blob = "\n".join(lines)
            ok = (rc == want_rc
                  and all(token in blob for token in want)
                  and not any(token in blob for token in forbid))
            detail = f"rc={rc} want={want_rc}"
            if not ok:
                missing = [t for t in want if t not in blob]
                seen = [t for t in forbid if t in blob]
                detail += f" missing={missing} forbidden={seen}"
            results.append((cid, ok, detail))
    finally:
        shutil.rmtree(root, ignore_errors=True)

    prefix = str(root) + os.sep
    under_root = bool(written) and all(str(p).startswith(prefix) for p in written)
    under_tmpdir = str(root).startswith(str(base) + os.sep)
    # When the caller exports TMPDIR the fixtures must land under it, never under /tmp.
    away_from_tmp = (not tmpdir) or not str(root).startswith("/tmp/")
    removed = not root.exists()
    detail = (f"under_tmpdir={under_tmpdir} under_root={under_root} "
              f"away_from_tmp={away_from_tmp} removed={removed} fixtures={len(written)}")
    results.append(("HERMETIC", under_tmpdir and under_root and away_from_tmp and removed, detail))
    observed = [cid for cid, _, _ in results]
    results.append(("CASES", observed == list(DECLARED) and len(observed) == len(set(observed)),
                    f"observed={','.join(observed)} declared={','.join(DECLARED)}"))

    passed = 0
    for cid, ok, detail in results:
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} (SELFTEST-{cid})" + ("" if ok else f" {detail}"))
    total = len(results)
    print(f"SELFTEST: {'PASS' if passed == total else 'FAIL'} "
          f"({total} cases, {passed} passed, {total - passed} failed)")
    return 0 if passed == total else 1


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
