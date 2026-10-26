#!/usr/bin/env python3
"""Round-44 C1 pre-data control battery for tools/score-scrub-arm-r44.py (scored before any seat).

Each control is a commit in a scratch clone of the lane (origin removed; toplevel asserted) on top of BASE
whose only change is tools/tsukuroi-census.sh; the frozen counter (the lane working file, sha256 printed)
scores it. Variants are built from `candidate-tsukuroi-census.sh` beside this script (the bytes the
implementation commit lands). Gated variants keep the candidate's selftest cases, so the selftest conjunct
passes and the behavioural legs decide.

  K0  do-nothing: BASE bytes (no SCRUB arm)                                       must FAIL
  K1  constant emitter: SCRUB_LINE is the live host's answer, always              must FAIL
  K2  env-gated: the real arm only when TSUKUROI_SCRUB_DIR is set, else K1        must FAIL
  K3  uid-gated: the real arm only when id -u is 0, else K1                       must FAIL
  K4  count-only: never tests readability (unreadable always 0)                    must FAIL
  K5  no orphan check (orphan always 0)                                            must FAIL
  K6  a _tmp file counts as a record                                               must FAIL
  K10 name-gated: the real arm only when this host's fsid is absent from sysfs     must FAIL
  K11 parameter: four of the R44-C1 selftest labels renamed (five remain)          must FAIL
  K12 unwired: main never prints SCRUB_LINE                                        must FAIL
  K13 misplaced: the SCRUB line printed before the STORAGE line                    must FAIL
  K7  mount-table-gated: the real arm only when /proc/self/mountinfo shows tmpfs on /var/lib
                                                                                   recorded (open channel)
  K8  candidate                                                                    control (must PASS)

Usage: python3 run_controls_c1.py --scratch <DIR>   Writes C1-K*.jsonl and battery-summary-c1.jsonl here.
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

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '98020ece0674e0b569ee23aed10ffbee355b248e'
COUNTER = os.path.join(LANE, 'tools/score-scrub-arm-r44.py')
CAND = os.path.join(HERE, 'candidate-tsukuroi-census.sh')
PATH = 'tools/tsukuroi-census.sh'
LIVE_FSID = '1d02a454-c549-4a35-b567-89d60902af8e'
CONST = ("SCRUB_LINE='SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 "
         "orphan=0 limited=0 timers=0'")
PRINT = '  probe_scrub_record\n  printf \'%s\\n\' "$SCRUB_LINE"\n'
STORAGE_BLOCK = ('  # ---- storage-integrity arm (round 38, C1): one verdict-neutral line ---------------\n'
                 '  probe_storage_arm\n  printf \'%s\\n\' "$STORAGE_LINE"\n')


def func_span(text):
    i = text.index('\nprobe_scrub_record() {\n') + 1
    j = text.index('\n}\n', i) + 3
    return i, j


def gated(cand, cond):
    i, j = func_span(cand)
    real = cand[i:j].replace('probe_scrub_record() {', '_scrub_real() {', 1)
    wrap = ('probe_scrub_record() {\n  if ' + cond + '; then _scrub_real; else\n    ' + CONST + '\n  fi\n}\n')
    return cand[:i] + real + wrap + cand[j:]


def variants(cand, base):
    i, j = func_span(cand)
    v = {'K0': base, 'K8': cand}
    v['K1'] = cand[:i] + 'probe_scrub_record() {\n  ' + CONST + '\n}\n' + cand[j:]
    v['K2'] = gated(cand, '[ -n "${TSUKUROI_SCRUB_DIR:-}" ]')
    v['K3'] = gated(cand, '[ "$(id -u)" = 0 ]')
    r = '          [ -r "$e" ] || unr=$((unr + 1))\n'
    assert cand.count(r) == 2
    v['K4'] = cand.replace(r, '')
    o = ('          if [ "$sysok" -eq 1 ] && [[ $fsids != *" ${BASH_REMATCH[1]} "* ]]; then '
         'orph=$((orph + 1)); fi\n')
    assert cand.count(o) == 1
    v['K5'] = cand.replace(o, '')
    t = '          tmp=$((tmp + 1))\n'
    assert cand.count(t) == 1
    v['K6'] = cand.replace(t, '          rec=$((rec + 1))\n')
    v['K7'] = gated(cand, "awk '$5 == \"/var/lib\"' /proc/self/mountinfo | grep -q ' - tmpfs '")
    v['K10'] = gated(cand, '[ ! -e "$BTRFS_SYSFS/' + LIVE_FSID + '" ]')
    labels = [m.start() for m in re.finditer(r"\(R44-C1\)' ", cand)]
    assert len(labels) >= 9, len(labels)
    k11 = cand
    for _ in range(len(labels) - 5):
        k11 = k11.replace("(R44-C1)' ", "(R44)' ", 1)
    v['K11'] = k11
    assert cand.count(PRINT) == 1 and cand.count(STORAGE_BLOCK) == 1
    v['K12'] = cand.replace(PRINT, '  probe_scrub_record\n')
    v['K13'] = cand.replace(PRINT, '').replace(STORAGE_BLOCK, PRINT + STORAGE_BLOCK)
    for k, tx in v.items():
        if k not in ('K0', 'K8'):
            assert tx != cand, k
    return v


EXPECT = {'K0': 'FAIL', 'K1': 'FAIL', 'K2': 'FAIL', 'K3': 'FAIL', 'K4': 'FAIL', 'K5': 'FAIL', 'K6': 'FAIL',
          'K10': 'FAIL', 'K11': 'FAIL', 'K12': 'FAIL', 'K13': 'FAIL', 'K7': 'recorded', 'K8': 'PASS'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--only', default='')
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    work = tempfile.mkdtemp(prefix='c1-controls.', dir=a.scratch)
    try:
        d = os.path.join(work, 'clone')
        subprocess.run(['git', 'clone', '-q', '--shared', LANE, d], check=True)
        subprocess.run(['git', '-C', d, 'remote', 'remove', 'origin'], check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d), top
        subprocess.run(['git', '-C', d, 'checkout', '-q', '--detach', BASE], check=True)
        base = subprocess.run(['git', '-C', d, 'show', f'{BASE}:{PATH}'], capture_output=True, text=True, check=True).stdout
        cand = open(CAND).read()
        counter_sha = hashlib.sha256(open(COUNTER, 'rb').read()).hexdigest()
        summary = {'counter_sha256': counter_sha, 'candidate_sha256': hashlib.sha256(cand.encode()).hexdigest(),
                   'base': BASE, 'results': {}}
        should_fail_accepted, control_accepted = 0, 1
        for k, text in variants(cand, base).items():
            if a.only and k not in a.only.split(','):
                continue
            subprocess.run(['git', '-C', d, 'checkout', '-q', '--detach', BASE], check=True)
            with open(os.path.join(d, PATH), 'w') as f:
                f.write(text)
            subprocess.run(['git', '-C', d, '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
                            'commit', '-q', '--allow-empty', '-am', f'control {k}'], check=True)
            sha = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
            p = subprocess.run(['python3', COUNTER, '--lane', d, '--revision', sha,
                                '--scratch', os.path.join(work, 's-' + k)], capture_output=True, text=True)
            line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else json.dumps({'error': p.stderr[-300:]})
            with open(os.path.join(HERE, f'C1-{k}.jsonl'), 'w') as f:
                f.write(json.dumps({'control': k, 'expect': EXPECT[k], 'variant_sha256':
                                    hashlib.sha256(text.encode()).hexdigest(), 'exit': p.returncode}) + '\n')
                f.write(line + '\n')
            res = json.loads(line)
            verdict = res.get('verdict')
            summary['results'][k] = {'expect': EXPECT[k], 'verdict': verdict, 'exit': p.returncode,
                                     'correct': res.get('correct'), 'wired_ok': res.get('wired_ok'),
                                     'live_agree': res.get('live_agree'), 'selftest_pass': res.get('selftest_pass'),
                                     'selftest_r44': res.get('selftest_r44')}
            print(k, json.dumps(summary['results'][k]), flush=True)
            if EXPECT[k] == 'FAIL' and verdict != 'FAIL':
                should_fail_accepted += 1
            if EXPECT[k] == 'PASS' and verdict != 'PASS':
                control_accepted = 0
        summary['should_fail_accepted'] = should_fail_accepted
        summary['control_accepted'] = control_accepted
        if not a.only:
            with open(os.path.join(HERE, 'battery-summary-c1.jsonl'), 'w') as f:
                f.write(json.dumps(summary, sort_keys=True) + '\n')
                f.write(json.dumps({'should_fail_accepted': should_fail_accepted,
                                    'control_accepted': control_accepted}) + '\n')
        print(json.dumps(summary, sort_keys=True))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
