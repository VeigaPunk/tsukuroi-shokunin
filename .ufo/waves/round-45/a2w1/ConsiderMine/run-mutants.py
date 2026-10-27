#!/usr/bin/env python3
"""run-mutants.py — able-to-fail driver for seat-harm-log.py.

Writes one single-field mutant of seat-harm.jsonl per case into scratch, runs the checker on it and
requires exactly the expected finding code to appear (plus PASS is absent). Mutants live in
`mutants/` beside this file for the record. Read-only w.r.t. the lane and the host.

Usage: python3 run-mutants.py [--scratch DIR]
Exit 0 when every mutant is killed; 1 with the survivors listed.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
CHECKER = os.path.join(HERE, 'seat-harm-log.py')
BASE = os.path.join(HERE, 'seat-harm.jsonl')


def rows():
    with open(BASE, encoding='utf-8') as fh:
        return [json.loads(l) for l in fh if l.strip()]


def mutate(r, i, field, value):
    r[i][field] = value
    return r


def drop(r, i, field):
    del r[i][field]
    return r


CASES = [
    ('K01-cite-line-drift', 'SH-CITE-QUOTE', lambda r: mutate(r, 0, 'cite', 'corpus/lessons/round-37.md:101')),
    ('K02-quote-paraphrase', 'SH-CITE-QUOTE', lambda r: mutate(r, 0, 'quote', 'listed ?? corpus/, containing only')),
    ('K03-invented-lesson-id', 'SH-ID-NOT-ON-LINE', lambda r: mutate(r, 1, 'id', 'R39-SEAT-PKILLX')),
    ('K04-class-unknown', 'SH-CLASS-UNKNOWN', lambda r: mutate(r, 0, 'class', 'host-everything')),
    ('K05-id-duplicate', 'SH-ID-DUPLICATE', lambda r: mutate(r, 2, 'id', 'R39-SEAT-PKILL')),
    ('K06-round-out-of-window', 'SH-ROUND-OUT-OF-WINDOW', lambda r: mutate(r, 0, 'round', 30)),
    ('K07-absolute-cite', 'SH-CITE-ABSOLUTE', lambda r: mutate(r, 0, 'cite', '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-37.md:102')),
    ('K08-missing-file', 'SH-CITE-MISSING', lambda r: mutate(r, 0, 'cite', 'corpus/lessons/round-99.md:1')),
    ('K09-harm-unknown', 'SH-HARM-UNKNOWN', lambda r: mutate(r, 0, 'harm', ['fleet-root'])),
    ('K10-today-unknown', 'SH-TODAY-UNKNOWN', lambda r: mutate(r, 2, 'today', 'closed')),
    ('K11-minted-id-reuses-landed', 'SH-ID-ALREADY-IN-LESSONS', lambda r: mutate(r, 8, 'id', 'R44-W1-UNREPORTED-SEATS')),
    ('K12-closed-without-proof', 'SH-PROOF-MISSING', lambda r: drop(r, 2, 'proof_red')),
    ('K13-status-quote-paraphrase', 'SH-STATUS-QUOTE', lambda r: mutate(r, 1, 'status_quote', 'never pkill/killall by pattern')),
    ('K14-id-basis-unknown', 'SH-ID-BASIS', lambda r: mutate(r, 0, 'id_basis', 'made-up')),
    ('K15-proof-green-names-old', 'SH-PROOF-QUOTE', lambda r: mutate(r, 2, 'proof_green', '.ufo/waves/round-41/w1/RoutedSelfAssessScratch.md:54')),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scratch', default=os.environ.get('TMPDIR') or '/fast/scratch/hyaku/tsukuroi-r45/ConsiderMine')
    a = ap.parse_args()
    os.makedirs(os.path.join(HERE, 'mutants'), exist_ok=True)
    os.makedirs(a.scratch, exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    results = []
    for name, want, fn in CASES:
        mutant = fn(rows())
        path = os.path.join(HERE, 'mutants', name + '.jsonl')
        with open(path, 'w', encoding='utf-8') as fh:
            for r in mutant:
                fh.write(json.dumps(r) + '\n')
        proc = subprocess.run(
            [sys.executable, CHECKER, '--log', path, '--lane', LANE],
            capture_output=True, text=True, cwd=HERE, env=env)
        codes = sorted({ln.split()[1] for ln in proc.stdout.splitlines() if ln.startswith('FAIL ')})
        killed = proc.returncode != 0 and want in codes and 'PASS:' not in proc.stdout
        results.append({'mutant': name, 'expected': want, 'codes': codes,
                        'rc': proc.returncode, 'killed': killed})
        print(f"{'KILLED ' if killed else 'SURVIVED'} {name}: rc={proc.returncode} codes={codes}")
    killed = sum(1 for r in results if r['killed'])
    with open(os.path.join(HERE, 'mutants', 'results.json'), 'w', encoding='utf-8') as fh:
        json.dump({'baseline': 'PASS rows=10 findings=0', 'killed': killed,
                   'total': len(results), 'results': results}, fh, indent=1)
    print(f'killed={killed}/{len(results)} survived={[r["mutant"] for r in results if not r["killed"]] or "none"}')
    return 0 if killed == len(results) else 1


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(main())
