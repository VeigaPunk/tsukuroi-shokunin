#!/usr/bin/env python3
"""ScoutDrift seat measurement (round 97, wave w1) — read-only.

Measures the drift surface the round's claims touch and the named limit C2 discloses:

  A. hash comparison table (lane tree, frozen controls, pre-round tip f48d1642)
  B. operative-table binding coverage: rows of the operative SKILL.md registry table that
     carry a cell of a kind `tools/check-registry-content.py`'s BINDINGS binds
     (selftest tally / roster size / variant span / schema token / argparse default),
     with each such cell re-derived from the bytes of the tool its row names
  C. drift sweep over the r96 documents the round corrects (103/103, Z-cap, leading-zero)

Nothing is written outside the seat dir; the lane tree is only read.
Usage: python3 measure.py <lane> <outdir>
"""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE, OUT = sys.argv[1], sys.argv[2]
SKILL = sys.argv[3] if len(sys.argv) > 3 else os.path.join(LANE, "SKILL.md")
os.makedirs(OUT, exist_ok=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_show(rev, path):
    p = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (rev, path)],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


# ---------------------------------------------------------------- A. hashes
PRE = "f48d16428d8bb92fd6cf546a745bff5b624e3f18"
A_ROWS = [
    ("tools/check-limine-pins.py", "7d79ac29…", "gate (unchanged this round)"),
    (".ufo/waves/round-97/before/controls/do-nothing-gate.py", "7d79ac29…", "frozen do-nothing gate copy"),
    (".ufo/waves/round-97/before/controls/do-nothing-battery-r96.py", "f06d90ae…", "frozen do-nothing r96 battery copy"),
    ("tools/check-registry-coverage.py", "6fcb2d0a…", "coverage gate (unchanged)"),
    (".ufo/waves/round-97/before/controls/do-nothing-registry-coverage.py", "6fcb2d0a…", "frozen do-nothing coverage copy"),
    ("tools/limine-pin-battery-r97.py", "e678c34f…", "C1 instrument"),
    ("tools/check-registry-content.py", "2daf5926…", "C2 instrument"),
    ("tools/check-r96-calibration.py", "7ff63524…", "frozen instrument"),
    ("tools/make-r97-bends.py", "972c672b…", "frozen instrument"),
    ("tools/limine-pin-battery-r96.py", "f06d90ae… at " + PRE,
     "r96 battery — worktree carries the r97 docstring correction, so its bytes are NOT f06d90ae"),
]
a_rows = []
for rel, expected, note in A_ROWS:
    p = os.path.join(LANE, rel)
    observed = sha256(p) if os.path.exists(p) else "MISSING"
    if rel == "tools/limine-pin-battery-r96.py":
        # the worktree file was corrected this round (routed defect 2/3); its pre-round bytes
        # are re-derivable at PRE and are what the frozen control pins.
        base = git_show(PRE, rel)
        observed = "%s (worktree; pre-round bytes %s)" % (observed, hashlib.sha256(base).hexdigest())
        expected = "f06d90ae… (pre-round bytes)"
    a_rows.append({"file": rel, "expected": expected, "observed": observed, "note": note})

# manifest check
mp = subprocess.run(["sha256sum", "-c", ".ufo/waves/round-97/before/instruments.sha256"],
                    cwd=LANE, capture_output=True, text=True)
manifest_lines = mp.stdout.strip().splitlines()
manifest_failed = [l for l in manifest_lines if not l.endswith(": OK")]

# control copies vs the frozen pre-round tip
b_rows = []
for rel, tip_rel in [
    (".ufo/waves/round-97/before/controls/do-nothing-battery-r96.py", "tools/limine-pin-battery-r96.py"),
    (".ufo/waves/round-97/before/controls/do-nothing-gate.py", "tools/check-limine-pins.py"),
    (".ufo/waves/round-97/before/controls/do-nothing-registry-coverage.py", "tools/check-registry-coverage.py"),
]:
    copy = sha256(os.path.join(LANE, rel))
    tip = hashlib.sha256(git_show(PRE, tip_rel)).hexdigest()
    b_rows.append({"control": rel, "pre_round_path": "%s:%s" % (PRE, tip_rel),
                   "control_sha256": copy, "pre_round_sha256": tip,
                   "identical": copy == tip,
                   "difference": "none (byte-identical)" if copy == tip else "DIFFERS"})

# ---------------------------------------------------------------- B. binding coverage
spec = importlib.util.spec_from_file_location("crc", os.path.join(LANE, "tools/check-registry-content.py"))
crc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crc)

text = open(SKILL, encoding="utf-8").read()
rows = crc.operative_rows(text)

CAPS = [(b["id"], b["capture"], b["derive"]) for b in crc.BINDINGS]
NUMERIC = {"RC-SELFTEST-COUNT", "RC-CAL-SELFTEST", "RC-ROSTER-VERDICT", "RC-ROSTER-PINNED", "RC-BEND-SPAN"}


def entry_tool(row):
    m = re.search(r"tools/([A-Za-z0-9._-]+\.py)", row["cells"][2])
    return m.group(1) if m else None


WORK = tempfile.mkdtemp(prefix="scoutdrift-", dir=OUT)
cache = {}


def derive(tool, kind):
    key = (tool, kind)
    if key in cache:
        return cache[key]
    try:
        if kind == "selftest_total":
            tmp = tempfile.mkdtemp(prefix="rc-", dir=WORK)
            try:
                dst = os.path.join(tmp, tool)
                shutil.copyfile(os.path.join(LANE, "tools", tool), dst)
                os.chmod(dst, 0o755)
                p = subprocess.run([sys.executable, "-I", dst, "--selftest"], cwd=tmp,
                                   capture_output=True, text=True, timeout=180,
                                   env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": tmp})
                if p.returncode != 0:
                    raise ValueError("--selftest exited %d" % p.returncode)
                first, second = crc.parse_tally(p.stdout)
                if first != second:
                    raise ValueError("tally not N/N")
                val = str(first)
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
        else:
            val = str(crc.DERIVERS[kind](open(os.path.join(LANE, "tools", tool)).read(), None))
        cache[key] = ("DERIVED", val)
    except Exception as exc:
        cache[key] = ("DERIVE-FAILED", str(exc)[:120])
    return cache[key]


cells = []
for row in rows:
    for bid, cap, kind in CAPS:
        for ci, cell in enumerate(row["cells"]):
            m = re.search(cap, cell)
            if not m:
                continue
            declared = m.group(1)
            tool = entry_tool(row)
            if not tool or not os.path.exists(os.path.join(LANE, "tools", tool)):
                status, derived = "NO-TOOL", None
            else:
                status, derived = derive(tool, kind)
            cells.append({"row": row["cells"][0], "line": row["line"], "binding": bid,
                          "cell_index": ci, "declared": declared, "tool": tool,
                          "status": status, "derived": derived,
                          "matches": (status == "DERIVED" and derived == declared),
                          "numeric_kind": bid in NUMERIC})
            break

shape_rows = sorted({c["row"] for c in cells})
numeric_shape_rows = sorted({c["row"] for c in cells if c["numeric_kind"]})
checkable_rows = sorted({c["row"] for c in cells if c["matches"]})
failing_rows = sorted({c["row"] for c in cells if c["numeric_kind"] and not c["matches"]
                        and c["status"] == "DERIVE-FAILED"})
bound_rows = sorted({b["row"] for b in crc.BINDINGS})
unbound_checkable = [r for r in checkable_rows if r not in bound_rows]

# ---------------------------------------------------------------- C. drift sweep
def git_grep(pattern, paths):
    p = subprocess.run(["git", "-C", LANE, "grep", "-n", pattern, "--"] + paths,
                       capture_output=True, text=True)
    return [l for l in p.stdout.splitlines() if l]


c_103 = git_grep("103/103", ["corpus", "SCORECARD.md", "LOG.md"])
c_z = git_grep(r"Z-cap\|leading-zero", ["corpus"])
# the same sweep at the frozen pre-round tip, for the count that the round's own
# documents were written against
p103 = subprocess.run(["git", "-C", LANE, "grep", "-n", "103/103", PRE, "--",
                        "corpus", "SCORECARD.md", "LOG.md"], capture_output=True, text=True)
pz = subprocess.run(["git", "-C", LANE, "grep", "-n", r"Z-cap\|leading-zero", PRE, "--", "corpus"],
                    capture_output=True, text=True)

# r96 Frontier sentences that this round's families supersede
supersede_probes = [
    ("corpus/README.md", "The Z component's 9-digit boundary is **uncertified**"),
    ("corpus/README.md", "a 9-digit component with"),
    ("corpus/knowledge/limine-bound-per-component-r96.md",
     "The Z component's 9-digit boundary and a 9-digit component with leading zeros are **unsent**"),
    ("SCORECARD.md", "leading zeros are uncertified"),
    ("corpus/lessons/round-96.md", "M06 Z-cap and M08"),
]
carry = []
for rel, needle in supersede_probes:
    p = subprocess.run(["git", "-C", LANE, "grep", "-n", "-F", needle, "--", rel],
                       capture_output=True, text=True)
    carry.append({"file": rel, "sentence_needle": needle,
                  "still_present": [l for l in p.stdout.splitlines() if l]})

out = {"pre_round_tip": PRE,
       "A_hashes": a_rows,
       "A_manifest_failed": manifest_failed,
       "A_manifest_failed_count": len(manifest_failed),
       "B_controls_vs_pre_round_tip": b_rows,
       "B_operative_rows": len(rows),
       "B_cells": cells,
       "B_shape_rows": shape_rows,
       "B_numeric_shape_rows": numeric_shape_rows,
       "B_machine_checkable_rows": checkable_rows,
       "B_derive_failed_rows": failing_rows,
       "B_bound_rows": bound_rows,
       "B_unbound_but_machine_checkable_rows": unbound_checkable,
       "C_103_count_worktree": len(c_103), "C_103_lines_worktree": c_103,
       "C_103_count_pre_round": len([l for l in p103.stdout.splitlines() if l]),
       "C_zcap_count_worktree": len(c_z), "C_zcap_lines_worktree": c_z,
       "C_zcap_count_pre_round": len([l for l in pz.stdout.splitlines() if l]),
       "C_r96_frontier_carriers": carry}
with open(os.path.join(OUT, "measure.json"), "w") as f:
    json.dump(out, f, indent=1, sort_keys=True)
shutil.rmtree(WORK, ignore_errors=True)
print(json.dumps({k: v for k, v in out.items() if k not in ("B_cells", "A_hashes", "C_103_lines_worktree",
                                                            "C_zcap_lines_worktree")}, indent=1, sort_keys=True))
print("wrote", os.path.join(OUT, "measure.json"))
