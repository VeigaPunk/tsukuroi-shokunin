#!/usr/bin/env bash
# Round-91 C1 freeze controls: every gate in gates/ through the frozen r91 battery, 3 runs each.
# Usage: run-controls.sh LANE_ROOT LAYOUT_LABEL SCRATCH
# LANE_ROOT is the lane checkout or a `git clone --shared` of it (the battery and the gates are read
# from it); receipts go to <this dir>/runs-<LAYOUT_LABEL>/ and summary-<LAYOUT_LABEL>.txt.
set -euo pipefail
lane=$1 label=$2 scratch=$3
here=$(cd "$(dirname "$0")" && pwd)
out="$here/runs-$label"
mkdir -p "$out" "$scratch"
battery="$lane/tools/limine-pin-battery-r91.py"
gates="$lane/.ufo/waves/round-91/before/controls/gates"
{
  echo "# r91 C1 controls, layout=$label lane=$lane"
  echo "# lane rev: $(git -C "$lane" rev-parse HEAD 2>/dev/null || echo n/a)"
  echo "# battery sha256: $(sha256sum "$battery" | cut -d' ' -f1)"
  echo "# date: $(date -Iseconds)"
} > "$out/HEADER.txt"
ls "$gates"/*.py | xargs -P 12 -I{} bash -c '
  g={}; n=$(basename "$g" .py)
  w=$(mktemp -d -p "'"$scratch"'")
  ( cd "$w" && python3 "'"$battery"'" --gate "$g" --runs 3 --work "$w" --json "'"$out"'/$n.json" > "'"$out"'/$n.txt" 2>&1; echo "rc=$?" >> "'"$out"'/$n.txt" )
  rm -rf -- "$w"'
python3 - "$out" "$gates/INDEX.tsv" > "$here/summary-$label.txt" <<'EOF'
import json, os, sys
out, index = sys.argv[1], sys.argv[2]
rows = [l.rstrip("\n").split("\t") for l in open(index)][1:]
print(open(os.path.join(out, "HEADER.txt")).read().rstrip())
print("name\tfamilies_passed_per_run\tverdicts\terror_cases\trc\tfailed_families(run1)\texpected_killers\tkilled_by_expected_all_runs")
for name, clause, killers in rows:
    runs = json.load(open(os.path.join(out, name + ".json")))
    rc = open(os.path.join(out, name + ".txt")).read().strip().splitlines()[-1]
    errs = sum(1 for r in runs for e in r["case_log"] if e["error"])
    exp = [] if "families" in killers else killers.split()
    killed = all(any(k in r["failed_families"] for k in exp) for r in runs) if exp else "n/a"
    print("\t".join([name, " ".join(str(r["families_passed"]) for r in runs),
                     " ".join(r["verdict"] for r in runs), str(errs), rc,
                     ",".join(runs[0]["failed_families"]), killers, str(killed)]))
EOF
cat "$here/summary-$label.txt"
