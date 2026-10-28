#!/usr/bin/env python3
"""Repeat of phase A (3 concurrent, distinct spaced TMPDIRs) with the behaviour-neutral
diagnostic copy, so the census output of a failing host-read case is captured."""
import json
import os
import re
import subprocess
import sys
import time

S = '/fast/scratch/hyaku/tsukuroi-r48/TExecParallel'
CENSUS = os.path.join(S, 'census-diag.sh')
CASES = 166
WANT = f'TSUKUROI_CENSUS_SELFTEST: PASS ({CASES} cases, {CASES} passed, 0 failed)'


def last_line(t):
    ls = [x for x in t.split('\n') if x.strip()]
    return ls[-1] if ls else ''


WRAPPER = r'''#!/bin/bash
out=$(/usr/bin/mktemp "$@") || exit $?
case "$*" in
  *tsukuroi-r3-2-selftest*) printf '%s\t%s\t%s\n' "$*" "$out" "$(readlink -f -- "$out")" >>"$MKTEMP_LOG" ;;
esac
printf '%s\n' "$out"
'''


def run(tag, sub):
    wrap = os.path.join(S, 'wrap-' + tag)
    os.makedirs(wrap, exist_ok=True)
    with open(os.path.join(wrap, 'mktemp'), 'w') as f:
        f.write(WRAPPER)
    os.chmod(os.path.join(wrap, 'mktemp'), 0o755)
    rd = os.path.join(S, 'run-' + tag)
    os.makedirs(rd, exist_ok=True)
    tmpdir = os.path.join(S, sub)
    os.makedirs(tmpdir, exist_ok=True)
    log = os.path.join(rd, 'mktemp.log')
    env = {'PATH': wrap + ':/usr/bin:/bin', 'LC_ALL': 'C', 'MKTEMP_LOG': log,
           'TMPDIR': tmpdir, 'TSUKUROI_SELFTEST_DIAG': os.path.join(rd, 'diag.txt')}
    fo = open(os.path.join(rd, 'stdout.txt'), 'wb')
    fe = open(os.path.join(rd, 'stderr.txt'), 'wb')
    t0 = time.time()
    p = subprocess.Popen(['bash', CENSUS, '--selftest'], env=env, cwd=rd,
                         stdin=subprocess.DEVNULL, stdout=fo, stderr=fe)
    return tag, tmpdir, log, rd, p, fo, fe, t0


def main():
    rs = [run(t, sub) for t, sub in (('A1c', 'p one'), ('A2c', 'p two'), ('A3c', 'p three'))]
    out = []
    for tag, tmpdir, log, rd, p, fo, fe, t0 in rs:
        rc = p.wait(timeout=1800)
        fo.close()
        fe.close()
        text = open(os.path.join(rd, 'stdout.txt'), encoding='utf-8', errors='replace').read()
        rows = []
        try:
            for ln in open(log, encoding='utf-8', errors='replace'):
                if ln.strip():
                    rows.append(ln.rstrip('\n').split('\t'))
        except FileNotFoundError:
            pass
        resolved = rows[0][2] if len(rows) == 1 and len(rows[0]) == 3 else None
        rec = {
            'tag': tag, 'tmpdir': tmpdir, 'rc': rc, 'wall_s': round(time.time() - t0, 1),
            'last_line': last_line(text), 'pass_ok': rc == 0 and last_line(text) == WANT,
            'creations': len(rows),
            'template_fd': (re.search(r'/proc/self/fd/(\d+)', rows[0][0]) or [None, None])[1] if rows else None,
            'resolved': resolved,
            'parent_is_own_tmpdir': bool(resolved) and os.path.dirname(resolved) == os.path.realpath(tmpdir),
            'fixture_removed': bool(resolved) and not os.path.exists(resolved),
            'tmpdir_after': sorted(os.listdir(tmpdir)),
            'diag_exists': os.path.exists(os.path.join(rd, 'diag.txt')),
            'stderr': open(os.path.join(rd, 'stderr.txt'), encoding='utf-8', errors='replace').read()[-1500:],
        }
        out.append(rec)
    res = {'census_sha256': subprocess.run(['sha256sum', CENSUS], capture_output=True,
                                           text=True).stdout.split()[0],
           'runs': out,
           'all_pass': all(r['pass_ok'] for r in out),
           'all_isolated': all(r['creations'] == 1 and r['parent_is_own_tmpdir']
                               and r['fixture_removed'] and not r['tmpdir_after'] for r in out),
           'distinct_resolved': len({r['resolved'] for r in out}) == len(out)}
    json.dump(res, open(os.path.join(S, 'result-repeat.json'), 'w'), indent=2)
    print(json.dumps({k: v for k, v in res.items() if k != 'runs'}, indent=2))
    for r in out:
        print(f"{r['tag']} rc={r['rc']} wall={r['wall_s']}s fd={r['template_fd']} "
              f"creations={r['creations']} parent_ok={r['parent_is_own_tmpdir']} "
              f"removed={r['fixture_removed']} diag={r['diag_exists']} last={r['last_line'][:70]!r}")
        if r['stderr'].strip():
            print('  STDERR:', r['stderr'].strip().replace('\n', ' | ')[:400])
    return 0


if __name__ == '__main__':
    sys.exit(main())
