#!/bin/sh
# Round-92 C1 receipts: before leg (r91 battery, channel open), after leg (r92 battery, clone),
# and the canonical-lane after leg. Run from the lane root: sh .ufo/waves/round-92/after/run-c1.sh
set -u
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r92/l1
A=$LANE/.ufo/waves/round-92/after/c1-controls
CLONE=$S/clone-495a9f6c
REV=495a9f6c71c50d2118a71c38b1bc188e9834e157
export TMPDIR=$S/tmp
mkdir -p "$TMPDIR" "$A" "$S"
rm -rf "$CLONE"
git clone --shared "$LANE" "$CLONE" -q
git -C "$CLONE" log -1 --format=%H > "$A/clone-revision.txt"
sha256sum "$CLONE/tools/check-limine-pins.py" "$CLONE/tools/limine-pin-battery-r92.py" \
  "$CLONE/tools/limine-pin-battery-r91.py" > "$A/clone-sha256.txt"
cp "$LANE"/.ufo/waves/round-92/before/controls/gates/*.py "$CLONE/tools/"
ONLY=K3-sibling,K4-syspath,K5-abspath,K6-proc,K7-env
echo "=== before leg (r91 battery, channel open) ==="
PYTHONPATH=$CLONE/tools python3 "$LANE/.ufo/waves/round-92/before/controls/run-controls.py" \
  --battery "$CLONE/tools/limine-pin-battery-r91.py" --gates "$CLONE/tools" --only "$ONLY" \
  --runs 3 --jobs 5 --label before-clone-r91-battery --env PYTHONPATH=$CLONE/tools \
  --work "$S/work/before" --out "$A/before-clone"
echo "=== after leg (r92 battery, clone) ==="
PYTHONPATH=$CLONE/tools python3 "$LANE/.ufo/waves/round-92/before/controls/run-controls.py" \
  --battery "$CLONE/tools/limine-pin-battery-r92.py" --gates "$CLONE/tools" --only "$ONLY" \
  --runs 3 --jobs 5 --label after-clone-r92-battery --env PYTHONPATH=$CLONE/tools \
  --work "$S/work/after" --out "$A/after-clone"
echo "=== after leg (r92 battery, canonical lane) ==="
PYTHONPATH=$LANE/tools python3 "$LANE/.ufo/waves/round-92/before/controls/run-controls.py" \
  --battery "$LANE/tools/limine-pin-battery-r92.py" \
  --gates "$LANE/.ufo/waves/round-92/before/controls/gates" --only "$ONLY" \
  --runs 3 --jobs 5 --label after-canonical-r92-battery --env PYTHONPATH=$LANE/tools \
  --work "$S/work/canon" --out "$A/canonical-after"
echo "=== honest gate, canonical (89/89 x3 expected) ==="
python3 "$LANE/tools/limine-pin-battery-r92.py" --gate "$LANE/tools/check-limine-pins.py" \
  --runs 3 --work "$S/work/gate-canon" --json "$A/gate-canonical.json" \
  | tee "$A/gate-canonical.txt"
echo "=== honest gate, clone (89/89 x3 expected) ==="
python3 "$CLONE/tools/limine-pin-battery-r92.py" --gate "$CLONE/tools/check-limine-pins.py" \
  --runs 3 --work "$S/work/gate-clone" --json "$A/gate-clone.json" \
  | tee "$A/gate-clone.txt"
echo "=== usage check (both layouts) ==="
python3 "$LANE/tools/limine-pin-battery-r92.py" --usage-check --gate "$LANE/tools/check-limine-pins.py" \
  --work "$S/work/usage" > "$A/usage-canonical.json"; echo "rc=$?" >> "$A/usage-canonical.json"
python3 "$CLONE/tools/limine-pin-battery-r92.py" --usage-check --gate "$CLONE/tools/check-limine-pins.py" \
  --work "$S/work/usage2" > "$A/usage-clone.json"; echo "rc=$?" >> "$A/usage-clone.json"
echo "=== isolation check receipt ==="
python3 "$LANE/tools/limine-pin-battery-r92.py" --isolation-check --work "$S/work/iso" > "$A/isolation-check.json"
echo "=== no-regression: r91 battery scores the r92 gate (82/82 expected) ==="
python3 "$LANE/tools/limine-pin-battery-r91.py" --gate "$LANE/tools/check-limine-pins.py" --runs 1 \
  --work "$S/work/noreg" | tee "$A/r91-battery-on-r92-gate.txt"
echo "=== do-nothing K1: r91 gate under the r92 battery (0/89, error rows expected) ==="
git -C "$LANE" show "$REV^:tools/check-limine-pins.py" > "$S/r91-gate.py"
python3 "$LANE/tools/limine-pin-battery-r92.py" --gate "$S/r91-gate.py" --runs 1 \
  --work "$S/work/k1" --json "$A/k1-donothing.json" | tee "$A/k1-donothing.txt"
echo ALL-DONE
