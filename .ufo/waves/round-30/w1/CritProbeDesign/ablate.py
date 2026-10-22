#!/usr/bin/env python3
"""CritProbeDesign ablation harness (round 30, wave 1).

Runs chosen probe targets under the probe's control environment and under each ingredient of the
probe's user-files channel separately (hooks path, ignore '*', attributes, identity), with a git
wrapper first on PATH that logs `rc<TAB>cwd<TAB>argv` for every git call (in every variant,
control included, so PATH is identical across variants and only HOME content differs).
Prints, per (tool, variant), the tool exit code and the first git call whose rc differs from the
control's call at the same position.

Usage: ablate.py --tree <export> --clone <bare clone> --rev <sha> --out <dir> TOOL...
"""
import argparse, json, os, shutil, stat, subprocess, sys, tempfile

SYSTEM_GIT = '/usr/bin/git'
ARGV = {
    'tools/mutants-adjacency-overlap.py': ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}'],
    'tools/mutants-kernel-taint.py': ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}'],
    'tools/mutants-owed-statements-r29.py':
        ['--base', '81a061a67466c5e1be812814a895a4b5ed89b4ff', '--counter-rev', '{rev}', '--lane', '{clone}'],
    'tools/mutants-owed-statements-r29-landed.py': ['--base', '{rev}', '--counter-rev', '{rev}', '--lane', '{clone}'],
}
VARIANTS = ('control', 'full', 'hooks', 'ignore', 'attrs', 'identity', 'ignore+identity')


def wexec(p, body):
    with open(p, 'w') as fh:
        fh.write(body)
    os.chmod(p, os.stat(p).st_mode | stat.S_IXUSR)


def build_home(work, variant, hooklog):
    home = os.path.join(work, 'home')
    gdir = os.path.join(home, '.config', 'git')
    os.makedirs(gdir)
    cfg = ''
    if variant in ('full', 'hooks'):
        hooks = os.path.join(work, 'hooks')
        os.makedirs(hooks)
        for h in ('pre-commit', 'post-commit', 'post-checkout'):
            wexec(os.path.join(hooks, h), '#!/bin/sh\necho "%s $PWD" >> "%s"\nexit 0\n' % (h, hooklog))
        cfg += '[core]\n\thooksPath = %s\n' % hooks
    if 'identity' in variant:
        cfg += '[user]\n\tname = canary\n\temail = canary@invalid\n'
    if cfg:
        for f in (os.path.join(home, '.gitconfig'), os.path.join(gdir, 'config')):
            with open(f, 'w') as fh:
                fh.write(cfg)
    if variant in ('full', 'ignore', 'ignore+identity'):
        with open(os.path.join(gdir, 'ignore'), 'w') as fh:
            fh.write('*\n')
    if variant in ('full', 'attrs'):
        with open(os.path.join(gdir, 'attributes'), 'w') as fh:
            fh.write('* -text -diff\n')
    return home


def read_calls(log):
    if not os.path.exists(log):
        return []
    out = []
    with open(log, errors='replace') as fh:
        for line in fh:
            rc, cwd, argv = line.rstrip('\n').split('\t', 2)
            out.append((int(rc), cwd, argv))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tree', required=True)
    ap.add_argument('--clone', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--variants', nargs='*', default=list(VARIANTS))
    ap.add_argument('tools', nargs='+')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    root = tempfile.mkdtemp(prefix='ablate-', dir=a.out)
    for tool in a.tools:
        args = [x.format(rev=a.rev, clone=a.clone) for x in ARGV.get(tool, ['--selftest'])]
        ctl_calls = None
        for v in a.variants:
            work = os.path.join(root, os.path.basename(tool) + '-' + v.replace('+', '_'))
            os.makedirs(work)
            tmp = os.path.join(work, 'tmp')
            os.makedirs(tmp)
            bindir = os.path.join(work, 'bin')
            os.makedirs(bindir)
            gitlog = os.path.join(work, 'git-calls.log')
            hooklog = os.path.join(work, 'hooks.log')
            wexec(os.path.join(bindir, 'git'),
                  '#!/bin/sh\n"%s" "$@"\nrc=$?\nprintf "%%s\\t%%s\\t%%s\\n" "$rc" "$PWD" "$*" >> "%s"\nexit $rc\n'
                  % (SYSTEM_GIT, gitlog))
            home = build_home(work, v, hooklog)
            env = {k: val for k, val in os.environ.items() if not k.startswith('GIT_')}
            env.update({'GIT_CONFIG_NOSYSTEM': '1', 'LC_ALL': 'C', 'HOME': home,
                        'XDG_CONFIG_HOME': os.path.join(home, '.config'), 'TMPDIR': tmp,
                        'PATH': bindir + os.pathsep + env.get('PATH', os.defpath)})
            r = subprocess.run([sys.executable, os.path.join(a.tree, tool), *args], cwd=a.tree, env=env,
                               capture_output=True, timeout=900)
            with open(os.path.join(work, 'stdout'), 'wb') as fh:
                fh.write(r.stdout)
            with open(os.path.join(work, 'stderr'), 'wb') as fh:
                fh.write(r.stderr)
            calls = read_calls(gitlog)
            res = {'tool': tool, 'variant': v, 'rc': r.returncode, 'git_calls': len(calls),
                   'nonzero_git': sum(1 for c in calls if c[0] != 0),
                   'hook_lines': len(open(hooklog).read().splitlines()) if os.path.exists(hooklog) else 0,
                   'work': work}
            if v == 'control':
                ctl_calls = calls
            elif ctl_calls is not None:
                for i, c in enumerate(calls):
                    base = ctl_calls[i] if i < len(ctl_calls) else None
                    if base is None or c[0] != base[0]:
                        res['first_divergent_call'] = {'index': i, 'rc': c[0], 'argv': c[2], 'cwd': c[1],
                                                       'control_rc_same_index': base[0] if base else None,
                                                       'control_argv_same_index': base[2] if base else None}
                        break
                res['stdout_equal_control'] = r.stdout == open(
                    os.path.join(os.path.dirname(work), os.path.basename(tool) + '-control', 'stdout'), 'rb').read()
            res['stderr_tail'] = r.stderr.decode('utf-8', 'replace')[-400:]
            print(json.dumps(res), flush=True)


if __name__ == '__main__':
    main()
