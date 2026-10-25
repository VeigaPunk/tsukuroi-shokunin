#!/usr/bin/env python3
"""Check the round-37 correction block for the systemd v262 field-list note.

This is a finite committed-text conformance gate. It does not execute journalctl,
prove all possible prose semantics, or certify behaviour on another systemd build.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import _revision

ROOT = Path(__file__).resolve().parents[1]
NOTE = "corpus/knowledge/journalctl-v262-field-filter-r36.md"
BRANCH = "master"
PASS, FAIL, CANNOT = 0, 1, 2
STATUS = ("PASS", "FAIL", "CANNOT_EVALUATE")
BLOCK = "## Round 37 correction — predicate count, output states, action precedence and prior teaching"
TERMS = (
    "arg_boot_filter", "arg_invocation", "arg_dmesg", "arg_cursor",
    "arg_after_cursor", "arg_cursor_file", "arg_system_units", "arg_user_units",
    "arg_syslog_identifier", "arg_exclude_identifier", "arg_priorities",
    "arg_facilities", "arg_since_set", "arg_until_set", "arg_pattern",
)


def evaluate(note: str | None) -> tuple[int, dict[str, object]]:
    findings: list[dict[str, str]] = []
    if note is None:
        return CANNOT, {"status": STATUS[CANNOT], "checked": 0, "mismatches": None,
                        "findings": [{"id": "C2-NOTE-MISSING", "detail": NOTE}]}
    if BLOCK not in note:
        findings.append({"id": "C2-CORRECTION-MISSING", "detail": "round-37 correction block absent"})
        block = ""
    else:
        block = note.split(BLOCK, 1)[1]

    term_match = re.search(r"has \*\*15 OR terms\*\*, not 16:\s*(.*?)\s*\(`journalctl-filter\.c:26-43`", block, re.S)
    observed_terms = tuple(re.findall(r"`([a-z_]+)`", term_match.group(1))) if term_match else ()
    if observed_terms != TERMS:
        findings.append({"id": "C2-TERM-COUNT", "detail": f"expected exact ordered 15-term predicate, got {len(observed_terms)} terms"})

    required = (
        "`journalctl --no-pager -n 1 -F PRIORITY`",
        "`-F` value list is truncated to one value (`5`)",
        "`journalctl --no-pager -n 1 -N`",
        "`-N` field-name output is unchanged from plain `-N`",
        "both 2882 bytes and identical stdout SHA-256 `3480f2aac48ee794f741dfd7dbffa31c86d933df70482db14adf5e57dfc2f20a`",
        "`journalctl --no-pager -F PRIORITY --list-boots`",
        "it does not produce the field-value list",
        "`ACTION_LIST_FIELDS`",
        "`ACTION_LIST_BOOTS`",
        "`corpus/lessons/round-1.md:111`",
        "S024",
        "does not newly discover the rejection",
        "S199 was re-opened on 2026-10-25",
    )
    for phrase in required:
        if phrase not in block:
            findings.append({"id": "C2-CLAIM-MISSING", "detail": phrase})

    passing = not findings
    return (PASS if passing else FAIL), {
        "status": STATUS[PASS if passing else FAIL],
        "checked": 3,
        "mismatches": len(findings),
        "predicate": "15 exact limiting-option terms; distinct -n/-F and -n/-N outcomes; action replacement; prior teaching acknowledged",
        "findings": findings,
    }


def _clean_git_env() -> dict[str, str]:
    env = _revision.clean_env()
    env["GIT_NO_LAZY_FETCH"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def git_read(revision: str) -> str | None:
    args = ["git", "--no-pager", "-C", str(ROOT), "show", f"{revision}:{NOTE}"]
    proc = subprocess.run(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=_clean_git_env(), timeout=30, check=False)
    if proc.returncode:
        exists = subprocess.run(
            ["git", "--no-pager", "-C", str(ROOT), "ls-tree", "-z", revision, "--", NOTE],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=_clean_git_env(), timeout=30, check=False)
        if exists.returncode == 0 and not exists.stdout:
            return None
        raise RuntimeError(f"cannot read committed {NOTE}")
    return proc.stdout.decode("utf-8")


def _fixture() -> str:
    return """## Round 37 correction — predicate count, output states, action precedence and prior teaching
has **15 OR terms**, not 16: `arg_boot_filter`, `arg_invocation`, `arg_dmesg`, `arg_cursor`, `arg_after_cursor`, `arg_cursor_file`, `arg_system_units`, `arg_user_units`, `arg_syslog_identifier`, `arg_exclude_identifier`, `arg_priorities`, `arg_facilities`, `arg_since_set`, `arg_until_set`, and `arg_pattern` (`journalctl-filter.c:26-43` in the pinned v262 source snapshot).
`journalctl --no-pager -n 1 -F PRIORITY` is accepted (exit 0); `-F` value list is truncated to one value (`5`). `journalctl --no-pager -n 1 -N` is accepted (exit 0); `-N` field-name output is unchanged from plain `-N`; both 2882 bytes and identical stdout SHA-256 `3480f2aac48ee794f741dfd7dbffa31c86d933df70482db14adf5e57dfc2f20a`.
`journalctl --no-pager -F PRIORITY --list-boots` exits 0; it does not produce the field-value list. `ACTION_LIST_FIELDS` is replaced by `ACTION_LIST_BOOTS`.
The rejection was already recorded in `corpus/lessons/round-1.md:111` and S024; this entry does not newly discover the rejection. S199 was re-opened on 2026-10-25.
"""


def selftest() -> int:
    good = _fixture()
    cases = [("uncorrected-base", "old note", FAIL), ("corrected", good, PASS)]
    cases.extend((
        ("wrong-term-count", good.replace("15 OR terms", "16 OR terms"), FAIL),
        ("missing-f-truncation", good.replace("`-F` value list is truncated to one value (`5`)", "`-F` still works"), FAIL),
        ("missing-n-unchanged", good.replace("`-N` field-name output is unchanged from plain `-N`", "`-N` fields are narrowed"), FAIL),
        ("action-overwrite-called-work", good.replace("it does not produce the field-value list", "it works for field enumeration"), FAIL),
        ("prior-teaching-omitted", good.replace("S024", "S000"), FAIL),
    ))
    results = []
    for name, note, expected in cases:
        actual, payload = evaluate(note)
        results.append({"case": name, "expected_exit": expected, "actual_exit": actual,
                        "mismatches": payload.get("mismatches")})
    failed = [row["case"] for row in results if row["expected_exit"] != row["actual_exit"]]
    code = FAIL if failed else PASS
    print(json.dumps({"status": STATUS[code], "cases": len(cases),
                      "passed": len(cases) - len(failed), "failures": failed,
                      "results": results}, sort_keys=True))
    return code


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--revision")
    choice.add_argument("--selftest", action="store_true")
    parser.add_argument("--branch", default=BRANCH)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        if exc.code == 0:
            return PASS
        print(json.dumps({"status": STATUS[CANNOT], "error": "invalid arguments"}, sort_keys=True))
        return CANNOT
    if args.selftest:
        return selftest()
    try:
        binding = _revision.bind(ROOT, args.revision, args.branch)
        code, payload = evaluate(git_read(binding.sha))
        payload.update(revision=binding.sha, branch=binding.branch, branch_tip=binding.branch_tip)
    except _revision.RevisionError as exc:
        code, payload = CANNOT, {"status": STATUS[CANNOT], "error": {"id": exc.fid, "detail": exc.detail}}
    except (OSError, RuntimeError, UnicodeError, subprocess.TimeoutExpired) as exc:
        code, payload = CANNOT, {"status": STATUS[CANNOT], "error": {"id": "E-READ", "detail": str(exc)[:120]}}
    print(json.dumps(payload, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
