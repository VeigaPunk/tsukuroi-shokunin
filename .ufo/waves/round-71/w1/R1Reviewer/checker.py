#!/usr/bin/env python3
"""R1Reviewer independent C1 checker (round-71).

Written from the frozen declaration clauses in SCORECARD.md "Round 71 — declaration"
only. Shares no code with tools/count-mp-rows-r71.py. Checks:

  note carries exactly six MP rows; row grammar = one physical line, exactly 6 cells
  (7 pipe chars), no pipe inside a cell; per row: unique contiguous id; statement
  >= 12 words; >= 6 distinct non-stopword tokens (len >= 4) shared with the row's
  snapshot text AND shared/total >= 0.5; source=S### resolves to a registry row at
  the same revision; snapshot file exists with sha256 == digest == the digest in
  src/SOURCES.json; registry source cell contains the map URL; registry anchor cell
  contains the snapshot basename; quote <= 25 words, no pipe, verbatim
  (whitespace-normalized) in the snapshot. Any MP-shaped line that does not parse is
  a malformed-row finding. No snapshot cited more than twice.

Exit rc 0 iff targets met (rows==6, verified==6, sources>=4, snapshots>=4,
malformed==0, ids contiguous, reuse <= 2).
"""
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
CLONE = "/fast/scratch/hyaku/tsukuroi-r71/R1Reviewer/clone"

TARGET_ROWS = 6
TARGET_SOURCES = 4
TARGET_SNAPSHOTS = 4
MIN_STMT_WORDS = 12
MIN_SHARED = 6
MIN_SHARE = 0.5
MAX_QUOTE_WORDS = 25
MAX_REUSE = 2

# My own stopword list: general English function words only. Domain nouns
# (parameter, kernel, module, file, ...) are deliberately NOT stopwords here —
# they are exactly the tokens that should ground a statement in a kernel source.
STOP = frozenset("""
the this that these those there here it its they them their he she his her hers we our
ours you your yours me my mine of to in on at by for with without from into onto over
under above below up down out off again further once during before after between through
against about across along among around because before behind beneath beside besides
and but or nor not no only also just too very so than then when while where which who
whom whose what why how whether all any both each either every few more most other some
such own same none somebody someone something neither
is are was were be been being am do does did done doing has have had having will would
shall should can could may might must ought
if although though unless until since as like
""".split())

TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_-]{3,}")
CAND = re.compile(r"^\s*\|\s*MP[0-9]+")
def parse_row(line):
    parts = line.split("|")
    if len(parts) != 8 or parts[0] or parts[-1]:
        return None
    if any(not (p.startswith(" ") and p.endswith(" ")) for p in parts[1:-1]):
        return None
    cells = [p[1:-1] for p in parts[1:-1]]
    if not re.fullmatch(r"MP[0-9]+", cells[0]) or not cells[1]:
        return None
    result = {"n": cells[0][2:], "stmt": cells[1]}
    for key, prefix, pattern, cell in [
        ("src", "source=", r"S[0-9]{3,}", cells[2]),
        ("snap", "snapshot=", r"[A-Za-z0-9._-]+", cells[3]),
        ("digest", "digest=", r"[0-9a-f]{64}", cells[4]),
        ("quote", 'quote="', r'[^"]*', cells[5]),
    ]:
        if not cell.startswith(prefix):
            return None
        value = cell[len(prefix):]
        if key == "quote":
            if not value.endswith('"'):
                return None
            value = value[:-1]
        if not re.fullmatch(pattern, value):
            return None
        result[key] = value
    return result

SROW = re.compile(r"^\|\s*S(?P<n>[0-9]{3,})\s*\|")


def norm(s):
    return " ".join(s.split())


def token_set(text):
    return {t.lower() for t in TOKEN.findall(text)}


def grounding(stmt, snapshot_text):
    total = token_set(stmt) - STOP
    snap = snapshot_text.lower()
    hits = set()
    for t in sorted(total):
        if re.search(r"(?<![A-Za-z0-9_-])" + re.escape(t) + r"(?![A-Za-z0-9_-])", snap):
            hits.add(t)
    return hits, total


def readers(fixture, revision):
    if fixture:
        root = Path(fixture)

        def rt(rel):
            p = root / rel
            return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else None

        def rb(rel):
            p = root / rel
            return p.read_bytes() if p.is_file() else None

        return rt, rb

    def rt(rel):
        r = subprocess.run(["git", "-C", CLONE, "show", f"{revision}:{rel}"],
                           capture_output=True)
        return r.stdout.decode("utf-8", errors="replace") if r.returncode == 0 else None

    def rb(rel):
        r = subprocess.run(["git", "-C", CLONE, "show", f"{revision}:{rel}"],
                           capture_output=True)
        return r.stdout if r.returncode == 0 else None

    return rt, rb


def registry_rows(text):
    rows = {}
    for line in (text or "").splitlines():
        m = SROW.match(line)
        if not m:
            continue
        cells = line.split("|")
        if len(cells) < 7:
            continue
        rows["S" + m.group("n")] = {"source": cells[2], "anchor": cells[6]}
    return rows


def evaluate(rt, rb):
    findings = []
    note = rt(NOTE)
    if note is None:
        findings.append("NOTE-ABSENT " + NOTE)
        print("\n".join(findings))
        return 128
    reg_text = rt(REGISTRY)
    map_text = rt(MAP)
    if reg_text is None:
        findings.append("REGISTRY-ABSENT " + REGISTRY)
    if map_text is None:
        findings.append("MAP-ABSENT " + MAP)
    if reg_text is None or map_text is None:
        print("\n".join(findings))
        return 128
    try:
        snapmap = json.loads(map_text)["snapshots"]
        assert isinstance(snapmap, dict)
    except Exception:
        findings.append("MAP-MALFORMED " + MAP)
        print("\n".join(findings))
        return 1
    reg = registry_rows(reg_text)

    rows, malformed = [], 0
    for line in note.splitlines():
        if CAND.match(line):
            parsed = parse_row(line)
            if parsed is not None:
                rows.append(parsed)
            else:
                malformed += 1
                findings.append(f"MALFORMED-ROW line={line.strip()[:70]}")

    verified = 0
    sources, snaps, reuse, seen_ids = set(), set(), {}, []
    for m in rows:
        n = int(m["n"])
        stmt = m["stmt"].strip()
        snap_name, src, digest = m["snap"], m["src"], m["digest"]
        quote = m["quote"]
        problems = []
        seen_ids.append(n)
        if seen_ids.count(n) > 1:
            problems.append("duplicate-id")
        if len(stmt.split()) < MIN_STMT_WORDS:
            problems.append(f"statement-words<{MIN_STMT_WORDS}")
        if "|" in quote:
            problems.append("quote-pipe")
        if len(quote.split()) > MAX_QUOTE_WORDS:
            problems.append(f"quote-words>{MAX_QUOTE_WORDS}")

        snap_b = rb(f"{SNAPDIR}/{snap_name}")
        if snap_b is None:
            problems.append("snapshot-absent")
            snap_text = None
        else:
            snap_text = snap_b.decode("utf-8", errors="replace")
            if hashlib.sha256(snap_b).hexdigest() != digest:
                problems.append("digest-mismatch")
            entry = snapmap.get(snap_name)
            if not isinstance(entry, dict) or entry.get("sha256") != digest:
                problems.append("map-digest")
            elif not isinstance(entry.get("url"), str) or not entry.get("url"):
                problems.append("map-url")
            hits, total = grounding(stmt, snap_text)
            if len(hits) < MIN_SHARED or (total and len(hits) / len(total) < MIN_SHARE):
                problems.append(f"statement-grounding={len(hits)}/{len(total)}")
            if norm(quote) not in norm(snap_text):
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
            findings.append(f"ROW MP{n} fail {' '.join(sorted(problems))}")
        else:
            verified += 1
            findings.append(f"ROW MP{n} ok source={src} snapshot={snap_name}")

    ids_sorted = sorted(set(seen_ids))
    contiguous = ids_sorted == list(range(1, len(ids_sorted) + 1))
    if rows and not contiguous:
        findings.append("IDS-NOT-CONTIGUOUS " + ",".join(str(i) for i in sorted(seen_ids)))
    over = {k: v for k, v in sorted(reuse.items()) if v > MAX_REUSE}
    for k, v in over.items():
        findings.append(f"SNAPSHOT-REUSE {k}={v}")

    met = (malformed == 0 and len(rows) == TARGET_ROWS and verified == TARGET_ROWS
           and contiguous and not over and len(sources) >= TARGET_SOURCES
           and len(snaps) >= TARGET_SNAPSHOTS)
    print("\n".join(findings))
    print(f"MP_ROWS={len(rows)} MP_VERIFIED={verified} MP_SOURCES={len(sources)} "
          f"MP_SNAPSHOTS={len(snaps)} MP_MALFORMED={malformed} MET={1 if met else 0}")
    return 0 if met else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--fixture")
    g.add_argument("--revision")
    args = ap.parse_args()
    return evaluate(*readers(args.fixture, args.revision))


if __name__ == "__main__":
    sys.exit(main())
