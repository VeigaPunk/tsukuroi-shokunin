#!/usr/bin/env bash
# C1MutOctal: mutant M2 run — zero test `[[ $v =~ ^0+$ ]]` -> `(( v > 0 ))`
# PRECONDITION: clone worktree already carries the M2 edit (applied via edit tool).
set -u
S=/fast/scratch/hyaku/tsukuroi-r38/C1MutOctal
D=$S/clone; OUT=$S/out
export TMPDIR="$S/tmp"; mkdir -p "$TMPDIR" "$OUT"
REV=52ffd65f868431f021b8615ab281efd87195eac6
echo "driver bash: $(bash --version | head -n1)"

sha256sum "$D/tools/tsukuroi-census.sh" > "$OUT/m2-worktree.sha"

( cd "$D" && bash tools/tsukuroi-census.sh --selftest ) > "$OUT/selftest-m2.txt" 2>&1
echo "selftest-m2 exit=$?" >> "$OUT/selftest-m2.txt"

# direct capture: reproduce the selftest storage-nonzero fixture, grab the mutant's STORAGE line
FXD="$S/tmp/fx-m2-nonzero"; rm -rf "$FXD"
mkdir -p "$FXD/btrfs/11111111-2222-3333-4444-555555555555/devinfo/1" "$FXD/btrfs/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/devinfo/2"
printf 'write_errs 1\nread_errs 0\nflush_errs 0\ncorruption_errs 3\ngeneration_errs 0\n' > "$FXD/btrfs/11111111-2222-3333-4444-555555555555/devinfo/1/error_stats"
printf 'write_errs 0\nread_errs 0\nflush_errs 0\ncorruption_errs 0\ngeneration_errs 010\n' > "$FXD/btrfs/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/devinfo/2/error_stats"
( cd "$D" && TSUKUROI_BTRFS_SYSFS="$FXD/btrfs" bash tools/tsukuroi-census.sh ) > "$OUT/m2-storage-nonzero-direct.txt" 2>&1
grep '^STORAGE ' "$OUT/m2-storage-nonzero-direct.txt" > "$OUT/m2-storage-line.txt" || true

git -C "$D" add tools/tsukuroi-census.sh
git -C "$D" -c user.name='C1MutOctal scratch' -c user.email='c1mutoctal@scratch.invalid' -c commit.gpgsign=false commit -q -m 'MUTANT M2 (C1MutOctal): zero test [[ $v =~ ^0+$ ]] -> (( v > 0 ))'
M2=$(git -C "$D" rev-parse HEAD)
echo "$M2" > "$OUT/m2.sha"
git -C "$D" show "$M2:tools/tsukuroi-census.sh" | sha256sum > "$OUT/m2-committed.sha"
git -C "$D" diff "$REV" "$M2" -- tools/tsukuroi-census.sh > "$OUT/m2.diff"

python3 "$D/tools/score-storage-arm-r38.py" --repo "$D" --revision "$M2" --branch mut --scratch "$S/counter-m2" > "$OUT/counter-m2.json" 2>&1
echo "counter-m2 exit=$?" >> "$OUT/counter-m2.json"
python3 "$S/q82-counter.py" --repo "$D" --revision "$M2" --branch mut --scratch "$S/q82-m2" > "$OUT/q82-m2.json" 2>&1
echo "q82-m2 exit=$?" >> "$OUT/q82-m2.json"

git -C "$D" checkout -q "$REV" -- tools/tsukuroi-census.sh
if cmp -s "$S/census-pristine.sh" "$D/tools/tsukuroi-census.sh"; then echo "RESTORED-OK" > "$OUT/m2-restored.sha"; else echo "RESTORE-MISMATCH" > "$OUT/m2-restored.sha"; fi
sha256sum "$D/tools/tsukuroi-census.sh" >> "$OUT/m2-restored.sha"

echo "--- M2 sha: $(cat "$OUT/m2.sha")"
echo "--- selftest tail:"; tail -n 4 "$OUT/selftest-m2.txt"
echo "--- selftest FAIL count: $(grep -c '^FAIL ' "$OUT/selftest-m2.txt" || true)"
echo "--- mutant STORAGE line (storage-nonzero fixture):"; cat "$OUT/m2-storage-line.txt"
echo "--- counter verdict:"; grep -E '"(result|fixtures_matched|live_match|six_planes_all|error)"' "$OUT/counter-m2.json" || tail -n 5 "$OUT/counter-m2.json"
echo "--- q82 verdict:"; grep -E '"(result|ns_views_matched|ns_available|error)"' "$OUT/q82-m2.json" || tail -n 5 "$OUT/q82-m2.json"
echo "--- restore:"; cat "$OUT/m2-restored.sha"
