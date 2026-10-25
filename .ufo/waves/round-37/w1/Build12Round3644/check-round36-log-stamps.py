#!/usr/bin/env python3
"""check-round36-log-stamps.py — isolated runnable replication of the round-36 LOG stamp typo.

Design item 12/12 (tsukuroi round 37 w1): "round-36 LOG typo reproduction".

The defect this reproduces (located this round, lane read-only):
  * LOG.md:1379 heading
        ## Round 36 — wave 2, measured outcome, budget-forced landing
        (2026-10-24T04:4043Z stamped via date -u)
    carries the malformed UTC stamp `2026-10-24T04:4043Z` (minute field
    `4043` is not a two-digit 00-59 value).
  * Routed as "new instance of the bad-stamp class" in
    corpus/lessons/round-36-verifier-spotcheck.md item 3, with the
    R36-PLACEHOLDER-TIME remedy (corpus/lessons/round-36.md): omit a time
    stamp rather than placeholder it, otherwise restamp honestly (UTC per the
    round-36 declaration erratum, `date -u`).

Behavior
  * Scans only `## Round N ...` headings of the LOG file with N >= 36 (the
    UTC stamp convention applies from the round-36 declaration erratum on).
  * Extracts ISO-like stamp tokens (`YYYY-MM-DD[T ]HH:MM[:SS]Z` family) from
    each such heading and validates calendar and clock fields.
  * Exit 0: no malformed stamps.  Exit 1: at least one malformed stamp.
    Exit 2: usage/input error (missing/unreadable LOG file).

Baseline vs after state
  * Unchanged lane LOG.md fails: exit 1 with one LOG-STAMP-INVALID finding
    naming `2026-10-24T04:4043Z` at line 1379.
  * The after state (the precise patch proposal in fixture/patch.diff:
    restamp to a valid stamp or omit the time) passes: exit 0.

Self-test: `python3 check-round36-log-stamps.py --selftest`
"""

import argparse
import datetime
import pathlib
import re
import sys

MIN_ROUND = 36  # UTC stamp convention applies from the round-36 declaration on.

HEADING_RE = re.compile(r"^## Round ([0-9]+) ")
# ISO-like token family seen in LOG headings, including the malformed shapes
# `04:4043Z` (over-long minutes) and `03:5xZ` (placeholder minutes).
STAMP_RE = re.compile(
    r"([0-9]{4}-[0-9]{2}-[0-9]{2})[T ]([0-9]{2}):([0-9A-Za-z]{2,4})(Z)"
)

EXIT_OK = 0
EXIT_FINDING = 1
EXIT_ERROR = 2


class Finding:
    __slots__ = ("line", "token", "reason")

    def __init__(self, line, token, reason):
        self.line = line
        self.token = token
        self.reason = reason


def _valid_minutes(text):
    if len(text) != 2 or not text.isdigit():
        return False
    minutes = int(text)
    return minutes <= 59


def _validate_stamp(date_part, hh, mm, suffix):
    """Return (ok, reason) for one stamp token."""
    if suffix != "Z":
        return False, f"timezone suffix {suffix!r} is not Z"
    if not _valid_minutes(mm):
        return False, f"minute field {mm!r} is not a two-digit 00-59 value"
    try:
        when = datetime.datetime.strptime(
            f"{date_part}T{hh}:{mm}Z", "%Y-%m-%dT%H:%MZ")
    except ValueError as exc:
        return False, f"not a calendar-valid UTC stamp ({exc})"
    if when.hour > 23 or when.minute > 59:
        return False, "clock field out of range"
    return True, ""


def scan_headings(text):
    """Return (findings, headings_checked) for round >= MIN_ROUND headings."""
    findings = []
    headings_checked = 0
    for number, line in enumerate(text.splitlines(), start=1):
        match = HEADING_RE.match(line)
        if match is None:
            continue
        if int(match.group(1)) < MIN_ROUND:
            continue
        headings_checked += 1
        for stamp in STAMP_RE.finditer(line):
            date_part, hh, mm, suffix = stamp.groups()
            token = stamp.group(0)
            ok, reason = _validate_stamp(date_part, hh, mm, suffix)
            if not ok:
                findings.append(Finding(number, token, reason))
    return findings, headings_checked


def run(log_path):
    try:
        text = pathlib.Path(log_path).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"check-round36-log-stamps: cannot read {log_path}: {exc}")
        return EXIT_ERROR
    findings, headings_checked = scan_headings(text)
    for finding in findings:
        print(
            f"LOG-STAMP-INVALID line {finding.line}: {finding.token!r} "
            f"({finding.reason})")
    print(
        f"LOG-STAMP-CHECK headings_checked={headings_checked} "
        f"findings={len(findings)}")
    return EXIT_FINDING if findings else EXIT_OK


def _selftest_case(name, text, expected_exit):
    findings, _ = scan_headings(text)
    actual = EXIT_FINDING if findings else EXIT_OK
    status = "ok" if actual == expected_exit else "FAIL"
    print(f"[selftest] {name}: expected exit {expected_exit}, got {actual} ({status})")
    if actual != expected_exit:
        raise SystemExit(EXIT_FINDING)


def selftest():
    freeze_heading = (
        "## Round 36 — freeze (2026-10-24T04:28Z stamped at write via date -u)\n")
    typo_heading = (
        "## Round 36 — wave 2, measured outcome, budget-forced landing "
        "(2026-10-24T04:4043Z stamped via date -u)\n")
    corrected_heading = typo_heading.replace("04:4043Z", "04:40Z")
    omitted_heading = typo_heading.replace(" (2026-10-24T04:4043Z", "")
    legacy_heading = "## Round 35 — gate repairs (2026-10-23 ~12:05Z)\n"
    _selftest_case("baseline-typo", typo_heading, EXIT_FINDING)
    _selftest_case("corrected-stamp", corrected_heading, EXIT_OK)
    _selftest_case("omitted-stamp", omitted_heading, EXIT_OK)
    _selftest_case("valid-freeze-stamp", freeze_heading, EXIT_OK)
    _selftest_case("legacy-pre36-stamp-ignored", legacy_heading, EXIT_OK)
    _selftest_case("placeholder-m02utes", typo_heading.replace("4043", "5x"),
                   EXIT_FINDING)
    _selftest_case("no-round36-headings", "## Round 35 — legacy\n", EXIT_OK)


def main(argv):
    parser = argparse.ArgumentParser(
        description="Validates round >=36 LOG heading UTC stamps (round-36 "
                    "LOG typo reproduction).")
    parser.add_argument(
        "--log", default=None,
        help="path to the LOG markdown file (default: lane root LOG.md)")
    parser.add_argument(
        "--selftest", action="store_true",
        help="run embedded fixture cases and exit")
    args = parser.parse_args(argv)
    if args.selftest:
        selftest()
        return EXIT_OK
    if args.log is None:
        args.log = pathlib.Path(__file__).resolve().parents[5] / "LOG.md"
    return run(args.log)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
