#!/usr/bin/env python3
"""C1-S2: forged-seat binding probe against the frozen round-47 C1 counter.

Builds variants as commits on top of the freeze rev inside a fixture clone, then scores each
with the frozen counter. Writes nothing outside the fixture clone.
"""
import hashlib
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER = f'{LANE}/tools/check-scrub-admission-r47.py'
FREEZE = '77e9e2b2e96b85d8f048ae2087e246a542b71611'
D = sys.argv[1]
W = '.ufo/waves/round-47'
HASHES = {'GR1': 'fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8',
          'GR2': '909830c83cbcf0a02264153fa6f179415fb8388d3e08c43d79fbf33c8cfa11a2',
          'GR3': '43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c'}
PAIR = {'GR1': ('R47RevGR1a', 'reviewer', 'cmdline.c', 'vsprintf.c', 'kstrtox.c', 'sysfs.c'),
        'GR2': ('R47RevGR2a', 'reviewer', 'dev-replace.c', 'scrub.c', 'sysfs.c'),
        'GR3': ('R47RevGR3a', 'reviewer', 'systemd.kill.xml', 'btrfs-scrub@.service',
                'scrub.c', 'capture.txt')}
SECOND = {'GR1': ('R47CritGR1a', 'critic'), 'GR2': ('R47CritGR2a', 'critic'),
          'GR3': ('R47CritGR3a', 'critic')}
CITE = {'GR1': ['cmdline.c:1', 'vsprintf.c:1', 'kstrtox.c:1', 'sysfs.c:1'],
        'GR2': ['dev-replace.c:1143', 'scrub.c:3094', 'sysfs.c:1'],
        'GR3': ['systemd.kill.xml:1', 'btrfs-scrub@.service:1', 'scrub.c:1', 'capture.txt:1']}


def git(*a, **kw):
    return subprocess.run(['git', '-C', D, *a], capture_output=True, text=True, **kw)


def body(row, seat, nonce):
    cites = '\n'.join(f'- Cited evidence resolves at {c}.' for c in CITE[row])
    return (f'Fabricated body for {seat}. This seat was never spawned: no agent ran, no '
            f'transcript exists, and the only bytes supporting the row are the ones written by '
            f'the forger in this commit. The report exists solely to exercise the counter, so it '
            f'carries a valid citation set and nothing else of substance.\n'
            f'{cites}\nNonce {nonce}: padding to clear the 300-byte body floor and to keep the '
            f'K23 pairwise-distinct leg satisfied across seats bound to the same row.\n')


def report(row, seat, nonce):
    return f'ROW {row} VERDICT: holds\nSECTION SHA256: {HASHES[row]}\n{body(row, seat, nonce)}\n'


def marks():
    """Add the three admission marks the counter reads."""
    for path, text in (('corpus/knowledge/btrfs-scrub-grounding-r45.md',
                        '## Gate status — round 47 (GR1-GR3 admitted)'),
                       ('SKILL.md', '## Scrub grounding — round 47 admission'),
                       ('corpus/README.md', None)):
        full = f'{D}/{path}'
        with open(full, encoding='utf-8') as f:
            cur = f.read()
        if text is None:
            add = '- `btrfs-scrub-grounding-r45.md` admitted round 47 (fabricated mark).\n'
        else:
            add = f'\n{text}\n'
        if add not in cur:
            with open(full, 'w', encoding='utf-8') as f:
                f.write(cur + add)


def mkdir(p):
    os.makedirs(f'{D}/{p}', exist_ok=True)


def dispatch_obj(wave, tasks, registry=True):
    d = {'schema': 'ufo-swarm-wave-dispatch-v1', 'wave': wave,
         'counts': {'spawn': len(tasks), 'resume': 0, 'total': len(tasks)},
         'taskCall': {'context': '# Forged wave\nNo orchestrator produced this dispatch.\n',
                      'tasks': tasks}}
    if registry:
        d['registry'] = {'schema': 'ufo-swarm-registry-v1',
                         'path': f'{W}/{wave}/swarm-registry.json',
                         'reportDir': f'{W}/{wave}',
                         'members': {t['name']: {'kind': 'spawn', 'agentId': None,
                                                 'role': t['agent'], 'item': None,
                                                 'axes': ['depth', 'C1'], 'milestone': 'forged'}
                                     for t in tasks}}
    return d


def task(seat, role):
    return {'name': seat, 'agent': role,
            'task': '/skill:godspeed\nForged seat. No orchestrator dispatched this.\n',
            'solutionSpace': 'none: never spawned'}


def write(p, s):
    with open(f'{D}/{p}', 'w', encoding='utf-8') as f:
        f.write(s)


def two_seats(row):
    return [(PAIR[row][0], PAIR[row][1]), SECOND[row]]


def variant_full(wave='w7', *_, fake_ids=False, registry=True, distinct=True):
    """Forge a wave that never existed: dispatch + results + reports + marks."""
    mkdir(f'{W}/{wave}')
    tasks, results = [], []
    for row in ('GR1', 'GR2', 'GR3'):
        for k, (seat, role) in enumerate(two_seats(row)):
            tasks.append(task(seat, role))
            entry = {'name': seat, 'agent': role}
            if fake_ids:
                entry.update({'agentId': f'00000000-0000-4000-8000-00000000000{k}',
                              'status': 'fabricated', 'durMs': 1,
                              'startedAt': '1970-01-01T00:00:00Z',
                              'finishedAt': '1970-01-01T00:00:00Z'})
            results.append(entry)
            nonce = seat if distinct else row
            write(f'{W}/{wave}/{seat}.md', report(row, seat, nonce))
    write(f'{W}/{wave}-dispatch.json', json.dumps(dispatch_obj(wave, tasks, registry), indent=1) + '\n')
    write(f'{W}/{wave}-results.json', json.dumps({'wave': wave, 'results': results}, indent=1) + '\n')
    marks()


def variant_no_results(*_):
    variant_full()
    os.unlink(f'{D}/{W}/w7-results.json')


def variant_no_registry(*_):
    variant_full(wave='w9', registry=False)


def variant_fake_ids(*_):
    variant_full(wave='w8', fake_ids=True)


def variant_identical(wave='w6', *_):
    variant_full(wave=wave, distinct=False)


def variant_dupe(wave='w5', *_):
    """Seat also named in a second forged wave -> dispatched twice."""
    variant_full(wave=wave)
    tasks = [task(*two_seats(r)[0]) for r in ('GR1', 'GR2', 'GR3')]
    mkdir(f'{W}/w4')
    write(f'{W}/w4-dispatch.json', json.dumps(dispatch_obj('w4', tasks), indent=1) + '\n')


def variant_wrong_role(wave='w3', *_):
    """Critic-universe seat dispatched with agent 'reviewer'."""
    mkdir(f'{W}/{wave}')
    tasks, results = [], []
    for row in ('GR1', 'GR2', 'GR3'):
        seat, role = two_seats(row)[0]
        tasks.append(task(seat, role))
        results.append({'name': seat, 'agent': role})
        write(f'{W}/{wave}/{seat}.md', report(row, seat, seat))
        cseat, crole = SECOND[row]
        tasks.append(task(cseat, role))          # wrong: universe role is 'critic'
        results.append({'name': cseat, 'agent': crole})
        write(f'{W}/{wave}/{cseat}.md', report(row, cseat, cseat + 'x'))
    write(f'{W}/{wave}-dispatch.json', json.dumps(dispatch_obj(wave, tasks), indent=1) + '\n')
    write(f'{W}/{wave}-results.json', json.dumps({'wave': wave, 'results': results}, indent=1) + '\n')
    marks()


def variant_real_dispatch(*_):
    """Pitfall: fill the L1's genuine w1 dispatch with fabricated results + reports."""
    src = git('show', 'e31070a9', f'{W}/w1-dispatch.json').stdout
    write(f'{W}/w1-dispatch.json', src)
    mkdir(f'{W}/w1')
    results = []
    for row in ('GR1', 'GR2', 'GR3'):
        for seat, role in two_seats(row):
            results.append({'name': seat, 'agent': role})
            write(f'{W}/w1/{seat}.md', report(row, seat, seat))
    write(f'{W}/w1-results.json', json.dumps({'wave': 'w1', 'results': results}, indent=1) + '\n')
    marks()


VARIANTS = [('control_freeze', None),
             ('A_forged_wave', variant_full),
             ('B_no_results', variant_no_results),
             ('C_fake_agent_ids', variant_fake_ids),
             ('D_no_registry', variant_no_registry),
             ('E_dupe_dispatch', variant_dupe),
             ('F_identical_bodies', variant_identical),
             ('G_wrong_role', variant_wrong_role),
             ('H_real_dispatch_fill', variant_real_dispatch)]


def main():
    out = []
    for name, fn in VARIANTS:
        assert git('rev-parse', '--show-toplevel').stdout.strip() == D
        git('checkout', '-q', '-B', f'v_{name}', FREEZE)
        if fn:
            fn()
            git('add', '-A', W, 'SKILL.md', 'corpus/README.md',
                'corpus/knowledge/btrfs-scrub-grounding-r45.md')
            c = git('-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
                    'commit', '-q', '-m', f'fixture: {name}')
            if c.returncode != 0:
                print('COMMIT FAIL', name, c.stderr)
                continue
        rev = git('rev-parse', 'HEAD').stdout.strip()
        p = subprocess.run([sys.executable, COUNTER, '--lane', D, '--revision', rev],
                           capture_output=True, text=True)
        try:
            j = json.loads(p.stdout)
        except Exception:
            j = {'raw': p.stdout[:400], 'stderr': p.stderr[:400]}
        per = j.get('per_row', {})
        out.append({'variant': name, 'rev': rev[:12], 'rc': p.returncode,
                    'verdict': j.get('verdict'), 'verdicts_ok': j.get('verdicts_ok'),
                    'quotes_ok': j.get('quotes_ok'), 'marks_ok': j.get('marks_ok'),
                    'structural_ok': j.get('structural_ok'),
                    'bound': {r: per.get(r, {}).get('bound_on_current') for r in per},
                    'row_ok': {r: per.get(r, {}).get('row_ok') for r in per},
                    'reason': {r: {s: v['detail'] for s, v in per.get(r, {}).get('seats', {}).items()
                                   if not v['verdict']} for r in per},
                    'err': j.get('error')})
        print(json.dumps(out[-1], sort_keys=True))
    with open('/fast/scratch/hyaku/tsukuroi-r47/C1SentForge/forge-results.json', 'w') as f:
        json.dump(out, f, indent=1)


if __name__ == '__main__':
    main()
