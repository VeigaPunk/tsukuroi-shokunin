#!/bin/bash
# TExecCounterB replicate B: hostile ambient env, single counter run (no /usr/bin/time on host).
S=/fast/scratch/hyaku/tsukuroi-r48/TExecCounterB
W=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
OUT="$W/.ufo/waves/round-48/w2/TExecCounterB/counter.json"
mkdir -p "$S/receipts" "$S/amb space"
start=$(date +%s)
env TMPDIR="$S/amb space" HYAKU_SCRATCH="$S/hs" nice -n 10 \
  python3 "$W/tools/score-selftest-tmpdir-r48.py" \
    --revision ae99f021b76f8eb1c8805d32d80644464afb1ff6 --work "$S/w" \
  > "$OUT" 2> "$S/receipts/counter.stderr"
rc=$?
end=$(date +%s)
printf 'rc=%s\nstart=%s\nend=%s\ndur=%s\ncmd=counter --revision ae99f02 (hostile ambient: TMPDIR="$S/amb space" HYAKU_SCRATCH="$S/hs" nice -n 10)\n' \
  "$rc" "$start" "$end" "$((end-start))" > "$S/receipts/run-status.txt"
touch "$S/receipts/DONE"
