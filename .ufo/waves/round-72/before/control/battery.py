#!/usr/bin/env python3
"""round-72 C1 pre-data battery: one well-formed control plus eleven mutants.

Builds fixture mirrors under $TMPDIR (default /fast/scratch/hyaku) and runs the frozen
counter with --fixture. The control must read met=1 rc 0; every mutant must read met=0 rc 1.
Creates and removes its own scratch root; no lane file is written.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
COUNTER = LANE / "tools/count-md-rows-r72.py"
SNAPDIR = ".ufo/waves/round-72/before/src"
BASE = "https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/"
SNAPURL = {
    "modprobe.d.5.scd": BASE + "man/modprobe.d.5.scd?h=v34",
    "libkmod-config.c": BASE + "libkmod/libkmod-config.c?h=v34",
    "modprobe.c": BASE + "tools/modprobe.c?h=v34",
}
SNAPS = list(SNAPURL)

ROWS = [
    ("Configuration directories are read in SYNOPSIS order of precedence: once a filename is "
     "loaded, the same name in subsequent directories is ignored",
     "S301", "modprobe.d.5.scd",
     "Once a file of a given filename is loaded, any file of the same name in subsequent directories is ignored."),
    ("Configuration files from every directory are sorted in one lexicographic order, so a "
     "configuration file ordered later partially replaces an earlier configuration file",
     "S301", "modprobe.d.5.scd",
     "All configuration files are sorted in lexicographic order, regardless of the directory they reside in."),
    ("conf_files_insert_sorted keeps one sorted list and returns EEXIST when strcmp reports a "
     "duplicate config file, so a later path copy is never parsed",
     "S302", "libkmod-config.c",
     "Ignoring duplicate config file: %s/%s\\n"),
    ("kmod_config_parse_kcmdline runs after the configuration files, so kernel command line "
     "module options land in the same config object",
     "S302", "libkmod-config.c",
     "kmod_config_parse_kcmdline(config);"),
    ("modprobe dry-run does not execute operations; it will print the install command "
     "instead of inserting the module",
     "S303", "modprobe.c",
     "Do not execute operations, just print out"),
    ("modprobe flags include APPLY_BLACKLIST_ALIAS_ONLY always, and APPLY_BLACKLIST only "
     "with use_blacklist, so a blacklisted module named explicitly is not refused",
     "S303", "modprobe.c",
     "Apply blacklist to resolved alias."),
]

REG = """# SOURCES — fixture registry (battery only)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S301 | kmod v34 modprobe.d(5) — {u1} | docs | A | fixture scope | tag v34; modprobe.d.5.scd lines 40-118 | fixture teaches | mined | 2026-11-03 | on-release | corpus/knowledge/modprobe-config-plane-r72.md |
| S302 | kmod v34 libkmod-config.c — {u2} | code | A | fixture scope | tag v34; libkmod-config.c lines 920-1085 | fixture teaches | mined | 2026-11-03 | on-release | corpus/knowledge/modprobe-config-plane-r72.md |
| S303 | kmod v34 tools/modprobe.c — {u3} | code | A | fixture scope | tag v34; modprobe.c lines 100-130 and 600-640 | fixture teaches | mined | 2026-11-03 | on-release | corpus/knowledge/modprobe-config-plane-r72.md |
"""


def build(root: Path, rows, kind_swap=None):
    src = root / SNAPDIR
    src.mkdir(parents=True)
    snapmap = {}
    for name in SNAPS:
        shutil.copyfile(LANE / SNAPDIR / name, src / name)
        digest = hashlib.sha256((src / name).read_bytes()).hexdigest()
        snapmap[name] = {"url": SNAPURL[name], "sha256": digest, "tag": "v34",
                         "accessed": "2026-11-03"}
    (src / "SOURCES.json").write_text(json.dumps({"snapshots": snapmap}, indent=1) + "\n")
    note = ["# fixture note", "", "| id | statement | source | snapshot | digest | quote |",
            "|---|---|---|---|---|---|"]
    for i, (stmt, sid, snap, quote) in enumerate(rows, 1):
        note.append(f'| MD{i} | {stmt} | source={sid} | snapshot={snap} | '
                    f'digest={snapmap.get(snap, {}).get("sha256", "0" * 64)} | quote="{quote}" |')
    (root / "corpus/knowledge").mkdir(parents=True)
    (root / "corpus/knowledge/modprobe-config-plane-r72.md").write_text("\n".join(note) + "\n")
    reg = REG.replace("{u1}", SNAPURL["modprobe.d.5.scd"]) \
             .replace("{u2}", SNAPURL["libkmod-config.c"]) \
             .replace("{u3}", SNAPURL["modprobe.c"])
    if kind_swap:
        reg = reg.replace(kind_swap[0], kind_swap[1], 1)
    (root / "corpus/SOURCES.md").write_text(reg)
    return snapmap


def run(fixture: Path):
    r = subprocess.run([sys.executable, str(COUNTER), "--fixture", str(fixture)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout


def main():
    base = Path(os.environ.get("TMPDIR", "/fast/scratch/hyaku")) / "md-battery-r72"
    shutil.rmtree(base, ignore_errors=True)
    base.mkdir(parents=True, exist_ok=True)
    cases = []
    try:
        ctrl = base / "control"
        build(ctrl, ROWS)
        cases.append(("control", ctrl, 0, "met=1"))

        def mut(name, rows, kind_swap=None):
            d = base / name
            build(d, rows, kind_swap)
            cases.append((name, d, 1, "met=0"))

        thin = list(ROWS)
        thin[0] = ("Configuration directories are read and files are ignored", thin[0][1],
                   thin[0][2], thin[0][3])
        mut("mutant-short-statement", thin)

        mut("mutant-source-unregistered",
            [(ROWS[0][0], "S999", ROWS[0][2], ROWS[0][3])] + ROWS[1:])

        mut("mutant-quote-absent",
            [(ROWS[0][0], ROWS[0][1], ROWS[0][2], "no such sentence in any snapshot at all")] + ROWS[1:])

        mut("mutant-five-rows", ROWS[:5])
        mut("mutant-duplicate-id", [ROWS[0], ROWS[1], ROWS[1], ROWS[3], ROWS[4], ROWS[5]])

        # R72-D5 amendment: a true in-place duplicate id (reuse stays at 2 per snapshot, so only
        # duplicate-id / ids-not-contiguous can fail). The original case above is killed by reuse.
        dup = base / "mutant-duplicate-id-true"
        build(dup, ROWS)
        dp = dup / "corpus/knowledge/modprobe-config-plane-r72.md"
        dp.write_text(dp.read_text().replace("| MD4 |", "| MD3 |", 1))
        cases.append(("mutant-duplicate-id-true", dup, 1, "met=0"))

        # three rows citing modprobe.d.5.scd (reuse 3 > 2)
        mut("mutant-snapshot-reuse",
            ROWS[:5] + [(ROWS[5][0], "S301", "modprobe.d.5.scd", ROWS[0][3])])

        gib = list(ROWS)
        gib[0] = ("Zzyzx quorbex flimwad gruppled snorxt vlimbo twerpish blorptastic "
                  "yonderflux quaintrix", gib[0][1], gib[0][2], gib[0][3])
        mut("mutant-ungrounded", gib)

        mal = base / "mutant-malformed-row"
        build(mal, ROWS)
        p = mal / "corpus/knowledge/modprobe-config-plane-r72.md"
        p.write_text(p.read_text() + "| MD7 | invisible broken row |\n")
        cases.append(("mutant-malformed-row", mal, 1, "met=0"))

        swap = base / "mutant-digest-swap"
        sm = build(swap, ROWS)
        p = swap / "corpus/knowledge/modprobe-config-plane-r72.md"
        p.write_text(p.read_text().replace(sm["modprobe.c"]["sha256"], "0" * 64, 1))
        cases.append(("mutant-digest-swap", swap, 1, "met=0"))

        mut("mutant-ownwork-kind", ROWS, ("| code | A |", "| own-work | A |"))

        passed = failed = 0
        for name, d, want_rc, want_tok in cases:
            rc, out = run(d)
            ok = rc == want_rc and want_tok in out
            passed += ok
            failed += not ok
            print(f"BATTERY {name}: rc={rc} want_rc={want_rc} {'PASS' if ok else 'FAIL'}")
            if not ok:
                print(out)
        print(f"BATTERY cases={len(cases)} passed={passed} failed={failed}")
        return 0 if failed == 0 else 1
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
