#!/usr/bin/env python3
"""Independent method 3: extract the table from the INSTALLED man page (roff).

Third code path (neither ElementTree nor XML-regex). Reads the installed
systemd 262.1 man page rather than the pinned v262 XML, so it tests both the
matrix transcription and whether the host's installed docs agree with the
pinned upstream source.
"""
import json
import re
import sys

raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()
i = raw.find("Exit causes and the effect of")
if i < 0:
    raise SystemExit("title not found in roff source")
seg = raw[i:]
end = seg.find(".TE")
seg = seg[:end]

groups = re.findall(r"T\{(.*?)T\}", seg, re.S)


def clean(s):
    s = re.sub(r"\\f[BIRP]", "", s)
    s = s.replace("\\-", "-").replace("\\&", "").replace("\n", " ")
    return re.sub(r"\s+", " ", s).strip()


vals = [clean(g) for g in groups]
settings = vals[1:8]
rows = []
i = 8
while i + 8 <= len(vals):
    cause = vals[i]
    marks = vals[i + 1: i + 8]
    if cause == "":
        break
    rows.append({"cause": cause, "restart": [m == "X" for m in marks]})
    i += 8

out = {"method": "roff-installed-man", "settings": settings, "rows": rows}
json.dump(out, open(sys.argv[2], "w"), indent=2)
print(json.dumps(out, indent=2))
