#!/usr/bin/env python3
"""Standalone source-rows schema validator for corpus/SOURCES.md (round-37 w1 Build10Source42).

Design item 10/12: "source rows schema validator".
Independent, runnable re-implementation of the frozen fleet census contract
(/home/vgpnk/Projects/shokunin/scripts/sources-census.sh, E01-E12/W01-W04) plus one
NEW structural check that the frozen line-based parser does not enforce:

  E13  row-shaped source inside the `## Registry` section but OUTSIDE the single
       contiguous Markdown table block (header + separator + unbroken body rows).

The frozen census scans line-by-line (`gawk -F'|'`) and counts any `|`-prefixed
line in the Registry section as a row, so it silently accepts rows that a
CommonMark/GFM block parser never sees in the table (a blank line after the body
ends the table block; such stray rows render as literal text). E13 makes that
structural drift observable.

Usage:
  python3 check-source-rows-schema.py --file PATH [--root DIR] [--today YYYY-MM-DD]

Exit: 0 clean (warnings allowed) · 1 schema errors · 2 usage/env error.
Output: TSV on stdout — label<TAB>code<TAB>value… (census-compatible shape).
Codes (contract E01-E12/W01-W04 + new E13):
  E00 no registry header/separator found under `## Registry`
  E01 malformed row (cell count != 11)
  E02 id not S[0-9]{3,}
  E03 duplicate id
  E04 duplicate URL+scope (no supersedes exemption)
  E05 kind enum violation   E06 tier enum violation   E07 status enum violation
  E08 opened not a past/present ISO date   E09 invalid recheck (ISO, NNd, symbolic)
  E10 community at tier A   E11 used-by path missing on disk (mined)
  E12 row-shaped source outside the ## Registry section (mirrors census)
  E13 row-shaped source outside the contiguous table block (NEW)
  W01 tier-C mined with non-— used-by   W02 rejected row, thin teaches
  W03 mined row with used-by = —        W04 same URL across scopes
"""

import argparse
import datetime
import os
import re
import sys

URL_RE = re.compile(r"https?://[^\s|]+")
ID_RE = re.compile(r"^S[0-9]{3,}$")
KIND_OK = {"spec", "docs", "paper", "code", "tool", "dataset",
           "talk", "book", "community", "own-work"}
STATUS_OK = {"queued", "mined", "rejected"}
HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(\S.*)$")
ROWLINE = re.compile(r"^ {0,3}\|")
SEPCELL = re.compile(r"^:?-+:?$")


def trim(s):
    return s.strip()


def is_separator(cells):
    return all(SEPCELL.match(trim(c)) for c in cells)


def iso_epoch(s):
    try:
        t = datetime.date.fromisoformat(s)
        return t.toordinal()
    except ValueError:
        return None


def symbolic(s):
    return bool(re.fullmatch(r"[A-Za-z][A-Za-z0-9 _-]*", s))


def url_of(s):
    m = URL_RE.search(s)
    if not m:
        return ""
    u = m.group(0)
    u = re.sub(r"#[^ ]*$", "", u)
    u = re.sub(r"/$", "", u)
    u = re.sub(r"^[A-Za-z]+://", "", u)
    i = u.find("/")
    if i >= 0:
        u = u[:i].lower() + u[i:]
    else:
        u = u.lower()
    return u


def split_row(line):
    """Split a markdown table line into logical cells (0-3 leading spaces allowed)."""
    line = re.sub(r"^ {0,3}", "", line)
    cells = [trim(c) for c in line.split("|")[1:-1]]
    return cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--today", default=datetime.date.today().isoformat())
    args = ap.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError as exc:
        print(f"usage: cannot open {args.file}: {exc}", file=sys.stderr)
        return 2

    today_ord = iso_epoch(args.today)
    if today_ord is None:
        print(f"usage: bad --today {args.today}", file=sys.stderr)
        return 2

    label = args.file
    out = []  # (code, id, message)
    errors = 0

    # ---- pass 1: section tracking; keep every Registry-section line ----
    in_registry = False
    section_lines = []      # (lineno, line, is_row) inside ## Registry
    outside_rows = []       # (lineno, line) row-shaped outside ## Registry
    for n, line in enumerate(lines, start=1):
        m = HEADING.match(line)
        if m:
            is_h1 = m.group(1) == "#"
            if is_h1:
                in_registry = False
            else:
                in_registry = (trim(m.group(2)) == "Registry")
            continue
        is_row = bool(ROWLINE.match(line))
        if in_registry:
            section_lines.append((n, line, is_row))
        elif is_row:
            outside_rows.append((n, line))

    # E12 mirror
    for n, line in outside_rows:
        cells = split_row(line)
        if cells and ID_RE.match(cells[0]):
            out.append(("E12", cells[0], f"row outside Registry section (line {n})"))
            errors += 1

    # ---- pass 2: locate header + separator and the contiguous table block ----
    rows_in_section = [(n, line) for n, line, is_row in section_lines if is_row]
    header_i = None
    for i, (n, line) in enumerate(rows_in_section):
        cells = split_row(line)
        if cells and cells[0] == "id" and i + 1 < len(rows_in_section):
            nxt = rows_in_section[i + 1][1]
            if is_separator(split_row(nxt)):
                header_i = i
                break
    if header_i is None:
        out.append(("E00", "-", "no registry header+separator under ## Registry"))
        errors += 1
        block_nums = set()
    else:
        hdr_lineno = rows_in_section[header_i][0]
        sep_lineno = rows_in_section[header_i + 1][0]
        # contiguous run of row-shaped lines immediately following the separator:
        # walk the raw section line list from sep_lineno+1 and stop at the first
        # non-row-shaped line (blank, prose, heading, indented code).
        block_nums = {hdr_lineno, sep_lineno}
        started = False
        for n, line, is_row in section_lines:
            if n <= sep_lineno:
                continue
            if is_row:
                block_nums.add(n)
                started = True
            elif started:
                break
        # E13: any section row outside the single contiguous block
        for n, line, is_row in section_lines:
            if not is_row or n in block_nums:
                continue
            cells = split_row(line)
            if cells and ID_RE.match(cells[0]):
                out.append(("E13", cells[0],
                            f"row outside contiguous table block (line {n})"))
                errors += 1

    # ---- pass 3: per-row schema validation on contiguous block rows ----
    seen = set()
    url_seen = {}
    url_scopes = set()
    url_scope_nonrejected = set()
    rows = 0
    for n, line, is_row in section_lines:
        if not is_row or n not in block_nums:
            continue
        cells = split_row(line)
        if cells and cells[0] == "id":
            continue  # header
        if all(SEPCELL.match(c) for c in cells):
            continue  # separator
        rows += 1
        if len(cells) != 11:
            out.append(("E01", cells[0] if cells else "-",
                        f"fields={len(cells)} (line {n})"))
            errors += 1
            continue
        sid, source, kind, tier, scope, anchor, teaches, status, opened, recheck, usedby = cells
        if not ID_RE.match(sid):
            out.append(("E02", sid, f"id malformed (line {n})"))
            errors += 1
        elif sid in seen:
            out.append(("E03", sid, "duplicate id"))
            errors += 1
        seen.add(sid)
        u = url_of(source)
        sk = (u, scope)
        if u and u in url_seen and sk not in url_scopes:
            out.append(("W04", sid, f"duplicate url {u} across scopes"))
        if u and sk in url_scopes and status != "rejected" and \
                sk in url_scope_nonrejected and \
                not re.search(r"supersedes S[0-9]{3}", teaches):
            out.append(("E04", sid, f"duplicate url {u} within scope {scope}"))
            errors += 1
        if u:
            url_seen[u] = True
            url_scopes.add(sk)
            if status != "rejected":
                url_scope_nonrejected.add(sk)
        if kind not in KIND_OK:
            out.append(("E05", sid, f"kind={kind}"))
            errors += 1
        if tier not in ("A", "B", "C"):
            out.append(("E06", sid, f"tier={tier}"))
            errors += 1
        if status not in STATUS_OK:
            out.append(("E07", sid, f"status={status}"))
            errors += 1
        op = iso_epoch(opened)
        if op is None or op > today_ord:
            out.append(("E08", sid, f"opened={opened}"))
            errors += 1
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", recheck):
            if iso_epoch(recheck) is None:
                out.append(("E09", sid, f"recheck={recheck}"))
                errors += 1
        elif not re.fullmatch(r"\d+d", recheck) and not symbolic(recheck):
            out.append(("E09", sid, f"recheck={recheck}"))
            errors += 1
        if tier == "A" and kind == "community":
            out.append(("E10", sid, "community-at-A"))
            errors += 1
        if status == "mined" and usedby != "—":
            for p in usedby.split(","):
                p = p.strip()
                if p and not os.path.exists(os.path.join(args.root, p)):
                    out.append(("E11", sid, f"used-by missing {p}"))
                    errors += 1
        if tier == "C" and status == "mined" and usedby != "—":
            out.append(("W01", sid, f"tierC mined used-by={usedby}"))
        if status == "rejected" and len(teaches) < 8:
            out.append(("W02", sid, "thin reject reason"))
        if status == "mined" and usedby == "—":
            out.append(("W03", sid, "mined but unused"))

    # ---- informational census line ----
    out.append(("C", "rows", str(rows)))
    out.append(("C", "section-row-lines", str(len(rows_in_section))))
    out.append(("C", "contiguous-block-rows", str(rows)))

    for code, sid, msg in out:
        print(f"{label}\t{code}\t{sid} {msg}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
