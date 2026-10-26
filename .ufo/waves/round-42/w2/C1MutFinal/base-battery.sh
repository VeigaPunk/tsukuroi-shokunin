#!/bin/bash
# C1MutFinal baseline battery: tip selftest + frozen C1 counter on pristine 78abb8b5.
# Selftest runs from an extracted copy (git show) so the clone worktree stays untouched.
set -u
S=/fast/scratch/hyaku/tsukuroi-r42/C1MutFinal
D=$S/clone
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
REV=78abb8b5cdc9da511b4fc523e661517a68dd33d3
export TMPDIR=$S/tmp
mkdir -p "$S/tmp/base-st" "$S/rec"

[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo TOPLEVEL_FAIL; exit 3; }

git -C "$D" show "$REV:tools/tsukuroi-census.sh" > "$S/base-census-extracted.sh"
echo "extracted_sha256=$(sha256sum "$S/base-census-extracted.sh" | cut -d' ' -f1)"

echo "== baseline selftest (pristine $REV) =="
TMPDIR=$S/tmp/base-st bash "$S/base-census-extracted.sh" --selftest > "$S/rec/base-selftest.txt" 2>&1
rc=$?
echo "selftest_rc=$rc"
tail -2 "$S/rec/base-selftest.txt"

echo "== baseline counter (pristine $REV) =="
python3 "$LANE/tools/score-size-invariance-r42.py" --lane "$D" --revision "$REV" --scratch "$S/s" \
  > "$S/rec/base-counter.json" 2> "$S/rec/base-counter.err"
crc=$?
echo "counter_rc=$crc"
[ -s "$S/rec/base-counter.json" ] && python3 - "$S/rec/base-counter.json" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1]))
keys = ('revision', 'cases', 'invariant', 'ns_invariant', 'selftest_pass', 'selftest_rc',
        'selftest_label', 'default_equal', 'verdict', 'non_invariant')
print(json.dumps({k: d.get(k) for k in keys}, sort_keys=True))
EOF
[ -s "$S/rec/base-counter.err" ] && { echo 'counter stderr tail:'; tail -3 "$S/rec/base-counter.err"; }
echo "BASELINE_DONE rc_selftest=$rc rc_counter=$crc"
