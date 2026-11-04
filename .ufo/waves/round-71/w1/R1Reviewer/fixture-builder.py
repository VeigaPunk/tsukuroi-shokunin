#!/usr/bin/env python3
"""Build C1 fixtures (base + mutants), run MY checker and the lane counter on each,
and emit a row-by-row verdict diff. Fixture mirror layout only; no lane writes."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/tsukuroi-r71/R1Reviewer")
FIX = S / "fix"
OUT = S / "out"
CLONE = S / "clone"
SNAPSRC = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-71/before/src")
LANE_COUNTER = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/count-mp-rows-r71.py"
MY_CHECKER = S / "check_c1.py"
REV = "0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e"

SNAPS = ["params.c", "moduleparam.h", "main.c", "kernel-parameters.rst"]
URLS = {
    "params.c": "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/kernel/params.c?h=v7.2.11",
    "moduleparam.h": "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/include/linux/moduleparam.h?h=v7.2.11",
    "main.c": "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/kernel/module/main.c?h=v7.2.11",
    "kernel-parameters.rst": "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/kernel-parameters.rst?h=v7.2.11",
}
DIGESTS = {
    "params.c": "923610d5de631d8b8dddcb89bf4b0f6932fb0dbf1f500d07453ea0b73b3782a4",
    "moduleparam.h": "220f2dac723a7b080211791a33cb3308ed12eaeb2309747232786d786cd14846",
    "main.c": "e1e1a1c8a13f3d5e402bb8773b4aea3561dadcdca446b3dfb0482b0ddcb95929",
    "kernel-parameters.rst": "45587d8e411db06dc600550f03236d3b7cbe7ad5bd898dbb9f965934ecd88799",
}
SRC_ID = {"params.c": "S297", "moduleparam.h": "S298", "main.c": "S299",
          "kernel-parameters.rst": "S300"}

STMT = {
    1: "The module_param_sysfs_setup support adds entries through add_sysfs_param, but skips kparam entries with zero perm before allocating the parameters array.",
    2: "Runtime DAC changes cannot make param writable: attr mode takes perm, while param_attr_store needs a write bit and otherwise store stays NULL.",
    3: "Each parameter ops struct records how its callbacks behave: setting returns zero or a negative errno, getting returns the length written, and freeing stays optional.",
    4: "An unknown parameter name is warned about and then ignored, so a misspelled parameter never fails the module load on its own.",
    5: "The module_blacklist option carries a comma-separated list of module names, and the loader refuses to load a module whose name appears there.",
    6: "Module parameters can be supplied in two ways: with a module name prefix on the kernel command line, or through the modprobe command line without any prefix.",
}
QUOTE = {
    1: "if (kparam[i].perm == 0) continue;",
    2: "mk->mp->attrs[mk->mp->num - 1].mattr.attr.mode = kp->perm;",
    3: "Returns 0, or -errno.",
    4: "unknown parameter '%s' ignored",
    5: "module_blacklist is a comma-separated list of module names",
    6: "Module parameters can be specified in two ways: via the kernel command line with a module name prefix, or via modprobe, e.g.::",
}
SNAP_OF = {1: "params.c", 2: "params.c", 3: "moduleparam.h", 4: "main.c",
           5: "main.c", 6: "kernel-parameters.rst"}

NOTE_INTRO = """# The kernel module-parameter plane

Notes on how Linux module parameters reach sysfs and the command line, read from
the pinned v7.2.11 sources.

"""


def norm(s):
    return " ".join(s.split())


def row_text(n, stmt=None, snap=None, digest=None, quote=None, src=None, mid="MP"):
    snap = snap or SNAP_OF[n]
    digest = digest or DIGESTS[snap]
    src = src or SRC_ID[snap]
    return (f"| {mid}{n} | {stmt or STMT[n]} | source={src} | snapshot={snap} "
            f"| digest={digest} | quote=\"{quote or QUOTE[n]}\" |")


def registry_extra(anchor_over=None, source_over=None):
    anchor_over = anchor_over or {}
    source_over = source_over or {}

    def regrow(sid, path, desc):
        url = URLS[path]
        source = source_over.get(sid, f"{path} at Linux v7.2.11 — {url}")
        anchor = anchor_over.get(sid, f"pinned snapshot .ufo/waves/round-71/before/src/{path}, tag v7.2.11, accessed 2026-11-04")
        return f"| {sid} | {source} | code | A | {desc} | {anchor} | retained |"
    return "\n".join([
        regrow("S297", "params.c", "The parameter sysfs exposure and store dispatch implementation behind the C1 rules"),
        regrow("S298", "moduleparam.h", "The kernel_param_ops contract definition site behind the C1 rules"),
        regrow("S299", "main.c", "The loader side unknown parameter handling and module_blacklist behind the C1 rules"),
        regrow("S300", "kernel-parameters.rst", "The specification routes for module parameters behind the C1 rules"),
    ])


def build_tree(name, note_text, registry_text, map_over=None):
    root = FIX / name
    if root.exists():
        shutil.rmtree(root)
    (root / "corpus/knowledge").mkdir(parents=True)
    (root / "corpus").mkdir(parents=True, exist_ok=True)
    src = root / ".ufo/waves/round-71/before/src"
    src.mkdir(parents=True)
    (root / "corpus/knowledge/module-parameter-plane-r71.md").write_text(note_text)
    (root / "corpus/SOURCES.md").write_text(registry_text)
    for s in SNAPS:
        shutil.copy2(SNAPSRC / s, src / s)
    shutil.copy2(SNAPSRC / "SHA256SUMS", src / "SHA256SUMS")
    mapj = json.loads((SNAPSRC / "SOURCES.json").read_text())
    if map_over:
        for k, v in map_over.items():
            mapj["snapshots"][k]["sha256"] = v
    (src / "SOURCES.json").write_text(json.dumps(mapj, indent=1))
    return root


def main():
    OUT.mkdir(exist_ok=True)
    base_reg = subprocess.run(["git", "-C", str(CLONE), "show", f"{REV}:corpus/SOURCES.md"],
                              capture_output=True, text=True, check=True).stdout
    reg_full = base_reg.rstrip("\n") + "\n" + registry_extra() + "\n"

    # verify quotes are located verbatim in the real snapshots (normalized)
    snap_text = {s: (SNAPSRC / s).read_text(errors="replace") for s in SNAPS}
    for n, q in QUOTE.items():
        assert norm(q) in norm(snap_text[SNAP_OF[n]]), f"quote MP{n} not in snapshot"

    base_note = NOTE_INTRO + "\n".join(row_text(n) for n in range(1, 7)) + "\n"
    fixtures = {"base": (base_note, reg_full, None)}

    def note_with_rows(rows):
        return NOTE_INTRO + "\n".join(rows) + "\n"

    base_rows = [row_text(n) for n in range(1, 7)]

    def rows_variant(overrides=None):
        # overrides: {n: dict(stmt=..., quote=..., digest=..., snap=..., src=..., mid=...)}
        out = []
        for n in range(1, 7):
            over = (overrides or {}).get(n, {})
            out.append(row_text(n, **over))
        return out

    fixtures["m01_short_stmt"] = (note_with_rows(rows_variant({
        1: {"stmt": "Skipped when perm is zero."}})), reg_full, None)
    fixtures["m02_ungrounded"] = (note_with_rows(rows_variant({
        2: {"stmt": "Velvet barnacles negotiate paradigm umbrellas whenever lantern castles juggle quantum marbles quickly."}})), reg_full, None)
    fixtures["m03_digest_swap"] = (note_with_rows(rows_variant({
        3: {"digest": DIGESTS["params.c"]}})), reg_full, None)
    fixtures["m04_quote_absent"] = (note_with_rows(rows_variant({
        4: {"quote": "unknown parameter never ignored"}})), reg_full, None)
    long_quote = ("/* module_blacklist is a comma-separated list of module names */ static char "
                  "*module_blacklist; static bool blacklisted(const char *module_name) { "
                  "const char *p; size_t len; if (!module_blacklist) return false;")
    assert norm(long_quote) in norm(snap_text["main.c"])
    fixtures["m05_quote_long"] = (note_with_rows(rows_variant({5: {"quote": long_quote}})), reg_full, None)
    fixtures["m06_extra_cell"] = (note_with_rows(
        [base_rows[0].replace(' | quote="', ' | tag=extra | quote="')] + base_rows[1:]), reg_full, None)
    # ids 1,2,3,3,5,6: replace row4 id with 3
    dup = base_rows[:3] + [base_rows[3].replace("| MP4 |", "| MP3 |")] + base_rows[4:]
    fixtures["m07_duplicate_id"] = (note_with_rows(dup), reg_full, None)
    noncont = base_rows[:4] + [base_rows[4].replace("| MP5 |", "| MP6 |"),
                               base_rows[5].replace("| MP6 |", "| MP7 |")]
    fixtures["m08_noncontiguous"] = (note_with_rows(noncont), reg_full, None)
    fixtures["m09_source_unregistered"] = (note_with_rows(rows_variant({1: {"src": "S999"}})), reg_full, None)
    reuse3 = rows_variant({3: {"snap": "params.c", "src": "S297"}})
    fixtures["m10_reuse3"] = (note_with_rows(reuse3), reg_full, None)
    reg_anchor = reg_full.replace(
        "pinned snapshot .ufo/waves/round-71/before/src/moduleparam.h",
        "pinned snapshot .ufo/waves/round-71/before/src/kernel-param-header, tag v7.2.11")
    fixtures["m11_anchor_unbound"] = (base_note, reg_anchor, None)
    reg_src = reg_full.replace(
        "params.c at Linux v7.2.11 — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/kernel/params.c?h=v7.2.11",
        "params.c at Linux v7.2.11 (URL withheld by mutation)")
    fixtures["m12_source_unbound"] = (base_note, reg_src, None)
    invis = base_rows[:1] + base_rows[1:]
    invis[0] = invis[0].replace("| MP1 |", "|  MP1 |", 1)
    fixtures["m13_invisible_row"] = (note_with_rows(invis), reg_full, None)
    fixtures["m14_map_digest"] = (base_note, reg_full,
                                  {"params.c": "0" * 64})
    fixtures["m15_fewer_rows"] = (note_with_rows(base_rows[:5]), reg_full, None)
    fixtures["m16_gibberish_mix"] = (note_with_rows(rows_variant({
        2: {"stmt": "perm sysfs module velvet paradigm umbrellas whenever lantern castles juggle quantum marbles"}})), reg_full, None)

    results = {}
    for name, (note, reg, map_over) in sorted(fixtures.items()):
        root = build_tree(name, note, reg, map_over)
        res = {}
        for tag, cmd in (("mine", [sys.executable, str(MY_CHECKER), "--fixture", str(root)]),
                         ("lane", [sys.executable, LANE_COUNTER, "--fixture", str(root)])):
            p = subprocess.run(cmd, capture_output=True, text=True)
            res[tag] = {"rc": p.returncode, "out": p.stdout, "err": p.stderr[-400:]}
            (OUT / f"{name}.{tag}.txt").write_text(p.stdout + (f"\nSTDERR:{p.stderr}" if p.stderr else ""))
        results[name] = res
        print(f"== {name}: mine rc={res['mine']['rc']} lane rc={res['lane']['rc']}")
        for line in res["mine"]["out"].splitlines():
            if line.startswith(("ROW", "MP_", "MALFORMED", "IDS", "SNAPSHOT")):
                print("  M |", line)
        for line in res["lane"]["out"].splitlines():
            if line.startswith(("MP_ROW", "MP_", "malformed")) or "MP_ROW fail" in line:
                print("  L |", line)
    (OUT / "results.json").write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
