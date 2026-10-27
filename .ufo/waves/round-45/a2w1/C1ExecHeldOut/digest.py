#!/usr/bin/env python3
"""Emit a compact per-case digest of every harness comparison (evidence receipt)."""
import hashlib
import importlib.util
import json
import os
import sys

ROOT = '/fast/scratch/hyaku/tsukuroi-r45/C1ExecHeldOut'
spec = importlib.util.spec_from_file_location('h', os.path.join(ROOT, 'harness.py'))
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

MODE_TAGS = {'raw': 'raw_', 'prod': 'prod_'}


def sha(b):
    return hashlib.sha256(b).hexdigest()[:16] if b is not None else None


def main():
    out = []
    for sid in h.SITE_ORDER:
        cases = sorted(f[:-4] for f in os.listdir(os.path.join(ROOT, 'corpus', sid))
                       if f.endswith('.dat'))
        for loc in h.LOCALES:
            for mode, pref in MODE_TAGS.items():
                d = os.path.join(ROOT, 'out', sid, pref + loc.replace('.', '_'))
                for c in cases:
                    b = h.readval(os.path.join(d, c + '.base'))
                    i = h.readval(os.path.join(d, c + '.impl'))
                    brc = int(h.readval(os.path.join(d, c + '.base.rc')).strip())
                    irc = int(h.readval(os.path.join(d, c + '.impl.rc')).strip())
                    raw = open(os.path.join(ROOT, 'corpus', sid, c + '.dat'), 'rb').read()
                    out.append({'site': sid, 'locale': loc, 'mode': mode, 'case': c,
                                'raw_len': len(raw),
                                'captured_sha': sha(raw if mode == 'raw' else raw.rstrip(b'\n')),
                                'base_rc': brc, 'impl_rc': irc,
                                'base_sha': sha(b), 'impl_sha': sha(i),
                                'base_len': None if b is None else len(b),
                                'impl_len': None if i is None else len(i),
                                'equal': (b is not None and i is not None and b == i
                                          and brc == 0 and irc == 0)})
    with open(os.path.join(ROOT, 'digest.jsonl'), 'w') as f:
        for r in out:
            f.write(json.dumps(r, sort_keys=True) + '\n')
    bad = [r for r in out if not r['equal']]
    print('digest rows=%d equal=%d not_equal=%d' % (len(out), len(out) - len(bad), len(bad)))
    for r in bad[:10]:
        print('NOT-EQUAL', r)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
