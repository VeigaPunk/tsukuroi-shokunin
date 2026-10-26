#!/bin/bash
# C1SentScope: SIGINT scratch-removal probe for score-size-invariance-r42.py.
# Sends SIGINT to the counter's own PID only (~20 s in); records pre/post scratch state.
set -u
B=/fast/scratch/hyaku/tsukuroi-r42/C1SentScope
S=$B/sig
rm -rf -- "$S"; mkdir -p "$S"
export TMPDIR=$S
COUNTER=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-size-invariance-r42.py
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
REV=447662088dfd3155e31aed239179a79c1d1046c7

date -Is > "$S/started"
python3 "$COUNTER" --revision "$REV" --lane "$LANE" --scratch "$S/s" \
  >"$S/out" 2>"$S/err" &
pid=$!
echo "$pid" > "$S/counter.pid"

sleep 20
date -Is > "$S/sigint.at"
{ echo "counter pid=$pid alive=$(kill -0 "$pid" 2>/dev/null && echo yes || echo no)"
  echo "children: $(cat /proc/"$pid"/task/"$pid"/children 2>/dev/null)"
  echo "--- scratch tree at 20 s ---"
  find "$S" -maxdepth 3 -printf '%y %s %p\n' 2>/dev/null | sort | head -60
  du -sh "$S/s" 2>/dev/null
} > "$S/pre-sigint.txt" 2>&1
cp -a "$S/pre-sigint.txt" "$B/pre-sigint.txt"

kill -INT "$pid"
# the counter's own Popen() waits for its census child; allow it to finish.
wait "$pid"; rc=$?
echo "counter_exit=$rc" > "$S/result.txt"
date -Is >> "$S/result.txt"
{ echo "--- after exit ---"
  echo "counter dir present: $(test -e "$S/s" && echo yes || echo no)"
  find "$S/s" -maxdepth 3 -printf '%y %p\n' 2>/dev/null | sort | head -40
  echo "--- orphan check ---"
  for c in $(cat "$B/pre-sigint.txt" | sed -n 's/^children: //p'); do
    if kill -0 "$c" 2>/dev/null; then echo "orphan alive: $c $(tr '\0' ' ' < /proc/"$c"/cmdline 2>/dev/null)"; else echo "child gone: $c"; fi
  done
} >> "$S/result.txt" 2>&1
cat "$S/result.txt"
