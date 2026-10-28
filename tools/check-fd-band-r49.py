#!/usr/bin/env python3
"""Round-49 C3 counter (frozen before any seat of round 49): the census selftest names
descriptor-band exhaustion instead of failing silently, and its stale /tmp comment is gone.

Surface moved: `tools/tsukuroi-census.sh` `selftest_base_dir` / `run_selftest`, the alias
resolver that round 48 introduced (a TMPDIR the root-override locator refuses is reached
through a /proc/self/fd alias inside that TMPDIR, never /tmp). At base it retried the fixed
240-249 band and returned 1 with no diagnostic when every descriptor was already open, and
its admin comment still claimed the fixture tree is built under /tmp. Now the resolver
records a failure class (ST_BASE_ERR) and the selftest prints a named `fd band ... exhausted`
diagnostic for the exhausted-band case, and one new selftest case (R49-C3) proves it.

Legs (counted):
  stale_ok   the literal stale comment `builds a /tmp fixture tree` is absent from the script
  diag_ok    the script carries the failure class assignment `ST_BASE_ERR=fd-band`, the
             printed diagnostic `fd band %s exhausted`, and >=2 occurrences of `fd band`
             (code path + usage text)
  band_ok    `bash <census> --selftest` at REV exits 0, its last line is PASS with 0 failed,
             includes at least the 167 cases present at the round-49 freeze, and the
             R49-C3 case line is a PASS line (later independent cases may increase the total)
  cases      the case count parsed from that last line (minimum 167 = 166 + R49-C3)

Predicate: stale_ok == 1 and diag_ok == 1 and band_ok == 1 and cases >= 167

Scratch: the selftest tree lives under --work (default $HYAKU_SCRATCH/tsukuroi-r49/counter-c3,
HYAKU_SCRATCH default /fast/scratch/hyaku); the counter removes its work dir on exit and
never writes under /tmp itself.
Usage: python3 tools/check-fd-band-r49.py --revision <REV> [--work DIR] [--census-file FILE]
Writes nothing outside --work. Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read error.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

BASE = '6256760d1382ce4ce20fcba830d4b2912cfbf12b'
CENSUS = 'tools/tsukuroi-census.sh'
TARGET_CASES = 167
STALE = 'builds a /tmp fixture tree'
DIAG_CODE = 'ST_BASE_ERR=fd-band'
DIAG_TEXT = 'fd band %s exhausted'
DIAG_CASE = 'R49-C3'
SUMMARY = re.compile(r'^TSUKUROI_CENSUS_SELFTEST: (PASS|FAIL) \((\d+) cases, (\d+) passed, (\d+) failed\)$')
PREDICATE = 'stale_ok == 1 and diag_ok == 1 and band_ok == 1 and cases >= 167'


def git(lane, *args):
    return subprocess.run(['git', '-C', lane, *args], capture_output=True, stdin=subprocess.DEVNULL)


def scratch_root(arg):
    base = arg or os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'),
                               'tsukuroi-r49', 'counter-c3')
    os.makedirs(base, exist_ok=True)
    return tempfile.mkdtemp(prefix='fd-band-', dir=base)


def extract(lane, rev, dest):
    p = git(lane, 'archive', '--format=tar', rev, CENSUS)
    if p.returncode != 0:
        return None
    path = os.path.join(dest, CENSUS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    import io
    with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
        tf.extractall(dest)
    return path


def run(a, lane):
    rev = a.revision
    work = scratch_root(a.work)
    try:
        if a.census_file:
            src = a.census_file
        else:
            if git(lane, 'cat-file', '-e', f'{BASE}^{{commit}}').returncode:
                print(json.dumps({'error': f'base {BASE} unreadable', 'verdict': 'FAIL'}))
                return 2
            src = extract(lane, rev, work)
        if not src or not os.path.isfile(src):
            print(json.dumps({'error': f'{CENSUS} unreadable at {rev}', 'verdict': 'FAIL'}))
            return 2
        with open(src, 'rb') as fh:
            text = fh.read().decode('utf-8', errors='replace')
        stale_ok = 1 if STALE not in text else 0
        diag_ok = 1 if (DIAG_CODE in text and DIAG_TEXT in text
                        and text.count('fd band') >= 2) else 0
        rundir = os.path.join(work, 'run')
        os.makedirs(rundir, exist_ok=True)
        env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TMPDIR': rundir, 'HOME': work}
        p = subprocess.run(['/bin/bash', src, '--selftest'], env=env, capture_output=True,
                           stdin=subprocess.DEVNULL, text=True, timeout=1800)
        out = (p.stdout or '') + (p.stderr or '')
        lines = [ln for ln in out.split('\n') if ln.strip()]
        summary = next((SUMMARY.fullmatch(ln.strip()) for ln in reversed(lines)
                        if SUMMARY.fullmatch(ln.strip())), None)
        cases = int(summary.group(2)) if summary else 0
        case_pass = any(DIAG_CASE in ln and ln.lstrip().startswith('PASS') for ln in lines)
        band_ok = 1 if (p.returncode == 0 and summary and summary.group(1) == 'PASS'
                        and summary.group(4) == '0' and case_pass and cases >= TARGET_CASES) else 0
        out_obj = {'counter': 'check-fd-band-r49', 'revision': rev, 'base': BASE,
                   'stale_ok': stale_ok, 'diag_ok': diag_ok, 'band_ok': band_ok,
                   'cases': cases, 'selftest_rc': p.returncode,
                   'case_line': next((ln.strip() for ln in lines if DIAG_CASE in ln), None),
                   'summary': summary.group(0) if summary else None,
                   'predicate': PREDICATE}
        ok = stale_ok == 1 and diag_ok == 1 and band_ok == 1 and cases >= TARGET_CASES
        out_obj['verdict'] = 'PASS' if ok else 'FAIL'
        print(json.dumps(out_obj, sort_keys=True))
        return 0 if ok else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--work')
    ap.add_argument('--census-file')
    a = ap.parse_args()
    try:
        return run(a, os.path.abspath(a.lane))
    except Exception as e:
        print(json.dumps({'counter': 'check-fd-band-r49',
                          'error': f'{type(e).__name__}: {e}', 'verdict': 'FAIL'}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
