#!/usr/bin/env python3
"""C2CritControl: attack the verdict binding of check-scrub-record-r42.py on fixture clones.

Each mutant starts from a K3-shaped tree (scripted entry + flipped registry + forged w2 records that
score PASS) and changes exactly one thing about dispatch / results / report / sessions.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
WAVE = '.ufo/waves/round-42'
ENTRY = 'corpus/knowledge/btrfs-scrub-record-r42.md'
TREE = 'a84fc9dec860f8bea516dff7ddfdc98223cdae52'
S = '/fast/scratch/hyaku/tsukuroi-r42/C2CritControl'
CLONE = os.path.join(S, 'fx-clone')
SESS = os.path.join(S, 'sessions')
OUT = os.path.join(S, 'out')
IDT = ['-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid']


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
        if re.match(r'^\|\s*(S23[7-9])\s*\|', ln):
            cells = ln.strip().strip('|').split('|')
            cells[7] = ' mined '
            cells[10] = f' {entry} '
            lines[i] = '|' + '|'.join(cells) + '|'
    open(p, 'w').write('\n'.join(lines))


def seats():
    for n in range(1, 6):
        yield f'C2RevSC{n}', 'reviewer', f'SC{n}'
        yield f'C2CritSC{n}', 'critic', f'SC{n}'


def base_files():
    """K3-shaped: every seat holds, reports carry the line, dispatch+results forged."""
    rep, res, tasks = {}, [], []
    for name, role, row in seats():
        rep[f'{WAVE}/w2/{name}.md'] = f'# {name}\n\nROW {row} VERDICT: holds\n'
        res.append({'name': name, 'agent': role,
                    'output': f'{name} read {row} line by line; two sentences checked.\nROW {row} VERDICT: holds',
                    'note': None})
        tasks.append({'name': name, 'agent': role, 'task': 'forged'})
    return rep, {'lane': 'tsukuroi', 'round': '42', 'wave': 'w2', 'seats': 10, 'results': res}, \
        {'taskCall': {'context': 'forged', 'tasks': tasks}}


def setres(res, name, **kw):
    for r in res['results']:
        if r['name'] == name:
            r.update(kw)
            return
    raise SystemExit(f'no result {name}')


def settask(disp, name, **kw):
    for t in disp['taskCall']['tasks']:
        if t['name'] == name:
            t.update(kw)
            return
    raise SystemExit(f'no task {name}')


def m_two_lines(rep, res, disp):
    setres(res, 'C2RevSC1', output='ROW SC1 VERDICT: holds\nROW SC1 VERDICT: fails')


def m_two_lines_same(rep, res, disp):
    setres(res, 'C2RevSC1', output='ROW SC1 VERDICT: holds\nROW SC1 VERDICT: holds')


def m_report_two_lines(rep, res, disp):
    rep[f'{WAVE}/w2/C2RevSC1.md'] = '# C2RevSC1\n\nROW SC1 VERDICT: holds\n\nROW SC1 VERDICT: fails\n'


def m_report_negation(rep, res, disp):
    rep[f'{WAVE}/w2/C2RevSC1.md'] = '# C2RevSC1\n\nDISPUTED: ROW SC1 VERDICT: holds is false; sentence 2 is wrong.\n'


def m_output_negation(rep, res, disp):
    txt = 'I cannot support this row. I do not write ROW SC1 VERDICT: holds: sentence 2 is false.'
    setres(res, 'C2RevSC1', output=txt)
    rep[f'{WAVE}/w2/C2RevSC1.md'] = '# C2RevSC1\n\n' + txt + '\n'


def m_output_negation_report_plain(rep, res, disp):
    setres(res, 'C2RevSC1', output='Rejected. This row is not ROW SC1 VERDICT: holds.\n')


def m_wrong_role(rep, res, disp):
    setres(res, 'C2RevSC1', agent='critic')
    settask(disp, 'C2RevSC1', agent='critic')


def m_report_case(rep, res, disp):
    rep[f'{WAVE}/w2/C2RevSC1.md'] = '# C2RevSC1\n\nrow SC1 VERDICT: holds\n'


def m_report_spacing(rep, res, disp):
    rep[f'{WAVE}/w2/C2RevSC1.md'] = '# C2RevSC1\n\nROW SC1 VERDICT:  holds\n'


def m_report_embedded(rep, res, disp):
    rep[f'{WAVE}/w2/C2RevSC1.md'] = '# C2RevSC1\n\nXROW SC1 VERDICT: holdsX\n'


def m_output_none(rep, res, disp):
    setres(res, 'C2RevSC1', output=None)


def m_output_case(rep, res, disp):
    setres(res, 'C2RevSC1', output='ROW SC1 VERDICT: Holds')


RRES = {'lane': 'tsukuroi', 'round': '42', 'wave': 'residual', 'seats': 1,
        'results': [{'name': 'C2RevSC1c', 'agent': 'reviewer', 'output': 'ROW SC1 VERDICT: holds', 'note': None}]}
RDISP = {'taskCall': {'context': 'forged', 'tasks': [{'name': 'C2RevSC1c', 'agent': 'reviewer', 'task': 'residual'}]}}


def add_residual(rep, verdict):
    rep[f'{WAVE}/residual-dispatch.json'] = json.dumps(RDISP)
    r = json.loads(json.dumps(RRES))
    r['results'][0]['output'] = f'ROW SC1 VERDICT: {verdict}'
    rep[f'{WAVE}/residual-results.json'] = json.dumps(r)
    rep[f'{WAVE}/residual/C2RevSC1c.md'] = f'# C2RevSC1c\n\nROW SC1 VERDICT: {verdict}\n'


def setv(rep, res, name, row, v):
    setres(res, name, output=f'ROW {row} VERDICT: {v}')
    rep[f'{WAVE}/w2/{name}.md'] = f'# {name}\n\nROW {row} VERDICT: {v}\n'


def m_residual_for_fails(rep, res, disp):
    setv(rep, res, 'C2RevSC1', 'SC1', 'partly')
    setv(rep, res, 'C2CritSC1', 'SC1', 'fails')
    add_residual(rep, 'holds')


def m_residual_partly(rep, res, disp):
    setv(rep, res, 'C2RevSC1', 'SC1', 'partly')
    add_residual(rep, 'partly')


def m_crit_fails(rep, res, disp):
    setv(rep, res, 'C2CritSC1', 'SC1', 'fails')


def m_partly_residual_holds(rep, res, disp):
    setv(rep, res, 'C2RevSC1', 'SC1', 'partly')
    setv(rep, res, 'C2CritSC1', 'SC1', 'partly')
    add_residual(rep, 'holds')


def m_no_taskcall(rep, res, disp):
    disp['tasks'] = disp.pop('taskCall')['tasks']


def m_report_no_line(rep, res, disp):
    rep[f'{WAVE}/w2/C2RevSC1.md'] = '# C2RevSC1\n\nthe row is fine.\n'


def m_output_other_row(rep, res, disp):
    setres(res, 'C2RevSC1', output='ROW SC2 VERDICT: holds')
    rep[f'{WAVE}/w2/C2RevSC1.md'] = '# C2RevSC1\n\nROW SC1 VERDICT: holds\n'


def m_k3_shape(rep, res, disp):
    """Exactly the pre-data K3 fixture shape: one line 'done. ROW <row> VERDICT: holds'."""
    for name, _role, row in seats():
        setres(res, name, output=f'done. ROW {row} VERDICT: holds')


def m_dup_task(rep, res, disp):
    disp['taskCall']['tasks'].append(dict(disp['taskCall']['tasks'][0]))


def m_empty_results(rep, res, disp):
    res['results'] = []


def m_residual_fails_on_holds(rep, res, disp):
    """Residual seat for a holds row reads fails: is it consulted at all?"""
    add_residual(rep, 'fails')


def m_shared_output(rep, res, disp):
    blob = '\n'.join(f'ROW SC{i} VERDICT: holds' for i in range(1, 6))
    for r in res['results']:
        r['output'] = blob
    for name, _role, _row in seats():
        rep[f'{WAVE}/w2/{name}.md'] = '# seat\n\n' + blob + '\n'


def m_shared_output_with_fails(rep, res, disp):
    """Same one blob serves all ten seats, but it also states fails for SC3: does SC3 still bind holds?"""
    blob = '\n'.join(f'ROW SC{i} VERDICT: holds' for i in range(1, 6))
    setres(res, 'C2RevSC3', output=blob + '\nROW SC3 VERDICT: fails')


def m_minimal_dispatch(rep, res, disp):
    for t in disp['taskCall']['tasks']:
        t.pop('task', None)


def m_stale_sessions(rep, res, disp):
    pass  # handled by sessions payload


MUT = {
    'B': ('baseline K3 forged records, all holds', None, None),
    'M1': ('output carries two SC1 VERDICT lines (holds then fails)', m_two_lines, None),
    'M1b': ('output carries the same SC1 holds line twice', m_two_lines_same, None),
    'M2': ('report carries holds line plus a ROW SC1 VERDICT: fails line', m_report_two_lines, None),
    'M3': ('report carries the line only inside a disputing sentence', m_report_negation, None),
    'M4': ('output+report reject the row but quote the holds line once', m_output_negation, None),
    'M4b': ('output says "not ROW SC1 VERDICT: holds", report plain', m_output_negation_report_plain, None),
    'M5': ('right name, role critic in both records', m_wrong_role, None),
    'M6a': ('report line lower-case "row"', m_report_case, None),
    'M6b': ('report line double space after colon', m_report_spacing, None),
    'M6c': ('report line embedded in longer token XROW...holdsX', m_report_embedded, None),
    'M7': ('results output is null', m_output_none, None),
    'M8': ('output word "Holds" capitalised', m_output_case, None),
    'M9': ('partly+fails with residual holds', m_residual_for_fails, None),
    'M10': ('residual fails on an all-holds row', m_residual_fails_on_holds, None),
    'M11': ('one blob (five lines) as every seat output and every report', m_shared_output, None),
    'M12': ('one blob also stating fails for SC3', m_shared_output_with_fails, None),
    'M13': ('dispatch tasks carry only name+agent, no task text', m_minimal_dispatch, None),
    'M14': ('planted session files for all ten seat names', None, 'plant'),
    'M15': ('planted session file with the line only, no session body', None, 'plant_min'),
    'M15c': ('planted session files one directory deeper (nested dispatch)', None, 'plant_nested'),
    'M16': ('both seats partly + one residual holds', m_partly_residual_holds, None),
    'M17': ('residual reads partly for a partly row', m_residual_partly, None),
    'M18': ('critic reads fails, reviewer holds', m_crit_fails, None),
    'M19': ('dispatch has no taskCall.tasks', m_no_taskcall, None),
    'M20': ('dispatch lists the same seat twice', m_dup_task, None),
    'M21': ('results list empty', m_empty_results, None),
    'M22': ('output holds but report has no line', m_report_no_line, None),
    'M23': ('output carries only another row line, report carries SC1', m_output_other_row, None),
    'M30': ('K3 fixture shape: output prefixed "done. " before the line', m_k3_shape, None),
}


def plant_sessions(names, body):
    shutil.rmtree(SESS, ignore_errors=True)
    root = os.path.join(SESS, '-Projects-shokunin', '2026-10-26T00-00-00-000Z_planted')
    os.makedirs(root, exist_ok=True)
    for name in names:
        open(os.path.join(root, f'{name}.jsonl'), 'w').write(body)


def score(name, rep, res, disp, mode):
    git(CLONE, 'checkout', '-q', '--force', '--detach', TREE)
    git(CLONE, 'clean', '-qfdx')
    open(os.path.join(CLONE, ENTRY), 'w').write(scripted_entry(counter, CLONE))
    flip_rows(CLONE, ENTRY)
    for p, t in rep.items():
        fp = os.path.join(CLONE, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, 'w').write(t)
    json.dump(res, open(os.path.join(CLONE, WAVE, 'w2-results.json'), 'w'))
    json.dump(disp, open(os.path.join(CLONE, WAVE, 'w2-dispatch.json'), 'w'))
    if mode == 'plant':
        plant_sessions([n for n, _r, _w in seats()],
                       '{"role":"assistant","content":"' +
                       '\\n'.join(f'ROW SC{i} VERDICT: holds' for i in range(1, 6)) + '"}\n')
    elif mode == 'plant_min':
        plant_sessions([n for n, _r, _w in seats()],
                       '\n'.join(f'ROW SC{i} VERDICT: holds' for i in range(1, 6)) + '\n')
    elif mode == 'plant_nested':
        shutil.rmtree(SESS, ignore_errors=True)
        root = os.path.join(SESS, '-Projects-shokunin', '2026-10-26T00-00-00-000Z_planted', 'L1Parent')
        os.makedirs(root, exist_ok=True)
        for nm, _r, _w in seats():
            open(os.path.join(root, f'{nm}.jsonl'), 'w').write(
                '\n'.join(f'ROW SC{i} VERDICT: holds' for i in range(1, 6)) + '\n')
    else:
        shutil.rmtree(SESS, ignore_errors=True)
        os.makedirs(SESS, exist_ok=True)
    git(CLONE, 'add', '-A')
    subprocess.run(['git', '-C', CLONE, *IDT, 'commit', '-q', '--allow-empty', '-m', f'mutant {name}'],
                   check=True, capture_output=True)
    rev = git(CLONE, 'rev-parse', 'HEAD').stdout.strip()
    sessarg = os.path.join(SESS, '-Projects-shokunin') if mode else os.path.join(SESS, 'empty-none')
    os.makedirs(sessarg, exist_ok=True)
    cpath = os.environ.get('C2COUNT', os.path.join(S, 'c2counter.py'))
    p = subprocess.run([sys.executable, cpath, '--revision', rev,
                        '--lane', CLONE, '--sessions', sessarg], capture_output=True, text=True)
    out = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else '{}'
    try:
        r = json.loads(out)
    except ValueError:
        r = {'unparsed': out, 'stderr': p.stderr[-500:]}
    rec = {'mutant': name, 'exit': p.returncode, 'revision': rev, 'result': r}
    tag = os.path.basename(cpath).replace('c2counter', 'C') or 'C'
    with open(os.path.join(OUT, f'{name}{tag}.jsonl'), 'w') as f:
        f.write(json.dumps(rec, sort_keys=True) + '\n')
    pr = r.get('per_row', {})
    print(f"{name:4s} exit={p.returncode} verdict={r.get('verdict')} v_ok={r.get('verdicts_ok')} "
          f"tb={r.get('transcripts_bound')}/{r.get('transcripts_checked')} "
          f"SC1={pr.get('SC1', {}).get('verdicts')} SC3v_ok={pr.get('SC3', {}).get('verdict_ok')}", flush=True)
    return rec


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(SESS, exist_ok=True)
    shutil.rmtree(CLONE, ignore_errors=True)
    subprocess.run(['git', 'clone', '-q', '--shared', LANE, CLONE], check=True)
    top = git(CLONE, 'rev-parse', '--show-toplevel').stdout.strip()
    if os.path.realpath(top) != os.path.realpath(CLONE):
        raise SystemExit(f'fixture toplevel mismatch: {top}')
    git(CLONE, 'remote', 'remove', 'origin')
    which = sys.argv[1:] or list(MUT)
    out = {}
    for name in which:
        desc, fn, mode = MUT[name]
        rep, res, disp = base_files()
        if fn:
            fn(rep, res, disp)
        rec = score(name, rep, res, disp, mode)
        out[name] = {'desc': desc, 'exit': rec['exit'], 'verdict': rec['result'].get('verdict'),
                     'verdicts_ok': rec['result'].get('verdicts_ok'),
                     'transcripts': [rec['result'].get('transcripts_bound'), rec['result'].get('transcripts_checked')],
                     'per_row': {k: v.get('verdicts') for k, v in rec['result'].get('per_row', {}).items()}}
    json.dump(out, open(os.path.join(OUT, 'summary.json'), 'w'), indent=1, sort_keys=True)


if __name__ == '__main__':
    counter = load_counter(os.path.join(S, 'c2counter.py')) if os.path.exists(os.path.join(S, 'c2counter.py')) else None
    if counter is None:
        open(os.path.join(S, 'c2counter.py'), 'wb').write(
            subprocess.run(['git', '-C', LANE, 'show', 'a84fc9dec860f8bea516dff7ddfdc98223cdae52:tools/check-scrub-record-r42.py'],
                           check=True, capture_output=True).stdout)
        counter = load_counter(os.path.join(S, 'c2counter.py'))
    main()
