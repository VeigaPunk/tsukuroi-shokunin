#!/usr/bin/env python3
"""Round-88 frozen discrimination counter for a Limine pin-gate battery (tsukuroi lane).

PREDICATE (the same sentence in SCORECARD.md "Round 88 — declaration" and in every receipt):
  The battery under test, driven by this counter over the frozen roster
  `.ufo/waves/round-88/before/roster/roster-r88.json`, reads `met` (exit 0 and JSON verdict
  "met") for every POSITIVE gate and `unmet` (exit 1 and JSON verdict "unmet") for every
  NEGATIVE gate, in each of three runs, with every gate handed to the battery as a freshly
  renamed, nonce-perturbed copy inside a sandbox that hides the lane repository.
TARGET: positives P/P and negatives N/N in each of the three runs (verdict `met`, exit 0).
KILL RULE: unmet if any run reads below P/P or N/N; void (exit 2) if this file or any roster
  file differs from `.ufo/waves/round-88/before/freeze-manifest.sha256` / the roster digests.

Isolation (why a battery cannot read the answer):
  * each roster gate is copied to a random file name and gets one trailing comment line
    `# nonce <random hex>` per invocation, so no stored digest or name identifies it;
  * the battery file is copied next to it and both run under `bwrap` with the lane repository
    replaced by an empty tmpfs and the network unshared, so the roster, its labels, the forger
    sources and the reference gate are not readable from inside.
A gate whose behaviour depends on its own bytes or file name is not in the roster.

Battery interface (same as tools/limine-pin-battery-r87.py):
  python3 BATTERY --gate GATE --runs 1 --work DIR --json OUT    exit 0 met / 1 unmet

Usage: battery-discrimination-r88.py --battery PATH [--runs 3] [--jobs 8] [--scratch DIR]
                                     [--json OUT] [--roster PATH]
Exit: 0 met; 1 unmet; 2 void/usage.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
import secrets
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
ROSTER = os.path.join(LANE, ".ufo", "waves", "round-88", "before", "roster", "roster-r88.json")
BATTERY_TIMEOUT = 900


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_roster(path):
    with open(path) as f:
        roster = json.load(f)
    base = os.path.dirname(os.path.abspath(path))
    bad = []
    for g in roster["gates"]:
        g["abs"] = os.path.join(base, g["file"])
        if not os.path.isfile(g["abs"]) or sha256(g["abs"]) != g["sha256"]:
            bad.append(g["id"])
        if g["expect"] not in ("met", "unmet"):
            bad.append(g["id"] + ":expect")
    return roster, bad


def one(battery, gate, scratch, lane):
    """Run the battery once on one perturbed gate copy; return 'met', 'unmet' or 'error:<why>'."""
    d = tempfile.mkdtemp(prefix="bd-", dir=scratch)
    try:
        name = "g" + secrets.token_hex(6) + ".py"
        with open(gate["abs"], "rb") as f:
            src = f.read()
        if not src.endswith(b"\n"):
            src += b"\n"
        src += b"# nonce " + secrets.token_hex(16).encode() + b"\n"
        gp = os.path.join(d, name)
        with open(gp, "wb") as f:
            f.write(src)
        for extra in gate.get("support", []):
            shutil.copy(os.path.join(os.path.dirname(gate["abs"]), extra), os.path.join(d, extra))
        bp = os.path.join(d, "battery-" + secrets.token_hex(4) + ".py")
        shutil.copy(battery, bp)
        work = os.path.join(d, "work")
        os.makedirs(work)
        out = os.path.join(d, "out.json")
        argv = ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
                "--tmpfs", lane, "--bind", d, d, "--chdir", d, "--unshare-net",
                "--die-with-parent", "--setenv", "TMPDIR", work,
                sys.executable, bp, "--gate", gp, "--runs", "1", "--work", work, "--json", out]
        try:
            p = subprocess.run(argv, capture_output=True, text=True, timeout=BATTERY_TIMEOUT)
        except subprocess.TimeoutExpired:
            return "error:timeout", None
        try:
            with open(out) as f:
                j = json.load(f)
            if isinstance(j, list):
                j = j[0]
            verdict = j["verdict"]
            fp = j.get("families_passed")
        except Exception as e:  # noqa: BLE001 - a missing/garbled receipt is an error, never a verdict
            return "error:json %s rc=%s %s" % (type(e).__name__, p.returncode, p.stderr[-200:]), None
        if p.returncode == 0 and verdict == "met":
            return "met", fp
        if p.returncode == 1 and verdict == "unmet":
            return "unmet", fp
        return "error:rc=%s verdict=%s" % (p.returncode, verdict), fp
    finally:
        shutil.rmtree(d, ignore_errors=True)


def run_once(battery, roster, scratch, lane, jobs):
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = {ex.submit(one, battery, g, scratch, lane): g for g in roster["gates"]}
        for fu in concurrent.futures.as_completed(futs):
            g = futs[fu]
            got, fp = fu.result()
            rows.append({"id": g["id"], "expect": g["expect"], "got": got, "families_passed": fp,
                         "ok": got == g["expect"]})
    rows.sort(key=lambda r: r["id"])
    pos = [r for r in rows if r["expect"] == "met"]
    neg = [r for r in rows if r["expect"] == "unmet"]
    return {"positives_ok": sum(r["ok"] for r in pos), "positives_total": len(pos),
            "negatives_ok": sum(r["ok"] for r in neg), "negatives_total": len(neg),
            "failures": [r["id"] for r in rows if not r["ok"]], "rows": rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--battery", required=True)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--scratch", default=os.environ.get("TMPDIR"))
    ap.add_argument("--json")
    ap.add_argument("--roster", default=ROSTER)
    a = ap.parse_args()
    if shutil.which("bwrap") is None:
        print("void: bwrap not found", file=sys.stderr)
        return 2
    battery = os.path.abspath(a.battery)
    if not os.path.isfile(battery):
        print("void: battery not found: %s" % battery, file=sys.stderr)
        return 2
    roster, bad = load_roster(a.roster)
    if bad:
        print("void: roster digest/label mismatch: %s" % ",".join(bad), file=sys.stderr)
        return 2
    scratch = a.scratch or tempfile.gettempdir()
    os.makedirs(scratch, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="battery-discrimination-r88-", dir=scratch)
    lane = LANE
    try:
        runs = [run_once(battery, roster, scratch, lane, a.jobs) for _ in range(a.runs)]
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    met = all(r["positives_ok"] == r["positives_total"] and r["negatives_ok"] == r["negatives_total"]
              for r in runs)
    res = {"schema": "tsukuroi-battery-discrimination-r88-v1", "battery": battery,
           "battery_sha256": sha256(battery), "counter_sha256": sha256(os.path.abspath(__file__)),
           "roster_sha256": sha256(a.roster), "runs": runs, "verdict": "met" if met else "unmet"}
    if a.json:
        with open(a.json, "w") as f:
            json.dump(res, f, indent=1)
    for i, r in enumerate(runs, 1):
        print("run %d positives %d/%d negatives %d/%d failures %s" % (
            i, r["positives_ok"], r["positives_total"], r["negatives_ok"], r["negatives_total"],
            ",".join(r["failures"]) or "-"))
    print("verdict %s" % res["verdict"])
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
