#!/bin/bash
# usage: run.sh <label> [pre-exec snippet]   env overrides: TM (TMPDIR) NOLIMIT
S=/fast/scratch/hyaku/tsukuroi-r48/TExecFdHold
label=$1; pre=${2:-:}
out=$S/logs/$label.txt
: > "$S/logs/mktemp.log"
t0=$(date +%s)
if [ -n "${TMSET:-}" ]; then
  env -i PATH="$S/stub:/usr/bin:/bin" LC_ALL=C TMPDIR="$S/dirty tmpdir" bash -c "$pre; exec bash '$S/lane/tools/tsukuroi-census.sh' --selftest" >"$out" 2>"$S/logs/$label.err"
else
  env -i PATH="$S/stub:/usr/bin:/bin" LC_ALL=C bash -c "$pre; exec bash '$S/lane/tools/tsukuroi-census.sh' --selftest" >"$out" 2>"$S/logs/$label.err"
fi
rc=$?
t1=$(date +%s)
{ echo "LABEL: $label"; echo "PRE: $pre"; echo "RC: $rc"; echo "SECONDS: $((t1-t0))";
  echo "LASTLINE: $(tail -n1 "$out")";
  echo "STDERR1: $(sed -n '1p' "$S/logs/$label.err")";
  echo "STDERR_LINES: $(wc -l < "$S/logs/$label.err")";
  echo "LINES: $(wc -l < "$out")"; } | tee "$S/logs/$label.summary"
echo "--- mktemp.log high-fd lines ---"
grep -n "fd 2[0-9][0-9]:\|-> /fast/scratch\|-> /tmp\|-> pipe\|-> socket" "$S/logs/mktemp.log" | head -30
