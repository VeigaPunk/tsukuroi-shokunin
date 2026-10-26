import json, os, subprocess, sys, pathlib
S = pathlib.Path('/fast/scratch/hyaku/tsukuroi-r38/C1CritControl')
D = S / 'clone'; CENSUS = D / 'tools/tsukuroi-census.sh'
COUNTER = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-storage-arm-r38.py'
BASE = '5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf'
ANCHOR = '# ---- hermetic selftest'
def git(*a):
    return subprocess.run(['git', '-C', str(D), *a], capture_output=True, text=True)
def run(name):
    k = git('reset', '--hard', BASE).returncode
    assert k == 0, 'reset failed'
    txt = CENSUS.read_text()
    assert txt.count(ANCHOR) == 1, txt.count(ANCHOR)
    body = (S / 'cands' / f'{name}.sh').read_text()
    CENSUS.write_text(txt.replace(ANCHOR, body + '\n' + ANCHOR, 1))
    assert git('add', 'tools/tsukuroi-census.sh').returncode == 0
    c = git('-c', 'user.name=C1CritControl', '-c', 'user.email=crit@example.invalid',
            'commit', '-q', '-m', f'CONTROL {name}: cheap storage arm')
    assert c.returncode == 0, c.stderr
    sha = git('rev-parse', 'HEAD').stdout.strip()
    out = S / f'{name}.json'
    p = subprocess.run(['python3', COUNTER, '--repo', str(D), '--revision', sha,
                        '--scratch', str(S / 'tmp')], capture_output=True, text=True, timeout=900)
    out.write_text(p.stdout)
    d = json.loads(p.stdout)
    d['candidate'], d['commit'] = name, sha
    d['diffstat'] = git('show', '--stat', '--oneline', 'HEAD').stdout.strip().splitlines()[-1]
    print(json.dumps({k: d[k] for k in ('candidate', 'commit', 'fixtures_matched', 'fixtures_expected',
                                        'live_match', 'six_planes_all', 'result')}))
    for f in d['fixtures']:
        if not f['match']:
            print('   MISS', f['fixture'], 'exp', f['expected'], 'got', f['got'])
    out.write_text(json.dumps(d, indent=1))
    return d
res = [run(n) for n in sys.argv[1:]]
