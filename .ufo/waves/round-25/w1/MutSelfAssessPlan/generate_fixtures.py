#!/usr/bin/env python3
"""Mutation-fixture generator for tools/check-self-assessment.py (round 25, C1).

Seat: MutSelfAssessPlan. Read-only against the lane; writes only inside its own
seat directory (or an --out directory under it).

Purpose
-------
The round-25 declaration fixes 23 checks K01..K23 over three documents:

  * the current axes table  - the last table under the last SCORECARD.md heading
    that starts "## Axes - " (em dash);
  * the Capabilities table  - the last table under the last heading that starts
    "## Capabilities";
  * the four SHONEN.md promotion boxes.

For every check id this generator materialises a MUTANT: a copy of the relevant
section carrying exactly ONE defect, plus the check id that defect must trip.
A runner (run_mutations.py, same directory) builds one throwaway git repo per
mutant, runs the checker read-only against it, and records killed / survived.

Baseline modes
--------------
landed    The baseline section is taken verbatim from the given revision, i.e.
          from the lane's own corrected artifacts.  This is the mode that
          matters once the lane's repaired table is landed: every mutant is
          then "pristine lane artifact + one defect" and the pristine run must
          report 0 mismatches.
computed  The baseline axes/Capabilities tables are synthesised from values
          measured at the given revision (note count, SKILL.md line and
          table-line counts, lessons count, corpus/README.md line count,
          census --selftest case count, PROVINCE.md heading presence, census
          --identity arm presence, PROVINCE.md "| ID | Finding" header
          presence, and the axis ordinals read with the declared K01-K06
          regex).  This mode exists so wave 1 can exercise the runner before
          the lane's corrected table is landed; it is a fixture harness, not a
          lane artifact.

Declared grammar implemented here (SCORECARD.md round-25 refinements):
  * K01-K06 ordinal reference regex
        \\b<axis>\\b[^0-9|->\\n]{0,12}?(\\d{1,2})\\s*(?:->|->)\\s*(\\d{1,2})
    both numbers 0..10, last match by line order outside the axes table.
  * K12 stated absent  <- "Core/Frontier/Adjacent not landed"
    stated present <- "Core, Frontier and Adjacent sections present"
  * K14 "--identity` not landed"  /  "--identity` landed"
    observed present only when tools/tsukuroi-census.sh has a case arm
    matching ^\\s*--identity\\)
  * K15 "no formal overlap table"  /  "formal overlap table present"
    observed present when PROVINCE.md has a line starting "| ID | Finding"
  * K16-K23 path grammar: Capabilities cells are read from backticked spans,
    SHONEN boxes from bare tokens; a token is a path when it contains "/" or
    ends in .md/.json/.py/.sh/.txt, after one brace group is expanded.  A row
    or box naming no path is a mismatch.  A box marked [x] must contain
    "non-author verifier:" and a name.

Usage
-----
  python3 generate_fixtures.py --lane <repo> --revision <REV> \\
      --mode landed|computed --out <dir>
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

AXES_HEADING_RE = re.compile(r"^##\s+Axes\s+—")
CAPS_HEADING_RE = re.compile(r"^##\s+Capabilities\b")

AXES = ["depth", "coverage", "operability", "freshness", "calibration", "adjacency"]

ORDINAL_RE = re.compile(
    r"\b(depth|coverage|operability|freshness|calibration|adjacency)\b"
    r"[^0-9|→\n]{0,12}?(\d{1,2})\s*(?:→|->)\s*(\d{1,2})"
)

TOKEN_PRESENT_PROVINCE = "Core, Frontier and Adjacent sections present"
TOKEN_ABSENT_PROVINCE = "Core/Frontier/Adjacent not landed"
TOKEN_IDENTITY_LANDED = "`--identity` landed"
TOKEN_IDENTITY_NOT = "`--identity` not landed"
TOKEN_OVERLAP_PRESENT = "formal overlap table present"
TOKEN_OVERLAP_NONE = "no formal overlap table"


# --------------------------------------------------------------------------
# lane reading (read-only)
# --------------------------------------------------------------------------
def git(lane: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(lane), *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def show(lane: Path, rev: str, path: str) -> str:
    return git(lane, "show", f"{rev}:{path}")


def materialize(lane: Path, rev: str, dest: Path) -> None:
    archive = subprocess.run(["git", "-C", str(lane), "archive", rev], capture_output=True)
    if archive.returncode != 0:
        raise RuntimeError("git archive failed")
    dest.mkdir(parents=True, exist_ok=True)
    tar = subprocess.run(["tar", "-x", "-C", str(dest)], input=archive.stdout, capture_output=True)
    if tar.returncode != 0:
        raise RuntimeError("tar extract failed: " + tar.stderr.decode("utf-8", "replace"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------
# measured values at a revision
# --------------------------------------------------------------------------
def wc_l(text: str) -> int:
    return text.count("\n")


def measure(tree: Path) -> dict:
    skill = (tree / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    readme = (tree / "corpus" / "README.md").read_text(encoding="utf-8", errors="replace")
    census = (tree / "tools" / "tsukuroi-census.sh").read_text(encoding="utf-8", errors="replace")
    province = (tree / "PROVINCE.md").read_text(encoding="utf-8", errors="replace")
    census_cases = None
    proc = subprocess.run(["bash", "tools/tsukuroi-census.sh", "--selftest"], cwd=tree,
                          capture_output=True, text=True, timeout=3600)
    m = re.search(r"PASS \((\d+) cases", proc.stdout + proc.stderr)
    if m:
        census_cases = int(m.group(1))
    notes = glob.glob(str(tree / "corpus" / "knowledge" / "*.md"))
    lessons = [p for p in glob.glob(str(tree / "corpus" / "lessons" / "**"), recursive=True)
               if os.path.isfile(p)]
    plines = province.split("\n")
    return {
        "notes": len(notes),
        "lessons": len(lessons),
        "skill_wc": wc_l(skill),
        "skill_table_lines": sum(1 for l in skill.split("\n") if l.startswith("|")),
        "readme_wc": wc_l(readme),
        "census_cases": census_cases,
        "census_exit": proc.returncode,
        "province_core": any(l.startswith("## Core") for l in plines),
        "province_frontier": any(l.startswith("## Frontier") for l in plines),
        "province_adjacent": any(l.startswith("## Adjacent") for l in plines),
        "province_overlap_present": any(l.startswith("| ID | Finding") for l in plines),
        "census_identity_present": bool(re.search(r"^\s*--identity\)", census, re.M)),
    }


# --------------------------------------------------------------------------
# section extraction
# --------------------------------------------------------------------------
def last_table_after(text: str, heading_re: re.Pattern, header_key: str | None = None):
    """Return (heading_line, heading_index, table_lines, table_line_indexes).

    The declared rule is "the last table under the last heading that starts X".
    A heading owns the tables until the NEXT markdown heading, so the scan
    stops at any line starting with '#'.  Within that scope the table chosen
    is the last one whose header first cell names header_key, falling back to
    the last table in the scope — the same rule the checker applies.
    """
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if heading_re.match(l)]
    if not hits:
        raise RuntimeError(f"no heading matching {heading_re.pattern}")
    start = hits[-1]
    tables: list[tuple[list[str], list[int]]] = []
    cur: list[str] = []
    cur_idx: list[int] = []
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("#"):
            break
        if lines[i].startswith("|"):
            cur.append(lines[i])
            cur_idx.append(i)
        else:
            if cur:
                tables.append((cur, cur_idx))
                cur, cur_idx = [], []
    if cur:
        tables.append((cur, cur_idx))
    if not tables:
        raise RuntimeError(f"no table under heading {heading_re.pattern}")
    if header_key:
        for table, idxs in reversed(tables):
            cells = [c.strip().strip("`").strip().lower() for c in split_row_cells(table[0])]
            if cells and cells[0] == header_key.lower():
                return lines[start], start, table, idxs
    table, idxs = tables[-1]
    return lines[start], start, table, idxs


def split_row_cells(line: str) -> list[str]:
    """Split a markdown table row on pipes outside backtick code spans."""
    cells, current, in_code = [], [], False
    for char in line:
        if char == "`":
            in_code = not in_code
            current.append(char)
            continue
        if char == "|" and not in_code:
            cells.append("".join(current))
            current = []
            continue
        current.append(char)
    cells.append("".join(current))
    if cells and not cells[0].strip():
        cells = cells[1:]
    if cells and not cells[-1].strip():
        cells = cells[:-1]
    return [c.strip() for c in cells]


def replace_last_table(text: str, heading_re: re.Pattern, new_table: list[str],
                       header_key: str | None = None) -> str:
    """Replace the last table under the last heading matching heading_re."""
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if heading_re.match(l)]
    if not hits:
        raise RuntimeError(f"heading {heading_re.pattern} not found")
    start = hits[-1]
    tabs = []
    cur, cur_idx = [], []
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("#"):
            break
        if lines[i].startswith("|"):
            cur.append(lines[i])
            cur_idx.append(i)
        else:
            if cur:
                tabs.append((cur, cur_idx))
                cur, cur_idx = [], []
    if cur:
        tabs.append((cur, cur_idx))
    if not tabs:
        raise RuntimeError(f"no table under {heading_re.pattern}")
    chosen = None
    if header_key:
        for table, idxs in reversed(tabs):
            cells = [c.strip().strip("`").strip().lower() for c in split_row_cells(table[0])]
            if cells and cells[0] == header_key.lower():
                chosen = idxs
                break
    if chosen is None:
        chosen = tabs[-1][1]
    out = lines[:chosen[0]] + list(new_table) + lines[chosen[-1] + 1:]
    return "\n".join(out)


def shonen_boxes(text: str) -> list[str]:
    return [l for l in text.split("\n") if l.startswith("- [")]


def last_ordinals(scorecard: str, table_idxs: set[int]) -> dict:
    """Declared K01-K06 reference: last match by line order outside the axes table."""
    last = {}
    for i, line in enumerate(scorecard.split("\n")):
        if i in table_idxs:
            continue
        for m in ORDINAL_RE.finditer(line):
            if int(m.group(2)) <= 10 and int(m.group(3)) <= 10:
                last[m.group(1)] = {"line": i + 1, "before": int(m.group(2)),
                                    "after": int(m.group(3)), "text": line[:160]}
    return last


# --------------------------------------------------------------------------
# computed baseline (fixture harness only)
# --------------------------------------------------------------------------
def computed_axes_table(obs: dict, ordinals: dict) -> list[str]:
    """Synthesised axes table whose every declared check agrees with the tree.

    The stated tokens follow the OBSERVED state, so the baseline passes:
      * K12 states present only when PROVINCE.md really has Core, Frontier and
        Adjacent headings;
      * K14 states landed only when tools/tsukuroi-census.sh really has a
        --identity case arm;
      * K15 states present only when PROVINCE.md really has a "| ID | Finding"
        header line.
    """
    province_state = (TOKEN_PRESENT_PROVINCE
                      if (obs["province_core"] and obs["province_frontier"] and obs["province_adjacent"])
                      else TOKEN_ABSENT_PROVINCE)
    identity_state = TOKEN_IDENTITY_LANDED if obs["census_identity_present"] else TOKEN_IDENTITY_NOT
    overlap_state = TOKEN_OVERLAP_PRESENT if obs["province_overlap_present"] else TOKEN_OVERLAP_NONE
    score = {a: ordinals.get(a, {}).get("after", 0) for a in AXES}
    return [
        "| Axis | Score | Evidence pointer (counting command) | Last change |",
        "|---|---|---|---|",
        (f"| depth | {score['depth']} | {obs['notes']} notes (`ls corpus/knowledge/*.md \\| wc -l`); "
         f"census {obs['census_cases']} executed cases (`bash tools/tsukuroi-census.sh --selftest`); "
         f"`SKILL.md` {obs['skill_wc']} `wc -l` / {obs['skill_table_lines']} table lines "
         f"(`grep -c '^\\|' SKILL.md`), every rule cited to `corpus/knowledge/*.md`. "
         f"Ceiling: `corpus/lessons/` {obs['lessons']} files. | r25 |"),
        (f"| coverage | {score['coverage']} | 6 gate planes == the surfaces `PROVINCE.md` owns, each with a "
         f"landed note; corpus covers AUR/memory/kill-event/boot classes beyond the r1 five. "
         f"Ceiling: {province_state}; `corpus/README.md` rows stop at r3, {obs['readme_wc']} `wc -l`. | r25 |"),
        (f"| operability | {score['operability']} | `bash tools/tsukuroi-census.sh --selftest` → rc=0 "
         f"`PASS ({obs['census_cases']} cases, {obs['census_cases']} passed, 0 failed)`; "
         f"`bash tools/tsukuroi-census.sh` → rc=1, six-plane rollup; zero-mutation contract held "
         f"(`git status` byte-identical; `db.lck` absent). "
         f"Ceiling: D12 {identity_state} (three-command re-derivation stands). | r25 |"),
        (f"| freshness | {score['freshness']} | every round's record re-ran its predecessor's pins "
         f"(LOG rounds 1–10); receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md`, "
         f"`closeout-r11.md` §5 recheck block. Ceiling: counts are live captures. | r25 |"),
        (f"| calibration | {score['calibration']} | `calibration-synthesis.md` — the claim→re-measure→append→"
         f"supersede→rule loop with its mismeasure rows; errata kept visible rather than rewritten. "
         f"Ceiling: the D13 verification debts still open (`closeout-r11.md` §3.2). | r25 |"),
        (f"| adjacency | {score['adjacency']} | reported-not-absorbed rows across the arc: coredump storm → "
         f"journal workstream + the godot/node/LOVE app lanes; contested scope reported, never absorbed "
         f"(`closeout-r11.md` §3.2; LOG rounds 1–10). Ceiling: {overlap_state}. | r25 |"),
    ]


def computed_capabilities_table(caps_table: list[str], obs: dict) -> list[str]:
    """Keep the lane's four capability rows; repair only the host-census-gate case count."""
    out = []
    for row in caps_table:
        if row.startswith("| host-census-gate "):
            row = re.sub(r"\b(\d+)-case\b", lambda m: f"{obs['census_cases']}-case", row)
            row = re.sub(r"PASS (\d+)/(\d+)", lambda m: f"PASS {obs['census_cases']}/{obs['census_cases']}", row)
        out.append(row)
    return out


# --------------------------------------------------------------------------
# mutation primitives (applied to a section's lines)
# --------------------------------------------------------------------------
def row_index(table: list[str], axis: str) -> int | None:
    for i, row in enumerate(table):
        if row.startswith(f"| {axis} "):
            return i
    return None


def set_score(table: list[str], axis: str, value: int) -> tuple[list[str], int]:
    i = row_index(table, axis)
    if i is None:
        return table, 0
    row = table[i]
    new, n = re.subn(r"^(\| " + re.escape(axis) + r" \| )\d+( \|)",
                     lambda m: m.group(1) + str(value) + m.group(2), row, count=1)
    out = list(table)
    out[i] = new
    return out, n


def bump_in_row(table: list[str], axis: str, pattern: str, repl) -> tuple[list[str], int]:
    i = row_index(table, axis)
    if i is None:
        return table, 0
    row = table[i]
    new, n = re.subn(pattern, repl, row, count=1)
    out = list(table)
    out[i] = new
    return out, n


def swap_in_row(table: list[str], axis: str, old: str, new: str) -> tuple[list[str], int]:
    i = row_index(table, axis)
    if i is None:
        return table, 0
    row = table[i]
    if old not in row:
        return table, 0
    out = list(table)
    out[i] = row.replace(old, new, 1)
    return out, 1


def drop_in_row(table: list[str], axis: str, fragment: str) -> tuple[list[str], int]:
    i = row_index(table, axis)
    if i is None:
        return table, 0
    row = table[i]
    if fragment not in row:
        return table, 0
    out = list(table)
    out[i] = row.replace(fragment, "", 1)
    return out, 1


# --------------------------------------------------------------------------
# fixture definitions
# --------------------------------------------------------------------------
# (id, check, kind, section, description, expected_check_ids, apply)
def axes_score_fixture(axis, delta):
    """Set the axis score one off from the LAST RECORDED ordinal for that axis.

    The offset is relative, never absolute: the recorded value is read from
    SCORECARD.md with the declared K01-K06 regex, so the mutant mismatches
    whichever value the checker itself derives.
    """
    def apply(t, obs, ordinals):
        recorded = ordinals.get(axis, {}).get("after")
        if recorded is None:
            return t, 0
        value = recorded + delta
        if not (0 <= value <= 10):
            value = recorded - delta
        return set_score(t, axis, value)
    return apply


def axes_count_fixture(axis, pattern, repl):
    def apply(t, obs, ordinals):
        return bump_in_row(t, axis, pattern, repl)
    return apply


def _flip(t, obs, axis, observed_token, opposite_token):
    """Swap the stated token for the one that contradicts the observed state."""
    i = row_index(t, axis)
    if i is None:
        return t, 0
    row = t[i]
    if observed_token in row:
        new = row.replace(observed_token, opposite_token, 1)
    elif opposite_token in row:
        new = row.replace(opposite_token, observed_token, 1)
    else:
        return t, 0
    out = list(t)
    out[i] = new
    return out, 1


def _omit(t, obs, axis, token):
    """Remove the statement entirely (unstated is a mismatch)."""
    i = row_index(t, axis)
    if i is None:
        return t, 0
    row = t[i]
    if token not in row:
        return t, 0
    out = list(t)
    out[i] = row.replace(token, "", 1)
    return out, 1


def flip_province(t, obs):
    present = obs["province_core"] and obs["province_frontier"] and obs["province_adjacent"]
    if present:
        return _flip(t, obs, "coverage", TOKEN_PRESENT_PROVINCE, TOKEN_ABSENT_PROVINCE)
    return _flip(t, obs, "coverage", TOKEN_ABSENT_PROVINCE, TOKEN_PRESENT_PROVINCE)


def omit_province(t, obs):
    present = obs["province_core"] and obs["province_frontier"] and obs["province_adjacent"]
    token = TOKEN_PRESENT_PROVINCE if present else TOKEN_ABSENT_PROVINCE
    return _omit(t, obs, "coverage", token)


def flip_identity(t, obs):
    if obs["census_identity_present"]:
        return _flip(t, obs, "operability", TOKEN_IDENTITY_LANDED, TOKEN_IDENTITY_NOT)
    return _flip(t, obs, "operability", TOKEN_IDENTITY_NOT, TOKEN_IDENTITY_LANDED)


def omit_identity(t, obs):
    token = TOKEN_IDENTITY_LANDED if obs["census_identity_present"] else TOKEN_IDENTITY_NOT
    return _omit(t, obs, "operability", token)


def flip_overlap(t, obs):
    if obs["province_overlap_present"]:
        return _flip(t, obs, "adjacency", TOKEN_OVERLAP_PRESENT, TOKEN_OVERLAP_NONE)
    return _flip(t, obs, "adjacency", TOKEN_OVERLAP_NONE, TOKEN_OVERLAP_PRESENT)


def omit_overlap(t, obs):
    token = TOKEN_OVERLAP_PRESENT if obs["province_overlap_present"] else TOKEN_OVERLAP_NONE
    return _omit(t, obs, "adjacency", token)


AXES_FIXTURES = [
    ("M01-ordinal-depth", "K01", "ordinal one off", "axes",
     "depth score in the axes table set one above the last recorded depth ordinal",
     ["K01"], axes_score_fixture("depth", +1)),
    ("M02-ordinal-coverage", "K02", "ordinal one off", "axes",
     "coverage score set one off the last recorded coverage ordinal",
     ["K02"], axes_score_fixture("coverage", -1)),
    ("M03-ordinal-operability", "K03", "ordinal one off", "axes",
     "operability score set one off the last recorded operability ordinal",
     ["K03"], axes_score_fixture("operability", -1)),
    ("M04-ordinal-freshness", "K04", "ordinal one off", "axes",
     "freshness score set one off the last recorded freshness ordinal",
     ["K04"], axes_score_fixture("freshness", -1)),
    ("M05-ordinal-calibration", "K05", "ordinal one off", "axes",
     "calibration score set one off the last recorded calibration ordinal",
     ["K05"], axes_score_fixture("calibration", -1)),
    ("M06-ordinal-adjacency", "K06", "ordinal one off", "axes",
     "adjacency score set one above the last recorded adjacency ordinal",
     ["K06"], axes_score_fixture("adjacency", +1)),
    ("M07-count-notes", "K07", "count one off", "axes",
     "depth row states one more corpus/knowledge note than the tree holds",
     ["K07"], axes_count_fixture("depth", r"(\| )(\d+)( notes\b)",
                                 lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3))),
    ("M08-count-skill-lines", "K08", "count one off", "axes",
     "depth row states one more SKILL.md line than the file holds",
     ["K08"], axes_count_fixture("depth", r"(`SKILL\.md` )(\d+)( `wc -l`)",
                                 lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3))),
    ("M09-count-table-lines", "K09", "count one off", "axes",
     "depth row states one more SKILL.md table line than the file holds",
     ["K09"], axes_count_fixture("depth", r"(\d+)( table lines\b)",
                                 lambda m: str(int(m.group(1)) + 1) + m.group(2))),
    ("M10-count-lessons", "K10", "count one off", "axes",
     "depth row states one more corpus/lessons file than the directory holds",
     ["K10"], axes_count_fixture("depth", r"(`corpus/lessons/` )(\d+)( files)",
                                 lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3))),
    ("M11-count-readme-lines", "K11", "count one off", "axes",
     "coverage row states one more corpus/README.md line than the file holds",
     ["K11"], axes_count_fixture("coverage", r"(`corpus/README\.md`[^|]*?)(\d+)( `wc -l`)",
                                 lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3))),
    ("M13-count-cases", "K13", "count one off", "axes",
     "operability row states one more census --selftest case than the census prints",
     ["K13"], axes_count_fixture("operability", r"(PASS \(\d+ cases, \d+ passed)",
                                 lambda m: re.sub(r"\d+", lambda d: str(int(d.group(0)) + 1), m.group(1)))),
    ("M12-stale-province", "K12", "stale phrase", "axes",
     "coverage row states the OPPOSITE of the observed PROVINCE.md Core/Frontier/Adjacent state",
     ["K12"], lambda t, o, d: flip_province(t, o)),
    ("M27-omit-province", "K12", "omitted fact", "axes",
     "coverage row omits the PROVINCE.md Core/Frontier/Adjacent statement entirely, so the "
     "check is unstated",
     ["K12"], lambda t, o, d: omit_province(t, o)),
    ("M14-stale-identity", "K14", "stale phrase", "axes",
     "operability row states the OPPOSITE of the observed `--identity` state",
     ["K14"], lambda t, o, d: flip_identity(t, o)),
    ("M28-omit-identity", "K14", "omitted fact", "axes",
     "operability row omits the `--identity` statement entirely",
     ["K14"], lambda t, o, d: omit_identity(t, o)),
    ("M15-stale-overlap", "K15", "stale phrase", "axes",
     "adjacency row states the OPPOSITE of the observed formal-overlap-table state",
     ["K15"], lambda t, o, d: flip_overlap(t, o)),
    ("M15b-omit-overlap", "K15", "omitted fact", "axes",
     "adjacency row omits the formal-overlap-table statement entirely, so the check is unstated",
     ["K15"], lambda t, o, d: omit_overlap(t, o)),
]


def cap_row_span(caps: list[str], key: str, old_span: str, new_span: str) -> tuple[list[str], int]:
    """Replace one exact backticked span of the named capability row.

    The declared grammar reads Capabilities cells from backticked spans, so the
    mutation must swap a span that the checker actually reads, not a token
    buried in prose.
    """
    out = list(caps)
    for i, row in enumerate(out):
        if not row.startswith(f"| {key} "):
            continue
        needle = f"`{old_span}`"
        if needle not in row:
            return out, 0
        out[i] = row.replace(needle, f"`{new_span}`", 1)
        return out, 1
    return out, 0


def cap_cases(caps: list[str], delta: int) -> tuple[list[str], int]:
    out = list(caps)
    for i, row in enumerate(out):
        if not row.startswith("| host-census-gate "):
            continue
        new = re.sub(r"\b(\d+)-case\b", lambda m: f"{int(m.group(1)) + delta}-case", row)
        new = re.sub(r"PASS (\d+)/(\d+)",
                     lambda m: f"PASS {int(m.group(1)) + delta}/{int(m.group(2)) + delta}", new)
        out[i] = new
        return out, 1
    return out, 0


def cap_omit_cases(caps: list[str]) -> tuple[list[str], int]:
    out = list(caps)
    for i, row in enumerate(out):
        if not row.startswith("| host-census-gate "):
            continue
        new = re.sub(r"\b\d+-case\b", "the selftest case count", row)
        new = re.sub(r"PASS \d+/\d+", "PASS", new)
        out[i] = new
        return out, 1
    return out, 0


CAPS_FIXTURES = [
    ("M16-capability-path-sources", "K16", "broken capability path", "capabilities",
     "sources-registry row names a corpus path that does not exist at the revision",
     ["K16"], lambda c, o: cap_row_span(c, "sources-registry",
                                        "corpus/SOURCES.md", "corpus/SOURCES-registry.md")),
    ("M17-capability-path-census", "K17", "broken capability path", "capabilities",
     "host-census-gate row names a census evidence path that does not exist at the revision",
     ["K17"], lambda c, o: cap_row_span(c, "host-census-gate",
                                        ".ufo/evidence/round-1-kaika/scout-live.md",
                                        ".ufo/evidence/round-1-kaika/scout-live-absent.md")),
    ("M29-capability-cases-off", "K17", "count one off", "capabilities",
     "host-census-gate row states one more selftest case than the census prints",
     ["K17"], lambda c, o: cap_cases(c, +1)),
    ("M30-capability-omit-cases", "K17", "omitted fact", "capabilities",
     "host-census-gate row omits the selftest case count entirely",
     ["K17"], lambda c, o: cap_omit_cases(c)),
    ("M18-capability-path-metadata", "K18", "broken capability path", "capabilities",
     "root-metadata-observer row names a fixture path that does not exist at the revision",
     ["K18"], lambda c, o: cap_row_span(c, "root-metadata-observer",
                                        ".ufo/waves/round-12/resumed/{after,selftest-after,mode-policy-mutant}.json",
                                        ".ufo/waves/round-12/resumed/absent-fixture.json")),
    ("M19-capability-path-bootchain", "K19", "broken capability path", "capabilities",
     "boot-chain-audit row names a capture path that does not exist at the revision",
     ["K19"], lambda c, o: cap_row_span(c, "boot-chain-audit",
                                        ".ufo/waves/round-17/l1-capture/audit-live.txt",
                                        ".ufo/waves/round-17/l1-capture/absent-audit.txt")),
]


def shonen_boxes_with_ranges(lines: list[str]):
    """Return [(ordinal, [line indexes of the box header + its body])]."""
    boxes = []
    i = 0
    ordinal = 0
    while i < len(lines):
        if lines[i].startswith("- ["):
            idxs = [i]
            j = i + 1
            while j < len(lines) and lines[j].strip() and not lines[j].startswith("- ["):
                idxs.append(j)
                j += 1
            boxes.append((ordinal, idxs))
            ordinal += 1
            i = j
            continue
        i += 1
    return boxes


def shonen_checked(text: str) -> tuple[str, int]:
    """Flip the FIRST box's marker to [x].  The box still says non-author
    verification is owed and names no `non-author verifier:`, so the declared
    rule "a box marked [x] must contain `non-author verifier:` and a name"
    fails."""
    lines = text.split("\n")
    for i, l in enumerate(lines):
        if l.startswith("- [~]"):
            lines[i] = l.replace("- [~]", "- [x]", 1)
            return "\n".join(lines), 1
    return text, 0


def shonen_break_path(text: str, box_ordinal: int, old_path: str) -> tuple[str, int]:
    """Point one named path of a box at a path that does not exist."""
    lines = text.split("\n")
    boxes = shonen_boxes_with_ranges(lines)
    for ordinal, idxs in boxes:
        if ordinal != box_ordinal:
            continue
        for i in idxs:
            if old_path in lines[i]:
                lines[i] = lines[i].replace(old_path, "corpus/knowledge/absent-fixture.md", 1)
                return "\n".join(lines), 1
    return text, 0


def shonen_drop_paths(text: str, box_ordinal: int) -> tuple[str, int]:
    """Leave the box naming no path at all (declared a mismatch)."""
    lines = text.split("\n")
    boxes = shonen_boxes_with_ranges(lines)
    for ordinal, idxs in boxes:
        if ordinal != box_ordinal:
            continue
        applied = 0
        for i in idxs:
            new = re.sub(r"[A-Za-z0-9_./-]*\.md\b", "", lines[i])
            if new != lines[i]:
                applied += 1
            lines[i] = new
        return "\n".join(lines), applied
    return text, 0


SHONEN_FIXTURES = [
    ("M20-shonen-box1-checked", "K20", "SHONEN [x] without verifier", "shonen",
     "SHONEN box 1 flipped from [~] to [x] while it still says non-author verification is owed, "
     "so it is a [x] box with no `non-author verifier:` name",
     ["K20"], lambda t: shonen_checked(t)),
    ("M31-shonen-box1-no-path", "K20", "omitted fact", "shonen",
     "SHONEN box 1 names no repository path at all",
     ["K20"], lambda t: shonen_drop_paths(t, 0)),
    ("M21-shonen-box2-path", "K21", "broken path", "shonen",
     "SHONEN box 2 names a corpus path that does not exist at the revision",
     ["K21"], lambda t: shonen_break_path(t, 1, "corpus/knowledge/host-health-report-r3.md")),
    ("M22-shonen-box3-path", "K22", "broken path", "shonen",
     "SHONEN box 3 names a corpus path that does not exist at the revision",
     ["K22"], lambda t: shonen_break_path(t, 2, "corpus/knowledge/executor-test-sufficiency.md")),
    ("M23-shonen-box4-path", "K23", "broken path", "shonen",
     "SHONEN box 4 names a repo path that does not exist at the revision",
     ["K23"], lambda t: shonen_break_path(t, 3, ".ufo/waves/round-12/resumed/OverlapHostR.md")),
    ("M32-shonen-box4-no-path", "K23", "omitted fact", "shonen",
     "SHONEN box 4 names no repository path at all",
     ["K23"], lambda t: shonen_drop_paths(t, 3)),
]


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
    ap.add_argument("--revision", required=True)
    ap.add_argument("--mode", choices=["landed", "computed"], default="computed")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    lane = Path(args.lane).resolve()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    scorecard = show(lane, args.revision, "SCORECARD.md")
    shonen = show(lane, args.revision, "SHONEN.md")

    with tempfile.TemporaryDirectory(prefix="mut-selfassess-") as tmp:
        tree = Path(tmp) / "tree"
        materialize(lane, args.revision, tree)
        obs = measure(tree)

    axes_heading, axes_idx, axes_table, axes_idxs = last_table_after(scorecard, AXES_HEADING_RE, "Axis")
    caps_heading, caps_idx, caps_table, caps_idxs = last_table_after(scorecard, CAPS_HEADING_RE, "Capability")
    ordinals = last_ordinals(scorecard, set(axes_idxs))

    if args.mode == "computed":
        base_axes = computed_axes_table(obs, ordinals)
        base_caps = computed_capabilities_table(caps_table, obs)
    else:
        base_axes = axes_table
        base_caps = caps_table

    # The baseline SCORECARD.md is the revision's own file with the baseline
    # tables substituted in.  Every fixture that carries a whole SCORECARD.md
    # derives from THIS text, so a structural fixture differs from the
    # baseline by its injected defect alone.
    baseline_scorecard = replace_last_table(scorecard, AXES_HEADING_RE, base_axes, "Axis")
    baseline_scorecard = replace_last_table(baseline_scorecard, CAPS_HEADING_RE, base_caps, "Capability")

    base_dir = out / "baseline"
    base_dir.mkdir(exist_ok=True)
    (base_dir / "axes-table.md").write_text("\n".join(base_axes) + "\n", encoding="utf-8")
    (base_dir / "capabilities-table.md").write_text("\n".join(base_caps) + "\n", encoding="utf-8")
    (base_dir / "shonen.md").write_text(shonen, encoding="utf-8")
    (base_dir / "SCORECARD.md").write_text(baseline_scorecard, encoding="utf-8")

    manifest = {
        "generated_for": "tools/check-self-assessment.py",
        "lane": str(lane),
        "revision": args.revision,
        "mode": args.mode,
        "observed": obs,
        "axes_heading_line": axes_heading,
        "capabilities_heading_line": caps_heading,
        "ordinal_reference": ordinals,
        "baseline_sha256": {
            "axes-table.md": sha256_text("\n".join(base_axes) + "\n"),
            "capabilities-table.md": sha256_text("\n".join(base_caps) + "\n"),
            "shonen.md": sha256_text(shonen),
        },
        "fixtures": [],
        "not_materializable": [],
    }

    def record(fid, section, check, kind, desc, expected, files, applied, extra=None):
        d = out / "fixtures" / fid
        d.mkdir(parents=True, exist_ok=True)
        meta = {
            "fixture": fid,
            "check": check,
            "kind": kind,
            "description": desc,
            "expected_check_ids": expected,
            "section": section,
            "files": files,
            "substitutions_applied": applied,
        }
        if extra:
            meta.update(extra)
        (d / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        manifest["fixtures"].append(meta)
        if applied == 0:
            manifest["not_materializable"].append(fid)

    # ---- axes fixtures ----------------------------------------------------
    for fid, check, kind, _sec, desc, expected, fn in AXES_FIXTURES:
        table, applied = fn(base_axes, obs, ordinals)
        d = out / "fixtures" / fid
        d.mkdir(parents=True, exist_ok=True)
        text = "\n".join(table) + "\n"
        (d / "axes-table.md").write_text(text, encoding="utf-8")
        record(fid, "axes", check, kind, desc, expected, ["axes-table.md"], applied,
               {"sha256": sha256_text(text)})

    # ---- capabilities fixtures -------------------------------------------
    for fid, check, kind, _sec, desc, expected, fn in CAPS_FIXTURES:
        caps, applied = fn(base_caps, obs)
        d = out / "fixtures" / fid
        d.mkdir(parents=True, exist_ok=True)
        text = "\n".join(caps) + "\n"
        (d / "capabilities-table.md").write_text(text, encoding="utf-8")
        record(fid, "capabilities", check, kind, desc, expected, ["capabilities-table.md"], applied,
               {"sha256": sha256_text(text)})

    # ---- shonen fixtures --------------------------------------------------
    for fid, check, kind, _sec, desc, expected, fn in SHONEN_FIXTURES:
        text, applied = fn(shonen)
        d = out / "fixtures" / fid
        d.mkdir(parents=True, exist_ok=True)
        (d / "shonen.md").write_text(text, encoding="utf-8")
        record(fid, "shonen", check, kind, desc, expected, ["shonen.md"], applied,
               {"sha256": sha256_text(text)})

    # ---- structural fixtures ----------------------------------------------
    # These derive from the BASELINE SCORECARD.md, so the only difference from
    # the baseline is the injected heading.
    base_lines = baseline_scorecard.split("\n")
    base_heading = [i for i, l in enumerate(base_lines) if AXES_HEADING_RE.match(l)][-1]
    base_table_start = None
    base_table_end = None
    for i in range(base_heading + 1, len(base_lines)):
        if base_lines[i].startswith("#"):
            break
        if base_lines[i].startswith("|"):
            if base_table_start is None:
                base_table_start = i
            base_table_end = i
    stale = []
    for r in base_axes:
        stale.append(re.sub(r"^(\| depth \| )(\d+)", lambda m: m.group(1) + "5", r)
                     if r.startswith("| depth ") else r)

    # (a) an extra "## Axes — " heading BEFORE the current one (not last)
    extra = ["## Axes — superseded round-11 draft (historical, retained for the move log)", ""] + stale + [""]
    new_text = "\n".join(base_lines[:base_heading] + extra + base_lines[base_heading:])
    d = out / "fixtures" / "M24-axes-second-heading-not-last"
    d.mkdir(parents=True, exist_ok=True)
    (d / "SCORECARD.md").write_text(new_text, encoding="utf-8")
    record("M24-axes-second-heading-not-last", "scorecard", "K01..K15 (selection)",
           "second `## Axes — ` heading that is not last",
           "an EARLIER `## Axes — ` heading carries a stale axes table (depth 5). The declared rule "
           "takes the LAST such heading, so a correct checker reports no mismatch; a checker that "
           "reads the first heading falsely trips K01. Control fixture: the injected defect must "
           "NOT produce a mismatch.",
           [], ["SCORECARD.md"], 1, {"control": True, "sha256": sha256_text(new_text)})

    # (b) an extra "## Axes — " heading AFTER the current one (it becomes the last)
    extra2 = ["", "## Axes — round-25 re-measure (stale copy)", ""] + stale + [""]
    new_text2 = "\n".join(base_lines[:base_table_end + 1] + extra2 + base_lines[base_table_end + 1:])
    d = out / "fixtures" / "M25-axes-second-heading-last"
    d.mkdir(parents=True, exist_ok=True)
    (d / "SCORECARD.md").write_text(new_text2, encoding="utf-8")
    record("M25-axes-second-heading-last", "scorecard", "K01",
           "second `## Axes — ` heading that is last",
           "a LATER `## Axes — ` heading carries a stale axes table (depth 5). The declared rule "
           "takes the LAST such heading, so the stale table becomes the current axes table and the "
           "checker must trip K01 (depth 5 against the recorded 8).",
           ["K01"], ["SCORECARD.md"], 1, {"sha256": sha256_text(new_text2)})

    # (c) a table row with an extra pipe
    extra_pipe = []
    for r in base_axes:
        extra_pipe.append(r.replace("| depth |", "| depth ||", 1) if r.startswith("| depth ") else r)
    d = out / "fixtures" / "M26-axes-extra-pipe"
    d.mkdir(parents=True, exist_ok=True)
    text = "\n".join(extra_pipe) + "\n"
    (d / "axes-table.md").write_text(text, encoding="utf-8")
    record("M26-axes-extra-pipe", "axes", "K01 (row shape)",
           "table row with an extra pipe",
           "the depth row of the axes table carries an extra `|`, so a fixed-column parser "
           "misreads the score cell. The checker must still attribute a mismatch (K01) or refuse "
           "to evaluate (exit 2); it must not report a clean pass.",
           ["K01"], ["axes-table.md"], 1, {"sha256": sha256_text(text),
                                           "accept_exit_2": True})

    manifest["fixtures"].sort(key=lambda m: m["fixture"])
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=False) + "\n",
                                        encoding="utf-8")
    print(f"mode={args.mode} revision={args.revision}")
    print(f"fixtures={len(manifest['fixtures'])} not_materializable={manifest['not_materializable']}")
    print(f"observed={json.dumps(obs, sort_keys=True)}")
    print(f"ordinal_reference={json.dumps({a: ordinals.get(a, {}).get('after') for a in AXES})}")
    print(f"out={out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
