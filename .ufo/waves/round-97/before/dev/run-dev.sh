#!/bin/sh
# Round-97 development run (QUALITY 140: re-read every target clause against one development run
# before the freeze). Writes receipts under .ufo/waves/round-97/before/dev/ and never edits an
# instrument. Run from the lane root.
set -eu
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r97/dev
W=$S/work
D=$LANE/.ufo/waves/round-97/before/dev
BENDS=$LANE/.ufo/waves/round-97/before/controls/bends
DN=$LANE/.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py
mkdir -p "$W" "$D"

python3 "$LANE/tools/make-r97-bends.py" > "$D/00-bends-emitted.txt"

python3 "$LANE/tools/limine-pin-battery-r97.py" --gate "$LANE/tools/check-limine-pins.py" \
  --runs 1 --work "$W" --json "$D/c1-battery-gate.json" > "$D/c1-battery-gate.txt"
set +e
for b in N05-z-cap-8 N06-leading-zero-reject; do
  python3 "$LANE/tools/limine-pin-battery-r97.py" --gate "$BENDS/$b.py" \
    --runs 1 --work "$W" --json "$D/c1-bend-$b.json" > "$D/c1-bend-$b.txt" || true
done
python3 "$DN" --gate "$LANE/tools/check-limine-pins.py" \
  --runs 1 --work "$W" --json "$D/c1-dn-gate.json" > "$D/c1-dn-gate.txt" || true
for b in N05-z-cap-8 N06-leading-zero-reject; do
  python3 "$DN" --gate "$BENDS/$b.py" \
    --runs 1 --work "$W" --json "$D/c1-dn-bend-$b.json" > "$D/c1-dn-bend-$b.txt" || true
done
set -e
python3 "$LANE/tools/check-registry-content.py" --root "$LANE" --json "$D/c2-content-live.json" \
  > "$D/c2-content-live.txt"
python3 "$LANE/tools/check-registry-content.py" --selftest > "$D/c2-content-selftest.txt"

# the doctored-table fixture: a shared clone in scratch, one commit, content-only cell changes
CLONE=$S/doctored
rm -rf "$CLONE"
git clone --shared -q "$LANE" "$CLONE"
[ "$(git -C "$CLONE" rev-parse --show-toplevel)" = "$CLONE" ] || { echo "fixture toplevel mismatch" >&2; exit 1; }
python3 - "$CLONE" <<'PY'
import sys
p = sys.argv[1] + "/SKILL.md"
s = open(p).read()
subs = [("default `auto`", "default `12.9.4`"),
        ("(39 fixtures", "(88 fixtures"),
        ("roster 103 (", "roster 99 ("),
        ("FAMILY_ROSTER, 103,", "FAMILY_ROSTER, 99,"),
        ("--selftest` (7 cases", "--selftest` (29 cases"),
        ("r96 VARIANTS N01-N04", "r96 VARIANTS N01-N05")]
for old, new in subs:
    assert s.count(old) == 1, (old, s.count(old))
    s = s.replace(old, new)
open(p, "w").write(s)
PY
git -C "$CLONE" -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local \
  commit -q -am "round-97 dev fixture: content-only cell doctor (row set unchanged)"
REV=$(git -C "$CLONE" rev-parse HEAD)
echo "doctored revision $REV" > "$D/c2-doctored-revision.txt"
set +e
python3 "$CLONE/tools/check-registry-content.py" --revision "$REV" --json "$D/c2-content-doctored.json" \
  > "$D/c2-content-doctored.txt" 2>&1
echo "content rc=$?" >> "$D/c2-content-doctored.txt"
python3 "$CLONE/tools/check-registry-coverage.py" --revision "$REV" > "$D/c2-coverage-doctored.json" 2>&1
echo "coverage rc=$?" >> "$D/c2-content-doctored.txt"
set -e
rm -rf "$CLONE"
echo "dev run done"
