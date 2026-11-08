#!/bin/sh
# ScribeKnowledge round-96: three-run battery measurements (landed gate + the four frozen bends).
set -u
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r96/ScribeKnowledge
cd "$LANE" || exit 1
for spec in "landed:tools/check-limine-pins.py" \
            "N01-echo-wrong:.ufo/waves/round-96/before/controls/bends/N01-echo-wrong.py" \
            "N02-y-cap-8:.ufo/waves/round-96/before/controls/bends/N02-y-cap-8.py" \
            "N03-era-label-flip:.ufo/waves/round-96/before/controls/bends/N03-era-label-flip.py" \
            "N04-extra-components:.ufo/waves/round-96/before/controls/bends/N04-extra-components.py"; do
  n=${spec%%:*}; g=${spec#*:}
  timeout 1200 python3 tools/limine-pin-battery-r96.py --gate "$g" --runs 3 \
      --work "$S/r3-$n" --json "$S/r3-$n.json" >"$S/r3-$n.stdout" 2>&1
  echo "exit=$? $n"
  python3 - "$S/r3-$n.json" "$n" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
print(sys.argv[2], d['verdict'], d['families_passed'],'/',d['families_total'],
      'failed=',d['failed_families'], 'cases=',d['cases'],
      'error_rows=', sum(1 for e in d['case_log'] if e.get('error')))
PY
done
