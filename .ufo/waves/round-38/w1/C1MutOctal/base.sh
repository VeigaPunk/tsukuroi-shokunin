#!/usr/bin/env bash
# C1MutOctal: pristine baseline — census --selftest, frozen v1 counter, q82 counter.
set -u
S=/fast/scratch/hyaku/tsukuroi-r38/C1MutOctal
D=$S/clone; OUT=$S/out
export TMPDIR="$S/tmp"; mkdir -p "$TMPDIR" "$OUT"
REV=52ffd65f868431f021b8615ab281efd87195eac6

( cd "$D" && bash tools/tsukuroi-census.sh --selftest ) > "$OUT/selftest-pristine.txt" 2>&1
echo "selftest-pristine exit=$?" >> "$OUT/selftest-pristine.txt"

python3 "$D/tools/score-storage-arm-r38.py" --repo "$D" --revision "$REV" --branch mut --scratch "$S/counter-pristine" > "$OUT/counter-pristine.json" 2>&1
echo "counter-pristine exit=$?" >> "$OUT/counter-pristine.json"

python3 "$S/q82-counter.py" --repo "$D" --revision "$REV" --branch mut --scratch "$S/q82-pristine" > "$OUT/q82-pristine.json" 2>&1
echo "q82-pristine exit=$?" >> "$OUT/q82-pristine.json"

echo "--- selftest tail:"; tail -n 4 "$OUT/selftest-pristine.txt"
echo "--- counter verdict:"; grep -E '"(result|fixtures_matched|live_match|six_planes_all|error)"' "$OUT/counter-pristine.json" || tail -n 5 "$OUT/counter-pristine.json"
echo "--- q82 verdict:"; grep -E '"(result|ns_views_matched|ns_available|error)"' "$OUT/q82-pristine.json" || tail -n 5 "$OUT/q82-pristine.json"
