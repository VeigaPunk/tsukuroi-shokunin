#!/usr/bin/env python3
"""C3 counter, round 83 — one ordinal per round and axis, or a named correction that
retires only what came before it.

Carries the round-82 predicate (`tools/check-scorecard-ordinals.py`) with its three
routed defects repaired — the r82 bytes stand as history, nothing above them is
rewritten:

  * R82-V2 — `if key[0] == round_no or True:` retired a `(round, axis)` key
    *globally*, silencing every later block including contradicting ones. Retirement
    is now positional: a block's `supersedes-ordinal: round-N axis` retires that
    key's assertions in blocks *before it in file order*, never its own assertion
    and never a later block's. A later block that re-asserts the retired value is a
    finding, not silence.
  * R82-V2 (prose half) — quoted prose is not an assertion: inline code spans
    (`` `...` ``) are stripped from a line before the ordinal pairs are read, so the
    round-82 correction block's quotation of the retired `depth 8 → 9` line is
    history being cited, not a value being claimed.
  * R82-V3 — the `--revision` path failed closed but leaked: a missing SCORECARD at
    the revision raised `CannotEvaluate` inside a try whose only handler caught
    `_revision.RevisionError`, printing a traceback with exit 1 (the *findings*
    code). Every failure now exits 2 with the JSON shape, never a traceback.

Findings, unchanged in meaning: two non-retired blocks disagreeing about one
(round, axis); a correction naming nothing retires nothing; `cannot-evaluate` is
not a pass.

  --revision REV   read SCORECARD.md at a landed lane revision
  --fixture PATH   read a SCORECARD.md file directly (hermetic selftest)
  --selftest       hermetic case suite; writes nothing outside it

Exit: 0 clean / 1 findings / 2 could-not-evaluate / 3 selftest failed.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

SCORECARD = "SCORECARD.md"
AXES = ("depth", "coverage", "operability", "freshness", "calibration", "adjacency")
CLAIM = "C3"

BLOCK = re.compile(r"^## Round (\d+)\b")
PAIR = re.compile(r"(?<![\w-])(" + "|".join(AXES) + r")\s+(\d)\s*(?:→|->)\s*(\d)")
AXES_NOW = re.compile(r"Axes now:\s*(.*)")
AXES_NOW_PAIR = re.compile(r"(?<![\w-])(" + "|".join(AXES) + r")\s*(\d)\b")
SUPERSEDES = re.compile(r"^supersedes-ordinal:\s*round-(\d+)\s+([a-z, ]+)$")
CODE = re.compile(r"`[^`]*`")


class CannotEvaluate(Exception):
    """Input is absent or unusable: this is not a verdict."""


def blocks(text):
    """[(round, first_line_no, [lines])] in file order."""
    out, current = [], None
    for number, line in enumerate(text.splitlines(), 1):
        match = BLOCK.match(line)
        if match:
            current = (int(match.group(1)), number, [])
            out.append(current)
        elif line.startswith("## ") and current is not None:
            current = None
        elif current is not None:
            current[2].append(line)
    return out


def assertions(body):
    """[(axis, after_ordinal)] asserted by one block body; quoted prose is not an assertion."""
    found = []
    for line in body:
        bare = CODE.sub("", line)
        for match in PAIR.finditer(bare):
            found.append((match.group(1), int(match.group(3))))
        now = AXES_NOW.search(bare)
        if now:
            for match in AXES_NOW_PAIR.finditer(now.group(1)):
                found.append((match.group(1), int(match.group(2))))
    return found


def superseded(body):
    """{(round, axis)} this block retires."""
    out = set()
    for line in body:
        match = SUPERSEDES.match(line.strip())
        if match:
            for axis in match.group(2).split(","):
                axis = axis.strip()
                if axis in AXES:
                    out.add((int(match.group(1)), axis))
    return out


def measure(text):
    """(findings, examined) — findings is [] when the lane speaks with one voice.

    Retirement is positional (R82-V2): an assertion in block i is retired when a
    block j > i (file order) carries a supersedes line naming its key; block i's
    own supersedes line never retires its own assertions, and a later block that
    re-asserts a retired value after the correcting block is a finding.
    """
    rows = blocks(text)
    if not rows:
        raise CannotEvaluate("no-round-blocks")
    seen = [(round_no, line_no, assertions(body), superseded(body))
            for round_no, line_no, body in rows]

    values = {}
    for i, (round_no, line_no, found, _retires) in enumerate(seen):
        retired_by_later = set()
        for j in range(i + 1, len(seen)):
            retired_by_later |= seen[j][3]
        for axis, after in found:
            if (round_no, axis) in retired_by_later:
                continue
            values.setdefault((round_no, axis), []).append((after, line_no))

    findings = []
    for (round_no, axis), pairs in sorted(values.items()):
        distinct = sorted({after for after, _ in pairs})
        if len(distinct) > 1:
            findings.append({"round": round_no, "axis": axis, "ordinals": distinct,
                             "sites": [{"after": after, "line": line} for after, line in pairs]})
    return findings, len(values)


def selftest():
    cases = []

    def case(name, text, want_rc, want_findings):
        try:
            findings, examined = measure(text)
            rc = 1 if findings else 0
            observed = f"rc={rc} findings={len(findings)} examined={examined}"
        except CannotEvaluate as exc:
            findings, rc, observed = [], 2, f"rc=2 could-not-evaluate {exc}"
        ok = (rc == 2) if want_rc == -1 else (rc == want_rc and len(findings) == want_findings)
        cases.append((name, ok, observed))

    # 1. the round-81 shape: two blocks, two after-ordinals -> one finding.
    case("contradiction", (
        "## Round 81 — measured outcome\n"
        "| C1 | depth 8 → 9 |\n"
        "Axes now: depth9, coverage9.\n"
        "## Round 81 — measured outcome (later)\n"
        "| C1 | depth 8 → 8 (no uplift claimed) |\n"), 1, 1)
    # 2. a named correction retires the earlier claim -> clean.
    case("named-correction", (
        "## Round 81 — measured outcome\n"
        "Axes now: depth9, coverage9.\n"
        "## Round 81 — ordinal correction\n"
        "supersedes-ordinal: round-81 depth\n"
        "depth 8 → 8; coverage stays 9.\n"), 0, 0)
    # 3. a correction that names nothing retires nothing.
    case("silent-correction", (
        "## Round 81 — measured outcome\n"
        "Axes now: depth9.\n"
        "## Round 81 — correction\n"
        "depth 8 → 8.\n"), 1, 1)
    # 4. one block, one value -> clean.
    case("single-block", "## Round 7 — outcome\ndepth 6 → 7\n", 0, 0)
    # 5. two axes disagreeing independently -> two findings.
    case("two-axes", (
        "## Round 9 — a\nAxes now: depth8, freshness8.\n"
        "## Round 9 — b\ndepth 8 → 9; freshness 8 → 7.\n"), 1, 2)
    # 6. no round blocks -> could-not-evaluate, never a clean pass.
    case("no-blocks", "# Scorecard\n\nnothing here\n", -1, 0)
    # 7. a gate name that ends in an axis word is not an ordinal claim.
    case("hyphenated-name", (
        "## Round 33 — outcome\n"
        "check-registry-coverage 1 → 0; coverage 9 → 9.\n"), 0, 0)
    # 8. arrow spelling `->` is the same claim as `→`.
    case("ascii-arrow", (
        "## Round 3 — a\ndepth 5 -> 6\n## Round 3 — b\ndepth 5 → 7\n"), 1, 1)

    # R82-V2 red controls.
    # 9. a LATER block re-asserting a superseded value is a finding, not silence:
    #    the r82 harness retired the key globally and read this shape clean.
    case("late-contradiction", (
        "## Round 81 — measured outcome\n"
        "| C1 | depth 8 → 9 |\n"
        "## Round 81 — ordinal correction\n"
        "supersedes-ordinal: round-81 depth\n"
        "depth 8 → 8 — the lane stands behind 8.\n"
        "## Round 81 — re-measured (late)\n"
        "depth 8 → 9 — the retired value re-asserted below the correction.\n"), 1, 1)
    # 10. quoted prose is not an assertion: the r82 correction block's citation of
    #     `depth 8 → 9` inside backticks is a quotation, and the block's own named
    #     correction still stands.
    case("quoted-prose-not-assertion", (
        "## Round 81 — measured outcome\n"
        "Axes now: depth9.\n"
        "## Round 81 — ordinal correction\n"
        "supersedes-ordinal: round-81 depth\n"
        "The earlier block prints `C1 | depth 8 → 9`; that 9 is quoted prose.\n"
        "depth 8 → 8 — one named correction.\n"), 0, 0)
    # 11. a correction does not reach its own block's other assertions.
    case("correction-scoped-to-earlier-blocks", (
        "## Round 81 — measured outcome\n"
        "Axes now: depth9, coverage9.\n"
        "## Round 81 — ordinal correction\n"
        "supersedes-ordinal: round-81 depth, coverage\n"
        "depth 8 → 8; coverage 9 → 9 — both named, both stand.\n"), 0, 0)

    failed = [c for c in cases if not c[1]]
    for name, ok, observed in cases:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}: {observed}")
    print(f"SELFTEST total={len(cases)} passed={len(cases) - len(failed)} failed={len(failed)}")
    return 0 if not failed else 3


def read_scorecard_at(repo, revision):
    proc = subprocess.run(
        ["git", "--no-pager", "-C", str(repo), "show", f"{revision}:{SCORECARD}"],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=120)
    if proc.returncode != 0:
        raise CannotEvaluate(f"absent-at-revision:{SCORECARD}")
    return proc.stdout.decode("utf-8", "replace")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--revision")
    group.add_argument("--fixture", type=Path)
    group.add_argument("--selftest", action="store_true")
    p.add_argument("--repo", default=".")
    p.add_argument("--branch", default="master")
    a = p.parse_args(argv)

    if a.selftest:
        return selftest()

    repo = Path(a.repo).resolve()
    revision = None
    text = None
    if a.revision:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import _revision  # noqa: E402  (shared landed-revision binding, QUALITY 27)
        try:
            revision = _revision.bind(repo, a.revision, a.branch).sha
        except _revision.RevisionError as exc:
            print(json.dumps({"claim": CLAIM, "revision": a.revision,
                              "finding": "cannot-evaluate", "problems": [str(exc)]}))
            return 2
        try:
            text = read_scorecard_at(repo, revision)
        except CannotEvaluate as exc:
            print(json.dumps({"claim": CLAIM, "revision": revision,
                              "finding": "cannot-evaluate", "problems": [str(exc)]}))
            return 2
    else:
        if not a.fixture.is_file():
            print(json.dumps({"claim": CLAIM, "finding": "cannot-evaluate",
                              "problems": [f"absent:{a.fixture}"]}))
            return 2
        text = a.fixture.read_text(encoding="utf-8", errors="replace")

    try:
        findings, examined = measure(text)
    except CannotEvaluate as exc:
        print(json.dumps({"claim": CLAIM, "revision": revision, "count": 0,
                          "finding": "cannot-evaluate", "problems": [str(exc)]}))
        return 2

    print(json.dumps({"claim": CLAIM, "revision": revision, "count": len(findings),
                      "examined": examined, "finding": "clean" if not findings else "findings",
                      "findings": findings}))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
