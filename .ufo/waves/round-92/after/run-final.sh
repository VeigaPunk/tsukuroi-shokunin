#!/bin/sh
# Round-92 final-byte receipts: C1 after legs (final battery aef33925) in both layouts and the C2
# near-misses with the A4 bends. Run from the lane root.
set -u
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r92/l1
A=$LANE/.ufo/waves/round-92/after
C=$S/clone-final
export TMPDIR=$S/tmp
mkdir -p "$TMPDIR" "$A"
rm -rf "$C"
git clone --shared "$LANE" "$C" -q
git -C "$C" log -1 --format=%H > "$A/final-clone-revision.txt"
sha256sum "$C/tools/check-limine-pins.py" "$C/tools/limine-pin-battery-r92.py" \
  "$C/tools/limine-pin-battery-r91.py" "$C"/.ufo/waves/round-92/before/controls/gates/*.py \
  "$C"/.ufo/waves/round-92/before/controls/c2gates/*.py > "$A/final-instrument-shas.txt"
ONLY=K3-sibling,K4-syspath,K5-abspath,K6-proc,K7-env
echo "=== C1 after, clone (final battery)"
PYTHONPATH=$C/tools python3 "$LANE/.ufo/waves/round-92/before/controls/run-controls.py" \
  --battery "$C/tools/limine-pin-battery-r92.py" --gates "$C/tools" --only "$ONLY" \
  --runs 3 --jobs 5 --label c1-after-clone-final --env PYTHONPATH=$C/tools \
  --work "$S/work/f-after" --out "$A/c1-controls/after-clone-final"
echo "=== C1 after, canonical (final battery)"
PYTHONPATH=$LANE/tools python3 "$LANE/.ufo/waves/round-92/before/controls/run-controls.py" \
  --battery "$LANE/tools/limine-pin-battery-r92.py" \
  --gates "$LANE/.ufo/waves/round-92/before/controls/gates" --only "$ONLY" \
  --runs 3 --jobs 5 --label c1-after-canonical-final --env PYTHONPATH=$LANE/tools \
  --work "$S/work/f-can" --out "$A/c1-controls/canonical-after-final"
echo "=== C2 near-misses, canonical (A4 bends)"
python3 "$LANE/.ufo/waves/round-92/before/controls/run-controls.py" \
  --battery "$LANE/tools/limine-pin-battery-r92.py" \
  --gates "$LANE/.ufo/waves/round-92/before/controls/c2gates" \
  --runs 3 --jobs 4 --label c2-near-misses-canonical-final \
  --work "$S/work/f-nc" --out "$A/c2-near-misses/canonical-final"
echo "=== C2 near-misses, clone (A4 bends)"
python3 "$LANE/.ufo/waves/round-92/before/controls/run-controls.py" \
  --battery "$C/tools/limine-pin-battery-r92.py" \
  --gates "$LANE/.ufo/waves/round-92/before/controls/c2gates" \
  --runs 3 --jobs 4 --label c2-near-misses-clone-final \
  --work "$S/work/f-ncl" --out "$A/c2-near-misses/clone-final"
echo "=== N04 usage check (the clause's named certifier)"
python3 "$LANE/tools/limine-pin-battery-r92.py" --usage-check --gate "$LANE/.ufo/waves/round-92/before/controls/c2gates/N04-accept-any.py" \
  --work "$S/work/f-u4" > "$A/usage-n04.txt" 2>&1; echo "rc=$?" >> "$A/usage-n04.txt"
echo FINAL-DONE
