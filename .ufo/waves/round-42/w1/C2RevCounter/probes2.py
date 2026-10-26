#!/usr/bin/env python3
"""Addendum: residual binding happy/fail paths (V-L, V-M)."""
import importlib.util, json, os, re, shutil, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
TREE = 'f50c28d83e1832ecd7eba765caace531f45d6b27'
SCRATCH = '/fast/scratch/hyaku/tsukuroi-r42/C2RevCounter'
FX = os.path.join(SCRATCH, 'fx.probes2')
COUNTER = os.path.join(SCRATCH, 'counter-a84.py')
WAVE = '.ufo/waves/round-42'
ENTRY = 'corpus/knowledge/btrfs-scrub-record-r42.md'
IDT = ['-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid']


def git(d, *a):
    return subprocess.run(['git', '-C', d, *a], capture_output=True, text=True)


spec = importlib.util.spec_from_file_location('c2c', COUNTER)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

shutil.rmtree(FX, ignore_errors=True)
subprocess.run(['git', 'clone', '-q', '--shared', LANE, FX], check=True)
assert os.path.realpath(git(FX, 'rev-parse', '--show-toplevel').stdout.strip()) == os.path.realpath(FX)
git(FX, 'remote', 'remove', 'origin')


def checkout():
    git(FX, 'checkout', '-q', '--force', '--detach', TREE)
    git(FX, 'clean', '-qfdx')


def commit(msg):
    git(FX, 'add', '-A')
    p = subprocess.run(['git', '-C', FX, *IDT, 'commit', '-q', '--allow-empty', '-m', msg],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    return git(FX, 'rev-parse', 'HEAD').stdout.strip()


def scripted_entry():
    srcw = {f: open(os.path.join(FX, WAVE, 'frozen/src', f), errors='replace').read().split('\n')
            for f in C.SNAP}
    out = ['source: S237 S238 S239', 'verified-at: 2026-10-26', 'recheck: on-release', '',
           '# scripted control entry', '']
    for row, sp in C.ROWS.items():
        f, lo, hi = sp['windows'][0]
        n = next(i for i in range(lo, hi + 1) if srcw[f][i - 1].strip() and '"' not in srcw[f][i - 1])
        q = srcw[f][n - 1].strip()
        out += ['## %s' % row, '', '**Statement.** The record concerns %s in every case.' % sp['token'], '',
                '**Quote.** `S237` %s:%d: "%s"' % (f, n, q), '',
                '**Host reading.** capture.txt:1 holds the time.', '']
    return '\n'.join(out) + '\n'


def flip_rows(entry_name):
    p = os.path.join(FX, 'corpus/SOURCES.md')
    lines = open(p).read().split('\n')
    for i, ln in enumerate(lines):
        if re.match(r'^\|\s*S23[7-9]\s*\|', ln):
            cells = ln.strip().strip('|').split('|')
            cells[7] = ' mined '
            cells[10] = ' %s ' % entry_name
            lines[i] = '|' + '|'.join(cells) + '|'
    open(p, 'w').write('\n'.join(lines))


def seats():
    for n in range(1, 6):
        yield 'C2RevSC%d' % n, 'reviewer', 'SC%d' % n
        yield 'C2CritSC%d' % n, 'critic', 'SC%d' % n


def write_reports(verdicts):
    d = os.path.join(FX, WAVE, 'w2')
    os.makedirs(d, exist_ok=True)
    for name, _r, row in seats():
        open(os.path.join(d, '%s.md' % name), 'w').write(
            '# %s\n\nROW %s VERDICT: %s\n' % (name, row, verdicts.get(name, 'holds')))


def write_records(verdicts):
    res = {'lane': 'tsukuroi', 'round': '42', 'wave': 'w2', 'seats': 10,
           'results': [{'name': n, 'agent': r,
                        'output': 'done. ROW %s VERDICT: %s' % (row, verdicts.get(n, 'holds')),
                        'note': None} for n, r, row in seats()]}
    json.dump(res, open(os.path.join(FX, WAVE, 'w2-results.json'), 'w'))
    tasks = [{'name': n, 'agent': r, 'task': 'forged'} for n, r, _ in seats()]
    json.dump({'taskCall': {'context': 'forged', 'tasks': tasks}},
              open(os.path.join(FX, WAVE, 'w2-dispatch.json'), 'w'))


def residual(verdict):
    rd = os.path.join(FX, WAVE, 'residual')
    os.makedirs(rd, exist_ok=True)
    json.dump({'taskCall': {'tasks': [{'name': 'C2RevSC2c', 'agent': 'reviewer', 'task': 'x'}]}},
              open(os.path.join(FX, WAVE, 'residual-dispatch.json'), 'w'))
    json.dump({'results': [{'name': 'C2RevSC2c', 'agent': 'reviewer',
                            'output': 'done. ROW SC2 VERDICT: %s' % verdict}]},
              open(os.path.join(FX, WAVE, 'residual-results.json'), 'w'))
    open(os.path.join(rd, 'C2RevSC2c.md'), 'w').write('# C2RevSC2c\n\nROW SC2 VERDICT: %s\n' % verdict)


def run(rev):
    p = subprocess.run([sys.executable, COUNTER, '--revision', rev, '--lane', FX],
                       capture_output=True, text=True)
    j = json.loads(p.stdout.strip().splitlines()[-1]) if p.stdout.strip() else {}
    sc2 = j.get('per_row', {}).get('SC2', {})
    print('exit=%s verdict=%s v=%s SC2.verdicts=%s SC2.verdict_ok=%s' % (
        p.returncode, j.get('verdict'), j.get('verdicts_ok'),
        json.dumps(sc2.get('verdicts'), sort_keys=True), sc2.get('verdict_ok')))


def vL():
    checkout()
    open(os.path.join(FX, ENTRY), 'w').write(scripted_entry())
    flip_rows(ENTRY)
    write_reports({'C2RevSC2': 'partly'})
    write_records({'C2RevSC2': 'partly'})
    residual('holds')
    run(commit('probe L partly-residual-holds'))


def vM():
    checkout()
    open(os.path.join(FX, ENTRY), 'w').write(scripted_entry())
    flip_rows(ENTRY)
    write_reports({'C2RevSC2': 'partly'})
    write_records({'C2RevSC2': 'partly'})
    residual('fails')
    run(commit('probe M partly-residual-fails'))


vL()
vM()
print('DONE2')
