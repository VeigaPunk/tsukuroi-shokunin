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
import contextlib
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


# --- round-79 routed selftest (C2 item 2): hermetic, TMPDIR-bound, read-only ---
# The frozen evaluate/readers logic above is not modified; the selftest only
# drives it over synthetic fixture trees.
HARNESS_LINE = "HARNESS-TMPDIR-REFUSED"

_URLS = {"modprobe.conf": "https://example.com/r72/modprobe.json",
         "blacklist.conf": "https://example.com/r72/blacklist.json",
         "alsa.conf": "https://example.com/r72/alsa.json"}

_SNAP_MODPROBE = (
    "synthetic fixture snapshot one for the counter selftest\n"
    "the modprobe program reads configuration files from the etc directory\n"
    "and applies options to kernel modules while loading them on demand\n"
    "blacklisted modules are skipped during automatic loading\n"
    "install commands run external helpers when a module loads\n")
_SNAP_BLACKLIST = (
    "synthetic fixture snapshot two\n"
    "the blacklist entry prevents automatic module loading at boot time\n"
    "alias lines map device driver names onto alternative modules\n")
_SNAP_ALSA = (
    "synthetic fixture snapshot three\n"
    "sound hardware configuration stores card order and index options per module\n"
    "users pin slot assignments through the options line of the sound driver\n")
_LONG_SENTENCE = (
    "when the boot process reaches the stage where automatic module loading happens "
    "the helper reads every options line and then merges each requested parameter "
    "into the final module parameter set before the kernel starts the module")

_STMT1 = ("the modprobe program reads configuration files from the etc directory "
          "and applies options to kernel modules while loading them")
_STMT2 = ("blacklisted modules are skipped during automatic loading and "
          "install commands run external helpers")
_STMT3 = ("the blacklist entry prevents automatic module loading at boot time "
          "and alias lines map names")
_STMT4 = ("alias lines map device driver names onto alternative modules "
          "when automatic hardware detection runs")
_STMT5 = "sound hardware configuration stores card order and index options per loaded module"
_STMT6 = "users pin slot assignments through the options line of the sound driver"
_QUOTES = {
    1: "reads configuration files from the etc directory",
    2: "blacklisted modules are skipped during automatic loading",
    3: "prevents automatic module loading at boot time",
    4: "map device driver names onto alternative modules",
    5: "stores card order and index options per module",
    6: "pin slot assignments through the options line",
}


def selftest_root():
    """Private fixture root: an explicit TMPDIR, never unset, never under /tmp."""
    tmp = os.environ.get("TMPDIR")
    if not tmp:
        print(f"{HARNESS_LINE} reason=tmpdir-unset")
        return None
    real = os.path.realpath(tmp)
    if real == "/tmp" or real.startswith("/tmp/"):
        print(f"{HARNESS_LINE} reason=tmpdir-under-tmp")
        return None
    if not os.path.isdir(real):
        print(f"{HARNESS_LINE} reason=tmpdir-missing")
        return None
    return real


def _md_rows():
    return [
        {"n": 1, "stmt": _STMT1, "src": "S901", "snap": "modprobe.conf", "quote": _QUOTES[1]},
        {"n": 2, "stmt": _STMT2, "src": "S901", "snap": "modprobe.conf", "quote": _QUOTES[2]},
        {"n": 3, "stmt": _STMT3, "src": "S902", "snap": "blacklist.conf", "quote": _QUOTES[3]},
        {"n": 4, "stmt": _STMT4, "src": "S902", "snap": "blacklist.conf", "quote": _QUOTES[4]},
        {"n": 5, "stmt": _STMT5, "src": "S903", "snap": "alsa.conf", "quote": _QUOTES[5]},
        {"n": 6, "stmt": _STMT6, "src": "S903", "snap": "alsa.conf", "quote": _QUOTES[6]},
    ]


def _swap(idx, row):
    rows = _md_rows()
    rows[idx] = row
    return rows


def _render_row(row, raw):
    digest = row.get("digest") or raw.get(row["snap"], "0" * 64)
    return (f'| MD{row["n"]} | {row["stmt"]} | source={row["src"]} | '
            f'snapshot={row["snap"]} | digest={digest} | quote="{row["quote"]}" |')


def _md_fixture(rows=None, registry=None, snapshots=None, map_entries=None,
                map_text=None, note_extra=(), omit=()):
    """One synthetic mirror tree; each case mutates exactly one facet."""
    snaps = {"modprobe.conf": _SNAP_MODPROBE, "blacklist.conf": _SNAP_BLACKLIST,
             "alsa.conf": _SNAP_ALSA}
    if snapshots:
        snaps.update(snapshots)
    reg = {sid: [f"fixture source — {_URLS[name]}", "docs", f"{name} pinned snapshot"]
           for sid, name in (("S901", "modprobe.conf"), ("S902", "blacklist.conf"),
                             ("S903", "alsa.conf"))}
    if registry:
        for sid, patch in registry.items():
            row = reg.get(sid, ["", "docs", ""])
            for key, val in patch.items():
                row[{"source": 0, "kind": 1, "anchor": 2}[key]] = val
            reg[sid] = row
    raw = {name: hashlib.sha256(text.encode("utf-8")).hexdigest()
           for name, text in snaps.items()}
    entries = {name: {"sha256": raw[name], "url": _URLS[name]}
               for name in snaps}
    if map_entries:
        for name, patch in map_entries.items():
            slot = entries.setdefault(name, {})
            for key, val in patch.items():
                if val is None:
                    slot.pop(key, None)
                else:
                    slot[key] = val
    rows = _md_rows() if rows is None else rows
    note = ["# modprobe configuration plane — fixture note", ""]
    note += [_render_row(r, raw) for r in rows]
    note += list(note_extra)
    reglines = ["# SOURCES fixture", "",
                "| id | source | kind | tier | scope | anchor | teaches | status | "
                "opened | recheck | used-by |",
                "|---|---|---|---|---|---|---|---|---|---|---|"]
    for sid in sorted(reg):
        src, kind, anchor = reg[sid]
        reglines.append(f"| {sid} | {src} | {kind} | A | synthetic scope | {anchor} | "
                        "synthetic teaches cell | mined | 2026-11-04 | 90d | — |")
    files = {NOTE: "\n".join(note) + "\n", REGISTRY: "\n".join(reglines) + "\n",
             MAP: map_text if map_text is not None
                  else json.dumps({"snapshots": entries}, indent=1) + "\n"}
    for name, text in snaps.items():
        files[f"{SNAPDIR}/{name}"] = text
    for rel in omit:
        files.pop(rel, None)
    return files


def _write_tree(root, files):
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def run_selftest():
    """Fixture-tree selftest: one SELFTEST line per case, rc 0 all-pass, rc 3 any-fail."""
    root = selftest_root()
    if root is None:
        return 2
    work = Path(tempfile.mkdtemp(prefix="count-md-rows-r72-selftest-", dir=root))
    cases = []

    def case(name, files, want_rc, need, forbid=()):
        d = work / name
        d.mkdir(parents=True)
        _write_tree(d, files)
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                rc = evaluate(*readers(None, str(d)))
        except Exception as exc:  # a crashing case is a failing case, never a hang
            rc = None
            buf.write(f"case-exception: {type(exc).__name__}: {exc}\n")
        out = buf.getvalue()
        absent = [s for s in need if s not in out]
        present = [s for s in forbid if s in out]
        ok = rc == want_rc and not absent and not present
        cases.append(ok)
        print(f"SELFTEST {name} rc={rc} {'PASS' if ok else 'FAIL'}")
        if absent:
            print(f"  expected-but-absent: {absent}")
        if present:
            print(f"  forbidden-but-present: {present}")
        if not ok:
            for line in out.rstrip().splitlines():
                print(f"  | {line}")

    case("clean-pass", _md_fixture(), 0,
         ["MD_ROWS=6", "MD_VERIFIED=6", "met=1"], forbid=("fail",))
    case("note-absent", _md_fixture(omit=(NOTE,)), 128, ["MD_NOTE absent"])
    case("registry-absent", _md_fixture(omit=(REGISTRY,)), 128, ["MD_REGISTRY absent"])
    case("map-absent", _md_fixture(omit=(MAP,)), 128, ["MD_MAP absent"])
    case("map-malformed", _md_fixture(map_text="{not json"), 1, ["MD_MAP malformed"])
    case("malformed-row", _md_fixture(note_extra=("| MD9 | oops |",)), 1, ["malformed-row"])
    case("duplicate-id", _md_fixture(rows=_md_rows()[:5] + [dict(_md_rows()[0])]), 1,
         ["duplicate-id"])
    short = dict(_md_rows()[0])
    short["stmt"] = "too short this statement"
    case("statement-words", _md_fixture(rows=_swap(0, short)), 1, ["statement-words="])
    unground = dict(_md_rows()[0])
    unground["stmt"] = "alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo lima"
    case("statement-grounding", _md_fixture(rows=_swap(0, unground)), 1,
         ["statement-grounding=0/"])
    ghost = dict(_md_rows()[0])
    ghost["snap"] = "ghost.conf"
    case("snapshot-absent", _md_fixture(rows=_swap(0, ghost)), 1, ["snapshot-absent"])
    wrong_digest = dict(_md_rows()[0])
    wrong_digest["digest"] = "a" * 64
    case("digest-mismatch", _md_fixture(rows=_swap(0, wrong_digest)), 1, ["digest-mismatch"])
    case("map-digest", _md_fixture(map_entries={"modprobe.conf": {"sha256": "b" * 64}}), 1,
         ["map-digest"])
    case("map-url-absent", _md_fixture(map_entries={"modprobe.conf": {"url": None}}), 1,
         ["map-url"])
    no_quote = dict(_md_rows()[0])
    no_quote["quote"] = "words that appear nowhere in this snapshot"
    case("quote-absent", _md_fixture(rows=_swap(0, no_quote)), 1, ["quote-absent"])
    long_quote = dict(_md_rows()[1])
    long_quote["quote"] = _LONG_SENTENCE
    case("quote-words", _md_fixture(
        snapshots={"modprobe.conf": _SNAP_MODPROBE + _LONG_SENTENCE + "\n"},
        rows=_swap(1, long_quote)), 1, ["quote-words="])
    piped = dict(_md_rows()[1])
    piped["quote"] = "skipped | during automatic loading"
    case("quote-pipe-dead-branch", _md_fixture(rows=_swap(1, piped)), 1,
         ["malformed-row"], forbid=("quote-pipe",))
    unregistered = dict(_md_rows()[0])
    unregistered["src"] = "S999"
    case("source-unregistered", _md_fixture(rows=_swap(0, unregistered)), 1,
         ["source-unregistered"])
    case("source-kind-own-work", _md_fixture(registry={"S901": {"kind": "own-work"}}), 1,
         ["source-kind=own-work"])
    case("source-not-bound",
         _md_fixture(registry={"S901": {"source": "https://example.com/unbound.json"}}), 1,
         ["source-not-bound"])
    case("anchor-not-bound", _md_fixture(registry={"S901": {"anchor": "other.conf"}}), 1,
         ["anchor-not-bound"])
    seven = dict(_md_rows()[5])
    seven["n"] = 7
    case("ids-not-contiguous", _md_fixture(rows=_md_rows()[:5] + [seven]), 1,
         ["ids-not-contiguous"])
    reuse = {"n": 3, "stmt": _STMT2, "src": "S902", "snap": "modprobe.conf",
             "quote": _QUOTES[2]}
    case("snapshot-reuse",
         _md_fixture(rows=[_md_rows()[0], _md_rows()[1], reuse] + _md_rows()[3:]), 1,
         ["snapshot-reuse modprobe.conf=3"])
    variant = [_md_rows()[0], _md_rows()[2], _md_rows()[1],
               _md_rows()[4], _md_rows()[3], _md_rows()[5]]
    spaced = dict(variant[1])
    spaced["quote"] = "prevents   automatic module loading at boot time"
    variant[1] = spaced
    case("accepted-variant",
         _md_fixture(rows=variant,
                     note_extra=("", "prose between rows is ignored by the candidate scan", ""),
                     registry={"S901": {"anchor": "modprobe.conf (round-72 pinned snapshot)"}}),
         0, ["MD_ROWS=6", "MD_VERIFIED=6", "met=1"], forbid=("fail",))
    shutil.rmtree(work, ignore_errors=True)
    total, passed = len(cases), sum(cases)
    print(f"SELFTEST: {'PASS' if passed == total else 'FAIL'} "
          f"({total} cases, {passed} passed, {total - passed} failed)")
    return 0 if passed == total else 3


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--revision", default="HEAD")
    group.add_argument("--fixture")
    group.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return run_selftest()
    return evaluate(*readers(args.revision, args.fixture))


if __name__ == "__main__":
    sys.exit(main())
