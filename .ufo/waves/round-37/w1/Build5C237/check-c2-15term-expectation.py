#!/usr/bin/env python3
"""C2 fixed 15-term expectation check (design item 5/12, seat Build5C237).

Reads, read-only, the lane's active claim surface for the round-36 journalctl
v262 correction: every active companion claim about the
field_list_has_scope_options() predicate must say 15 terms, and the captured
evidence must still show exactly 15 OR operands.

Fails on the unchanged baseline: corpus/knowledge/journalctl-v262-field-filter-r36.md:126
and corpus/README.md:264,269 still claim a "16-term" predicate.

Usage:
  python3 check-c2-15term-expectation.py [ROOT]        # check lane root (default: this repo root)
  python3 check-c2-15term-expectation.py --selftest     # sensitivity self-test on fixtures

Exit 0 = expectation holds; exit 1 = at least one assertion failed.
Stdlib only. Never writes to the lane.
"""

import re
import shutil
import sys
import tempfile
from pathlib import Path

FORBIDDEN = re.compile(r"16[\s-]term")
REQUIRED = re.compile(r"15[\s-]term")

PREDICATE_REL = Path(".ufo/waves/round-36/w1/ScribeC2Draft/journalctl-filter-c-predicate.txt")
NOTE_REL = Path("corpus/knowledge/journalctl-v262-field-filter-r36.md")
README_REL = Path("corpus/README.md")

FAILURES: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  FAIL: {msg}")


def predicate_operand_count(excerpt: str) -> int:
    body = excerpt[excerpt.index("return") + len("return") : excerpt.index("}", excerpt.index("return"))]
    return len([o for o in body.split("||") if o.strip()])


def check_evidence(root: Path) -> None:
    """Source of truth: the captured v262 predicate excerpt has exactly 15 OR terms."""
    p = root / PREDICATE_REL
    if not p.is_file():
        fail(f"evidence excerpt missing: {PREDICATE_REL}")
        return
    n = predicate_operand_count(p.read_text())
    if n != 15:
        fail(f"{PREDICATE_REL} exposes {n} OR operands, expected exactly 15")
    else:
        print(f"  ok: {PREDICATE_REL} exposes exactly 15 OR operands")


def check_note(root: Path) -> None:
    p = root / NOTE_REL
    if not p.is_file():
        fail(f"note missing: {NOTE_REL}")
        return
    lines = p.read_text().splitlines()
    joined = "\n".join(lines)
    hits = [(i + 1, l) for i, l in enumerate(lines) if FORBIDDEN.search(l)]
    if hits:
        for ln, line in hits:
            fail(f"{NOTE_REL}:{ln} still claims a 16-term count: {line!r}")
    elif not REQUIRED.search(joined):
        fail(f"{NOTE_REL} never states the corrected 15-term count")
    else:
        print(f"  ok: {NOTE_REL} has no 16-term claim and states the 15-term count")

    # The note's own decision table must list 15 limiter rows (internal consistency).
    arg_rows = [l for l in lines if re.match(r"^\| `arg_", l)]
    if len(arg_rows) != 15:
        fail(f"{NOTE_REL} decision table has {len(arg_rows)} `arg_*` limiter rows, expected 15")
    else:
        print(f"  ok: {NOTE_REL} decision table lists 15 `arg_*` limiter rows")


def check_readme(root: Path) -> None:
    p = root / README_REL
    if not p.is_file():
        fail(f"README missing: {README_REL}")
        return
    lines = p.read_text().splitlines()
    hits = [(i + 1, l) for i, l in enumerate(lines) if FORBIDDEN.search(l)]
    if hits:
        for ln, line in hits:
            fail(f"{README_REL}:{ln} still claims a 16-term count: {line!r}")
    elif not any(REQUIRED.search(l) for l in lines):
        fail(f"{README_REL} never states the corrected 15-term count")
    else:
        print(f"  ok: {README_REL} has no 16-term claim and states the 15-term count")


def run(root: Path) -> int:
    print(f"checking C2 fixed 15-term expectation at {root}")
    check_evidence(root)
    check_note(root)
    check_readme(root)
    if FAILURES:
        print(f"result: FAIL ({len(FAILURES)} assertion(s) failed)")
        return 1
    print("result: PASS")
    return 0


def selftest() -> int:
    """Prove sensitivity: a 16-term 'before' copy must fail, the 'after' copy must pass."""
    lane_root = Path(__file__).resolve().parents[5]
    with tempfile.TemporaryDirectory(prefix="c2-15term-selftest-") as td:
        t = Path(td)
        (t / PREDICATE_REL.parent).mkdir(parents=True)
        shutil.copy2(lane_root / PREDICATE_REL, t / PREDICATE_REL)

        # after-note: corrected sources line, 15 terms
        after_note = (
            "# systemd 262 rejects `journalctl -F`/`-N` combined with journal-limiting options (round 36, C2 exploratory)\n"
            "\n"
            "| limiting option (v262 `field_list_has_scope_options()` term) | CLI form | verdict |\n"
            "|---|---|---|\n"
            "| `arg_boot_filter` | `-b` | **REJECT** |\n"
            "| `arg_invocation` | `--invocation=` | **REJECT** |\n"
            "| `arg_dmesg` | `-k` | **REJECT** |\n"
            "| `arg_cursor` | `--cursor=` | **REJECT** |\n"
            "| `arg_after_cursor` | `--after-cursor=` | **REJECT** |\n"
            "| `arg_cursor_file` | `--cursor-file=` | **REJECT** |\n"
            "| `arg_system_units` | `-u` | **REJECT** |\n"
            "| `arg_user_units` | `--user-unit=` | **REJECT** |\n"
            "| `arg_syslog_identifier` | `-t` | **REJECT** |\n"
            "| `arg_exclude_identifier` | `--exclude-identifier=` | **REJECT** |\n"
            "| `arg_priorities` | `-p` | **REJECT** |\n"
            "| `arg_facilities` | `--facility=` | **REJECT** |\n"
            "| `arg_since_set` | `--since=` | **REJECT** |\n"
            "| `arg_until_set` | `--until=` | **REJECT** |\n"
            "| `arg_pattern` | `--grep=` | **REJECT** |\n"
            "\n"
            "Sources: `src/journal/journalctl-filter.c` (26-43): `field_list_has_scope_options()`, the 15-term limiting-option predicate.\n"
        )
        (t / NOTE_REL).parent.mkdir(parents=True, exist_ok=True)
        (t / NOTE_REL).write_text(after_note)

        # before-note: same content but with the 16-term line (the baseline bug)
        before_note = after_note.replace("the 15-term limiting-option predicate", "the 16-term limiting-option predicate")
        (t / "before" / NOTE_REL).parent.mkdir(parents=True, exist_ok=True)
        (t / "before" / NOTE_REL).write_text(before_note)
        (t / "before" / PREDICATE_REL).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(lane_root / PREDICATE_REL, t / "before" / PREDICATE_REL)

        # after-README: corrected rows
        after_readme = (
            "C2 (depth, exploratory): `knowledge/journalctl-v262-field-filter-r36.md`\n"
            "— the v262 rejection of `journalctl -F`/`-N` combined with limiting options (15-term predicate,\n"
            "`-n` third state, scope selectors allowed), sourced on S198/S199.\n"
            "| `knowledge/journalctl-v262-field-filter-r36.md` | ... the 15-term `field_list_has_scope_options()` predicate term-by-term ... |\n"
        )
        (t / README_REL).parent.mkdir(parents=True, exist_ok=True)
        (t / README_REL).write_text(after_readme)

        before_readme = after_readme.replace("15-term", "16-term")
        (t / "before" / README_REL).write_text(before_readme)

        # 1) before fixture must FAIL (this is the unchanged baseline shape)
        FAILURES.clear()
        rc_before = run(t / "before")
        if rc_before != 1:
            print("selftest FAIL: before-fixture did not fail as expected")
            return 1
        print("selftest ok: before-fixture (16-term claims) is detected and fails")

        # 2) after fixture must PASS
        FAILURES.clear()
        rc_after = run(t)
        if rc_after != 0:
            print("selftest FAIL: after-fixture (15-term claims) did not pass")
            return 1
        print("selftest ok: after-fixture (15-term claims) passes")

    print("selftest: PASS")
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        return selftest()
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[5]
    return run(root)


if __name__ == "__main__":
    sys.exit(main())
