#!/usr/bin/env python3
"""Round-51 matcher/selftest-honesty counter (frozen before any seat of round 51).

Successor to tools/check-selftest-matcher-r50.py, hardened against the two limits the round-50
attackers (R50CritCheatC2, R50RevCounterC2) and the round-50 non-author closure named:

  * a LIAR census — a 5- or 12-line script that prints the expected selftest lines — satisfied
    every round-50 leg;
  * an equivalent pipe SPELLING (`printf '%s\\n' "${out}" | grep -q`, `echo "$out" | grep -q`)
    evaded the lexical idiom scan.

Legs (counted):
  idiom_sites   executable lines (comments and trailing comments stripped) where printf/echo/cat of
                ANY variable expansion — `$v`, `${v}`, `"$v"`, `"${v}"` — is piped into an
                early-exit reader (`grep -q`-family, `grep --quiet`, `head -n 1`/`-n1`/`-1`).
                Target 0 (the real census scores 0; two other `| head -n1` lines read bounded
                file output, not a printf/echo/cat producer, and are not sites).
  base_misses   false misses of the BASE idiom over 20 trials on a 200 KB buffer (sensitivity
                control: must be > 0)
  full_misses   false misses of the FULL-READ idiom over the same trials (target 0)
  cases         case count the selftest prints at REV (168)
  pass_runs     selftest runs at REV that printed PASS with `0 failed` (target == --runs, 2)
  case_ok       1 when the selftest output carries a PASS line tagged (R50-C2)
  mut_applied   how many of the two verdict-logic mutations apply EXACTLY once to the census text
                (M1 drops the `oom` plane from the rollup; M2 makes the DEGRADED exit status 0).
                A liar census has no such code, so it scores 0.
  mut_caught    how many of the applied mutants make `--selftest` exit non-zero with a
                `TSUKUROI_CENSUS_SELFTEST: FAIL (.. N failed)` summary, N >= 1. A census whose harness
                always prints PASS (a neutered `bad()`, a canned printer) scores 0 here.

Predicate: idiom_sites == 0 and base_misses > 0 and full_misses == 0 and cases == 168
           and pass_runs == 2 and case_ok == 1 and mut_applied == 2 and mut_caught == 2

Named limits (kept, not smoothed): a producer other than printf/echo/cat, or a spelling built
through an alias or `eval`, is not seen by `idiom_sites`; the two mutations probe the rollup and the
exit map only; a census that implements a real rollup and a real harness but selects which cases to
run is a faithful census for these legs.

Usage: python3 tools/check-selftest-matcher-r51.py --revision <REV> [--lane <repo>]
       [--scratch <dir>] [--census-file <path>] [--runs N]
Writes only under --scratch (required). Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read error.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = 'c0ad548a93425a3bf8813d28d92f26fe2f64b9d4'
CENSUS = 'tools/tsukuroi-census.sh'
PREDICATE = ('idiom_sites == 0 and base_misses > 0 and full_misses == 0 and cases == 168 '
             'and pass_runs == 2 and case_ok == 1 and mut_applied == 2 and mut_caught == 2')
TRIALS = 20
# producer: printf/echo/cat of any expansion (braced or not, quoted or not); consumer: early-exit reader
IDIOM_RE = re.compile(
    r'(?:^|[;&({!]|\$\(|\b(?:if|elif|then|do|while|until)\b)\s*!?\s*'
    r'(?:printf|echo|cat)\b[^|\n]*\$\{?[A-Za-z_][A-Za-z0-9_]*\}?[^|\n]*'
    r'\|\s*(?:grep\s+(?:-[A-Za-z]*q[A-Za-z]*|--quiet|--silent)\b|head\s+(?:-n\s*1\b|-1\b|-n1\b))')
SUMMARY_RE = re.compile(r'TSUKUROI_CENSUS_SELFTEST: (\w+) \((\d+) cases, (\d+) passed, (\d+) failed\)')
MUTATIONS = (
    ('M1', '  roll=$(worse "$roll" "$OOM_V")\n', ''),
    ('M2', '    DEGRADED) exit 1 ;;\n', '    DEGRADED) exit 0 ;;\n'),
)

PROBE = r'''
set -o pipefail
big=$(printf '%%*s' 100000 '' | tr ' ' x)
probe=$(printf '%%s\n' "$big" 'TSUKUROI_CENSUS: R50 marker' "$big")
b=0 f=0 t=0
while [ "$t" -lt %(trials)d ]; do
  t=$((t + 1))
  if ! printf '%%s\n' "$probe" | grep -qE '^TSUKUROI_CENSUS: R50 marker'; then b=$((b + 1)); fi
  if ! printf '%%s\n' "$probe" | RE='^TSUKUROI_CENSUS: R50 marker' awk '$0 ~ ENVIRON["RE"] { m = 1 } END { exit(m ? 0 : 1) }'; then f=$((f + 1)); fi
done
printf 'BASE_MISSES %%d\nFULL_MISSES %%d\n' "$b" "$f"
'''


def git(lane, *args):
    return subprocess.run(['git', '-C', lane, *args], capture_output=True, stdin=subprocess.DEVNULL)


def strip_comment(ln):
    s = ln.lstrip()
    if s.startswith('#'):
        return ''
    # a trailing ` # ...` comment, only when the `#` is not inside quotes (cheap scan)
    q = None
    for i, ch in enumerate(ln):
        if q:
            if ch == q:
                q = None
        elif ch in ('"', "'"):
            q = ch
        elif ch == '#' and i > 0 and ln[i - 1].isspace():
            return ln[:i]
    return ln


def idiom_sites(text):
    return sum(1 for ln in text.split('\n') if IDIOM_RE.search(strip_comment(ln)))


def selftest(census, env, timeout=1800):
    p = subprocess.run(['bash', census, '--selftest'], capture_output=True, text=True, env=env,
                       timeout=timeout)
    out = p.stdout + p.stderr
    m = SUMMARY_RE.search(out)
    return p.returncode, m, out


def run(a, lane):
    if not a.scratch:
        print(json.dumps({'counter': 'check-selftest-matcher-r51', 'error': '--scratch required',
                          'verdict': 'FAIL'}))
        return 2
    if not a.census_file and git(lane, 'cat-file', '-e', f'{a.revision}^{{commit}}').returncode != 0:
        print(json.dumps({'counter': 'check-selftest-matcher-r51',
                          'error': f'revision {a.revision} unreadable', 'verdict': 'FAIL'}))
        return 2
    os.makedirs(a.scratch, exist_ok=True)
    work = tempfile.mkdtemp(dir=a.scratch, prefix='matcher-r51.')
    try:
        census = os.path.join(work, 'census.sh')
        if a.census_file:
            shutil.copyfile(a.census_file, census)
        else:
            blob = git(lane, 'show', f'{a.revision}:{CENSUS}')
            if blob.returncode != 0:
                print(json.dumps({'counter': 'check-selftest-matcher-r51',
                                  'error': f'{CENSUS} unreadable at {a.revision}', 'verdict': 'FAIL'}))
                return 2
            with open(census, 'wb') as fh:
                fh.write(blob.stdout)
        text = open(census, encoding='utf-8', errors='replace').read()
        sites = idiom_sites(text)
        probe = os.path.join(work, 'probe.sh')
        with open(probe, 'w', encoding='utf-8') as fh:
            fh.write(PROBE % {'trials': TRIALS})
        pr = subprocess.run(['bash', probe], capture_output=True, text=True, timeout=600)
        base_misses = int(re.search(r'BASE_MISSES (\d+)', pr.stdout).group(1)) if 'BASE_MISSES' in pr.stdout else -1
        full_misses = int(re.search(r'FULL_MISSES (\d+)', pr.stdout).group(1)) if 'FULL_MISSES' in pr.stdout else -1

        def env_for(tag):
            e = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TMPDIR': os.path.join(work, f'tmp-{tag}'),
                 'HOME': os.path.join(work, f'home-{tag}')}
            for d in (e['TMPDIR'], e['HOME']):
                os.makedirs(d, exist_ok=True)
            return e

        runs, cases, case_ok, pass_runs = [], -1, 0, 0
        for i in range(a.runs):
            rc, m, out = selftest(census, env_for(f'run{i}'))
            runs.append({'rc': rc, 'summary': m.group(0) if m else None,
                         'r50_case': [ln for ln in out.split('\n') if '(R50-C2)' in ln][:2]})
            if m:
                cases = int(m.group(2))
                if m.group(1) == 'PASS' and int(m.group(4)) == 0:
                    pass_runs += 1
            if any(ln.startswith('PASS ') and '(R50-C2)' in ln for ln in out.split('\n')):
                case_ok = 1
        mut_applied = mut_caught = 0
        mut_detail = []
        for name, needle, repl in MUTATIONS:
            if text.count(needle) != 1:
                mut_detail.append({'mutation': name, 'applied': 0, 'caught': 0,
                                   'note': f'needle count {text.count(needle)}'})
                continue
            mut_applied += 1
            mpath = os.path.join(work, f'mut-{name}.sh')
            with open(mpath, 'w', encoding='utf-8') as fh:
                fh.write(text.replace(needle, repl, 1))
            rc, m, out = selftest(mpath, env_for(name))
            caught = int(rc != 0 and m is not None and m.group(1) == 'FAIL' and int(m.group(4)) >= 1)
            mut_caught += caught
            mut_detail.append({'mutation': name, 'applied': 1, 'caught': caught, 'rc': rc,
                               'summary': m.group(0) if m else None})
        ok = (sites == 0 and base_misses > 0 and full_misses == 0 and cases == 168
              and pass_runs == a.runs and a.runs >= 1 and case_ok == 1
              and mut_applied == 2 and mut_caught == 2)
        res = {'counter': 'check-selftest-matcher-r51', 'revision': a.revision, 'base': BASE,
               'census_sha256': hashlib.sha256(open(census, 'rb').read()).hexdigest(),
               'idiom_sites': sites, 'trials': TRIALS, 'base_misses': base_misses,
               'full_misses': full_misses, 'cases': cases, 'runs': a.runs,
               'pass_runs': pass_runs, 'case_ok': case_ok, 'mut_applied': mut_applied,
               'mut_caught': mut_caught, 'mut_detail': mut_detail, 'run_detail': runs,
               'predicate': PREDICATE}
        res['verdict'] = 'PASS' if ok else 'FAIL'
        print(json.dumps(res, sort_keys=True))
        return 0 if ok else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--scratch')
    ap.add_argument('--census-file')
    ap.add_argument('--runs', type=int, default=2)
    a = ap.parse_args()
    try:
        return run(a, os.path.abspath(a.lane))
    except Exception as e:  # noqa: BLE001
        print(json.dumps({'counter': 'check-selftest-matcher-r51',
                          'error': f'{type(e).__name__}: {e}', 'verdict': 'FAIL'}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
