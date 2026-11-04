#!/usr/bin/env python3
"""R1Reviewer fixture probe: prove F4 traps against the FROZEN counter (read-only over repo).

Builds a synthetic fixture under this seat dir that mirrors the real pinned snapshots and
runs tools/count-uf-rows-r74.py --fixture three times:
  CONTROL : the six recommended rows -> expect rc 0, met=1
  T1      : UF2 quote swapped to the `\"%s\"` log string -> expect malformed row, rc 1
  T2      : UF6 quote without the ` * ` continuation marker -> expect quote-not-located, rc 1
No repo file is modified; the fixture lives under the seat dir.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

SEAT = Path(__file__).resolve().parent
REPO = SEAT.parents[4]
TOOL = REPO / "tools" / "count-uf-rows-r74.py"
FX = SEAT / "fx"

SRC = REPO / ".ufo/waves/round-74/before/src"
SNAPS = ("unit-file.c", "load-fragment.c", "unit-file.h")

DIGESTS = {
    "unit-file.c": "141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd",
    "load-fragment.c": "a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5",
    "unit-file.h": "e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f",
}
URLS = {
    "unit-file.c": "https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.c",
    "load-fragment.c": "https://raw.githubusercontent.com/systemd/systemd/v262/src/core/load-fragment.c",
    "unit-file.h": "https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.h",
}

ROWS = {
    "UF1": ("Unit search paths are walked in priority order and a name already registered is skipped, so the first-seen copy wins",
            "S309", "unit-file.c", "Search paths are ordered by priority (highest first), and we need to maintain this order."),
    "UF2": ("unit_validate_alias_symlink_or_warn returns ELOOP for a unit self-alias and EXDEV when the symlink target name type does not match source",
            "S309", "unit-file.c", "-EXDEV if the target filename is not a valid unit name or doesn't match the source,"),
    "UF3": ("unit_type_may_alias admits only UNIT_SERVICE UNIT_SOCKET UNIT_TARGET UNIT_DEVICE UNIT_TIMER UNIT_PATH so volume units can never carry aliases",
            "S311", "unit-file.h", "static inline bool unit_type_may_alias(UnitType type) { return IN_SET(type, UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH);"),
    "UF4": ("UnitFileState separates UNIT_FILE_ENABLED from UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED from UNIT_FILE_LINKED_RUNTIME, and UNIT_FILE_MASKED from UNIT_FILE_MASKED_RUNTIME",
            "S311", "unit-file.h", "UNIT_FILE_ENABLED, UNIT_FILE_ENABLED_RUNTIME, UNIT_FILE_LINKED, UNIT_FILE_LINKED_RUNTIME, UNIT_FILE_ALIAS, UNIT_FILE_MASKED, UNIT_FILE_MASKED_RUNTIME,"),
    "UF5": ("a null_or_empty fragment sets load_state to UNIT_MASKED and zero fragment_mtime except that perpetual units load as UNIT_LOADED instead",
            "S310", "load-fragment.c", "u->load_state = u->perpetual ? UNIT_LOADED : UNIT_MASKED; /* don't allow perpetual units to ever be masked */ u->fragment_mtime = 0;"),
    "UF6": ("missing fragments for system-scope units fall back to builtin_unit_lookup while on-disk files and masks unconditionally override built-ins",
            "S310", "load-fragment.c", "No fragment found on disk. For system units, fall back to a built-in copy if we have one * embedded."),
}

REG_ROWS = [
    "| S309 | systemd v262 src/shared/unit-file.c — {u} | code | A | The unit-file name-map plane | unit-file.c (snapshot .ufo/waves/round-74/before/src/unit-file.c) | probe | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-unit-fragment-plane-r74.md | |",
    "| S310 | systemd v262 src/core/load-fragment.c — {u} | code | A | The fragment load and mask plane | load-fragment.c (snapshot .ufo/waves/round-74/before/src/load-fragment.c) | probe | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-unit-fragment-plane-r74.md | |",
    "| S311 | systemd v262 src/shared/unit-file.h — {u} | code | A | The unit-file state and alias gate header | unit-file.h (snapshot .ufo/waves/round-74/before/src/unit-file.h) | probe | mined | 2026-11-04 | on-release | corpus/knowledge/systemd-unit-fragment-plane-r74.md | |",
]


def build():
    if FX.exists():
        shutil.rmtree(FX)
    snapdir = FX / ".ufo/waves/round-74/before/src"
    snapdir.mkdir(parents=True)
    for s in SNAPS:
        shutil.copy2(SRC / s, snapdir / s)
    smap = {s: {"url": URLS[s], "sha256": DIGESTS[s], "tag": "v262", "bytes": (SRC / s).stat().st_size} for s in SNAPS}
    (snapdir / "SOURCES.json").write_text(json.dumps(smap, indent=2), encoding="utf-8")
    reg = FX / "corpus/SOURCES.md"
    reg.parent.mkdir(parents=True)
    reg.write_text(
        "# SOURCES\n\n"
        "| ID | Title | Kind | Tier | Scope | Location | Summary | Status | Date | Recheck | Used-by | Notes |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---|\n"
        + "\n".join(r.format(u=URLS[s]) for r, s in zip(REG_ROWS, ("unit-file.c", "load-fragment.c", "unit-file.h"))) + "\n",
        encoding="utf-8")


def note_text(quote_overrides):
    lines = ["# probe note", ""]
    for uf in ("UF1", "UF2", "UF3", "UF4", "UF5", "UF6"):
        stmt, src, snap, quote = ROWS[uf]
        quote = quote_overrides.get(uf, quote)
        lines.append(f"| {uf} | {stmt} | source={src} | snapshot={snap} | digest={DIGESTS[snap]} | quote=\"{quote}\" |")
    (FX / "corpus/knowledge").mkdir(parents=True, exist_ok=True)
    (FX / "corpus/knowledge/systemd-unit-fragment-plane-r74.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(label, expect_rc, expect_sub):
    res = subprocess.run([sys.executable, str(TOOL), "--fixture", str(FX)],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = res.stdout.strip(), res.stderr.strip()
    ok = res.returncode == expect_rc and expect_sub in (out + err)
    print(f"[{label}] rc={res.returncode} expect={expect_rc} {'PASS' if ok else 'FAIL'}")
    print(f"    stdout: {out}")
    if err:
        print(f"    stderr: {err}")
    return ok


if __name__ == "__main__":
    build()
    results = []
    note_text({})
    results.append(run("CONTROL (six REC rows)", 0, "UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0"))
    note_text({"UF2": '%s: symlink target name type \\"%s\\" does not match source, rejecting.'})
    results.append(run("T1 escaped-quote log string", 1, "malformed row shape"))
    note_text({"UF6": "On-disk files always take precedence (including masks), since we only get here when nothing was found in the lookup paths."})
    results.append(run("T2 asterisk-less multiline comment", 1, "quote not located in snapshot load-fragment.c"))
    print("PROBE:", "PASS" if all(results) else "FAIL")
    sys.exit(0 if all(results) else 1)
