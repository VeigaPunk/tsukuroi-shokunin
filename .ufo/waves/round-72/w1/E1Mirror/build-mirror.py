#!/usr/bin/env python3
"""E1Mirror fixture builder: copy the three committed round-72 snapshots into a
mirror root and write a six-row MD note plus a three-row registry.

Usage: build-mirror.py <root>
Creates (and replaces) <root>/.ufo/waves/round-72/before/src,
<root>/corpus/SOURCES.md and <root>/corpus/knowledge/modprobe-config-plane-r72.md.
Writes nothing outside <root>.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
SNAPDIR = ".ufo/waves/round-72/before/src"
BASE = "https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/"
SNAPURL = {
    "modprobe.d.5.scd": BASE + "man/modprobe.d.5.scd?h=v34",
    "libkmod-config.c": BASE + "libkmod/libkmod-config.c?h=v34",
    "modprobe.c": BASE + "tools/modprobe.c?h=v34",
}
SNAPS = list(SNAPURL)

# (statement, source id, snapshot name, verbatim quote <= 25 words)
ROWS = [
    ("Configuration directories are read in SYNOPSIS precedence order; once a filename is "
     "loaded, the same name in subsequent directories is ignored.",
     "S301", "modprobe.d.5.scd",
     "Configuration files are read from directories in listed in SYNOPSIS in that order of precedence."),
    ("Configuration files can either be completely replaced by a new configuration file with "
     "the same name in a directory of higher priority, or partially replaced by a configuration "
     "file that is ordered later.",
     "S301", "modprobe.d.5.scd",
     "Configuration files can either be completely replaced (by having a new configuration file "
     "with the same name in a directory of higher priority)"),
    ("conf_files_insert_sorted stops at a sorted position and returns EEXIST on a strcmp "
     "duplicate, so the later directory copy is never parsed.",
     "S302", "libkmod-config.c",
     "Ignoring duplicate config file: %s/%s"),
    ("kmod_config_parse_kcmdline is called after every configuration file is parsed, so kernel "
     "command line options land in the same config object.",
     "S302", "libkmod-config.c",
     "kmod_config_parse_kcmdline(config);"),
    ("When dry_run is set, modprobe will print the insert operations and execute nothing "
     "instead.",
     "S303", "modprobe.c",
     "Do not execute operations, just print out"),
    ("By default modprobe flags the blacklist by resolved alias only; use_blacklist adds the "
     "unconditional apply, so a blacklisted module argument is inserted regardless.",
     "S303", "modprobe.c",
     "Apply blacklist to resolved alias."),
]

REG = """# SOURCES — E1Mirror fixture registry (mirror only)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S301 | kmod v34 modprobe.d(5) — {u1} | docs | A | fixture scope | tag v34; modprobe.d.5.scd lines 40-118 | fixture teaches | mined | 2026-11-03 | on-release | corpus/knowledge/modprobe-config-plane-r72.md |
| S302 | kmod v34 libkmod-config.c — {u2} | code | A | fixture scope | tag v34; libkmod-config.c lines 920-1085 | fixture teaches | mined | 2026-11-03 | on-release | corpus/knowledge/modprobe-config-plane-r72.md |
| S303 | kmod v34 tools/modprobe.c — {u3} | code | A | fixture scope | tag v34; modprobe.c lines 100-130 and 600-640 | fixture teaches | mined | 2026-11-03 | on-release | corpus/knowledge/modprobe-config-plane-r72.md |
"""


def build(root: Path):
    src = root / SNAPDIR
    src.mkdir(parents=True, exist_ok=True)
    snapmap = {}
    for name in SNAPS:
        data = (LANE / SNAPDIR / name).read_bytes()
        (src / name).write_bytes(data)
        snapmap[name] = {"url": SNAPURL[name], "sha256": hashlib.sha256(data).hexdigest(),
                         "tag": "v34", "accessed": "2026-11-03"}
    (src / "SOURCES.json").write_text(json.dumps({"snapshots": snapmap}, indent=1) + "\n")

    note = ["# modprobe configuration plane — E1Mirror fixture note", "",
            "| id | statement | source | snapshot | digest | quote |",
            "|---|---|---|---|---|---|"]
    for i, (stmt, sid, snap, quote) in enumerate(ROWS, 1):
        note.append(f'| MD{i} | {stmt} | source={sid} | snapshot={snap} | '
                    f'digest={snapmap[snap]["sha256"]} | quote="{quote}" |')
    (root / "corpus/knowledge").mkdir(parents=True, exist_ok=True)
    (root / "corpus/knowledge/modprobe-config-plane-r72.md").write_text("\n".join(note) + "\n")

    reg = REG.replace("{u1}", SNAPURL["modprobe.d.5.scd"]) \
             .replace("{u2}", SNAPURL["libkmod-config.c"]) \
             .replace("{u3}", SNAPURL["modprobe.c"])
    (root / "corpus/SOURCES.md").write_text(reg)
    return snapmap


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[0])
        return 2
    root = Path(sys.argv[1])
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True, exist_ok=True)
    snap = build(root)
    note = root / "corpus/knowledge/modprobe-config-plane-r72.md"
    print(f"BUILD root={root}")
    for name in SNAPS:
        print(f"BUILD snapshot={name} sha256={snap[name]['sha256']} url={snap[name]['url']}")
    print(f"BUILD note={note} lines={len(note.read_text().splitlines())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
