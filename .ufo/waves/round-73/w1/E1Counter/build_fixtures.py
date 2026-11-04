#!/usr/bin/env python3
"""E1Counter round-73: build independent mirror + isolation fixtures for the frozen C1 counter.

Rows here are written by this seat from the pinned v262 snapshots; no row is copied from the
tool's SAMPLE_ROWS. Every quote is asserted verbatim (whitespace-normalized) in its snapshot
before the fixture is written.
"""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
SRC = LANE / ".ufo/waves/round-73/before/src"
OUT = Path(sys.argv[1]).resolve()

SNAPDIR = ".ufo/waves/round-73/before/src"
NOTE = "corpus/knowledge/systemd-unit-load-plane-r73.md"
REGISTRY = "corpus/SOURCES.md"
MAP = SNAPDIR + "/SOURCES.json"

NAMES = ("systemd.unit.xml", "unit.c", "install.c")
DIG = {n: hashlib.sha256((SRC / n).read_bytes()).hexdigest() for n in NAMES}
URL = {
    "systemd.unit.xml": "https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml",
    "unit.c": "https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c",
    "install.c": "https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/install.c",
}
REG = {
    "S304": ("systemd.unit.xml", "docs",
             "snapshot .ufo/waves/round-73/before/src/systemd.unit.xml lines 369-378 unit load "
             "path and 226-239 drop-in precedence"),
    "S305": ("unit.c", "code",
             "snapshot .ufo/waves/round-73/before/src/unit.c lines 3860-3915 reload freshness and "
             "687-718 dropin path removal"),
    "S306": ("install.c", "code",
             "snapshot .ufo/waves/round-73/before/src/install.c lines 2350-2390 mask symlink and "
             "340-355 install change log"),
}

# (id, snapshot, source, statement, quote) — this seat's own reading of the pinned files.
ROWS = [
    ("UL1", "systemd.unit.xml", "S304",
     "Unit files are loaded from a compilation-time path list, and a unit file found in an "
     "earlier directory overrides the same name lower in the list",
     "Unit files are loaded from a set of paths determined during compilation, described in the "
     "two tables below."),
    ("UL2", "systemd.unit.xml", "S304",
     "Setting the SYSTEMD_UNIT_PATH variable overrides the compiled unit load path entirely, "
     "while a trailing colon appends the usual unit load path to the variable contents",
     "the contents of this variable overrides the unit load path"),
    ("UL3", "unit.c", "S305",
     "A loaded unit needs a daemon reload when the recomputed set of drop-ins differs from the "
     "stored path list, or when a recorded drop-in file is newer than the reload timestamp",
     "if (!strv_equal(u->dropin_paths, dropins))"),
    ("UL4", "unit.c", "S305",
     "A masked unit stays fresh while the null or empty test on the fragment path holds, so a "
     "zero-size mask file and a dev null symlink keep the masked state until the path changes",
     "return !null_or_empty(&st);"),
    ("UL5", "install.c", "S306",
     "The mask operation writes a dev null symlink at the unit name, choosing the runtime config "
     "directory when the runtime flag is set and the persistent config directory otherwise",
     "config_path = (flags & UNIT_FILE_RUNTIME) ? lp.runtime_config : lp.persistent_config;"),
    ("UL6", "install.c", "S306",
     "An Install alias whose target unit does not exist is reported as a dangling install change "
     "and ignored, so enable never creates the alias symlink",
     "case INSTALL_CHANGE_IS_DANGLING:"),
]

ROW_RE = re.compile(
    r'^\| UL(?P<n>[0-9]+) \| (?P<stmt>[^|]+) \| source=(?P<src>S[0-9]{3,}) '
    r'\| snapshot=(?P<snap>[^ |]+) \| digest=(?P<digest>[0-9a-f]{64}) '
    r'\| quote="(?P<quote>[^"]*)" \|$')


def norm(s):
    return " ".join(s.split())


def read(name):
    return (SRC / name).read_text(encoding="utf-8", errors="replace")


def row_line(rid, snap, src, stmt, quote, digest=None):
    assert "|" not in stmt and "|" not in quote and '"' not in quote, rid
    return (f'| {rid} | {stmt} | source={src} | snapshot={snap} | '
            f'digest={digest or DIG[snap]} | quote="{quote}" |')


def note_text(rows):
    return "# round-73 C1 note (E1Counter independent mirror)\n\n" + "\n".join(rows) + "\n"


def registry_text(kinds=None):
    kinds = kinds or {}
    out = ["# SOURCES — fixture mirror (E1Counter)",
           "",
           "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | "
           "used-by |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for sid, (name, kind, anchor) in REG.items():
        out.append(f"| {sid} | mirror {name} — {URL[name]} | {kinds.get(sid, kind)} | A | "
                   f"fixture mirror of the committed snapshot | {anchor} | mirror lesson | mined "
                   f"| 2026-11-03 | on-release | — |")
    return "\n".join(out) + "\n"


def map_text(mut=None):
    snaps = {n: {"url": URL[n], "sha256": DIG[n], "bytes": (SRC / n).stat().st_size}
             for n in NAMES}
    if mut:
        mut(snaps)
    return json.dumps({"tag": "v262", "fetched": "2026-11-03", "snapshots": snaps},
                      indent=2) + "\n"


def write_tree(root, rows, kinds=None, map_mut=None, files=None, registry=None):
    root = Path(root)
    src = root / SNAPDIR
    src.mkdir(parents=True, exist_ok=True)
    for n in NAMES:
        (src / n).write_bytes((SRC / n).read_bytes() if not files or n not in files
                              else files[n])
    (src / "SOURCES.json").write_text(map_text(map_mut))
    (root / "corpus/knowledge").mkdir(parents=True, exist_ok=True)
    (root / NOTE).write_text(note_text(rows))
    (root / REGISTRY).write_text(registry if registry is not None else registry_text(kinds))


def verify_rows(rows):
    for line in rows:
        m = ROW_RE.match(line)
        assert m, f"row does not parse: {line[:60]}"
        assert line.count("|") == 7, line[:60]
        snap = m.group("snap")
        assert norm(m.group("quote")) in norm(read(snap)), f"quote not verbatim: {snap}"
        assert len(m.group("quote").split()) <= 25, "quote too long"
        assert m.group("digest") == DIG[snap]


def base_rows():
    rows = [row_line(*r) for r in ROWS]
    verify_rows(rows)
    return rows


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    rows = base_rows()
    base = OUT / "mirror"
    write_tree(base, rows)
    made = ["mirror"]

    def var(name, mutate):
        d = OUT / name
        shutil.copytree(base, d)
        mutate(d)
        made.append(name)

    # --- clause isolation -------------------------------------------------
    def iso_id(d):
        p = d / NOTE
        p.write_text(p.read_text().replace("| UL6 |", "| UL7 |", 1))

    def iso_words(d):
        p = d / NOTE
        new = row_line("UL1", "systemd.unit.xml", "S304",
                       "Unit files loaded from compilation path override name",
                       ROWS[0][4])
        p.write_text(p.read_text().replace(rows[0], new, 1))

    def iso_ground(d):
        p = d / NOTE
        new = row_line("UL1", "systemd.unit.xml", "S304",
                       "Zebra quokka wombat xylophone nostril platypus marmalade truffle blizzard "
                       "kumquat yonder zeppelin flagon",
                       ROWS[0][4])
        p.write_text(p.read_text().replace(rows[0], new, 1))

    def iso_kind(d):
        (d / REGISTRY).write_text(registry_text(kinds={"S306": "own-work"}))

    def iso_digest(d):
        p = d / SNAPDIR / "unit.c"
        p.write_bytes(p.read_bytes() + b"\n")

    def iso_mapdigest(d):
        p = d / MAP
        data = json.loads(p.read_text())
        data["snapshots"]["unit.c"]["sha256"] = "0" * 64
        p.write_text(json.dumps(data, indent=2) + "\n")

    def iso_mapurl(d):
        t = (d / REGISTRY).read_text().replace(URL["unit.c"], "mirror unit.c")
        (d / REGISTRY).write_text(t)

    def iso_anchor(d):
        t = (d / REGISTRY).read_text().replace("install.c lines 2350-2390", "mask symlink")
        (d / REGISTRY).write_text(t)

    def iso_quote_loc(d):
        p = d / NOTE
        new = row_line("UL2", "systemd.unit.xml", "S304", ROWS[1][3],
                       "the contents of this variable replaces the unit load path")
        p.write_text(p.read_text().replace(rows[1], new, 1))

    LONG_QUOTE = ("from this directory will be merged in the alphanumeric order and parsed after "
                  "the main unit file itself has been parsed. This is useful to alter or add "
                  "configuration settings for a unit, without having to modify unit files. Each "
                  "drop-in file must contain appropriate")

    def iso_quote_len(d):
        p = d / NOTE
        new = row_line("UL1", "systemd.unit.xml", "S304", ROWS[0][3], LONG_QUOTE)
        p.write_text(p.read_text().replace(rows[0], new, 1))

    UL3B = ("UL3", "systemd.unit.xml", "S304",
            "Equally named drop-in files located further down the truncated prefix hierarchy "
            "override those from a shallower prefix, so foo-bar-.service.d overrides "
            "foo-.service.d",
            "Note that equally named drop-in files further down the prefix hierarchy override "
            "those further up")

    def iso_reuse(d):
        rows2 = [row_line(*UL3B) if r.startswith("| UL3 |") else r for r in rows]
        verify_rows([row_line(*UL3B)])
        (d / NOTE).write_text(note_text(rows2))

    # --- blind spot: same tokens, negated statement -----------------------
    def blind_negate(d):
        p = d / NOTE
        new = row_line("UL1", "systemd.unit.xml", "S304",
                       ROWS[0][3].replace("earlier directory overrides",
                                          "earlier directory never overrides"),
                       ROWS[0][4])
        p.write_text(p.read_text().replace(rows[0], new, 1))

    var("iso-id", iso_id)
    var("iso-words", iso_words)
    var("iso-ground", iso_ground)
    var("iso-kind", iso_kind)
    var("iso-digest", iso_digest)
    var("iso-mapdigest", iso_mapdigest)
    var("iso-mapurl", iso_mapurl)
    var("iso-anchor", iso_anchor)
    var("iso-quote-loc", iso_quote_loc)
    var("iso-quote-len", iso_quote_len)
    var("iso-reuse", iso_reuse)
    var("blind-negate", blind_negate)

    # --- scripted non-reader control --------------------------------------
    scripted = OUT / "scripted"
    write_tree(scripted, base_rows())  # scaffolding only; rows replaced below
    srows, picks = [], []
    per = [("systemd.unit.xml", "S304", 0), ("systemd.unit.xml", "S304", 1),
           ("unit.c", "S305", 0), ("unit.c", "S305", 1),
           ("install.c", "S306", 0), ("install.c", "S306", 1)]
    for i, (snap, src, which) in enumerate(per, start=1):
        text = read(snap)
        candidates = []
        for line in text.splitlines():
            n = norm(line)
            if 4 <= len(n.split()) <= 24 and "|" not in n and '"' not in n:
                candidates.append(n)
        quote = candidates[which]
        toks, seen = [], set()
        for tok in re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", text):
            t = tok.lower()
            if len(t) >= 5 and t not in seen:
                seen.add(t)
                toks.append(t)
        block = toks[which * 16:(which + 1) * 16]
        stmt = " ".join(block)
        srows.append(row_line(f"UL{i}", snap, src, stmt, quote))
        picks.append((f"UL{i}", snap, which, quote[:60], len(stmt.split())))
    verify_rows(srows)
    (scripted / NOTE).write_text(note_text(srows))
    made.append("scripted")
    return made, picks


if __name__ == "__main__":
    made, picks = build()
    print("built:", " ".join(made))
    print("scripted picks (row, snapshot, candidate index, quote head, statement words):")
    for p in picks:
        print("  ", p)
