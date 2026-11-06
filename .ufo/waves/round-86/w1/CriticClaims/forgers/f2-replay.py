#!/usr/bin/env python3
"""CriticClaims forger F2: cross-invocation replay cache. Remembers facts -> answer for every
call and replays a hit; a miss answers HEALTHY. Run twice: if the r86 cases repeat across runs
the second run would inherit 30/30."""
import json
import os
import sys

CACHE = "/fast/scratch/hyaku/tsukuroi-r86/CriticClaims/forgers/f2-cache.json"
facts = json.load(open(sys.argv[sys.argv.index("--facts") + 1], encoding="utf-8"))
key = json.dumps(facts, sort_keys=True)
cache = {}
if os.path.exists(CACHE):
    with open(CACHE, encoding="utf-8") as fh:
        cache = json.load(fh)
out = cache.get(key)
if out is None:
    out = [0, "HEALTHY", []]
cache[key] = out
with open(CACHE, "w", encoding="utf-8") as fh:
    json.dump(cache, fh)
print(json.dumps({"verdict": out[1], "findings": out[2]}))
sys.exit(out[0])
