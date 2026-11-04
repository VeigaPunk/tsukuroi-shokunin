#!/usr/bin/env python3
# round-75 C2 routed-defect checker (frozen by the round-75 declaration, before any repair exists).
#
# Closes the four routed defects the round-74 non-author closure filed for this lane's next round
# (`corpus/lessons/round-74-verifier-spotcheck.md` section 7 items 1-4). Each item is one appended
# record in committed bytes; the checker reads only committed text (--revision) or a fixture mirror
# (--root) and never writes.
#
# Item 1  R74-DEATH-RECEIPT  corpus/lessons/round-74.md carries a block naming the missing
#         SC3Index death receipt with its observed class (RESOURCE_EXHAUSTED or 429).
# Item 2  R74-REPORT-WORDING corpus/lessons/round-74.md carries a block naming the accurate
#         statement ("no review-accepted drafts") and the existing `w1/SC3Index/report.md`.
# Item 3  R74-SWEEP-RESIDUE  .ufo/waves/round-74/w1/E3HostProbe/receipt-g-landing.txt carries a
#         naming correction that quotes BOTH the fabricated full OID and the real one.
# Item 4  R74-STALE-AXES-TABLE SCORECARD.md carries a `## Round 75 — axes table restated` block
#         with one row per owned axis, each row carrying a backticked counting command, and a
#         sentence naming the round-65 table it supersedes.
#
# Block rule (frozen): an item's block is the token's own line plus the 80 lines that follow it in
# the same file. Item 4's block is delimited by its heading and the next `## ` heading, because a
# restated table is the block itself. A token placed further than 80 lines above its content is a
# stale finding (DECOY-DISTANT), not a pass. Every block must also carry a supersede verb
# (supersede/superseded/supersedes/superseding, erratum, correction, corrected, replaced).
#
# Exit map: 0 every item satisfied (`ROUTED_STALE=0 ROUTED_OK=4/4`); 1 one or more stale, with a
# finding line per item and `reason=` one of `absent`, `token`, `need`, `verb`, `heading`,
# `rows`, `command`; 3 self-test failed. An absent file is a stale finding (rc 1), never rc 2.
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

WINDOW = 80
VERBS = ("supersede", "superseded", "supersedes", "superseding",
         "erratum", "correction", "corrected", "replaced")
FABRICATED = "d749a625f483c66f2a6f2005db3799630c776bc3"
REAL = "d749a625b3054b7cb3435983fb9626ab3d0ed0c4"
AXES = ["depth", "coverage", "operability", "freshness", "calibration", "adjacency"]
AXES_HEADING = "## Round 75 — axes table restated"
BACKTICK = re.compile(r"`[^`]+`")


def load(root, path, revision=None):
    if revision:
        res = subprocess.run(["git", "-C", str(root), "show", f"{revision}:{path}"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return res.stdout.decode("utf-8", "replace") if res.returncode == 0 else None
    p = Path(root) / path
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else None


def token_block(text, token):
    """The token's line plus the WINDOW lines after it; None when the token is absent."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if token in line:
            return "\n".join(lines[i:i + WINDOW + 1])
    return None


def has_verb(block):
    low = block.lower()
    return any(v in low for v in VERBS)


def check_window_item(root, revision, path, token, need_all, need_any):
    text = load(root, path, revision)
    if text is None:
        return f"absent path={path}"
    block = token_block(text, token)
    if block is None:
        return f"token path={path}"
    low = block.lower()
    for item in need_all:
        if item.lower() not in low:
            return f"need path={path} missing={item}"
    for group in need_any:
        if not any(alt.lower() in low for alt in group):
            return f"need path={path} missing_any={group}"
    if not has_verb(block):
        return f"verb path={path}"
    return None


def check_axes(root, revision):
    text = load(root, "SCORECARD.md", revision)
    if text is None:
        return "absent path=SCORECARD.md"
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.rstrip() == AXES_HEADING:
            start = i
            break
    if start is None:
        return "heading path=SCORECARD.md"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    block = "\n".join(lines[start:end])
    for axis in AXES:
        row = None
        for line in lines[start:end]:
            if line.startswith(f"| {axis} |"):
                row = line
                break
        if row is None:
            return f"rows path=SCORECARD.md missing={axis}"
        if not BACKTICK.search(row):
            return f"command path=SCORECARD.md axis={axis}"
    if "round 65" not in block.lower() and "round-65" not in block.lower():
        return "need path=SCORECARD.md missing=round 65"
    if not has_verb(block):
        return "verb path=SCORECARD.md"
    return None


def evaluate(root, revision=None):
    findings = []
    checks = [
        ("R74-DEATH-RECEIPT", lambda: check_window_item(
            root, revision, "corpus/lessons/round-74.md", "R74-DEATH-RECEIPT-MISSING",
            need_all=["SC3Index"], need_any=[["RESOURCE_EXHAUSTED", "429"]])),
        ("R74-REPORT-WORDING", lambda: check_window_item(
            root, revision, "corpus/lessons/round-74.md", "R74-REPORT-WORDING",
            need_all=["no review-accepted drafts", "w1/SC3Index/report.md"], need_any=[])),
        ("R74-SWEEP-RESIDUE", lambda: check_window_item(
            root, revision, ".ufo/waves/round-74/w1/E3HostProbe/receipt-g-landing.txt",
            "R74-SWEEP-RESIDUE", need_all=[FABRICATED, REAL], need_any=[])),
        ("R74-STALE-AXES-TABLE", lambda: check_axes(root, revision)),
    ]
    ok = 0
    for item, fn in checks:
        reason = fn()
        if reason is None:
            ok += 1
        else:
            findings.append(f"{item} STALE reason={reason}")
    stale = len(checks) - ok
    print(f"ROUTED_STALE={stale} ROUTED_OK={ok}/{len(checks)}")
    for f in findings:
        print(f)
    return (0 if stale == 0 else 1), findings


def run_selftest():
    good_lesson = (
        "# Round 74 — synthetic lesson\n\n"
        "## Corrections (round 75, appended)\n\n"
        "- R74-DEATH-RECEIPT-MISSING — the SC3Index death (RESOURCE_EXHAUSTED, 429) had no committed\n"
        "  death receipt; the absence is named here and superseded by this erratum.\n"
        "- R74-REPORT-WORDING — the accurate statement is no review-accepted drafts; the 27.5 KB\n"
        "  self-verified w1/SC3Index/report.md exists on disk; this correction supersedes the report line.\n"
    )
    good_receipt = (
        "=== RECEIPT G ===\n"
        "Base commit: d749a625f483c66f2a6f2005db3799630c776bc3\n"
        "\n## Correction (round 75, R74-SWEEP-RESIDUE)\n"
        f"The header above prints the fabricated full OID d749a625f483c66f2a6f2005db3799630c776bc3; "
        f"the resolving real object is {REAL}. This erratum supersedes the header line.\n"
    )
    good_axes = (
        "# Scorecard\n\n"
        "## Round 75 — axes table restated\n\n"
        "Supersedes the round-65 table; the ordinal rows resolve again.\n\n"
        "| Axis | Score | Counting command |\n|---|---|---|\n"
        + "".join(f"| {a} | 8 | `python3 tools/x.py --revision <REV>` |\n" for a in AXES)
        + "\n## Next section\n"
    )

    def write(root, rel, text):
        p = Path(root) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    cases = []
    cases.append(("CONTROL", None, 0))
    cases.append(("MISSING-DEATH-BLOCK", lambda r: write(
        r, "corpus/lessons/round-74.md",
        good_lesson.replace("R74-DEATH-RECEIPT-MISSING", "SOMETHING-ELSE")), 1))
    cases.append(("DEATH-WRONG-UNIT", lambda r: write(
        r, "corpus/lessons/round-74.md", good_lesson.replace("SC3Index", "SC2Sources")), 1))
    cases.append(("DEATH-NO-CLASS", lambda r: write(
        r, "corpus/lessons/round-74.md",
        good_lesson.replace("RESOURCE_EXHAUSTED, 429", "a provider error")), 1))
    cases.append(("MISSING-WORDING-BLOCK", lambda r: write(
        r, "corpus/lessons/round-74.md",
        good_lesson.replace("R74-REPORT-WORDING", "R74-OTHER")), 1))
    cases.append(("WORDING-WRONG-PHRASE", lambda r: write(
        r, "corpus/lessons/round-74.md",
        good_lesson.replace("no review-accepted drafts", "no drafts at all")), 1))
    cases.append(("MISSING-SWEEP-BLOCK", lambda r: write(
        r, ".ufo/waves/round-74/w1/E3HostProbe/receipt-g-landing.txt",
        good_receipt.replace("R74-SWEEP-RESIDUE", "R74-OTHER")), 1))
    cases.append(("SWEEP-FABRICATED-ONLY", lambda r: write(
        r, ".ufo/waves/round-74/w1/E3HostProbe/receipt-g-landing.txt",
        good_receipt.replace(REAL, "d749a625")), 1))
    cases.append(("AXES-NO-HEADING", lambda r: write(
        r, "SCORECARD.md", good_axes.replace(AXES_HEADING, "## Round 75 — table")), 1))
    cases.append(("AXES-FIVE-ROWS", lambda r: write(
        r, "SCORECARD.md",
        good_axes.replace("| adjacency | 8 | `python3 tools/x.py --revision <REV>` |\n", "")), 1))
    cases.append(("AXES-NO-COMMAND", lambda r: write(
        r, "SCORECARD.md",
        good_axes.replace("| depth | 8 | `python3 tools/x.py --revision <REV>` |",
                          "| depth | 8 | none |")), 1))
    cases.append(("DECOY-DISTANT", lambda r: write(
        r, "corpus/lessons/round-74.md",
        "- R74-DEATH-RECEIPT-MISSING\n" + ("filler line\n" * (WINDOW + 5))
        + "- SC3Index RESOURCE_EXHAUSTED\n"), 1))
    cases.append(("NO-VERB", lambda r: write(
        r, "SCORECARD.md", good_axes.replace("Supersedes the round-65 table;", "The round-65 table;")), 1))

    with tempfile.TemporaryDirectory() as td:
        passed = 0
        failures = []
        for name, mutate, expected in cases:
            root = Path(td) / name
            write(root, "corpus/lessons/round-74.md", good_lesson)
            write(root, ".ufo/waves/round-74/w1/E3HostProbe/receipt-g-landing.txt", good_receipt)
            write(root, "SCORECARD.md", good_axes)
            if mutate is not None:
                mutate(root)
            import io
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc, _ = evaluate(root)
            if rc == expected:
                passed += 1
            else:
                failures.append(f"{name}: expected rc {expected}, got {rc}")
        if failures:
            for f in failures:
                print(f"SELFTEST-FAIL {f}", file=sys.stderr)
            print(f"SELFTEST: FAIL ({len(cases)} cases, {passed} passed, {len(failures)} failed)")
            return 3
        print(f"SELFTEST: PASS ({len(cases)} cases, {passed} passed, 0 failed)")
        return 0


def main():
    parser = argparse.ArgumentParser(description="round-75 C2 routed-defect checker")
    parser.add_argument("--revision", help="git revision to inspect")
    parser.add_argument("--root", help="fixture root directory to inspect")
    parser.add_argument("--selftest", action="store_true", help="run hermetic self-test")
    parser.add_argument("--repo", default=".", help="repo directory")
    args = parser.parse_args()

    if args.selftest:
        sys.exit(run_selftest())

    root = args.root or args.repo
    rc, _ = evaluate(root, args.revision)
    sys.exit(rc)


if __name__ == "__main__":
    main()
