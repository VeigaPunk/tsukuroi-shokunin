#!/bin/sh
# Round-97 registry pre-flight: read the WORKING-TREE SKILL.md (with the three r97 rows) at a
# scratch revision and confirm the coverage gate still certifies every tool, and that the content
# bindings still read PASS. Never writes the lane.
#   sh .ufo/waves/round-97/after/preflight-registry.sh
set -eu
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r97/preflight
C=$S/work
O=$S/origin.git
mkdir -p "$S"
rm -rf "$C" "$O"
git clone --shared --bare -q "$LANE" "$O"
git clone -q "$O" "$C"
[ "$(git -C "$C" rev-parse --show-toplevel)" = "$C" ] || { echo "preflight toplevel mismatch" >&2; exit 1; }
cp "$LANE/SKILL.md" "$C/SKILL.md"
git -C "$C" -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local commit -q -am "round-97 preflight: working-tree registry rows"
git -C "$C" push -q origin master
REV=$(git -C "$C" rev-parse HEAD)
echo "preflight revision $REV"
set +e
python3 "$C/tools/check-registry-coverage.py" --revision "$REV"
echo "coverage rc=$?"
python3 "$LANE/tools/check-registry-content.py" --revision "$REV"
echo "content rc=$?"
set -e
rm -rf "$C" "$O"
