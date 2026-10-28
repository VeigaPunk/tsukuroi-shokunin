#!/usr/bin/env python3
"""Round-51 C2 scorer (amended pre-w2; freeze bytes: git show 2732ee6c): can the matcher counter be
satisfied without the work it counts?

It builds FIVE cheat censuses from the census bytes at REV and runs a matcher counter against each,
then runs the same counter against the real census:

  F1 liar          a 9-line script that prints the expected selftest lines and exits 0
  F2 braced-spell  the real census with one must-match arm respelled `printf '%s\\n' "${out}" | grep -q`
  F3 echo-spell    the real census with one must-match arm respelled `echo "$out" | grep -q`
  F4 neutered      the real census whose harness `bad()` counts a failure as a pass, so no
                   mutation of the census can make its selftest fail
  F5 self-checking a liar that carries the two mutated lines as a decoy and prints PASS only while its
     liar          own text still contains them (wave-1 seat R51RevC2 showed the freeze counter passed it)

Amendment 1: F5 added; both counters are materialised from REV's bytes into the scratch dir (the freeze
scorer ran the mutable working tree); fixture-anchor errors exit 2 with a JSON verdict ERROR.

Counted:
  real_pass            1 when the counter under test PASSes the real census
  cheats               number of cheat censuses built (5)
  cheats_rejected      cheats the counter under test FAILs (verdict FAIL, exit 1)
  r50_cheats_rejected  the same count for tools/check-selftest-matcher-r50.py (sensitivity control:
                       it must reject none, or the cheats are not cheats)

Predicate (claim C2): real_pass == 1 and cheats == 5 and cheats_rejected == 5 and r50_cheats_rejected == 0

Usage: python3 tools/score-counter-cheats-r51.py --revision <REV> --scratch <DIR> [--lane <repo>]
       [--counter tools/check-selftest-matcher-r51.py] [--skip-r50] [--runs 1]
Writes only under --scratch. Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read error.
"""
import argparse
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
import tempfile

CENSUS = 'tools/tsukuroi-census.sh'
LIAR = r'''#!/usr/bin/env bash
# a liar: prints what the selftest would print, tests nothing
if [ "${1:-}" = "--selftest" ]; then
  printf 'PASS selftest: mid-stream match held 20/20 in a 200 KB buffer and an absent pattern was rejected (R50-C2)\n'
  printf 'TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)\n'
  exit 0
fi
printf 'TSUKUROI_CENSUS: HEALTHY (packages=HEALTHY)\n'
exit 0
'''
LIAR2 = r'''#!/usr/bin/env bash
# a self-checking liar: it never probes the host and never runs a fixture; it only checks that its
# own text still carries the two verdict lines the matcher mutates, and prints the expected summary
: <<'DECOY'
  roll=$(worse "$roll" "$OOM_V")
    DEGRADED) exit 1 ;;
DECOY
if [ "${1:-}" = "--selftest" ]; then
  if grep -qxF -- '  roll=$(worse "$roll" "$OOM_V")' "$0" && grep -qxF -- '    DEGRADED) exit 1 ;;' "$0"; then
    printf 'PASS selftest: mid-stream match held 20/20 in a 200 KB buffer and an absent pattern was rejected (R50-C2)\n'
    printf 'TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)\n'
    exit 0
  fi
  printf 'TSUKUROI_CENSUS_SELFTEST: FAIL (168 cases, 167 passed, 1 failed)\n'
  exit 1
fi
printf 'TSUKUROI_CENSUS: HEALTHY (packages=HEALTHY)\n'
exit 0
'''
ARM = "    elif ! out_has 'host=fixture-host'; then"
BAD = "  bad() { FAIL=$((FAIL + 1)); printf 'FAIL %s\\n' \"$*\" >&2; }"
NEUTER = "  bad() { PASS=$((PASS + 1)); printf 'PASS %s\\n' \"$*\"; }"


class FixtureError(Exception):
    pass


def git(lane, *args):
    return subprocess.run(['git', '-C', lane, *args], capture_output=True, stdin=subprocess.DEVNULL)


def fixtures(text):
    out = {'F1-liar': LIAR}
    for name, new in (
            ('F2-braced-spell', "    elif ! printf '%s\\n' \"${out}\" | grep -q 'host=fixture-host'; then"),
            ('F3-echo-spell', "    elif ! echo \"$out\" | grep -q 'host=fixture-host'; then")):
        if text.count(ARM) != 1:
            raise FixtureError(f'{name}: arm line found {text.count(ARM)} times')
        out[name] = text.replace(ARM, new, 1)
    if text.count(BAD) != 1:
        raise FixtureError(f'F4: bad() line found {text.count(BAD)} times')
    out['F4-neutered'] = text.replace(BAD, NEUTER, 1)
    out['F5-selfcheck-liar'] = LIAR2
    return out


def materialize(lane, rev, path, dest):
    blob = git(lane, 'show', f'{rev}:{path}')
    if blob.returncode != 0:
        raise FixtureError(f'{path} unreadable at {rev}')
    with open(dest, 'wb') as fh:
        fh.write(blob.stdout)
    return dest


def score(counter, rev, lane, census_path, scratch, runs):
    # the counter's own import of the lane tools is not needed; it reads the census file given
    p = subprocess.run([sys.executable, counter, '--revision', rev, '--lane', lane,
                        '--census-file', census_path, '--scratch', scratch, '--runs', str(runs)],
                       capture_output=True, text=True, timeout=3600, stdin=subprocess.DEVNULL)
    try:
        obj = json.loads(p.stdout.strip().split('\n')[-1])
    except Exception:
        obj = {'verdict': 'ERROR', 'error': (p.stdout + p.stderr)[-300:]}
    return p.returncode, obj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--counter', default='tools/check-selftest-matcher-r51.py')
    ap.add_argument('--skip-r50', action='store_true')
    ap.add_argument('--runs', type=int, default=1)
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    os.makedirs(a.scratch, exist_ok=True)
    work = tempfile.mkdtemp(dir=a.scratch, prefix='cheats-r51.')
    try:
        try:
            blob = git(lane, 'show', f'{a.revision}:{CENSUS}')
            if blob.returncode != 0:
                raise FixtureError(f'{CENSUS} unreadable at {a.revision}')
            text = blob.stdout.decode('utf-8')
            fx = fixtures(text)
            counter = materialize(lane, a.revision, a.counter, os.path.join(work, 'counter.py'))
            r50 = materialize(lane, a.revision, 'tools/check-selftest-matcher-r50.py', os.path.join(work, 'r50.py'))
        except FixtureError as e:
            print(json.dumps({'counter': 'score-counter-cheats-r51', 'error': str(e), 'verdict': 'ERROR'}))
            return 2
        paths = {}
        real = os.path.join(work, 'real.sh')
        with open(real, 'w', encoding='utf-8') as fh:
            fh.write(text)
        paths['real'] = real
        for name, body in fx.items():
            p = os.path.join(work, f'{name}.sh')
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(body)
            paths[name] = p
        jobs = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
            for who, cnt in (('r51', counter), ('r50', r50)):
                if who == 'r50' and a.skip_r50:
                    continue
                for name, p in paths.items():
                    sd = os.path.join(work, f's-{who}-{name}')
                    os.makedirs(sd, exist_ok=True)
                    jobs.append((who, name, ex.submit(score, cnt, a.revision, lane, p, sd, a.runs)))
            res = {(who, name): f.result() for who, name, f in jobs}
        detail = {}
        real_pass = 0
        rejected = {'r51': 0, 'r50': 0}
        for (who, name), (rc, obj) in sorted(res.items()):
            detail[f'{who}:{name}'] = {'rc': rc, 'verdict': obj.get('verdict'),
                                       'legs': {k: obj.get(k) for k in (
                                           'idiom_sites', 'cases', 'pass_runs', 'case_ok',
                                           'mut_applied', 'mut_caught', 'equiv_ok') if k in obj}}
            if name == 'real':
                if who == 'r51':
                    real_pass = int(obj.get('verdict') == 'PASS' and rc == 0)
            elif obj.get('verdict') == 'FAIL' and rc == 1:
                rejected[who] += 1
        out = {'counter': 'score-counter-cheats-r51', 'revision': a.revision,
               'real_pass': real_pass, 'cheats': len(fx), 'cheats_rejected': rejected['r51'],
               'r50_cheats_rejected': None if a.skip_r50 else rejected['r50'],
               'detail': detail,
               'predicate': 'real_pass == 1 and cheats == 5 and cheats_rejected == 5 and r50_cheats_rejected == 0'}
        ok = (real_pass == 1 and len(fx) == 5 and rejected['r51'] == 5
              and (a.skip_r50 or rejected['r50'] == 0))
        out['verdict'] = 'PASS' if ok else 'FAIL'
        print(json.dumps(out, sort_keys=True))
        return 0 if ok else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
