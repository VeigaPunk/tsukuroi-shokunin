#!/usr/bin/env python3
"""SentinelProbeHollow harness — falsify the C2 after-value by hand.

For every one of the eleven frozen targets this runs the target four ways with one
piece of instrumentation the declared probe does not have: an LD_PRELOAD constructor
(gitspy.so) that records each git child's own HOME/PATH/GIT_CONFIG_GLOBAL/
GIT_CONFIG_NOSYSTEM/GIT_CEILING_DIRECTORIES, plus the full stdout digest.

Variants
  control       probe-like control env (private HOME, TMPDIR, GIT_CONFIG_NOSYSTEM)
  user-files    hostile HOME/XDG_CONFIG_HOME: .gitconfig + .config/git/config with
                core.hooksPath, .config/git/ignore = '*', .config/git/attributes
  path-wrapper  a `git` shell wrapper first on PATH that logs argv then execs system git
  enclosing     tool tree, cwd and TMPDIR inside a canary repo, WIDENED fingerprint
                (adds .git/config, hooks/, info/, logs/ — the CritProbeDesign gap)

Output: one JSON line per (target, variant, mode); summary compares
  * rc against control,
  * normalised stdout digest against control (hollow detection: the probe compares rc only),
  * every git child's contract variables (hollow detection where rc/stdout are unchanged),
  * hook log / wrapper log / canary fingerprint delta.
Usage: python3 hollow.py --lane <clone> --rev <rev> [--only ...] [--modes ...]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile

TARGETS = (
    ('tools/check-adjacency-overlap.py', ['--selftest']),
    ('tools/check-freshness-r17.py', ['--selftest']),
    ('tools/check-kernel-taint.py', ['--selftest']),
    ('tools/check-memory-pressure.py', ['--selftest']),
    ('tools/check-registry-coverage.py', ['--selftest']),
    ('tools/check-storage-health.py', ['--selftest']),
    ('tools/mutants-adjacency-overlap.py', ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}']),
    ('tools/mutants-kernel-taint.py', ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}']),
    ('tools/check-self-assessment.py', ['--selftest']),
    ('tools/mutants-owed-statements-r29.py',
     ['--base', '81a061a67466c5e1be812814a895a4b5ed89b4ff', '--counter-rev', '{rev}', '--lane', '{clone}']),
    ('tools/mutants-owed-statements-r29-landed.py', ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}']),
)
# production (non-selftest) invocation, run from inside the clone so ROOT resolves there
PRODUCTION = {
    'tools/check-adjacency-overlap.py': ['--revision', '{rev}', '--repo', '{clone}'],
    'tools/check-freshness-r17.py': ['--revision', '{rev}'],
    'tools/check-kernel-taint.py': ['--revision', '{rev}', '--repo', '{clone}'],
    'tools/check-memory-pressure.py': ['--revision', '{rev}'],
    'tools/check-registry-coverage.py': ['--revision', '{rev}'],
    'tools/check-storage-health.py': ['--revision', '{rev}', '--repo', '{clone}'],
    'tools/check-self-assessment.py': ['--revision', '{rev}', '--repo', '{clone}'],
}
HERE = os.path.dirname(os.path.abspath(__file__))
SPY = os.path.join(HERE, 'gitspy.so')
TIMEOUT = 900
HEX40 = re.compile(r'\b[0-9a-f]{40}\b')
HEX64 = re.compile(r'\b[0-9a-f]{64}\b')


def norm(text, root):
    t = text.replace(root, '<ROOT>')
    t = HEX64.sub('<SHA64>', t)
    t = HEX40.sub('<SHA40>', t)
    return '\n'.join(' '.join(line.split()) for line in t.splitlines())


def dig(t):
    return hashlib.sha256(t.encode()).hexdigest()[:16]


def base_env(home, tmpdir, spylog):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'LC_ALL': 'C', 'HOME': home,
                'XDG_CONFIG_HOME': os.path.join(home, '.config'), 'TMPDIR': tmpdir,
                'SPY_LOG': spylog, 'LD_PRELOAD': SPY})
    return env


def run(cmd, cwd, env, timeout=TIMEOUT):
    try:
        r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return 'timeout', b'', b'timeout'


def write_exec(path, body):
    with open(path, 'w') as fh:
        fh.write(body)
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def git(env, *args):
    return subprocess.run(['/usr/bin/git', *args], env=env, capture_output=True)


def fp(canary, env):
    """Widened canary fingerprint: probe fields plus config, hooks, info, logs."""
    gd = os.path.join(canary, '.git')
    h = hashlib.sha256()
    h.update(git(env, '-C', canary, 'rev-parse', 'HEAD').stdout)
    h.update(git(env, '-C', canary, 'for-each-ref', '--format=%(refname) %(objectname)').stdout)
    for sub in ('objects', 'refs', 'hooks', 'info', 'logs'):
        d = os.path.join(gd, sub)
        if not os.path.isdir(d):
            continue
        for dp, _dn, fn in sorted(os.walk(d)):
            for f in sorted(fn):
                p = os.path.join(dp, f)
                h.update(os.path.relpath(p, gd).encode() + b'\n')
                try:
                    with open(p, 'rb') as fh:
                        h.update(hashlib.sha256(fh.read()).digest())
                except OSError:
                    pass
    for f in ('HEAD', 'index', 'packed-refs', 'config'):
        p = os.path.join(gd, f)
        if os.path.exists(p):
            with open(p, 'rb') as fh:
                h.update(f.encode() + hashlib.sha256(fh.read()).digest())
    return h.hexdigest()


def make_canary(path, env):
    os.makedirs(path, exist_ok=True)
    git(env, 'init', '-q', '-b', 'canary', path).check_returncode()
    with open(os.path.join(path, 'CANARY'), 'w') as fh:
        fh.write('canary\n')
    git(env, '-C', path, 'add', 'CANARY').check_returncode()
    git(env, '-C', path, '-c', 'user.name=probe', '-c', 'user.email=probe@invalid',
        '-c', 'commit.gpgsign=false', 'commit', '-qm', 'canary').check_returncode()


def children(spylog):
    """Parse the LD_PRELOAD records: one line per git child, its contract vars."""
    if not os.path.exists(spylog):
        return []
    with open(spylog, encoding='utf-8', errors='replace') as fh:
        rows = []
        for line in fh:
            f = line.rstrip('\n').split('\t')
            if len(f) < 9:
                continue
            rows.append({'exe': f[0], 'home': f[1], 'path': f[2], 'gcg': f[3],
                         'gns': f[4], 'ceil': f[5], 'lc': f[6], 'cwd': f[7]})
        return rows


def classify(rows, hostile_home, hostile_path):
    """Count git children whose environment is NOT the round-30 contract."""
    bad = []
    for r in rows:
        probs = []
        if r['path'] != '/usr/bin:/bin':
            probs.append('PATH=' + r['path'][:120])
        if r['gcg'] != os.devnull:
            probs.append('GIT_CONFIG_GLOBAL=' + r['gcg'])
        if r['gns'] != '1':
            probs.append('GIT_CONFIG_NOSYSTEM=' + r['gns'])
        if r['ceil'] == '-':
            probs.append('no GIT_CEILING_DIRECTORIES')
        if hostile_home and r['home'] == hostile_home:
            probs.append('HOME=hostile')
        if hostile_path and hostile_path in (r['path'] or ''):
            probs.append('PATH carries hostile dir')
        if probs:
            bad.append({'cwd': r['cwd'], 'home': r['home'], 'probs': probs})
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--modes', nargs='*', default=['selftest', 'production'])
    ap.add_argument('--variants', nargs='*', default=['control', 'user-files', 'path-wrapper', 'enclosing'])
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    root = os.path.realpath(tempfile.mkdtemp(prefix='hollow-', dir='/fast/scratch/hyaku/tsukuroi-r30/SentinelProbeHollow'))
    tar = git(dict(os.environ), '-C', lane, 'archive', a.rev).stdout
    tree = os.path.join(root, 'tree')
    os.makedirs(tree)
    with tarfile.open(fileobj=__import__('io').BytesIO(tar)) as t:
        t.extractall(tree, filter='data')
    clean_home = os.path.join(root, 'home-clean')
    clean_tmp = os.path.join(root, 'tmp-clean')
    os.makedirs(os.path.join(clean_home, '.config'))
    os.makedirs(clean_tmp)
    out = open(a.out, 'w')
    for tool, argv in TARGETS:
        if a.only and tool not in a.only and os.path.basename(tool) not in a.only:
            continue
        for mode in a.modes:
            if mode == 'production':
                if tool not in PRODUCTION:
                    continue
                args = [x.format(rev=a.rev, clone=lane) for x in PRODUCTION[tool]]
                ctdir = lane
            else:
                args = [x.format(rev=a.rev, clone=lane) for x in argv]
                ctdir = tree
            runs = {}
            for v in a.variants:
                w = os.path.join(root, f'{os.path.basename(tool)}.{mode}.{v}')
                os.makedirs(w)
                spylog = os.path.join(w, 'children.tsv')
                env = base_env(clean_home, clean_tmp, spylog)
                cwd = ctdir
                rec = {'tool': tool, 'mode': mode, 'variant': v}
                hooklog = os.path.join(w, 'hooks.log')
                if v == 'user-files':
                    hh = os.path.join(w, 'hostile-home')
                    hooks = os.path.join(w, 'hooks')
                    os.makedirs(os.path.join(hh, '.config', 'git'))
                    os.makedirs(hooks)
                    for hk in ('pre-commit', 'post-commit', 'post-checkout'):
                        write_exec(os.path.join(hooks, hk),
                                   '#!/bin/sh\necho "%s $PWD" >> "%s"\nexit 0\n' % (hk, hooklog))
                    cfg = '[core]\n\thooksPath = %s\n' % hooks
                    for f in (os.path.join(hh, '.gitconfig'), os.path.join(hh, '.config', 'git', 'config')):
                        with open(f, 'w') as fh:
                            fh.write(cfg)
                    with open(os.path.join(hh, '.config', 'git', 'ignore'), 'w') as fh:
                        fh.write('*\n')
                    with open(os.path.join(hh, '.config', 'git', 'attributes'), 'w') as fh:
                        fh.write('* -text -diff\n')
                    env.update({'HOME': hh, 'XDG_CONFIG_HOME': os.path.join(hh, '.config')})
                    rec['hostile_home'] = hh
                elif v == 'path-wrapper':
                    wd = os.path.join(w, 'bin')
                    os.makedirs(wd)
                    wrap = os.path.join(wd, 'git')
                    write_exec(wrap, '#!/bin/sh\nprintf "%%s\\n" "$*" >> "%s"\nexec /usr/bin/git "$@"\n' % hooklog)
                    env['PATH'] = wd + os.pathsep + env.get('PATH', os.defpath)
                    rec['hostile_path'] = wd
                elif v == 'enclosing':
                    canary = os.path.join(w, 'encl')
                    make_canary(canary, base_env(clean_home, clean_tmp, os.path.join(w, 'unused.tsv')))
                    cwd = os.path.join(canary, 'tree')
                    shutil.copytree(tree, cwd, symlinks=True)
                    it = os.path.join(canary, 'tmp')
                    os.makedirs(it)
                    env['TMPDIR'] = it
                    rec['fp_before'] = fp(canary, base_env(clean_home, clean_tmp, os.path.join(w, 'unused.tsv')))
                    rec['canary'] = canary
                rc, so, se = run([sys.executable, os.path.join(cwd, tool), *args], cwd, env)
                rec.update({'rc': rc, 'stdout_len': len(so), 'stderr_tail': se.decode('utf-8', 'replace')[-300:]})
                ns = norm(so.decode('utf-8', 'replace'), root)
                rec['stdout_digest'] = dig(ns)
                rows = children(spylog)
                rec['git_children'] = len(rows)
                rec['noncontract_children'] = classify(rows, rec.get('hostile_home'), rec.get('hostile_path'))
                rec['hook_log_lines'] = len(open(hooklog).read().splitlines()) if os.path.exists(hooklog) else 0
                if v == 'enclosing':
                    rec['fp_after'] = fp(canary, base_env(clean_home, clean_tmp, os.path.join(w, 'unused.tsv')))
                    rec['fp_changed'] = rec['fp_after'] != rec['fp_before']
                    del rec['fp_before'], rec['fp_after']
                runs[v] = rec
                out.write(json.dumps(rec) + '\n')
                out.flush()
            ctl = runs.get('control')
            if ctl:
                for v, rec in runs.items():
                    if v == 'control':
                        continue
                    cmp_rows = []
                    if rec['rc'] != ctl['rc']:
                        cmp_rows.append('rc %s vs control %s' % (rec['rc'], ctl['rc']))
                    if rec['stdout_digest'] != ctl['stdout_digest']:
                        cmp_rows.append('stdout differs from control (%d vs %d bytes, %s vs %s)' % (
                            rec['stdout_len'], ctl['stdout_len'], rec['stdout_digest'], ctl['stdout_digest']))
                    if rec['git_children'] != ctl['git_children']:
                        cmp_rows.append('git children %d vs control %d' % (rec['git_children'], ctl['git_children']))
                    if rec['noncontract_children']:
                        cmp_rows.append('%d non-contract git children' % len(rec['noncontract_children']))
                    out.write(json.dumps({'delta': True, 'tool': tool, 'mode': mode, 'variant': v,
                                          'control_git_children': ctl['git_children'],
                                          'notes': cmp_rows}) + '\n')
                    out.flush()
    out.close()
    print(json.dumps({'scratch': root, 'out': a.out}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
