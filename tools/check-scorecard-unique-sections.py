#!/usr/bin/env python3
"""check-scorecard-unique-sections — SCORECARD round-section uniqueness gate (round 55, claim C3).

Closes the routed defect class "the lane shipped a section twice under the byte-identical heading
and the non-author closure had to find it" (closure 59a62bfe defect 1: two identical "Round 54 —
declaration" sections; this round's sweep found the same unmarked pattern on a round-30 declaration
repost, plus three LEGACY pairs that are the file's declared-correction convention and stay).

Contract
  python tools/check-scorecard-unique-sections.py [--file <path>]
    Reads the file (default: SCORECARD.md at the lane root, i.e. beside tools/), splits it into
    sections at every level-2 heading (`^## `), and for every heading text that appears on more
    than one section requires the SUPERSESSION RULE: at least one of the duplicate sections'
    bodies declares the supersession — a line matching
        supersed | correct | re-stated | restat | deduplication   (case-insensitive)
    Exit map: 0 every duplicate heading pair carries a supersession declaration (and there is at
    least one section); 1 at least one duplicate heading pair where NEITHER body declares it (each
    finding printed as SCORECARD-DUPLICATE-UNMARKED with the heading and its line numbers);
    2 could-not-evaluate (file missing or unreadable).

  python tools/check-scorecard-unique-sections.py --selftest
    Hermetic fixture suite over temp files: an unmarked duplicate (must fail), a marked duplicate
    (must pass), a no-duplicate file (must pass), a missing file (must exit 2). Prints
    SCORECARD_UNIQUE_SECTIONS: PASS/FAIL (N cases, N passed, N failed) and exits 0/1.

Scope limit (named): this gate enforces that a supersession is DECLARED where the file carries
duplicate headings; it does not prove the declaration is true — the same shape-gate limit as
check-knowledge-header.py. A content-bearing correction still needs its own evidence.

Read-only on the lane tree: the gate itself only reads; --selftest writes fixture files under its
own temp directory and removes them. Spell `python`, not `python3`, on this host (drift row D8).
Owner: tsukuroi.
"""
from __future__ import annotations

import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

PROG = "check-scorecard-unique-sections"
TAG = "SCORECARD_UNIQUE_SECTIONS"
FINDING = "SCORECARD-DUPLICATE-UNMARKED"
MARKER = re.compile(r"supersed|correct|re-stated|restat|deduplication", re.I)
HEADING = re.compile(r"^## ", re.M)


def section_bodies(text: str) -> dict[str, list[tuple[int, str]]]:
    """Return {heading_text: [(start_line_1based, body), ...]} for every level-2 section."""
    lines = text.splitlines()
    starts = [i for i, l in enumerate(lines) if l.startswith("## ")]
    out: dict[str, list[tuple[int, str]]] = {}
    for k, s in enumerate(starts):
        e = starts[k + 1] if k + 1 < len(starts) else len(lines)
        out.setdefault(lines[s], []).append((s + 1, "\n".join(lines[s + 1:e])))
    return out


def check_text(text: str) -> list[str]:
    """Return one finding line per unmarked duplicate heading (empty list = pass)."""
    findings: list[str] = []
    for heading, secs in section_bodies(text).items():
        if len(secs) < 2:
            continue
        if any(MARKER.search(body) for _, body in secs):
            continue
        where = ", ".join(str(n) for n, _ in secs)
        findings.append(f"{FINDING} {heading.strip()} — lines {where} ({len(secs)} copies, "
                        f"no supersession marker in any copy)")
    return findings


def selftest() -> int:
    fixtures: list[tuple[str, Path, int, str]] = []

    def case(name: str, content: str | None, want_rc: int, want_text: str) -> None:
        d = Path(tempfile.mkdtemp(prefix="scorecard-unique-selftest-"))
        p = d / "SCORECARD.md"
        if content is not None:
            p.write_text(content, encoding="utf-8", newline="\n")
        fixtures.append((name, p, want_rc, want_text))

    case(
        "unmarked-duplicate-fails",
        "## Round N — declaration\n\nbody one\n\n## other\n\nx\n\n## Round N — declaration\n\nbody two\n",
        1, FINDING,
    )
    case(
        "marked-duplicate-passes",
        "## Axes — current (round N)\n\nfirst table\n\n## elsewhere\n\ny\n\n"
        "## Axes — current (round N)\n\nCorrection to the preceding table: fixed counts\n",
        0, "",
    )
    case(
        "unique-headings-pass",
        "## Round 1 — declaration\n\na\n\n## Round 2 — declaration\n\nb\n",
        0, "",
    )
    case(
        "no-level2-headings-rc2",
        "# Just a title\n\nplain prose, no level-2 sections\n",
        2, "no level-2 headings",
    )
    fixtures.append(("missing-file-rc2", Path(tempfile.mkdtemp()) / "absent.md", 2, ""))

    passed = 0
    failed = 0
    for name, path, want_rc, want_text in fixtures:
        rc, out = run_check(path)
        ok = rc == want_rc and (want_text in out)
        print(f"PASS {name}" if ok else f"FAIL {name} — rc {rc} want {want_rc}; output: {out.strip()[:120]}")
        if ok:
            passed += 1
        else:
            failed += 1
        if path.exists():
            path.unlink()
        shutil.rmtree(path.parent, ignore_errors=True)
    verdict = "PASS" if failed == 0 else "FAIL"
    print(f"{TAG}: {verdict} ({len(fixtures)} cases, {passed} passed, {failed} failed)")
    return 0 if failed == 0 else 1


def run_check(path: Path) -> tuple[int, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return 2, f"{PROG}: cannot read {path}: {exc}\n"
    if not HEADING.search(text):
        return 2, f"{PROG}: no level-2 headings found in {path}\n"
    findings = check_text(text)
    if findings:
        return 1, "".join(f + "\n" for f in findings)
    return 0, f"{PROG}: every duplicate level-2 heading pair carries a supersession marker; ok\n"


def main() -> int:
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    target = Path("SCORECARD.md")
    if "--file" in args:
        i = args.index("--file")
        if i + 1 >= len(args):
            print(f"{PROG}: --file requires a path", file=sys.stderr)
            return 2
        target = Path(args[i + 1])
    elif args:
        print(f"{PROG}: unknown arguments {args}", file=sys.stderr)
        return 2
    rc, out = run_check(target)
    print(out, end="")
    return rc


if __name__ == "__main__":
    sys.exit(main())
