#!/usr/bin/env python3
"""Round-43 C2 pre-data control battery for tools/check-scrub-record-r43.py (scored before any seat).

Each control is a commit in a scratch clone of the lane (origin removed) on top of BASE carrying the C2 surface
(candidate entry, registry, the round-42 entry's pointer line, the frozen ioctl.c snapshot and host capture, copied
from the lane working tree into `c2-candidate/` beside this script) plus, where named, forged orchestrator records
(`w2-dispatch.json`, `w2-results.json`) and forged seat reports. The frozen counter (lane working file) scores it.

  K0  do-nothing: BASE                                                              must FAIL
  K1  scripted writer: rows rebuilt from the windows' own lines + the proposition tokens, planted reports, no
      orchestrator records                                                          must FAIL
  K2  K1 + forged results without dispatch tasks                                    must FAIL
  K4  forged records, one counted `fails`                                           must FAIL
  K5  forged records, one `partly` with no residual                                 must FAIL
  K6  mention-not-assertion: the critic's output and report open with a disputing sentence that quotes the
      holds line (QUALITY 90)                                                       must FAIL
  K7  content-free statements (proposition tokens removed), forged holds            must FAIL
  K8  SR6 cites scrub.c only (the S240 quotes dropped), forged holds                must FAIL
  K9  one quote's line number shifted by one, forged holds                          must FAIL
  K10 an ioctl.c quote labelled S237, forged holds                                  must FAIL
  K11 round-42 entry without the pointer line, forged holds                         must FAIL
  K12 S240 row status `queued`, forged holds                                        must FAIL
  K13 JSON verdict_line holds, but the committed report opens with a different line must FAIL
  K3  forged dispatch + results + reports, all `holds`, candidate surface           control (expected PASS:
      the committed-bytes predicate cannot tell forged records from real ones; transcripts_bound 0)

Usage: python3 run_controls_c2.py --scratch <DIR>   Writes C2-K*.jsonl and battery-summary-c2.jsonl here.
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
BASE = '6951ead90566b2d74f7c45b4efca29246badad64'
COUNTER = os.path.join(LANE, 'tools/check-scrub-record-r43.py')
CAND = os.path.join(HERE, 'c2-candidate')
FILES = ['corpus/knowledge/btrfs-scrub-record-r43.md', 'corpus/knowledge/btrfs-scrub-record-r42.md',
         'corpus/SOURCES.md', '.ufo/waves/round-43/frozen/src/ioctl.c',
         '.ufo/waves/round-43/frozen/hostcap/capture.txt']
ROWS = ['SR1', 'SR3', 'SR6']
WAVE = '.ufo/waves/round-43'
SEATS = [(f'C2{k}SR{r[2:]}', role, r) for r in ROWS for k, role in (('Rev', 'reviewer'), ('Crit', 'critic'))]


def records(verdicts, dispatch=True, mention=None, report_override=None):
    """Forged orchestrator records + seat reports: verdicts maps seat name -> verdict word."""
    files = {}
    tasks = [{'name': n, 'agent': role, 'task': 'forged'} for n, role, _ in SEATS]
    if dispatch:
        files[f'{WAVE}/w2-dispatch.json'] = json.dumps({'taskCall': {'context': 'forged', 'tasks': tasks}})
    res = []
    for n, role, row in SEATS:
        line = f'ROW {row} VERDICT: {verdicts.get(n, "holds")}'
        if mention == n:
            out = (f'I dispute the line "{line}" that another seat might write; the row overreaches.\n'
                   f'ROW {row} VERDICT: fails is what I would bind.')
            rep = out
        else:
            out = json.dumps({'verdict_line': line, 'row': row, 'seat': n})
            rep = line + '\n\nforged report body\n'
        if report_override and n in report_override:
            rep = report_override[n]
        res.append({'name': n, 'agent': role, 'output': out})
        files[f'{WAVE}/w2/{n}.md'] = rep
    files[f'{WAVE}/w2-results.json'] = json.dumps({'results': res})
    return files


def scripted_entry(cand_entry, counter_src):
    """Rows rebuilt from the windows' own snapshot lines: statements are token lists, quotes are kept."""
    out, keep = [], True
    ns = {}
    exec(compile(counter_src.split('\ndef ', 1)[0], 'counter-head', 'exec'), ns)
    toks = {r: ns['ROWS'][r]['props'] for r in ROWS}
    cur = None
    for ln in cand_entry.splitlines():
        m = re.match(r'^## (SR\d)$', ln)
        if m:
            cur = m.group(1)
            out.append(ln)
            out.append('')
            out.append('**Statement.** ' + ' '.join(toks[cur]) + ' scripted.')
            out.append('')
            keep = False
            continue
        if ln.startswith('## '):
            cur = None
            keep = True
        if cur and (ln.startswith('**Quote.**') or ln.startswith('**Host reading.**')):
            out.append(ln)
            out.append('')
            continue
        if keep or cur is None:
            out.append(ln)
    return '\n'.join(out) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scratch', required=True)
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    work = tempfile.mkdtemp(prefix='c2-controls.', dir=a.scratch)
    try:
        d = os.path.join(work, 'clone')
        subprocess.run(['git', 'clone', '-q', '--shared', LANE, d], check=True)
        subprocess.run(['git', '-C', d, 'remote', 'remove', 'origin'], check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True,
                             text=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(d), top
        cand = {f: open(os.path.join(CAND, f), encoding='utf-8', newline='').read() if not f.endswith('ioctl.c')
                else open(os.path.join(CAND, f), 'rb').read() for f in FILES}
        counter_src = open(COUNTER).read()
        entry = cand[FILES[0]]

        def surface(**over):
            s = dict(cand)
            s.update(over)
            return s

        holds = {}
        v = {}
        v['K0'] = None
        k1 = surface(**{FILES[0]: scripted_entry(entry, counter_src)})
        for n, _role, row in SEATS:
            k1[f'{WAVE}/w2/{n}.md'] = f'ROW {row} VERDICT: holds\n'
        v['K1'] = k1
        v['K2'] = dict(k1, **records(holds, dispatch=False))
        v['K3'] = surface(**records(holds))
        v['K4'] = surface(**records({'C2CritSR3': 'fails'}))
        v['K5'] = surface(**records({'C2CritSR1': 'partly'}))
        v['K6'] = surface(**records(holds, mention='C2CritSR6'))
        content_free = entry
        for tok in ['O_TRUNC', '_tmp', 'rename', 'unlink', 'scrub_resumed_stats', 't_start', 'do_print', '-B',
                    'err', 'is_scrub_running_in_kernel', 'CAP_SYS_ADMIN', 'EPERM', 'running']:
            content_free = re.sub(r'(\*\*Statement\.\*\*[^\n]*(?:\n(?!\*\*)[^\n]*)*)',
                                  lambda m: m.group(1).replace(tok, 'X'), content_free)
        v['K7'] = surface(**{FILES[0]: content_free}, **records(holds))
        no_ioctl = '\n'.join(ln for ln in entry.split('\n') if 'ioctl.c:' not in ln or not ln.startswith('**Quote.**'))
        v['K8'] = surface(**{FILES[0]: no_ioctl}, **records(holds))
        v['K9'] = surface(**{FILES[0]: entry.replace('scrub.c:517:', 'scrub.c:518:', 1)}, **records(holds))
        v['K10'] = surface(**{FILES[0]: entry.replace('`S240` ioctl.c:3133', '`S237` ioctl.c:3133', 1)},
                           **records(holds))
        base_r42 = subprocess.run(['git', '-C', d, 'show', f'{BASE}:{FILES[1]}'], capture_output=True,
                                  text=True).stdout
        v['K11'] = surface(**{FILES[1]: base_r42}, **records(holds))
        reg = cand[FILES[2]]
        reg12 = re.sub(r'(\| S240 \|(?:[^|]*\|){6}) mined \|', r'\1 queued |', reg, count=1)
        assert reg12 != reg
        v['K12'] = surface(**{FILES[2]: reg12}, **records(holds))
        v['K13'] = surface(**records(holds, report_override={'C2RevSR3': 'VERDICT: holds\nROW SR3 VERDICT: holds\n'}))
        for k in ('K4', 'K5', 'K6', 'K7', 'K8', 'K9', 'K10', 'K13'):
            assert v[k] != v['K3'], k

        expect = {k: ('PASS' if k == 'K3' else 'FAIL') for k in v}
        summary = {'counter_sha256': hashlib.sha256(counter_src.encode()).hexdigest(), 'base': BASE,
                   'candidate_sha256': {f: hashlib.sha256(c if isinstance(c, bytes) else c.encode()).hexdigest()
                                        for f, c in cand.items()}, 'results': {}}
        sfa, ca = 0, 1
        for k, files in v.items():
            subprocess.run(['git', '-C', d, 'checkout', '-q', '--detach', '-f', BASE], check=True)
            subprocess.run(['git', '-C', d, 'clean', '-qfdx'], check=True)
            if files:
                for f, c in files.items():
                    p = os.path.join(d, f)
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    with open(p, 'wb') as fh:
                        fh.write(c if isinstance(c, bytes) else c.encode())
                subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
            subprocess.run(['git', '-C', d, '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
                            'commit', '-q', '--allow-empty', '-m', f'control {k}'], check=True)
            sha = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
            p = subprocess.run(['python3', COUNTER, '--lane', d, '--revision', sha,
                                '--sessions', os.path.join(work, 'no-sessions')], capture_output=True, text=True)
            line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else json.dumps({'error': p.stderr[-300:]})
            res = json.loads(line)
            with open(os.path.join(HERE, f'C2-{k}.jsonl'), 'w') as fh:
                fh.write(json.dumps({'control': k, 'expect': expect[k], 'exit': p.returncode}) + '\n')
                fh.write(line + '\n')
            summary['results'][k] = {kk: res.get(kk) for kk in ('verdict', 'rows', 'quotes_ok', 'props_ok', 'host_ok',
                                                                 'sources_ok', 'verdicts_ok', 'novelty_base_hits',
                                                                 'pointer_ok', 'transcripts_bound')}
            if expect[k] == 'FAIL' and res.get('verdict') != 'FAIL':
                sfa += 1
            if expect[k] == 'PASS' and res.get('verdict') != 'PASS':
                ca = 0
        summary['should_fail_accepted'] = sfa
        summary['control_accepted'] = ca
        with open(os.path.join(HERE, 'battery-summary-c2.jsonl'), 'w') as fh:
            fh.write(json.dumps(summary, sort_keys=True) + '\n')
            fh.write(json.dumps({'should_fail_accepted': sfa, 'control_accepted': ca}) + '\n')
        print(json.dumps(summary, sort_keys=True))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
