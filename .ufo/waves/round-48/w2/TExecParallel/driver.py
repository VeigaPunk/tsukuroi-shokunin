#!/usr/bin/env python3
"""C1-X11 concurrency probe: N census --selftest runs at once, each under its own
spaced TMPDIR (phase A) or sharing one spaced TMPDIR (phase B).

Fixture location is read from what the harness DID (mktemp wrapper log), as in
tools/score-selftest-tmpdir-r48.py, never from census text.
"""
import json
import os
import re
import subprocess
import sys
import time

S = '/fast/scratch/hyaku/tsukuroi-r48/TExecParallel'
CENSUS = os.path.join(S, 'census.sh')
CASES = 166
WANT = f'TSUKUROI_CENSUS_SELFTEST: PASS ({CASES} cases, {CASES} passed, 0 failed)'
WRAPPER = r'''#!/bin/bash
out=$(/usr/bin/mktemp "$@") || exit $?
case "$*" in
  *tsukuroi-r3-2-selftest*) printf '%s\t%s\t%s\n' "$*" "$out" "$(readlink -f -- "$out")" >>"$MKTEMP_LOG" ;;
esac
printf '%s\n' "$out"
'''


def mk_wrap(name):
    d = os.path.join(S, 'wrap-' + name)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'mktemp')
    with open(p, 'w') as f:
        f.write(WRAPPER)
    os.chmod(p, 0o755)
    return d


def log_rows(path):
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            return [ln.rstrip('\n').split('\t') for ln in f if ln.strip()]
    except FileNotFoundError:
        return []


def last_line(text):
    lines = [ln for ln in text.split('\n') if ln.strip()]
    return lines[-1] if lines else ''


def launch(tag, tmpdir):
    wrap = mk_wrap(tag)
    rd = os.path.join(S, 'run-' + tag)
    os.makedirs(rd, exist_ok=True)
    log = os.path.join(rd, 'mktemp.log')
    out = os.path.join(rd, 'stdout.txt')
    err = os.path.join(rd, 'stderr.txt')
    env = {'PATH': wrap + ':/usr/bin:/bin', 'LC_ALL': 'C', 'MKTEMP_LOG': log,
           'TMPDIR': tmpdir}
    fo = open(out, 'wb')
    fe = open(err, 'wb')
    p = subprocess.Popen(['bash', CENSUS, '--selftest'], env=env, cwd=rd,
                         stdin=subprocess.DEVNULL, stdout=fo, stderr=fe)
    return {'tag': tag, 'tmpdir': tmpdir, 'log': log, 'out': out, 'err': err,
            'proc': p, 'fo': fo, 'fe': fe, 't0': time.time()}


def finish(r):
    try:
        rc = r['proc'].wait(timeout=1800)
    except subprocess.TimeoutExpired:
        r['proc'].kill()
        rc = 'timeout-killed'
    r['fo'].close()
    r['fe'].close()
    r['rc'] = rc
    r['wall_s'] = round(time.time() - r['t0'], 1)
    with open(r['out'], encoding='utf-8', errors='replace') as f:
        text = f.read()
    with open(r['err'], encoding='utf-8', errors='replace') as f:
        errt = f.read()
    rows = log_rows(r['log'])
    parent = None
    tmpl_fd = None
    resolved = None
    if len(rows) == 1 and len(rows[0]) == 3:
        tmpl_fd = (re.search(r'/proc/self/fd/(\d+)', rows[0][0]) or [None, None])[1]
        resolved = rows[0][2]
        parent = os.path.dirname(resolved)
    expect = os.path.realpath(r['tmpdir'])
    r.update({
        'last_line': last_line(text),
        'stderr_tail': errt[-600:],
        'creations': len(rows),
        'template_fd': tmpl_fd,
        'resolved': resolved,
        'real_parent': parent,
        'parent_is_own_tmpdir': parent == expect,
        'fixture_removed': bool(resolved) and not os.path.exists(resolved),
        'pass_ok': rc == 0 and last_line(text) == WANT,
        'rows': rows,
    })
    return r


def phase(label, spec):
    """spec: list of (tag, tmpdir)."""
    print(f'== phase {label}: {len(spec)} concurrent ==', flush=True)
    rs = [launch(t, d) for t, d in spec]
    done = [finish(r) for r in rs]
    return done


def snap_tmp():
    try:
        return sorted(n for n in os.listdir('/tmp') if 'tsukuroi-r3-2-selftest' in n)
    except OSError:
        return []


def main():
    os.makedirs(S, exist_ok=True)
    dirs = {}
    for nm, sub in (('one', 'p one'), ('two', 'p two'), ('three', 'p three')):
        d = os.path.join(S, sub)
        os.makedirs(d, exist_ok=True)
        dirs[nm] = d
    pre_tmp = snap_tmp()
    res = {'frozen_blob_sha256': '375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426',
           'census': CENSUS, 'want': WANT, 'tmp_pre': pre_tmp, 'phases': {}}

    A = phase('A_three_distinct_spaced_tmpdirs',
              [('A1', dirs['one']), ('A2', dirs['two']), ('A3', dirs['three'])])
    for r in A:
        r['tmpdir_contents_after'] = sorted(os.listdir(r['tmpdir']))
    res['phases']['A'] = [{k: v for k, v in r.items() if k not in ('proc', 'fo', 'fe')} for r in A]

    B = phase('B_two_sharing_one_spaced_tmpdir',
              [('B1', dirs['one']), ('B2', dirs['one'])])
    for r in B:
        r['tmpdir_contents_after'] = sorted(os.listdir(dirs['one']))
    res['phases']['B'] = [{k: v for k, v in r.items() if k not in ('proc', 'fo', 'fe')} for r in B]

    res['tmp_post'] = snap_tmp()
    # cross-talk: each run must resolve under its OWN tmpdir, and the two B runs
    # must have distinct resolved fixture paths (no shared/clobbered tree).
    res['B_distinct_resolved'] = (len({r['resolved'] for r in B}) == len(B)
                                  and all(r['resolved'] for r in B))
    res['A_distinct_resolved'] = len({r['resolved'] for r in A}) == len(A)
    res['all_pass'] = all(r['pass_ok'] for r in A + B)
    res['all_one_creation'] = all(r['creations'] == 1 for r in A + B)
    res['all_parent_ok'] = all(r['parent_is_own_tmpdir'] for r in A + B)
    res['all_removed'] = all(r['fixture_removed'] for r in A + B)
    res['all_tmpdirs_empty_after'] = all(not r['tmpdir_contents_after'] for r in A + B)
    res['no_tmp_fixture'] = res['tmp_post'] == pre_tmp == []
    with open(os.path.join(S, 'result.json'), 'w') as f:
        json.dump(res, f, indent=2)
    print(json.dumps({k: res[k] for k in (
        'all_pass', 'all_one_creation', 'all_parent_ok', 'all_removed',
        'all_tmpdirs_empty_after', 'no_tmp_fixture', 'A_distinct_resolved',
        'B_distinct_resolved', 'tmp_pre', 'tmp_post')}, indent=2))
    for ph, rows in res['phases'].items():
        for r in rows:
            print(f"{ph}/{r['tag']} rc={r['rc']} wall={r['wall_s']}s fd={r['template_fd']} "
                  f"creations={r['creations']} parent_ok={r['parent_is_own_tmpdir']} "
                  f"removed={r['fixture_removed']} last={r['last_line'][:80]!r}")
    return 0 if (res['all_pass'] and res['all_one_creation'] and res['all_parent_ok']
                 and res['all_removed'] and res['no_tmp_fixture']) else 1


if __name__ == '__main__':
    sys.exit(main())
