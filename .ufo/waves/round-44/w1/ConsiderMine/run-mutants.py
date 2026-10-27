#!/usr/bin/env python3
"""Run every mutant through seat-harm-log.py and record kill/survival."""
import json
import subprocess
import sys

HERE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w1/ConsiderMine"
rows, killed, survived = [], 0, []
for line in open(HERE + "/mutants/index.jsonl", encoding="utf-8"):
    item = json.loads(line)
    proc = subprocess.run(
        [sys.executable, HERE + "/seat-harm-log.py", "--log", item["path"], "--json"],
        capture_output=True, text=True)
    try:
        doc = json.loads(proc.stdout)
    except json.JSONDecodeError:
        rows.append({"mutant": item["mutant"], "exit": proc.returncode,
                     "expected": item["expected"], "observed": [], "error": proc.stderr[-200:]})
        survived.append(item["mutant"])
        continue
    codes = sorted({f["code"] for f in doc["findings"]})
    hit = item["expected"] in codes
    rows.append({"mutant": item["mutant"], "row": item["row"], "field": item["field"],
                 "exit": proc.returncode, "expected": item["expected"],
                 "observed": codes, "killed": hit and proc.returncode == 1})
    if hit and proc.returncode == 1:
        killed += 1
    else:
        survived.append(item["mutant"])
base = subprocess.run([sys.executable, HERE + "/seat-harm-log.py",
                       "--log", HERE + "/seat-harm.jsonl", "--json"],
                      capture_output=True, text=True)
base_doc = json.loads(base.stdout) if base.stdout else {}
print(f"baseline exit={base.returncode} rows={base_doc.get('summary', {}).get('rows')} "
      f"findings={base_doc.get('summary', {}).get('findings')}")
for r in rows:
    print(f"{r['mutant']}\texit={r['exit']}\texpected={r['expected']}\t"
          f"killed={r.get('killed')}\tobserved={','.join(r['observed'])}")
print(f"killed={killed}/{len(rows)} survived={survived or 'none'}")
with open(HERE + "/mutants/results.json", "w", encoding="utf-8") as fh:
    json.dump({"baseline_exit": base.returncode,
               "baseline_findings": base_doc.get("summary", {}).get("findings"),
               "mutants": len(rows), "killed": killed,
               "survived": survived, "rows": rows}, fh, indent=1)
sys.exit(0 if killed == len(rows) and base.returncode == 0 else 1)
