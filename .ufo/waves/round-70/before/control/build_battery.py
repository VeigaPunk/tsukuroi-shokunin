#!/usr/bin/env python3
"""Round-70 C1 pre-data control battery for tools/count-xs-rows-r70.py.

Builds fixture mirrors in a scratch root (never /tmp), each mirror a repository layout, and
runs the frozen counter on every case. The control must read 6/6 rc 0; every mutant must read
below the target and exit 1. Creates nothing outside the given scratch root.
"""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
COUNTER = LANE / "tools/count-xs-rows-r70.py"

SNAPS = {
    "s_stats.c": (
        "/* fixture stats source: group table and per_cpu counter sums */\n"
        "static const struct xstats_entry xstats[] = {\n"
        "    { \"extent_alloc\", xfsstats_offset(xs_abt_lookup) },\n"
        "};\n"
        "int xfs_stats_format(struct xfsstats *stats, char *buf) {\n"
        "    val += *(((__u32 *)per_cpu_ptr(stats, cpu) + idx));\n"
        "    return len;\n"
        "}\n"
        "/* the stats group line prints one summary per named counter group */\n"
    ),
    "s_sysfs.c": (
        "/* fixture sysfs source: stats attribute and clear store */\n"
        "STATIC ssize_t stats_clear_store(struct kobject *kobject, const char *buf,\n"
        "        size_t count) {\n"
        "    if (val != 1)\n"
        "        return -EINVAL;\n"
        "    xfs_stats_clearall(stats->xs_stats);\n"
        "    return count;\n"
        "}\n"
        "XFS_SYSFS_ATTR_WO(stats_clear);\n"
    ),
    "s_docs.rst": (
        "Fixture documentation: error configuration tree\n"
        "================================================\n"
        "Each filesystem exposes an error handler class directory under sysfs.\n"
        "The metadata class applies to metadata buffer write input output errors.\n"
        "The fail_at_unmount option defines the error behaviour at unmount time.\n"
    ),
    "s_health.c": (
        "/* fixture spaceman source: online health reader messages */\n"
        "printf(_(\"Health status has not been collected for this filesystem.\\n\"));\n"
        "printf(_(\"Please run xfs_scrub(8) to remedy this situation.\\n\"));\n"
    ),
}
ROWS = [
    ("S901", "s_stats.c",
     "Each stats group line prints one summary whose values are a summed per_cpu counter array.",
     "val += *(((__u32 *)per_cpu_ptr(stats, cpu) + idx));"),
    ("S901", "s_stats.c",
     "The stats format function walks the named xstats group table and emits a summary line.",
     "static const struct xstats_entry xstats[] = {"),
    ("S902", "s_sysfs.c",
     "The stats_clear store accepts only the one value before it clears the xstats stats.",
     "    if (val != 1)"),
    ("S902", "s_sysfs.c",
     "The stats_clear attribute is declared write only in the sysfs attribute table.",
     "XFS_SYSFS_ATTR_WO(stats_clear);"),
    ("S903", "s_docs.rst",
     "The metadata class applies to metadata buffer write input output errors for each filesystem.",
     "The metadata class applies to metadata buffer write input output errors."),
    ("S904", "s_health.c",
     "The online health reader prints that health status has not been collected for this filesystem.",
     "Health status has not been collected for this filesystem."),
]
URLS = {
    "S901": "https://example.invalid/fixture/s_stats.c?h=v1",
    "S902": "https://example.invalid/fixture/s_sysfs.c?h=v1",
    "S903": "https://example.invalid/fixture/s_docs.rst?h=v1",
    "S904": "https://example.invalid/fixture/s_health.c?h=v1",
}
SNAP_OF = {"S901": "s_stats.c", "S902": "s_sysfs.c", "S903": "s_docs.rst",
           "S904": "s_health.c"}


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def build(base):
    src = base / ".ufo/waves/round-70/before/src"
    (base / "corpus/knowledge").mkdir(parents=True)
    src.mkdir(parents=True)
    snaps = {}
    for name, text in SNAPS.items():
        (src / name).write_text(text)
        sid = [k for k, v in SNAP_OF.items() if v == name][0]
        snaps[name] = {"url": URLS[sid], "rev": "v1", "accessed": "2026-11-03",
                       "sha256": digest(text), "bytes": len(text.encode())}
    (src / "SOURCES.json").write_text(json.dumps({"snapshots": snaps}, indent=1))
    reg = ["# SOURCES — fixture", "## Registry",
           "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for sid in ("S901", "S902", "S903", "S904"):
        reg.append(f"| {sid} | fixture source — {URLS[sid]} | code | A | fixture scope | "
                   f"v1 line | teaches nothing | mined | 2026-11-03 | 90d | corpus/knowledge/x.md |")
    (base / "corpus/SOURCES.md").write_text("\n".join(reg) + "\n")


def write_note(base, rows, digests=None, ids=None):
    lines = ["# fixture note", "", "| row | statement | source | snapshot | digest | quote |",
             "|---|---|---|---|---|---|"]
    for i, (src, snap, stmt, quote) in enumerate(rows):
        d = digests[i] if digests else digest(SNAPS[snap])
        n = ids[i] if ids else i + 1
        lines.append(f'| XS{n} | {stmt} | source={src} | snapshot={snap} | digest={d} '
                     f'| quote="{quote}" |')
    (base / "corpus/knowledge/xfs-storage-plane-r70.md").write_text("\n".join(lines) + "\n")


def run(base):
    r = subprocess.run([sys.executable, str(COUNTER), "--fixture", str(base)],
                       capture_output=True, text=True)
    summary = [ln for ln in r.stdout.splitlines() if ln.startswith(("XS_ROWS", "XS_TARGET"))]
    return r.returncode, " | ".join(summary)


def main():
    root = pathlib.Path(os.environ.get("XS_BATTERY_SCRATCH",
                                       "/fast/scratch/hyaku/tsukuroi-r70/l1/battery"))
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    cases = []

    def add(name, rows, want, note, digests=None, ids=None):
        base = root / name
        build(base)
        write_note(base, rows, digests, ids)
        cases.append((name, base, want, note))

    add("ok-control", ROWS, 0, "control reaches the frozen target")
    filler = [(s, sn, "This fixture row records a general claim measured on an earlier occasion.", q)
              for s, sn, _, q in ROWS]
    add("mutant-content-free", filler, 1, "statement-substance clause kills filler prose")
    anyid = [("S902", sn, st, q) if i == 0 else (s, sn, st, q)
             for i, (s, sn, st, q) in enumerate(ROWS)]
    add("mutant-any-registered-id", anyid, 1, "source-to-snapshot binding kills any registered id")
    ds = [digest(SNAPS[r[1]]) for r in ROWS]
    ds[0] = digest(SNAPS["s_health.c"])
    add("mutant-digest-swap", ROWS, 1, "a digest from another snapshot fails", digests=ds)
    absent = list(ROWS)
    absent[1] = (absent[1][0], absent[1][1], absent[1][2],
                 "This quoted sentence is not present in the source.")
    add("mutant-quote-absent", absent, 1, "an unlocated quote fails")
    short = list(ROWS)
    short[2] = (short[2][0], short[2][1], "Too short a claim.", short[2][3])
    add("mutant-short-statement", short, 1, "a statement under 12 words fails")
    add("mutant-five-rows", ROWS[:5], 1, "five rows is below the frozen target")
    dupids = [1, 1, 3, 4, 5, 6]
    add("mutant-duplicate-id", ROWS, 1, "a duplicate row id fails", ids=dupids)

    fails = 0
    print(f"round-70 C1 counter battery (frozen counter, fixtures under {root})")
    print(f"counter sha256 {hashlib.sha256(COUNTER.read_bytes()).hexdigest()}")
    for name, base, want_rc, note in cases:
        rc, summary = run(base)
        ok = rc == want_rc
        fails += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'} {name}: rc={rc} want={want_rc} {summary} — {note}")
    print(f"BATTERY: {'PASS' if fails == 0 else 'FAIL'} ({len(cases)} cases, "
          f"{len(cases) - fails} passed, {fails} failed)")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
