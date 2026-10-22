#!/usr/bin/env bash
# Run the round-25 C1 detector in the work sandbox at a given revision and
# print the exit code plus the ids/statuses of every check.
# Usage: run-detector.sh <rev> <label>
set -uo pipefail
SB=/fast/scratch/hyaku/tsukuroi-r25/w2/MutC1TokensPaths
rev=${1:-HEAD}
label=${2:-run}
cd "$SB/work" || exit 9
out="$SB/out-$label.json"
python3 tools/check-self-assessment.py --revision "$rev" > "$out" 2> "$SB/err-$label.txt"
rc=$?
echo "label=$label rev=$rev exit=$rc"
python3 - "$out" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print("checked=%s mismatches=%s status=%s" % (d["checked"], d["mismatches"], d["status"]))
for c in d["checks"]:
    if c["status"] != "match":
        print("  %s %s stated=%r observed=%r reason=%s" % (c["id"], c["status"], c["stated"], c["observed"], c["reason"]))
PY
exit $rc
