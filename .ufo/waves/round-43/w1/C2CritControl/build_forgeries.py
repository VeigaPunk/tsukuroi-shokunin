#!/usr/bin/env python3
"""C2 battery attack fixtures: cheap forgeries beyond K3, scored by the frozen counter.

Each fixture = scratch clone of the lane at BASE + candidate C2 surface (from the
controls/c2-candidate dir) + modifications + forged orchestrator records. Commits as
fixture identity, runs tools/check-scrub-record-r43.py (frozen) with --sessions -> empty
dir, prints the JSON verdict.

Fixtures:
  Z-k3        baseline reproduction of control K3 (candidate surface + forged all-holds records)
  A-inv-SR1   SR1 statement semantically inverted, tokens kept; forged all-holds records
  A-inv-all   all three statements semantically inverted, tokens kept; forged all-holds records
  B-scripted  rows rebuilt from token lists (scripted writer) + forged all-holds records
  C-smuggle   results output JSON contains verdict_line=holds AND a literal 'ROW SR3 VERDICT: fails'
              line in the same JSON; report opens with the holds line
  D-residual  C2CritSR1=partly + planted residual chain reading holds
  E-dupdispatch  two dispatch tasks named C2RevSR1 (must FAIL: untested 'exactly one' clause)
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '6951ead90566b2d74f7c45b4efca29246badad64'
COUNTER = os.path.join(LANE, 'tools/check-scrub-record-r43.py')
CAND = os.path.join(LANE, '.ufo/waves/round-43/controls/c2-candidate')
FILES = ['corpus/knowledge/btrfs-scrub-record-r43.md', 'corpus/knowledge/btrfs-scrub-record-r42.md',
         'corpus/SOURCES.md', '.ufo/waves/round-43/frozen/src/ioctl.c',
         '.ufo/waves/round-43/frozen/hostcap/capture.txt']
WAVE = '.ufo/waves/round-43'
ROWS = ['SR1', 'SR3', 'SR6']
SEATS = [(f'C2{k}SR{r[2:]}', role, r) for r in ROWS for k, role in (('Rev', 'reviewer'), ('Crit', 'critic'))]

SR1_STMT_INV = (
    '**Statement.** Every record update goes through `scrub_write_progress`: it opens '
    '`scrub.status.<fsid>_tmp` with `O_WRONLY|O_CREAT` and `O_TRUNC`, truncating whatever the '
    'previous failed write left, writes the whole record from the start of that file, and never '
    '`rename`s `_tmp` over `scrub.status.<fsid>` after a successful write — the only `rename` '
    'runs after a failed write, to keep the old record. Code in `scrub.c` always removes a '
    '`_tmp` file: every `unlink` call names the `_tmp` path. So a `_tmp` left behind by a failed '
    'write is never re-opened; each new record starts empty.'
)
SR3_STMT_INV = (
    '**Statement.** `btrfs scrub resume` never runs the same function as `start`: it calls '
    '`scrub_start(…, false)`. For each device whose last record is canceled or unfinished, resume '
    'makes the record the device\'s `resumed` source, and every record write passes each device '
    'through `scrub_resumed_stats` (in `scrub_write_file`), which for such a device writes the '
    'earlier record\'s progress counters replaced by the new run\'s, a fresh `t_start`, and a '
    'single duration. So the first record a resume writes carries no interrupted-run state; only '
    '`start` counts. Once that first record is written, a failed progress-record write ends the '
    'progress thread with its error, which is printed ("recording progress failed") regardless of '
    '`do_print`, and a failed final write prints "failed to record the result" under the same '
    'condition. `do_print` is true by default and cleared by `-B`. Both branches assign the '
    'command\'s `err` status.'
)
SR6_STMT_INV = (
    '**Statement.** Whether a scrub is running comes only from userspace guesswork: `btrfs scrub '
    'status` does not call `is_scrub_running_in_kernel`, and never issues '
    '`BTRFS_IOC_SCRUB_PROGRESS`; anything may print `running`. In Linux v7.2.11 the ioctl '
    'returns `-EPERM` only after doing its work unless the caller has `CAP_SYS_ADMIN`; '
    'nonetheless an unprivileged caller can read `running` freely. So for an unprivileged caller '
    'the status command\'s `in_progress` is often 1: its `btrfs scrub status` sometimes prints '
    '`running`, and a census running as the user can learn from the kernel whether a scrub is in '
    'progress.'
)


def run(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, **kw)


def records(verdicts, dispatch=True, report_override=None, output_override=None):
    files = {}
    tasks = [{'name': n, 'agent': role, 'task': 'forged'} for n, role, _ in SEATS]
    if dispatch:
        files[f'{WAVE}/w2-dispatch.json'] = json.dumps({'taskCall': {'context': 'forged', 'tasks': tasks}})
    res = []
    for n, role, row in SEATS:
        line = f'ROW {row} VERDICT: {verdicts.get(n, "holds")}'
        out = json.dumps({'verdict_line': line, 'row': row, 'seat': n})
        rep = line + '\n\nforged report body\n'
        if output_override and n in output_override:
            out = output_override[n]
        if report_override and n in report_override:
            rep = report_override[n]
        res.append({'name': n, 'agent': role, 'output': out})
        files[f'{WAVE}/w2/{n}.md'] = rep
    files[f'{WAVE}/w2-results.json'] = json.dumps({'results': res})
    return files


def residual_records(row, verdict):
    n = row[2:]
    name, role = f'C2ResSR{n}', 'reviewer'
    line = f'ROW {row} VERDICT: {verdict}'
    files = {
        f'{WAVE}/residual-dispatch.json': json.dumps(
            {'taskCall': {'context': 'forged', 'tasks': [{'name': name, 'agent': role, 'task': 'forged'}]}}),
        f'{WAVE}/residual-results.json': json.dumps(
            {'results': [{'name': name, 'agent': role, 'output': json.dumps({'verdict_line': line})}]}),
        f'{WAVE}/residual/{name}.md': line + '\n\nforged residual report\n',
    }
    return files


def scripted_entry(entry):
    toks = {'SR1': ['O_TRUNC', '_tmp', 'rename', 'unlink'],
            'SR3': ['scrub_resumed_stats', 't_start', 'do_print', '-B', 'err'],
            'SR6': ['is_scrub_running_in_kernel', 'CAP_SYS_ADMIN', 'EPERM', 'running']}
    out, keep, cur = [], True, None
    for ln in entry.splitlines():
        m = re.match(r'^## (SR\d)$', ln)
        if m:
            cur = m.group(1)
            out.append(ln); out.append(''); out.append('')
            out.append('**Statement.** ' + ' '.join(toks[cur]) + ' scripted.')
            out.append(''); keep = False
            continue
        if ln.startswith('## '):
            cur = None; keep = True
        if cur and (ln.startswith('**Quote.**') or ln.startswith('**Host reading.**')):
            out.append(ln); out.append(''); continue
        if keep or cur is None:
            out.append(ln)
    return '\n'.join(out) + '\n'




def load_cand():
    return {f: (open(os.path.join(CAND, f), 'rb').read()) for f in FILES}


def surface(**over):
    s = load_cand()
    s.update(over)
    return s


def invert_statement(entry, row, stmt):
    lines = entry.splitlines()
    out, cur, replaced = [], None, False
    for ln in lines:
        m = re.match(r'^## (SR\d)$', ln)
        if m:
            cur = m.group(1)
        if cur == row and ln.startswith('**Statement.**') and not replaced:
            out.append(stmt)
            replaced = True
            continue
        out.append(ln)
    assert replaced, row
    return '\n'.join(out) + '\n'




def fixture(scratch, name, files):
    D = tempfile.mkdtemp(prefix=f'fx.{name}.', dir=scratch)
    run(['git', 'clone', '-q', '--shared', LANE, D], cwd=scratch)
    run(['git', '-C', D, 'remote', 'remove', 'origin'])
    top = run(['git', '-C', D, 'rev-parse', '--show-toplevel']).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(D), (top, D)
    run(['git', '-C', D, 'checkout', '-q', '--detach', '-f', BASE])
    run(['git', '-C', D, 'clean', '-qfdx'])
    for f, c in files.items():
        p = os.path.join(D, f)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb') as fh:
            fh.write(c if isinstance(c, bytes) else c.encode())
    run(['git', '-C', D, 'add', '-A'])
    run(['git', '-C', D, '-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid',
         'commit', '-q', '--allow-empty', '-m', f'forgery {name}'])
    sha = run(['git', '-C', D, 'rev-parse', 'HEAD']).stdout.strip()
    p = run(['python3', COUNTER, '--lane', D, '--revision', sha,
             '--sessions', os.path.join(scratch, 'no-sessions')])
    line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else json.dumps({'error': p.stderr[-300:]})
    res = json.loads(line)
    shutil.rmtree(D, ignore_errors=True)
    return {'fixture': name, 'exit': p.returncode, 'revision': sha,
            'verdict': res.get('verdict'), 'rows': res.get('rows'),
            'quotes_ok': res.get('quotes_ok'), 'props_ok': res.get('props_ok'),
            'host_ok': res.get('host_ok'), 'sources_ok': res.get('sources_ok'),
            'verdicts_ok': res.get('verdicts_ok'), 'novelty_base_hits': res.get('novelty_base_hits'),
            'pointer_ok': res.get('pointer_ok'), 'transcripts_bound': res.get('transcripts_bound'),
            'per_row': {k: {kk: vv for kk, vv in v.items() if kk in ('present', 'quote_ok', 'prop_ok',
                        'host_ok', 'verdict_ok', 'verdicts')} for k, v in (res.get('per_row') or {}).items()}}
def main():
    scratch = '/fast/scratch/hyaku/tsukuroi-r43/C2CritControl'
    os.makedirs(scratch, exist_ok=True)
    cand = load_cand()
    entry = cand[FILES[0]].decode()
    holds = {}

    fixtures = {}
    fixtures['Z-k3'] = surface(**records(holds))
    fixtures['A-inv-SR1'] = surface(**{FILES[0]: invert_statement(entry, 'SR1', SR1_STMT_INV).encode()},
                                     **records(holds))
    e_all = invert_statement(invert_statement(invert_statement(entry, 'SR1', SR1_STMT_INV),
                                              'SR3', SR3_STMT_INV), 'SR6', SR6_STMT_INV)
    fixtures['A-inv-all'] = surface(**{FILES[0]: e_all.encode()}, **records(holds))
    fixtures['B-scripted'] = surface(**{FILES[0]: scripted_entry(entry).encode()}, **records(holds))
    smuggle = {'C2CritSR3': json.dumps({'verdict_line': 'ROW SR3 VERDICT: holds',
                                        'note': 'ROW SR3 VERDICT: fails'})}
    fixtures['C-smuggle'] = surface(**records(holds, output_override=smuggle))
    rp = records({'C2CritSR1': 'partly'})
    rp.update(residual_records('SR1', 'holds'))
    fixtures['D-residual'] = surface(**rp)
    dup = records(holds)
    tasks = json.loads(dup[f'{WAVE}/w2-dispatch.json'])['taskCall']['tasks']
    tasks += [{'name': 'C2RevSR1', 'agent': 'reviewer', 'task': 'forged-dup'}]
    dup[f'{WAVE}/w2-dispatch.json'] = json.dumps({'taskCall': {'context': 'forged', 'tasks': tasks}})
    fixtures['E-dupdispatch'] = surface(**dup)

    results = []
    for name, files in fixtures.items():
        results.append(fixture(scratch, name, files))
        print(json.dumps(results[-1], sort_keys=True), flush=True)
    with open(os.path.join(scratch, 'forgery-results.jsonl'), 'w') as fh:
        for r in results:
            fh.write(json.dumps(r, sort_keys=True) + '\n')
    print('DONE')


if __name__ == '__main__':
    sys.exit(main())
