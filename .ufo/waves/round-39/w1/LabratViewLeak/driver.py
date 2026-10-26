#!/usr/bin/env python3
"""LabratViewLeak driver: run the r39 counter's exact namespace command shape with a channel probe.

Shape copied verbatim from tools/score-storage-hidden-r39.py main():
  inner = 'mount -t tmpfs tsk "$1" && python3 -c "$2" && exec bash "$3" </dev/null'
  subprocess.run([unshare, '-rm', 'sh', '-c', inner, 'r39', target, BUILDER, script],
                 env=env, input=json.dumps(spec), capture_output=True, text=True, timeout=600)
"""
import importlib.util
import json
import os
import pathlib
import random
import shutil
import subprocess

S = pathlib.Path('/fast/scratch/hyaku/tsukuroi-r39/LabratViewLeak')
LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
REC = S / 'receipts'
REC.mkdir(parents=True, exist_ok=True)

mod_spec = importlib.util.spec_from_file_location('c39', LANE / 'tools' / 'score-storage-hidden-r39.py')
m = importlib.util.module_from_spec(mod_spec)
mod_spec.loader.exec_module(m)

WORK = S / 'work'
shutil.rmtree(WORK, ignore_errors=True)
(WORK / 'home').mkdir(parents=True)
(WORK / 'tmp').mkdir(parents=True)
shutil.copy2(S / 'src' / 'census-impl.sh', WORK / 'census.sh')
os.chmod(WORK / 'census.sh', 0o755)

ENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': str(WORK / 'home'), 'TMPDIR': str(WORK / 'tmp')}
INNER = 'mount -t tmpfs tsk "$1" && python3 -c "$2" && exec bash "$3" </dev/null'
PROD = '/sys/fs/btrfs'

view_zero = m.draw_view(random.Random(0xA11CE), 'zero')
view_nonzero = m.draw_view(random.Random(0xB0B), 'nonzero')


def ns(prog, target, spec, tag, timeout=180):
    p = subprocess.run(['unshare', '-rm', 'sh', '-c', INNER, 'r39', target, m.BUILDER, str(prog)],
                       env=ENV, input=json.dumps(spec), capture_output=True, text=True, timeout=timeout)
    (REC / (tag + '.stdout')).write_text(p.stdout)
    (REC / (tag + '.stderr')).write_text(p.stderr)
    return p


def plain(prog, tag):
    p = subprocess.run(['bash', str(prog)], env=ENV, stdin=subprocess.DEVNULL,
                       capture_output=True, text=True, timeout=180)
    (REC / (tag + '.stdout')).write_text(p.stdout)
    (REC / (tag + '.stderr')).write_text(p.stderr)
    return p


summary = []
for tag, target, spec in (('probe-H1-tmpfs-over-prod', PROD, []),
                          ('probe-H2-tmpfs-over-sysfs', '/sys/fs', []),
                          ('probe-view-nonzero', PROD, view_nonzero),
                          ('probe-view-zero', PROD, view_zero)):
    p = ns(S / 'probe.sh', target, spec, tag)
    summary.append({'leg': tag, 'target': target, 'spec_len': len(spec), 'exit': p.returncode})

p = plain(S / 'probe.sh', 'probe-no-namespace')
summary.append({'leg': 'probe-no-namespace', 'exit': p.returncode})

for tag, target, spec in (('census-impl-H1', PROD, []), ('census-impl-H2', '/sys/fs', []),
                          ('census-impl-view-nonzero', PROD, view_nonzero),
                          ('census-impl-view-zero', PROD, view_zero)):
    p = ns(WORK / 'census.sh', target, spec, tag)
    st = [l for l in p.stdout.splitlines() if l.startswith('STORAGE ')]
    six = len([l for l in p.stdout.splitlines() if l.startswith('PLANE ')]) == 6
    summary.append({'leg': tag, 'target': target, 'storage': st, 'six_planes': six, 'exit': p.returncode})

for tag, target, spec in (('cheat-H1', PROD, []), ('cheat-view-nonzero', PROD, view_nonzero)):
    p = ns(S / 'cheat_escape.sh', target, spec, tag)
    summary.append({'leg': tag, 'lines': [l for l in p.stdout.splitlines() if l.startswith('CHEAT')]})

out = {'counter': 'LabratViewLeak-probe',
       'expected_view_nonzero': list(m.model_from_spec(view_nonzero)),
       'expected_view_zero': list(m.model_from_spec(view_zero)),
       'spec_view_nonzero': view_nonzero,
       'legs': summary}
(REC / 'summary.json').write_text(json.dumps(out, indent=1))
print(json.dumps({k: out[k] for k in ('expected_view_nonzero', 'expected_view_zero', 'legs')}, indent=1))
