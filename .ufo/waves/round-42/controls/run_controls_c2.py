#!/usr/bin/env python3
"""Round-42 C2 pre-data controls: score control trees with the frozen counter
tools/check-scrub-record-r42.py (read from --counter-rev) in a private fixture clone of --tree-rev
(`git clone --shared`, origin removed, fixture identity only inside the clone).

Every control writes an entry by script, never by reading a source: each row's statement is the row's frozen
token plus filler, each quote is copied from the first non-blank line inside the row's frozen window (so every
lexical check passes by construction), the host line names capture.txt:1, and the three registry rows are
flipped to `mined` with used-by naming the entry.
  K0 do-nothing          the tree as frozen (no entry)
  K1 planted verdicts    scripted entry + ten `ROW SC<n> VERDICT: holds` report files, no dispatch/results
  K2 forged results      K1 + a w2-results.json binding the ten seats; w2-dispatch.json lacks them
  K3 forged records      K1 + forged w2-dispatch.json and w2-results.json (reachability of the predicate,
                         and the recorded limit: committed bytes cannot tell forged orchestrator files apart;
                         the reported transcripts_bound stays 0)
  K4 one fails           K3 with C2CritSC3 reading `fails`
  K5 partly unanswered   K3 with C2RevSC2 reading `partly` and no residual seat
Expected: K3 PASS, every other control FAIL.

Usage: python3 run_controls_c2.py --lane <lane> --tree-rev <REV> --counter-rev <REV|WORKTREE> --scratch <DIR> --out <DIR>
"""
import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

WAVE = '.ufo/waves/round-42'


def git(d, *a):
    return subprocess.run(['git', '-C', d, *a], check=True, capture_output=True, text=True)


def load_counter(path):
    spec = importlib.util.spec_from_file_location('c2counter', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def scripted_entry(c, clone):
    src = {f: open(os.path.join(clone, WAVE, 'frozen/src', f), errors='replace').read().split('\n') for f in c.SNAP}
    sid = {'scrub.c': 'S237', 'CHANGES': 'S238'}
    out = ['source: S237 S238 S239', 'verified-at: 2026-10-26', 'recheck: on-release', '', '# scripted control entry', '']
    for row, spec in c.ROWS.items():
        f, lo, hi = spec['windows'][0]
        n = next(i for i in range(lo, hi + 1) if src[f][i - 1].strip() and '"' not in src[f][i - 1])
        q = src[f][n - 1].strip()
        out += [f'## {row}', '', f'**Statement.** The record concerns {spec["token"]} in every case.', '',
                f'**Quote.** `{sid[f]}` {f}:{n}: "{q}"', '', '**Host reading.** capture.txt:1 holds the time.', '']
    return '\n'.join(out) + '\n'


def flip_rows(clone, entry):
    p = os.path.join(clone, 'corpus/SOURCES.md')
    lines = open(p).read().split('\n')
    for i, ln in enumerate(lines):
        m = re.match(r'^\|\s*(S23[7-9])\s*\|', ln)
        if m:
            cells = ln.strip().strip('|').split('|')
            cells[7] = ' mined '
            cells[10] = f' {entry} '
            lines[i] = '|' + '|'.join(cells) + '|'
    open(p, 'w').write('\n'.join(lines))


def seats():
    for n in range(1, 6):
        yield f'C2RevSC{n}', 'reviewer', f'SC{n}'
        yield f'C2CritSC{n}', 'critic', f'SC{n}'


def write_reports(clone, verdicts):
    d = os.path.join(clone, WAVE, 'w2')
    os.makedirs(d, exist_ok=True)
    for name, _role, row in seats():
        open(os.path.join(d, f'{name}.md'), 'w').write(f'# {name}\n\nROW {row} VERDICT: {verdicts.get(name, "holds")}\n')


def write_records(clone, verdicts, dispatch=True):
    res = {'lane': 'tsukuroi', 'round': '42', 'wave': 'w2', 'seats': 10,
           'results': [{'name': n, 'agent': r, 'output': f'done. ROW {row} VERDICT: {verdicts.get(n, "holds")}', 'note': None}
                       for n, r, row in seats()]}
    json.dump(res, open(os.path.join(clone, WAVE, 'w2-results.json'), 'w'))
    tasks = [{'name': n, 'agent': r, 'task': 'forged'} for n, r, _ in seats()] if dispatch else \
            [{'name': 'Other', 'agent': 'scout', 'task': 'x'}]
    json.dump({'taskCall': {'context': 'forged', 'tasks': tasks}}, open(os.path.join(clone, WAVE, 'w2-dispatch.json'), 'w'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--tree-rev', required=True)
    ap.add_argument('--counter-rev', required=True)
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--names', default='K0,K1,K2,K3,K4,K5')
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    os.makedirs(a.out, exist_ok=True)
    clone = os.path.join(a.scratch, 'fixture-clone-c2')
    shutil.rmtree(clone, ignore_errors=True)
    entry = 'corpus/knowledge/btrfs-scrub-record-r42.md'
    summary = {}
    try:
        subprocess.run(['git', 'clone', '-q', '--shared', a.lane, clone], check=True)
        if os.path.realpath(git(clone, 'rev-parse', '--show-toplevel').stdout.strip()) != os.path.realpath(clone):
            raise SystemExit('fixture toplevel mismatch')
        git(clone, 'remote', 'remove', 'origin')
        cpath = os.path.join(a.scratch, 'c2counter.py')
        if a.counter_rev == 'WORKTREE':   # pre-freeze dry run only
            shutil.copy(os.path.join(a.lane, 'tools/check-scrub-record-r42.py'), cpath)
        else:
            open(cpath, 'wb').write(subprocess.run(['git', '-C', a.lane, 'show', f'{a.counter_rev}:tools/check-scrub-record-r42.py'],
                                                   check=True, capture_output=True).stdout)
        c = load_counter(cpath)
        idt = ['-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid']
        for name in a.names.split(','):
            git(clone, 'checkout', '-q', '--force', '--detach', a.tree_rev)
            git(clone, 'clean', '-qfdx')
            if name != 'K0':
                open(os.path.join(clone, entry), 'w').write(scripted_entry(c, clone))
                flip_rows(clone, entry)
                v = {'K4': {'C2CritSC3': 'fails'}, 'K5': {'C2RevSC2': 'partly'}}.get(name, {})
                write_reports(clone, v)
                if name == 'K2':
                    write_records(clone, v, dispatch=False)
                elif name in ('K3', 'K4', 'K5'):
                    write_records(clone, v)
            git(clone, 'add', '-A')
            subprocess.run(['git', '-C', clone, *idt, 'commit', '-q', '--allow-empty', '-m', f'control {name}'],
                           check=True, capture_output=True)
            rev = git(clone, 'rev-parse', 'HEAD').stdout.strip()
            p = subprocess.run([sys.executable, cpath, '--revision', rev, '--lane', clone], capture_output=True, text=True)
            line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else '{}'
            rec = {'control': name, 'exit': p.returncode, 'counter_rev': a.counter_rev, 'tree_rev': a.tree_rev,
                   'result': json.loads(line)}
            with open(os.path.join(a.out, f'C2-{name}.jsonl'), 'w') as f:
                f.write(json.dumps(rec, sort_keys=True) + '\n')
            r = rec['result']
            summary[name] = r.get('verdict')
            print(name, p.returncode, r.get('verdict'), 'rows', r.get('rows'), 'q', r.get('quotes_ok'), 'nov', r.get('novelty_ok'),
                  'host', r.get('host_ok'), 'src', r.get('sources_ok'), 'v', r.get('verdicts_ok'), 'base', r.get('novelty_base_hits'),
                  'tb', r.get('transcripts_bound'), flush=True)
        sf = [k for k, v in summary.items() if k != 'K3' and v == 'PASS']
        last = {'battery': 'C2', 'controls': summary, 'should_fail_accepted': len(sf),
                'should_fail_accepted_names': sf, 'control_accepted': int(summary.get('K3') == 'PASS')}
        with open(os.path.join(a.out, 'battery-summary.jsonl'), 'w') as f:
            f.write(json.dumps(last, sort_keys=True) + '\n')
        print(json.dumps(last, sort_keys=True))
    finally:
        shutil.rmtree(clone, ignore_errors=True)


if __name__ == '__main__':
    main()
