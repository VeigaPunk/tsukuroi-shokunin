#!/usr/bin/env python3
"""Round-46 C2 pre-data battery: score scripted wave records with the frozen counter before any seat.
Each control is committed in its own scratch clone (git clone --shared, origin removed, toplevel checked, fixture
identity) on top of BASE; `tools/check-scrub-admission-r46.py --lane <clone> --revision HEAD` runs from the LANE
working copy. Expected verdicts are in EXPECT; K3, K15 and K18 PASS by design (K3 = the standing limit: committed
bytes cannot tell forged orchestrator records from real ones; K15 = the D5 proof that the binding survives any
wave name; K18 = the amendment path: partly on old bytes, residual holds on the amended bytes).
Usage: python3 run_controls_c2.py <scratch dir>   Writes C2-<control>.jsonl and battery-summary-c2.jsonl here."""
import concurrent.futures as cf
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '2042117cfb724170772f4c128cc2ddba0b61d817'
COUNTER = os.path.join(LANE, 'tools/check-scrub-admission-r46.py')
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
W = '.ufo/waves/round-46'
ENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_SYSTEM': os.devnull}
EXPECT = {'K0-donothing': 'FAIL', 'K1-marks-only': 'FAIL', 'K2-reports-no-dispatch': 'FAIL', 'K3-forged-all': 'PASS',
          'K4-partly-current': 'FAIL', 'K5-stale-hash': 'FAIL', 'K6-json-first-line': 'FAIL',
          'K7-preamble': 'FAIL', 'K8-fails-old-hash': 'FAIL', 'K9-outside-universe': 'FAIL',
          'K10-two-waves': 'FAIL', 'K11-wrong-agent': 'FAIL', 'K12-contradiction': 'FAIL',
          'K13-content-free': 'FAIL', 'K14-no-citation': 'FAIL', 'K15-any-wave-name': 'PASS',
          'K16-quote-broken': 'FAIL', 'K17-no-results': 'FAIL', 'K18-amend-residual': 'PASS',
          'K19-dup-key': 'FAIL', 'K20-cr-first-line': 'FAIL', 'K21-no-marks': 'FAIL'}
CITES = {'GR1': 'cmdline.c:156', 'GR2': 'dev-replace.c:701', 'GR3': 'systemd.kill.xml:114'}
BODY = ('\nEvidence. I re-read the row statement against the digest-checked snapshot lines it quotes; each quoted line '
        'is present verbatim at the cited line number and supports the clause that cites it. The host reading names '
        'capture lines that exist and say what the row says. No clause states more than its quoted lines decide; '
        'the inference marks sit where the pinned code stops. Citation: {cite}.\n')


def g(d, *args, inp=None):
    return subprocess.run(['git', '-C', d, *args], check=True, capture_output=True, input=inp,
                          env={**ENV, 'HOME': d}).stdout


def hashes(entry_text):
    lines = entry_text.split('\n')
    out = {}
    for row in ('GR1', 'GR2', 'GR3'):
        i = lines.index(f'## {row}')
        j = i + 1
        while j < len(lines) and not lines[j].startswith('## '):
            j += 1
        out[row] = hashlib.sha256('\n'.join(lines[i:j]).encode()).hexdigest()
    return out


def report(row, word, h, cite=True, body=True):
    b = BODY.format(cite=CITES[row] if cite else 'the snapshot') if body else '\nok\n'
    return f'ROW {row} VERDICT: {word}\nSECTION SHA256: {h}\n' + b


def counted(row):
    n = row[2:]
    return [(f'V46RevGR{n}a', 'reviewer'), (f'V46CritGR{n}a', 'critic')]


def build(d, control):
    """Write the control's files into clone d; return nothing (commit done by caller)."""
    p = os.path.join(d, ENTRY)
    entry = open(p, encoding='utf-8').read()
    if control == 'K16-quote-broken':
        entry = entry.replace('**Quote.** `S246` cmdline.c:192: "ret = ULLONG_MAX;"',
                              '**Quote.** `S246` cmdline.c:192: "ret = ULLONG_MAX + 1;"')
        open(p, 'w', encoding='utf-8').write(entry)
    if control == 'K18-amend-residual':
        old = hashes(entry)
        entry = entry.replace('[inference for the ioctl and btrfs-progs side:',
                              '[inference (amended) for the ioctl and btrfs-progs side:')
        open(p, 'w', encoding='utf-8').write(entry)
    h = hashes(entry)
    if control == 'K0-donothing':
        return
    marks = control != 'K21-no-marks'
    if marks:
        with open(p, 'a', encoding='utf-8') as fh:
            fh.write('\n## Gate status — round 46 (GR1-GR3 admitted)\n\nfixture\n')
        with open(os.path.join(d, 'SKILL.md'), 'a', encoding='utf-8') as fh:
            fh.write('\n## Scrub grounding — round 46 admission\n\nfixture\n')
        with open(os.path.join(d, 'corpus/README.md'), 'a', encoding='utf-8') as fh:
            fh.write('\n- `btrfs-scrub-grounding-r45.md` GR1-GR3 admitted round 46 (fixture)\n')
    if control == 'K1-marks-only':
        return
    wave = 'zz9' if control == 'K15-any-wave-name' else 'w1'
    seats = []  # (wave, name, role, row, text)
    for row in ('GR1', 'GR2', 'GR3'):
        for name, role in counted(row):
            seats.append([wave, name, role, row, report(row, 'holds', h[row])])
    if control == 'K4-partly-current':
        seats.append([wave, 'V46RevGR2b', 'reviewer', 'GR2', report('GR2', 'partly', h['GR2'])])
    if control == 'K5-stale-hash':
        for s in seats:
            if s[1].startswith('V46Crit'):
                s[4] = report(s[3], 'holds', '0' * 64)
    if control == 'K6-json-first-line':
        seats[0][4] = json.dumps({'verdict_line': 'ROW GR1 VERDICT: holds'}) + '\n' + seats[0][4]
    if control == 'K7-preamble':
        seats[0][4] = 'Report written.\n' + seats[0][4]
    if control == 'K8-fails-old-hash':
        seats.append([wave, 'V46RevGR1b', 'reviewer', 'GR1', report('GR1', 'fails', 'f' * 64)])
    if control == 'K9-outside-universe':
        seats[0][1] = 'V46RevGR1c'
    if control == 'K11-wrong-agent':
        seats[0][2] = 'executor'
    if control == 'K12-contradiction':
        seats[0][4] += 'On reflection: ROW GR1 VERDICT: partly\n'
    if control == 'K13-content-free':
        seats[0][4] = report('GR1', 'holds', h['GR1'], body=False)
    if control == 'K14-no-citation':
        seats[0][4] = report('GR1', 'holds', h['GR1'], cite=False)
    if control == 'K20-cr-first-line':
        seats[0][4] = seats[0][4].replace('VERDICT: holds\n', 'VERDICT: holds\r\n', 1)
    if control == 'K18-amend-residual':
        for s in seats:
            if s[3] == 'GR2':
                s[4] = report('GR2', 'partly', old['GR2'])
        seats.append(['r1', 'V46ResRevGR2', 'reviewer', 'GR2', report('GR2', 'holds', h['GR2'])])
        seats.append(['r1', 'V46ResCritGR2', 'critic', 'GR2', report('GR2', 'holds', h['GR2'])])
    waves = {}
    for wv, name, role, row, text in seats:
        waves.setdefault(wv, []).append((name, role))
        os.makedirs(os.path.join(d, W, wv), exist_ok=True)
        open(os.path.join(d, W, wv, f'{name}.md'), 'w', encoding='utf-8', newline='').write(text)
    if control == 'K10-two-waves':
        waves.setdefault('w2', []).append(('V46RevGR1a', 'reviewer'))
    if control == 'K2-reports-no-dispatch':
        return
    for wv, lst in waves.items():
        disp = {'taskCall': {'context': 'fixture', 'tasks': [{'name': n, 'agent': r, 'task': 'x'} for n, r in lst]}}
        dtext = json.dumps(disp)
        if control == 'K19-dup-key' and wv == 'w1':
            dtext = dtext[:-1] + ', "taskCall": {"tasks": []}}'
        open(os.path.join(d, W, f'{wv}-dispatch.json'), 'w').write(dtext)
        if control == 'K17-no-results':
            continue
        res = {'lane': 'tsukuroi', 'round': 46, 'wave': wv,
               'results': [{'name': n, 'agent': r, 'status': 'completed', 'output': None} for n, r in lst]}
        open(os.path.join(d, W, f'{wv}-results.json'), 'w').write(json.dumps(res))


def one(scratch, control):
    root = os.path.join(scratch, control)
    shutil.rmtree(root, ignore_errors=True)
    d = os.path.join(root, 'clone')
    os.makedirs(root)
    subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', LANE, d], check=True,
                   env={**ENV, 'HOME': root})
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    g(d, 'remote', 'remove', 'origin')
    g(d, 'checkout', '-q', '--detach', BASE)
    build(d, control)
    if control != 'K0-donothing':
        g(d, 'add', '-A')
        g(d, '-c', 'user.name=r46-control', '-c', 'user.email=r46-control@fixture.invalid', 'commit', '-q', '-m',
          f'r46 C2 control {control}')
    p = subprocess.run([sys.executable, COUNTER, '--lane', d, '--revision', 'HEAD'], capture_output=True, text=True,
                       env={**ENV, 'HOME': root})
    out = p.stdout.strip()
    open(os.path.join(HERE, f'C2-{control}.jsonl'), 'w').write(out + '\n')
    try:
        r = json.loads(out)
    except ValueError:
        r = {'verdict': 'ERROR', 'stderr': p.stderr[-400:]}
    shutil.rmtree(root, ignore_errors=True)
    return {'control': control, 'expect': EXPECT[control], 'verdict': r.get('verdict'), 'exit_code': p.returncode,
            'as_expected': r.get('verdict') == EXPECT[control], 'r45_legs_ok': r.get('r45_legs_ok'),
            'verdicts_ok': r.get('verdicts_ok'), 'marks_ok': r.get('marks_ok'),
            'rows_ok': {k: v.get('row_ok') for k, v in (r.get('per_row') or {}).items()}}


def main():
    scratch = os.path.abspath(sys.argv[1])
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        rows = list(ex.map(lambda c: one(scratch, c), list(EXPECT)))
    with open(os.path.join(HERE, 'battery-summary-c2.jsonl'), 'w') as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + '\n')
            print(json.dumps(r, sort_keys=True))
    return 0 if all(r['as_expected'] for r in rows) else 1


if __name__ == '__main__':
    sys.exit(main())
