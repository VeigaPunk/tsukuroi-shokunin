#!/usr/bin/env python3
"""Round-45 attempt-2 re-run of the C2 pre-data control battery (wave names a2w1/a2r1; candidate bytes and
control set unchanged from controls/run_controls_c2.py).

Original docstring: Round-45 C2 pre-data control battery for tools/check-scrub-grounding-r45.py (scored before any seat).

Each control is a commit in a scratch clone of the lane (origin removed; toplevel asserted) on top of BASE carrying
the C2 surface copied into `c2-candidate/` beside this script (the r45 entry, the r44 entry with its appended
round-45 section, the registry, the round-45 frozen sources and host capture) plus, where named, forged orchestrator
records (`a2w1-dispatch.json`, `a2w1-results.json`, `a2r1-*` residual records) and forged seat reports. The frozen
counter (lane working file) scores it.

  K0  do-nothing: BASE                                                              must FAIL
  K1  scripted writer: statements are the proposition tokens, quotes kept, planted reports, no records  must FAIL
  K2  K1 + forged results without dispatch tasks                                    must FAIL
  K4  forged records, one counted `fails`                                           must FAIL
  K5  forged records, one `partly` with no residual                                 must FAIL
  K6  mention-not-assertion: output and report open with a sentence quoting the holds line   must FAIL
  K7  content-free statements (proposition tokens removed), forged holds            must FAIL
  K8  GR2 without its dev-replace.c quotes, forged holds                            must FAIL
  K9  one quote's line number shifted by one, forged holds                          must FAIL
  K10 a sysfs.c quote labelled S242, forged holds                                   must FAIL
  K11 r44 entry without the round-45 section, forged holds                          must FAIL
  K12 S246 row status `queued`, forged holds                                        must FAIL
  K13 JSON verdict_line holds, the committed report opens with a different line     must FAIL
  K14 padded verdict line: text output and report open with two spaces              must FAIL
  K15 blank-line-prefixed verdict: text output and report open with an empty line   must FAIL
  K16 JSON verdict_line holds beside a contradictory `verdict: fails`               must FAIL
  K17 S247 dropped from the entry's source: line, forged holds                      must FAIL
  K18 GR3 without a host line, forged holds                                         must FAIL
  K20 gutted quote: one quote's text replaced by `n` (round-44 F1)                  must FAIL
  K21 doctored duplicate S246 row appended after the registry (used-by dropped; round-44 F2)  must FAIL
  K22 duplicate S246 row inside a fenced block under Search log                     must FAIL
  K23 duplicate `verdict_line` keys in one output, `fails` then `holds` (C2MutBinding F1)  must FAIL
  K24 top-level JSON array as a2w1-results.json (C2MutBinding F4: must not crash)     must FAIL
  K25 orphan repository without the base commit (round-44 F3)                       must FAIL (exit 2)
  K27 text output opening `holds` that later states `ROW GR1 VERDICT: fails`         must FAIL
  K28 held knowledge restated: GR1's statement replaced by the round-44 SR8 statement  must FAIL
  K29 quotes as statement: each statement is its row's quote texts joined           must FAIL
  K3  forged dispatch + results + reports, all `holds`                              control (expected PASS: the
      committed-bytes predicate cannot tell forged records from real ones; transcripts_bound 0)
  K19 forged records, one `partly` followed by a bound residual `holds`             control (expected PASS)
  K26 outputs recorded as JSON-encoded strings (the round-44 C2RevSR7 shape)        control (expected PASS)

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
BASE = '5bbd5ff588120fd8e7c744695351a6978b4241c1'
COUNTER = os.path.join(LANE, 'tools/check-scrub-grounding-r45.py')
CAND = os.path.join(os.path.dirname(HERE), 'controls', 'c2-candidate')
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
OLD = 'corpus/knowledge/btrfs-scrub-record-r44.md'
REG = 'corpus/SOURCES.md'
ROWS = ['GR1', 'GR2', 'GR3']
WAVE = '.ufo/waves/round-45'
SEATS = [(f'C2{k}GR{r[2:]}', role, r) for r in ROWS for k, role in (('Rev', 'reviewer'), ('Crit', 'critic'))]


def cand_files():
    out = {}
    for root, _dirs, files in os.walk(CAND):
        for f in files:
            p = os.path.join(root, f)
            out[os.path.relpath(p, CAND)] = open(p, 'rb').read()
    return out


def records(verdicts, dispatch=True, mention=None, report_override=None, output_override=None, residual=None,
            results_raw=None, as_json_string=False):
    files = {}
    tasks = [{'name': n, 'agent': role, 'task': 'forged'} for n, role, _ in SEATS]
    if dispatch:
        files[f'{WAVE}/a2w1-dispatch.json'] = json.dumps({'taskCall': {'context': 'forged', 'tasks': tasks}}).encode()
    res = []
    for n, role, row in SEATS:
        line = f'ROW {row} VERDICT: {verdicts.get(n, "holds")}'
        if mention == n:
            out = (f'I dispute the line "{line}" that another seat might write; the row overreaches.\n'
                   f'ROW {row} VERDICT: fails is what I would bind.')
            rep = out
        elif as_json_string:
            out = json.dumps(line + '\n\nforged body')
            rep = line + '\n\nforged report body\n'
        else:
            out = json.dumps({'verdict_line': line, 'row': row, 'seat': n})
            rep = line + '\n\nforged report body\n'
        if output_override and n in output_override:
            out = output_override[n]
        if report_override and n in report_override:
            rep = report_override[n]
        res.append({'name': n, 'agent': role, 'output': out})
        files[f'{WAVE}/a2w1/{n}.md'] = rep.encode()
    files[f'{WAVE}/a2w1-results.json'] = results_raw if results_raw is not None else json.dumps({'results': res}).encode()
    if residual:
        name, row, verdict = residual
        line = f'ROW {row} VERDICT: {verdict}'
        files[f'{WAVE}/a2r1-dispatch.json'] = json.dumps(
            {'taskCall': {'context': 'forged', 'tasks': [{'name': name, 'agent': 'reviewer', 'task': 'forged'}]}}).encode()
        files[f'{WAVE}/a2r1-results.json'] = json.dumps(
            {'results': [{'name': name, 'agent': 'reviewer', 'output': json.dumps({'verdict_line': line})}]}).encode()
        files[f'{WAVE}/a2r1/{name}.md'] = (line + '\n\nforged residual body\n').encode()
    return files


def counter_rows(counter_src):
    ns = {}
    exec(compile(counter_src.split('\nclass ', 1)[0], 'counter-head', 'exec'), ns)
    return ns['ROWS']


def scripted_entry(entry, rows_spec):
    out, cur, keep = [], None, True
    for ln in entry.splitlines():
        m = re.match(r'^## (GR\d)$', ln)
        if m:
            cur = m.group(1)
            out += [ln, '', '**Statement.** ' + ' '.join(rows_spec[cur]['props']) + ' scripted.', '']
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


def replace_statement(entry, row, text):
    pat = re.compile(r'(## %s\n\n)\*\*Statement\.\*\*.*?(?=\n\n\*\*Quote\.\*\*)' % row, re.S)
    out, n = pat.subn(lambda m: m.group(1) + '**Statement.** ' + text, entry, count=1)
    assert n == 1, row
    return out


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
        rows_spec = counter_rows(counter_src)
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
        k1 = surface(**{ENTRY: scripted_entry(entry, rows_spec)})
        for n, _role, row in SEATS:
            k1[f'{WAVE}/a2w1/{n}.md'] = f'ROW {row} VERDICT: holds\n'.encode()
        v['K1'] = k1
        v['K2'] = with_records(k1, records({}, dispatch=False))
        v['K3'] = with_records(surface(), records({}))
        v['K4'] = with_records(surface(), records({'C2CritGR2': 'fails'}))
        v['K5'] = with_records(surface(), records({'C2CritGR1': 'partly'}))
        v['K6'] = with_records(surface(), records({}, mention='C2CritGR3'))
        cf = entry
        for row in ROWS:
            cf = replace_statement(cf, row, 'This row says nothing about the quoted code.')
        v['K7'] = with_records(surface(**{ENTRY: cf}), records({}))
        no_dr = '\n'.join(ln for ln in entry.split('\n')
                          if not (ln.startswith('**Quote.**') and 'dev-replace.c:' in ln))
        v['K8'] = with_records(surface(**{ENTRY: no_dr}), records({}))
        assert 'sysfs.c:2040:' in entry
        v['K9'] = with_records(surface(**{ENTRY: entry.replace('sysfs.c:2040:', 'sysfs.c:2041:', 1)}), records({}))
        assert '`S243` sysfs.c:2043' in entry
        v['K10'] = with_records(surface(**{ENTRY: entry.replace('`S243` sysfs.c:2043', '`S242` sysfs.c:2043', 1)}),
                                records({}))
        base_old = subprocess.run(['git', '-C', d, 'show', f'{BASE}:{OLD}'], capture_output=True).stdout
        v['K11'] = with_records(surface(**{OLD: base_old}), records({}))
        reg = cand[REG].decode()
        reg12 = re.sub(r'(\| S246 \|(?:[^|]*\|){6}) mined \|', r'\1 queued |', reg, count=1)
        assert reg12 != reg
        v['K12'] = with_records(surface(**{REG: reg12}), records({}))
        v['K13'] = with_records(surface(), records({}, report_override={
            'C2RevGR2': 'VERDICT: holds\nROW GR2 VERDICT: holds\n'}))
        v['K14'] = with_records(surface(), records({}, output_override={
            'C2RevGR1': '  ROW GR1 VERDICT: holds\nbody'}, report_override={'C2RevGR1': '  ROW GR1 VERDICT: holds\nbody\n'}))
        v['K15'] = with_records(surface(), records({}, output_override={
            'C2CritGR3': '\nROW GR3 VERDICT: holds\nbody'}, report_override={'C2CritGR3': '\nROW GR3 VERDICT: holds\nbody\n'}))
        v['K16'] = with_records(surface(), records({}, output_override={
            'C2CritGR2': json.dumps({'verdict_line': 'ROW GR2 VERDICT: holds', 'verdict': 'fails'})}))
        srcfix = re.sub(r'^(source: [^\n]*?) S247', r'\1', entry, count=1, flags=re.M)
        assert srcfix != entry
        v['K17'] = with_records(surface(**{ENTRY: srcfix}), records({}))
        sec = entry.split('## GR3', 1)
        nohost = sec[0] + '## GR3' + re.sub(r'\*\*Host reading\.\*\*.*?(?=\n\n## )', '', sec[1], count=1, flags=re.S)
        assert nohost != entry
        v['K18'] = with_records(surface(**{ENTRY: nohost}), records({}))
        v['K19'] = with_records(surface(), records({'C2RevGR3': 'partly'}, residual=('C2ResGR3', 'GR3', 'holds')))
        gut = re.sub(r'(\*\*Quote\.\*\* `S246` cmdline\.c:156: )"[^"\n]*"', r'\1"n"', entry, count=1)
        assert gut != entry
        v['K20'] = with_records(surface(**{ENTRY: gut}), records({}))
        row246 = next(ln for ln in reg.split('\n') if ln.startswith('| S246 |'))
        doctored = row246.replace('| ' + ENTRY + ' |', '| — |')
        assert doctored != row246
        v['K21'] = with_records(surface(**{REG: reg.rstrip('\n') + '\n\n' + doctored + '\n'}), records({}))
        fenced = reg.replace('## Search log\n', '## Search log\n\n```\n' + doctored + '\n```\n', 1)
        assert fenced != reg
        v['K22'] = with_records(surface(**{REG: fenced}), records({}))
        v['K23'] = with_records(surface(), records({}, output_override={
            'C2RevGR1': '{"verdict_line": "ROW GR1 VERDICT: fails", "verdict_line": "ROW GR1 VERDICT: holds"}'}))
        v['K24'] = with_records(surface(), records({}, results_raw=json.dumps(
            [{'name': n, 'agent': r, 'output': f'ROW {row} VERDICT: holds'} for n, r, row in SEATS]).encode()))
        v['K26'] = with_records(surface(), records({}, as_json_string=True))
        v['K27'] = with_records(surface(), records({}, output_override={
            'C2CritGR1': 'ROW GR1 VERDICT: holds\n\nOn reflection:\nROW GR1 VERDICT: fails'}))
        sr8 = re.search(r'## SR8\n\n\*\*Statement\.\*\* (.*?)\n\n\*\*Quote', cand[OLD].decode(), re.S).group(1)
        v['K28'] = with_records(surface(**{ENTRY: replace_statement(entry, 'GR1', sr8)}), records({}))
        qs_entry = entry
        for row in ROWS:
            body = entry.split(f'## {row}\n', 1)[1].split('\n## ', 1)[0]
            qtexts = re.findall(r'^\*\*Quote\.\*\* `S\d+` [^:]+:\d+: "(.+)"\s*$', body, re.M)
            qs_entry = replace_statement(qs_entry, row, ' '.join(qtexts))
        v['K29'] = with_records(surface(**{ENTRY: qs_entry}), records({}))

        expect = {k: ('PASS' if k in ('K3', 'K19', 'K26') else 'FAIL') for k in v}
        expect['K25'] = 'FAIL'
        summary = {'counter_sha256': hashlib.sha256(counter_src.encode()).hexdigest(), 'base': BASE,
                   'candidate_sha256': {f: hashlib.sha256(c).hexdigest() for f, c in sorted(cand.items())},
                   'results': {}}
        sfa, ca = 0, 1

        def score(k, repo, sha):
            nonlocal sfa, ca
            p = subprocess.run(['python3', COUNTER, '--lane', repo, '--revision', sha,
                                '--sessions', os.path.join(work, 'no-sessions')], capture_output=True, text=True)
            line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else json.dumps({'error': p.stderr[-300:]})
            res = json.loads(line)
            res.setdefault('verdict', 'FAIL')
            with open(os.path.join(HERE, f'C2-{k}.jsonl'), 'w') as fh:
                fh.write(json.dumps({'control': k, 'expect': expect[k], 'exit': p.returncode}) + '\n')
                fh.write(line + '\n')
            summary['results'][k] = {kk: res.get(kk) for kk in ('verdict', 'rows', 'quotes_ok', 'props_ok', 'host_ok',
                                                                 'sources_ok', 'verdicts_ok', 'novelty_base_hits',
                                                                 'pointer_ok', 'transcripts_bound', 'error')}
            summary['results'][k]['exit'] = p.returncode
            print(k, expect[k], json.dumps(summary['results'][k]), flush=True)
            if expect[k] == 'FAIL' and res.get('verdict') != 'FAIL':
                sfa += 1
            if expect[k] == 'PASS' and res.get('verdict') != 'PASS':
                ca = 0

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
            score(k, d, sha)

        # K25: orphan repository holding K3's files but not the base commit
        o = os.path.join(work, 'orphan')
        subprocess.run(['git', 'init', '-q', o], check=True)
        top = subprocess.run(['git', '-C', o, 'rev-parse', '--show-toplevel'], capture_output=True,
                             text=True).stdout.strip()
        assert os.path.realpath(top) == os.path.realpath(o), top
        subprocess.run(['git', '-C', d, 'checkout', '-q', '--detach', '-f', BASE], check=True)
        subprocess.run(['git', '-C', d, 'archive', '--format=tar', '-o', os.path.join(work, 'base.tar'), BASE],
                       check=True)
        subprocess.run(['tar', '-xf', os.path.join(work, 'base.tar'), '-C', o], check=True)
        for f, c in v['K3'].items():
            p = os.path.join(o, f)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'wb') as fh:
                fh.write(c)
        subprocess.run(['git', '-C', o, 'add', '-A'], check=True)
        subprocess.run(['git', '-C', o, '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
                        'commit', '-q', '-m', 'orphan K25'], check=True)
        sha = subprocess.run(['git', '-C', o, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        score('K25', o, sha)

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
