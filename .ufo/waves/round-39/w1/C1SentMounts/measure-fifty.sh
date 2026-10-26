#!/usr/bin/env bash
# Measure the 50 MB mount-table cost: elapsed, peak RSS across the census process tree.
set -uo pipefail
S=/fast/scratch/hyaku/tsukuroi-r39/C1SentMounts
cd "$S"
rm -rf "$S/work" "$S/tmp"; mkdir -p "$S/tmp"
KEEP_WORK=1 ./harness.sh fifty-mb 300 > "$S/fifty.txt" 2>&1 &
HPID=$!
desc() { local p=$1 c; for c in $(pgrep -P "$p"); do echo "$c"; desc "$c"; done; }
HWM=0; CENSUS_SEEN=''
while kill -0 "$HPID" 2>/dev/null; do
  for p in $(desc "$HPID"); do
    cmd=$(tr '\0' ' ' < "/proc/$p/cmdline" 2>/dev/null)
    case "$cmd" in *tools/tsukuroi-census.sh*) CENSUS_SEEN="$p" ;; esac
    v=$(awk '/VmHWM/{print $2}' "/proc/$p/status" 2>/dev/null)
    if [ -n "${v:-}" ] && [ "$v" -gt "$HWM" ]; then HWM=$v; HWMPID=$p; fi
  done
  sleep 0.2
done
echo "peak_VmHWM_kB=$HWM pid=$HWMPID last_census_pid=$CENSUS_SEEN"
echo "--- tmpdir after run ---"; ls -la "$S/tmp" | head -5
wait "$HPID"; echo "harness_rc=$?"
echo "--- result ---"; cat "$S/fifty.txt"
