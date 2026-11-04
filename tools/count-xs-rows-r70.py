#!/usr/bin/env python3
# round-70 C1 strict row counter (frozen by the round-70 declaration, before any note exists).
#
# Counts only XS rows of corpus/knowledge/xfs-storage-plane-r70.md that satisfy every frozen
# clause below. Reads Git objects (--revision) or a fixture mirror (--fixture) and creates no
# temporary file. It is NOT the scorecard's counter for the census arm (round 70 C2); C2's
# predicate greps tools/tsukuroi-census.sh.
#
# Frozen clauses per row: id unique and contiguous from 1; statement >= 12 words; statement
# shares >= 3 distinct non-stopword tokens (length >= 4) with the row's snapshot text
# (statement-substance clause); source=S### resolves to a registry row at the same revision;
# snapshot=<name> exists under .ufo/waves/round-70/before/src with sha256 == digest; the row's
# digest equals the digest recorded for that snapshot in src/SOURCES.json AND the registry
# row's source cell contains that map URL (source-to-snapshot binding clause); quote <= 25
# words, contains no pipe, and is located verbatim (whitespace-normalized) in the snapshot.
# Target: rows == 6 and verified == 6 and distinct sources >= 4 and distinct snapshots >= 4.
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

NOTE = "corpus/knowledge/xfs-storage-plane-r70.md"
REGISTRY = "corpus/SOURCES.md"
SNAPDIR = ".ufo/waves/round-70/before/src"
MAP = SNAPDIR + "/SOURCES.json"
TARGET_ROWS = 6
TARGET_SOURCES = 4
TARGET_SNAPSHOTS = 4
MIN_WORDS = 12
MIN_TOKENS = 3
MAX_QUOTE_WORDS = 25

ROW_RE = re.compile(
    r'^\| XS(?P<n>[0-9]+) \| (?P<stmt>.+?) \| source=(?P<src>S[0-9]{3,}) '
    r'\| snapshot=(?P<snap>[A-Za-z0-9._-]+) \| digest=(?P<digest>[0-9a-f]{64}) '
    r'\| quote="(?P<quote>[^"]*)" \|$')
SROW_RE = re.compile(r'^\| *S(?P<n>[0-9]{3,}) *\|')
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{3,}")
STOP = {
    "this", "that", "these", "those", "with", "from", "have", "has", "had", "were", "was",
    "each", "when", "then", "than", "only", "also", "into", "over", "under", "such", "which",
    "where", "there", "their", "they", "them", "what", "will", "would", "should", "could",
    "must", "does", "does", "been", "being", "because", "after", "before", "about", "above",
    "below", "more", "most", "less", "some", "any", "all", "not", "and", "but", "for", "its",
    "row", "rows", "note", "entry", "lane", "host", "statement", "value", "values",
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


def grounded(stmt, snapshot):
    snap = snapshot.lower()
    hits = set()
    for tok in WORD_RE.findall(stmt):
        t = tok.lower()
        if t in STOP or t in hits:
            continue
        if re.search(r"(?<![a-z0-9_])" + re.escape(t) + r"(?![a-z0-9_])", snap):
            hits.add(t)
    return len(hits)


def evaluate(rt, rb):
    read = rt
    note = read(NOTE)
    if note is None:
        print(f"XS_NOTE absent path={NOTE}")
        return 128
    reg_text = read(REGISTRY)
    if reg_text is None:
        print(f"XS_REGISTRY absent path={REGISTRY}")
        return 128
    map_text = read(MAP)
    if map_text is None:
        print(f"XS_MAP absent path={MAP}")
        return 128
    try:
        snapmap = json.loads(map_text)["snapshots"]
    except (ValueError, KeyError):
        print(f"XS_MAP malformed path={MAP}")
        return 1
    reg = registry_rows(reg_text)
    rows = []
    for line in note.splitlines():
        if not line.startswith("| XS"):
            continue
        rows.append(line)
    verified = 0
    sources, snaps = set(), set()
    seen_ids = set()
    for line in rows:
        m = ROW_RE.match(line)
        if not m or line.count("|") != 7:
            print(f"XS_ROW fail malformed: {line[:60]}")
            continue
        n, stmt = int(m.group("n")), m.group("stmt").strip()
        problems = []
        if n in seen_ids:
            problems.append("duplicate-id")
        seen_ids.add(n)
        if words(stmt) < MIN_WORDS:
            problems.append(f"statement-words={words(stmt)}")
        snap_name = m.group("snap")
        snap_b = rb(f"{SNAPDIR}/{snap_name}")
        if snap_b is None:
            problems.append("snapshot-absent")
        else:
            snap = snap_b.decode("utf-8", errors="replace")
            digest = hashlib.sha256(snap_b).hexdigest()
            if digest != m.group("digest"):
                problems.append("digest-mismatch")
            entry = snapmap.get(snap_name)
            if not isinstance(entry, dict) or entry.get("sha256") != m.group("digest"):
                problems.append("map-digest")
            elif not isinstance(entry.get("url"), str):
                problems.append("map-url")
            if grounded(stmt, snap) < MIN_TOKENS:
                problems.append(f"statement-tokens={grounded(stmt, snap)}")
            quote = m.group("quote")
            if "|" in quote:
                problems.append("quote-pipe")
            if words(quote) > MAX_QUOTE_WORDS:
                problems.append(f"quote-words={words(quote)}")
            if norm(quote) not in norm(snap):
                problems.append("quote-absent")
        src = m.group("src")
        regrow = reg.get(src)
        if regrow is None:
            problems.append("source-unregistered")
        else:
            entry = snapmap.get(snap_name)
            url = entry.get("url") if isinstance(entry, dict) else None
            if not url or url not in regrow["source"]:
                problems.append("source-not-bound")
            sources.add(src)
            snaps.add(snap_name)
        if problems:
            print(f"XS_ROW fail XS{n} " + " ".join(problems))
        else:
            verified += 1
            print(f"XS_ROW ok XS{n} source={src} snapshot={snap_name}")
    contiguous = sorted(seen_ids) == list(range(1, len(seen_ids) + 1))
    if rows and not contiguous:
        print("XS_ROW fail ids-not-contiguous")
    met = (len(rows) == TARGET_ROWS and verified == TARGET_ROWS and contiguous
           and verified == len(rows) and len(sources) >= TARGET_SOURCES
           and len(snaps) >= TARGET_SNAPSHOTS)
    print(f"XS_ROWS={len(rows)} XS_VERIFIED={verified} XS_SOURCES={len(sources)} "
          f"XS_SNAPSHOTS={len(snaps)}")
    print(f"XS_TARGET rows={TARGET_ROWS} verified={TARGET_ROWS} sources>={TARGET_SOURCES} "
          f"snapshots>={TARGET_SNAPSHOTS} met={1 if met else 0}")
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
