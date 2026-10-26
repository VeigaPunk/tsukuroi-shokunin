#!/usr/bin/env bash
# Run the implementation, hybrid and five single-revert variants through --selftest.
# One run at a time (the host is shared); each run's full transcript is kept in logs/.
set -uo pipefail
cd /fast/scratch/hyaku/tsukuroi-r42/C1ExecAbleToFail || exit 90
export TMPDIR=$PWD/tmp
mkdir -p "$TMPDIR" logs
for f in hybrid-census.sh v1-test692-census.sh v2-note694-census.sh v3-qu-census.sh v4-sup-census.sh v5-suu-census.sh; do
  name=${f%-census.sh}
  echo "=== diff impl -> $name (line counts) ==="
  diff --unified=0 impl-census.sh "$f" | grep -c '^[-+][^-+]' || true
done
run() { # run LABEL FILE
  local label=$1 file=$2 rc
  echo "===== RUN $label ($file) ====="
  bash "$file" --selftest > "logs/$label.log" 2>&1
  rc=$?
  echo "exit=$rc"
  grep -E '^(PASS|FAIL|TSUKUROI_CENSUS_SELFTEST)' "logs/$label.log" | grep -vE '^PASS .*\(exit ' | head -5
  echo "--- selftest summary: $(grep -E '^TSUKUROI_CENSUS_SELFTEST' "logs/$label.log")"
  echo "--- failing cases:"
  grep -E '^FAIL ' "logs/$label.log" || echo '(none)'
  echo
}
run impl impl-census.sh
run hybrid hybrid-census.sh
run v1-test692 v1-test692-census.sh
run v2-note694 v2-note694-census.sh
run v3-qu v3-qu-census.sh
run v4-sup v4-sup-census.sh
run v5-suu v5-suu-census.sh
echo "ALL RUNS DONE"
