#!/usr/bin/env python3
"""Path tricks against the frozen C2 counter, each applied on top of forgery B.

Every trick starts from the B tip, mutates inside the sandbox, commits, runs the
frozen counter and records what happened to seat R48RevGR1a (and GR1 credit).
"""
import json, os, shutil, subprocess, sys

SBX = '/fast/scratch/hyaku/tsukuroi-r48/GSentForge/sbx'
FROZEN = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER = f'{FROZEN}/tools/check-scrub-admission-r48.py'
BASE = 'ae99f021b76f8eb1c8805d32d80644464afb1ff6'
W = '.ufo/waves/round-48'
OUT = '/fast/scratch/hyaku/tsukuroi-r48/GSentForge/receipts'


def sh(args, **kw):
    r = subprocess.run(args, capture_output=True, text=True, **kw)
    return r


def git(*a):
    r = sh(['git', '-C', SBX, *a])
    if r.returncode != 0:
        raise SystemExit(f'git {" ".join(a)}: {r.stderr}')
    return r.stdout


def commit(msg):
    git('add', '-A')
    git('-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid', 'commit', '-qm', msg)


def run_counter(tag):
    r = sh(['python3', COUNTER, '--lane', SBX, '--revision', 'HEAD'])
    path = f'{OUT}/{tag}-counter.json'
    with open(path, 'w') as f:
        f.write(r.stdout)
    try:
        d = json.loads(r.stdout)
    except Exception:
        return {'exit': r.returncode, 'stderr': r.stderr[-400:], 'raw': r.stdout[-400:]}
    g = d.get('per_row', {}).get('GR1', {})
    return {'exit': r.returncode, 'verdict': d.get('verdict'),
            'gr1_credited': len(g.get('credited', [])), 'gr1_row_ok': g.get('row_ok'),
            'seat_R48RevGR1a': g.get('seats', {}).get('R48RevGR1a'),
            'verdicts_ok': d.get('verdicts_ok')}


def load(p):
    with open(os.path.join(SBX, p)) as f:
        return json.load(f)


def dump(p, o):
    with open(os.path.join(SBX, p), 'w') as f:
        json.dump(o, f, indent=1)
        f.write('\n')


def main():
    B = sys.argv[1]
    results = {}
    assert git('rev-parse', '--show-toplevel').strip() == SBX

    # T0: baseline
    git('reset', '-q', '--hard', B)
    results['T0_baseline'] = run_counter('trick-T0')

    # T1: traversal name as dispatch seat + report parked in the w1 dir
    git('reset', '-q', '--hard', B)
    os.rename(os.path.join(SBX, f'{W}/w2/R48RevGR1a.md'), os.path.join(SBX, f'{W}/w1/R48RevGR1a.md'))
    d = load(f'{W}/w2-dispatch.json')
    d['taskCall']['tasks'].append({'name': '../w1/R48RevGR1a', 'agent': 'reviewer',
                                   'task': 'Item C2-GR1-../w1/R48RevGR1a traversal probe ' + 'x' * 200})
    dump(f'{W}/w2-dispatch.json', d)
    commit('trick T1: traversal seat name, report in w1')
    results['T1_traversal_seat'] = run_counter('trick-T1')
    results['T1_git_show_dotdot'] = sh(['git', '-C', SBX, 'show',
                                        f'HEAD:{W}/w2/../w1/R48RevGR1a.md']).returncode

    # T2: report is a relative symlink to another seat's report
    git('reset', '-q', '--hard', B)
    p = os.path.join(SBX, f'{W}/w2/R48RevGR1a.md')
    os.remove(p)
    os.symlink('R48RevGR1c.md', p)
    commit('trick T2: relative symlink report')
    results['T2_symlink_relative'] = run_counter('trick-T2')

    # T3: report is an absolute symlink to a path outside the repo
    git('reset', '-q', '--hard', B)
    p = os.path.join(SBX, f'{W}/w2/R48RevGR1a.md')
    os.remove(p)
    os.symlink('/etc/hostname', p)
    commit('trick T3: absolute symlink report')
    results['T3_symlink_absolute'] = run_counter('trick-T3')

    # T4: report only in the w1 dir, dispatch unchanged
    git('reset', '-q', '--hard', B)
    os.rename(os.path.join(SBX, f'{W}/w2/R48RevGR1a.md'), os.path.join(SBX, f'{W}/w1/R48RevGR1a.md'))
    commit('trick T4: report in another wave dir')
    results['T4_other_wave_dir'] = run_counter('trick-T4')

    # T5: the w2 directory itself becomes a symlink to a sibling directory
    git('reset', '-q', '--hard', B)
    os.rename(os.path.join(SBX, f'{W}/w2'), os.path.join(SBX, f'{W}/w2-alt'))
    os.symlink('w2-alt', os.path.join(SBX, f'{W}/w2'))
    commit('trick T5: w2 is a symlinked directory')
    results['T5_wave_dir_symlink'] = run_counter('trick-T5')

    # T6: duplicate JSON key in the dispatch
    git('reset', '-q', '--hard', B)
    raw = open(os.path.join(SBX, f'{W}/w2-dispatch.json')).read()
    raw = raw.replace('"wave": "w2",', '"wave": "w2",\n "wave": "w1",', 1)
    open(os.path.join(SBX, f'{W}/w2-dispatch.json'), 'w').write(raw)
    commit('trick T6: duplicate dispatch key')
    results['T6_duplicate_key'] = run_counter('trick-T6')

    # T7: the seat is dispatched twice
    git('reset', '-q', '--hard', B)
    d = load(f'{W}/w2-dispatch.json')
    t = dict(d['taskCall']['tasks'][0])
    d['taskCall']['tasks'].append(t)
    dump(f'{W}/w2-dispatch.json', d)
    commit('trick T7: duplicated dispatch entry')
    results['T7_duplicate_dispatch'] = run_counter('trick-T7')

    # T8: results entry role disagrees with the dispatch
    git('reset', '-q', '--hard', B)
    r = load(f'{W}/w2-results.json')
    for e in r['results']:
        if e['name'] == 'R48RevGR1a':
            e['agent'] = 'critic'
    dump(f'{W}/w2-results.json', r)
    commit('trick T8: results role mismatch')
    results['T8_role_mismatch'] = run_counter('trick-T8')

    # T9: two results entries for the same seat
    git('reset', '-q', '--hard', B)
    r = load(f'{W}/w2-results.json')
    r['results'].append(dict(r['results'][0]))
    dump(f'{W}/w2-results.json', r)
    commit('trick T9: duplicated results entry')
    results['T9_duplicate_results'] = run_counter('trick-T9')

    # T10: CRLF line endings in one report (brittleness probe, not an attack)
    git('reset', '-q', '--hard', B)
    p = os.path.join(SBX, f'{W}/w2/R48RevGR1a.md')
    data = open(p).read().replace('\n', '\r\n')
    open(p, 'w', newline='').write(data)
    commit('trick T10: CRLF report')
    results['T10_crlf_report'] = run_counter('trick-T10')

    git('reset', '-q', '--hard', B)
    print(json.dumps(results, indent=1, sort_keys=True))


main()
