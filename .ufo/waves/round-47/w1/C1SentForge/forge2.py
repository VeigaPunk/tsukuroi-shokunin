#!/usr/bin/env python3
"""C1-S2 part 2: K23 test (truly identical bodies), real-dispatch fill, backdated commit,
and provenance laundering of a real round-46 seat body."""
import json
import os
import re
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER = f'{LANE}/tools/check-scrub-admission-r47.py'
FREEZE = '77e9e2b2e96b85d8f048ae2087e246a542b71611'
D = sys.argv[1]
W = '.ufo/waves/round-47'
H = {'GR1': 'fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8',
     'GR2': '909830c83cbcf0a02264153fa6f179415fb8388d3e08c43d79fbf33c8cfa11a2',
     'GR3': '43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c'}
PAIR = {'GR1': ('R47RevGR1a', 'reviewer'), 'GR2': ('R47RevGR2a', 'reviewer'),
        'GR3': ('R47RevGR3a', 'reviewer')}
PAIR2 = {'GR1': ('R47CritGR1a', 'critic'), 'GR2': ('R47CritGR2a', 'critic'),
         'GR3': ('R47CritGR3a', 'critic')}
CITE = {'GR1': ['cmdline.c:1', 'vsprintf.c:1', 'kstrtox.c:1', 'sysfs.c:1'],
        'GR2': ['dev-replace.c:1143', 'scrub.c:3094', 'sysfs.c:1'],
        'GR3': ['systemd.kill.xml:1', 'btrfs-scrub@.service:1', 'scrub.c:1', 'capture.txt:1']}
PAD = ('The body is a template emitted by a forger: no agent produced it, no transcript backs '
       'it, and the only bytes supporting the row are in the forging commit itself. It exists to '
       'clear the 300-byte floor and the citation leg, nothing more.')


def git(*a, env=None):
    return subprocess.run(['git', '-C', D, *a], capture_output=True, text=True, env=env)


def body(row, tag):
    return PAD + '\n' + '\n'.join(f'- resolves at {c}' for c in CITE[row]) + f'\n{tag}\n'


def rep(row, tag):
    return f'ROW {row} VERDICT: holds\nSECTION SHA256: {H[row]}\n{body(row, tag)}\n'


def write(p, s):
    with open(f'{D}/{p}', 'w', encoding='utf-8') as f:
        f.write(s)


def marks():
    for path, line in (('corpus/knowledge/btrfs-scrub-grounding-r45.md',
                        '## Gate status — round 47 (GR1-GR3 admitted)'),
                       ('SKILL.md', '## Scrub grounding — round 47 admission'),
                       ('corpus/README.md',
                        '- `btrfs-scrub-grounding-r45.md` admitted round 47 (fabricated mark).')):
        cur = open(f'{D}/{path}', encoding='utf-8').read()
        add = f'\n{line}\n'
        if add not in cur:
            open(f'{D}/{path}', 'w', encoding='utf-8').write(cur + add)


def task(seat, role):
    return {'name': seat, 'agent': role, 'task': 'forged: never spawned',
            'solutionSpace': 'none'}


def disp(wave, tasks):
    return json.dumps({'schema': 'ufo-swarm-wave-dispatch-v1', 'wave': wave,
                       'counts': {'spawn': len(tasks), 'resume': 0, 'total': len(tasks)},
                       'taskCall': {'context': '# forged', 'tasks': tasks}}, indent=1) + '\n'


def commit(msg, date=None):
    git('add', '-A', W, 'SKILL.md', 'corpus/README.md',
        'corpus/knowledge/btrfs-scrub-grounding-r45.md')
    env = dict(os.environ)
    if date:
        env.update({'GIT_AUTHOR_DATE': date, 'GIT_COMMITTER_DATE': date})
    c = git('-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
            'commit', '-q', '-m', msg, env=env)
    if c.returncode != 0:
        raise SystemExit(f'commit failed: {c.stderr}')


def base(wave):
    """dispatch for 6 seats (2 per row, universe-valid roles) + results + reports."""
    os.makedirs(f'{D}/{W}/{wave}', exist_ok=True)
    tasks, results = [], []
    for row in ('GR1', 'GR2', 'GR3'):
        for seat, role, tag in ((*PAIR[row], 'alpha'), (*PAIR2[row], 'beta')):
            tasks.append(task(seat, role))
            results.append({'name': seat, 'agent': role})
            write(f'{W}/{wave}/{seat}.md', rep(row, tag))
    write(f'{W}/{wave}-dispatch.json', disp(wave, tasks))
    write(f'{W}/{wave}-results.json', json.dumps({'wave': wave, 'results': results}, indent=1) + '\n')
    marks()


def v_identical():
    """K23: the two bound seats of each row carry byte-identical bodies."""
    wave = 'w6'
    os.makedirs(f'{D}/{W}/{wave}', exist_ok=True)
    tasks, results = [], []
    same = {r: rep(r, 'x') for r in H}
    for row in ('GR1', 'GR2', 'GR3'):
        for seat, role in (PAIR[row], PAIR2[row]):
            tasks.append(task(seat, role))
            results.append({'name': seat, 'agent': role})
            write(f'{W}/{wave}/{seat}.md', same[row])
    write(f'{W}/{wave}-dispatch.json', disp(wave, tasks))
    write(f'{W}/{wave}-results.json', json.dumps({'wave': wave, 'results': results}, indent=1) + '\n')
    marks()


def v_identical_nonce():
    """K23 evasion: one extra character of nonce per body."""
    wave = 'w6'
    os.makedirs(f'{D}/{W}/{wave}', exist_ok=True)
    tasks, results = [], []
    for row in ('GR1', 'GR2', 'GR3'):
        for seat, role, tag in ((*PAIR[row], 'x1'), (*PAIR2[row], 'x2')):
            tasks.append(task(seat, role))
            results.append({'name': seat, 'agent': role})
            write(f'{W}/{wave}/{seat}.md', rep(row, tag))
    write(f'{W}/{wave}-dispatch.json', disp(wave, tasks))
    write(f'{W}/{wave}-results.json', json.dumps({'wave': wave, 'results': results}, indent=1) + '\n')
    marks()


def v_real_fill():
    """Fill the L1's genuine w1 dispatch (rev e31070a9) with forged results + reports."""
    src = subprocess.run(['git', '-C', LANE, 'show',
                          'e31070a9:.ufo/waves/round-47/w1-dispatch.json'],
                         capture_output=True, text=True)
    assert src.returncode == 0 and len(src.stdout) > 100000, (src.returncode, len(src.stdout))
    print('  w1-dispatch fetched bytes:', len(src.stdout))
    write(f'{W}/w1-dispatch.json', src.stdout)
    os.makedirs(f'{D}/{W}/w1', exist_ok=True)
    results = []
    for row in ('GR1', 'GR2', 'GR3'):
        for seat, role, tag in ((*PAIR[row], 'alpha'), (*PAIR2[row], 'beta')):
            results.append({'name': seat, 'agent': role, 'note': None})
            write(f'{W}/w1/{seat}.md', rep(row, tag))
    write(f'{W}/w1-results.json', json.dumps({'lane': 'tsukuroi', 'round': 47, 'wave': 'w1',
                                             'results': results}, indent=1) + '\n')
    marks()


def v_backdated():
    """Same forgery, committed with 2001 timestamps."""
    base('w11')


def v_laundered():
    """Body copied from a real round-46 seat report; only the two binding lines are forged."""
    real = open(f'{LANE}/.ufo/waves/round-46/r1/V46ResCritGR2.md', encoding='utf-8').read()
    lines = [ln for ln in real.split('\n')[2:]
             if not re.match(r'ROW GR\d VERDICT|SECTION SHA256', ln)]
    stolen = '\n'.join(lines)
    text = f'ROW GR2 VERDICT: holds\nSECTION SHA256: {H["GR2"]}\n{stolen}\n'
    print('  laundered body bytes:', len(text), 'citations:',
          re.findall(r'\b([A-Za-z0-9_.@+-]+\.[a-z0-9]+):(\d+)\b', stolen)[:6])
    base('w12')
    write(f'{W}/w12/R47CritGR2a.md', text)
    write(f'{W}/w12/R47RevGR2a.md', rep('GR2', 'alpha'))


V = [('F_identical_bodies', v_identical, None),
     ('F2_k23_nonce', v_identical_nonce, None),
     ('H_real_dispatch_fill', v_real_fill, None),
     ('I_backdated', v_backdated, '2001-01-01T00:00:00Z'),
     ('L_laundered_body', v_laundered, None)]


def main():
    out = []
    for name, fn, date in V:
        assert git('rev-parse', '--show-toplevel').stdout.strip() == D
        git('checkout', '-q', '-B', f'v2_{name}', FREEZE)
        fn()
        commit(f'fixture: {name}', date)
        rev = git('rev-parse', 'HEAD').stdout.strip()
        p = subprocess.run([sys.executable, COUNTER, '--lane', D, '--revision', rev],
                           capture_output=True, text=True)
        j = json.loads(p.stdout)
        per = j.get('per_row', {})
        rec = {'variant': name, 'rev': rev[:12], 'rc': p.returncode, 'verdict': j.get('verdict'),
               'verdicts_ok': j.get('verdicts_ok'), 'marks_ok': j.get('marks_ok'),
               'quotes_ok': j.get('quotes_ok'), 'structural_ok': j.get('structural_ok'),
               'bound': {r: per[r]['bound_on_current'] for r in per},
               'distinct': {r: per[r]['distinct_bodies'] for r in per},
               'row_ok': {r: per[r]['row_ok'] for r in per},
               'unbound': {r: [s for s, v in per[r]['seats'].items() if not v['verdict']]
                           for r in per},
               'detail': {r: {s: v['detail'] for s, v in per[r]['seats'].items()
                              if not v['verdict']} for r in per}}
        rec['commit_date'] = git('log', '-1', '--format=%aI').stdout.strip()
        out.append(rec)
        print(json.dumps(rec, sort_keys=True))
    json.dump(out, open('/fast/scratch/hyaku/tsukuroi-r47/C1SentForge/forge2-results.json', 'w'),
              indent=1)


if __name__ == '__main__':
    main()
