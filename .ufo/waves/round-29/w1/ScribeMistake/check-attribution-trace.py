#!/usr/bin/env python3
"""Draft check for the round-29 Mistake row: an attribution names process evidence.

The defect it is built against: in round 28 the L1 blamed seat RevFamilyB2 for
sandbox commits that seat SentinelBattery had made, named the seat in the round
lesson, and cancelled it; the row itself records that the "attribution is by
assignment and timing, not by a process trace" (corpus/lessons/round-28.md:49 at
81a061a), and an appended correction (same file, "### Correction to
R28-SEAT-COMMITTED-IN-LANE") names the real writer and says the seat "was
cancelled on a wrong suspicion".

Rules.  Each row of a "Mistakes" table yields at most one finding per code:

  UNTRACED  the row names a seat and disclaims a process trace ("not by a process
            trace", "attribution is by ... timing") while carrying no trace token
            (environ, GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE, argv, pid, strace,
            shell history).
  UNOWNED   the row names a seat as the actor but cites no .ufo/ path whose text
            carries that seat's own name (its report or seat directory).  A commit
            listing is not a writer trace.
  REVERSED  a "Correction to <ID>" section carries reversal wording ("is wrong",
            "wrong suspicion", "incorrect") and names a seat the row did not name.

Exit 1 if any finding fires, 0 otherwise.  --selftest runs five fixtures and
prints PASS/FAIL per case plus a summary line.

Scope limits: this reads lesson prose, not process records; it can refuse an
attribution that lacks a cited trace but cannot prove a cited trace correct.
"""

import argparse
import re
import sys
import tempfile
from pathlib import Path

SEAT = re.compile(r"\b[A-Z][a-z]+(?:[A-Z][A-Za-z0-9]*)+\b")
TRACE_TOKENS = (
    "environ",
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "argv",
    " pid",
    "strace",
    "shell history",
)
DISCLAIM = re.compile(r"not by a process trace|attribution is by [^.|]*timing", re.I)
REVERSAL = re.compile(r"is wrong|wrong suspicion|incorrect", re.I)
UFOPATH = re.compile(r"\.ufo/[^\s`'\",;)]+")
MISTAKES = re.compile(r"^(#{2,4})\s+Mistakes\b")
CORRECTION = re.compile(r"^(#{2,4})\s+Correction to\s+(\S+)")
HEADING = re.compile(r"^(#{1,6})\s")


def table_rows(lines):
    """Rows of every Mistakes table: list of (id, cells)."""
    out = []
    i = 0
    while i < len(lines):
        m = MISTAKES.match(lines[i])
        if not m:
            i += 1
            continue
        level = len(m.group(1))
        i += 1
        while i < len(lines):
            line = lines[i]
            h = HEADING.match(line)
            if h and len(h.group(1)) <= level:
                break
            if line.startswith("|"):
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if (
                    cells
                    and cells[0]
                    and cells[0] != "ID"
                    and not set(cells[0]) <= set("-: ")
                ):
                    out.append((cells[0], cells))
            i += 1
    return out


def corrections(lines):
    """(id, body_text) for each Correction to <ID> section."""
    out = []
    i = 0
    while i < len(lines):
        m = CORRECTION.match(lines[i])
        if not m:
            i += 1
            continue
        level = len(m.group(1))
        ident = m.group(2).strip("`*_ ")
        i += 1
        body = []
        while i < len(lines):
            h = HEADING.match(lines[i])
            if h and len(h.group(1)) <= level:
                break
            body.append(lines[i])
            i += 1
        out.append((ident, "\n".join(body)))
    return out


def analyse(text):
    lines = text.splitlines()
    findings = []
    rows = table_rows(lines)
    for ident, cells in rows:
        # Rules 1 and 2 read the evidence-pointer cell only: a seat named in the
        # Captured-by or Fix cell is a recorder or a target, not an attribution.
        evidence = cells[2] if len(cells) > 2 else " | ".join(cells)
        seats = set(SEAT.findall(evidence))
        if not seats:
            continue
        if DISCLAIM.search(evidence) and not any(t in evidence for t in TRACE_TOKENS):
            findings.append((ident, "UNTRACED", "seat=" + ",".join(sorted(seats))))
        cited = UFOPATH.findall(evidence)
        if not any(s in p for s in seats for p in cited):
            findings.append(
                (ident, "UNOWNED", "seat=" + ",".join(sorted(seats)) + " cited=0")
            )
    row_ids = {ident for ident, _ in rows}
    row_seats = {}
    for ident, cells in rows:
        ev = cells[2] if len(cells) > 2 else " | ".join(cells)
        row_seats[ident] = set(SEAT.findall(ev))
    ncorr = 0
    for ident, body in corrections(lines):
        ncorr += 1
        if ident not in row_ids or not REVERSAL.search(body):
            continue
        new = set(SEAT.findall(body)) - row_seats[ident]
        if new:
            findings.append(
                (
                    ident,
                    "REVERSED",
                    "original="
                    + ",".join(sorted(row_seats[ident]))
                    + " correction="
                    + ",".join(sorted(new)),
                )
            )
    return findings, len(rows), ncorr


def report(path):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    findings, nrows, ncorr = analyse(text)
    for ident, code, detail in findings:
        print(f"FINDING {ident} {code} {detail}")
    print(
        f"verdict findings={len(findings)} rows={nrows} corrections={ncorr} "
        f"exit={1 if findings else 0}"
    )
    return 1 if findings else 0


FIXTURES = {
    "r28-live-shape": (
        """# Round 28 — lesson
### Mistakes added before closure
| ID | Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|---|
| R28-SEAT-COMMITTED-IN-LANE | seat scope breach | a wave-1 seat's sandbox driver committed battery mutants inside the lane repository: sandbox commit `a330fb0` and children `ee430cd` (lane `git reflog`). The mutant names are the B2 family assigned to seat RevFamilyB2 (cancelled by the L1 at 19:15Z); attribution is by assignment and timing, not by a process trace. | the wave contract, stated not enforced | update-ref repair |
### Correction to R28-SEAT-COMMITTED-IN-LANE
The attribution above to RevFamilyB2 is wrong. Seat SentinelBattery disclosed that it created the sandbox commits itself.
""",
        {("R28-SEAT-COMMITTED-IN-LANE", "UNTRACED"),
         ("R28-SEAT-COMMITTED-IN-LANE", "UNOWNED"),
         ("R28-SEAT-COMMITTED-IN-LANE", "REVERSED")},
    ),
    "clean-cited": (
        """## Mistakes
| ID | Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|---|
| R29-A | scope breach | process trace: GIT_DIR in the child environ; seat SentinelBattery disclosed it in `.ufo/waves/round-28/w1/SentinelBattery.md` | QUALITY 3 | scrub GIT_* |
""",
        set(),
    ),
    "untraced-only": (
        """## Mistakes
| ID | Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|---|
| R29-B | attribution | seat SeatA is named in `.ufo/waves/round-29/w1/SeatA/SeatA.md`; attribution is by assignment and timing. | none | require a trace |
""",
        {("R29-B", "UNTRACED")},
    ),
    "reversed-only": (
        """## Mistakes
| ID | Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|---|
| R29-C | scope breach | process trace: argv in `.ufo/waves/round-29/w1/SeatA/SeatA.md` | none | none |
### Correction to R29-C
The attribution to SeatA is wrong. Seat SeatB made the write.
""",
        {("R29-C", "REVERSED")},
    ),
    "correction-other-id": (
        """## Mistakes
| ID | Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|---|
| R29-D | scope breach | process trace: environ, cited `.ufo/waves/round-29/w1/SeatA/SeatA.md` | none | none |
### Correction to R29-Z
This correction is wrong and names Seat SeatB.
""",
        set(),
    ),
}


def selftest():
    failed = 0
    tmp = Path(tempfile.mkdtemp(prefix="attr-trace-selftest-"))
    for name, (text, expected) in FIXTURES.items():
        path = tmp / (name + ".md")
        path.write_text(text, encoding="utf-8")
        findings, _, _ = analyse(path.read_text(encoding="utf-8"))
        got = {(ident, code) for ident, code, _ in findings}
        ok = got == expected
        failed += 0 if ok else 1
        print(
            ("PASS " if ok else "FAIL ")
            + name
            + (" expected=" + ",".join(sorted(c for _, c in expected)) if not ok else "")
            + (" got=" + ",".join(sorted(c for _, c in got)) if not ok else "")
        )
    print(f"selftest cases={len(FIXTURES)} failed={failed}")
    return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.lesson:
        ap.error("--lesson or --selftest")
    return report(a.lesson)


if __name__ == "__main__":
    sys.exit(main())
