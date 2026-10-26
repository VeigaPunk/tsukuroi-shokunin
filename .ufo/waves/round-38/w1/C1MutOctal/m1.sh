#!/usr/bin/env bash
# C1MutOctal: mutant M1 run — zero test `[[ $v =~ ^0+$ ]]` -> `[ "$v" -gt 0 ]`
# PRECONDITION: clone worktree already carries the M1 edit (applied via edit tool).
set -u
S=/fast/scratch/hyaku/tsukuroi-r38/C1MutOctal
D=$S/clone; OUT=$S/out
export TMPDIR="$S/tmp"; mkdir -p "$TMPDIR" "$OUT"
REV=52ffd65f868431f021b8615ab281efd87195eac6
echo "driver bash: $(bash --version | head -n1)"

sha256sum "$D/tools/tsukuroi-census.sh" > "$OUT/m1-worktree.sha"

( cd "$D" && bash tools/tsukuroi-census.sh --selftest ) > "$OUT/selftest-m1.txt" 2>&1
echo "selftest-m1 exit=$?" >> "$OUT/selftest-m1.txt"

# direct capture: reproduce the selftest storage-nonzero fixture, grab the mutant's STORAGE line
FXD="$S/tmp/fx-m1-nonzero"; rm -rf "$FXD"
mkdir -p "$FXD/btrfs/11111111-2222-3333-4444-555555555555/devinfo/1" "$FXD/btrfs/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/devinfo/2"
printf 'write_errs 1\nread_errs 0\nflush_errs 0\ncorruption_errs 3\ngeneration_errs 0\n' > "$FXD/btrfs/11111111-2222-3333-4444-555555555555/devinfo/1/error_stats"
printf 'write_errs 0\nread_errs 0\nflush_errs 0\ncorruption_errs 0\ngeneration_errs 010\n' > "$FXD/btrfs/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/devinfo/2/error_stats"
( cd "$D" && TSUKUROI_BTRFS_SYSFS="$FXD/btrfs" bash tools/tsukuroi-census.sh ) > "$OUT/m1-storage-nonzero-direct.txt" 2>&1
grep '^STORAGE ' "$OUT/m1-storage-nonzero-direct.txt" > "$OUT/m1-storage-line.txt" || true

git -C "$D" add tools/tsukuroi-census.sh
git -C "$D" -c user.name='C1MutOctal scratch' -c user.email='c1mutoctal@scratch.invalid' -c commit.gpgsign=false commit -q -m 'MUTANT M1 (C1MutOctal): zero test [[ $v =~ ^0+$ ]] -> [ "$v" -gt 0 ]'
M1=$(git -C "$D" rev-parse HEAD)
echo "$M1" > "$OUT/m1.sha"
git -C "$D" show "$M1:tools/tsukuroi-census.sh" | sha256sum > "$OUT/m1-committed.sha"
git -C "$D" diff "$REV" "$M1" -- tools/tsukuroi-census.sh > "$OUT/m1.diff"

python3 "$D/tools/score-storage-arm-r38.py" --repo "$D" --revision "$M1" --branch mut --scratch "$S/counter-m1" > "$OUT/counter-m1.json" 2>&1
echo "counter-m1 exit=$?" >> "$OUT/counter-m1.json"
python3 "$S/q82-counter.py" --repo "$D" --revision "$M1" --branch mut --scratch "$S/q82-m1" > "$OUT/q82-m1.json" 2>&1
echo "q82-m1 exit=$?" >> "$OUT/q82-m1.json"

git -C "$D" checkout -q "$REV" -- tools/tsukuroi-census.sh
if cmp -s "$S/census-pristine.sh" "$D/tools/tsukuroi-census.sh"; then echo "RESTORED-OK" > "$OUT/m1-restored.sha"; else echo "RESTORE-MISMATCH" > "$OUT/m1-restored.sha"; fi
sha256sum "$D/tools/tsukuroi-census.sh" >> "$OUT/m1-restored.sha"

echo "--- M1 sha: $(cat "$OUT/m1.sha")"
echo "--- selftest tail:"; tail -n 4 "$OUT/selftest-m1.txt"
echo "--- selftest FAIL count: $(grep -c '^FAIL ' "$OUT/selftest-m1.txt" || true)"
echo "--- mutant STORAGE line (storage-nonzero fixture):"; cat "$OUT/m1-storage-line.txt"
echo "--- counter verdict:"; grep -E '"(result|fixtures_matched|live_match|six_planes_all|error)"' "$OUT/counter-m1.json" || tail -n 5 "$OUT/counter-m1.json"
echo "--- q82 verdict:"; grep -E '"(result|ns_views_matched|ns_available|error)"' "$OUT/q82-m1.json" || tail -n 5 "$OUT/q82-m1.json"
echo "--- restore:"; cat "$OUT/m1-restored.sha"
