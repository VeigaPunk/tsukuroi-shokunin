#!/usr/bin/env python3
"""Effect harness: does an ambient variable change what a child of the eleven frozen C2 tools DOES?

Seat SentinelChildEnv, round 31 wave 1. Companion to `probe-ambient-child-env-r31.py` (reach).

For each (tool, variable) pair the harness runs the tool twice under the same strace harness the
frozen probe uses -- once with a CONTROL ambient environment and once with the variable set to a
sentinel -- and reports whether the tool's observable behaviour changed:

  rc_changed            the tool's exit code differs
  stdout_changed        the normalised stdout digest differs
  stderr_changed        the normalised stderr digest differs
  extra_execs           the set of executed programs differs (a new child appeared)
  child_env_var         the variable is present in a descendant execve's environment block
  marker_file_created   the variable's canary had a side effect on disk (BASH_ENV, MALLOC_TRACE)

Nothing here asks a canary to run foreign code: the BASH_ENV canary only appends one line to a
file, the MALLOC_TRACE canary only names a path, and the locale canary only selects a gettext
translation. Usage:
  python3 effects-r31.py --revision <REV> --lane <repo> [--only <tool> ...]
"""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

TOKEN = 'SENTINEL31'

# variable -> (kind, effect-probe)
#   'bashenv'  : a bash startup file; bash sources it for non-interactive shells
#   'locale'   : a gettext translation selection
#   'path'     : a path-valued name with no side effect we can observe without running code
#   'value'    : a scalar with no observable side effect here
EFFECTS = (
    ('BASH_ENV', 'bashenv'),
    ('ENV', 'bashenv'),
    ('GCONV_PATH', 'path'),
    ('MALLOC_TRACE', 'path'),
    ('MALLOC_PERTURB_', 'value'),
    ('MALLOC_CHECK_', 'value'),
    ('GLIBC_TUNABLES', 'value'),
    ('PERL5LIB', 'path'),
    ('PERL5OPT', 'value'),
    ('PERLLIB', 'path'),
    ('EDITOR', 'path'),
    ('VISUAL', 'path'),
    ('PAGER', 'path'),
    ('SSH_ASKPASS', 'path'),
    ('SSH_AUTH_SOCK', 'path'),
    ('TMPDIR', 'path'),
    ('LANG', 'locale'),
    ('LANGUAGE', 'locale'),
    ('LC_ALL', 'locale'),
    ('LC_MESSAGES', 'locale'),
    ('LC_CTYPE', 'locale'),
    ('TZ', 'value'),
    ('HOSTALIASES', 'path'),
    ('RES_OPTIONS', 'value'),
    ('XDG_DATA_HOME', 'path'),
    ('XDG_CACHE_HOME', 'path'),
    ('XDG_RUNTIME_DIR', 'path'),
)


def load_probe(lane):
    path = os.path.join(lane, 'tools', 'probe-git-child-env-r31.py')
    spec = importlib.util.spec_from_file_location('frozen_probe_r31', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_bashenv_canary(root):
    log = os.path.join(root, 'bashenv.log')
    script = os.path.join(root, 'bashenv.canary')
    with open(script, 'w') as fh:
        fh.write('echo "BASHENV-SOURCED pid=$$" >> %s\n' % log)
    return script, log


def run(probe, root, name, tree, tool, args, extra_env):
    work = os.path.join(root, name)
    home = os.path.join(work, 'home')
    tmp = os.path.join(work, 'tmp')
    os.makedirs(os.path.join(home, '.config'))
    os.makedirs(tmp)
    wtree = os.path.join(work, 'tree')
    shutil.copytree(tree, wtree, symlinks=True)
    env = probe.hermetic_env(home, tmp)
    env.pop('LC_ALL', None)        # do not mask an ambient locale
    if extra_env:
        env.update(extra_env)
    trace = os.path.join(root, name + '.trace')
    cmd = [probe.STRACE, '-f', '-qq', '-v', '-s', '65536', '-e', 'trace=execve', '-o', trace,
           '--', sys.executable, os.path.join(wtree, tool), *args]
    try:
        p = subprocess.run(cmd, cwd=wtree, env=env, capture_output=True, timeout=probe.TIMEOUT)
        rc, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        rc, out, err = 'timeout', b'', b''
    execs = probe.parse_trace(trace) if os.path.exists(trace) else []
    out = out.replace(work.encode(), b'<W>').replace(root.encode(), b'<R>')
    err = err.replace(work.encode(), b'<W>').replace(root.encode(), b'<R>')
    out = probe.HEX.sub(b'<HEX>', out)
    err = probe.HEX.sub(b'<HEX>', err)
    shutil.rmtree(wtree, ignore_errors=True)
    return {'rc': rc, 'out': hashlib.sha256(out).hexdigest(), 'err': hashlib.sha256(err).hexdigest(),
            'execs': [e[1] for e in execs], 'envs': [e[3] for e in execs]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', required=True)
    ap.add_argument('--scratch', default=None)
    ap.add_argument('--only', nargs='*', default=None)
    a = ap.parse_args()
    lane = os.path.realpath(a.lane)
    probe = load_probe(lane)
    parent = a.scratch or ('/fast/scratch/hyaku' if os.path.isdir('/fast/scratch/hyaku') else None)
    root = os.path.realpath(tempfile.mkdtemp(prefix='ambient-effects-', dir=parent))
    penv = probe.plumbing_env(root)
    rev = probe.git(penv, '-C', lane, 'rev-parse', '--verify', a.revision + '^{commit}').stdout.decode().strip()
    tree = os.path.join(root, 'tree')
    probe.export_tree(lane, rev, tree, penv)
    clone = os.path.join(root, 'lane.git')
    probe.git(penv, 'clone', '-q', '--bare', '--no-local', lane, clone, timeout=600).check_returncode()
    bashenv, bashenv_log = make_bashenv_canary(root)
    results = []
    for i, (tool, argv) in enumerate(probe.TARGETS):
        if a.only and tool not in a.only and os.path.basename(tool) not in a.only:
            continue
        args = [x.format(rev=rev, clone=clone) for x in argv]
        ctl = run(probe, root, 'ctl-%d' % i, tree, tool, args, None)
        for var, kind in EFFECTS:
            if kind == 'bashenv':
                value = bashenv
                marker = bashenv_log
            elif kind == 'locale':
                value = 'de_DE.UTF-8'
                marker = None
            else:
                d = os.path.join(root, 'canary', var, TOKEN + '_' + var)
                os.makedirs(d, exist_ok=True)
                value = d
                marker = None
            if os.path.exists(bashenv_log):
                os.remove(bashenv_log)
            can = run(probe, root, 'var-%d-%s' % (i, var.replace('_', '-')), tree, tool, args, {var: value})
            child_has = any(('%s=' % var) in e for e in can['envs'][1:])
            marker_hit = bool(marker and os.path.exists(marker))
            row = {'tool': tool, 'variable': var, 'kind': kind,
                   'child_env_var': child_has,
                   'rc_changed': ctl['rc'] != can['rc'],
                   'stdout_changed': ctl['out'] != can['out'],
                   'stderr_changed': ctl['err'] != can['err'],
                   'extra_execs': sorted(set(can['execs']) - set(ctl['execs'])),
                   'marker_file_created': marker_hit,
                   'control_rc': ctl['rc'], 'canary_rc': can['rc']}
            results.append(row)
            print(json.dumps(row, sort_keys=True), flush=True)
    print(json.dumps({'phase': 'effects-summary', 'revision': rev, 'rows': len(results),
                      'rows_detail': results}, sort_keys=True))
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'effects.json')
    with open(outdir, 'w') as fh:
        json.dump({'revision': rev, 'rows': results}, fh, indent=1, sort_keys=True)
    shutil.rmtree(root, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
