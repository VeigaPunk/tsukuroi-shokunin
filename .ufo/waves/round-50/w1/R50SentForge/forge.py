#!/usr/bin/env python3
"""C1-B7 forgery probe: can one process fabricate the counted cohort?

Variants (all run against the frozen counter bytes at REV):
  prod  : no overrides, --revision REV  (what the L1 will run before wave files exist)
  a     : 18 reports written by this single process into --wave-dir + hand-written
          --results-file, dispatch read from the real frozen w1-dispatch.json (no dispatch ran)
  b1    : forged --dispatch-file carrying only decoy names (universe seats absent)
  b2    : reports/results under decoy names, real dispatch
  b3    : forged --dispatch-file that carries the universe names with the WRONG roles
  c     : universe names in the real dispatch, one body copied 18x with whitespace padding
  c2    : one body copied 18x, each copy differing by a single citation line number
  fixture: fixture clone of the lane at REV, forged reports+results COMMITTED inside it,
          counter run with NO overrides at the fixture HEAD (production path, forged bytes)
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

S = Path('/fast/scratch/hyaku/tsukuroi-r50/R50SentForge')
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '8029cdba1049df25632c91a23c8db4eefb54be5f'
COUNTER = str(S / 'bin' / 'counter.py')
HASHES = {  # observed: counter.py --section-hash --revision REV (matches the frozen claim)
    'GR1': '3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1',
    'GR2': 'a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f',
    'GR3': '43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c',
}
SEATS = [(f'R50RevGR{n}{x}', 'reviewer', f'GR{n}') for n in '123' for x in 'abc'] + \
        [(f'R50CritGR{n}{x}', 'critic', f'GR{n}') for n in '123' for x in 'abc']
CITES = {'GR1': ('cmdline.c', 'vsprintf.c'),
         'GR2': ('dev-replace.c', 'scrub.c'),
         'GR3': ('systemd.kill.xml', 'capture.txt')}


def body(row, n, pad=False, vary=False):
    a, b = CITES[row]
    line = n + 1 if vary else 1
    core = (f'This report was produced without any dispatch of the named seat. '
            f'It cites {a}:{line} and {b}:1 as the two distinct row sources the counter asks for, '
            f'and asserts that the row bound at the frozen entry holds on these bytes. '
            f'The remaining prose exists only to clear the three hundred byte floor that the '
            f'citation leg applies before it resolves a single citation in this body. '
            f'Fabricated by one process, seat index {n}.')
    if pad:
        core = core.replace('. ', '.  ') + '\n' * 6 + ' ' * 40
    return core


def report(seat, row, text):
    return f'ROW {row} VERDICT: holds\nSECTION SHA256: {HASHES[row]}\n{text}\n'


def write_cohort(d, seats, pad=False, vary=False, same=False):
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    for i, (seat, role, row) in enumerate(seats):
        idx = i if vary else (0 if same else i)
        txt = body(row, idx, pad=pad, vary=vary)
        (d / f'{seat}.md').write_text(report(seat, row, txt))
    return d


def results(path, seats, decoy=False):
    p = Path(path)
    names = [f'R50FakeRevGR{n}{x}' for n in '123' for x in 'abc'] + \
            [f'R50FakeCritGR{n}{x}' for n in '123' for x in 'abc'] if decoy else None
    rows = []
    for i, (seat, role, row) in enumerate(seats):
        rows.append({'name': (names[i] if decoy else seat), 'agent': role,
                     'output': 'completed (fabricated by one process)'})
    p.write_text(json.dumps({'results': rows}, indent=1))
    return p


def dispatch(path, seats, wrong_role=False):
    tasks = []
    for i, (seat, role, row) in enumerate(seats):
        tasks.append({'name': seat, 'agent': ('critic' if role == 'reviewer' else 'reviewer')
                      if wrong_role else role})
    Path(path).write_text(json.dumps({'taskCall': {'tasks': tasks}}))
    return path


def run(tag, args):
    p = subprocess.run([sys.executable, COUNTER, '--revision', REV, '--lane', LANE, *args],
                       capture_output=True, text=True, cwd=str(S), timeout=600)
    out = p.stdout.strip().splitlines()
    try:
        obj = json.loads(out[-1])
    except Exception:
        obj = {'raw': p.stdout[-2000:], 'stderr': p.stderr[-2000:]}
    (S / 'receipts').mkdir(exist_ok=True)
    (S / 'receipts' / f'{tag}.json').write_text(json.dumps(obj, indent=1, sort_keys=True) + '\n')
    keep = {k: obj.get(k) for k in ('verdict', 'structural_ok', 'corr_ok', 'quotes_ok',
                                    'verdicts_ok', 'seats_ok', 'marks_ok', 'error')}
    notes = obj.get('seat_notes') or []
    print(f'[{tag}] rc={p.returncode} {json.dumps(keep)} notes={len(notes)}')
    if notes:
        print('    note[0]:', notes[0][:160])
    for row in ('GR1', 'GR2', 'GR3'):
        pr = (obj.get('per_row') or {}).get(row)
        if pr:
            print(f'    {row}: credited={len(pr["credited"])} blocking={pr["blocking"]} '
                  f'distinct={pr["distinct_bodies"]} row_ok={pr["row_ok"]}')
    return p.returncode, obj


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    print('== prod: no overrides (freeze has no w1 files)')
    run('prod-rev', [])

    print('== a: one process writes 18 reports + hand-written results; real dispatch, no dispatch ran')
    wa = write_cohort(S / 'a' / 'reports', SEATS)
    run('a-forged-cohort', ['--wave-dir', str(wa),
                            '--results-file', str(results(S / 'a' / 'results.json', SEATS))])

    print('== b1: forged dispatch with decoy names only')
    b1 = S / 'b1'
    wb1 = write_cohort(b1 / 'reports', SEATS)
    run('b1-decoy-dispatch',
        ['--wave-dir', str(wb1), '--results-file', str(results(b1 / 'results.json', SEATS)),
         '--dispatch-file', str(dispatch(b1 / 'dispatch.json', [
             (f'R50FakeRevGR{n}{x}', 'reviewer', f'GR{n}') for n in '123' for x in 'abc']))])

    print('== b2: reports/results under names absent from the real dispatch')
    b2 = S / 'b2'
    wb2 = write_cohort(b2 / 'reports', SEATS)
    run('b2-decoy-names',
        ['--wave-dir', str(wb2), '--results-file', str(results(b2 / 'results.json', SEATS, decoy=True))])

    print('== b3: universe names, forged dispatch with wrong roles')
    b3 = S / 'b3'
    wb3 = write_cohort(b3 / 'reports', SEATS)
    run('b3-wrong-role-dispatch',
        ['--wave-dir', str(wb3), '--results-file', str(results(b3 / 'results.json', SEATS)),
         '--dispatch-file', str(dispatch(b3 / 'dispatch.json', SEATS, wrong_role=True))])

    print('== c: real dispatch, one body copied 18x with whitespace padding')
    wc = write_cohort(S / 'c' / 'reports', SEATS, pad=True, same=True)
    run('c-padded-copies', ['--wave-dir', str(wc),
                            '--results-file', str(results(S / 'c' / 'results.json', SEATS))])

    print('== c2: one body copied 18x, one citation line number varied per copy')
    wc2 = write_cohort(S / 'c2' / 'reports', SEATS, same=True, vary=True)
    run('c2-token-varied-copies', ['--wave-dir', str(wc2),
                                   '--results-file', str(results(S / 'c2' / 'results.json', SEATS))])

    if which == 'all':
        print('== fixture: forged reports+results committed in a fixture clone, no overrides')
        fx = S / 'fx'
        if fx.exists():
            shutil.rmtree(fx)
        subprocess.run(['git', 'clone', '-q', '--shared', LANE, str(fx)], check=True, timeout=900)
        assert subprocess.run(['git', '-C', str(fx), 'rev-parse', '--show-toplevel'],
                              capture_output=True, text=True).stdout.strip() == str(fx)
        subprocess.run(['git', '-C', str(fx), 'checkout', '-q', '--detach', REV], check=True)
        wdir = fx / '.ufo' / 'waves' / 'round-50' / 'w1'
        write_cohort(wdir, SEATS)
        results(fx / '.ufo' / 'waves' / 'round-50' / 'w1-results.json', SEATS)
        subprocess.run(['git', '-C', str(fx), '-c', 'user.name=fixture',
                        '-c', 'user.email=fixture@invalid', 'add', '-A'], check=True)
        subprocess.run(['git', '-C', str(fx), '-c', 'user.name=fixture',
                        '-c', 'user.email=fixture@invalid', 'commit', '-q', '-m',
                        'forged cohort: fabricated reports + hand-written results'], check=True)
        head = subprocess.run(['git', '-C', str(fx), 'rev-parse', 'HEAD'],
                              capture_output=True, text=True).stdout.strip()
        print('   fixture HEAD', head, 'parent', REV)
        p = subprocess.run([sys.executable, COUNTER, '--revision', head, '--lane', str(fx)],
                           capture_output=True, text=True, cwd=str(S), timeout=900)
        obj = json.loads(p.stdout.strip().splitlines()[-1])
        (S / 'receipts' / 'fixture-committed.json').write_text(
            json.dumps(obj, indent=1, sort_keys=True) + '\n')
        print('[fixture-committed] rc=%d %s' % (p.returncode, json.dumps(
            {k: obj.get(k) for k in ('verdict', 'structural_ok', 'corr_ok', 'quotes_ok',
                                     'verdicts_ok', 'seats_ok', 'marks_ok')})))
        for row in ('GR1', 'GR2', 'GR3'):
            pr = obj['per_row'][row]
            print(f'    {row}: credited={len(pr["credited"])} distinct={pr["distinct_bodies"]} '
                  f'row_ok={pr["row_ok"]}')


if __name__ == '__main__':
    main()
