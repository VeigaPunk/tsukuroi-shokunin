#!/usr/bin/env python3
"""Live-mode git-alias/untraced detector for tools/measure-update-recheck.py.

Reuses the frozen r36 probe's injection builder, hermetic env and untraced
predicate helpers (imported by path). PATH shims (git/python3/bash/sh) record
their own argv plus /proc/self/environ before exec'ing the real /usr/bin binary,
then the tool runs in LIVE mode (--revision <rev> --branch master) inside a real
repository with the shim directory first on PATH.
"""
import hashlib
import importlib.util
import json
import os
import random
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
PROBE = os.path.join(LANE, 'tools/probe-child-env-allowlist-r36.py')
spec = importlib.util.spec_from_file_location('probe_r36', PROBE)
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)

S, PRISTINE, MUTANT_CLONE, REV = sys.argv[1:5]
root = os.path.join(S, 'live2')
os.makedirs(root, exist_ok=True)
home = os.path.join(root, 'home')
tmp = os.path.join(root, 'tmp')
os.makedirs(os.path.join(home, '.config'), exist_ok=True)
os.makedirs(tmp, exist_ok=True)
inject = os.path.join(root, 'inject-' + P.rand_label('i'))
os.makedirs(inject)
rng = random.Random(int.from_bytes(os.urandom(32), 'big'))
taken = set(os.environ) | set(P.hermetic_env('/h', '/t')) | set(P.NAMED_INJECTED)
extra, names = P.build_injection(rng, inject, taken, named=True)
wrapper_dir = os.path.join(inject, P.rand_label('w'))
os.makedirs(wrapper_dir)
log = os.path.join(inject, 'untraced.jsonl')
BODY = """#!/usr/bin/python3
import json, os, sys
name = os.path.basename(sys.argv[0])
raw = open('/proc/self/environ', 'rb').read()
envp = [i.decode('utf-8', 'replace') for i in raw.split(b'\\0') if i]
rec = {'wrapper': name, 'argv': sys.argv[1:], 'env': envp}
with open(%r, 'a') as fh:
    fh.write(json.dumps(rec) + '\\n')
real = '/usr/bin/' + name
os.execv(real, [real] + sys.argv[1:])
""" % log
for name in ('git', 'python3', 'bash', 'sh'):
    path = os.path.join(wrapper_dir, name)
    with open(path, 'w') as fh:
        fh.write(BODY)
    os.chmod(path, 0o755)
extra['PATH'] = wrapper_dir + ':/usr/bin:/bin'
env = P.hermetic_env(home, tmp)
env.update(extra)
tokens = {inject, env.get('HOME'), env.get('XDG_CONFIG_HOME')}
tokens |= {extra[n] for n in ('LANG', 'TZ', 'TERM', 'USER', 'LOGNAME', 'SHELL')}
tokens |= {extra[n] for n in names}
tokens = {t for t in tokens if t}
out = {'inject': inject, 'wrapper_dir': wrapper_dir,
       'value_channel': {n: env[n] for n in P.VALUE_NAMES if n in env},
       'injected_names': names, 'runs': {}}
for label, clone in (('pristine', PRISTINE), ('mutant', MUTANT_CLONE)):
    open(log, 'w').close()
    tool = os.path.join(clone, 'tools/measure-update-recheck.py')
    argv = [sys.executable, tool, '--revision', REV, '--branch', 'master']
    proc = subprocess.run(argv, cwd=clone, env=env, capture_output=True, timeout=300)
    records = []
    for line in open(log):
        rec = json.loads(line)
        records.append((rec['wrapper'], rec['env'], rec['argv']))
    reached, vreached, areached = P.untraced_carriers(
        [(w, e) for w, e, _a in records], list(P.NAMED_INJECTED) + list(names), env,
        tokens, {env.get('TMPDIR')})
    shown = []
    for wrapper, envp, argv_tail in records[:20]:
        d = {}
        keep = ('PATH', 'BASH_ENV', 'ENV', 'GCONV_PATH', 'PERL5OPT', 'LANG', 'TZ', 'TERM',
                'USER', 'LOGNAME', 'SHELL', 'HOME', 'TMPDIR', 'GIT_CONFIG_NOSYSTEM',
                'GIT_CONFIG_GLOBAL') + tuple(names)
        for item in envp:
            n, sep, v = item.partition('=')
            if sep and n in keep:
                d[n] = v
        shown.append({'wrapper': wrapper, 'argv': argv_tail, 'env': d,
                      'ambient_name_count': len(envp)})
    out['runs'][label] = {
        'tool_sha256': hashlib.sha256(open(tool, 'rb').read()).hexdigest(),
        'argv': argv, 'cwd': clone, 'rc': proc.returncode,
        'stdout_sha256': hashlib.sha256(proc.stdout).hexdigest(),
        'stdout_tail': proc.stdout.decode('utf-8', 'replace').strip()[-400:],
        'stderr_tail': proc.stderr.decode('utf-8', 'replace').strip()[-300:],
        'wrapper_record_count': len(records),
        'wrapper_argv_multiset': sorted(
            [w + ' ' + ' '.join(a[:6]) for w, _e, a in records])[:30],
        'reached_injected_names': reached,
        'values_reached': vreached,
        'anyname_values_reached': areached,
        'record_env_samples': shown,
        'leak_probe_predicate': bool(reached or vreached or areached),
    }
print(json.dumps(out, sort_keys=True))
