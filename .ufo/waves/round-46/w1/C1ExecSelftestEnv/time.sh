#!/usr/bin/env bash
# Interleaved A/B timing: base 2042117c vs impl a4477049, 3 pairs, default locale,
# space-free TMPDIR. Reports per-run wall ms and case counts.
S=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv
R=$S/receipts
mkdir -p "$R" "$S/tmpdefault"
: > "$R/timing.tsv"
for i in 1 2 3; do
  for rev in base impl; do
    t0=$(date +%s%N)
    env TMPDIR="$S/tmpdefault" bash "$S/$rev/tsukuroi-census.sh" --selftest > "$R/tm-$rev-$i.out" 2>&1
    rc=$?
    t1=$(date +%s%N)
    line=$(grep -E '^TSUKUROI_CENSUS_SELFTEST:' "$R/tm-$rev-$i.out")
    printf '%s\t%d\t%d\t%s\t%s\n' "$rev" "$i" "$(( (t1-t0)/1000000 ))" "$rc" "$line" | tee -a "$R/timing.tsv"
  done
done
echo TIMING_DONE
