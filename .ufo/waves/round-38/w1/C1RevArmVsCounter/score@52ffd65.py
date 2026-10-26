#!/usr/bin/env python3
"""Round-38 C1 counter (coverage): does the census at <REV> read the storage-integrity surface?

Frozen before any seat scored (round-38 declaration, SCORECARD.md "Round 38 — declaration").
Predicate, the same sentence in the plan, this code and the receipt label:

    fixtures_matched == FIXTURES_EXPECTED and live_match == 1 and six_planes_all == 1  -> PASS, exit 0

The census bytes are read through git at the bound revision (`git show <REV>:tools/tsukuroi-census.sh`)
into a scratch directory and run with `bash`; no working-tree byte of the measured revision is used.
For each fixture the counter builds a fake btrfs sysfs tree under the scratch root, runs the census
with TSUKUROI_BTRFS_SYSFS=<tree>, and reads exactly one line of the frozen grammar

    STORAGE btrfs-device-stats state=<HEALTHY|DEGRADED|BLOCKED> filesystems=<n> devices=<n> nonzero=<n>[ ...]

A fixture matches when exactly one such line is printed and its state, filesystems, devices and
nonzero fields equal the fixture's expected values. `nonzero` is the number of (device, counter) pairs
whose value is greater than zero. Verdict rules the fixtures encode (sourced on SH1/SH2 of
corpus/knowledge/storage-health-r26.md, S128/S133): a btrfs sysfs root that does not exist means no
btrfs filesystem is mounted (HEALTHY, 0/0/0); a filesystem directory (UUID-named) without readable
devinfo/<devid>/error_stats, or an error_stats file that does not carry exactly the five known
counters as non-negative integers, is BLOCKED; any counter above zero is DEGRADED (a lifetime total,
never a dated event); otherwise HEALTHY. Non-UUID entries (`features`) are ignored.

live_match: the census at REV run against the real /sys/fs/btrfs prints a STORAGE line whose four
fields equal what this counter computes from the same sysfs files read directly.
six_planes_all: every run (fixtures and live) prints exactly six `PLANE ` lines and one
`TSUKUROI_CENSUS:` line — the storage arm is verdict-neutral and adds no plane to the rollup.

Exit: 0 PASS; 1 FAIL (predicate false); 2 could-not-evaluate (revision binding, git, bash missing).
Scratch: --scratch DIR (default: a mkdtemp under $TMPDIR); removed on exit. Read-only on the host.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _revision  # noqa: E402

COUNTER_ID = 'score-storage-arm-r38'
CENSUS = 'tools/tsukuroi-census.sh'
LIVE_SYSFS = '/sys/fs/btrfs'
KEYS = ('write_errs', 'read_errs', 'flush_errs', 'corruption_errs', 'generation_errs')
UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
LINE_RE = re.compile(
    r'^STORAGE btrfs-device-stats state=(HEALTHY|DEGRADED|BLOCKED) '
    r'filesystems=(\d+) devices=(\d+) nonzero=(\d+)(?: .*)?$')
U1 = '11111111-2222-3333-4444-555555555555'
U2 = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'
CHILD_ENV_BASE = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'}


def stats(**over):
    vals = {k: 0 for k in KEYS}
    vals.update(over)
    return ''.join('%s %s\n' % (k, vals[k]) for k in KEYS)


ZERO = stats()
# name -> (tree spec, expected (state, filesystems, devices, nonzero))
# tree spec: list of (relative path, content | None for a directory, mode or None)
FIXTURES = {
    'F01-zero-one-device': ([(f'{U1}/devinfo/1/error_stats', ZERO, None)], ('HEALTHY', 1, 1, 0)),
    'F02-two-counters-nonzero': ([(f'{U1}/devinfo/1/error_stats', stats(corruption_errs=3, write_errs=1), None)],
                                 ('DEGRADED', 1, 1, 2)),
    'F03-second-device-nonzero': ([(f'{U1}/devinfo/1/error_stats', ZERO, None),
                                   (f'{U1}/devinfo/2/error_stats', stats(read_errs=1), None)],
                                  ('DEGRADED', 1, 2, 1)),
    'F04-missing-counter': ([(f'{U1}/devinfo/1/error_stats',
                              ''.join('%s 0\n' % k for k in KEYS[:4]), None)], ('BLOCKED', 1, 1, 0)),
    'F05-non-integer': ([(f'{U1}/devinfo/1/error_stats', ZERO.replace('read_errs 0', 'read_errs x'), None)],
                        ('BLOCKED', 1, 1, 0)),
    'F06-no-btrfs-root': ([], ('HEALTHY', 0, 0, 0)),
    'F07-fs-without-devinfo': ([(f'{U1}/features', None, None)], ('BLOCKED', 1, 0, 0)),
    'F08-zero-with-noise': ([('features/free_space_tree', 'live\n', None),
                             ('not-a-uuid', 'x\n', None),
                             (f'{U1}/devinfo/1/error_stats', ZERO, None)], ('HEALTHY', 1, 1, 0)),
    'F09-second-fs-nonzero': ([(f'{U1}/devinfo/1/error_stats', ZERO, None),
                               (f'{U2}/devinfo/1/error_stats', stats(generation_errs=7), None)],
                              ('DEGRADED', 2, 2, 1)),
    'F10-unreadable-stats': ([(f'{U1}/devinfo/1/error_stats', ZERO, 0o000)], ('BLOCKED', 1, 1, 0)),
}
FIXTURES_EXPECTED = len(FIXTURES)


def build(root: Path, spec) -> Path:
    tree = root / 'sys-fs-btrfs'
    if not spec:
        return tree  # F06: the root itself does not exist
    tree.mkdir(parents=True)
    for rel, content, mode in spec:
        p = tree / rel
        if content is None:
            p.mkdir(parents=True, exist_ok=True)
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        if mode is not None:
            os.chmod(p, mode)
    return tree


def expected_from_sysfs(root: str):
    """Independent reading of a btrfs sysfs root under the frozen rules."""
    if not os.path.isdir(root):
        return ('HEALTHY', 0, 0, 0)
    state, fss, devs, nonzero = 'HEALTHY', 0, 0, 0
    blocked = False
    for name in sorted(os.listdir(root)):
        if not UUID_RE.match(name):
            continue
        fss += 1
        devinfo = os.path.join(root, name, 'devinfo')
        ids = sorted(os.listdir(devinfo)) if os.path.isdir(devinfo) else []
        if not ids:
            blocked = True
            continue
        for d in ids:
            devs += 1
            f = os.path.join(devinfo, d, 'error_stats')
            try:
                text = open(f).read()
            except OSError:
                blocked = True
                continue
            seen = {}
            ok = True
            for line in text.splitlines():
                parts = line.split()
                if len(parts) != 2 or parts[0] not in KEYS or parts[0] in seen or not parts[1].isdigit():
                    ok = False
                    break
                seen[parts[0]] = int(parts[1])
            if not ok or set(seen) != set(KEYS):
                blocked = True
                continue
            nonzero += sum(1 for v in seen.values() if v > 0)
    if blocked:
        state = 'BLOCKED'
    elif nonzero:
        state = 'DEGRADED'
    return (state, fss, devs, nonzero)


def run_census(script: Path, sysfs: str | None, scratch: Path):
    env = dict(CHILD_ENV_BASE)
    env['HOME'] = str(scratch / 'home')
    env['TMPDIR'] = str(scratch / 'tmp')
    if sysfs is not None:
        env['TSUKUROI_BTRFS_SYSFS'] = sysfs
    p = subprocess.run(['bash', str(script)], env=env, capture_output=True, text=True, timeout=300)
    return p.returncode, p.stdout, p.stderr


def parse(stdout: str):
    lines = [l for l in stdout.splitlines() if l.startswith('STORAGE ')]
    planes = [l for l in stdout.splitlines() if l.startswith('PLANE ')]
    rollups = [l for l in stdout.splitlines() if l.startswith('TSUKUROI_CENSUS:')]
    got = None
    if len(lines) == 1:
        m = LINE_RE.match(lines[0])
        if m:
            got = (m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)))
    return got, lines, len(planes) == 6 and len(rollups) == 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--repo', default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument('--revision', required=True)
    ap.add_argument('--branch', default='master')
    ap.add_argument('--scratch', default=None)
    ap.add_argument('--no-live', action='store_true', help='skip the live leg (predicate then cannot PASS)')
    a = ap.parse_args(argv)
    try:
        b = _revision.bind(a.repo, a.revision, a.branch)
    except _revision.RevisionError as e:
        print(json.dumps({'counter': COUNTER_ID, 'error': str(e), 'exit': 2}))
        return 2
    if shutil.which('bash', path=CHILD_ENV_BASE['PATH']) is None:
        print(json.dumps({'counter': COUNTER_ID, 'error': 'bash not found', 'exit': 2}))
        return 2
    base = Path(a.scratch) if a.scratch else Path(tempfile.mkdtemp(prefix='tsk-r38-c1-'))
    base.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix='run-', dir=str(base)))
    try:
        (work / 'home').mkdir()
        (work / 'tmp').mkdir()
        show = subprocess.run(['git', '-C', a.repo, 'show', f'{b.sha}:{CENSUS}'], env=_revision.clean_env(),
                              capture_output=True, timeout=60)
        if show.returncode != 0:
            print(json.dumps({'counter': COUNTER_ID, 'error': 'git show failed: ' + show.stderr.decode()[-300:], 'exit': 2}))
            return 2
        script = work / 'tsukuroi-census.sh'
        script.write_bytes(show.stdout)
        root_user = os.geteuid() == 0
        results, matched, six_all = [], 0, True
        for name, (spec, exp) in FIXTURES.items():
            fx = work / 'fx' / name
            fx.mkdir(parents=True)
            tree = build(fx, spec)
            rc, out, err = run_census(script, str(tree), work)
            got, lines, six = parse(out)
            six_all = six_all and six
            ok = got == exp
            if name == 'F10-unreadable-stats' and root_user:
                ok = False  # root reads mode-000 files; the case cannot discriminate and is not credited
            matched += 1 if ok else 0
            results.append({'fixture': name, 'expected': list(exp), 'got': list(got) if got else None,
                            'storage_lines': lines, 'six_planes': six, 'census_exit': rc, 'match': ok})
        live = {'skipped': True}
        live_match = 0
        if not a.no_live:
            exp = expected_from_sysfs(LIVE_SYSFS)
            rc, out, err = run_census(script, None, work)
            got, lines, six = parse(out)
            six_all = six_all and six
            live_match = 1 if got == exp else 0
            live = {'expected': list(exp), 'got': list(got) if got else None, 'storage_lines': lines,
                    'six_planes': six, 'census_exit': rc, 'match': bool(live_match)}
        verdict = matched == FIXTURES_EXPECTED and live_match == 1 and six_all
        rec = {'counter': COUNTER_ID, 'revision': b.sha, 'branch_tip': b.branch_tip,
               'predicate': 'fixtures_matched == FIXTURES_EXPECTED and live_match == 1 and six_planes_all == 1',
               'fixtures_expected': FIXTURES_EXPECTED, 'fixtures_matched': matched,
               'live_match': live_match, 'six_planes_all': int(six_all), 'euid_root': root_user,
               'result': 'PASS' if verdict else 'FAIL', 'exit': 0 if verdict else 1,
               'fixtures': results, 'live': live}
        print(json.dumps(rec, indent=1))
        return rec['exit']
    finally:
        for p in work.rglob('*'):
            try:
                if not p.is_symlink():
                    os.chmod(p, stat.S_IRWXU)
            except OSError:
                pass
        shutil.rmtree(work, ignore_errors=True)
        if not a.scratch:
            shutil.rmtree(base, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
