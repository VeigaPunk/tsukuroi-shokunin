#!/bin/bash
# C1MutFinal mutant battery: tip selftest + frozen C1 counter per mutant, strictly sequential.
set -u
S=/fast/scratch/hyaku/tsukuroi-r42/C1MutFinal
D=$S/clone
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
export TMPDIR=$S/tmp

SHAS_m1=95e80557991330f603440f5b32354cf395cef34b
SHAS_m2=91f6be9cc8d584cbd0d875c3477631409c81c0c1
SHAS_m3=56eea9b79cd9bc22e92e8114dbdd1e52de2ccc07
SHAS_m4=bd0bbee88de7bd7afcba55326d7eaa3f026cedbc
SHAS_m5=95601a73a8cab9155ea518b8f6820b7e9853ccba
SHAS_m6=81924df37eed3cb4a41ccd8a549525a72ff472bc

for m in m1 m2 m3 m4 m5 m6; do
  eval "sha=\$SHAS_$m"
  git -C "$D" show "$sha:tools/tsukuroi-census.sh" > "$S/$m-census.sh"
  h=$(sha256sum "$S/$m-census.sh" | cut -d' ' -f1)
  echo "===== $m sha=$sha census_sha256=$h ====="
  mkdir -p "$S/tmp/$m-st"
  TMPDIR="$S/tmp/$m-st" bash "$S/$m-census.sh" --selftest > "$S/rec/$m-selftest.txt" 2>&1
  rc=$?
  echo "selftest_rc=$rc"
  tail -1 "$S/rec/$m-selftest.txt"
  python3 "$LANE/tools/score-size-invariance-r42.py" --lane "$D" --revision "$sha" --scratch "$S/s" \
    > "$S/rec/$m-counter.json" 2> "$S/rec/$m-counter.err"
  crc=$?
  echo "counter_rc=$crc"
  python3 - "$S/rec/$m-counter.json" "$m" <<'EOF'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception as e:
    print('counter_json_error', e); sys.exit(0)
keys = ('cases', 'invariant', 'ns_invariant', 'selftest_pass', 'selftest_rc',
        'selftest_label', 'default_equal', 'verdict', 'non_invariant')
print(json.dumps({k: d.get(k) for k in keys}, sort_keys=True))
nsbad = [k for k, v in (d.get('ns_cases') or {}).items() if not v.get('invariant')]
print('ns_non_invariant:', nsbad)
EOF
  [ -s "$S/rec/$m-counter.err" ] && { echo 'counter stderr tail:'; tail -2 "$S/rec/$m-counter.err"; }
done
echo MUTANT_BATTERY_DONE
