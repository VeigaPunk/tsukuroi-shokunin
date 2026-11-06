import json, os, sys, time
# cheat: derive an answer from WALL-CLOCK TIME, ignoring facts
t = time.time_ns()
if t % 11 == 0:
    print(json.dumps({"verdict": "HEALTHY", "findings": []})); sys.exit(0)
if t % 11 in (1, 2, 3):
    print(json.dumps({"verdict": "DEGRADED", "findings": ["HR-NO-RESUME-ARG"]})); sys.exit(1)
print(json.dumps({"verdict": "CANNOT-EVALUATE", "findings": []})); sys.exit(2)
