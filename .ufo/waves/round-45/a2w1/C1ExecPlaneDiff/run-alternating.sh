#!/usr/bin/env bash
# C1ExecPlaneDiff item C1-4: run both census revisions back to back on the live host,
# three alternating rounds (b i b i b i), capture stdout/stderr/exit code, time each run.
set -uo pipefail
S=/fast/scratch/hyaku/tsukuroi-r45/C1ExecPlaneDiff/fresh
export TMPDIR="$S/tmp"
mkdir -p "$TMPDIR"
cd "$S"
: > runlog.txt
for i in 1 2 3; do
  for rev in base impl; do
    case $rev in
      base) script=$S/census-base.sh ;;
      impl) script=$S/census-impl.sh ;;
    esac
    f=$S/run-$rev-$i.out
    t0=$(date +%s%N)
    "$script" >"$f" 2>"$S/run-$rev-$i.err"
    rc=$?
    t1=$(date +%s%N)
    printf '%s run%s rc=%s dur_ms=%s lines=%s bytes=%s sha256=%s\n' \
      "$rev" "$i" "$rc" "$(( (t1 - t0) / 1000000 ))" "$(wc -l <"$f")" "$(wc -c <"$f")" "$(sha256sum "$f" | cut -d' ' -f1)" >> runlog.txt
  done
done
cat runlog.txt
