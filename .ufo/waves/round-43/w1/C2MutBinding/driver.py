#!/usr/bin/env python3
"""C2MutBinding — binding-attack battery for tools/check-scrub-record-r43.py (seat item C2-7).

Builds a golden forged fixture (the declared C2-K3 shape) in a scratch clone of the lane, then scores the
seven declared binding attacks (a)-(g) plus extra probes, one fixture commit each, scored by the frozen lane
counter run from its lane path with --sessions pointed at a nonexistent dir (hermetic, transcripts_bound 0).
Writes receipts only under .ufo/waves/round-43/w1/C2MutBinding/. Scratch work dir removed in finally.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER = os.path.join(LANE, 'tools/check-scrub-record-r43.py')
CAND = os.path.join(LANE, '.ufo/waves/round-43/controls/c2-candidate')
SEAT = 'C2MutBinding'
SCRATCH = '/fast/scratch/hyaku/tsukuroi-r43/' + SEAT
RECEIPTS = os.path.join(LANE, '.ufo/waves/round-43/w1', SEAT)
BASE = '6951ead90566b2d74f7c45b4efca29246badad64'
WAVE = '.ufo/waves/round-43'
ROWS = ['SR1', 'SR3', 'SR6']
SEATS = [(f'C2{k}SR{r[2:]}', role, r) for r in ROWS for k, role in (('Rev', 'reviewer'), ('Crit', 'critic'))]
FILES = ['corpus/knowledge/btrfs-scrub-record-r43.md', 'corpus/knowledge/btrfs-scrub-record-r42.md',
         'corpus/SOURCES.md', '.ufo/waves/round-43/frozen/src/ioctl.c',
         '.ufo/waves/round-43/frozen/hostcap/capture.txt']
HOLDS1 = 'ROW SR1 VERDICT: holds'


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def vline(row, v='holds'):
    return f'ROW {row} VERDICT: {v}'


def surface():
    out = {}
    for f in FILES:
        p = os.path.join(CAND, f)
        out[f] = open(p, 'rb').read() if f.endswith('ioctl.c') else open(p, encoding='utf-8', newline='').read()
    return out


def base_tasks():
    return [{'name': n, 'agent': role, 'task': 'forged'} for n, role, _ in SEATS]


def base_results(agent_over=None):
    ents = []
    for n, role, row in SEATS:
        a = (agent_over or {}).get(n, role)
        ents.append({'name': n, 'agent': a,
                     'output': json.dumps({'verdict_line': vline(row), 'row': row, 'seat': n})})
    return ents


def golden(seat_out=None, seat_report=None, tasks=None, results=None):
    files = {}
    files[f'{WAVE}/w2-dispatch.json'] = json.dumps({'taskCall': {'context': 'forged',
                                                                'tasks': tasks if tasks is not None else base_tasks()}})
    ents = results if results is not None else base_results()
    if seat_out:
        for e in ents:
            if e['name'] in seat_out:
                e['output'] = seat_out[e['name']]
    files[f'{WAVE}/w2-results.json'] = json.dumps({'results': ents})
    for n, role, row in SEATS:
        line = vline(row)
        rep = line + '\n\nforged report body\n'
        if seat_report and n in seat_report:
            rep = seat_report[n]
        files[f'{WAVE}/w2/{n}.md'] = rep
    return files


def mk(seat_out=None, seat_report=None, tasks=None, results=None, extra=None):
    s = surface()
    s.update(golden(seat_out, seat_report, tasks, results))
    if extra:
        s.update(extra)
    return s


def variants():
    vs = []
    vs.append(('GOLD', 'K3-equivalent golden forged fixture (baseline)', 'PASS', lambda: mk()))
    # (a) JSON object output: verdict_line holds, sibling 'verdict': 'fails'
    vs.append(('A', "(a) SR1 rev output JSON {'verdict_line': holds, 'verdict': 'fails'}", 'PASS',
               lambda: mk(seat_out={'C2RevSR1': json.dumps({'verdict_line': HOLDS1, 'verdict': 'fails'})})))
    # (b) output is a JSON list
    vs.append(('B', '(b) SR1 rev output is a JSON list', 'FAIL',
               lambda: mk(seat_out={'C2RevSR1': json.dumps([{'verdict_line': HOLDS1}])})))
    # (c) text output: first line the holds line, later line the fails line
    vs.append(('C', '(c) SR1 rev output: first line holds, later line "ROW SR1 VERDICT: fails"', 'PASS',
               lambda: mk(seat_out={'C2RevSR1': HOLDS1 + '\nROW SR1 VERDICT: fails\n'})))
    # (d1) report first line with trailing spaces
    vs.append(('D1', '(d1) SR1 rev report first line with trailing spaces', 'FAIL',
               lambda: mk(seat_report={'C2RevSR1': HOLDS1 + '   \n\nforged report body\n'})))
    # (d2) report with CRLF line endings
    vs.append(('D2', '(d2) SR1 rev report with CRLF line endings', 'PASS',
               lambda: mk(seat_report={'C2RevSR1': HOLDS1 + '\r\n\r\nforged report body\r\n'})))
    # (e1) two dispatch tasks of the same name AND role
    t_e1 = base_tasks() + [{'name': 'C2RevSR1', 'agent': 'reviewer', 'task': 'forged-dup'}]
    vs.append(('E1', '(e1) dispatch has C2RevSR1/reviewer twice', 'FAIL', lambda: mk(tasks=t_e1)))
    # (e2) two dispatch tasks of the same name, different roles
    t_e2 = base_tasks() + [{'name': 'C2RevSR1', 'agent': 'critic', 'task': 'forged-extra'}]
    vs.append(('E2', '(e2) dispatch adds a second C2RevSR1 task as critic (same name, other role)', 'PASS',
               lambda: mk(tasks=t_e2)))
    # (f1) results entry agent differs from dispatch agent
    r_f1 = base_results()
    for e in r_f1:
        if e['name'] == 'C2RevSR1':
            e['agent'] = 'critic'
    vs.append(('F1', "(f1) SR1 rev results entry has agent 'critic' (dispatch says reviewer)", 'FAIL',
               lambda: mk(results=r_f1)))
    # (f2) dispatch and results both say a different agent
    t_f2 = base_tasks()
    for t in t_f2:
        if t['name'] == 'C2RevSR1':
            t['agent'] = 'executor'
    r_f2 = base_results(agent_over={'C2RevSR1': 'executor'})
    vs.append(('F2', "(f2) SR1 rev dispatch+results both agent 'executor'", 'FAIL',
               lambda: mk(tasks=t_f2, results=r_f2)))
    # (g1) verdict line for the wrong row
    vs.append(('G1', '(g1) SR1 rev verdict line names SR3', 'FAIL',
               lambda: mk(seat_out={'C2RevSR1': json.dumps({'verdict_line': vline('SR3')})},
                          seat_report={'C2RevSR1': vline('SR3') + '\n\nforged report body\n'})))
    # (g2) cross-wired rows between the two reviewers
    so = {'C2RevSR1': json.dumps({'verdict_line': vline('SR3')}),
          'C2RevSR3': json.dumps({'verdict_line': HOLDS1})}
    sr = {'C2RevSR1': vline('SR3') + '\n\nforged report body\n',
          'C2RevSR3': HOLDS1 + '\n\nforged report body\n'}
    vs.append(('G2', '(g2) SR1 and SR3 reviewers cross-wired (each binds the other row)', 'FAIL',
               lambda: mk(seat_out=so, seat_report=sr)))
    # (h) results output line with leading+trailing whitespace (text path strips before the exactness test)
    vs.append(('H', "(h) SR1 rev output '  ROW SR1 VERDICT: holds  '", 'PASS',
               lambda: mk(seat_out={'C2RevSR1': '  ' + HOLDS1 + '  \n'})))
    # (i) report opens with blank lines before the verdict line
    vs.append(('I', '(i) SR1 rev report opens with two blank lines, verdict line third', 'PASS',
               lambda: mk(seat_report={'C2RevSR1': '\n\n' + HOLDS1 + '\n\nforged report body\n'})))
    # (j1) w2-results.json is a top-level JSON list
    r_j1 = [{'name': n, 'agent': role, 'output': json.dumps({'verdict_line': vline(row)})}
            for n, role, row in SEATS]
    vs.append(('J1', '(j1) w2-results.json is a top-level JSON list', 'CRASH',
               lambda: mk(extra={f'{WAVE}/w2-results.json': json.dumps(r_j1)})))
    # (j2) w2-dispatch.json is a top-level JSON list
    d_j2 = [{'name': n, 'agent': role, 'task': 'forged'} for n, role, _ in SEATS]
    vs.append(('J2', '(j2) w2-dispatch.json is a top-level JSON list', 'CRASH',
               lambda: mk(extra={f'{WAVE}/w2-dispatch.json': json.dumps(d_j2)})))
    # (k) duplicate verdict_line keys: fails first, holds last
    vs.append(('K', '(k) SR1 rev output JSON with duplicate verdict_line keys (fails then holds)', 'PASS',
               lambda: mk(seat_out={'C2RevSR1': '{"verdict_line": "ROW SR1 VERDICT: fails", '
                                                '"verdict_line": "ROW SR1 VERDICT: holds"}'})))
    # (l) two results entries of the same name+role
    r_l = base_results() + [dict(base_results()[0])]
    vs.append(('L', '(l) results has the C2RevSR1/reviewer entry twice', 'FAIL', lambda: mk(results=r_l)))
    # (m) SR1 critic partly + forged residual reviewer holds
    def mk_m():
        s = surface()
        recs = golden(seat_out={'C2CritSR1': json.dumps({'verdict_line': vline('SR1', 'partly'),
                                                        'row': 'SR1', 'seat': 'C2CritSR1'})},
                      seat_report={'C2CritSR1': vline('SR1', 'partly') + '\n\nforged report body\n'})
        recs[f'{WAVE}/residual-dispatch.json'] = json.dumps(
            {'taskCall': {'context': 'forged',
                          'tasks': [{'name': 'C2ResSR1', 'agent': 'reviewer', 'task': 'forged'}]}})
        recs[f'{WAVE}/residual-results.json'] = json.dumps(
            {'results': [{'name': 'C2ResSR1', 'agent': 'reviewer',
                          'output': json.dumps({'verdict_line': HOLDS1})}]})
        recs[f'{WAVE}/residual/C2ResSR1.md'] = HOLDS1 + '\n\nforged residual body\n'
        s.update(recs)
        return s
    vs.append(('M', '(m) SR1 critic partly + forged residual C2ResSR1 holds', 'PASS', mk_m))
    # (n) report starts with a UTF-8 BOM
    vs.append(('N', '(n) SR1 rev report starts with a UTF-8 BOM', 'FAIL',
               lambda: mk(seat_report={'C2RevSR1': '﻿' + HOLDS1 + '\n\nforged report body\n'})))
    # (o) output JSON preceded by a UTF-8 BOM
    vs.append(('O', '(o) SR1 rev output JSON preceded by a UTF-8 BOM', 'FAIL',
               lambda: mk(seat_out={'C2RevSR1': '﻿' + json.dumps({'verdict_line': HOLDS1})})))
    # (q) JSON verdict_line with a trailing space inside the string (JSON path does not strip)
    vs.append(('Q', "(q) SR1 rev output JSON verdict_line 'ROW SR1 VERDICT: holds ' (trailing space)", 'FAIL',
               lambda: mk(seat_out={'C2RevSR1': json.dumps({'verdict_line': HOLDS1 + ' '})})))
    return vs


def main():
    os.makedirs(RECEIPTS, exist_ok=True)
    counter_sha = hashlib.sha256(open(COUNTER, 'rb').read()).hexdigest()
    work = tempfile.mkdtemp(prefix='c2mutbind.', dir=SCRATCH)
    summary = {'seat': SEAT, 'counter': COUNTER, 'counter_sha256': counter_sha, 'base': BASE, 'variants': {}}
    try:
        d = os.path.join(work, 'clone')
        cp = sh('git', 'clone', '-q', '--shared', LANE, d)
        assert cp.returncode == 0, cp.stderr
        assert sh('git', '-C', d, 'remote', 'remove', 'origin').returncode == 0
        top = sh('git', '-C', d, 'rev-parse', '--show-toplevel').stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d), top
        sessions = os.path.join(work, 'no-sessions')
        gold_files = None
        for vid, attack, expect, fn in variants():
            files = fn()
            if gold_files is not None:
                assert files != gold_files, f'{vid} does not differ from GOLD'
            if vid == 'GOLD':
                gold_files = files
            sh('git', '-C', d, 'checkout', '-q', '--detach', '-f', BASE)
            sh('git', '-C', d, 'clean', '-qfdx')
            top = sh('git', '-C', d, 'rev-parse', '--show-toplevel').stdout.strip()
            assert os.path.realpath(top) == os.path.realpath(d), top
            for f, c in files.items():
                p = os.path.join(d, f)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, 'wb') as fh:
                    fh.write(c if isinstance(c, bytes) else c.encode())
            assert sh('git', '-C', d, 'add', '-A').returncode == 0
            cp = sh('git', '-C', d, '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
                    'commit', '-q', '--allow-empty', '-m', f'binding variant {vid}')
            assert cp.returncode == 0, cp.stderr
            sha = sh('git', '-C', d, 'rev-parse', 'HEAD').stdout.strip()
            p = subprocess.run([sys.executable, COUNTER, '--lane', d, '--revision', sha,
                                '--sessions', sessions], capture_output=True, text=True)
            out = p.stdout.strip()
            if out:
                res = json.loads(out.splitlines()[-1])
                verdict = res.get('verdict')
                vok = res.get('verdicts_ok')
                pr = {r: res['per_row'].get(r, {}).get('verdicts') for r in ROWS}
            else:
                res, verdict, vok, pr = None, 'NO-JSON', None, None
            cls = 'CRASH' if res is None else verdict
            hit = (expect == cls) or (expect == 'PASS' and cls == 'PASS') or (expect in ('FAIL', 'CRASH') and cls in ('FAIL', 'NO-JSON'))
            with open(os.path.join(RECEIPTS, f'{vid}.jsonl'), 'w') as fh:
                fh.write(json.dumps({'variant': vid, 'attack': attack, 'expect': expect, 'classified': cls,
                                     'match': hit, 'fixture_sha': sha, 'exit': p.returncode,
                                     'counter_sha256': counter_sha}) + '\n')
                fh.write((out if out else json.dumps({'error': p.stderr[-400:]})) + '\n')
            summary['variants'][vid] = {'attack': attack, 'expect': expect, 'classified': cls, 'match': hit,
                                        'verdicts_ok': vok, 'per_row_verdicts': pr, 'fixture_sha': sha,
                                        'exit': p.returncode}
            print(f"{vid:5s} expect={expect:5s} observed={cls:7s} verdicts_ok={vok} sr1={pr and pr['SR1']}")
        ok = all(v['match'] for v in summary['variants'].values())
        summary['all_matched_expectations'] = ok
        with open(os.path.join(RECEIPTS, 'summary.jsonl'), 'w') as fh:
            fh.write(json.dumps(summary, sort_keys=True) + '\n')
        print('ALL-MATCHED' if ok else 'MISMATCH-PRESENT')
        print('counter_sha256', counter_sha)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
