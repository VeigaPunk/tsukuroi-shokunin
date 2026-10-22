#!/usr/bin/env python3
r"""Count self-assessment mismatches between a lane's stated axes and observed state.

Round 26, claim C2 (calibration). Fixed check set v2, K01 to K27, declared in
SCORECARD.md, "Round 26 - declaration, attempt 1".

Every input is read through Git at one revision (`git show`, `git ls-tree`,
`git archive`); the working tree is never read. K13 runs the census selftest
from a temporary directory populated by `git archive <REV>`.

K01 to K06 (round-26 refinement of the round-25 rule, routed defect 3). The
current axes table is the last table under the last SCORECARD heading that
starts `## Axes - `, and that heading must name the round as `round N`; a
heading without a round number exits 2. The ordinal reference holds only the
SCORECARD lines inside a section whose heading (any level, `#` to `######`)
carries `measured outcome` (case-insensitive), from any round; every other
line (declarations, refinements, move logs, corrections) is excluded, and the
axes table itself never qualifies. A section runs to the next heading of the
same or higher level, so a measured-outcome section keeps its subsections.
The reference line is the last match, by line order, of the round-25
refinement regex `\b<axis>\b[^0-9|→\n]{0,12}?(\d{1,2})\s*(?:→|->)\s*(\d{1,2})`
with both numbers from 0 to 10. An axis with no match in any
measured-outcome section is a mismatch with the reason `no dated move record`,
never a silent pass and never exit 2.

K24 to K27 (new in round 26, routed defect 7). For SHONEN boxes 1 to 4, every
`corpus/knowledge/*.md` path the box names exists at the revision, and none of
its first 20 lines carries the case-insensitive word `superseded`; a box
citing a missing or superseded note is a mismatch.

K07 to K23 are unchanged from the round-25 declaration and its refinements.

Usage:
    python3 tools/check-self-assessment.py --revision <REV> [--repo <path>]
    python3 tools/check-self-assessment.py --selftest [--repo <path>]

Prints one JSON object on stdout. Exit 0 when mismatches == 0, exit 1 when any
check mismatches, exit 2 when the revision or a required input cannot be
evaluated (unknown revision, missing file, missing axes table, axes heading
without a round number, missing axis row, missing capabilities table, missing
capability row, fewer than four SHONEN boxes).
"""

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

AXES = ("depth", "coverage", "operability", "freshness", "calibration", "adjacency")
CAPABILITIES = ("sources-registry", "host-census-gate", "root-metadata-observer", "boot-chain-audit")

# Path grammar shared by the capabilities rows (K16-K19) and the SHONEN boxes
# (K20-K23): a token is a path when it matches this charset, holds a "/" or a
# known source suffix, and does not start with "/" or "-".
PATH_CHARSET = re.compile(r"[A-Za-z0-9_.{},/-]+")
PATH_SUFFIXES = (".md", ".json", ".py", ".sh", ".txt")

EXIT_PASS = 0
EXIT_MISMATCH = 1
EXIT_CANNOT_EVALUATE = 2


class CannotEvaluate(Exception):
    """Raised when the check set cannot be evaluated at the given revision."""

    def __init__(self, reason, detail=""):
        super().__init__(reason if not detail else "%s: %s" % (reason, detail))
        self.reason = reason
        self.detail = detail


# --------------------------------------------------------------------------
# Git access (cleaned environment, no worktree attributes, no replace refs)
# --------------------------------------------------------------------------

def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["LC_ALL"] = "C"
    return env


def git(repo, *args, binary=False):
    cmd = ["git", "-C", repo, "--no-replace-objects",
           "-c", "core.attributesFile=/dev/null",
           "-c", "core.excludesFile=/dev/null",
           *args]
    return subprocess.run(cmd, capture_output=True, env=git_env(), text=not binary)


def git_ok(repo, *args):
    proc = git(repo, *args)
    if proc.returncode != 0:
        raise CannotEvaluate("git failed", "git %s: %s" % (" ".join(args), (proc.stderr or "").strip()))
    return proc.stdout


def resolve_rev(repo, rev):
    proc = git(repo, "rev-parse", "--verify", "%s^{commit}" % rev)
    if proc.returncode != 0:
        raise CannotEvaluate("unknown revision", rev)
    return proc.stdout.strip()


def show_blob(repo, rev, path):
    """The blob at REV:path, read through Git only."""
    proc = git(repo, "show", "%s:%s" % (rev, path))
    if proc.returncode != 0:
        raise CannotEvaluate("missing file", path)
    return proc.stdout


def list_paths(repo, rev):
    """Every path at REV: blobs and trees."""
    out = git_ok(repo, "ls-tree", "-r", "-t", "--name-only", rev)
    paths = set()
    for line in out.splitlines():
        line = line.strip()
        if line:
            paths.add(line)
            paths.add(line.rstrip("/"))
    return paths


def list_files(repo, rev, directory):
    """Blob paths under a directory at REV (recursive), relative names."""
    out = git_ok(repo, "ls-tree", "-r", "--name-only", rev, directory)
    names = []
    for line in out.splitlines():
        line = line.strip()
        if line:
            names.append(line)
    return names


def list_dir_entries(repo, rev, directory):
    """Direct children of a directory at REV (non-recursive), blob paths."""
    out = git_ok(repo, "ls-tree", "--name-only", rev, directory)
    names = []
    for line in out.splitlines():
        line = line.strip()
        if line:
            names.append(line)
    return names


def census_case_count(repo, rev):
    """Run `bash tools/tsukuroi-census.sh --selftest` on `git archive REV`."""
    archive = git(repo, "archive", "--format=tar", rev, binary=True)
    if archive.returncode != 0:
        raise CannotEvaluate("git archive failed", rev)
    work = tempfile.mkdtemp(prefix="self-assessment-census-")
    try:
        with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tar:
            tar.extractall(work, filter="data")
        script = os.path.join(work, "tools", "tsukuroi-census.sh")
        if not os.path.isfile(script):
            raise CannotEvaluate("missing file", "tools/tsukuroi-census.sh")
        proc = subprocess.run(["bash", "tools/tsukuroi-census.sh", "--selftest"],
                              cwd=work, capture_output=True, text=True, env=git_env(), timeout=900)
        output = (proc.stdout or "") + (proc.stderr or "")
        match = re.search(r"\((\d+) cases", output)
        if not match:
            raise CannotEvaluate("census selftest produced no case count", "exit %d" % proc.returncode)
        last = output.strip().splitlines()[-1] if output.strip() else ""
        return int(match.group(1)), last
    finally:
        shutil.rmtree(work, ignore_errors=True)


# --------------------------------------------------------------------------
# Markdown helpers
# --------------------------------------------------------------------------

def split_cells(line):
    """Split a table row on pipes that are not inside backtick code spans."""
    cells = []
    current = []
    in_code = False
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
    return [cell.strip() for cell in cells]


def table_blocks(lines, start, end):
    """Consecutive pipe-table blocks inside lines[start:end], as (lo, hi, rows)."""
    blocks = []
    index = start
    while index < end:
        if lines[index].lstrip().startswith("|"):
            lo = index
            while index < end and lines[index].lstrip().startswith("|"):
                index += 1
            rows = [split_cells(row) for row in lines[lo:index]]
            blocks.append((lo, index, rows))
        else:
            index += 1
    return blocks


def find_section(lines, heading_pattern):
    """(start, end) line range of the last section whose heading matches."""
    found = None
    for index, line in enumerate(lines):
        if heading_pattern.match(line):
            found = index
    if found is None:
        return None
    end = len(lines)
    for index in range(found + 1, len(lines)):
        if re.match(r"^##\s", lines[index]):
            end = index
            break
    return found, end


def pick_table(blocks, header_key):
    """Last table whose header names header_key; else the last table."""
    for lo, hi, rows in reversed(blocks):
        if rows and rows[0] and rows[0][0].strip().lower() == header_key.lower():
            return lo, hi, rows
    if blocks:
        lo, hi, rows = blocks[-1]
        return lo, hi, rows
    return None


def path_candidates(text):
    """Tokens of a piece of text that match the declared path grammar."""
    found = []
    for raw in PATH_CHARSET.findall(text or ""):
        token = raw.rstrip(".,;:)")
        if not token or token.startswith("/") or token.startswith("-"):
            continue
        if not re.fullmatch(r"[A-Za-z0-9_.{},/-]+", token):
            continue
        if "/" in token or token.endswith(PATH_SUFFIXES):
            found.append(token)
    return found


def is_path_like(token, paths_at_rev):
    """True when a grammar-matching token names a repository path.

    The declared path grammar is exact: a token is a path when it matches
    `[A-Za-z0-9_.{},/-]+`, contains "/" or ends in .md/.json/.py/.sh/.txt,
    and does not start with "/" or "-", after stripping a trailing
    `.,;:)`; one `{a,b,c}` group is expanded. No further shape test is
    applied, so a token that holds a slash but names nothing in the
    repository is still a path and is reported as absent.
    """
    return True


def expand_braces(token):
    """Expand one `{a,b,c}` group into its concrete paths."""
    match = re.search(r"\{([^{}]*)\}", token)
    if not match:
        return [token]
    parts = [part.strip() for part in match.group(1).split(",")]
    if len(parts) < 2 or not all(parts):
        return [token]
    return [token[:match.start()] + part + token[match.end():] for part in parts]


def resolve_paths(tokens, paths_at_rev):
    """Repository paths named by an ordered token list, brace groups expanded.

    The declared path grammar is applied exactly. A token is named as a path
    when it matches the grammar, and it is reported as absent when nothing at
    the revision carries that name; no resolution against a preceding
    directory is attempted.
    """
    paths = []
    for token in tokens:
        for candidate in path_candidates(token):
            for expanded in expand_braces(candidate):
                if expanded in paths:
                    continue
                paths.append(expanded)
    return paths


def all_paths(text, paths_at_rev):
    """Repository paths named by a piece of text, brace groups expanded."""
    return resolve_paths([text], paths_at_rev)


def backtick_spans(text):
    return re.findall(r"`([^`]*)`", text or "")


def header_index(header, *keywords, default=None):
    """Index of the first header cell matching any keyword, else default."""
    for index, cell in enumerate(header):
        lowered = cell.lower()
        if any(keyword in lowered for keyword in keywords):
            return index
    return default


def number_after(text, pattern, group=1):
    match = re.search(pattern, text or "")
    if not match:
        return None
    return int(match.group(group))


# --------------------------------------------------------------------------
# Round sections (K01 to K06) and supersession markers (K24 to K27)
# --------------------------------------------------------------------------

HEADING_RE = re.compile(r"^[ \t]{0,3}(#{1,6})[ \t]+(.*)$")
ROUND_IN_TEXT_RE = re.compile(r"round[^0-9A-Za-z]{0,3}(\d+)", re.I)
SUPERSEDED_RE = re.compile(r"\bsuperseded\b", re.I)
MEASURED_OUTCOME = "measured outcome"


def heading_sections(lines):
    """Every heading in lines, as (index, level, text, end).

    `end` is the exclusive line bound of the heading's section: a section
    runs from its heading to the next heading of the same or higher level (a
    level-1 `#` heading outranks a level-3 `###` heading), or to the end of
    the file.
    """
    headings = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            headings.append([index, len(match.group(1)), match.group(2), len(lines)])
    for position, heading in enumerate(headings):
        for later in headings[position + 1:]:
            if later[1] <= heading[1]:
                heading[3] = later[0]
                break
    return headings


ROUND_HEADING_RE = re.compile(r"^Round ?(\d+)\b", re.I)


def reference_lines(lines, declaring_round):
    """Line indices that may serve as the ordinal reference.

    Only lines inside a section whose heading (any level) starts with
    `Round N` (anchored at the start of the heading text, `Round16` and
    `Round 16` both read) and carries `measured outcome` (case-insensitive)
    qualify, and only when N is earlier than the declaring round: a round's
    own outcome record is the next round's reference, never its own
    (QUALITY 65, round-26 routed defect 2; added in round 27).  A
    declaration, a refinement, a move log or a correction is never a dated
    move record.  A section runs to the next heading of the same or higher
    level, so a measured-outcome section keeps its subsections.
    """
    candidates, excluded = set(), set()
    for heading in heading_sections(lines):
        text = heading[2].strip()
        match = ROUND_HEADING_RE.match(text)
        if match is None:
            continue
        if int(match.group(1)) >= declaring_round:
            # A section of the declaring round (or a later one) never
            # qualifies, even when nested inside an earlier outcome section.
            excluded.update(range(heading[0], heading[3]))
            continue
        if MEASURED_OUTCOME in text.lower():
            candidates.update(range(heading[0], heading[3]))
    return candidates - excluded


def superseded_line(text):
    """1-based line number of the first `superseded` word in the first 20 lines."""
    for index, line in enumerate((text or "").split("\n")[:20], start=1):
        if SUPERSEDED_RE.search(line):
            return index
    return None


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------

def check(checks, cid, subject, stated, observed, status, reason, **extra):
    record = {"id": cid, "subject": subject, "stated": stated, "observed": observed,
              "status": status, "reason": reason}
    record.update(extra)
    checks.append(record)
    return record


def evaluate(repo, rev):
    """Run K01 to K27 at rev. Returns (result dict, exit code)."""
    checks = []
    rev = resolve_rev(repo, rev)

    scorecard = show_blob(repo, rev, "SCORECARD.md")
    shonen = show_blob(repo, rev, "SHONEN.md")
    province = show_blob(repo, rev, "PROVINCE.md")
    skill_blob = show_blob(repo, rev, "SKILL.md")
    readme_blob = show_blob(repo, rev, "corpus/README.md")
    census_script = show_blob(repo, rev, "tools/tsukuroi-census.sh")

    score_lines = scorecard.split("\n")
    shonen_lines = shonen.split("\n")
    province_lines = province.split("\n")
    paths_at_rev = list_paths(repo, rev)

    # ---- axes table ------------------------------------------------------
    section = find_section(score_lines, re.compile(r"^##\s+Axes\s+[—-]\s"))
    if section is None:
        raise CannotEvaluate("no axes table", "no SCORECARD heading starting '## Axes - '")
    axes_heading = score_lines[section[0]]
    round_match = ROUND_IN_TEXT_RE.search(axes_heading)
    if round_match is None:
        raise CannotEvaluate("no round number in the axes heading",
                             "heading %r must name the round as 'round N'" % axes_heading)
    declaring_round = int(round_match.group(1))
    reference = reference_lines(score_lines, declaring_round)
    axes_blocks = table_blocks(score_lines, section[0] + 1, section[1])
    axes_table = pick_table(axes_blocks, "Axis")
    if axes_table is None:
        raise CannotEvaluate("no axes table", "no table under the last '## Axes - ' heading")
    axes_lo, axes_hi, axes_rows = axes_table
    axes_header = axes_rows[0] if axes_rows else []
    score_col = header_index(axes_header, "score", default=1)
    evidence_col = header_index(axes_header, "evidence", "pointer", default=2)
    axes_line_no = {row[0].strip().strip("`").strip().lower(): (index + 1, row)
                    for index, row in enumerate(axes_rows[1:], axes_lo + 1) if row}
    for axis in AXES:
        if axis not in axes_line_no:
            raise CannotEvaluate("missing axis row", axis)

    # ---- capabilities table ---------------------------------------------
    section = find_section(score_lines, re.compile(r"^##\s+Capabilities\b"))
    if section is None:
        raise CannotEvaluate("no capabilities table", "no SCORECARD heading starting '## Capabilities'")
    cap_blocks = table_blocks(score_lines, section[0] + 1, section[1])
    cap_table = pick_table(cap_blocks, "Capability")
    if cap_table is None:
        raise CannotEvaluate("no capabilities table", "no table under the last '## Capabilities' heading")
    cap_lo, cap_hi, cap_rows = cap_table
    cap_line_no = {row[0].strip().strip("`").strip().lower(): (index + 1, row)
                   for index, row in enumerate(cap_rows[1:], cap_lo + 1) if row}
    for capability in CAPABILITIES:
        if capability not in cap_line_no:
            raise CannotEvaluate("missing capability row", capability)

    # ---- SHONEN boxes ----------------------------------------------------
    boxes = []
    index = 0
    while index < len(shonen_lines):
        if re.match(r"^- \[", shonen_lines[index]):
            lo = index
            index += 1
            while index < len(shonen_lines) and not re.match(r"^- \[", shonen_lines[index]):
                index += 1
            boxes.append((lo, index))
        else:
            index += 1
    if len(boxes) < 4:
        raise CannotEvaluate("fewer than four SHONEN boxes", "%d found" % len(boxes))

    # ---- K01 to K06: axes score vs last recorded ordinal transition -------
    # The ordinal reference holds only the lines inside a section whose
    # heading carries `measured outcome`: a declaration, a refinement, a move
    # log or a correction is never a dated move record.
    for number, axis in enumerate(AXES, start=1):
        cid = "K%02d" % number
        line_no, row = axes_line_no[axis]
        score_cell = row[score_col] if len(row) > score_col else ""
        stated = number_after(score_cell, r"(\d+)")
        pattern = (r"\b" + re.escape(axis) + r"(?![A-Za-z])[^0-9|→\n]{0,12}?"
                   r"(\d{1,2})\s*(?:→|->)\s*(\d{1,2})")
        observed = None
        observed_line = None
        for index, line in enumerate(score_lines):
            if axes_lo <= index < axes_hi:
                continue
            if index not in reference:
                continue
            for match in re.finditer(pattern, line):
                before, after = int(match.group(1)), int(match.group(2))
                if not (0 <= before <= 10 and 0 <= after <= 10):
                    continue
                observed = after
                observed_line = index + 1
        subject = ("%s score equals the after-value of the last recorded %s ordinal transition"
                   % (axis, axis))
        if stated is None:
            check(checks, cid, subject, None, observed, "mismatch",
                  "axes table %s row states no numeric score" % axis,
                  stated_line=line_no, observed_line=observed_line)
        elif observed is None:
            check(checks, cid, subject, stated, None, "mismatch",
                  "no dated move record for %s: no %s ordinal transition in any measured-outcome section"
                  % (axis, axis),
                  stated_line=line_no, observed_line=None)
        else:
            status = "match" if stated == observed else "mismatch"
            reason = ("axes table %s score %d equals the after-value %d of the last recorded transition "
                      "(SCORECARD.md:%d)" % (axis, stated, observed, observed_line)
                      if status == "match" else
                      "axes table %s score %d differs from the after-value %d of the last recorded transition "
                      "(SCORECARD.md:%d)" % (axis, stated, observed, observed_line))
            check(checks, cid, subject, stated, observed, status, reason,
                  stated_line=line_no, observed_line=observed_line)

    depth_line, depth_row = axes_line_no["depth"]
    coverage_line, coverage_row = axes_line_no["coverage"]
    operability_line, operability_row = axes_line_no["operability"]
    adjacency_line, adjacency_row = axes_line_no["adjacency"]
    depth_cell = depth_row[evidence_col] if len(depth_row) > evidence_col else ""
    coverage_cell = coverage_row[evidence_col] if len(coverage_row) > evidence_col else ""
    operability_cell = operability_row[evidence_col] if len(operability_row) > evidence_col else ""
    adjacency_cell = adjacency_row[evidence_col] if len(adjacency_row) > evidence_col else ""
    depth_row_text = " | ".join(depth_row)
    coverage_row_text = " | ".join(coverage_row)
    operability_row_text = " | ".join(operability_row)
    adjacency_row_text = " | ".join(adjacency_row)

    def stated_in(cell, row_text, pattern, group=1):
        """First number for a pattern in the evidence cell, else in the whole row."""
        value = number_after(cell, pattern, group)
        if value is None:
            value = number_after(row_text, pattern, group)
        return value

    def stated_case_count(cell, row_text):
        """The case count a row states, in any of the lane's counting styles.

        `PASS (N cases, ...)`, `N cases`, `N-case` and `PASS N/N` state the
        same fact; the first form present wins.
        """
        for pattern in (r"PASS \((\d+)\s+cases", r"(\d+)\s+cases\b",
                        r"(\d+)-case\b", r"PASS (\d+)/"):
            value = stated_in(cell, row_text, pattern)
            if value is not None:
                return value
        return None

    # ---- K07: depth row "N notes" vs corpus/knowledge/*.md ----------------
    stated = stated_in(depth_cell, depth_row_text, r"(\d+)\s+notes\b")
    observed = len([p for p in list_dir_entries(repo, rev, "corpus/knowledge/") if p.endswith(".md")])
    check(checks, "K07", "depth row note count equals the corpus/knowledge/*.md count at the revision",
          stated, observed, "match" if stated == observed else "mismatch",
          "depth row states %s notes; corpus/knowledge holds %d .md files" % (stated, observed),
          stated_line=depth_line)

    # ---- K08: depth row "`SKILL.md` N `wc -l`" vs SKILL.md line count ----
    observed = skill_blob.count("\n")
    stated = stated_in(depth_cell, depth_row_text, r"`SKILL\.md`\s+(\d+)\s+`wc -l`")
    if stated is None:
        stated = stated_in(depth_cell, depth_row_text, r"SKILL\.md`?\s+(\d+)")
    check(checks, "K08", "depth row SKILL.md line count equals the line count of SKILL.md",
          stated, observed, "match" if stated == observed else "mismatch",
          "depth row states %s SKILL.md lines; SKILL.md holds %d newline characters" % (stated, observed),
          stated_line=depth_line)

    # ---- K09: depth row "N table lines" vs SKILL.md pipe lines ------------
    observed = sum(1 for line in skill_blob.split("\n") if line.startswith("|"))
    stated = stated_in(depth_cell, depth_row_text, r"(\d+)\s+table lines\b")
    check(checks, "K09", "depth row table-line count equals the pipe-prefixed line count of SKILL.md",
          stated, observed, "match" if stated == observed else "mismatch",
          "depth row states %s table lines; SKILL.md holds %d pipe-prefixed lines" % (stated, observed),
          stated_line=depth_line)

    # ---- K10: depth row corpus/lessons file count ------------------------
    tail = depth_cell.split("corpus/lessons/", 1)[1] if "corpus/lessons/" in depth_cell else ""
    stated = number_after(tail, r"(\d+)\s+files?\b")
    if stated is None:
        stated = stated_in(depth_cell, depth_row_text, r"corpus/lessons/`?[^|]{0,40}?(\d+)\s+files?\b")
    observed = len(list_files(repo, rev, "corpus/lessons/"))
    check(checks, "K10", "depth row corpus/lessons file count equals the file count under corpus/lessons/",
          stated, observed, "match" if stated == observed else "mismatch",
          "depth row states %s lesson files; corpus/lessons holds %d files" % (stated, observed),
          stated_line=depth_line)

    # ---- K11: coverage row corpus/README.md wc -l ------------------------
    observed = readme_blob.count("\n")
    tail = coverage_cell.split("corpus/README.md", 1)[1] if "corpus/README.md" in coverage_cell else ""
    stated = number_after(tail, r"(\d+)\s+`?wc -l`?")
    if stated is None:
        stated = stated_in(coverage_cell, coverage_row_text, r"corpus/README\.md`?[^|]{0,80}?(\d+)\s+`?wc -l`?")
    check(checks, "K11", "coverage row corpus/README.md line count equals the line count of corpus/README.md",
          stated, observed, "match" if stated == observed else "mismatch",
          "coverage row states %s corpus/README.md lines; the file holds %d newline characters"
          % (stated, observed), stated_line=coverage_line)

    # ---- K12: coverage row on PROVINCE Core/Frontier/Adjacent ------------
    if "Core/Frontier/Adjacent not landed" in coverage_row_text:
        stated = "absent"
    elif "Core, Frontier and Adjacent sections present" in coverage_row_text:
        stated = "present"
    else:
        stated = "unstated"
    has_core = any(line.startswith("## Core") for line in province_lines)
    has_frontier = any(line.startswith("## Frontier") for line in province_lines)
    has_adjacent = any(line.startswith("## Adjacent") for line in province_lines)
    observed = "present" if (has_core and has_frontier and has_adjacent) else "absent"
    status = "match" if stated == observed else "mismatch"
    check(checks, "K12", "coverage row statement about PROVINCE.md Core/Frontier/Adjacent matches the headings",
          stated, observed, status,
          "coverage row states the sections are %s; PROVINCE.md holds Core=%s Frontier=%s Adjacent=%s"
          % (stated, has_core, has_frontier, has_adjacent), stated_line=coverage_line)

    # ---- K13: operability row case count vs census selftest --------------
    observed, census_last = census_case_count(repo, rev)
    census_count = observed
    stated = stated_case_count(operability_cell, operability_row_text)
    check(checks, "K13", "operability row case count equals the census selftest case count at the revision",
          stated, observed, "match" if stated == observed else "mismatch",
          "operability row states %s cases; the census selftest at this revision prints %d cases (%s)"
          % (stated, observed, census_last), stated_line=operability_line)

    # ---- K14: operability row --identity mode ----------------------------
    if "`--identity` not landed" in operability_row_text:
        stated = "absent"
    elif "`--identity` landed" in operability_row_text:
        stated = "present"
    else:
        stated = "unstated"
    observed = "present" if re.search(r"^\s*--identity\)", census_script, re.M) else "absent"
    status = "match" if stated == observed else "mismatch"
    check(checks, "K14", "operability row statement about a --identity mode matches tools/tsukuroi-census.sh",
          stated, observed, status,
          "operability row states the mode is %s; the census script holds a --identity case arm: %s"
          % (stated, observed == "present"), stated_line=operability_line)

    # ---- K15: adjacency row formal overlap table -------------------------
    if "no formal overlap table" in adjacency_row_text:
        stated = "absent"
    elif "formal overlap table present" in adjacency_row_text:
        stated = "present"
    else:
        stated = "unstated"
    observed = "present" if any(line.startswith("| ID | Finding") for line in province_lines) else "absent"
    status = "match" if stated == observed else "mismatch"
    check(checks, "K15", "adjacency row statement about a formal overlap table matches PROVINCE.md",
          stated, observed, status,
          "adjacency row states the table is %s; PROVINCE.md holds a '| ID | Finding' table: %s"
          % (stated, observed == "present"), stated_line=adjacency_line)

    # ---- K16 to K19: capabilities rows name only existing paths -----------
    for number, capability in enumerate(CAPABILITIES, start=16):
        cid = "K%02d" % number
        line_no, row = cap_line_no[capability]
        cell_text = " ".join(row[1:]) if len(row) > 1 else ""
        tokens = []
        for span in backtick_spans(cell_text):
            tokens.extend(span.split())
        named = resolve_paths(tokens, paths_at_rev)
        existing = [p for p in named if p.rstrip("/") in paths_at_rev]
        missing = [p for p in named if p.rstrip("/") not in paths_at_rev]
        subject = "%s row names only repository paths that exist at the revision" % capability
        if not named:
            check(checks, cid, subject, named, existing, "mismatch",
                  "%s row names no repository path" % capability, stated_line=line_no)
            continue
        if capability == "host-census-gate":
            stated_count = stated_case_count(cell_text, cell_text)
            observed_count = census_count  # the census count measured for K13
            problems = []
            if missing:
                problems.append("names %d path(s) absent at the revision: %s"
                                % (len(missing), ", ".join(sorted(missing))))
            if stated_count != observed_count:
                problems.append("states %s cases; the census selftest at this revision prints %d cases"
                                % (stated_count, observed_count))
            if problems:
                check(checks, cid, subject, named, existing, "mismatch",
                      "host-census-gate row %s" % "; ".join(problems), stated_line=line_no)
                continue
            check(checks, cid, subject, named, existing, "match",
                  "host-census-gate row names %d existing path(s) and states %d cases, equal to the census selftest"
                  % (len(named), stated_count), stated_line=line_no)
            continue
        if missing:
            check(checks, cid, subject, named, existing, "mismatch",
                  "%s row names %d path(s) absent at the revision: %s"
                  % (capability, len(missing), ", ".join(sorted(missing))), stated_line=line_no)
            continue
        check(checks, cid, subject, named, existing, "match",
              "%s row names %d path(s), all present at the revision" % (capability, len(named)),
              stated_line=line_no)

    # ---- K20 to K23: SHONEN boxes ----------------------------------------
    for number in range(4):
        cid = "K%02d" % (20 + number)
        lo, hi = boxes[number]
        text = "\n".join(shonen_lines[lo:hi])
        named = all_paths(text, paths_at_rev)
        existing = [p for p in named if p.rstrip("/") in paths_at_rev]
        missing = [p for p in named if p.rstrip("/") not in paths_at_rev]
        marked = bool(re.match(r"^- \[x\]", shonen_lines[lo]))
        verifier = re.search(r"non-author verifier:\s*([A-Za-z0-9][\w.\-]*)", text)
        subject = "SHONEN box %d names only repository paths that exist at the revision" % (number + 1)
        if not named:
            check(checks, cid, subject, named, existing, "mismatch",
                  "SHONEN box %d names no repository path" % (number + 1), stated_line=lo + 1)
            continue
        if missing:
            check(checks, cid, subject, named, existing, "mismatch",
                  "SHONEN box %d names %d path(s) absent at the revision: %s"
                  % (number + 1, len(missing), ", ".join(sorted(missing))), stated_line=lo + 1)
            continue
        if marked and not verifier:
            check(checks, cid, subject, named, existing, "mismatch",
                  "SHONEN box %d is marked [x] without a named non-author verifier" % (number + 1),
                  stated_line=lo + 1)
            continue
        check(checks, cid, subject, named, existing, "match",
              "SHONEN box %d names %d existing path(s)%s"
              % (number + 1, len(named),
                 " and names a non-author verifier" if marked else " and is not marked complete"),
              stated_line=lo + 1)

    # ---- K24 to K27: SHONEN boxes cite current knowledge notes ----------
    # A box may not cite a corpus/knowledge note that is absent at the
    # revision or that carries a supersession marker in its first 20 lines.
    for number in range(4):
        cid = "K%02d" % (24 + number)
        lo, hi = boxes[number]
        text = "\n".join(shonen_lines[lo:hi])
        named = all_paths(text, paths_at_rev)
        notes = [p for p in named if p.startswith("corpus/knowledge/") and p.endswith(".md")]
        subject = ("SHONEN box %d cites only corpus/knowledge notes that exist at the revision "
                   "and carry no supersession marker" % (number + 1))
        if not notes:
            check(checks, cid, subject, notes, notes, "match",
                  "SHONEN box %d names no corpus/knowledge/*.md note" % (number + 1),
                  stated_line=lo + 1)
            continue
        problems = []
        for note in notes:
            if note.rstrip("/") not in paths_at_rev:
                problems.append({"path": note, "line": None,
                                 "detail": "%s is absent at the revision" % note})
                continue
            marker = superseded_line(show_blob(repo, rev, note))
            if marker is not None:
                problems.append({"path": note, "line": marker,
                                 "detail": "%s carries a supersession marker at its line %d"
                                           % (note, marker)})
        if problems:
            detail = "; ".join(problem["detail"] for problem in problems)
            check(checks, cid, subject, notes, [], "mismatch",
                  "SHONEN box %d cites %d corpus/knowledge note(s), %d of them unusable: %s"
                  % (number + 1, len(notes), len(problems), detail),
                  stated_line=lo + 1, problems=problems)
            continue
        check(checks, cid, subject, notes, notes, "match",
              "SHONEN box %d cites %d corpus/knowledge note(s), all present at the revision and "
              "free of a supersession marker in their first 20 lines" % (number + 1, len(notes)),
              stated_line=lo + 1)

    mismatches = sum(1 for record in checks if record["status"] == "mismatch")
    result = {
        "revision": rev,
        "checked": len(checks),
        "mismatches": mismatches,
        "status": "PASS" if mismatches == 0 else "FAIL",
        "declaring_round": declaring_round,
        "axes_heading": axes_heading,
        "reference_lines": len(reference),
        "checks": checks,
    }
    return result, (EXIT_PASS if mismatches == 0 else EXIT_MISMATCH)


# --------------------------------------------------------------------------
# Hermetic selftest over temporary Git repositories
# --------------------------------------------------------------------------

FIXTURE_FILES = {
    "corpus/knowledge/one.md": "# one\n\nknowledge note one\n",
    "corpus/knowledge/two.md": "# two\n\nknowledge note two\n",
    "corpus/lessons/lesson-one.md": "# lesson one\n\nlesson body\n",
    "corpus/README.md": "# corpus readme\n\nrow one\nrow two\n",
    "corpus/SOURCES.md": "# sources\n\n| id | source |\n|---|---|\n",
    "PROVINCE.md": ("# province\n\n## Core\n\ncore body\n\n## Frontier\n\nfrontier body\n\n"
                    "## Adjacent\n\nadjacent body\n\n| ID | Finding / boundary trigger |\n|---|---|\n| X | y |\n"),
    "SKILL.md": "# skill\n\n| rule | action |\n|---|---|\n| one | do one |\n",
    "tools/boot-chain-audit.sh": "#!/usr/bin/env bash\necho boot chain audit\n",
    "tools/tsukuroi-census.sh": """#!/usr/bin/env bash
case "${1:-}" in
  --selftest)
    echo "TSUKUROI_CENSUS_SELFTEST: PASS (3 cases, 3 passed, 0 failed)"
    exit 0
    ;;
  --identity)
    echo "TSUKUROI_CENSUS_IDENTITY"
    exit 0
    ;;
esac
exit 1
""",
    "SHONEN.md": """# Promotion checklist

- [~] Box one
  Author-side evidence: corpus/knowledge/one.md.
- [~] Box two
  Author-side evidence: corpus/knowledge/two.md.
- [~] Box three
  Author-side evidence: corpus/README.md.
- [~] Box four
  Author-side evidence: corpus/SOURCES.md.
""",
}

FIXTURE_SCORECARD_TEMPLATE = """# Fixture scorecard

## Axes - fixture self-assessment (round 2)

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| depth | {depth} | {notes} notes (`ls corpus/knowledge/*.md`); `SKILL.md` {skill_lines} `wc -l` / {skill_tables} table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` {lessons} file | r1 |
| coverage | {coverage} | `corpus/README.md` rows stop at r1 ({readme_lines} `wc -l`); `PROVINCE.md` Core, Frontier and Adjacent sections present | r1 |
| operability | {operability} | `bash tools/tsukuroi-census.sh --selftest` -> rc=0 `PASS ({cases} cases, {cases} passed, 0 failed)`; Ceiling: D12 `--identity` landed | r1 |
| freshness | 9 | receipts | r1 |
| calibration | 9 | notes | r1 |
| adjacency | {adjacency} | Ceiling: formal overlap table present | r1 |

## Round 1 measured outcome

- depth 8 -> 8
- coverage 9 -> 9
- operability 9 -> 9
- freshness 9 -> 9
- calibration 9 -> 9
- adjacency 8 -> 8

## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates `corpus/SOURCES.md` | `corpus/SOURCES.md` | r1 |
| host-census-gate | Emits a verdict with a hermetic {cases}-case `--selftest` | `bash tools/tsukuroi-census.sh --selftest` -> PASS {cases}/{cases} rc=0 | r1 |
| root-metadata-observer | Observes root mode | `corpus/knowledge/one.md` | r1 |
| boot-chain-audit | Audits boot entries | `tools/boot-chain-audit.sh` | r1 |
"""

FIXTURE_SCORES = {"depth": 8, "coverage": 9, "operability": 9, "freshness": 9, "calibration": 9, "adjacency": 8}


def fixture_scorecard(overrides=None):
    """The fixture SCORECARD with every stated number computed from the fixture."""
    overrides = overrides or {}
    values = {
        "depth": FIXTURE_SCORES["depth"],
        "coverage": FIXTURE_SCORES["coverage"],
        "operability": FIXTURE_SCORES["operability"],
        "adjacency": FIXTURE_SCORES["adjacency"],
        "notes": len([p for p in FIXTURE_FILES if p.startswith("corpus/knowledge/") and p.endswith(".md")]),
        "skill_lines": FIXTURE_FILES["SKILL.md"].count("\n"),
        "skill_tables": sum(1 for line in FIXTURE_FILES["SKILL.md"].split("\n") if line.startswith("|")),
        "lessons": len([p for p in FIXTURE_FILES if p.startswith("corpus/lessons/")]),
        "readme_lines": FIXTURE_FILES["corpus/README.md"].count("\n"),
        "cases": 3,
    }
    values.update(overrides)
    return FIXTURE_SCORECARD_TEMPLATE.format(**values)


def fixture_files(case):
    files = dict(FIXTURE_FILES)
    scorecard = fixture_scorecard()
    shonen = FIXTURE_FILES["SHONEN.md"]
    expected = {"expected_exit": EXIT_PASS, "expected_mismatch_ids": [], "expected_error": ""}
    if case == "clean":
        pass
    elif case == "own-round-outcome-depth-10":
        # QUALITY 65: the round-26 depth-10 mutant. The declaring round (2)
        # states depth 10 in its table and records 8 -> 10 in its own
        # measured outcome; that record is the next round's reference, so
        # the reference stays the round-1 record (8) and K01 mismatches.
        scorecard = fixture_scorecard({"depth": 10}).replace(
            "## Capabilities\n",
            "### Round 2 measured outcome\n\n- depth 8 -> 10\n\n## Capabilities\n", 1)
        expected = {"expected_exit": EXIT_MISMATCH, "expected_mismatch_ids": ["K01"], "expected_error": ""}
    elif case == "outcome-heading-not-round-anchored":
        # A heading that names `measured outcome` but does not start with
        # `Round N` is not a dated move record.
        scorecard = scorecard.replace(
            "## Capabilities\n",
            "## Notes on the round 1 measured outcome\n\n- depth 8 -> 3\n\n## Capabilities\n", 1)
        expected = {"expected_exit": EXIT_PASS, "expected_mismatch_ids": [], "expected_error": ""}
    elif case == "stale-ordinal":
        scorecard = fixture_scorecard({"coverage": 8})
        expected = {"expected_exit": EXIT_MISMATCH, "expected_mismatch_ids": ["K02"], "expected_error": ""}
    elif case == "stale-count":
        scorecard = fixture_scorecard({"notes": 5})
        expected = {"expected_exit": EXIT_MISMATCH, "expected_mismatch_ids": ["K07"], "expected_error": ""}
    elif case == "unstated-fact":
        scorecard = scorecard.replace("; `PROVINCE.md` Core, Frontier and Adjacent sections present", "")
        expected = {"expected_exit": EXIT_MISMATCH, "expected_mismatch_ids": ["K12"], "expected_error": ""}
    elif case == "missing-capability-path":
        scorecard = scorecard.replace("| `corpus/SOURCES.md` | r1 |", "| `corpus/MISSING.md` | r1 |")
        expected = {"expected_exit": EXIT_MISMATCH, "expected_mismatch_ids": ["K16"], "expected_error": ""}
    elif case == "shonen-x-without-verifier":
        shonen = shonen.replace("- [~] Box one", "- [x] Box one")
        expected = {"expected_exit": EXIT_MISMATCH, "expected_mismatch_ids": ["K20"], "expected_error": ""}
    elif case == "missing-axes-table":
        scorecard = scorecard.replace("## Axes - fixture self-assessment (round 2)",
                                      "## Self assessment (no axes table)")
        expected = {"expected_exit": EXIT_CANNOT_EVALUATE, "expected_mismatch_ids": [],
                    "expected_error": "axes table"}
    elif case == "axes-heading-without-round":
        scorecard = scorecard.replace("## Axes - fixture self-assessment (round 2)",
                                      "## Axes - fixture self-assessment")
        expected = {"expected_exit": EXIT_CANNOT_EVALUATE, "expected_mismatch_ids": [],
                    "expected_error": "round number"}
    elif case == "declaring-round-declaration-line":
        # Plan prose in a declaration section is not a dated move record: the
        # depth ordinal still resolves to the measured outcome (8 -> 8).
        scorecard = scorecard.replace(
            "## Capabilities\n",
            "## Round 1 - declaration, attempt 1\n\n- depth 8 -> 3\n\n## Capabilities\n", 1)
        expected = {"expected_exit": EXIT_PASS, "expected_mismatch_ids": [], "expected_error": ""}
    elif case == "declaring-round-measured-outcome-line":
        # The same line under a `measured outcome` heading does record the
        # round's move, so the depth ordinal resolves to 3 and K01 mismatches.
        scorecard = scorecard.replace(
            "## Capabilities\n",
            "## Round 1 - declaration, attempt 1\n\n- depth 8 -> 3\n\n"
            "### Round 1 measured outcome\n\n- depth 8 -> 3\n\n## Capabilities\n", 1)
        expected = {"expected_exit": EXIT_MISMATCH, "expected_mismatch_ids": ["K01"], "expected_error": ""}
    elif case == "axis-without-move-record":
        # No measured-outcome section records a freshness move, so K04 is a
        # mismatch with the reason `no dated move record`.
        scorecard = scorecard.replace("- freshness 9 -> 9\n", "")
        expected = {"expected_exit": EXIT_MISMATCH, "expected_mismatch_ids": ["K04"],
                    "expected_error": "no dated move record"}
    elif case == "shonen-superseded-note":
        files["corpus/knowledge/one.md"] = ("# one\n\n> **Superseded** after an outside rejection.\n\n"
                                            "knowledge note one\n")
        expected = {"expected_exit": EXIT_MISMATCH, "expected_mismatch_ids": ["K24"], "expected_error": ""}
    elif case == "shonen-missing-note":
        shonen = shonen.replace("corpus/knowledge/one.md", "corpus/knowledge/missing.md")
        expected = {"expected_exit": EXIT_MISMATCH, "expected_mismatch_ids": ["K20", "K24"],
                    "expected_error": ""}
    else:
        raise ValueError("unknown fixture case: %s" % case)
    files["SCORECARD.md"] = scorecard
    files["SHONEN.md"] = shonen
    return files, expected


def build_fixture(case, root):
    files, expected = fixture_files(case)
    files["expected-findings.json"] = json.dumps(expected, indent=1, sort_keys=True) + "\n"
    repo = os.path.join(root, case)
    os.makedirs(repo)
    subprocess.run(["git", "init", "-q", repo], check=True)
    env = git_env()
    for path, text in files.items():
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as handle:
            handle.write(text)
    subprocess.run(["git", "-C", repo, "add", "-A"], check=True, env=env)
    subprocess.run(["git", "-C", repo, "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
                    "commit", "-q", "-m", "fixture: %s" % case], check=True, env=env)
    return repo


def run_selftest():
    root = tempfile.mkdtemp(prefix="self-assessment-selftest-")
    cases = ["clean", "stale-ordinal", "stale-count", "unstated-fact",
             "missing-capability-path", "shonen-x-without-verifier", "missing-axes-table",
             "axes-heading-without-round", "declaring-round-declaration-line",
             "declaring-round-measured-outcome-line", "axis-without-move-record",
             "shonen-superseded-note", "shonen-missing-note", "own-round-outcome-depth-10",
             "outcome-heading-not-round-anchored"]
    results = []
    failures = []
    try:
        for case in cases:
            repo = build_fixture(case, root)
            expectation = json.loads(show_blob(repo, "HEAD", "expected-findings.json"))
            entry = {"case": case, "expected_exit": expectation["expected_exit"],
                     "expected_mismatch_ids": expectation["expected_mismatch_ids"]}
            try:
                result, code = evaluate(repo, "HEAD")
                entry["actual_exit"] = code
                entry["actual_mismatch_ids"] = [r["id"] for r in result["checks"] if r["status"] == "mismatch"]
                entry["reasons"] = [r["reason"] for r in result["checks"] if r["status"] == "mismatch"]
                entry["error"] = ""
            except CannotEvaluate as exc:
                entry["actual_exit"] = EXIT_CANNOT_EVALUATE
                entry["actual_mismatch_ids"] = []
                entry["reasons"] = []
                entry["error"] = "%s: %s" % (exc.reason, exc.detail)
            observed_text = "%s %s" % (entry["error"], " ".join(entry["reasons"]))
            ok = (entry["actual_exit"] == entry["expected_exit"]
                  and entry["actual_mismatch_ids"] == entry["expected_mismatch_ids"]
                  and (not expectation["expected_error"]
                       or expectation["expected_error"] in observed_text))
            entry["result"] = "PASS" if ok else "FAIL"
            if not ok:
                failures.append(entry)
            results.append(entry)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    return {"selftest": "PASS" if not failures else "FAIL",
            "cases": len(results),
            "failures": failures,
            "results": results}


# --------------------------------------------------------------------------

def default_repo():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Count self-assessment mismatches at one revision.")
    parser.add_argument("--revision", help="revision to measure (read through Git)")
    parser.add_argument("--repo", default=None,
                        help="repository to read (default: the repository holding this script)")
    parser.add_argument("--selftest", action="store_true", help="run the hermetic fixture selftest")
    args = parser.parse_args(argv)

    repo = os.path.abspath(args.repo) if args.repo else default_repo()
    if not os.path.exists(os.path.join(repo, ".git")):
        print(json.dumps({"status": "CANNOT_EVALUATE", "error": "not a git repository",
                          "repo": repo, "checked": 0, "mismatches": None, "checks": []}, indent=1))
        return EXIT_CANNOT_EVALUATE

    if args.selftest:
        payload = run_selftest()
        print(json.dumps(payload, indent=1))
        return EXIT_PASS if payload["selftest"] == "PASS" else EXIT_MISMATCH

    if not args.revision:
        print(json.dumps({"status": "CANNOT_EVALUATE", "error": "no revision given",
                          "checked": 0, "mismatches": None, "checks": []}, indent=1))
        return EXIT_CANNOT_EVALUATE

    try:
        result, code = evaluate(repo, args.revision)
    except CannotEvaluate as exc:
        print(json.dumps({"status": "CANNOT_EVALUATE", "error": exc.reason, "detail": exc.detail,
                          "requested_revision": args.revision, "repo": repo, "checked": 0,
                          "mismatches": None, "checks": []}, indent=1))
        return EXIT_CANNOT_EVALUATE

    result["repo"] = repo
    result["requested_revision"] = args.revision
    print(json.dumps(result, indent=1))
    return code


if __name__ == "__main__":
    sys.exit(main())
