#!/usr/bin/env bash
set -euo pipefail
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r42/C1MutSites
R="$L/.ufo/waves/round-42/w1/C1MutSites"
name="$1"; D="$S/fx.$name"
mkdir -p "$R"
if [ "$name" = "base" ]; then
  sha=447662088dfd3155e31aed239179a79c1d1046c7
else
  sha="$(cat "$S/fx.$name.sha")"
fi
echo "--- counter run $name (revision $sha) start $(date -u +%H:%M:%SZ) ---"
export TMPDIR="$S"
set +e
python3 "$L/tools/score-size-invariance-r42.py" --lane "$D" --revision "$sha" --scratch "$S/s" > "$R/$name.json" 2> "$R/$name.err"
rc=$?
set -e
echo "counter_rc=$rc end $(date -u +%H:%M:%SZ)"
python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
keys=("revision","verdict","cases","invariant","non_invariant","ns_invariant","selftest_pass","selftest_rc","selftest_label","default_equal","token")
print(json.dumps({k:d.get(k) for k in keys}))
' "$R/$name.json"
