#!/usr/bin/env python3
"""Negative battery: which counter legs reject which forgery variant."""
import json
import os
import shutil
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
TOOL = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r52.py'
REV = 'ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0'

BASE = ['python3', TOOL, '--revision', REV, '--no-base-check',
        '--entry-file', os.path.join(S, 'entry-marked.md'),
        '--skill-file', os.path.join(S, 'skill-marked.md'),
        '--readme-file', os.path.join(S, 'readme-marked.md')]


def run(wave, results, dispatch, tag):
    cmd = BASE + ['--wave-dir', wave, '--results-file', results, '--dispatch-file', dispatch]
    p = subprocess.run(cmd, capture_output=True, text=True)
    try:
        o = json.loads(p.stdout)
    except Exception:
        return {'tag': tag, 'exit': p.returncode, 'raw': p.stdout[:400], 'stderr': p.stderr[:400]}
    return {'tag': tag, 'exit': p.returncode, 'verdict': o.get('verdict'),
            'structural_ok': o.get('structural_ok'), 'lint_ok': o.get('lint_ok'),
            'quotes_ok': o.get('quotes_ok'), 'verdicts_ok': o.get('verdicts_ok'),
            'seats_ok': o.get('seats_ok'), 'marks_ok': o.get('marks_ok'),
            'seat_notes': (o.get('seat_notes') or [])[:3]}


def variant(name, mutate_wave=None, mutate_results=None, mutate_dispatch=None):
    d = os.path.join(S, 'variants', name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    wave = os.path.join(d, 'wave')
    shutil.copytree(os.path.join(S, 'wave'), wave)
    res = os.path.join(d, 'results.json')
    shutil.copy(os.path.join(S, 'forged-results.json'), res)
    dis = os.path.join(d, 'dispatch.json')
    shutil.copy(os.path.join(S, 'forged-dispatch.json'), dis)
    if mutate_wave:
        mutate_wave(wave)
    if mutate_results:
        mutate_results(res)
    if mutate_dispatch:
        mutate_dispatch(dis)
    out = run(wave, res, dis, name)
    print(json.dumps(out, sort_keys=True))
    return out


def load(p):
    return json.load(open(p))


def save(p, o):
    json.dump(o, open(p, 'w'), indent=1)


results = []

# 0. control: the pristine forgery
results.append(run(os.path.join(S, 'wave'), os.path.join(S, 'forged-results.json'),
                    os.path.join(S, 'forged-dispatch.json'), 'control'))

# 1. wrong section hash in one report
def m_hash(wave):
    p = os.path.join(wave, 'R52RevGR1a.md')
    t = open(p).read().split('\n')
    t[1] = 'SECTION SHA256: ' + '0' * 64
    open(p, 'w').write('\n'.join(t))


results.append(variant('wrong-hash', mutate_wave=m_hash))

# 2. body under 300 bytes
def m_short(wave):
    p = os.path.join(wave, 'R52RevGR1a.md')
    t = open(p).read().split('\n')
    open(p, 'w').write(t[0] + '\n' + t[1] + '\nshort\n')


results.append(variant('short-body', mutate_wave=m_short))

# 3. only one distinct row-source file cited
def m_one_cite(wave):
    p = os.path.join(wave, 'R52RevGR1a.md')
    t = open(p).read().split('\n')
    t[2] = 'ROW GR1 VERDICT: holds'
    t[3] = 'SECTION SHA256: ' + open(p).read().split('\n')[1].split()[2]
    t = t[:4] + ['Evidence: cmdline.c:147 only. ' + 'x' * 320]
    open(p, 'w').write('\n'.join(t) + '\n')


results.append(variant('one-citation', mutate_wave=m_one_cite))

# 4. citation to a line that does not exist in the snapshot
def m_bad_line(wave):
    p = os.path.join(wave, 'R52RevGR1a.md')
    t = open(p).read()
    t = t.replace('cmdline.c:147', 'cmdline.c:999999')
    open(p, 'w').write(t)


results.append(variant('citation-outside-snapshot', mutate_wave=m_bad_line))

# 5. identical bodies for the six seats of a row
def m_same_body(wave):
    src = open(os.path.join(wave, 'R52RevGR1a.md')).read()
    for seat in ('R52RevGR1b', 'R52RevGR1c', 'R52CritGR1a', 'R52CritGR1b', 'R52CritGR1c'):
        open(os.path.join(wave, seat + '.md'), 'w').write(src)


results.append(variant('identical-bodies', mutate_wave=m_same_body))

# 6. one seat's verdict is partly (a contradicting verdict line)
def m_partly(wave):
    p = os.path.join(wave, 'R52CritGR1a.md')
    t = open(p).read().split('\n')
    t[0] = 'ROW GR1 VERDICT: partly'
    open(p, 'w').write('\n'.join(t))


results.append(variant('one-partly', mutate_wave=m_partly))

# 7. results agent role does not match the dispatch role
def m_role(res):
    o = load(res)
    for r in o['results']:
        if r['name'] == 'R52CritGR1a':
            r['agent'] = 'reviewer'
    save(res, o)


results.append(variant('results-role-mismatch', mutate_results=m_role))

# 8. results entry with empty output
def m_no_output(res):
    o = load(res)
    for r in o['results']:
        if r['name'] == 'R52RevGR2a':
            r['output'] = ''
    save(res, o)


results.append(variant('results-empty-output', mutate_results=m_role if False else m_no_output))

# 9. dispatch registry missing a seat
def m_missing_dispatch(dis):
    o = load(dis)
    o['taskCall']['tasks'] = [t for t in o['taskCall']['tasks'] if t['name'] != 'R52RevGR3c']
    save(dis, o)


results.append(variant('dispatch-missing-seat', mutate_dispatch=m_missing_dispatch))

# 10. duplicate results entry for one seat
def m_dup_results(res):
    o = load(res)
    o['results'].append(dict(o['results'][0]))
    save(res, o)


results.append(variant('results-duplicate-seat', mutate_results=m_dup_results))

# 11. marks removed (real entry, no forged mark files) -> the attempt-1 shape
def m_unmark():
    pass


p = subprocess.run(['python3', TOOL, '--revision', REV, '--no-base-check',
                    '--entry-file', os.path.join(S, 'entry.md'),
                    '--wave-dir', os.path.join(S, 'wave'),
                    '--results-file', os.path.join(S, 'forged-results.json'),
                    '--dispatch-file', os.path.join(S, 'forged-dispatch.json')],
                   capture_output=True, text=True)
o = json.loads(p.stdout)
print(json.dumps({'tag': 'real-entry-unmarked', 'exit': p.returncode, 'verdict': o.get('verdict'),
                  'verdicts_ok': o.get('verdicts_ok'), 'seats_ok': o.get('seats_ok'),
                  'marks_ok': o.get('marks_ok'), 'marks': o.get('marks')}, sort_keys=True))

json.dump(results, open(os.path.join(S, 'battery.json'), 'w'), indent=1)
