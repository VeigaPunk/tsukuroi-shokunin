#!/usr/bin/env python3
# A plausible misreading: "resume_offset= without a map-swapfile offset is inconsistent".
import json, sys
f = json.load(open(sys.argv[sys.argv.index("--facts") + 1]))
toks = f["cmdline"].split()
def last(k):
    v = None
    for t in toks:
        if t.startswith(k + "="): v = t.split("=", 1)[1]
    return v
o = last("resume_offset")
if o is not None and f["map_swapfile_offset"] is None:
    print(json.dumps({"verdict": "DEGRADED", "findings": ["HR-OFFSET-MISSING"]})); sys.exit(1)
print(json.dumps({"verdict": "HEALTHY", "findings": []})); sys.exit(0)
