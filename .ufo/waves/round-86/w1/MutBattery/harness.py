#!/usr/bin/env python3
"""Round-86 MutBattery: expectation mutants of resume-gate-battery-r86.py on the 10 r86 families."""
import concurrent.futures as cf
import json
import os
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(S, "battery.py")
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
BASE = os.path.join(LANE, ".ufo/waves/round-85/before/host/facts-v2.json")

MUTANTS = {}

def mut(name, *pairs):
    MUTANTS[name] = pairs

# --- M01 EMPTY-RESUME: empty last resume= expected HEALTHY (claim: it means no resume) ---
mut("M01-empty-resume-healthy",
    ('out.append(("EMPTY-RESUME", dict(f, cmdline=cl), (1, "DEGRADED", ["HR-NO-RESUME-ARG"]), {"suppressed": c_ids}))',
     'out.append(("EMPTY-RESUME", dict(f, cmdline=cl), (0, "HEALTHY", []), {"suppressed": c_ids}))'))
# --- M02 OFFSET-SSCANF: expect rc2 CANNOT-EVALUATE (the r85 gate's answer) ---
mut("M02-offset-sscanf-rc2",
    ('out.append(("OFFSET-SSCANF", dict(b, cmdline=cl), (0, "HEALTHY", []), {"kind": kind}))',
     'out.append(("OFFSET-SSCANF", dict(b, cmdline=cl), (2, "CANNOT-EVALUATE", []), {"kind": kind}))'))
# --- M03 MULTI-SWAP: image_size <= max single free, still expected HEALTHY (claim: sum counts) ---
mut("M03-multi-swap-max-single",
    ('image_size=rng.randint(max(frees) + 1, total)),\n                    (0, "HEALTHY", []), {}))',
     'image_size=rng.randint(1, max(frees))),\n                    (0, "HEALTHY", []), {}))'))
# --- M04 DECOYS-R86: a real noresume=1 joins the decoys, still expected HEALTHY ---
mut("M04-decoys-real-noresume",
    ('pool = ["no_resume", "noresum", "nohibernat", "x" + "noresume", "y" + "nohibernate",',
     'pool = ["no_resume", "noresum", "nohibernat", "noresume=1", "x" + "noresume", "y" + "nohibernate",'))
# --- M05 DECOYS-R86: omit xnoresume (substring-match decoy) ---
mut("M05-decoys-no-xnoresume",
    ('pool = ["no_resume", "noresum", "nohibernat", "x" + "noresume", "y" + "nohibernate",',
     'pool = ["no_resume", "noresum", "nohibernat", "y" + "nohibernate",'))
# --- M06 OFFSET-DUP wrong-first: expect DEGRADED mismatches (claim: last wins) ---
mut("M06-offset-dup-first-wins",
    ('out.append(("OFFSET-DUP", dict(b, cmdline=put_before(b["cmdline"], "resume_offset=", f"resume_offset={wrong}")),\n                    (0, "HEALTHY", []), {"order": "wrong-first"}))',
     'out.append(("OFFSET-DUP", dict(b, cmdline=put_before(b["cmdline"], "resume_offset=", f"resume_offset={wrong}")),\n                    (1, "DEGRADED", ["HR-OFFSET-MISMATCH", "HR-SYSFS-OFFSET-MISMATCH"]), {"order": "wrong-first"}))'))
# --- M07 NOHIB-VALUED: expect only HR-NORESUME-ARG (claim: nohibernate wins over noresume) ---
mut("M07-nohib-valued-noresume-arg",
    ('(1, "DEGRADED", ["HR-HIBERNATE-DISABLED"]), {"tokens": extra}))',
     '(1, "DEGRADED", ["HR-NORESUME-ARG"]), {"tokens": extra}))'))
# --- M08 NORESUME-VALUED: expect HEALTHY (claim: noresume=<v> still counts) ---
mut("M08-noresume-valued-healthy",
    ('(1, "DEGRADED", ["HR-NORESUME-ARG"]), {"token": "noresume" + v}))',
     '(0, "HEALTHY", []), {"token": "noresume" + v}))'))
# --- M09 HIBERNATE-NOX: hibernate=nocompress<sfx> expected DEGRADED (claim: nocompress is exempt) ---
mut("M09-hib-nocompress-degraded",
    ('("nocompress", (0, "HEALTHY", []))):',
     '("nocompress", (1, "DEGRADED", ["HR-HIBERNATE-DISABLED"]))):'))
# --- M10 SWAP-BOUNDARY: image_size == free+1 expected HEALTHY (claim: strict <) ---
mut("M10-swap-boundary-off-by-one",
    ('out.append(("SWAP-BOUNDARY", dict(b, image_size=free + 1), (1, "DEGRADED", ["HR-SWAP-TOO-SMALL"]), {}))',
     'out.append(("SWAP-BOUNDARY", dict(b, image_size=free + 1), (0, "HEALTHY", []), {}))'))
# --- M11 BOOL-FOR-INT: expect HEALTHY (claim: bool is not int) ---
mut("M11-bool-for-int-healthy",
    ('out.append(("BOOL-FOR-INT", f, (2, "CANNOT-EVALUATE", []), {"field": field}))',
     'out.append(("BOOL-FOR-INT", f, (0, "HEALTHY", []), {"field": field}))'))
# --- M12 drop the NORESUME-VALUED case entirely (family goes to zero cases) ---
mut("M12-noresume-family-dropped",
    ('out.append(("NORESUME-VALUED", dict(b, cmdline=add_tokens(b["cmdline"], rng, "noresume" + v)),\n                (1, "DEGRADED", ["HR-NORESUME-ARG"]), {"token": "noresume" + v}))',
     'pass  # M12: NORESUME-VALUED case dropped'))
# --- M13 OFFSET-SSCANF: drop the dash spelling case ---
mut("M13-offset-sscanf-no-dash",
    ('("digit-prefix", replace_tok(b["cmdline"], "resume_offset=", f"resume_offset={o}{word(rng, 3)}")),\n                         ("dash", replace_tok(b["cmdline"], "resume_offset=", f"resume-offset={o}"))):',
     '("digit-prefix", replace_tok(b["cmdline"], "resume_offset=", f"resume_offset={o}{word(rng, 3)}"))):'))
# --- M14 NORESUME-VALUED: bare noresume only, valued spellings gone ---
mut("M14-noresume-bare-only",
    ('v = rng.choice(["=1", "=0", "=" + word(rng, 3), "_" + word(rng, 3), word(rng, 2), "="])\n    out.append(("NORESUME-VALUED"',
     'v = ""\n    out.append(("NORESUME-VALUED"'))
# --- M15 NOHIB-VALUED: bare nohibernate only, valued spellings gone ---
mut("M15-nohib-bare-only",
    ('v = rng.choice(["=1", "=0", "=" + word(rng, 3), "_" + word(rng, 3), word(rng, 2)])\n    extra = ["nohibernate" + v] + ([rng.choice(["noresume=1", "noresume"])] if rng.random() < .5 else [])',
     'v = ""\n    extra = ["nohibernate" + v]'))
# --- M16 SWAP-BOUNDARY: both boundary cases gated off ---
mut("M16-swap-boundary-dropped",
    ('    if free > 0:\n        out.append(("SWAP-BOUNDARY"',
     '    if False:\n        out.append(("SWAP-BOUNDARY"'))


def build(name):
    src = open(SRC, encoding="utf-8").read()
    for old, new in MUTANTS[name]:
        if src.count(old) != 1:
            raise SystemExit(f"{name}: anchor count {src.count(old)} for {old[:60]!r}")
        src = src.replace(old, new)
    p = os.path.join(S, "mutants", name + ".py")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(src)
    return p


def run(battery, gate, tag):
    out = os.path.join(S, "out", f"{tag}.json")
    r = subprocess.run([sys.executable, battery, "--gate", gate, "--base", BASE, "--random", "5",
                        "--out", out], capture_output=True, text=True, cwd=LANE)
    try:
        res = json.load(open(out, encoding="utf-8"))
    except Exception:
        return {"tag": tag, "rc": r.returncode, "err": r.stderr[-400:], "summary": None}
    return {"tag": tag, "rc": r.returncode,
            "passed": res["families_passed"], "total": res["families_total"],
            "failed": res["failed_families"], "cases": res["cases"]}


def main():
    os.makedirs(os.path.join(S, "out"), exist_ok=True)
    built = {n: build(n) for n in MUTANTS}
    jobs = []
    jobs.append(("pristine", SRC))
    jobs += [(n, built[n]) for n in MUTANTS]
    gates = {"candidate": os.path.join(S, "gates/candidate.py"), "K1": os.path.join(S, "gates/K1.py")}
    work = [(b, g, f"{b}--{g}") for b in [j[0] for j in jobs] for g in gates]
    pathof = dict(jobs)
    with cf.ThreadPoolExecutor(max_workers=14) as ex:
        futs = {ex.submit(run, pathof[b], gates[g], t): (b, g) for b, g, t in work}
        res = {}
        for f in cf.as_completed(futs):
            r = f.result()
            res[futs[f]] = r
    table = {}
    for b, _g, t in work:
        table[t] = res[(b, _g)]
    print(json.dumps(table, indent=1, sort_keys=True))
    json.dump(table, open(os.path.join(S, "out", "table.json"), "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
