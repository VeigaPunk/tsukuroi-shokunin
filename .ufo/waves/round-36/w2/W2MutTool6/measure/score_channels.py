"""Score mutant m6 with the frozen probe's own measurement machinery.

The frozen CLI (tools/probe-child-env-allowlist-r36.py, VERSION 7, sha256 a2a5acac...)
exports its target tree with `git archive <rev>` and clones `--lane`; a mutation that
exists only in a sandbox working tree is therefore invisible to it (proved by
raw/literal-cli-mutant-worktree.jsonl: leaking 0, byte-identical verdict to pristine).
Creating the mutant commit/ref is reserved to the L1 (seat bounds: no git add/commit,
no ref mutation). This runner instead builds the livefive tree, overlays the mutated
file on the filesystem, and calls the probe module's own `build_injection`, `one_run`,
`carriers`, `value_carriers`, `anyname_carriers` -- the exact code paths of the
`names`/`quiet` channels -- plus an ordinary strace check for the ambient marker.

No git mutation: `git archive` and `git clone --bare` are reads.
"""
import hashlib
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys
import tarfile
import tempfile

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
SANDBOX = '/tmp/m6w/sandbox'
PRISTINE = '/tmp/m6w/backup/check-report-receipts.pristine.py'
MUTANT = '/tmp/m6w/sandbox/tools/check-report-receipts.py'
REV = 'c052bb7d41ced49aa888817069afd804eccfecf1'
PROBE = os.path.join(LANE, 'tools', 'probe-child-env-allowlist-r36.py')
TOOL = 'tools/check-report-receipts.py'
EXPECTED_PROBE_SHA = 'a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a'

spec = importlib.util.spec_from_file_location('frozen_probe_r36', PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
assert probe.VERSION == 7, probe.VERSION
with open(PROBE, 'rb') as fh:
    probe_sha = hashlib.sha256(fh.read()).hexdigest()
assert probe_sha == EXPECTED_PROBE_SHA, probe_sha

root = tempfile.mkdtemp(prefix='m6-chan-')
penv = probe.plumbing_env(root)


def archive_tree(dest):
    tar = subprocess.run(['/usr/bin/git', '-C', SANDBOX, 'archive', REV],
                         env=penv, capture_output=True, check=True).stdout
    os.makedirs(dest)
    with tarfile.open(fileobj=__import__('io').BytesIO(tar)) as t:
        t.extractall(dest, filter='data')
    probe.write_livefive_report(dest)


def make_tree(kind):
    dest = os.path.join(root, 'tree-' + kind)
    archive_tree(dest)
    src = MUTANT if kind == 'mutant' else PRISTINE
    shutil.copyfile(src, os.path.join(dest, TOOL))
    with open(os.path.join(dest, TOOL), 'rb') as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    return dest, sha


clone = os.path.join(root, 'lane.git')
subprocess.run(['/usr/bin/git', 'clone', '-q', '--bare', '--no-local', SANDBOX, clone],
               env=penv, check=True, timeout=600)
argv = [x.format(rev=REV, clone=clone) for x in
        dict(probe.LIVE_FIVE_TARGETS)[TOOL]]


def channel(tree, named):
    inject = os.path.join(root, probe.rand_label('i'))
    rng = random.Random(int.from_bytes(os.urandom(32), 'big'))
    taken = set(os.environ) | set(probe.hermetic_env('/h', '/t')) | set(probe.NAMED_INJECTED)
    extra, rnames = probe.build_injection(rng, inject, taken, named=named)
    r = probe.one_run(root, tree, TOOL, argv, extra_env=extra)
    names = (list(probe.NAMED_INJECTED) if named else []) + list(rnames)
    tokens = {inject, r['env'].get('HOME'), r['env'].get('XDG_CONFIG_HOME')}
    tokens |= {extra[n] for n in ('LANG', 'TZ', 'TERM', 'USER', 'LOGNAME', 'SHELL')}
    tokens |= {extra[n] for n in rnames}
    reached = probe.carriers(r['execs'], names)
    vreached = probe.value_carriers(r['execs'], r['env'])
    areached = probe.anyname_carriers(r['execs'], {t for t in tokens if t},
                                      {r['env'].get('TMPDIR')},
                                      home=r['env'].get('HOME'))
    child_paths = []
    for _pid, fname, _av, envp in r['execs'][1:]:
        for item in envp:
            if item.startswith('PATH='):
                child_paths.append({'exe': fname, 'PATH': item})
    return {
        'channel': 'names' if named else 'quiet',
        'rc': r['rc'],
        'child_execs': r['child_execs'],
        'git_execs': r['git_execs'],
        'git_missing_kept': r['git_missing_kept'],
        'ambient_PATH': r['env'].get('PATH'),
        'reached': reached,
        'value_channel_reached': vreached,
        'anyname_reached': sorted({n for n, _f in areached}),
        'child_PATH_records': child_paths,
        'leak': bool(reached or vreached or areached or r['execveat'] or r['unparsed']),
    }


def ordinal(kind):
    """Ordinary run: ambient marker + custom PATH, probe parse_trace, no injection dirs."""
    tree = os.path.join(root, 'ord-' + kind)
    archive_tree(tree)
    src = MUTANT if kind == 'mutant' else PRISTINE
    shutil.copyfile(src, os.path.join(tree, TOOL))
    home = os.path.join(root, 'ordhome-' + kind)
    tmp = os.path.join(root, 'ordtmp-' + kind)
    os.makedirs(os.path.join(home, '.config'))
    os.makedirs(tmp)
    env = probe.hermetic_env(home, tmp)
    sentinel = '%s/ambient-bin' % root
    os.makedirs(sentinel, exist_ok=True)
    marker = 'R36LEAKMARK=leak-%d' % os.getpid()
    env['PATH'] = '/usr/bin:/bin:' + sentinel
    env['R36LEAKMARK'] = 'leak-%d' % os.getpid()
    trace = os.path.join(root, 'ord-%s.trace' % kind)
    cmd = [probe.STRACE, '-f', '-qq', '-v', '-s', '65536', '-e', 'trace=execve,execveat',
           '-o', trace, '--', sys.executable, os.path.join(tree, TOOL), *argv]
    p = subprocess.run(cmd, cwd=tree, env=env, capture_output=True, timeout=probe.TIMEOUT)
    execs, unparsed, execveat = probe.parse_trace(trace)
    rows = []
    for _pid, fname, av, envp in execs[1:]:
        rows.append({
            'exe': fname,
            'argv0_2': av[:2],
            'marker_present': marker in envp or any(i.startswith('R36LEAKMARK=') for i in envp),
            'PATH': [i for i in envp if i.startswith('PATH=')],
        })
    return {'rc': p.returncode, 'children': len(execs) - 1,
            'marker': marker, 'unparsed': unparsed, 'execveat': execveat,
            'children_env': rows,
            'marker_leaks': sum(1 for r in rows if r['marker_present']),
            'nonfixed_PATH': sum(1 for r in rows if any(x != 'PATH=/usr/bin:/bin'
                                                       for x in r['PATH']))}


out = {'probe_sha256': probe_sha, 'probe_version': probe.VERSION, 'revision': REV,
       'argv': argv, 'root': root, 'trees': {}, 'channels': {}, 'ordinary': {}}
for kind in ('pristine', 'mutant'):
    tree, sha = make_tree(kind)
    out['trees'][kind] = {'path': tree, 'tool_sha256': sha}
    out['channels'][kind] = [channel(tree, True), channel(tree, False)]
    out['ordinary'][kind] = ordinal(kind)
print(json.dumps(out, indent=1))
