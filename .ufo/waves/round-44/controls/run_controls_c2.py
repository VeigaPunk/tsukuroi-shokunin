#!/usr/bin/env python3
"""Round-44 C2 pre-data control battery for tools/check-scrub-record-r44.py (scored before any seat).

Each control is a commit in a scratch clone of the lane (origin removed; toplevel asserted) on top of BASE carrying
the C2 surface copied into `c2-candidate/` beside this script (the r44 entry, the r43 entry with its pointer line,
the registry, the round-44 frozen sources and host capture) plus, where named, forged orchestrator records
(`w2-dispatch.json`, `w2-results.json`, residual records) and forged seat reports. The frozen counter (lane working
file) scores it.

  K0  do-nothing: BASE                                                              must FAIL
  K1  scripted writer: statements are the proposition tokens, quotes kept, planted reports, no records  must FAIL
  K2  K1 + forged results without dispatch tasks                                    must FAIL
  K4  forged records, one counted `fails`                                           must FAIL
  K5  forged records, one `partly` with no residual                                 must FAIL
  K6  mention-not-assertion: output and report open with a sentence quoting the holds line   must FAIL
  K7  content-free statements (proposition tokens removed), forged holds            must FAIL
  K8  SR7 without its ioctl.c quotes, forged holds                                  must FAIL
  K9  one quote's line number shifted by one, forged holds                          must FAIL
  K10 a sysfs.c quote labelled S242, forged holds                                   must FAIL
  K11 r43 entry without the pointer line, forged holds                              must FAIL
  K12 S242 row status `queued`, forged holds                                        must FAIL
  K13 JSON verdict_line holds, the committed report opens with a different line     must FAIL
  K14 padded verdict line: text output and report open with two spaces              must FAIL
  K15 blank-line-prefixed verdict: text output and report open with an empty line   must FAIL
  K16 JSON verdict_line holds beside a contradictory `verdict: fails`               must FAIL
  K17 S244 dropped from the entry's source: line, forged holds                      must FAIL
  K18 SR9 without a host line, forged holds                                         must FAIL
  K3  forged dispatch + results + reports, all `holds`                              control (expected PASS: the
      committed-bytes predicate cannot tell forged records from real ones; transcripts_bound 0)
  K19 forged records, one `partly` followed by a bound residual `holds`             control (expected PASS)

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
BASE = '98020ece0674e0b569ee23aed10ffbee355b248e'
COUNTER = os.path.join(LANE, 'tools/check-scrub-record-r44.py')
CAND = os.path.join(HERE, 'c2-candidate')
ENTRY = 'corpus/knowledge/btrfs-scrub-record-r44.md'
OLD = 'corpus/knowledge/btrfs-scrub-record-r43.md'
REG = 'corpus/SOURCES.md'
ROWS = ['SR7', 'SR8', 'SR9']
WAVE = '.ufo/waves/round-44'
SEATS = [(f'C2{k}SR{r[2:]}', role, r) for r in ROWS for k, role in (('Rev', 'reviewer'), ('Crit', 'critic'))]


def cand_files():
    out = {}
    for root, _dirs, files in os.walk(CAND):
        for f in files:
            p = os.path.join(root, f)
            out[os.path.relpath(p, CAND)] = open(p, 'rb').read()
    return out


def records(verdicts, dispatch=True, mention=None, report_override=None, output_override=None, residual=None):
    files = {}
    tasks = [{'name': n, 'agent': role, 'task': 'forged'} for n, role, _ in SEATS]
    if dispatch:
        files[f'{WAVE}/w2-dispatch.json'] = json.dumps({'taskCall': {'context': 'forged', 'tasks': tasks}}).encode()
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
        if output_override and n in output_override:
            out = output_override[n]
        if report_override and n in report_override:
            rep = report_override[n]
        res.append({'name': n, 'agent': role, 'output': out})
        files[f'{WAVE}/w2/{n}.md'] = rep.encode()
    files[f'{WAVE}/w2-results.json'] = json.dumps({'results': res}).encode()
    if residual:
        name, row, verdict = residual
        line = f'ROW {row} VERDICT: {verdict}'
        files[f'{WAVE}/residual-dispatch.json'] = json.dumps(
            {'taskCall': {'context': 'forged', 'tasks': [{'name': name, 'agent': 'reviewer', 'task': 'forged'}]}}).encode()
        files[f'{WAVE}/residual-results.json'] = json.dumps(
            {'results': [{'name': name, 'agent': 'reviewer', 'output': json.dumps({'verdict_line': line})}]}).encode()
        files[f'{WAVE}/residual/{name}.md'] = (line + '\n\nforged residual body\n').encode()
    return files


def scripted_entry(entry, counter_src):
    ns = {}
    exec(compile(counter_src.split('\ndef ', 1)[0], 'counter-head', 'exec'), ns)
    toks = {r: ns['ROWS'][r]['props'] for r in ROWS}
    out, cur, keep = [], None, True
    for ln in entry.splitlines():
        m = re.match(r'^## (SR\d)$', ln)
        if m:
            cur = m.group(1)
            out += [ln, '', '**Statement.** ' + ' '.join(toks[cur]) + ' scripted.', '']
            keep = False
            continue
        if ln.startswith('## '):
            cur = None
            keep = True
        if cur and (ln.startswith('**Quote.**') or ln.startswith('**Host reading.**')):
            out += [ln, '']
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
        cand = cand_files()
        counter_src = open(COUNTER).read()
        entry = cand[ENTRY].decode()

        def surface(**over):
            s = dict(cand)
            for k, v in over.items():
                s[k] = v if isinstance(v, bytes) else v.encode()
            return s

        def with_records(s, recs):
            s = dict(s)
            s.update(recs)
            return s

        v = {'K0': None}
        k1 = surface(**{ENTRY: scripted_entry(entry, counter_src)})
        for n, _role, row in SEATS:
            k1[f'{WAVE}/w2/{n}.md'] = f'ROW {row} VERDICT: holds\n'.encode()
        v['K1'] = k1
        v['K2'] = with_records(k1, records({}, dispatch=False))
        v['K3'] = with_records(surface(), records({}))
        v['K4'] = with_records(surface(), records({'C2CritSR8': 'fails'}))
        v['K5'] = with_records(surface(), records({'C2CritSR7': 'partly'}))
        v['K6'] = with_records(surface(), records({}, mention='C2CritSR9'))
        cf = entry
        for row in ROWS:
            for tok in re.search(r"'%s': \{.*?'props': (\[[^\]]*\])" % row, counter_src, re.S).group(1).strip('[]').replace("'", '').split(', '):
                tok = tok.strip()
                cf = re.sub(r'(\*\*Statement\.\*\*[^\n]*(?:\n(?!\*\*)[^\n]*)*)',
                            lambda m, t=tok: m.group(1).replace(t, 'X'), cf)
        assert cf != entry
        v['K7'] = with_records(surface(**{ENTRY: cf}), records({}))
        no_ioctl = '\n'.join(ln for ln in entry.split('\n') if not (ln.startswith('**Quote.**') and 'ioctl.c:' in ln))
        v['K8'] = with_records(surface(**{ENTRY: no_ioctl}), records({}))
        assert 'sysfs.c:2040:' in entry
        v['K9'] = with_records(surface(**{ENTRY: entry.replace('sysfs.c:2040:', 'sysfs.c:2041:', 1)}), records({}))
        v['K10'] = with_records(surface(**{ENTRY: entry.replace('`S243` sysfs.c:2044', '`S242` sysfs.c:2044', 1)}),
                                records({}))
        base_old = subprocess.run(['git', '-C', d, 'show', f'{BASE}:{OLD}'], capture_output=True).stdout
        v['K11'] = with_records(surface(**{OLD: base_old}), records({}))
        reg = cand[REG].decode()
        reg12 = re.sub(r'(\| S242 \|(?:[^|]*\|){6}) mined \|', r'\1 queued |', reg, count=1)
        assert reg12 != reg
        v['K12'] = with_records(surface(**{REG: reg12}), records({}))
        v['K13'] = with_records(surface(), records({}, report_override={
            'C2RevSR8': 'VERDICT: holds\nROW SR8 VERDICT: holds\n'}))
        v['K14'] = with_records(surface(), records({}, output_override={
            'C2RevSR7': '  ROW SR7 VERDICT: holds\nbody'}, report_override={'C2RevSR7': '  ROW SR7 VERDICT: holds\nbody\n'}))
        v['K15'] = with_records(surface(), records({}, output_override={
            'C2CritSR9': '\nROW SR9 VERDICT: holds\nbody'}, report_override={'C2CritSR9': '\nROW SR9 VERDICT: holds\nbody\n'}))
        v['K16'] = with_records(surface(), records({}, output_override={
            'C2CritSR8': json.dumps({'verdict_line': 'ROW SR8 VERDICT: holds', 'verdict': 'fails'})}))
        srcfix = re.sub(r'^(source: [^\n]*?) S244', r'\1', entry, count=1, flags=re.M)
        assert srcfix != entry
        v['K17'] = with_records(surface(**{ENTRY: srcfix}), records({}))
        sec = entry.split('## SR9', 1)
        nohost = sec[0] + '## SR9' + re.sub(r'\*\*Host reading\.\*\*.*?(?=\n\n## )', '', sec[1], count=1, flags=re.S)
        assert nohost != entry
        v['K18'] = with_records(surface(**{ENTRY: nohost}), records({}))
        v['K19'] = with_records(surface(), records({'C2RevSR9': 'partly'}, residual=('C2ResSR9', 'SR9', 'holds')))

        expect = {k: ('PASS' if k in ('K3', 'K19') else 'FAIL') for k in v}
        summary = {'counter_sha256': hashlib.sha256(counter_src.encode()).hexdigest(), 'base': BASE,
                   'candidate_sha256': {f: hashlib.sha256(c).hexdigest() for f, c in sorted(cand.items())},
                   'results': {}}
        sfa, ca = 0, 1
        for k, files in v.items():
            subprocess.run(['git', '-C', d, 'checkout', '-q', '--detach', '-f', BASE], check=True)
            subprocess.run(['git', '-C', d, 'clean', '-qfdx'], check=True)
            if files:
                for f, c in files.items():
                    p = os.path.join(d, f)
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    with open(p, 'wb') as fh:
                        fh.write(c)
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
            print(k, expect[k], json.dumps(summary['results'][k]), flush=True)
            if expect[k] == 'FAIL' and res.get('verdict') != 'FAIL':
                sfa += 1
            if expect[k] == 'PASS' and res.get('verdict') != 'PASS':
                ca = 0
        summary['should_fail_accepted'] = sfa
        summary['control_accepted'] = ca
        with open(os.path.join(HERE, 'battery-summary-c2.jsonl'), 'w') as fh:
            fh.write(json.dumps(summary, sort_keys=True) + '\n')
            fh.write(json.dumps({'should_fail_accepted': sfa, 'control_accepted': ca}) + '\n')
        print(json.dumps({'should_fail_accepted': sfa, 'control_accepted': ca}))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
