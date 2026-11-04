#!/usr/bin/env python3
# round-73 C1 strict row counter (frozen by the round-73 declaration, before any note exists).
#
# Counts only UL rows of corpus/knowledge/systemd-unit-load-plane-r73.md that satisfy every
# frozen clause below. Reads Git objects (--revision) or a fixture mirror (--fixture); the
# self-test copies the committed snapshots into one $TMPDIR root and writes nothing outside it.
#
# Frozen clauses per row: id unique and contiguous from 1; statement >= 12 words; >= 6 distinct
# non-stopword tokens (length >= 4) shared with the row's snapshot text AND shared/total >= 0.5;
# source=S### resolves to a registry row at the same revision; that row's kind is a source kind
# and is not own-work (QUALITY 86: an own-work row grounds host observations, never a rule);
# snapshot=<name> exists under .ufo/waves/round-73/before/src with sha256 == digest; the row's
# digest equals the digest recorded for that snapshot in src/SOURCES.json AND the registry
# row's source cell contains that map URL; the registry row's anchor cell contains the
# snapshot's basename; quote <= 25 words, contains no pipe, and is located verbatim
# (whitespace-normalized) in the snapshot. Any UL-shaped line that does not parse is a
# malformed-row finding. No snapshot may be cited more than twice.
# Target: rows == 6 and verified == 6 and distinct sources >= 3 and distinct snapshots >= 3.
#
# Exit map: 0 target met; 1 target missed (including UL_MAP malformed); 2 cannot evaluate under
# --selftest only ($TMPDIR names no directory, or is /tmp); 3 self-test failed; 128 UL_NOTE,
# UL_REGISTRY or UL_MAP absent. An absent data file in --revision/--fixture mode is 128, not 2.
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

NOTE = "corpus/knowledge/systemd-unit-load-plane-r73.md"
REGISTRY = "corpus/SOURCES.md"
SNAPDIR = ".ufo/waves/round-73/before/src"
MAP = SNAPDIR + "/SOURCES.json"
TARGET_ROWS = 6
TARGET_SOURCES = 3
TARGET_SNAPSHOTS = 3
MIN_WORDS = 12
MIN_TOKENS = 6
MIN_SHARE = 0.5
MIN_QUOTE_WORDS = 4
MAX_QUOTE_WORDS = 25
MAX_SNAPSHOT_REUSE = 2
KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community"}
BASE_URL = "https://raw.githubusercontent.com/systemd/systemd/v262/"

ROW_RE = re.compile(
    r'^\| UL(?P<n>[0-9]+) \| (?P<stmt>[^|]+) \| source=(?P<src>S[0-9]{3,}) '
    r'\| snapshot=(?P<snap>[^ |]+) \| digest=(?P<digest>[0-9a-f]{64}) '
    r'\| quote="(?P<quote>[^"]*)" \|$')
CAND_RE = re.compile(r'^\s*\|\s*UL[0-9]+\s*\|')
SROW_RE = re.compile(r'^\|\s*S(?P<n>[0-9]{3,})\s*\|')
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{3,}")
STOP = set("""
that this with from into than then them they their there these those which while where when
have has had been being were was are its it's not but for and the a an of to in on at by as or
is are do does did can could would should may might must shall will one two three also such
more most less least other others same different only over under about across after before
each every both all any some no nor own same very just even still yet because since until
""".split())

# Self-test sample rows. They carry the round's own statements so the control case exercises the
# same shape the counted note uses; their quotes are located in the committed snapshots. The
# self-test scores the counter's mechanics, never the note's admission.
SAMPLE_ROWS = [
    ("UL1", "systemd.unit.xml", "Unit files are loaded from a compiled load path, so a unit found "
     "in a directory listed earlier overrides the same name lower in the list, and the "
     "SYSTEMD_UNIT_PATH variable replaces the whole path",
     "Unit files found in directories listed earlier override files with the same name in "
     "directories lower in the list"),
    ("UL2", "systemd.unit.xml", "Multiple drop-in files with different names are applied in "
     "lexicographic order regardless of the directory they reside in, drop-in files in etc take "
     "precedence over run and usr/lib, and drop-ins beat unit files wherever located",
     "Multiple drop-in files with different names are applied in lexicographic order, regardless "
     "of which of the directories they reside in"),
    ("UL3", "unit.c", "A loaded unit needs a daemon reload when its drop-in path list differs from "
     "the list read at load time or a drop-in file is newer than the last reload, and masked "
     "drop-ins are omitted from that list",
     "any drop-ins that are masked are simply omitted from the list"),
    ("UL4", "unit.c", "A masked unit stays masked while its fragment path is null or empty, so a "
     "zero-size file and a dev/null symlink both keep the masked state until the path changes",
     "For masked files check if they are still so"),
    ("UL5", "install.c", "The mask operation writes a dev/null symlink at the unit name, the "
     "install mode distinguishes masked from masked-runtime, and a mask created by a generator "
     "cannot be unmasked",
     "Unit %s is masked, ignoring."),
    ("UL6", "install.c", "An Install alias is parsed when the unit is enabled, and an alias that "
     "points at a unit which does not exist is unresolvable and is ignored rather than created",
     "Unit %s is an alias to a non-existent unit, ignoring."),
]
SAMPLE_SOURCES = {
    "S304": ("systemd.unit.xml", BASE_URL + "man/systemd.unit.xml", "docs",
             "systemd.unit.xml at tag v262 (unit file load path and drop-in merge)"),
    "S305": ("unit.c", BASE_URL + "src/core/unit.c", "code",
             "unit.c at tag v262 (drop-in set and mask freshness)"),
    "S306": ("install.c", BASE_URL + "src/shared/install.c", "code",
             "install.c at tag v262 (mask symlink and alias install modes)"),
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


def evaluate(rt, rb, out=sys.stdout):
    def emit(line):
        print(line, file=out)

    note = rt(NOTE)
    if note is None:
        emit(f"UL_NOTE absent path={NOTE}")
        return 128
    reg_text = rt(REGISTRY)
    if reg_text is None:
        emit(f"UL_REGISTRY absent path={REGISTRY}")
        return 128
    map_text = rt(MAP)
    if map_text is None:
        emit(f"UL_MAP absent path={MAP}")
        return 128
    try:
        snapmap = json.loads(map_text)["snapshots"]
    except (ValueError, KeyError, TypeError):
        emit(f"UL_MAP malformed path={MAP}")
        return 1
    if not isinstance(snapmap, dict):
        emit(f"UL_MAP malformed path={MAP}")
        return 1
    reg = registry_rows(reg_text)

    rows, malformed = [], 0
    for line in note.splitlines():
        if CAND_RE.match(line):
            if ROW_RE.match(line) and line.count("|") == 7:
                rows.append(line)
            else:
                malformed += 1
                emit(f"UL_ROW fail malformed-row: {line[:70]}")

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
            if words(quote) < MIN_QUOTE_WORDS:
                problems.append(f"quote-words={words(quote)}")
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
            emit(f"UL_ROW fail UL{n} " + " ".join(problems))
        else:
            verified += 1
            emit(f"UL_ROW ok UL{n} source={src} snapshot={snap_name}")

    contiguous = sorted(seen_ids) == list(range(1, len(seen_ids) + 1))
    if rows and not contiguous:
        emit("UL_ROW fail ids-not-contiguous")
    over = {k: v for k, v in reuse.items() if v > MAX_SNAPSHOT_REUSE}
    for k, v in sorted(over.items()):
        emit(f"UL_ROW fail snapshot-reuse {k}={v}")
    met = (malformed == 0 and len(rows) == TARGET_ROWS and verified == TARGET_ROWS
           and contiguous and not over and len(sources) >= TARGET_SOURCES
           and len(snaps) >= TARGET_SNAPSHOTS)
    emit(f"UL_ROWS={len(rows)} UL_VERIFIED={verified} UL_SOURCES={len(sources)} "
         f"UL_SNAPSHOTS={len(snaps)} UL_MALFORMED={malformed}")
    emit(f"UL_TARGET rows={TARGET_ROWS} verified={TARGET_ROWS} sources>={TARGET_SOURCES} "
         f"snapshots>={TARGET_SNAPSHOTS} max_reuse={MAX_SNAPSHOT_REUSE} met={1 if met else 0}")
    return 0 if met else 1


def build_fixture(root, mutate=None):
    """Write one fixture tree under root; mutate(tree) edits it in place."""
    src = root / SNAPDIR
    src.mkdir(parents=True, exist_ok=True)
    lane = Path(__file__).resolve().parent.parent
    real = lane / SNAPDIR
    digests = {}
    for name in ("systemd.unit.xml", "unit.c", "install.c"):
        data = (real / name).read_bytes()
        (src / name).write_bytes(data)
        digests[name] = hashlib.sha256(data).hexdigest()
    snapmap = {"snapshots": {name: {"url": SAMPLE_SOURCES[sid][1], "sha256": digests[name]}
                             for sid, (name, _url, _k, _a) in SAMPLE_SOURCES.items()}}
    (src / "SOURCES.json").write_text(json.dumps(snapmap, indent=2) + "\n")
    (root / "corpus" / "knowledge").mkdir(parents=True, exist_ok=True)
    rows = []
    for rid, snap, stmt, quote in SAMPLE_ROWS:
        sid = {"UL1": "S304", "UL2": "S304", "UL3": "S305",
               "UL4": "S305", "UL5": "S306", "UL6": "S306"}[rid]
        rows.append(f'| {rid} | {stmt} | source={sid} | snapshot={snap} | '
                    f'digest={digests[snap]} | quote="{quote}" |')
    (root / NOTE).write_text("# fixture note\n\n" + "\n".join(rows) + "\n")
    reg = ["# fixture registry", "", "| id | source | kind | tier | scope | anchor | teaches | "
           "status | opened | recheck | used-by |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for sid, (name, url, kind, anchor) in SAMPLE_SOURCES.items():
        reg.append(f"| {sid} | fixture {name} — {url} | {kind} | A | fixture scope | {anchor} "
                   f"| fixture lesson | mined | 2026-11-03 | on-release | — |")
    (root / REGISTRY).write_text("\n".join(reg) + "\n")
    if mutate:
        mutate(root)


def score_tree(root, out):
    return evaluate(*readers("HEAD", str(root)), out=out)


def selftest():
    tmp = os.environ.get("TMPDIR")
    if not tmp or not Path(tmp).is_dir():
        print("SELFTEST: FAIL (SELFTEST-TMPDIR) $TMPDIR names no directory", file=sys.stderr)
        return 2
    base = Path(tempfile.mkdtemp(prefix="ul-counter-selftest-", dir=tmp))
    if Path(tmp).resolve() == Path("/tmp"):
        shutil.rmtree(base, ignore_errors=True)
        print("SELFTEST: FAIL (SELFTEST-HERMETIC) TMPDIR is /tmp", file=sys.stderr)
        return 2
    cases = []

    def case(cid, mutate, expect_rc, expect_token):
        root = base / cid
        build_fixture(root, mutate)
        buf = io.StringIO()
        rc = score_tree(root, buf)
        text = buf.getvalue()
        ok = rc == expect_rc and (expect_token in text or expect_token == "")
        cases.append((cid, ok, rc, expect_token))
        print(f"{'PASS' if ok else 'FAIL'} (SELFTEST-{cid}) rc={rc} expect={expect_rc} "
              f"token={expect_token}")

    def edit(rel, old, new):
        def _m(root):
            p = root / rel
            t = p.read_text()
            assert old in t, f"mutation target absent: {old[:40]}"
            p.write_text(t.replace(old, new, 1))
        return _m

    def drop_row(root):
        p = root / NOTE
        lines = [l for l in p.read_text().splitlines() if not l.startswith("| UL6 |")]
        p.write_text("\n".join(lines) + "\n")

    def dup_row(root):
        p = root / NOTE
        lines = p.read_text().splitlines()
        lines = [l.replace("| UL6 |", "| UL5 |", 1) if l.startswith("| UL6 |") else l for l in lines]
        p.write_text("\n".join(lines) + "\n")

    def reuse_three(root):
        p = root / NOTE
        lines = []
        for l in p.read_text().splitlines():
            if l.startswith("| UL3 |"):
                l = l.replace("snapshot=unit.c", "snapshot=systemd.unit.xml")
            lines.append(l)
        p.write_text("\n".join(lines) + "\n")

    def malformed(root):
        p = root / NOTE
        p.write_text(p.read_text() + "| UL7 | junk row without the required cells |\n")

    case("CONTROL", None, 0, "UL_TARGET")
    case("SHORT", edit(NOTE, SAMPLE_ROWS[0][2], "Too short a statement"), 1, "statement-words")
    case("UNREGISTERED", edit(NOTE, "source=S306", "source=S999"), 1, "source-unregistered")
    case("QUOTE", edit(NOTE, "Unit %s is masked, ignoring.", "Unit %s is not masked at all."),
         1, "quote-absent")
    case("FIVE", drop_row, 1, "UL_ROWS=5")
    case("DUPID", dup_row, 1, "duplicate-id")
    case("REUSE", reuse_three, 1, "snapshot-reuse")
    case("UNGROUNDED",
         edit(NOTE, SAMPLE_ROWS[5][2],
              "Zebra quokka wombat xylophone nostril platypus marmalade truffle blizzard kumquat "
              "yonder zeppelin"),
         1, "statement-grounding")
    case("MALFORMED", malformed, 1, "malformed-row")
    def digest_swap(root):
        p = root / NOTE
        out = []
        for l in p.read_text().splitlines():
            if l.startswith("| UL5 |"):
                l = re.sub(r"digest=[0-9a-f]{64}", "digest=" + "0" * 64, l)
            out.append(l)
        p.write_text("\n".join(out) + "\n")

    case("DIGEST", digest_swap, 1, "digest-mismatch")
    case("OWNWORK", edit(REGISTRY, "| code | A | fixture scope | install.c at",
                         "| own-work | A | fixture scope | install.c at"),
         1, "source-kind")

    def empty_quote(root):
        p = root / NOTE
        out = []
        for l in p.read_text().splitlines():
            if l.startswith("| UL1 |"):
                l = re.sub(r'quote="[^"]*"', 'quote=""', l)
            out.append(l)
        p.write_text("\n".join(out) + "\n")

    case("EMPTYQUOTE", empty_quote, 1, "quote-words")

    def map_list(root):
        p = root / MAP
        p.write_text(json.dumps({"snapshots": ["not-a-map"]}) + "\n")

    case("MAPLIST", map_list, 1, "UL_MAP malformed")
    shutil.rmtree(base, ignore_errors=True)
    passed = sum(1 for c in cases if c[1])
    print(f"SELFTEST: {'PASS' if passed == len(cases) else 'FAIL'} "
          f"({len(cases)} cases, {passed} passed, {len(cases) - passed} failed)")
    return 0 if passed == len(cases) else 3


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--revision", default="HEAD")
    ap.add_argument("--fixture")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    return evaluate(*readers(args.revision, args.fixture))


if __name__ == "__main__":
    sys.exit(main())
