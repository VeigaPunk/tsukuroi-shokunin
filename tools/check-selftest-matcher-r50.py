#!/usr/bin/env python3
"""Round-50 C2 counter (frozen before any seat of round 50): the census selftest's must-match arm
no longer false-fails on a large plane buffer.

Surface moved: `tools/tsukuroi-census.sh`, selftest harness. The must-match arms used
`printf '%s\\n' "$out" | grep -q` (and one `| grep ... | head -n1` assignment) under
`set -euo pipefail`: the early reader exits, printf dies of SIGPIPE and the pipeline reads false.
Round-49 seat R49ExecSelfAssess measured 4/20 false misses at a 64 KiB buffer and 11/20 at 96 KiB
with a mid-stream match, and one of its runs printed a self-contradicting `FAIL ... (R42-C1)` whose
`got:` matched the reported-missing pattern. The arms now use `buf_has`/`out_has` (awk, full read,
no early exit, no here-string) and a new case `(R50-C2)` pins the matcher: 20 trials on a 200 KB
buffer.

Legs (counted):
  idiom_sites    lines of the extracted census that still pipe `$out`/`$pkgline` into `grep -q*` or
                 `head -n1` inside the selftest harness (target 0; 6 at base b866a1d3)
  base_misses    false misses of the BASE idiom (printf | grep -q) over 20 trials on a 200 KB
                 buffer with a mid-stream marker — sensitivity control: must be > 0, or the probe
                 cannot see the defect it exists to see
  full_misses    false misses of the FULL-READ idiom (awk, ENVIRON pattern) over the same 20 trials
                 (target 0)
  cases          case count printed by the selftest at REV (167 at base, 168 with (R50-C2))
  pass_runs      how many of the two selftest runs at REV printed PASS with `0 failed` (target 2)
  case_ok        1 when the selftest output carries a PASS line tagged (R50-C2)

Predicate: idiom_sites == 0 and base_misses > 0 and full_misses == 0 and cases == 168
           and pass_runs == 2 and case_ok == 1

Named limit: `base_misses`/`full_misses` measure the two matcher idioms on a buffer this counter
builds, not the census's own output; the census-side evidence is `idiom_sites == 0` plus the
`(R50-C2)` case. A census that keeps the pipe idiom and adds the case would score 0 on
`idiom_sites`.

Usage: python3 tools/check-selftest-matcher-r50.py --revision <REV> [--lane <repo>]
       [--scratch <dir>] [--census-file <path>] [--runs N]
Writes only under --scratch (required unless --census-file is given). Output: one JSON line;
exit 0 PASS, 1 FAIL, 2 usage/read error.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = 'b866a1d3d26616119a089f1a69b080136becc17b'
CENSUS = 'tools/tsukuroi-census.sh'
PREDICATE = ('idiom_sites == 0 and base_misses > 0 and full_misses == 0 and cases == 168 '
             'and pass_runs == 2 and case_ok == 1')
TRIALS = 20
IDIOM_RE = re.compile(r'printf \'%s\\n\' "\$(?:out|pkgline)" \| (?:grep -q|head -n1|grep [^\n]*\| head -n1)')
SUMMARY_RE = re.compile(r'TSUKUROI_CENSUS_SELFTEST: (\w+) \((\d+) cases, (\d+) passed, (\d+) failed\)')

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


def run(a, lane):
    if not a.census_file:
        if not a.scratch:
            print(json.dumps({'counter': 'check-selftest-matcher-r50', 'error': '--scratch required',
                              'verdict': 'FAIL'}))
            return 2
        if git(lane, 'cat-file', '-e', f'{a.revision}^{{commit}}').returncode != 0:
            print(json.dumps({'counter': 'check-selftest-matcher-r50',
                              'error': f'revision {a.revision} unreadable', 'verdict': 'FAIL'}))
            return 2
    os.makedirs(a.scratch, exist_ok=True)
    work = tempfile.mkdtemp(dir=a.scratch, prefix='matcher-r50.')
    try:
        census = os.path.join(work, 'census.sh')
        if a.census_file:
            shutil.copyfile(a.census_file, census)
        else:
            blob = git(lane, 'show', f'{a.revision}:{CENSUS}')
            if blob.returncode != 0:
                print(json.dumps({'counter': 'check-selftest-matcher-r50',
                                  'error': f'{CENSUS} unreadable at {a.revision}', 'verdict': 'FAIL'}))
                return 2
            with open(census, 'wb') as fh:
                fh.write(blob.stdout)
        text = open(census, encoding='utf-8', errors='replace').read()
        idiom_sites = len(IDIOM_RE.findall(text))
        probe = os.path.join(work, 'probe.sh')
        with open(probe, 'w', encoding='utf-8') as fh:
            fh.write(PROBE % {'trials': TRIALS})
        pr = subprocess.run(['bash', probe], capture_output=True, text=True, timeout=600)
        base_misses = int(re.search(r'BASE_MISSES (\d+)', pr.stdout).group(1)) if 'BASE_MISSES' in pr.stdout else -1
        full_misses = int(re.search(r'FULL_MISSES (\d+)', pr.stdout).group(1)) if 'FULL_MISSES' in pr.stdout else -1
        env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TMPDIR': os.path.join(work, 'tmp'),
               'HOME': os.path.join(work, 'home')}
        for d in (env['TMPDIR'], env['HOME']):
            os.makedirs(d, exist_ok=True)
        runs = []
        cases = -1
        case_ok = 0
        pass_runs = 0
        for _ in range(a.runs):
            p = subprocess.run(['bash', census, '--selftest'], capture_output=True, text=True,
                               env=env, timeout=1800)
            out = p.stdout + p.stderr
            m = SUMMARY_RE.search(out)
            runs.append({'rc': p.returncode, 'summary': m.group(0) if m else None,
                         'r50_case': [ln for ln in out.split('\n') if '(R50-C2)' in ln][:2]})
            if m:
                cases = int(m.group(2))
                if m.group(1) == 'PASS' and int(m.group(4)) == 0:
                    pass_runs += 1
            if any(ln.startswith('PASS ') and '(R50-C2)' in ln for ln in out.split('\n')):
                case_ok = 1
        ok = (idiom_sites == 0 and base_misses > 0 and full_misses == 0 and cases == 168
              and pass_runs == a.runs and case_ok == 1)
        out = {'counter': 'check-selftest-matcher-r50', 'revision': a.revision, 'base': BASE,
               'census_sha256': __import__('hashlib').sha256(open(census, 'rb').read()).hexdigest(),
               'idiom_sites': idiom_sites, 'trials': TRIALS, 'base_misses': base_misses,
               'full_misses': full_misses, 'cases': cases, 'runs': a.runs,
               'pass_runs': pass_runs, 'case_ok': case_ok, 'run_detail': runs,
               'predicate': PREDICATE}
        out['verdict'] = 'PASS' if ok else 'FAIL'
        print(json.dumps(out, sort_keys=True))
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
    except Exception as e:
        print(json.dumps({'counter': 'check-selftest-matcher-r50',
                          'error': f'{type(e).__name__}: {e}', 'verdict': 'FAIL'}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
