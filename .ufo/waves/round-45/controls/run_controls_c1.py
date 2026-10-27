#!/usr/bin/env python3
"""Round-45 C1 pre-data control battery for tools/score-census-readers-r45.py (scored before any seat).

Each control is a commit in its own scratch clone of the lane (`git clone --shared`, origin removed, toplevel
asserted) on top of BASE, carrying a variant of the candidate census `c1-candidate/tools/tsukuroi-census.sh` and,
except K0, the candidate anchor registry `c1-candidate/corpus/knowledge/adjacency-anchors-r19.json` (IN-109
repinned). `refs/remotes/origin/master` is pointed at the control commit so the adjacency leg's revision binding
holds. The frozen counter (lane working file) scores it with `--lane <clone> --scratch <dir>`.

  K0  do-nothing: BASE                                                                         must FAIL
  K1  `| head -1` evasion at the five sites (still an early reader) + the candidate cases     must FAIL
  K2  constant writer: each site assigns a constant (running/success/610.57.04/active/active) must FAIL
  K3  candidate conversions without the six R45-C1 selftest cases                              must FAIL
  K4  candidate cases with the base early-reader sites                                         must FAIL
  K5  S5 conversion without the trailing-blank strip                                           must FAIL
  K6  vacuous cases: `r45pad` prints nothing (no output past the pipe buffer)                  must FAIL
  K7  candidate + one comment line above the IN-109 selftest case (unrepinned anchor drift)    must FAIL
  K10 fixture-gated: each site uses the new form only when TSUKUROI_FIXTURE is set (QUALITY 90) must FAIL
  K8  candidate                                                                                control (PASS)
  K9  alternative full read: `| sed -n 1p |` in place of `| head -n1 |` + the candidate cases control (PASS)

Usage: python3 run_controls_c1.py --scratch <DIR> [--jobs N]   Writes C1-K*.jsonl, battery-summary-c1.jsonl here.
"""
import argparse
import concurrent.futures as cf
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
BASE = '5bbd5ff588120fd8e7c744695351a6978b4241c1'
COUNTER = os.path.join(LANE, 'tools/score-census-readers-r45.py')
CEN = 'tools/tsukuroi-census.sh'
ANC = 'corpus/knowledge/adjacency-anchors-r19.json'
CAND = os.path.join(HERE, 'c1-candidate')
IN109 = "check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED"
SITES = [  # (variable, start marker in the candidate line, base line, constant)
    ('state', "  state=${CAP_OUT%%$'\\n'*};",
     "  state=$(printf '%s\\n' \"$CAP_OUT\" | head -n1 | tr -d '\\r' | sed -E 's/[[:space:]]+$//')", 'running'),
    ('r', "    r=${CAP_OUT%%$'\\n'*}; r=${r//$'\\r'/}   #",
     "    r=$(printf '%s\\n' \"$CAP_OUT\" | head -n1 | tr -d '\\r')", 'success'),
    ('driver', "      driver=${CAP_OUT%%$'\\n'*};",
     "      driver=$(printf '%s\\n' \"$CAP_OUT\" | head -n1 | awk -F', *' '{print $NF}')", '610.57.04'),
    ('t_word', "    t_word=${CAP_OUT%%$'\\n'*};",
     "    t_word=$(printf '%s\\n' \"$CAP_OUT\" | head -n1 | tr -d '\\r' | sed -E 's/[[:space:]]+$//')", 'active'),
    ('r', "    r=${CAP_OUT%%$'\\n'*}; r=${r//$'\\r'/}; r=${r%",
     "    r=$(printf '%s\\n' \"$CAP_OUT\" | head -n1 | tr -d '\\r' | sed -E 's/[[:space:]]+$//')", 'active'),
]


def site_index(lines, marker):
    idx = [i for i, ln in enumerate(lines) if ln.startswith(marker)]
    assert len(idx) == 1, (marker, idx)
    return idx[0]


def variant(cand, fn):
    lines = cand.split('\n')
    for k, (var, marker, base_line, const) in enumerate(SITES):
        i = site_index(cand.split('\n'), marker)
        lines[i] = fn(k, var, lines[i], base_line, const)
    return '\n'.join(lines)


def strip_cases(cand):
    a = cand.index('  # Round 45 (C1; routed since round 42')
    b = cand.index("  check_cli 'cli: unknown argument exits 2 with usage (S10-2)'")
    return cand[:a] + cand[b:]


def build(cand):
    v = {'K0': None, 'K8': cand}
    v['K1'] = variant(cand, lambda k, var, ln, bl, c: bl.replace('| head -n1 |', '| head -1 |'))
    v['K2'] = variant(cand, lambda k, var, ln, bl, c: re.match(r'^\s*', ln).group(0) + f'{var}={c}')
    v['K3'] = strip_cases(cand)
    v['K4'] = variant(cand, lambda k, var, ln, bl, c: bl)
    k5 = cand.split('\n')
    i = site_index(k5, SITES[4][1])
    k5[i] = "    r=${CAP_OUT%%$'\\n'*}; r=${r//$'\\r'/}   # first line, no early reader (R45-C1)"
    v['K5'] = '\n'.join(k5)
    old = "  r45pad() { awk -v t=\"$1\""
    assert cand.count(old) == 1
    k6 = cand.split('\n')
    j = next(n for n, ln in enumerate(k6) if ln.startswith(old))
    k6[j] = '  r45pad() { :; }'
    v['K6'] = '\n'.join(k6)
    k7 = cand.split('\n')
    j = next(n for n, ln in enumerate(k7) if IN109 in ln)
    k7.insert(j, '  # round-45 control K7: one inserted line moves every later census line by one')
    v['K7'] = '\n'.join(k7)
    v['K9'] = variant(cand, lambda k, var, ln, bl, c: bl.replace('| head -n1 |', '| sed -n 1p |'))
    v['K10'] = variant(cand, lambda k, var, ln, bl, c: (
        re.match(r'^\s*', ln).group(0) + f"{var}=''; if [ -n \"${{TSUKUROI_FIXTURE:-}}\" ]; then "
        + ln.strip().split('   #', 1)[0] + '; else ' + bl.strip() + '; fi'))
    return v


def run_one(k, census, anchors, scratch):
    work = tempfile.mkdtemp(prefix=f'c1-{k}.', dir=scratch)
    try:
        d = os.path.join(work, 'clone')
        subprocess.run(['git', 'clone', '-q', '--shared', LANE, d], check=True)
        subprocess.run(['git', '-C', d, 'remote', 'remove', 'origin'], check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True,
                             text=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d), top
        subprocess.run(['git', '-C', d, 'checkout', '-q', '--detach', '-f', BASE], check=True)
        if census is not None:
            with open(os.path.join(d, CEN), 'w') as fh:
                fh.write(census)
            with open(os.path.join(d, ANC), 'wb') as fh:
                fh.write(anchors)
            subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
        subprocess.run(['git', '-C', d, '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
                        'commit', '-q', '--allow-empty', '-m', f'control {k}'], check=True)
        sha = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        subprocess.run(['git', '-C', d, 'update-ref', 'refs/remotes/origin/master', sha], check=True)
        subprocess.run(['git', '-C', d, 'update-ref', 'refs/heads/master', sha], check=True)
        env = dict(os.environ, TMPDIR=os.path.join(work, 'tmp'))
        os.makedirs(env['TMPDIR'])
        p = subprocess.run(['python3', COUNTER, '--lane', d, '--revision', sha, '--scratch', os.path.join(work, 's')],
                           capture_output=True, text=True, env=env, stdin=subprocess.DEVNULL, timeout=3600)
        line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else json.dumps({'error': p.stderr[-300:]})
        return k, p.returncode, line
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--jobs', type=int, default=3)
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    cand = open(os.path.join(CAND, CEN)).read()
    anchors = open(os.path.join(CAND, ANC), 'rb').read()
    v = build(cand)
    expect = {k: ('PASS' if k in ('K8', 'K9') else 'FAIL') for k in v}
    counter_src = open(COUNTER, 'rb').read()
    summary = {'counter_sha256': hashlib.sha256(counter_src).hexdigest(), 'base': BASE,
               'candidate_sha256': {CEN: hashlib.sha256(cand.encode()).hexdigest(),
                                    ANC: hashlib.sha256(anchors).hexdigest()},
               'variant_sha256': {k: (hashlib.sha256(c.encode()).hexdigest() if c else None) for k, c in v.items()},
               'results': {}}
    sfa, ca = 0, 1
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(run_one, k, c, anchors, a.scratch) for k, c in v.items()]
        for f in cf.as_completed(futs):
            k, rc, line = f.result()
            res = json.loads(line)
            res.setdefault('verdict', 'FAIL')
            with open(os.path.join(HERE, f'C1-{k}.jsonl'), 'w') as fh:
                fh.write(json.dumps({'control': k, 'expect': expect[k], 'exit': rc}) + '\n')
                fh.write(line + '\n')
            summary['results'][k] = {kk: res.get(kk) for kk in (
                'verdict', 'lexical_hits', 'sites_found', 'equiv_ok', 'selftest_pass', 'selftest_line', 'selftest_r45',
                'revert_killed', 'adjacency_ok', 'error')}
            summary['results'][k]['exit'] = rc
            print(k, expect[k], json.dumps(summary['results'][k]), flush=True)
            if expect[k] == 'FAIL' and res.get('verdict') != 'FAIL':
                sfa += 1
            if expect[k] == 'PASS' and res.get('verdict') != 'PASS':
                ca = 0
    summary['should_fail_accepted'] = sfa
    summary['control_accepted'] = ca
    with open(os.path.join(HERE, 'battery-summary-c1.jsonl'), 'w') as fh:
        fh.write(json.dumps(summary, sort_keys=True) + '\n')
        fh.write(json.dumps({'should_fail_accepted': sfa, 'control_accepted': ca}) + '\n')
    print(json.dumps({'should_fail_accepted': sfa, 'control_accepted': ca}))


if __name__ == '__main__':
    sys.exit(main())
