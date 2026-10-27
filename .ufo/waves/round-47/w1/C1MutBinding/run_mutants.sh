#!/usr/bin/env bash
# Mutation-testing driver: run the committed R47 battery against each mutant counter, serialized.
set -u
BASE=/fast/scratch/hyaku/tsukuroi-r47/C1MutBinding
export HYAKU_SCRATCH="$BASE"
mkdir -p "$BASE/receipts"
for mut in "$BASE"/mutants/*.py; do
  name=$(basename "$mut" .py)
  echo "=== RUN $name $(date -u +%T) ==="
  BATTERY_OUT="$BASE/receipts/summary-$name.jsonl" \
  COUNTER="$mut" \
  python3 "$BASE/battery.py" > "$BASE/receipts/run-$name.log" 2>&1
  rc=$?
  tail -2 "$BASE/receipts/run-$name.log"
  echo "=== DONE $name rc=$rc ==="
done
echo "ALL-MUTANT-RUNS-COMPLETE"
