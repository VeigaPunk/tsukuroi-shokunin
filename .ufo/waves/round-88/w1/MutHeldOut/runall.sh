#!/bin/bash
# Run every mutant against both batteries, 3 runs each, stdout+JSON receipts.
set -u
S=/fast/scratch/hyaku/tsukuroi-r88/MutHeldOut
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
REC="$S/receipts"
mkdir -p "$REC" "$S/work/88" "$S/work/87"
: > "$REC/rc.txt"

run_one() {
  m="$1"; n="$(basename "$m" .py)"
  mkdir -p "$S/work/88/$n" "$S/work/87/$n"
  python3 "$LANE/tools/limine-pin-battery-r88.py" --gate "$m" --runs 3 \
      --work "$S/work/88/$n" --json "$REC/$n.r88.json" > "$REC/$n.r88.out" 2>&1
  echo "$n r88 rc=$?" >> "$REC/rc.txt"
  python3 "$LANE/tools/limine-pin-battery-r87.py" --gate "$m" --runs 3 \
      --work "$S/work/87/$n" --json "$REC/$n.r87.json" > "$REC/$n.r87.out" 2>&1
  echo "$n r87 rc=$?" >> "$REC/rc.txt"
}
export -f run_one
export S LANE REC
ls "$S"/mutants/h*.py | xargs -P 4 -I{} bash -c 'run_one "$@"' _ {}
echo DONE
