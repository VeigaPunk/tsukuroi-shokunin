#!/usr/bin/env bash
# Precise FIFO-table hang trace. Kills only its own descendants.
set -uo pipefail
S=/fast/scratch/hyaku/tsukuroi-r39/C1SentMounts
cd "$S"
rm -rf "$S/work"
./harness.sh fifo 20 > "$S/fifo-run.txt" 2>&1 &
HPID=$!
sleep 3
echo "harness pid=$HPID"
pstree -ap "$HPID" 2>/dev/null || true
desc() { local p=$1 c; for c in $(pgrep -P "$p"); do echo "$c"; desc "$c"; done; }
ALL=$(desc "$HPID")
for p in $ALL; do
  echo "--- pid=$p cmd=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null | cut -c1-120)"
  echo "    state=$(awk '{print $3}' /proc/$p/stat 2>/dev/null) wchan=$(cat /proc/$p/wchan 2>/dev/null) syscall=$(cat /proc/$p/syscall 2>/dev/null | awk '{print $1}')"
  ls -l /proc/$p/fd 2>/dev/null | grep -E 'mounts|fifo' || true
done
echo "=== kill own tree ==="
for p in $ALL; do kill -TERM "$p" 2>/dev/null; done
kill -TERM "$HPID" 2>/dev/null
wait "$HPID" 2>/dev/null
echo "rc_after_kill=$?"
