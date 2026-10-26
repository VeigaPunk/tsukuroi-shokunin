#!/usr/bin/env bash
# C1MutUuid mutant leg: commit the edited census in the scratch clone, run detector, restore.
# usage: phase-mut.sh LABEL
set -uo pipefail
S=/fast/scratch/hyaku/tsukuroi-r38/C1MutUuid
export TMPDIR="$S"
LOG="$S/logs"; mkdir -p "$LOG"
D="$S/clone/lane"
REV=52ffd65f868431f021b8615ab281efd87195eac6
LABEL=${1:?label}
TL=$(git -C "$D" rev-parse --show-toplevel)
if [ "$TL" != "$D" ]; then echo "TOPLEVEL-MISMATCH got=$TL want=$D"; exit 3; fi
echo "--- $LABEL diff (unstaged) ---"
git -C "$D" diff -- tools/tsukuroi-census.sh
MH=$(sha256sum "$D/tools/tsukuroi-census.sh" | awk '{print $1}')
echo "$LABEL census worktree sha256=$MH" | tee "$LOG/$LABEL-hash.txt"
git -C "$D" add -A && git -C "$D" commit -q -m "mutant $LABEL: C1MutUuid mutation probe" || { echo "COMMIT-FAILED"; exit 3; }
MREV=$(git -C "$D" rev-parse HEAD)
MB=$(git -C "$D" show "$MREV:tools/tsukuroi-census.sh" | sha256sum | awk '{print $1}')
echo "$LABEL commit=$MREV blob-sha256=$MB" | tee -a "$LOG/$LABEL-hash.txt"
echo "--- $LABEL selftest ---"
st=0
( cd "$D" && bash tools/tsukuroi-census.sh --selftest ) > "$LOG/$LABEL-selftest.out" 2> "$LOG/$LABEL-selftest.err" || st=$?
echo "$LABEL selftest exit=$st :: $(tail -1 "$LOG/$LABEL-selftest.out")"
echo "$LABEL selftest FAIL-lines:"
grep '^FAIL ' "$LOG/$LABEL-selftest.out" || echo "  (none)"
echo "--- $LABEL counter ---"
ct=0
python3 "$D/tools/score-storage-arm-r38.py" --repo "$D" --revision "$MREV" --scratch "$S" \
  > "$LOG/$LABEL-counter.json" 2> "$LOG/$LABEL-counter.err" || ct=$?
echo "$LABEL counter exit=$ct"
python3 - "$LOG/$LABEL-counter.json" "$LABEL" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print(json.dumps({k: d.get(k) for k in ("counter","revision","fixtures_expected","fixtures_matched","live_match","six_planes_all","result","exit","error")}))
for f in d.get("fixtures", []):
    if not f.get("match"):
        print("MISMATCH", json.dumps(f))
print("live:", json.dumps(d.get("live")))
PY
echo "--- restore ---"
git -C "$D" checkout -q -B master "$REV" || { echo "RESTORE-FAILED"; exit 3; }
RH=$(git -C "$D" show master:tools/tsukuroi-census.sh | sha256sum | awk '{print $1}')
WH=$(sha256sum "$D/tools/tsukuroi-census.sh" | awk '{print $1}')
echo "restored master blob sha256=$RH worktree sha256=$WH"
echo "restored status entries: $(git -C "$D" status --porcelain | wc -l)"
if [ "$RH" = "8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c" ] && [ "$WH" = "$RH" ]; then
  echo "RESTORE-VERIFIED bytes identical to pristine 52ffd65 blob"
else
  echo "RESTORE-DIVERGED"
fi
