#!/usr/bin/env python3
# round-74 C2 checker for round-73 routed defects (frozen by the round-74 declaration).
#
# Asserts that the two round-73 verifier spot-check routed defects close in committed bytes:
# 1. R73-GATE-QUOTE-LINE-DRIFT: corpus/lessons/round-73.md carries an appended correction naming
#    the S306 quote location install.c:2383 (superseding :2387) and the three S304 corrected line
#    anchors (:368-370 superseding :367-370, :237-238 superseding :236-238, :238-239 superseding :238-240).
# 2. R73-LOG-COUNT-STALE: LOG.md carries an appended correction naming the superseded Round 73
#    mid-wave counts (12 and 11 cases) and restating the final committed counts (13 and 14 cases).
#
# Exit map: 0 target met (ROUTED_STALE=0 ROUTED_OK=2/2); 1 target missed (ROUTED_STALE > 0);
# 2 error / selftest failure.
import argparse
import os
import re
import subprocess
import sys

LESSON_FILE = "corpus/lessons/round-73.md"
LOG_FILE = "LOG.md"


def load_file(repo, path, revision=None):
    if revision:
        cmd = ["git", "-C", repo, "show", f"{revision}:{path}"]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            return None
        return res.stdout.decode("utf-8", errors="replace")
    p = os.path.join(repo, path)
    if not os.path.isfile(p):
        return None
    with open(p, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def check_r73_gate_quote(lesson_text):
    if not lesson_text:
        return False, "lesson file absent"
    # Find the correction block for R73-GATE-QUOTE-LINE-DRIFT
    blocks = re.split(r'\n(?=##+ )', lesson_text)
    matching_block = None
    for b in blocks:
        if "R73-GATE-QUOTE-LINE-DRIFT" in b:
            matching_block = b
            break
    if not matching_block:
        return False, "R73-GATE-QUOTE-LINE-DRIFT section absent in lesson"

    # Must contain required tokens in body (not just heading)
    body = re.sub(r'^##+ [^\n]+\n', '', matching_block)
    required = [
        "install.c:2383",
        "2387",
        ":368-370",
        ":237-238",
        ":238-239",
    ]
    for req in required:
        if req not in body:
            return False, f"missing token '{req}' in R73-GATE-QUOTE-LINE-DRIFT block body"
    return True, "ok"


def check_r73_log_count(log_text):
    if not log_text:
        return False, "LOG.md absent"
    blocks = re.split(r'\n(?=##+ )', log_text)
    matching_block = None
    for b in blocks:
        if "R73-LOG-COUNT-STALE" in b or ("Round 73" in b and "correction" in b.lower() and "selftest" in b):
            matching_block = b
            break
    if not matching_block:
        return False, "R73-LOG-COUNT-STALE correction block absent in LOG.md"

    body = re.sub(r'^##+ [^\n]+\n', '', matching_block)
    required = [
        "13",
        "14",
    ]
    for req in required:
        if req not in body:
            return False, f"missing token '{req}' in LOG.md correction block body"
    # check that superseded counts (12 and 11) are mentioned
    if not ("12" in body or "twelfth" in body.lower()):
        return False, "missing superseded count 12/twelfth in LOG.md correction block"
    if not ("11" in body or "eleven" in body.lower()):
        return False, "missing superseded count 11/eleven in LOG.md correction block"
    return True, "ok"


def evaluate(repo=".", revision=None, fixture_texts=None):
    if fixture_texts:
        lesson_text = fixture_texts.get(LESSON_FILE)
        log_text = fixture_texts.get(LOG_FILE)
    else:
        lesson_text = load_file(repo, LESSON_FILE, revision)
        log_text = load_file(repo, LOG_FILE, revision)

    stale = 0
    ok = 0
    reasons = []

    res1, msg1 = check_r73_gate_quote(lesson_text)
    if res1:
        ok += 1
    else:
        stale += 1
        reasons.append(f"item 1 (gate quote): {msg1}")

    res2, msg2 = check_r73_log_count(log_text)
    if res2:
        ok += 1
    else:
        stale += 1
        reasons.append(f"item 2 (log count): {msg2}")

    return stale, ok, reasons


def run_selftest():
    good_lesson = """# Round 73 lesson

## Gate
Some gate prose.

## Correction (R73-GATE-QUOTE-LINE-DRIFT)
In the Gate section, the S306 quote was attributed to install.c:2387 but sits at install.c:2383 in the v262 snapshot.
The S304 line anchors carried one extra edge line: :368-370 replaces :367-370, :237-238 replaces :236-238, and :238-239 replaces :238-240.
"""

    good_log = """# Log

## Round 73 (hyaku run 15)
Initial log entry mentioning a twelfth selftest case and checker growing to eleven cases.

## Round 73 — correction (R73-LOG-COUNT-STALE)
The entry above cited mid-wave counts: a twelfth selftest case (12) and checker growing to eleven cases (11).
The final committed instruments carry 13 cases for tools/count-ul-rows-r73.py and 14 cases for tools/check-r72-routed-r73.py.
"""

    cases = [
        ("CONTROL", {"corpus/lessons/round-73.md": good_lesson, "LOG.md": good_log}, 0, 2),
        ("MISSING-LESSON-BLOCK", {"corpus/lessons/round-73.md": "# Empty lesson", "LOG.md": good_log}, 1, 1),
        ("MISSING-LOG-BLOCK", {"corpus/lessons/round-73.md": good_lesson, "LOG.md": "# Empty log"}, 1, 1),
        ("MISSING-BOTH", {"corpus/lessons/round-73.md": "# Empty", "LOG.md": "# Empty"}, 2, 0),
        ("TITLE-ONLY-TOKEN", {
            "corpus/lessons/round-73.md": "## Correction (R73-GATE-QUOTE-LINE-DRIFT: install.c:2383 :368-370 :237-238 :238-239 2387)\nBody with no tokens.",
            "LOG.md": good_log
        }, 1, 1),
        ("MISSING-SUPERSEDED-COUNT", {
            "corpus/lessons/round-73.md": good_lesson,
            "LOG.md": "## Round 73 — correction (R73-LOG-COUNT-STALE)\nFinal committed instruments carry 13 and 14 cases."
        }, 1, 1),
    ]

    passed = 0
    failed = 0
    for name, fixtures, exp_stale, exp_ok in cases:
        stale, ok, reasons = evaluate(fixture_texts=fixtures)
        if stale == exp_stale and ok == exp_ok:
            passed += 1
        else:
            failed += 1
            print(f"CASE {name}: expected (stale={exp_stale}, ok={exp_ok}), got (stale={stale}, ok={ok}), reasons={reasons}", file=sys.stderr)

    print(f"SELFTEST: PASS ({len(cases)} cases, {passed} passed, {failed} failed)")
    return 0 if failed == 0 else 2


def main():
    parser = argparse.ArgumentParser(description="round-74 C2 routed defect checker")
    parser.add_argument("--revision", help="git revision to inspect")
    parser.add_argument("--selftest", action="store_true", help="run hermetic self-test")
    parser.add_argument("--repo", default=".", help="repo directory")
    args = parser.parse_args()

    if args.selftest:
        sys.exit(run_selftest())

    stale, ok, reasons = evaluate(args.repo, args.revision)
    print(f"ROUTED_STALE={stale} ROUTED_OK={ok}/2")
    if reasons:
        for r in reasons:
            print(f"  {r}", file=sys.stderr)
    sys.exit(0 if stale == 0 else 1)


if __name__ == "__main__":
    main()
