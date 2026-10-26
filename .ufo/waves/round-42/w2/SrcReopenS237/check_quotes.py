#!/usr/bin/env python3
"""Verify knowledge-doc S237 quotes against fetched v7.1 scrub.c bytes."""
import re, sys

SRC = "/fast/scratch/hyaku/tsukuroi-r42/SrcReopenS237/v7.1-scrub.c"
DOC = "/fast/scratch/hyaku/tsukuroi-r42/SrcReopenS237/record-r42.md"

with open(SRC, encoding="utf-8") as f:
    lines = f.read().splitlines()

with open(DOC, encoding="utf-8") as f:
    doc = f.read().splitlines()

pat = re.compile(r'\*\*Quote\.\*\* `S237` scrub\.c:(\d+): "(.*)"\s*$')
ranges = [(67, 70), (280, 330), (446, 535), (826, 895), (1110, 1125),
          (1186, 1220), (1330, 1340), (1498, 1512), (1925, 1945)]

ok = bad = outside = 0
for i, dl in enumerate(doc, 1):
    m = pat.search(dl)
    if not m:
        continue
    ln = int(m.group(1))
    quote = m.group(2)
    src_line = lines[ln - 1].strip() if ln - 1 < len(lines) else None
    member = any(a <= ln <= b for a, b in ranges)
    if src_line is None:
        print(f"doc:{i} line {ln}: OUT OF FILE (file has {len(lines)} lines)")
        bad += 1
        continue
    match = src_line.startswith(quote) or src_line == quote
    if match:
        ok += 1
    else:
        bad += 1
        print(f"doc:{i} line {ln}: MISMATCH")
        print(f"  quote: {quote!r}")
        print(f"  source: {src_line!r}")
    if not member:
        outside += 1
        print(f"doc:{i} line {ln}: quote verified={match} but OUTSIDE anchor ranges {ranges}")

print(f"\nsummary: verified={ok} mismatch={bad} outside-ranges={outside} total-file-lines={len(lines)}")
