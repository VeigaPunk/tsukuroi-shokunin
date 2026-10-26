#!/usr/bin/env bash
# C1MutUuid phase 1: scratch clone at 52ffd65 + pristine baseline detector runs.
set -uo pipefail
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r38/C1MutUuid
REV=52ffd65f868431f021b8615ab281efd87195eac6
mkdir -p "$S"
export TMPDIR="$S"
LOG="$S/logs"; mkdir -p "$LOG"
D="$S/clone/lane"
rm -rf "$S/clone"; mkdir -p "$S/clone"
git clone -q --shared "$LANE" "$D" || { echo "CLONE-FAILED"; exit 3; }
TL=$(git -C "$D" rev-parse --show-toplevel)
if [ "$TL" != "$D" ]; then echo "TOPLEVEL-MISMATCH got=$TL want=$D"; exit 3; fi
git -C "$D" remote remove origin
git -C "$D" config user.name mut-c1uuid
git -C "$D" config user.email mut-c1uuid@fixture.invalid
git -C "$D" checkout -q -B master "$REV" || { echo "CHECKOUT-FAILED"; exit 3; }
echo "clone=$D"
echo "HEAD=$(git -C "$D" rev-parse HEAD)"
echo "branch-tip=$(git -C "$D" rev-parse --abbrev-ref HEAD) $(git -C "$D" rev-parse master)"
echo "worktree-status: [$(git -C "$D" status --porcelain | wc -l) entries]"
P=$(git -C "$D" show "$REV:tools/tsukuroi-census.sh" | sha256sum | awk '{print $1}')
echo "pristine-census-blob-sha256=$P" | tee "$LOG/pristine-hash.txt"
echo "live-sysfs-inventory:"
ls /sys/fs/btrfs 2>&1 | head -20
echo "--- pristine selftest ---"
st=0
( cd "$D" && bash tools/tsukuroi-census.sh --selftest ) > "$LOG/pristine-selftest.out" 2> "$LOG/pristine-selftest.err" || st=$?
echo "pristine selftest exit=$st :: $(tail -1 "$LOG/pristine-selftest.out")"
echo "PASS-lines=$(grep -c '^PASS ' "$LOG/pristine-selftest.out") FAIL-lines=$(grep -c '^FAIL ' "$LOG/pristine-selftest.out")"
echo "--- pristine counter ---"
ct=0
python3 "$D/tools/score-storage-arm-r38.py" --repo "$D" --revision "$REV" --scratch "$S" \
  > "$LOG/pristine-counter.json" 2> "$LOG/pristine-counter.err" || ct=$?
echo "pristine counter exit=$ct"
python3 - <<'PY'
import json
p="/fast/scratch/hyaku/tsukuroi-r38/C1MutUuid/logs/pristine-counter.json"
d=json.load(open(p))
print(json.dumps({k:d.get(k) for k in ("counter","revision","branch_tip","fixtures_expected","fixtures_matched","live_match","six_planes_all","result","exit","error")}))
print("live:", json.dumps(d.get("live")))
PY
