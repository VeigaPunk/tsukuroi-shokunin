#!/usr/bin/env python3
"""Mutation matrix over the round-44 SOURCES.md rows (fixture copy only)."""
import json
import re
import subprocess
import sys

CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
REAL = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md"
FIX = "/fast/scratch/hyaku/tsukuroi-r44/C2ExecFinalSources/fixture/lane/corpus/SOURCES.md"

base = open(REAL).read().splitlines(keepends=True)


def row_index(lines, rid):
    for i, line in enumerate(lines):
        if re.match(r"^\s*\| *%s *\|" % rid, line):
            return i
    raise SystemExit("row %s not found" % rid)


def cells(line):
    body = line.strip()
    assert body.startswith("|") and body.endswith("|")
    return [c.strip() for c in body.strip("|").split("|")]


def rebuild(vals):
    return "| " + " | ".join(vals) + " |\n"


def mutate_row(rid, fn):
    lines = list(base)
    i = row_index(lines, rid)
    vals = cells(lines[i])
    fn(vals)
    lines[i] = rebuild(vals)
    return lines


def run(lines, mode="validate", label=""):
    open(FIX, "w").writelines(lines)
    p = subprocess.run([CENSUS, mode, "--file", FIX], capture_output=True, text=True)
    codes = sorted({m for m in re.findall(r"\t([EW]\d\d)\t", p.stdout)})
    hits = [l for l in p.stdout.splitlines() if re.search(r"\t[EW]\d\d\t", l)]
    return {"label": label, "exit": p.returncode, "codes": codes, "lines": hits}


def drop_last(v):
    v.pop()


def set_status_watched(v):
    v[7] = "watched"


def set_usedby_missing(v):
    v[10] = "corpus/knowledge/btrfs-scrub-record-r44-missing.md"


def set_opened_future(v):
    v[8] = "2027-01-01"


def set_recheck_bogus(v):
    v[9] = "3w"


def set_tier_d(v):
    v[3] = "D"


def set_kind_bogus(v):
    v[2] = "source"


def set_usedby_dash(v):
    v[10] = "\u2014"


def set_community(v):
    v[2] = "community"


def outside_registry(rid):
    lines = list(base)
    i = row_index(lines, rid)
    row = lines.pop(i)
    j = next(k for k, l in enumerate(lines) if l.startswith("## Paths"))
    lines.insert(j + 1, row)
    return lines


results = []
results.append(run(base, label="control-unmutated"))

for rid, fn, name in [
    ("S242", drop_last, "S242-drop-usedby-cell"),
    ("S242", set_status_watched, "S242-status-watched"),
    ("S242", set_usedby_missing, "S242-usedby-dangling"),
    ("S242", set_opened_future, "S242-opened-future"),
    ("S242", set_recheck_bogus, "S242-recheck-3w"),
    ("S242", set_tier_d, "S242-tier-D"),
    ("S242", set_kind_bogus, "S242-kind-source"),
    ("S243", drop_last, "S243-drop-usedby-cell"),
    ("S244", set_status_watched, "S244-status-watched"),
    ("S245", set_community, "S245-community-at-A"),
    ("S242", set_usedby_dash, "S242-usedby-dash-warning-only"),
]:
    results.append(run(mutate_row(rid, fn), label=name))

for rid in ("S242", "S245"):
    results.append(run(outside_registry(rid), label="%s-outside-registry" % rid))

# duplicate id: copy S242 row verbatim right after itself
lines = list(base)
i = row_index(lines, "S242")
lines.insert(i + 1, lines[i])
results.append(run(lines, label="S242-duplicate-id"))

# census-row sensitivity: remove S245 entirely
lines = list(base)
i = row_index(lines, "S245")
lines.pop(i)
open("mutations.json","w").write(json.dumps({"mutations": results}, indent=1))
open(FIX, "w").writelines(base)
print("WROTE", len(results), "results")
