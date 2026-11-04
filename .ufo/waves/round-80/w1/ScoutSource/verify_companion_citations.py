#!/usr/bin/env python3
"""Verify a sibling companion note's source citations against the frozen snapshot.

Read-only. Checks that every `:NNN` / `:NNN-NNN` citation resolves to a non-blank,
in-range line of the snapshot, and that every quoted fragment carrying an explicit
`(:NNN, N words)` citation is present verbatim inside its cited range with the
claimed word count.

Usage: verify_companion_citations.py <snapshot.xml> <note.md>
"""
import re
import sys

snap = open(sys.argv[1], encoding="utf-8").read().split("\n")
note = open(sys.argv[2], encoding="utf-8").read()


def norm(t):
    return re.sub(r"\s+", " ", t).strip()


def seg(a, b):
    s = "\n".join(re.sub(r"<[^>]+>", "", x) for x in snap[a - 1:b])
    return norm(s)


cites = set()
for m in re.finditer(r"`:(\d+)(?:-(\d+))?`", note):
    a = int(m.group(1))
    b = int(m.group(2)) if m.group(2) else a
    cites.add((a, b))

bad = []
for a, b in sorted(cites):
    if a < 1 or b > len(snap):
        bad.append((a, b, "out of range"))
    elif not "".join(snap[a - 1:b]).strip():
        # A cited line must carry source text. Check the RAW line, not the
        # tag-stripped form: a table cell written as <entry/> is meaningful
        # markup (an unmarked policy cell), not a blank line.
        bad.append((a, b, "blank"))
print(f"line citations: {len(cites)}  unresolvable: {len(bad)}")
for x in bad:
    print("   ", x)

pat = re.compile(r'"([^"]{12,200})"\s*\(`:(\d+)(?:-(\d+))?`,\s*(\d+)\s*words?\)')
hits = pat.findall(note)
ok = 0
problems = []
for q, a, b, n in hits:
    a = int(a)
    b = int(b) if b else a
    qn = norm(q)
    present = qn in seg(a, b)
    wmatch = len(qn.split()) == int(n)
    if present and wmatch:
        ok += 1
    else:
        problems.append((qn[:70], a, b, len(qn.split()), n, present))
print(f"quoted-fragment citations: {len(hits)}  verbatim+wordcount OK: {ok}  problems: {len(problems)}")
for p in problems:
    print("   ", p)
sys.exit(1 if (bad or problems) else 0)

