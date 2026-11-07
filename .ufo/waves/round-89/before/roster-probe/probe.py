#!/usr/bin/env python3
"""Round-89 roster validation probe (tsukuroi L1, before the freeze; NOT the battery, NOT the counter).

Purpose: admit a gate to the r89 roster only if its label is behaviourally earned on hand-written,
deterministic fixtures whose expected answers follow the r88 battery docstring rule set R1-R8:
  * every POSITIVE gate returns exactly the expected answer on EVERY probe;
  * every NEGATIVE gate added in r89 returns a wrong answer on AT LEAST ONE probe (its witness).
A gate is compared as the r88 battery compares it: process rc, JSON rc, verdict, sorted
(line, status, consequence) per pin, and the R8 optional fields only when present
("entry" per pin; "hash_mismatch_panic" {line, value case-insensitive}).

Usage: probe.py [--work DIR] [--json OUT]     (TMPDIR honoured; nothing written outside --work)
Exit: 0 every positive exact and every r89 negative witnessed; 1 otherwise.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROSTER = os.path.join(os.path.dirname(HERE), "roster")
POSITIVES = ["pos-landed-gate-3ba37eb0.py", "m01-comment-not-skipped.py", "pos-r88-docstring-base.py"]
# g00-base was an r88 POSITIVE; this probe found it strips only a TRAILING CR (config.c raw 527-551 removes
# every CR) and crashes on an empty path, so r89 relabels it NEGATIVE (witnessed below like every r89 negative).
NEW_NEGATIVES = ["g00-base.py", "f01-any-whitespace-blank-class.py", "f03-optional-missing-skip.py",
                 "f06-empty-pin-list-cannot-evaluate.py", "f07-dollar-lstrip-all.py",
                 "f08-entry-label-trailing-plus.py", "f12-panic-value-raw-trailing-blanks.py",
                 "f14-cr-stripped-only-trailing.py", "f16-optional-unresolved-skip.py",
                 "f18-resource-case-insensitive.py", "f19-entry-label-not-trimmed.py",
                 "h01-key-sep-equals.py", "h10-empty-path-pin-ignored.py",
                 "h11-optional-case-sensitive.py", "h19-entry-plus-kept.py",
                 "h20-resource-case-insensitive.py", "m31-panic-value-untrimmed.py"]

A = b"kernel-a bytes for the r89 probe\n"
W = b"wallpaper bytes for the r89 probe\n"
HA = hashlib.blake2b(A).hexdigest()
HW = hashlib.blake2b(W).hexdigest()
BADA = HA[:-1] + ("0" if HA[-1] != "0" else "1")
BADW = HW[:-1] + ("0" if HW[-1] != "0" else "1")

# name: (conf lines, expected rc, verdict, pins [(line, status, consequence)],
#        expected entries {line: label} or None, expected panic None | (line, value))
PROBES = {
    "blank-class-indent": (["/e", "\x0cpath: boot():/a.efi#" + BADA, "path: boot():/a.efi#" + HA],
                           0, "HEALTHY", [(3, "OK", "none")], {3: "e"}, None),
    "blank-class-trailing": (["/e", "path: boot():/a.efi#" + HA + "\x0b"],
                             1, "DEGRADED", [(2, "LP-HASH-FORMAT", "panic")], {2: "e"}, None),
    "optional-missing": (["/e", "path: boot():/a.efi#" + HA, "wallpaper: boot():/zz.png#" + HW],
                         1, "DEGRADED", [(2, "OK", "none"), (3, "LP-MISSING", "not-modelled")],
                         {2: "e", 3: "e"}, None),
    "empty-pin-list": (["timeout: 3", "/e", "protocol: efi", "cmdline: quiet"], 0, "HEALTHY", [], {}, None),
    "double-dollar": (["/e", "path: $$boot():/a.efi#" + HA],
                      2, "CANNOT-EVALUATE", [(2, "LP-UNRESOLVED", "not-modelled")], {2: "e"}, None),
    "entry-trailing-plus": (["/e+", "path: boot():/a.efi#" + HA], 0, "HEALTHY", [(2, "OK", "none")],
                            {2: "e+"}, None),
    "panic-value-trailing-blanks": (["hash_mismatch_panic: no \t", "/e", "path: boot():/a.efi#" + BADA],
                                    1, "DEGRADED", [(3, "LP-MISMATCH", "prompt")], {3: "e"}, (1, "no")),
    "cr-internal": (["/e", "pa\rth: boot():/a.efi#" + BADA], 1, "DEGRADED", [(2, "LP-MISMATCH", "panic")],
                    {2: "e"}, None),
    "optional-unresolved": (["/e", "path: boot():/a.efi#" + HA, "wallpaper: guid(1234):/w.png#" + HW],
                            2, "CANNOT-EVALUATE", [(2, "OK", "none"), (3, "LP-UNRESOLVED", "not-modelled")],
                            {2: "e", 3: "e"}, None),
    "resource-case": (["/e", "path: BOOT():/a.efi#" + HA], 2, "CANNOT-EVALUATE",
                      [(2, "LP-UNRESOLVED", "not-modelled")], {2: "e"}, None),
    "entry-trim": (["/   e  x", "path: boot():/a.efi#" + HA], 0, "HEALTHY", [(2, "OK", "none")],
                   {2: "e  x"}, None),
    "key-equals": (["/e", "path= boot():/a.efi#" + BADA, "path: boot():/a.efi#" + HA], 0, "HEALTHY",
                   [(3, "OK", "none")], {3: "e"}, None),
    "empty-path": (["/e", "path: boot():/#" + HA], 1, "DEGRADED", [(2, "LP-MISSING", "not-modelled")],
                   {2: "e"}, None),
    "optional-key-case": (["/e", "WALLPAPER: boot():/w.png#" + BADW, "path: boot():/a.efi#" + HA],
                          1, "DEGRADED", [(2, "LP-MISMATCH", "skip"), (3, "OK", "none")],
                          {2: "e", 3: "e"}, None),
    "entry-plus": (["/+e", "path: boot():/a.efi#" + HA], 0, "HEALTHY", [(2, "OK", "none")], {2: "e"}, None),
    "panic-value-report": (["hash_mismatch_panic: no", "/e", "path: boot():/a.efi#" + BADA],
                           1, "DEGRADED", [(3, "LP-MISMATCH", "prompt")], {3: "e"}, (1, "no")),
}


def run(gate, lines, work):
    d = tempfile.mkdtemp(prefix="p", dir=work)
    esp = os.path.join(d, "esp")
    os.makedirs(esp)
    with open(os.path.join(esp, "a.efi"), "wb") as f:
        f.write(A)
    with open(os.path.join(esp, "w.png"), "wb") as f:
        f.write(W)
    conf = os.path.join(d, "limine.conf")
    with open(conf, "w", newline="") as f:
        f.write("\n".join(lines) + "\n")
    try:
        p = subprocess.run([sys.executable, gate, "--conf", conf, "--esp", esp], cwd=d,
                           capture_output=True, text=True, timeout=20)
        out = json.loads(p.stdout)
        pins = sorted((int(x["line"]), str(x["status"]), str(x["consequence"])) for x in out["pins"])
        ents = {int(x["line"]): x["entry"] for x in out["pins"] if "entry" in x}
        panic = ("present", out["hash_mismatch_panic"]) if "hash_mismatch_panic" in out else ("absent", None)
        return (p.returncode, out["rc"], out["verdict"], pins, ents, panic), None
    except Exception as e:  # noqa: BLE001
        return None, "%s" % type(e).__name__
    finally:
        shutil.rmtree(d, ignore_errors=True)


def exact(got, want):
    if got is None:
        return False
    rc, verdict, pins, ents, panic = want
    if not (got[0] == rc and got[1] == rc and got[2] == verdict and got[3] == sorted(pins)):
        return False
    for ln, label in got[4].items():
        if ents.get(ln, "<absent>") != label:
            return False
    state, pm = got[5]
    if state == "present":
        if panic is None:
            return pm is None
        return (isinstance(pm, dict) and pm.get("line") == panic[0]
                and str(pm.get("value", "")).lower() == panic[1].lower())
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=os.environ.get("TMPDIR") or tempfile.gettempdir())
    ap.add_argument("--json")
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    work = tempfile.mkdtemp(prefix="r89-probe-", dir=a.work)
    table = {}
    try:
        for g in POSITIVES + NEW_NEGATIVES:
            gp = os.path.join(ROSTER, g)
            table[g] = {}
            for name, (lines, *want) in PROBES.items():
                got, err = run(gp, lines, work)
                table[g][name] = "exact" if exact(got, want) else ("error:" + err if err else "differs")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    ok = True
    for g in POSITIVES:
        bad = [p for p, v in table[g].items() if v != "exact"]
        print("POSITIVE %-40s %s" % (g, "exact on %d/%d" % (len(PROBES) - len(bad), len(PROBES))
                                      + ("" if not bad else " NOT EXACT: " + ",".join(bad))))
        ok &= not bad
    for g in NEW_NEGATIVES:
        wit = [p for p, v in table[g].items() if v == "differs"]
        errs = [p for p, v in table[g].items() if v.startswith("error")]
        print("NEGATIVE %-40s witnesses: %s%s" % (g, ",".join(wit) or "NONE",
                                                 (" errors: " + ",".join(errs)) if errs else ""))
        ok &= bool(wit)
    if a.json:
        with open(a.json, "w") as f:
            json.dump(table, f, indent=1)
    print("probe %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
