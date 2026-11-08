#!/bin/sh
# ScribeKnowledge round-96: run the r96 battery against the three own-work era-rule mutants.
set -u
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r96/ScribeKnowledge
cd "$LANE" || exit 1
for m in M-x-only-era M-y-only-era M-z-only-era; do
  timeout 900 python3 tools/limine-pin-battery-r96.py --gate "$S/mutants/$m.py" --runs 1 \
      --work "$S/mw-$m" --json "$S/mut-$m.json" >"$S/mut-$m.stdout" 2>&1
  echo "exit=$? $m"
  python3 - "$S/mut-$m.json" "$m" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
r = d[0] if isinstance(d,list) else d
print(sys.argv[2], r['verdict'], r['families_passed'],'/',r['families_total'],
      'failed=',r['failed_families'], 'cases=',r['cases'],
      'error_rows=', sum(1 for e in r['case_log'] if e.get('error')))
PY
done
