#!/usr/bin/env python3
"""Additional direction mutants + candidate-gate mutants probing uncovered claims."""
import concurrent.futures as cf, json, os, subprocess, sys
S = "/fast/scratch/hyaku/tsukuroi-r86/MutBattery"
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
BASE = os.path.join(LANE, ".ufo/waves/round-85/before/host/facts-v2.json")
CTL = os.path.join(LANE, ".ufo/waves/round-86/before/controls")

BAT = {
 "M17-multi-swap-over-sum-healthy": [
   ('out.append(("MULTI-SWAP", dict(copy.deepcopy(b), swaps=sw, image_size=total + rng.randint(1, 10 ** 9)),\n                    (1, "DEGRADED", ["HR-SWAP-TOO-SMALL"]), {}))',
    'out.append(("MULTI-SWAP", dict(copy.deepcopy(b), swaps=sw, image_size=total + rng.randint(1, 10 ** 9)),\n                    (0, "HEALTHY", []), {}))')],
 "M18-offset-dup-last-healthy": [
   ('out.append(("OFFSET-DUP", dict(b, cmdline=put_after(b["cmdline"], "resume_offset=", f"resume_offset={wrong}")),\n                    (1, "DEGRADED", ["HR-OFFSET-MISMATCH", "HR-SYSFS-OFFSET-MISMATCH"]), {"order": "wrong-last"}))',
    'out.append(("OFFSET-DUP", dict(b, cmdline=put_after(b["cmdline"], "resume_offset=", f"resume_offset={wrong}")),\n                    (0, "HEALTHY", []), {"order": "wrong-last"}))')],
 "M19-empty-resume-then-value": [
   ('if rng.random() < .5:\n        cl = replace_tok(f["cmdline"], "resume=", "resume=")\n    else:\n        cl = put_after(f["cmdline"], "resume=", "resume=")',
    'cl = add_tokens(put_after(f["cmdline"], "resume=", "resume="), rng, "resume=/dev/" + word(rng, 4))'),
   ('out.append(("EMPTY-RESUME", dict(f, cmdline=cl), (1, "DEGRADED", ["HR-NO-RESUME-ARG"]), {"suppressed": c_ids}))',
    'out.append(("EMPTY-RESUME", dict(f, cmdline=cl), (0, "HEALTHY", []), {"suppressed": c_ids}))')],
}

# candidate-gate single-property mutants (defects the battery should catch)
GATE = {
 "G1-resume-first-wins": [
   ('    val = None\n    for tok in cmdline.split():\n        if matches(tok, setup):\n            val = tok[len(setup):]\n    return val',
    '    for tok in cmdline.split():\n        if matches(tok, setup):\n            return tok[len(setup):]\n    return None')],
 "G2-resume-empty-present": [
   ('    if not arg(cmdline, "resume="):  # absent, or empty: resume_file stays "" and find_resume_device fails',
    '    if arg(cmdline, "resume=") is None:  # mutant: empty resume= treated as present')],
 "G3-noresume-value-blind-exact": [
   ('        if matches(tok, "nohibernate"):\n            disabled = True  # nohibernate_setup ignores its argument\n        elif matches(tok, "noresume"):\n            noresume = True  # noresume_setup ignores its argument',
    '        if tok.replace("-", "_") == "nohibernate":\n            disabled = True\n        elif tok.replace("-", "_") == "noresume":\n            noresume = True')],
}

def build(src_path, pairs, dst):
    src = open(src_path, encoding="utf-8").read()
    for old, new in pairs:
        if src.count(old) != 1:
            raise SystemExit(f"{dst}: anchor count {src.count(old)}: {old[:50]!r}")
        src = src.replace(old, new)
    open(dst, "w").write(src)
    return dst

def run(battery, gate, tag):
    out = os.path.join(S, "out", tag + ".json")
    r = subprocess.run([sys.executable, battery, "--gate", gate, "--base", BASE, "--random", "5", "--out", out],
                       capture_output=True, text=True, cwd=LANE)
    try:
        res = json.load(open(out, encoding="utf-8"))
    except Exception:
        return {"tag": tag, "rc": r.returncode, "passed": None, "failed": ["ERR"], "err": r.stderr[-300:]}
    return {"tag": tag, "rc": r.returncode, "passed": res["families_passed"], "total": res["families_total"],
            "failed": res["failed_families"]}

os.makedirs(os.path.join(S, "gates2"), exist_ok=True)
jobs = []
for n, p in BAT.items():
    b = build(os.path.join(S, "battery.py"), p, os.path.join(S, "mutants", n + ".py"))
    jobs += [(b, os.path.join(S, "gates/candidate.py"), n + "__candidate"),
             (b, os.path.join(S, "gates/K1.py"), n + "__K1"),
             (b, os.path.join(CTL, "N06-no-dash.py"), n + "__N06"),
             (b, os.path.join(CTL, "N09-first-swap.py"), n + "__N09")]
for n, p in GATE.items():
    g = build(os.path.join(S, "gates/candidate.py"), p, os.path.join(S, "gates2", n + ".py"))
    jobs.append((os.path.join(S, "battery.py"), g, "pristine__" + n))
with cf.ThreadPoolExecutor(max_workers=12) as ex:
    futs = {ex.submit(run, *j): j[2] for j in jobs}
    res = {futs[f]: f.result() for f in cf.as_completed(futs)}
for k in sorted(res):
    r = res[k]
    print(f"{k:48s} rc={r['rc']} pass={r['passed']}/{r['total']} failed={','.join(r['failed']) or '-'}")
json.dump(res, open(os.path.join(S, "out", "matrix2.json"), "w"), indent=1, sort_keys=True)
