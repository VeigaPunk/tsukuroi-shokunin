#!/usr/bin/env python3
"""Derive a proposed instrument from the committed r84 counter by adding target-literal
and per-rule refusal cases to its selftest. Writes
  $S/proposed/count-resume-rows-r84.proposed.py
and (via git diff --no-index) the patch for my wave dir. Never touches the lane."""
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
S = "/fast/scratch/hyaku/tsukuroi-r84/MutCounter"
SRC = os.path.join(LANE, "tools/count-resume-rows-r84.py")
OUT = os.path.join(S, "proposed", "count-resume-rows-r84.proposed.py")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

s = open(SRC, encoding="utf-8").read()

OLD0 = """        base = _random_entry(root, rng, TARGET_ROWS, TARGET_SNAPSHOTS)
        check("P1-random-valid-rows-met", base, 0, lambda r: r["counted"] == TARGET_ROWS)
"""
NEW0 = """        # targets as frozen literals: a lowered module constant must fail this case, not follow it
        tgt_rows, tgt_snaps = 7, 4
        cases.append({"case": "G0-frozen-target-literals",
                      "pass": (TARGET_ROWS, TARGET_SNAPSHOTS) == (tgt_rows, tgt_snaps),
                      "rc": 0, "want_rc": 0, "counted": None, "verdict": None,
                      "detail": f"{TARGET_ROWS}/{TARGET_SNAPSHOTS}"})
        base = _random_entry(root, rng, tgt_rows, tgt_snaps)
        check("P1-random-valid-rows-met", base, 0,
              lambda r: r["counted"] == tgt_rows and r["distinct_snapshots"] == tgt_snaps)
"""

OLD1 = """        e = json.loads(json.dumps(base)); e["rows"] = e["rows"][:TARGET_ROWS - 1]
        check("F6-one-row-short", e, 1, lambda r: r["counted"] == TARGET_ROWS - 1 and r["failed"] == 0)
        e = _random_entry(root, rng, TARGET_ROWS, TARGET_SNAPSHOTS - 1)
        check("F7-too-few-snapshots", e, 1, lambda r: r["failed"] == 0 and r["distinct_snapshots"] == TARGET_SNAPSHOTS - 1)
"""
NEW1 = """        e = json.loads(json.dumps(base)); e["rows"] = e["rows"][:6]
        check("F6-one-row-short", e, 1, lambda r: r["counted"] == 6 and r["failed"] == 0)
        e = _random_entry(root, rng, 7, 3)
        check("F7-too-few-snapshots", e, 1, lambda r: r["failed"] == 0 and r["distinct_snapshots"] == 3)
"""

OLD2 = """        e = json.loads(json.dumps(base)); e["rows"][0]["host"]["receipt"] = "nope"
        check("F8-undeclared-receipt", e, 1, lambda r: r["rows"][0]["reason"] == "R5-receipt-undeclared")
"""
NEW2 = OLD2 + """        # ---- G-cases: one refusal per frozen rule, each reachable by a single-entry edit
        def _lines_of(entry, k):
            p = os.path.join(root, entry["snapshots"][k]["path"])
            return open(p, encoding="utf-8", errors="replace").read().split("\\n")

        def _span(lines, n):
            for i in range(len(lines)):
                for j in range(i, min(i + 6, len(lines))):
                    w = " ".join(lines[i:j + 1]).split()
                    if len(w) < n:
                        continue
                    q = " ".join(w[:n])
                    if exact_span(lines, i + 1, j + 1, q)[0]:
                        return [i + 1, j + 1], q
            return None, None

        def _any_span(entry, n):
            for k in sorted(entry["snapshots"]):
                span, q = _span(_lines_of(entry, k), n)
                if span:
                    return k, span, q
            return None, None, None

        # G1 declared digest and manifest intact, bytes on disk differ
        e = json.loads(json.dumps(base)); k = e["rows"][0]["source"]["snapshot"]
        p = os.path.join(root, e["snapshots"][k]["path"]); orig = open(p, "rb").read()
        with open(p, "wb") as fh:
            fh.write(orig + b"\\nprobe-extra-line\\n")
        check("G1-bytes-differ-declared-intact", e, 1,
              lambda r: any(x["reason"].startswith("R3-") for x in r["rows"]))
        with open(p, "wb") as fh:
            fh.write(orig)
        # G2/G3 quote word bounds
        k, span, q = _any_span(base, 30)
        e = json.loads(json.dumps(base)); e["rows"][0]["source"].update({"snapshot": k, "lines": span, "quote": q})
        check("G2-quote-longer-than-25-words", e, 1, lambda r: r["rows"][0]["reason"] == "R4-quote-length")
        k, span, q = _any_span(base, 4)
        e = json.loads(json.dumps(base)); e["rows"][0]["source"].update({"snapshot": k, "lines": span, "quote": q})
        check("G3-quote-shorter-than-6-words", e, 1, lambda r: r["rows"][0]["reason"] == "R4-quote-length")
        # G4 statement word floor
        e = json.loads(json.dumps(base)); e["rows"][0]["statement"] = "five word statement right here"
        check("G4-short-statement", e, 1, lambda r: r["rows"][0]["reason"] == "R2-statement")
        # G5 duplicate id
        e = json.loads(json.dumps(base)); e["rows"][6]["id"] = e["rows"][0]["id"]
        check("G5-duplicate-id", e, 1,
              lambda r: r["counted"] == 5 and r["failed"] == 2
              and any(x["reason"] == "R1-duplicate-id" for x in r["rows"]))
        # G6 snapshot url scheme
        e = json.loads(json.dumps(base)); k = e["rows"][0]["source"]["snapshot"]
        e["snapshots"][k]["url"] = "http://example.invalid/" + os.path.basename(e["snapshots"][k]["path"])
        check("G6-snapshot-url-not-https", e, 1,
              lambda r: any(x["reason"] == "R3-snapshot-url-not-https" for x in r["rows"]))
        # G7 a full count beside one failed row must refuse "met" (8 rows: 7 count, 1 fails)
        e = _random_entry(root, rng, 8, 4)
        e["rows"][0]["source"]["quote"] = "this sentence was never written in any pinned snapshot here"
        check("G7-counted-with-one-failed", e, 1, lambda r: r["counted"] == 7 and r["failed"] == 1)
        # G8 R6 span half: same raw span, a different quote inside it
        hit = None
        for kk in sorted(base["snapshots"]):
            ls = _lines_of(base, kk)
            for i, line in enumerate(ls):
                w = line.split()
                if len(w) >= 12 and " ".join(w[:6]) != " ".join(w[6:12]):
                    hit = (kk, i + 1, " ".join(w[:6]), " ".join(w[6:12]))
                    break
            if hit:
                break
        e = json.loads(json.dumps(base))
        kk, ln, q1, q2 = hit
        e["rows"][0]["source"].update({"snapshot": kk, "lines": [ln, ln], "quote": q1})
        e["rows"][1]["source"].update({"snapshot": kk, "lines": [ln, ln], "quote": q2})
        check("G8-same-span-different-quote", e, 1,
              lambda r: r["rows"][1]["reason"] == "R6-duplicate-quote-or-span")
        # G9 empty host value
        e = json.loads(json.dumps(base)); e["rows"][0]["host"]["value"] = ""
        check("G9-empty-host-value", e, 1, lambda r: r["counted"] == 6 and r["failed"] == 1)
"""

for old, new in ((OLD0, NEW0), (OLD1, NEW1), (OLD2, NEW2)):
    assert s.count(old) == 1, ("anchor", s.count(old), old[:60])
    s = s.replace(old, new, 1)

open(OUT, "w", encoding="utf-8").write(s)
print("wrote", OUT)
p = subprocess.run(["git", "diff", "--no-index", "--unified=3", "--", SRC, OUT], capture_output=True, text=True)
patch = p.stdout.replace(SRC, "a/tools/count-resume-rows-r84.py").replace(OUT, "b/tools/count-resume-rows-r84.py")
open(os.path.join(S, "proposed", "count-resume-rows-r84.patch"), "w", encoding="utf-8").write(patch)
print("diff lines:", len(patch.splitlines()))
