#!/usr/bin/env python3
"""round-71 C1 pre-data battery: one well-formed control plus eleven mutants.

Builds fixture mirrors under $TMPDIR (default /fast/scratch/hyaku) and runs the frozen
counter with --fixture. The control must read met=1 rc 0; every mutant must read met=0 rc 1.
Creates and removes its own scratch root; no lane file is written.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
COUNTER = LANE / "tools/count-mp-rows-r71.py"
SNAPDIR = ".ufo/waves/round-71/before/src"
SNAPS = ["kernel-parameters.rst", "params.c", "moduleparam.h", "main.c"]
URL = ("https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/{}?h=v7.2.11")

ROWS = [
    ("module_param_sysfs_setup skips any kparam whose perm equals zero before add_sysfs_param, "
     "so an invisible parameter never gets a sysfs file",
     "S297", "params.c", "invisible parameters"),
    ("add_sysfs_param sets mattr attr mode from kp perm and registers param_attr_store only when "
     "S_IWUSR S_IWGRP or S_IWOTH is present",
     "S297", "params.c", "Do not allow runtime DAC changes to make param writable."),
    ("struct kernel_param_ops holds flags and optional set get callbacks where set returns zero "
     "or negative errno and get returns the length written or negative errno",
     "S298", "moduleparam.h", "Returns 0, or -errno.  arg is in kp->arg."),
    ("unknown_module_param_cb warns that an unknown parameter is ignored and returns zero, so a "
     "typo does not fail the load",
     "S299", "main.c", "unknown parameter '%s' ignored"),
    ("module_blacklist is a comma-separated core_param charp list and blacklisted prints pr_err "
     "refusing the named module",
     "S299", "main.c", "Module %s is blacklisted"),
    ("module parameters are set on the kernel command line with a module name prefix or through "
     "modprobe, and loadable modules reveal them under sys module parameters",
     "S300", "kernel-parameters.rst", "reveal their parameters in /sys/module/${modulename}/parameters/."),
]

REG = """# SOURCES — fixture registry (battery only)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S297 | Linux v7.2.11 kernel/params.c — {u_params} | code | A | fixture scope | tag v7.2.11; params.c lines 709-711 | fixture teaches | mined | 2026-11-04 | on-release | corpus/knowledge/module-parameter-plane-r71.md |
| S298 | Linux v7.2.11 include/linux/moduleparam.h — {u_modp} | code | A | fixture scope | tag v7.2.11; moduleparam.h lines 60-68 | fixture teaches | mined | 2026-11-04 | on-release | corpus/knowledge/module-parameter-plane-r71.md |
| S299 | Linux v7.2.11 kernel/module/main.c — {u_main} | code | A | fixture scope | tag v7.2.11; main.c lines 3390-3394 | fixture teaches | mined | 2026-11-04 | on-release | corpus/knowledge/module-parameter-plane-r71.md |
| S300 | Linux v7.2.11 Documentation/admin-guide/kernel-parameters.rst — {u_kp} | docs | A | fixture scope | tag v7.2.11; kernel-parameters.rst lines 20-37 | fixture teaches | mined | 2026-11-04 | on-release | corpus/knowledge/module-parameter-plane-r71.md |
"""


def build(root: Path):
    src = root / SNAPDIR
    src.mkdir(parents=True)
    snapmap = {}
    for name in SNAPS:
        shutil.copyfile(LANE / SNAPDIR / name, src / name)
        import hashlib
        digest = hashlib.sha256((src / name).read_bytes()).hexdigest()
        snapmap[name] = {"url": URL.format(
            {"params.c": "kernel/params.c", "moduleparam.h": "include/linux/moduleparam.h",
             "main.c": "kernel/module/main.c",
             "kernel-parameters.rst": "Documentation/admin-guide/kernel-parameters.rst"}[name]),
            "tag": "v7.2.11", "accessed": "2026-11-04", "sha256": digest}
    (src / "SOURCES.json").write_text(json.dumps({"snapshots": snapmap}, indent=1) + "\n")
    (root / "corpus/knowledge").mkdir(parents=True)
    (root / "corpus/SOURCES.md").write_text(REG.format(
        u_params=snapmap["params.c"]["url"], u_modp=snapmap["moduleparam.h"]["url"],
        u_main=snapmap["main.c"]["url"], u_kp=snapmap["kernel-parameters.rst"]["url"]))
    return snapmap


def note_text(snapmap, rows):
    out = ["# fixture note (battery only)", ""]
    for i, (stmt, src, snap, quote) in enumerate(rows, 1):
        out.append(f'| MP{i} | {stmt} | source={src} | snapshot={snap} | '
                   f'digest={snapmap[snap]["sha256"]} | quote="{quote}" |')
    return "\n".join(out) + "\n"


def run(fixture: Path):
    r = subprocess.run([sys.executable, str(COUNTER), "--fixture", str(fixture)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main():
    base = Path(os.environ.get("TMPDIR") or "/fast/scratch/hyaku") / "tsukuroi-r71-battery"
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    cases = []

    def case(name, rows, want_rc):
        root = base / name
        snapmap = build(root)
        (root / "corpus/knowledge/module-parameter-plane-r71.md").write_text(note_text(snapmap, rows))
        rc, out = run(root)
        ok = rc == want_rc
        met = "met=1" if "met=1" in out else "met=0"
        cases.append((name, ok, rc, want_rc, met))
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: rc={rc} want={want_rc} {met}")
        print("    " + " | ".join(l for l in out.splitlines() if l.startswith("MP_")))

    case("control", ROWS, 0)

    r = list(ROWS)
    r[0] = ("the quick brown fox jumps over the lazy dog while nonsense words fill the rest of "
            "this statement", *ROWS[0][1:])
    case("mutant-content-free", r, 1)

    r = list(ROWS)
    r[0] = (ROWS[0][0], "S298", *ROWS[0][2:])
    case("mutant-source-unbound", r, 1)

    r = list(ROWS)
    r[1] = (ROWS[1][0], ROWS[1][1], ROWS[1][2],
            "quote text that is absent from the snapshot file")
    case("mutant-quote-absent", r, 1)

    r = list(ROWS)
    r[2] = ("too short a statement", *ROWS[2][1:])
    case("mutant-short-statement", r, 1)

    case("mutant-five-rows", ROWS[:5], 1)

    r = list(ROWS)
    r[5] = (ROWS[5][0], ROWS[5][1], ROWS[5][2], ROWS[5][3])
    r.append(ROWS[0])
    case("mutant-duplicate-id", r, 1)

    r = list(ROWS)
    r[3] = (ROWS[1][0], "S297", "params.c", "invisible parameters")
    case("mutant-snapshot-reuse", r, 1)

    r = list(ROWS)
    r[3] = ("the quick brown fox jumps over the lazy dog while nonsense words fill the rest of "
            "this statement", *ROWS[3][1:])
    case("mutant-ungrounded", r, 1)

    # malformed (invisible) row appended after the control rows
    root = base / "mutant-malformed-row"
    snapmap = build(root)
    (root / "corpus/knowledge/module-parameter-plane-r71.md").write_text(
        note_text(snapmap, ROWS) + '|MP7| short | source=S297 | snapshot=params.c | digest=0 | quote="x" |\n')
    rc, out = run(root)
    ok = rc == 1
    cases.append(("mutant-malformed-row", ok, rc, 1, "met=1" if "met=1" in out else "met=0"))
    print(f"[{'PASS' if ok else 'FAIL'}] mutant-malformed-row: rc={rc} want=1")
    print("    " + " | ".join(l for l in out.splitlines() if l.startswith("MP_")))

    # digest swap: valid hex, wrong for the snapshot
    r = list(ROWS)
    root = base / "mutant-digest-swap"
    snapmap = build(root)
    text = note_text(snapmap, ROWS).replace(snapmap["params.c"]["sha256"], "0" * 64, 1)
    (root / "corpus/knowledge/module-parameter-plane-r71.md").write_text(text)
    rc, out = run(root)
    ok = rc == 1
    cases.append(("mutant-digest-swap", ok, rc, 1, "met=1" if "met=1" in out else "met=0"))
    print(f"[{'PASS' if ok else 'FAIL'}] mutant-digest-swap: rc={rc} want=1")
    print("    " + " | ".join(l for l in out.splitlines() if l.startswith("MP_")))

    passed = sum(1 for c in cases if c[1])
    print(f"\nBATTERY cases={len(cases)} passed={passed} failed={len(cases) - passed}")
    shutil.rmtree(base, ignore_errors=True)
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
