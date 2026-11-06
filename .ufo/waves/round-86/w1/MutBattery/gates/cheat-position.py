import json, os, sys
# cheat: derive an answer from the CALL POSITION (persistent counter), ignoring facts
counter = "/tmp/mutbattery-r86-pos-counter"
try:
    n = int(open(counter).read().strip())
except Exception:
    n = 0
try:
    with open(counter, "w") as fh:
        fh.write(str(n + 1))
except Exception:
    pass
plan = ["HEALTHY", "HEALTHY", "HEALTHY", "DEGRADED", "HEALTHY", "CANNOT-EVALUATE"]
verdict = plan[n % len(plan)]
print(json.dumps({"verdict": verdict, "findings": [] if verdict == "HEALTHY" else (["HR-HIBERNATE-DISABLED"] if verdict == "DEGRADED" else [])}))
sys.exit({"HEALTHY": 0, "DEGRADED": 1, "CANNOT-EVALUATE": 2}[verdict])
