#!/usr/bin/env python3
"""Field-by-field diff of two run-receipt bodies (base vs measured).

Run-varying fields (revision, seed, branch_tip, started/finished stamps) are listed separately so a
behaviour change cannot hide inside them.
"""
import json
import sys

dec = json.JSONDecoder()


def body(path):
    text = open(path, encoding='utf-8', errors='replace').read()
    i, objs = 0, []
    while True:
        while i < len(text) and text[i].isspace():
            i += 1
        if i >= len(text):
            break
        try:
            o, i = dec.raw_decode(text, i)
        except ValueError:
            break
        objs.append(o)
    return objs[1] if len(objs) > 1 else {}

RUN_VARYING = {'revision', 'seed', 'branch_tip'}


def walk(a, b, path=''):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            out += walk(a.get(k), b.get(k), f'{path}.{k}' if path else k)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append((path, f'len {len(a)}', f'len {len(b)}'))
        for n, (x, y) in enumerate(zip(a, b)):
            out += walk(x, y, f'{path}[{n}]')
        if len(a) != len(b):
            out.append((path, f'set {sorted(str(x)[:60] for x in a)[:3]}', f'set {sorted(str(y)[:60] for y in b)[:3]}'))
    elif a != b:
        out.append((path, a, b))
    return out


base, meas = sys.argv[1], sys.argv[2]
d = walk(body(base), body(meas))
beh = [x for x in d if x[0].split('[')[0].split('.')[0] not in RUN_VARYING]
rv = [x for x in d if x[0].split('[')[0].split('.')[0] in RUN_VARYING]
print(f'base={base}\nmeas={meas}')
print(f'changed-fields total={len(d)} behaviour={len(beh)} run-varying={len(rv)}')
for p, x, y in rv:
    print(f'  RUNVARY {p}: {str(x)[:40]} -> {str(y)[:40]}')
for p, x, y in beh:
    print(f'  BEHAVIOUR {p}: {json.dumps(x, sort_keys=True)[:300]} -> {json.dumps(y, sort_keys=True)[:300]}')
