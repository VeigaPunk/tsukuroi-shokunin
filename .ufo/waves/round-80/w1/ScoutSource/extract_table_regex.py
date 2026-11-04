#!/usr/bin/env python3
"""Independent method 2: pure regex/text extraction, no XML parser.

Deliberately a different code path from extract_table.py (ElementTree) so a
shared parser bug cannot make both agree spuriously.
"""
import json
import re
import sys

raw = open(sys.argv[1], encoding="utf-8").read()

m = re.search(r"<title>Exit causes and the effect of the .*?Restart=</varname> settings</title>", raw)
if not m:
    raise SystemExit("table title not found")

# slice from the title to the end of that <table> element
seg = raw[m.start():]
end = seg.find("</table>")
seg = seg[:end]

# header: first <row> inside <thead>
thead = re.search(r"<thead>(.*?)</thead>", seg, re.S).group(1)
hdr_row = re.search(r"<row>(.*?)</row>", thead, re.S).group(1)


def cells_of(block):
    """Split a <row> block into cell texts; <entry/> -> ''."""
    out = []
    pos = 0
    for mm in re.finditer(r"<entry\s*/>|<entry>(.*?)</entry>", block, re.S):
        out.append("" if mm.group(1) is None else mm.group(1))
    return out


def clean(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()


header = [clean(c) for c in cells_of(hdr_row)]
settings = header[1:]

tbody = re.search(r"<tbody>(.*?)</tbody>", seg, re.S).group(1)
rows = []
for rb in re.finditer(r"<row>(.*?)</row>", tbody, re.S):
    vals = [clean(c) for c in cells_of(rb.group(1))]
    cause, marks = vals[0], vals[1:]
    assert len(marks) == len(settings), (cause, len(marks), len(settings))
    for mk in marks:
        assert mk in ("", "X"), (cause, mk)
    rows.append({"cause": cause, "restart": [mk == "X" for mk in marks]})

out = {
    "method": "regex-text",
    "settings": settings,
    "rows": rows,
}
json.dump(out, open(sys.argv[2], "w"), indent=2)
print(json.dumps(out, indent=2))
