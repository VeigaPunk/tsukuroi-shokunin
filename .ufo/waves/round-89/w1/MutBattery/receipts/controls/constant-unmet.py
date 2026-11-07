# control battery used in the report: answers unmet for every gate and writes the --json receipt
import json, sys
a = sys.argv
out = a[a.index("--json") + 1] if "--json" in a else None
j = {"verdict": "unmet", "families_passed": 0, "families_total": 50, "failed_families": ["POSITIVE"], "cases": 200}
if out:
    json.dump(j, open(out, "w"))
print(json.dumps(j))
sys.exit(1)
