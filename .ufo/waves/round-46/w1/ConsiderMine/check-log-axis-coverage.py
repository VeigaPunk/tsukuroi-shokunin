#!/usr/bin/env python3
"""Read-only check backing the burst-aware-reading criterion.

Two mechanical checks over committed lane bytes, both reproduced by observed
misses in rounds 44 and 45:

A. axis grade coverage -- every axis the non-author closure grades `improved`
   or `harmed` in its per-axis table is named in that round's LOG.md entry.
   (Round 44: `adjacency | harmed` at round-44-verifier-spotcheck.md:137 while
   the round-44 LOG entry never says "adjacency".)

B. disposition conflict -- a routed-defect row that states `closed` is not
   contradicted by a bullet in the same lesson's "Conflicts recorded verbatim"
   list that names the same defect id and says unchanged / half / not.
   (Round 45: `D3 ... | closed` at corpus/lessons/round-45.md:94 against the
   bullet at :108 "marks D3 'done' ... are unchanged from base".)

Numbered-list disposition sections (rounds 43 and 44) are not table-shaped and
are reported SKIPPED: their cells need a reader.

Usage: check-log-axis-coverage.py [--lane DIR] [--round 43 44 45]
"""
import argparse
import os
import re
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
ap.add_argument("--round", nargs="*", type=int, default=[43, 44, 45])
a = ap.parse_args()

log_path = os.path.join(a.lane, "LOG.md")
log_lines = open(log_path, encoding="utf-8").read().splitlines()

blocks = {}
cur = None
start = 0
for i, line in enumerate(log_lines, 1):
    m = re.match(r"^## Round (\d+) ", line)
    if m:
        if cur is not None:
            blocks[cur] = (start, i - 1)
        cur = int(m.group(1))
        start = i
    elif line.startswith("## ") and cur is not None:
        blocks[cur] = (start, i - 1)
        cur = None
if cur is not None:
    blocks[cur] = (start, len(log_lines))

findings = []
checked_axes = 0
checked_rows = 0
skipped = []

AXIS_ROW = re.compile(r"^\|\s*([a-z]+)\s*\|\s*(improved|unchanged|harmed)\s*\|")
DEFECT_ROW = re.compile(r"^\|\s*(D\d+)\b([^|]*)\|\s*([^|]+?)\s*\|")

for rnd in a.round:
    if rnd not in blocks:
        findings.append(("NO-LOG-BLOCK", f"LOG.md", f"no '## Round {rnd} ' heading"))
        continue
    lo, hi = blocks[rnd]
    block = "\n".join(log_lines[lo - 1:hi])

    spot = os.path.join(a.lane, "corpus", "lessons", f"round-{rnd}-verifier-spotcheck.md")
    if os.path.exists(spot):
        for n, line in enumerate(open(spot, encoding="utf-8").read().splitlines(), 1):
            m = AXIS_ROW.match(line)
            if not m:
                continue
            axis, grade = m.group(1), m.group(2)
            if grade not in ("improved", "harmed"):
                continue
            checked_axes += 1
            if not re.search(r"\b" + axis + r"\b", block, re.I):
                findings.append(
                    (
                        "AXIS-GRADE-OMITTED",
                        f"corpus/lessons/round-{rnd}-verifier-spotcheck.md:{n}",
                        f"{axis} graded {grade} but the round-{rnd} LOG entry "
                        f"(LOG.md:{lo}-{hi}) never names it",
                    )
                )

    lesson = os.path.join(a.lane, "corpus", "lessons", f"round-{rnd}.md")
    if not os.path.exists(lesson):
        continue
    text = open(lesson, encoding="utf-8").read().splitlines()
    states = {}
    for n, line in enumerate(text, 1):
        m = DEFECT_ROW.match(line)
        if m:
            states[m.group(1)] = (m.group(3).strip(), n)
    if not states:
        for n, line in enumerate(text, 1):
            if re.match(r"^## Round-\d+ routed defects", line):
                skipped.append(
                    f"corpus/lessons/round-{rnd}.md:{n} numbered-list disposition "
                    f"(not table-shaped): needs a reader"
                )
                break
        continue
    conflict_at = next((n for n, l in enumerate(text, 1) if l.startswith("Conflicts recorded")), None)
    bullets = []
    if conflict_at:
        cur_b = None
        for n in range(conflict_at, len(text) + 1):
            l = text[n - 1]
            if l.startswith("## ") and n > conflict_at:
                break
            if l.strip().startswith("- "):
                if cur_b:
                    bullets.append(cur_b)
                cur_b = [n, l.strip()[2:]]
            elif cur_b is not None and l.startswith("  ") and l.strip():
                cur_b[1] += " " + l.strip()
            elif not l.strip():
                if cur_b:
                    bullets.append(cur_b)
                cur_b = None
        if cur_b:
            bullets.append(cur_b)
    for did, (state, n) in sorted(states.items()):
        checked_rows += 1
        if not state.startswith("closed"):
            continue
        for bn, bl in bullets:
            if re.search(r"\b" + did + r"\b", bl) and re.search(
                r"unchanged|half closed|\bnot \b", bl
            ):
                findings.append(
                    (
                        "DISPOSITION-CONFLICT",
                        f"corpus/lessons/round-{rnd}.md:{n}",
                        f"{did} stated '{state}' while :{bn} names {did} as unchanged "
                        f"/ half closed",
                    )
                )

for kind, where, what in findings:
    print(f"{kind} {where}: {what}")
for s in skipped:
    print(f"SKIPPED {s}")
print()
print(
    f"TSUKUROI_BURST_READ_CHECK: findings={len(findings)} "
    f"axes_checked={checked_axes} disposition_rows_checked={checked_rows} "
    f"skipped_sections={len(skipped)}"
)
sys.exit(1 if findings else 0)
