#!/usr/bin/env python3
"""Single-point mutation sweep over tools/count-resume-rows-r84.py (r84 w1, MutCounter seat)."""
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
S = "/fast/scratch/hyaku/tsukuroi-r84/MutCounter"
SRC = os.path.join(LANE, "tools/count-resume-rows-r84.py")
MUTDIR = os.path.join(S, "mut")
os.makedirs(MUTDIR, exist_ok=True)

MUTANTS = [
    ("M01", "drop-manifest-pin-check", "L118-120",
     '        if sha(data) != pin:\n            raise CannotEvaluate(f"manifest-pin-mismatch:{mpath}")\n',
     '        pass  # MUTANT M01: manifest pin check removed\n'),
    ("M02", "drop-bytes-vs-manifest-check", "L154-155",
     '        if sha(data) != manifests[path]:\n            return None, f"{kind}-bytes-differ-from-manifest"\n',
     '        pass  # MUTANT M02: bytes-vs-manifest check removed\n'),
    ("M03", "drop-minimal-span-check", "L108-109",
     '    if a < b and (n in norm(" ".join(lines[a:b])) or n in norm(" ".join(lines[a - 1:b - 1]))):\n'
     '        return False, "span-not-minimal"\n',
     '    if False:  # MUTANT M03: minimality not enforced\n        return False, "span-not-minimal"\n'),
    ("M04", "drop-R6-distinctness", "L205-210",
     '                    if nq in counted_quotes or span in counted_spans:\n'
     '                        reason = "R6-duplicate-quote-or-span"\n'
     '                    else:\n'
     '                        counted_quotes.add(nq)\n'
     '                        counted_spans.add(span)\n'
     '                        counted_snaps.add(src["snapshot"])\n',
     '                    counted_quotes.add(nq)\n'
     '                    counted_spans.add(span)\n'
     '                    counted_snaps.add(src["snapshot"])\n'),
    ("M05", "accept-quotes-over-25-words", "L183",
     'if not isinstance(q, str) or not (6 <= len(q.split()) <= 25):',
     'if not isinstance(q, str) or not (6 <= len(q.split())):  # MUTANT M05: no 25-word cap'),
    ("M06", "skip-host-value-span-check", "L194-197",
     '                        c, d = host.get("lines") if isinstance(host.get("lines"), list) and len(host.get("lines")) == 2 else (None, None)\n'
     '                        ok, why = exact_span(hl, c, d, v)\n'
     '                        if not ok:\n'
     '                            reason = "R5-" + why\n',
     '                        pass  # MUTANT M06: host value span not verified\n'),
    ("M07", "TARGET_SNAPSHOTS-4-to-3", "L52",
     'TARGET_SNAPSHOTS = 4\n',
     'TARGET_SNAPSHOTS = 3  # MUTANT M07\n'),
    ("M08", "counted->=-to->", "L218",
     'met = counted >= TARGET_ROWS and failed == 0',
     'met = counted > TARGET_ROWS and failed == 0  # MUTANT M08'),
    ("M09", "cannot-evaluate-rc2-to-rc1", "L229",
     'return 2, {"verdict": "cannot-evaluate", "reason": str(e), "counted": 0}',
     'return 1, {"verdict": "cannot-evaluate", "reason": str(e), "counted": 0}  # MUTANT M09'),
    ("M10", "drop-snapshot-url-https-check", "L142-143",
     '        if kind == "snapshot" and not str(d.get("url", "")).startswith("https://"):\n'
     '            return None, "snapshot-url-not-https"\n',
     '        pass  # MUTANT M10: https url check removed\n'),
    ("M11", "drop-R1-duplicate-id-check", "L172-173",
     '            elif rid in dup_ids:\n                reason = "R1-duplicate-id"\n',
     '            elif False:  # MUTANT M11: duplicate ids not refused\n                reason = "R1-duplicate-id"\n'),
    ("M12", "R2-statement-min-8-to-5-words", "L174",
     'or len(r["statement"].split()) < 8:',
     'or len(r["statement"].split()) < 5:  # MUTANT M12'),
    ("M13", "drop-failed==0-clause", "L218",
     'and failed == 0 and len(counted_snaps) >= TARGET_SNAPSHOTS',
     'and len(counted_snaps) >= TARGET_SNAPSHOTS  # MUTANT M13: failed==0 dropped'),
    ("M14", "quote-min-6-to-3-words", "L183",
     'if not isinstance(q, str) or not (6 <= len(q.split()) <= 25):',
     'if not isinstance(q, str) or not (3 <= len(q.split()) <= 25):  # MUTANT M14'),
    ("M15", "distinct-snapshots->-to->", "L218",
     'and len(counted_snaps) >= TARGET_SNAPSHOTS',
     'and len(counted_snaps) > TARGET_SNAPSHOTS  # MUTANT M15'),
    ("M16", "skip-entire-host-leg", "L190-197",
     '                if reason == "ok":\n'
     '                    hl, why = load("receipt", host.get("receipt"))\n'
     '                    v = host.get("value")\n'
     '                    if hl is None:\n'
     '                        reason = "R5-" + why\n'
     '                    elif not isinstance(v, str) or not v.strip():\n'
     '                        reason = "R5-empty-value"\n'
     '                    else:\n'
     '                        c, d = host.get("lines") if isinstance(host.get("lines"), list) and len(host.get("lines")) == 2 else (None, None)\n'
     '                        ok, why = exact_span(hl, c, d, v)\n'
     '                        if not ok:\n'
     '                            reason = "R5-" + why\n',
     '                if reason == "ok":\n                    pass  # MUTANT M16: host leg skipped entirely\n'),
    ("M17", "drop-span-upper-bound", "L101",
     '    if not (1 <= a <= b <= len(lines)):',
     '    if not (1 <= a <= b):  # MUTANT M17: no upper bound'),
    ("M18", "drop-R5-empty-value-check", "L195-196",
     '                    elif not isinstance(v, str) or not v.strip():\n'
     '                        reason = "R5-empty-value"\n',
     '                    elif False:  # MUTANT M18: empty host value accepted\n'
     '                        reason = "R5-empty-value"\n'),
]

src = open(SRC, encoding="utf-8").read()
results = []
for mid, label, where, old, new in MUTANTS:
    n = src.count(old)
    if n != 1:
        results.append({"id": mid, "label": label, "where": where, "error": f"anchor count {n}"})
        continue
    mpath = os.path.join(MUTDIR, f"{mid}-{label}.py")
    open(mpath, "w", encoding="utf-8").write(src.replace(old, new, 1))
    st_runs, st_fail_cases = [], set()
    for i in range(3):
        p = subprocess.run([sys.executable, mpath, "--selftest", "--root", "."],
                           cwd=LANE, capture_output=True, text=True, env={**os.environ, "TMPDIR": S})
        try:
            d = json.loads(p.stdout)
        except Exception:
            st_runs.append({"rc": p.returncode, "selftest": "NON-JSON", "stderr": p.stderr[-300:]})
            continue
        bad = [c["case"] for c in d.get("cases", []) if not c["pass"]]
        st_runs.append({"rc": p.returncode, "selftest": d.get("selftest"), "failed_cases": bad})
        st_fail_cases.update(bad)
    p = subprocess.run([sys.executable, mpath, "--root", "."],
                       cwd=LANE, capture_output=True, text=True, env={**os.environ, "TMPDIR": S})
    real = {"rc": p.returncode}
    try:
        d = json.loads(p.stdout)
        for k in ("verdict", "counted", "failed", "distinct_snapshots"):
            if k in d:
                real[k] = d[k]
    except Exception:
        real["stdout"] = p.stdout[-200:]
        real["stderr"] = p.stderr[-300:]
    base = {"rc": 0, "verdict": "met", "counted": 10, "failed": 0, "distinct_snapshots": 6}
    st_broken = any(r.get("rc") != 0 or r.get("failed_cases") for r in st_runs)
    real_changed = any(real.get(k) != base[k] for k in ("rc", "verdict", "counted", "failed", "distinct_snapshots"))
    verdict = "KILLED" if (st_broken or real_changed) else "SURVIVED"
    results.append({"id": mid, "label": label, "where": where, "file": os.path.relpath(mpath, S),
                    "selftest_runs": st_runs, "real": real, "verdict": verdict,
                    "killing_case": sorted(st_fail_cases), "real_changed": real_changed,
                    "selftest_broken": st_broken})
    print(f"{mid:4} {label:34} {verdict:9} killing={sorted(st_fail_cases)!r:60} real={real}", flush=True)

json.dump(results, open(os.path.join(S, "sweep-results.json"), "w"), indent=1)
print("\nKILLED:", sum(r["verdict"] == "KILLED" for r in results), "SURVIVED:",
      sum(r["verdict"] == "SURVIVED" for r in results), "of", len(results))
