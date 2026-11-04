#!/usr/bin/env python3
# round-72 C1 strict row counter (frozen by the round-72 declaration, before any note exists).
#
# Counts only MD rows of corpus/knowledge/modprobe-config-plane-r72.md that satisfy every
# frozen clause below. Reads Git objects (--revision) or a fixture mirror (--fixture) and
# creates no temporary file.
#
# Frozen clauses per row: id unique and contiguous from 1; statement >= 12 words; >= 6 distinct
# non-stopword tokens (length >= 4) shared with the row's snapshot text AND shared/total >= 0.5;
# source=S### resolves to a registry row at the same revision; that row's kind is a source kind
# and is not own-work (QUALITY 86: an own-work row grounds host observations, never a rule);
# snapshot=<name> exists under .ufo/waves/round-72/before/src with sha256 == digest; the row's
# digest equals the digest recorded for that snapshot in src/SOURCES.json AND the registry
# row's source cell contains that map URL; the registry row's anchor cell contains the
# snapshot's basename; quote <= 25 words, contains no pipe, and is located verbatim
# (whitespace-normalized) in the snapshot. Any MD-shaped line that does not parse is a
# malformed-row finding. No snapshot may be cited more than twice.
# Target: rows == 6 and verified == 6 and distinct sources >= 3 and distinct snapshots >= 3.
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

NOTE = "corpus/knowledge/modprobe-config-plane-r72.md"
REGISTRY = "corpus/SOURCES.md"
SNAPDIR = ".ufo/waves/round-72/before/src"
MAP = SNAPDIR + "/SOURCES.json"
TARGET_ROWS = 6
TARGET_SOURCES = 3
TARGET_SNAPSHOTS = 3
MIN_WORDS = 12
MIN_TOKENS = 6
MIN_SHARE = 0.5
MAX_QUOTE_WORDS = 25
MAX_SNAPSHOT_REUSE = 2
KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community"}

ROW_RE = re.compile(
    r'^\| MD(?P<n>[0-9]+) \| (?P<stmt>[^|]+) \| source=(?P<src>S[0-9]{3,}) '
    r'\| snapshot=(?P<snap>[^ |]+) \| digest=(?P<digest>[0-9a-f]{64}) '
    r'\| quote="(?P<quote>[^"]*)" \|$')
CAND_RE = re.compile(r'^\s*\|\s*MD[0-9]+\s*\|')
SROW_RE = re.compile(r'^\|\s*S(?P<n>[0-9]{3,})\s*\|')
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{3,}")
STOP = set("""
that this with from into than then them they their there these those which while where when
have has had been being were was are its it's not but for and the a an of to in on at by as or
is are do does did can could would should may might must shall will one two three also such
more most less least other others same different only over under about across after before
each every both all any some no nor own same very just even still yet because since until
""".split())


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
        rows["S" + m.group("n")] = {
            "source": cells[2] if len(cells) > 2 else "",
            "kind": (cells[3] if len(cells) > 3 else "").strip(),
            "anchor": cells[6] if len(cells) > 6 else "",
        }
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
        print(f"MD_NOTE absent path={NOTE}")
        return 128
    reg_text = rt(REGISTRY)
    if reg_text is None:
        print(f"MD_REGISTRY absent path={REGISTRY}")
        return 128
    map_text = rt(MAP)
    if map_text is None:
        print(f"MD_MAP absent path={MAP}")
        return 128
    try:
        snapmap = json.loads(map_text)["snapshots"]
    except (ValueError, KeyError):
        print(f"MD_MAP malformed path={MAP}")
        return 1
    reg = registry_rows(reg_text)

    rows, malformed = [], 0
    for line in note.splitlines():
        if CAND_RE.match(line):
            if ROW_RE.match(line) and line.count("|") == 7:
                rows.append(line)
            else:
                malformed += 1
                print(f"MD_ROW fail malformed-row: {line[:70]}")

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
            if regrow["kind"] not in KINDS or regrow["kind"] == "own-work":
                problems.append(f"source-kind={regrow['kind'] or 'absent'}")
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
            print(f"MD_ROW fail MD{n} " + " ".join(problems))
        else:
            verified += 1
            print(f"MD_ROW ok MD{n} source={src} snapshot={snap_name}")

    contiguous = sorted(seen_ids) == list(range(1, len(seen_ids) + 1))
    if rows and not contiguous:
        print("MD_ROW fail ids-not-contiguous")
    over = {k: v for k, v in reuse.items() if v > MAX_SNAPSHOT_REUSE}
    for k, v in sorted(over.items()):
        print(f"MD_ROW fail snapshot-reuse {k}={v}")
    met = (malformed == 0 and len(rows) == TARGET_ROWS and verified == TARGET_ROWS
           and contiguous and not over and len(sources) >= TARGET_SOURCES
           and len(snaps) >= TARGET_SNAPSHOTS)
    print(f"MD_ROWS={len(rows)} MD_VERIFIED={verified} MD_SOURCES={len(sources)} "
          f"MD_SNAPSHOTS={len(snaps)} MD_MALFORMED={malformed}")
    print(f"MD_TARGET rows={TARGET_ROWS} verified={TARGET_ROWS} sources>={TARGET_SOURCES} "
          f"snapshots>={TARGET_SNAPSHOTS} max_reuse={MAX_SNAPSHOT_REUSE} met={1 if met else 0}")
    return 0 if met else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--revision", default="HEAD")
    ap.add_argument("--fixture")
    args = ap.parse_args()
    return evaluate(*readers(args.revision, args.fixture))


if __name__ == "__main__":
    sys.exit(main())
