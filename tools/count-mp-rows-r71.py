#!/usr/bin/env python3
# round-71 C1 strict row counter (frozen by the round-71 declaration, before any note exists).
#
# Counts only MP rows of corpus/knowledge/module-parameter-plane-r71.md that satisfy every
# frozen clause below. Reads Git objects (--revision) or a fixture mirror (--fixture) and
# creates no temporary file.
#
# Frozen clauses per row: id unique and contiguous from 1; statement >= 12 words; >= 6 distinct
# non-stopword tokens (length >= 4) shared with the row's snapshot text AND shared/total >= 0.5
# (the r70-M4 repair: three real tokens plus gibberish no longer grounds a statement);
# source=S### resolves to a registry row at the same revision; snapshot=<name> exists under
# .ufo/waves/round-71/before/src with sha256 == digest; the row's digest equals the digest
# recorded for that snapshot in src/SOURCES.json AND the registry row's source cell contains
# that map URL; the registry row's anchor cell contains the snapshot's basename (the r70-M6
# repair: the anchor cell is read, not parsed and dropped); quote <= 25 words, contains no
# pipe, and is located verbatim (whitespace-normalized) in the snapshot. Any MP-shaped line
# that does not parse is a malformed-row finding (the r70-M11 repair: an invisible row is not
# skipped). No snapshot may be cited more than twice (the r70-M5 repair).
# Target: rows == 6 and verified == 6 and distinct sources >= 4 and distinct snapshots >= 4.
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

NOTE = "corpus/knowledge/module-parameter-plane-r71.md"
REGISTRY = "corpus/SOURCES.md"
SNAPDIR = ".ufo/waves/round-71/before/src"
MAP = SNAPDIR + "/SOURCES.json"
TARGET_ROWS = 6
TARGET_SOURCES = 4
TARGET_SNAPSHOTS = 4
MIN_WORDS = 12
MIN_TOKENS = 6
MIN_SHARE = 0.5
MAX_QUOTE_WORDS = 25
MAX_SNAPSHOT_REUSE = 2

ROW_RE = re.compile(
    r'^\| MP(?P<n>[0-9]+) \| (?P<stmt>.+?) \| source=(?P<src>S[0-9]{3,}) '
    r'\| snapshot=(?P<snap>[A-Za-z0-9._-]+) \| digest=(?P<digest>[0-9a-f]{64}) '
    r'\| quote="(?P<quote>[^"]*)" \|$')
CAND_RE = re.compile(r'^\s*\|\s*MP[0-9]+\s*\|')
SROW_RE = re.compile(r'^\|\s*S(?P<n>[0-9]{3,})\s*\|')
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{3,}")
STOP = {
    "this", "that", "these", "those", "with", "from", "have", "has", "had", "were", "was",
    "each", "when", "then", "than", "only", "also", "into", "over", "under", "such", "which",
    "where", "there", "their", "they", "them", "what", "will", "would", "should", "could",
    "must", "does", "been", "being", "because", "after", "before", "about", "above", "below",
    "more", "most", "less", "some", "any", "all", "not", "and", "but", "for", "its", "row",
    "rows", "note", "entry", "lane", "host", "statement", "value", "values", "parameter",
    "parameters", "kernel", "module", "modules", "file", "files", "sysfs", "path", "paths",
}


def readers(revision, fixture):
    """Return (read_text, read_bytes) callables over one fixed tree."""
    if fixture:
        root = Path(fixture)

        def rt(rel):
            p = root / rel
            return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else None

        def rb(rel):
            p = root / rel
            return p.read_bytes() if p.is_file() else None

        return rt, rb
    lane = str(Path(__file__).resolve().parent.parent)

    def rt(rel):
        r = subprocess.run(["git", "-C", lane, "show", f"{revision}:{rel}"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        return r.stdout if r.returncode == 0 else None

    def rb(rel):
        r = subprocess.run(["git", "-C", lane, "show", f"{revision}:{rel}"],
                           capture_output=True)
        return r.stdout if r.returncode == 0 else None

    return rt, rb


def norm(s):
    return " ".join(s.split())


def words(s):
    return len(s.split())


def registry_rows(text):
    rows = {}
    for line in (text or "").splitlines():
        m = SROW_RE.match(line)
        if not m:
            continue
        cells = line.split("|")
        rows["S" + m.group("n")] = {"source": cells[2], "anchor": cells[6]}
    return rows


def grounding(stmt, snapshot):
    """(shared distinct tokens, total distinct tokens) against the snapshot text."""
    snap = snapshot.lower()
    total, hits = set(), set()
    for tok in WORD_RE.findall(stmt):
        t = tok.lower()
        if t in STOP:
            continue
        total.add(t)
        if re.search(r"(?<![a-z0-9_])" + re.escape(t) + r"(?![a-z0-9_])", snap):
            hits.add(t)
    return len(hits), len(total)


def evaluate(rt, rb):
    note = rt(NOTE)
    if note is None:
        print(f"MP_NOTE absent path={NOTE}")
        return 128
    reg_text = rt(REGISTRY)
    if reg_text is None:
        print(f"MP_REGISTRY absent path={REGISTRY}")
        return 128
    map_text = rt(MAP)
    if map_text is None:
        print(f"MP_MAP absent path={MAP}")
        return 128
    try:
        snapmap = json.loads(map_text)["snapshots"]
    except (ValueError, KeyError):
        print(f"MP_MAP malformed path={MAP}")
        return 1
    reg = registry_rows(reg_text)

    rows, malformed = [], 0
    for line in note.splitlines():
        if CAND_RE.match(line):
            if ROW_RE.match(line) and line.count("|") == 7:
                rows.append(line)
            else:
                malformed += 1
                print(f"MP_ROW fail malformed-row: {line[:70]}")

    verified = 0
    sources, snaps, reuse, seen_ids = set(), set(), {}, set()
    for line in rows:
        m = ROW_RE.match(line)
        n, stmt = int(m.group("n")), m.group("stmt").strip()
        snap_name, src = m.group("snap"), m.group("src")
        problems = []
        if n in seen_ids:
            problems.append("duplicate-id")
        seen_ids.add(n)
        if words(stmt) < MIN_WORDS:
            problems.append(f"statement-words={words(stmt)}")
        snap_b = rb(f"{SNAPDIR}/{snap_name}")
        if snap_b is None:
            problems.append("snapshot-absent")
        else:
            snap = snap_b.decode("utf-8", errors="replace")
            if hashlib.sha256(snap_b).hexdigest() != m.group("digest"):
                problems.append("digest-mismatch")
            entry = snapmap.get(snap_name)
            if not isinstance(entry, dict) or entry.get("sha256") != m.group("digest"):
                problems.append("map-digest")
            elif not isinstance(entry.get("url"), str):
                problems.append("map-url")
            hits, total = grounding(stmt, snap)
            if hits < MIN_TOKENS or (total and hits / total < MIN_SHARE):
                problems.append(f"statement-grounding={hits}/{total}")
            quote = m.group("quote")
            if "|" in quote:
                problems.append("quote-pipe")
            if words(quote) > MAX_QUOTE_WORDS:
                problems.append(f"quote-words={words(quote)}")
            if norm(quote) not in norm(snap):
                problems.append("quote-absent")
        regrow = reg.get(src)
        if regrow is None:
            problems.append("source-unregistered")
        else:
            entry = snapmap.get(snap_name)
            url = entry.get("url") if isinstance(entry, dict) else None
            if not url or url not in regrow["source"]:
                problems.append("source-not-bound")
            if snap_name not in regrow["anchor"]:
                problems.append("anchor-not-bound")
            sources.add(src)
            snaps.add(snap_name)
            reuse[snap_name] = reuse.get(snap_name, 0) + 1
        if problems:
            print(f"MP_ROW fail MP{n} " + " ".join(problems))
        else:
            verified += 1
            print(f"MP_ROW ok MP{n} source={src} snapshot={snap_name}")

    contiguous = sorted(seen_ids) == list(range(1, len(seen_ids) + 1))
    if rows and not contiguous:
        print("MP_ROW fail ids-not-contiguous")
    over = {k: v for k, v in reuse.items() if v > MAX_SNAPSHOT_REUSE}
    for k, v in sorted(over.items()):
        print(f"MP_ROW fail snapshot-reuse {k}={v}")
    met = (malformed == 0 and len(rows) == TARGET_ROWS and verified == TARGET_ROWS
           and contiguous and not over and len(sources) >= TARGET_SOURCES
           and len(snaps) >= TARGET_SNAPSHOTS)
    print(f"MP_ROWS={len(rows)} MP_VERIFIED={verified} MP_SOURCES={len(sources)} "
          f"MP_SNAPSHOTS={len(snaps)} MP_MALFORMED={malformed}")
    print(f"MP_TARGET rows={TARGET_ROWS} verified={TARGET_ROWS} sources>={TARGET_SOURCES} "
          f"snapshots>={TARGET_SNAPSHOTS} max_reuse={MAX_SNAPSHOT_REUSE} met={1 if met else 0}")
    return 0 if met else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--revision")
    g.add_argument("--fixture")
    args = ap.parse_args()
    return evaluate(*readers(args.revision, args.fixture))


if __name__ == "__main__":
    sys.exit(main())
