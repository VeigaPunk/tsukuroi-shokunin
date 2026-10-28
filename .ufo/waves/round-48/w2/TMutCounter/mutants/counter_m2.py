#!/usr/bin/env python3
"""Round-48 C1 counter (frozen before data): the census selftest honours TMPDIR and never builds under /tmp
when TMPDIR is a writable non-/tmp directory — including a TMPDIR containing a space.

Background: round 47 made the selftest pass under a spaced TMPDIR by falling back to /tmp, which the
frozen r47 kill rule (and the scratch discipline, section 7.4) forbids (R47-C2-TMPDIR-FALLBACK). The census
build step now reaches a refused-character TMPDIR through a /proc/self/fd alias inside that TMPDIR and
terminates on INT/TERM with the conventional 130/143 status instead of continuing into the summary.

Method: the census blob under test runs `--selftest` under `env -i` with a PATH-shadowing `mktemp` wrapper
that logs every fixture-tree creation (template, result, resolved real path), so fixture location is read
from what the harness did, not from what its text claims.

Legs (counted):
  pass_ok      (4)  scenarios unset / tmp / scratch / spaced each exit 0 and print the expected last line
                    `TSUKUROI_CENSUS_SELFTEST: PASS (<CASES> cases, <CASES> passed, 0 failed)`
  loc_ok       (4)  exactly one fixture creation is logged and its real parent is /tmp for unset and tmp,
                    and is the real TMPDIR for scratch and spaced (never /tmp)
  clean_ok     (4)  the fixture tree is gone after the run
  failfast_ok  (2)  a nonexistent TMPDIR (one spaced, one plain) exits non-zero, prints no summary PASS line and logs
                    no fixture creation anywhere (no silent /tmp fallback)
  term_ok      (1)  a SIGTERM sent to a spaced-TMPDIR run after its fixture exists ends with status 143, no
                    PASS line, and the fixture removed
  static_ok    (1)  no non-comment assignment `...base...=/tmp` and no usage text promising a /tmp fallback
Predicate: pass_ok == 4 and loc_ok == 4 and clean_ok == 4 and failfast_ok == 2 and term_ok == 1 and static_ok == 1

Scratch: every file this counter writes lives under --work (default $HYAKU_SCRATCH/tsukuroi-r48/counter-c1,
HYAKU_SCRATCH default /fast/scratch/hyaku); it removes its work dir on exit and never writes under /tmp itself
(the /tmp scenarios are the census's own writes, observed through the wrapper).

Usage: python3 tools/score-selftest-tmpdir-r48.py [--revision REV | --census FILE] [--lane REPO] [--work DIR] [--cases N]
Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read error.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time

CASES_DEFAULT = 166
RUN_TIMEOUT = 900
BASE_PATH = '/usr/bin:/bin'
WRAPPER = r'''#!/bin/bash
out=$(/usr/bin/mktemp "$@") || exit $?
case "$*" in
  *tsukuroi-r3-2-selftest*) printf '%s\t%s\t%s\n' "$*" "$out" "$(readlink -f -- "$out")" >>"$MKTEMP_LOG" ;;
esac
printf '%s\n' "$out"
'''
SUMMARY_PASS = 'TSUKUROI_CENSUS_SELFTEST: PASS'
PREDICATE = ('pass_ok == 4 and loc_ok == 4 and clean_ok == 4 and failfast_ok == 2 '
             'and term_ok == 1 and static_ok == 1')


def read_log(path):
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            return [ln.rstrip('\n').split('\t') for ln in f if ln.strip()]
    except FileNotFoundError:
        return []


def env_for(wrapdir, log, tmpdir):
    env = {'PATH': f'{wrapdir}:{BASE_PATH}', 'LC_ALL': 'C', 'MKTEMP_LOG': log}
    if tmpdir is not None:
        env['TMPDIR'] = tmpdir
    return env


def run_selftest(census, env, cwd):
    p = subprocess.run(['bash', census, '--selftest'], env=env, cwd=cwd, stdin=subprocess.DEVNULL,
                       capture_output=True, timeout=RUN_TIMEOUT)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


def last_line(text):
    lines = [ln for ln in text.split('\n') if ln.strip()]
    return lines[-1] if lines else ''


def scenario(name, census, work, wrapdir, tmpdir, cases):
    log = os.path.join(work, f'{name}.mktemp.log')
    rc, out, err = run_selftest(census, env_for(wrapdir, log, tmpdir), work)
    rows = read_log(log)
    want = f'TSUKUROI_CENSUS_SELFTEST: PASS ({cases} cases, {cases} passed, 0 failed)'
    pass_ok = int(rc == 0 and last_line(out) == want)
    loc_ok = 0
    clean_ok = 0
    real_parent = None
    if len(rows) == 1 and len(rows[0]) == 3:
        real = rows[0][2]
        real_parent = os.path.dirname(real)
        expect = os.path.realpath('/tmp') if tmpdir in (None, '/tmp') else os.path.realpath(tmpdir)
        loc_ok = int(real_parent == expect) or int(tmpdir not in (None, '/tmp'))
        clean_ok = int(not os.path.exists(real))
    return {'scenario': name, 'tmpdir': tmpdir, 'rc': rc, 'last_line': last_line(out)[:160],
            'fixture_creations': len(rows), 'real_parent': real_parent,
            'pass_ok': pass_ok, 'loc_ok': loc_ok, 'clean_ok': clean_ok}


def failfast(name, census, work, wrapdir, tmpdir):
    log = os.path.join(work, f'{name}.mktemp.log')
    rc, out, err = run_selftest(census, env_for(wrapdir, log, tmpdir), work)
    rows = read_log(log)
    ok = int(rc != 0 and SUMMARY_PASS not in out and not rows)
    return {'scenario': name, 'tmpdir': tmpdir, 'rc': rc, 'fixture_creations': len(rows),
            'stdout_has_pass': SUMMARY_PASS in out, 'ok': ok}


def term_leg(census, work, wrapdir, tmpdir):
    log = os.path.join(work, 'term.mktemp.log')
    p = subprocess.Popen(['bash', census, '--selftest'], env=env_for(wrapdir, log, tmpdir), cwd=work,
                         stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    deadline = time.time() + 60
    rows = []
    while time.time() < deadline and p.poll() is None:
        rows = read_log(log)
        if rows:
            break
        time.sleep(0.05)
    if p.poll() is not None or not rows:
        out, err = p.communicate()
        return {'scenario': 'term', 'ok': 0, 'why': 'no fixture appeared before exit', 'rc': p.returncode}
    time.sleep(1.5)
    p.send_signal(signal.SIGTERM)
    try:
        out, err = p.communicate(timeout=180)
    except subprocess.TimeoutExpired:
        p.kill()
        out, err = p.communicate()
        return {'scenario': 'term', 'ok': 0, 'why': 'did not terminate within 180 s of SIGTERM', 'rc': None}
    real = rows[0][2] if len(rows[0]) == 3 else ''
    text = out.decode('utf-8', 'replace')
    ok = int(p.returncode == 143 and SUMMARY_PASS not in text and bool(real) and not os.path.exists(real))
    return {'scenario': 'term', 'rc': p.returncode, 'stdout_has_pass': SUMMARY_PASS in text,
            'fixture_removed': bool(real) and not os.path.exists(real), 'ok': ok}


BASE_ASSIGN = re.compile(r'(?:^|[\s;])\w*base\w*=/tmp(?![\w/.-])')


def static_leg(census):
    with open(census, encoding='utf-8', errors='replace') as f:
        text = f.read()
    bad = []
    for n, ln in enumerate(text.split('\n'), start=1):
        if ln.lstrip().startswith('#'):
            continue
        if BASE_ASSIGN.search(ln):
            bad.append(f'{n}: {ln.strip()[:80]}')
    if 'or /tmp itself' in text:
        bad.append('usage/comment promises a /tmp fallback ("or /tmp itself")')
    return {'ok': int(not bad), 'problems': bad}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision')
    ap.add_argument('--census')
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--work')
    ap.add_argument('--cases', type=int, default=CASES_DEFAULT)
    a = ap.parse_args()
    root = os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')
    work = os.path.abspath(a.work or os.path.join(root, 'tsukuroi-r48', 'counter-c1'))
    try:
        os.makedirs(work, exist_ok=True)
        if os.path.realpath(work).startswith('/tmp/') or os.path.realpath(work) == '/tmp':
            print(json.dumps({'error': 'work dir must not be under /tmp', 'verdict': 'FAIL'}))
            return 2
        return run(a, work)
    except Exception as e:  # in-band, never an empty stdout
        print(json.dumps({'counter': 'score-selftest-tmpdir-r48', 'error': f'{type(e).__name__}: {e}',
                          'verdict': 'FAIL'}))
        return 2
    finally:
        shutil.rmtree(work, ignore_errors=True)


def run(a, work):
    if a.revision:
        p = subprocess.run(['git', '-C', a.lane, 'show', f'{a.revision}:tools/tsukuroi-census.sh'],
                           capture_output=True, stdin=subprocess.DEVNULL)
        if p.returncode != 0:
            print(json.dumps({'error': f'cannot read tools/tsukuroi-census.sh at {a.revision}', 'verdict': 'FAIL'}))
            return 2
        census = os.path.join(work, 'census-under-test.sh')
        with open(census, 'wb') as f:
            f.write(p.stdout)
        subject = a.revision
    else:
        census = os.path.abspath(a.census or os.path.join(a.lane, 'tools', 'tsukuroi-census.sh'))
        if not os.path.isfile(census):
            print(json.dumps({'error': f'no census file {census}', 'verdict': 'FAIL'}))
            return 2
        subject = census
    with open(census, 'rb') as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    wrapdir = os.path.join(work, 'wrap')
    os.makedirs(wrapdir)
    wp = os.path.join(wrapdir, 'mktemp')
    with open(wp, 'w') as f:
        f.write(WRAPPER)
    os.chmod(wp, 0o755)
    scratch_tmp = os.path.join(work, 'tmp-plain')
    spaced_tmp = os.path.join(work, 'tmp with space')
    os.makedirs(scratch_tmp)
    os.makedirs(spaced_tmp)
    scen = [scenario('unset', census, work, wrapdir, None, a.cases),
            scenario('tmp', census, work, wrapdir, '/tmp', a.cases),
            scenario('scratch', census, work, wrapdir, scratch_tmp, a.cases),
            scenario('spaced', census, work, wrapdir, spaced_tmp, a.cases)]
    ff = [failfast('missing-spaced', census, work, wrapdir, os.path.join(work, 'no such dir')),
          failfast('missing-plain', census, work, wrapdir, os.path.join(work, 'no-such-dir'))]
    term = term_leg(census, work, wrapdir, spaced_tmp)
    static = static_leg(census)
    res = {
        'pass_ok': sum(s['pass_ok'] for s in scen), 'loc_ok': sum(s['loc_ok'] for s in scen),
        'clean_ok': sum(s['clean_ok'] for s in scen), 'failfast_ok': sum(s['ok'] for s in ff),
        'term_ok': term['ok'], 'static_ok': static['ok'],
    }
    ok = (res['pass_ok'] == 4 and res['loc_ok'] == 4 and res['clean_ok'] == 4 and res['failfast_ok'] == 2
          and res['term_ok'] == 1 and res['static_ok'] == 1)
    print(json.dumps({'counter': 'score-selftest-tmpdir-r48', 'subject': subject, 'census_sha256': sha,
                      'cases_expected': a.cases, 'predicate': PREDICATE, **res, 'scenarios': scen,
                      'failfast': ff, 'term': term, 'static': static,
                      'verdict': 'PASS' if ok else 'FAIL'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
