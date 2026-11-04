#!/usr/bin/env python3
"""E1Mirror independent MD-row reader for the round-72 C1 note.

Clean-room: parses the note, the registry and the snapshot map with its own
quote-aware cell splitter; it does not import or call tools/count-md-rows-r72.py.

Checks per row (the seat's specified set):
  - the row parses into the grammar cells (| MDn | stmt | source= | snapshot= | digest= | quote= |)
  - quote is located verbatim in the named snapshot (whitespace-normalized)
  - digest equals sha256 of the named snapshot file
  - source id is present in corpus/SOURCES.md
  - that registry row's source cell contains the map URL for the snapshot
  - that registry row's anchor cell contains the snapshot basename
Global: row count, id contiguity from 1.

Usage: reader.py <fixture-root>
Prints per-row lines, then READER rows=N ok=N red=N, exit 0 when rows==6 and ok==6
and ids are contiguous, else 1.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

NOTE_REL = "corpus/knowledge/modprobe-config-plane-r72.md"
REG_REL = "corpus/SOURCES.md"
SNAPDIR_REL = ".ufo/waves/round-72/before/src"
MAP_REL = SNAPDIR_REL + "/SOURCES.json"

ID_CELL = re.compile(r"^MD([0-9]+)$")
REG_ID = re.compile(r"^S[0-9]{3,}$")
URL_RE = re.compile(r"https?://\S+")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
QUOTE_CELL = re.compile(r'^quote="(.*)"$')


def split_cells(line):
    """Split one markdown table line on pipes that are outside double quotes."""
    cells, cur, in_quote = [], [], False
    for ch in line:
        if ch == '"':
            in_quote = not in_quote
            cur.append(ch)
        elif ch == "|" and not in_quote:
            cells.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    cells.append("".join(cur))
    return cells


def norm(text):
    return " ".join(text.split())


def parse_row(line):
    """Return a row dict, or None when the line is not an MD row of the grammar."""
    cells = split_cells(line)
    if len(cells) != 8 or cells[0].strip() or cells[7].strip():
        return None
    mid = ID_CELL.match(cells[1].strip())
    if not mid:
        return None
    stmt = cells[2].strip()
    keys = {}
    for cell, key in zip(cells[3:7], ("source", "snapshot", "digest", "quote")):
        cell = cell.strip()
        if key == "quote":
            m = QUOTE_CELL.match(cell)
            if not m:
                return None
            keys[key] = m.group(1)
            continue
        if not cell.startswith(key + "="):
            return None
        keys[key] = cell[len(key) + 1:]
    return {"id": int(mid.group(1)), "stmt": stmt, **keys}


def parse_registry(text):
    rows = {}
    for line in text.splitlines():
        cells = split_cells(line)
        if len(cells) < 7:
            continue
        rid = cells[1].strip()
        if not REG_ID.match(rid):
            continue
        rows[rid] = {"source": cells[2].strip(), "kind": cells[3].strip(),
                     "anchor": cells[6].strip()}
    return rows


def main():
    if len(sys.argv) != 2:
        print("usage: reader.py <fixture-root>")
        return 2
    root = Path(sys.argv[1])
    note_p = root / NOTE_REL
    reg_p = root / REG_REL
    map_p = root / MAP_REL
    for p in (note_p, reg_p, map_p):
        if not p.is_file():
            print(f"READER absent {p}")
            return 128
    try:
        snapmap = json.loads(map_p.read_text())["snapshots"]
    except (ValueError, KeyError):
        print(f"READER map-malformed {map_p}")
        return 1
    reg = parse_registry(reg_p.read_text())

    parsed, malformed, ids = [], [], set()
    for line in note_p.read_text().splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        row = parse_row(line)
        if row is not None:
            parsed.append(row)
            ids.add(row["id"])
        elif stripped.startswith("| MD") or re.match(r"^\|\s*MD[0-9]", stripped):
            malformed.append(stripped)

    ok = 0
    for row in parsed:
        problems = []
        snap_p = root / SNAPDIR_REL / row["snapshot"]
        snap_bytes = snap_p.read_bytes() if snap_p.is_file() else None
        if snap_bytes is None:
            problems.append("snapshot-absent")
        else:
            snap = norm(snap_bytes.decode("utf-8", errors="replace"))
            if not DIGEST_RE.match(row["digest"]):
                problems.append("digest-shape")
            elif hashlib.sha256(snap_bytes).hexdigest() != row["digest"]:
                problems.append("digest-mismatch")
            if norm(row["quote"]) not in snap:
                problems.append("quote-absent")
        regrow = reg.get(row["source"])
        if regrow is None:
            problems.append("source-unregistered")
        else:
            url = (snapmap.get(row["snapshot"]) or {}).get("url")
            if not url or url not in regrow["source"]:
                problems.append("source-url-not-bound")
            if Path(row["snapshot"]).name not in regrow["anchor"]:
                problems.append("anchor-not-bound")
        if problems:
            print(f"READER row MD{row['id']} red " + " ".join(problems))
        else:
            ok += 1
            print(f"READER row MD{row['id']} ok source={row['source']} "
                  f"snapshot={row['snapshot']}")

    contiguous = sorted(ids) == list(range(1, len(ids) + 1))
    if not contiguous:
        print(f"READER global red ids-not-contiguous ids={sorted(ids)}")
    if malformed:
        print(f"READER info malformed-lines={len(malformed)} (not gated by this reader)")
    red = len(parsed) - ok
    print(f"READER rows={len(parsed)} ok={ok} red={red} contiguous={int(contiguous)}")
    return 0 if len(parsed) == 6 and ok == 6 and contiguous else 1


if __name__ == "__main__":
    sys.exit(main())
