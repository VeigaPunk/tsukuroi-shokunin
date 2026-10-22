#!/usr/bin/env python3
"""Generate one mutated copy of the frozen C2 probe per mutation, for round-31 mutation testing."""
import hashlib
import json
import os
import shutil
import subprocess

SRC = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/repo/tools/probe-git-child-env-r31.py'
OUT = '/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2/mutants'

PARITY_TUPLE = "    for k in ('rc', 'stdout_sha256', 'git_execs'):"
CARRY = "                carried = [e for e in r['execs'][1:] if any(inject in x for x in e[3])]"
EXTRA = """                extra = {'LD_PRELOAD': os.path.join(inject, 'libprobe-inject.so'),
                         'LD_LIBRARY_PATH': inject, 'PYTHONPATH': inject}"""
EXTRA_NO_LDP = """                extra = {'LD_PRELOAD': os.path.join(inject, 'libprobe-inject.so'),
                         'PYTHONPATH': inject}"""
EXTRA_NO_PY = """                extra = {'LD_PRELOAD': os.path.join(inject, 'libprobe-inject.so'),
                         'LD_LIBRARY_PATH': inject}"""
CTL_B_BLOCK = """        elif parity(ca, cb):
            herr = 'control runs disagree: ' + '; '.join(parity(ca, cb))
"""
NO_GIT_BLOCK = """        elif ca['git_execs'] < 1:
            herr = 'control run started no git child'
"""

MUTANTS = [
    ('M01-drop-parity-check', [(PARITY_TUPLE, "    for k in ():")]),
    ('M02-drop-stdout-comparison', [(PARITY_TUPLE, "    for k in ('rc', 'git_execs'):")]),
    ('M03-drop-git-exec-count', [(PARITY_TUPLE, "    for k in ('rc', 'stdout_sha256'):")]),
    ('M04-skip-first-exec-exclusion',
     [(CARRY, "                carried = [e for e in r['execs'] if any(inject in x for x in e[3])]")]),
    ('M05-injection-by-variable-name',
     [(CARRY, "                carried = [e for e in r['execs'][1:] if any(x.split('=', 1)[0] in ('LD_PRELOAD', 'LD_LIBRARY_PATH', 'PYTHONPATH') for x in e[3])]")]),
    ('M06-no-LD_LIBRARY_PATH-in-injection', [(EXTRA, EXTRA_NO_LDP)]),
    ('M07-no-PYTHONPATH-in-injection', [(EXTRA, EXTRA_NO_PY)]),
    ('M08-drop-control-B-determinism-check', [(CTL_B_BLOCK, "")]),
    ('M09-no-require-git-child', [(NO_GIT_BLOCK, "")]),
    ('M10-supplementary-drop-stdout-and-exec-count',
     [(PARITY_TUPLE, "    for k in ('rc',):")]),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    src = open(SRC, encoding='utf-8').read()
    base_sha = hashlib.sha256(src.encode()).hexdigest()
    manifest = {'source': SRC, 'source_sha256': base_sha, 'mutants': []}
    for name, subs in MUTANTS:
        text = src
        for old, new in subs:
            n = text.count(old)
            if n != 1:
                raise SystemExit('%s: anchor appears %d times: %r' % (name, n, old[:60]))
            text = text.replace(old, new)
        path = os.path.join(OUT, name + '.py')
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(text)
        shutil.copymode(SRC, path)
        # sanity: it must still compile
        c = subprocess.run(['python3', '-m', 'py_compile', path], capture_output=True)
        d = subprocess.run(['diff', '-u', SRC, path], capture_output=True, text=True)
        manifest['mutants'].append({
            'name': name,
            'file': path,
            'sha256': hashlib.sha256(text.encode()).hexdigest(),
            'compiles': c.returncode == 0,
            'compile_stderr': c.stderr.decode()[-200:],
            'diff': d.stdout,
        })
    with open(os.path.join(OUT, 'manifest.json'), 'w') as fh:
        json.dump(manifest, fh, indent=1)
    print(json.dumps({'source_sha256': base_sha,
                      'mutants': [(m['name'], m['sha256'][:12], m['compiles']) for m in manifest['mutants']]},
                     indent=1))


main()
