#!/usr/bin/env bash
# F-6 arm runner: clone the lane at its tip, commit one arm's census, score it with the frozen counter.
set -uo pipefail
S=/fast/scratch/hyaku/tsukuroi-r42/C1CritFinalEvasion
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
COUNTER=$LANE/tools/score-size-invariance-r42.py
TIPSHA=78abb8b5cdc9da511b4fc523e661517a68dd33d3
arm=$1
D=$(mktemp -d "$S/fx.XXXXXX") || exit 9
git clone -q --shared "$LANE" "$D" || exit 9
git -C "$D" remote remove origin
top=$(git -C "$D" rev-parse --show-toplevel)
[ "$top" = "$D" ] || { echo "TOPLEVEL MISMATCH: $top"; exit 9; }
git -C "$D" checkout -q --detach "$TIPSHA" || exit 9
head=$(git -C "$D" rev-parse HEAD)
[ "$head" = "$TIPSHA" ] || { echo "TIP MISMATCH: $head"; exit 9; }
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "TOPLEVEL MISMATCH after checkout"; exit 9; }
cp "$S/arm-$arm.sh" "$D/tools/tsukuroi-census.sh"
git -C "$D" add tools/tsukuroi-census.sh
git -C "$D" -c user.name=fixture -c user.email=fixture@invalid commit -q -m "arm $arm" || exit 9
sha=$(git -C "$D" rev-parse HEAD)
start=$(date +%s)
python3 "$COUNTER" --lane "$D" --revision "$sha" --scratch "$S/s" > "$S/result-$arm.jsonl" 2> "$S/result-$arm.err"
rc=$?
end=$(date +%s)
echo "arm=$arm clone=$D commit=$sha counter_rc=$rc secs=$((end-start))"
rm -rf -- "$D"
exit 0
