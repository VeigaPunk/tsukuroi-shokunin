#!/bin/bash
# Sequential flake census. One --selftest at a time. Writes only under this scratch dir.
set -u
S=/fast/scratch/hyaku/tsukuroi-r50/R50ScoutCensusFlake
cd "$S"
mkdir -p runs

run_one() {
  local rev=$1 n=$2 script=$3
  local d="$S/runs/${rev}-${n}"
  mkdir -p "$d/tmp" "$d/home" "$d/cwd"
  local start t0 t1 rc
  start=$(date -Is)
  t0=$(date +%s)
  TMPDIR="$d/tmp" HOME="$d/home" LC_ALL=C PATH=/usr/bin:/bin \
    /usr/bin/bash "$script" --selftest >"$d/stdout.txt" 2>"$d/stderr.txt"
  rc=$?
  t1=$(date +%s)
  {
    printf 'rev=%s\n' "$rev"
    printf 'n=%s\n' "$n"
    printf 'rc=%s\n' "$rc"
    printf 'elapsed_s=%s\n' "$((t1 - t0))"
    printf 'start=%s\n' "$start"
    printf 'end=%s\n' "$(date -Is)"
    printf 'script=%s\n' "$script"
  } > "$d/meta.txt"
  grep -E 'TSUKUROI_CENSUS_SELFTEST:' "$d/stdout.txt" "$d/stderr.txt" > "$d/summary.txt" || true
  grep -n -E '^FAIL ' "$d/stdout.txt" "$d/stderr.txt" > "$d/fails.txt" || true
  grep -n -E 'R50-C2' "$d/stdout.txt" "$d/stderr.txt" > "$d/r50.txt" || true
  echo "DONE ${rev}-${n} rc=${rc} elapsed=$((t1 - t0))"
  cat "$d/summary.txt"
  echo "FAIL_LINES $(wc -l < "$d/fails.txt")"
}

for i in 1 2 3 4 5; do
  run_one freeze "$i" "$S/census-freeze.sh"
done
for i in 1 2 3; do
  run_one base "$i" "$S/census-base.sh"
done
echo ALL_RUNS_DONE
