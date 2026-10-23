"""Ordinary-run check (seat MutOneTargetSkipWork): does an ambient name or value reach a git child
of check-btrfs-space-r30 in an ordinary, untraced run? Three byte sets of the one target
(claim base 2641591e, pristine tip 879daa95, mutant f4a10945), each run twice with
ZZ_R34_AMBIENT=1 in the ambient environment:
  run P: plain `python3 <tool> --revision REV --lane CLONE` with a git wrapper first on the
         ambient PATH (the wrapper records argv, the ZZ_R34_AMBIENT line and env names);
  run H: the same command under hookrun.py (sys.addaudithook 'subprocess.Popen', no ptrace),
         which records the exact env mapping handed to each child.
Bounded: every run has a 300 s timeout; the wrapper writes at most 200 files per run.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

SEAT = '/fast/scratch/hyaku/tsukuroi-r34/MutOneTargetSkipWork'
CLONE = SEAT + '/repo'
WRAPBIN = SEAT + '/wrapbin'
ORD = SEAT + '/ordinary'
DUMPS = ORD + '/dumps'
REV = 'f4a10945caf2a8ff49ad260918ba8601f947b3e5'
TOOL = 'tools/check-btrfs-space-r30.py'
BYTES = {'base-2641591e': '2641591e303057cd0f67e190a6bdf7fa91a45c31',
         'tip-879daa95': '879daa95b898b5c624c609eced31f7d0d5b933e8',
         'mutant-f4a10945': REV}
HEX = re.compile(rb'\b[0-9a-f]{64}\b|\b[0-9a-f]{40}\b')   # the probe's stdout normalisation
OUT = sys.argv[1]

genv = {k: v for k, v in os.environ.items() if k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
summary = {'revision_argument': REV, 'lane_argument': CLONE, 'ambient_marker': 'ZZ_R34_AMBIENT=1',
           'runs': {}}
os.makedirs(ORD, exist_ok=True)
for label, commit in BYTES.items():
    d = os.path.join(ORD, 'bytes', label)
    os.makedirs(os.path.join(d, 'tools'), exist_ok=True)
    blob = subprocess.run(['git', '-C', CLONE, 'show', f'{commit}:{TOOL}'], env=genv,
                          capture_output=True, timeout=60, check=True).stdout
    path = os.path.join(d, TOOL)
    with open(path, 'wb') as fh:
        fh.write(blob)
    rec = {'tool_bytes_commit': commit, 'tool_sha256': hashlib.sha256(blob).hexdigest()}
    amb = dict(genv, ZZ_R34_AMBIENT='1')
    # run P: plain run, git wrapper first on the ambient PATH
    shutil.rmtree(DUMPS, ignore_errors=True)
    os.makedirs(DUMPS)
    penv = dict(amb, PATH=WRAPBIN + ':' + genv.get('PATH', '/usr/bin:/bin'))
    p = subprocess.run([sys.executable, path, '--revision', REV, '--lane', CLONE], env=penv,
                       capture_output=True, timeout=300)
    dumps = sorted(os.listdir(DUMPS))
    texts = [open(os.path.join(DUMPS, f), encoding='utf-8', errors='replace').read() for f in dumps]
    rec['plain'] = {
        'rc': p.returncode,
        'stdout_lines': p.stdout.count(b'\n'),
        'normalised_stdout_sha256': hashlib.sha256(HEX.sub(b'<HEX>', p.stdout)).hexdigest(),
        'wrapper_invocations': len(dumps),
        'wrapper_invocations_with_ZZ_R34_AMBIENT_1': sum(1 for t in texts if '\nZZ_R34_AMBIENT=1\n' in t),
        'first_wrapper_record': ([ln if not ln.startswith('names: ') else
                                  'names: <%d names>' % len(ln.split()[1:])
                                  for ln in texts[0].splitlines()] if texts else None),
        'stderr_tail': p.stderr.decode('utf-8', 'replace')[-300:]}
    # run H: audit hook, exact env mapping handed to each child (no wrapper on PATH)
    log = os.path.join(ORD, label + '.hook.json')
    h = subprocess.run([sys.executable, SEAT + '/hookrun.py', log, path, '--revision', REV,
                        '--lane', CLONE], env=amb, capture_output=True, timeout=300)
    hk = json.load(open(log))
    rec['hook'] = {
        'runner_rc': h.returncode, 'tool_rc': hk['rc'], 'tracer': hk['tracer'],
        'normalised_stdout_sha256': hashlib.sha256(HEX.sub(b'<HEX>', h.stdout)).hexdigest(),
        'children': hk['spawns'],
        'children_env_passed': sum(1 for r in hk['records'] if r['env_passed']),
        'children_with_ZZ_R34_AMBIENT_1': sum(1 for r in hk['records'] if r['ZZ_R34_AMBIENT'] == '1'),
        'distinct_child_env_name_sets': sorted(
            {(' '.join(r['names']) if len(r['names']) <= 10 else
              '<%d names, ZZ_R34_AMBIENT %s>' % (len(r['names']),
                                                 'present' if 'ZZ_R34_AMBIENT' in r['names']
                                                 else 'absent'))
             for r in hk['records']}),
        'first_child_argv': hk['records'][0]['argv'] if hk['records'] else None,
        'git_subcommands': sorted({r['argv'][3] if len(r['argv']) > 3 else '?' for r in hk['records']})}
    summary['runs'][label] = rec
shutil.rmtree(DUMPS, ignore_errors=True)
with open(OUT, 'w') as fh:
    json.dump(summary, fh, indent=1)
print(json.dumps(summary, indent=1))
