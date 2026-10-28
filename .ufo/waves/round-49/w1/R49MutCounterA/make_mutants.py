#!/usr/bin/env python3
"""Produce the four C1 counter mutants (M1-M4) from the frozen original bytes."""
import hashlib, os

S = '/fast/scratch/hyaku/tsukuroi-r49/R49MutCounterA'
SRC = os.path.join(S, 'counter.orig.py')
orig = open(SRC).read()

MUT = {
    'M1': (  # drop the A2 blocking rule: a `partly`/`fails` seat no longer blocks the row
        """        row_ok = (len(credited) >= 3 and 'reviewer' in roles and 'critic' in roles
                  and distinct and not blocking)""",
        """        row_ok = (len(credited) >= 3 and 'reviewer' in roles and 'critic' in roles
                  and distinct)""",
    ),
    'M2': (  # drop the distinct-bodies check
        """        row_ok = (len(credited) >= 3 and 'reviewer' in roles and 'critic' in roles
                  and distinct and not blocking)""",
        """        row_ok = (len(credited) >= 3 and 'reviewer' in roles and 'critic' in roles
                  and not blocking)""",
    ),
    'M3': (  # drop the results.json seat check (name/agent/output binding)
        """    if tasks.get(seat) != role:
        return None, None, None, f'dispatch agent {tasks.get(seat)!r} != {role}'
    hits = [r for r in results if isinstance(r, dict) and r.get('name') == seat]
    if len(hits) != 1:
        return None, None, None, 'not exactly one results entry'
    if hits[0].get('agent') != role:
        return None, None, None, f'results agent {hits[0].get("agent")!r} != {role}'
    if not hits[0].get('output'):
        return None, None, None, 'no completed output'
""",
        """    if tasks.get(seat) != role:
        return None, None, None, f'dispatch agent {tasks.get(seat)!r} != {role}'
""",
    ),
    'M4': (  # accept any 64-hex report hash instead of the row's section hash
        """            if h != hashes.get(row):
                seat_rows.append(f'{seat}: hash {h} != {hashes.get(row)}')
                continue
""",
        """            if hashes.get(row) is None:
                seat_rows.append(f'{seat}: no row section hash')
                continue
""",
    ),
}

for name, (old, new) in MUT.items():
    assert orig.count(old) == 1, (name, orig.count(old))
    out = orig.replace(old, new)
    assert out != orig
    p = os.path.join(S, f'counter.{name}.py')
    open(p, 'w').write(out)
    print(name, hashlib.sha256(out.encode()).hexdigest(), len(out), 'bytes')
print('orig', hashlib.sha256(orig.encode()).hexdigest(), len(orig), 'bytes')
