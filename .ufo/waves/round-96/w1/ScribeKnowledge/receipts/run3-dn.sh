#!/bin/sh
# ScribeKnowledge round-96: three-run r95 do-nothing battery (the blindness control).
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
  timeout 1200 python3 .ufo/waves/round-96/before/controls/do-nothing-battery-r95.py --gate "$g" --runs 3 \
      --work "$S/dn3-$n" --json "$S/dn3-$n.json" >"$S/dn3-$n.stdout" 2>&1
  echo "exit=$? $n"
  python3 - "$S/dn3-$n.json" "$n" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
runs = d if isinstance(d,list) else [d]
for i,r in enumerate(runs):
    print(sys.argv[2], 'run',i, r['verdict'], r['families_passed'],'/',r['families_total'],
          'failed=',r['failed_families'], 'cases=',r['cases'],
          'error_rows=', sum(1 for e in r['case_log'] if e.get('error')))
PY
done
