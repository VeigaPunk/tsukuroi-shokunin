#!/usr/bin/env python3
"""C1-B4 part 2: corrected + sharper cheat probes (reuses cheat.py's builders)."""
import json
import os
import sys

sys.path.insert(0, '/fast/scratch/hyaku/tsukuroi-r50/R50CritCheatC1')
import cheat as C

S = C.S
out = {}
H = C.section_hashes(C.ENTRY)


def go(name, bodies, hashes, **kw):
    d = C.build(name, bodies, hashes, **kw)
    out[name] = C.summary(name, C.run(name, d))
    return out[name]


# Se1b: two real row sources AND an out-of-range lane citation -> the out-of-range leg fires.
b = {(r, s): C.body(r, s, 'p' + s + 'q' * 300) for r in C.ROWS for s, _ in C.SEATS[r]}
e1b = dict(b)
e1b[('GR1', 'R50RevGR1a')] = ('Row GR1 read. Anchors cmdline.c:147, vsprintf.c:86 and '
                              'entry.md:999999. ' + 'v' * 300)
go('Se1b-out-of-range-real2', e1b, H)

# Se1c: same shape but the lane citation is in range (entry.md:297) -> credited.
e1c = dict(b)
e1c[('GR1', 'R50RevGR1a')] = ('Row GR1 read. Anchors cmdline.c:147, vsprintf.c:86 and '
                              'entry.md:297. ' + 'v' * 300)
go('Se1c-in-range-lane-cite', e1c, H)

# S0b: citations at line 1 of two row sources -- no relation to the quoted evidence.
b1 = {}
for r in C.ROWS:
    a, bb = C.CITES[r]
    f1, f2 = a.split(':')[0], bb.split(':')[0]
    for s, _ in C.SEATS[r]:
        b1[(r, s)] = (f'Row {r} read.\n{f1}:1 and {f2}:1 are cited.\n' + 'b' + s + 'c' * 300)
go('S0b-line1-citations', b1, H)

# Smin2: cheapest PASS -- 3 credited (2 reviewer + 1 critic) + 3 stub seats per row.
m, stubs = {}, set()
for r in C.ROWS:
    seats = C.SEATS[r]
    for i, (s, _) in enumerate(seats):
        if i in (0, 1, 3):
            m[(r, s)] = C.body(r, s, 'p' + s + 'q' * 300)
        else:
            stubs.add(s)
go('Smin2-9credited-9stub', m, H, stub_hash_seats=stubs)

# Smin3: 4 credited, 2 stub per row (one more than the floor).
m3, st3 = {}, set()
for r in C.ROWS:
    for i, (s, _) in enumerate(C.SEATS[r]):
        if i in (0, 2, 3, 5):
            m3[(r, s)] = C.body(r, s, 'm' + s + 'n' * 300)
        else:
            st3.add(s)
go('Smin3-12credited-6stub', m3, H, stub_hash_seats=st3)

# Sf2: the MARKED entry keeps the four round-49 corrections, reintroduces a round-48 defect.
bad = C.marked_entry().replace('dev-replace.c:1171-1195',
                               'dev-replace.c:1171-1195 (earlier: dev-replace.c:1171-1199)', 1)
hb = C.section_hashes_path(bad, 'Sf2-entry.md')
bf = {(r, s): C.body(r, s, 'f' + s + 'k' * 300) for r in C.ROWS for s, _ in C.SEATS[r]}
go('Sf2-round48-defect', bf, hb, entry=bad)

# Sg: no entry mark, but a README/SKILL mark only -> measures which mark legs are separable.
d = C.build('Sg-mark-split', {(r, s): C.body(r, s, 'g' + s + 'h' * 300)
                              for r in C.ROWS for s, _ in C.SEATS[r]}, H,
            entry=C.read(C.ENTRY))
out['Sg-mark-split'] = C.summary('Sg-mark-split', C.run('Sg-mark-split', d))

C.write(os.path.join(S, 'receipts', 'summary2.json'), json.dumps(out, indent=1, sort_keys=True))
print(json.dumps({k: v['verdict'] for k, v in out.items()}, sort_keys=True))
