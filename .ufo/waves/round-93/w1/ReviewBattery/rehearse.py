#!/usr/bin/env python3
"""ReviewBattery r93: build one case per new family and run landed + N01..N06 through the battery's
own build/run_gate/run_usage, printing the hand-checkable tuple and every field that flips."""
import importlib.util
import json
import os
import random
import sys
import tempfile
import concurrent.futures as cf

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
BAT = os.path.join(LANE, "tools/limine-pin-battery-r93.py")
LANDED = os.path.join(LANE, "tools/check-limine-pins.py")
GATES = {
    "landed": LANDED,
    "N01": os.path.join(LANE, ".ufo/waves/round-93/before/controls/bends/N01-exact-split.py"),
    "N02": os.path.join(LANE, ".ufo/waves/round-93/before/controls/bends/N02-first-body.py"),
    "N03": os.path.join(LANE, ".ufo/waves/round-93/before/controls/bends/N03-era-b-u1.py"),
    "N04": os.path.join(LANE, ".ufo/waves/round-93/before/controls/bends/N04-accept-any.py"),
    "N05": os.path.join(LANE, ".ufo/waves/round-93/before/controls/bends/N05-auto-ignore.py"),
    "N06": os.path.join(LANE, ".ufo/waves/round-93/before/controls/bends/N06-auto-fallback.py"),
}
FAMS = ["ERA-EXACT-125", "ERA-B-FIRST-BODY", "ERA-B-U1", "REFUSAL-VERSIONS",
        "AUTO-ERA-A", "AUTO-ERA-B", "AUTO-PROBE-FAIL"]
SCRATCH = "/fast/scratch/hyaku/tsukuroi-r93/ReviewBattery"

spec = importlib.util.spec_from_file_location("battery_r93", BAT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def conf_dump(c):
    out = []
    for n, raw in enumerate(c.lines, 1):
        out.append("%3d| %s" % (n, raw))
    return "\n".join(out)


def expected(c):
    rc, verdict, pins = c.finish()
    entries, panic = c.meta()
    return {
        "rc": rc, "verdict": verdict, "pins": [list(x) for x in pins],
        "entry": {str(k): v for k, v in entries.items()},
        "panic": None if panic is None else [panic[0], panic[1]],
        "on_panic": None if (c.conf_missing or c.conf_dir) else c.want_on_panic(),
        "unverified": c.want_unverified(),
        "era_b": c.era_b(), "version": c.version, "auto": c.auto,
        "limine_version(if auto ok)": (None if c.auto in (None, "fail") else c.auto),
        "limine_version_source(if auto ok)": (None if c.auto in (None, "fail") else "probe"),
    }


def observed(got):
    if got is None:
        return None
    return {"exit": got[0], "verdict": got[1], "pins": [list(x) for x in got[2]], "rc": got[3],
            "entry": {str(k): v for k, v in got[4].items()},
            "panic": None if got[5][0] == "absent" else got[5][1],
            "panic_field": got[5][0],
            "on_panic": got[6], "unverified": got[7],
            "limine_version": got[8], "limine_version_source": got[9]}


def check(gate_path, c, d, conf, esp):
    if c.usage is not None or c.auto == "fail":
        ok, rows, err = m.run_usage(gate_path, conf, esp, c, d)
        return {"kind": "usage", "ok": ok, "rows": rows, "err": err}
    want = c.finish()
    got, err = m.run_gate(gate_path, conf, esp, c, d)
    if got is None:
        return {"kind": "verdict", "match": False, "error": err, "obs": None}
    want_op = None if (c.conf_missing or c.conf_dir) else c.want_on_panic()
    checks = {
        "exit": got[0] == want[0], "rc_field": got[3] == want[0], "verdict": got[1] == want[1],
        "pins": [list(x) for x in got[2]] == [list(x) for x in want[2]],
        "r8": m.r8_ok(c, got), "u1": m.u1_ok(c, got),
        "on_panic": want_op is None or got[6] == want_op, "auto": m.auto_ok(c, got),
    }
    return {"kind": "verdict", "match": all(checks.values()), "checks": checks,
            "obs": observed(got), "error": err}


def one(fam):
    rng = random.Random(0x93A0 + FAMS.index(fam))
    root = tempfile.mkdtemp(prefix="case-", dir=SCRATCH)
    c, d, conf, esp = m.build(fam, rng, root)
    exp = expected(c)
    conf_bytes = open(conf, "rb").read() if os.path.isfile(conf) else b"<no conf>"
    fake = ""
    fp = os.path.join(d, "bin", "limine")
    if os.path.isfile(fp):
        fake = open(fp).read()
    res = {}
    with cf.ThreadPoolExecutor(max_workers=7) as ex:
        futs = {ex.submit(check, p, c, d, conf, esp): name for name, p in GATES.items()}
        for f in cf.as_completed(futs):
            res[futs[f]] = f.result()
    return {"family": fam, "dir": d, "conf": conf, "esp": esp,
            "conf_text": conf_dump(c), "conf_bytes": conf_bytes[:400].decode("utf-8", "replace"),
            "fake_limine": fake, "expected": exp, "gates": res, "case": c}


def main():
    out = {}
    for fam in FAMS:
        out[fam] = one(fam)
    with open(os.path.join(SCRATCH, "rehearse.json"), "w") as f:
        json.dump({k: {kk: vv for kk, vv in v.items() if kk != "case"} for k, v in out.items()},
                  f, indent=1, default=str)
    for fam, r in out.items():
        print("=" * 100)
        print("FAMILY", fam, "case dir", r["dir"])
        print("--- conf bytes (%d) ---" % len(r["conf_bytes"]))
        print(r["conf_text"])
        if r["fake_limine"]:
            print("--- fake limine ---")
            print(r["fake_limine"].rstrip())
        print("--- expected (Case.finish/meta/want_unverified/era_b/want_on_panic) ---")
        print(json.dumps(r["expected"], indent=1, sort_keys=True))
        for g, res in r["gates"].items():
            if res["kind"] == "usage":
                print("-- %s usage ok=%s err=%s" % (g, res["ok"], res["err"]))
                for row in res["rows"]:
                    print("   ", json.dumps(row, default=str))
            else:
                print("-- %s match=%s checks=%s err=%s" % (g, res["match"], res.get("checks"), res["error"]))
                if g == "landed" or not res["match"]:
                    print("   obs:", json.dumps(res["obs"], default=str))
    print("cases kept under", SCRATCH)


if __name__ == "__main__":
    main()
