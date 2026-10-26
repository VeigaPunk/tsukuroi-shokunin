#!/bin/bash
# C1SentScope: SIGINT aimed at the running `--selftest` child (the longest-lived child the counter waits on).
set -u
B=/fast/scratch/hyaku/tsukuroi-r42/C1SentScope
S=$B/sig2
rm -rf -- "$S"; mkdir -p "$S"
export TMPDIR=$S
COUNTER=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-size-invariance-r42.py
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
REV=447662088dfd3155e31aed239179a79c1d1046c7

python3 "$COUNTER" --revision "$REV" --lane "$LANE" --scratch "$S/s" >"$S/out" 2>"$S/err" &
pid=$!
echo "counter pid=$pid" > "$S/log"
found=''
for i in $(seq 1 3000); do
  for c in $(cat /proc/"$pid"/task/"$pid"/children 2>/dev/null); do
    cl=$(tr '\0' ' ' < /proc/"$c"/cmdline 2>/dev/null)
    case "$cl" in *--selftest*) found=$c; echo "selftest child pid=$c at iter=$i cmd=$cl" >> "$S/log"; break 2;; esac
  done
  kill -0 "$pid" 2>/dev/null || { echo "counter exited before selftest appeared" >> "$S/log"; break; }
  sleep 0.1
done
if [ -n "$found" ]; then
  sleep 2
  echo "sigint at $(date -Is); selftest child alive=$(kill -0 "$found" 2>/dev/null && echo yes || echo no)" >> "$S/log"
  find "$S/s" -maxdepth 3 -printf '%y %p\n' 2>/dev/null | sort | head -30 >> "$S/log"
  kill -INT "$pid"
  t0=$(date +%s%N)
  for i in $(seq 1 3000); do kill -0 "$pid" 2>/dev/null || break; sleep 0.1; done
  t1=$(date +%s%N)
  echo "counter exit latency after SIGINT: $(( (t1-t0)/1000000 )) ms" >> "$S/log"
  wait "$pid"; echo "counter_exit=$?" >> "$S/log"
  echo "after exit $(date -Is): scratch root present=$(ls -d "$S"/s/size-inv-r42.* 2>/dev/null | wc -l) entries in s=$(ls -A "$S/s" | wc -l)" >> "$S/log"
  echo "selftest child after counter exit: $(kill -0 "$found" 2>/dev/null && echo ALIVE || echo gone)" >> "$S/log"
  if kill -0 "$found" 2>/dev/null; then
    tr '\0' ' ' < /proc/"$found"/cmdline >> "$S/log"; echo >> "$S/log"
    echo "  cwd=$(readlink /proc/$found/cwd 2>/dev/null)" >> "$S/log"
    # it is my own child of my own counter: stop it by PID after recording it
    kill -TERM "$found" 2>/dev/null; sleep 2
    echo "  after TERM: $(kill -0 "$found" 2>/dev/null && echo still-alive || echo gone)" >> "$S/log"
  fi
fi
cat "$S/log"
