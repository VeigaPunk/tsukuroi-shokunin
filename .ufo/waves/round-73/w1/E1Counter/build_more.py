#!/usr/bin/env python3
"""E1Counter round-73: second attack battery against the frozen C1 counter.

Variants: empty quote (content-free), unanchored quote, duplicated row content,
registry row shadowing, and wholly fabricated snapshots with a self-consistent map.
Each variant is built from the same independent mirror; only the named clause differs.
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
BASE = OUT / "mirror"

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

ROW_RE = re.compile(
    r'^\| UL(?P<n>[0-9]+) \| (?P<stmt>[^|]+) \| source=(?P<src>S[0-9]{3,}) '
    r'\| snapshot=(?P<snap>[^ |]+) \| digest=(?P<digest>[0-9a-f]{64}) '
    r'\| quote="(?P<quote>[^"]*)" \|$')


def row_line(rid, snap, src, stmt, quote, digest=None):
    return (f'| {rid} | {stmt} | source={src} | snapshot={snap} | '
            f'digest={digest or DIG[snap]} | quote="{quote}" |')


def norm(s):
    return " ".join(s.split())


def base_rows():
    text = (BASE / NOTE).read_text()
    return [l for l in text.splitlines() if l.startswith("| UL")]


def clone(name):
    d = OUT / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(BASE, d)
    return d


def var_empty_quote():
    d = clone("iso-emptyquote")
    rows = base_rows()
    new = row_line("UL1", "systemd.unit.xml", "S304",
                   ROW_RE.match(rows[0]).group("stmt"), "")
    (d / NOTE).write_text((d / NOTE).read_text().replace(rows[0], new, 1))


def var_one_word_quote():
    d = clone("iso-onewordquote")
    rows = base_rows()
    new = row_line("UL1", "systemd.unit.xml", "S304",
                   ROW_RE.match(rows[0]).group("stmt"), "override")
    (d / NOTE).write_text((d / NOTE).read_text().replace(rows[0], new, 1))


def var_unanchored():
    d = clone("iso-unanchored")
    rows = base_rows()
    # statement stays about the load path; quote comes from the XML licence header line
    new = row_line("UL1", "systemd.unit.xml", "S304",
                   ROW_RE.match(rows[0]).group("stmt"),
                   "<!-- SPDX-License-Identifier: LGPL-2.1-or-later -->")
    (d / NOTE).write_text((d / NOTE).read_text().replace(rows[0], new, 1))


def var_dupecontent():
    d = clone("iso-dupecontent")
    rows = base_rows()
    m1 = ROW_RE.match(rows[0])
    dup = row_line("UL2", "systemd.unit.xml", "S304", m1.group("stmt"), m1.group("quote"))
    (d / NOTE).write_text((d / NOTE).read_text().replace(rows[1], dup, 1))


def var_shadow():
    d = clone("iso-shadow")
    reg = (d / REGISTRY).read_text()
    # corrupt the real S305 row's source cell, then append a later duplicate that carries the URL
    bad = re.sub(r'\| S305 \| mirror unit\.c — [^|]+ \|', '| S305 | mirror unit.c — no url |', reg)
    good = [l for l in reg.splitlines() if l.startswith("| S305 |")][0]
    (d / REGISTRY).write_text(bad + good + "\n")


FAB = {
    "systemd.unit.xml":
        "Fabricated load path paragraph. Fabricated unit files are loaded from a fabricated "
        "framework list, and an earlier fabricated directory overrides a fabricated later name. "
        "Fabricated drop-ins always merge in fabricated lexicographic order inside each fabricated "
        "directory.\n",
    "unit.c":
        "Fabricated reload paragraph. Fabricated loaded unit needs a fabricated reload when the "
        "recomputed fabricated path list differs from the stored fabricated values. Fabricated "
        "masked fragment path absent or empty keeps a fabricated null symlink masked. Broken\n",
    "install.c":
        "Fabricated mask paragraph. Fabricated mask writes a fabricated symlink at the fabricated "
        "unit name, choosing the fabricated runtime config directory otherwise. A fabricated "
        "Install alias whose target unit does not exist is reported dangling and ignored. Broken\n",
}

FAB_ROWS = [
    ("UL1", "systemd.unit.xml", "S304",
     "Fabricated unit files are loaded from a fabricated framework list, and an earlier fabricated "
     "directory overrides a fabricated later name",
     "Fabricated unit files are loaded from a fabricated framework list"),
    ("UL2", "systemd.unit.xml", "S304",
     "Fabricated drop-ins always merge in fabricated lexicographic order inside each fabricated "
     "directory",
     "Fabricated drop-ins always merge in fabricated lexicographic order"),
    ("UL3", "unit.c", "S305",
     "Fabricated loaded unit needs a fabricated reload when the recomputed fabricated path list "
     "differs from the stored fabricated values",
     "Fabricated loaded unit needs a fabricated reload when the recomputed fabricated path list "
     "differs"),
    ("UL4", "unit.c", "S305",
     "Fabricated masked fragment path absent or empty keeps a fabricated null symlink masked",
     "Fabricated masked fragment path absent or empty keeps a fabricated null symlink masked"),
    ("UL5", "install.c", "S306",
     "Fabricated mask writes a fabricated symlink at the fabricated unit name, choosing the "
     "fabricated runtime config directory otherwise",
     "Fabricated mask writes a fabricated symlink at the fabricated unit name"),
    ("UL6", "install.c", "S306",
     "A fabricated Install alias whose target unit does not exist is reported dangling and ignored",
     "A fabricated Install alias whose target unit does not exist is reported dangling and ignored"),
]
FAB_REG = {
    "S304": "docs", "S305": "code", "S306": "code",
}


def var_fabricated():
    d = clone("iso-fabricated declared-spec")
    src = d / SNAPDIR
    fdig = {}
    for n, text in FAB.items():
        (src / n).write_text(text)
        fdig[n] = hashlib.sha256(text.encode()).hexdigest()
    snaps = {n: {"url": URL[n], "sha256": fdig[n], "bytes": len(FAB[n])} for n in NAMES}
    (src / "SOURCES.json").write_text(
        json.dumps({"tag": "v262", "fetched": "2026-11-03", "snapshots": snaps}, indent=2) + "\n")
    rows = [row_line(*r, digest=fdig[r[1]]) for r in FAB_ROWS]
    (d / NOTE).write_text("# fabricated note\n\n" + "\n".join(rows) + "\n")


def var_declared_spec():
    """Score the wave spec's own six rows (w1/L1Entry/note.md, untracked, written this wave)."""
    d = clone("declared-spec")
    spec = LANE / ".ufo/waves/round-73/w1/L1Entry/note.md"
    rows = [l for l in spec.read_text().splitlines() if re.match(r"^\| UL[0-9]+ \|", l)]
    assert len(rows) == 6, len(rows)
    (d / NOTE).write_text("# declared spec rows\n\n" + "\n".join(rows) + "\n")


if __name__ == "__main__":
    assert (BASE / NOTE).is_file(), "run build_fixtures.py first"
    var_empty_quote()
    var_one_word_quote()
    var_unanchored()
    var_dupecontent()
    var_shadow()
    var_fabricated()
    var_declared_spec()
    print("built: iso-emptyquote iso-onewordquote iso-unanchored iso-dupecontent iso-shadow "
          "iso-fabricated declared-spec")
