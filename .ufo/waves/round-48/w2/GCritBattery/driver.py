#!/usr/bin/env python3
"""GCritBattery: C2 pre-data battery attack fixtures.
Each fixture = shared clone of the lane @ BASE, mutated per spec, committed inside the clone,
then scored with the FROZEN counter (extracted at ae99f021). Receipts -> receipts dir.
"""
import json, os, shutil, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '5fdf062f969292736e36513e39f98b1b8de43635'
ROOT = '/fast/scratch/hyaku/tsukuroi-r48/GCritBattery'
COUNTER = os.path.join(ROOT, 'frozen-counter.py')
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
W = '.ufo/waves/round-48'
ROWS = ('GR1', 'GR2', 'GR3')
CITE = {'GR1': 'cmdline.c:100', 'GR2': 'dev-replace.c:1126', 'GR3': 'systemd.kill.xml:10'}
RECEIPTS = sys.argv[1]


def git(d, *a, inp=None):
    return subprocess.run(['git', '-C', d, '-c', 'user.name=ctl', '-c', 'user.email=ctl@sandbox.invalid', *a],
                          capture_output=True, input=inp, check=True).stdout


def counter(d, rev, *extra):
    p = subprocess.run(['python3', COUNTER, '--revision', rev, '--lane', d, *extra], capture_output=True)
    try:
        return p.returncode, json.loads(p.stdout.decode() or '{}')
    except json.JSONDecodeError:
        return p.returncode, {'_raw_stdout': p.stdout.decode(errors='replace'), '_stderr': p.stderr.decode(errors='replace')}


def seats(row):
    n = row[2:]
    return ([(f'R48RevGR{n}{x}', 'reviewer') for x in 'abc']
            + [(f'R48CritGR{n}{x}', 'critic') for x in 'abc'])


def clone(root, name):
    d = os.path.join(root, name)
    subprocess.run(['git', 'clone', '-q', '--shared', LANE, d], check=True)
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                         capture_output=True, check=True).stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    git(d, 'checkout', '-q', '--detach', BASE)
    return d


def write_marks(d, fence=False, readme_line=None):
    entry_p = os.path.join(d, ENTRY)
    skill_p = os.path.join(d, 'SKILL.md')
    readme_p = os.path.join(d, 'corpus/README.md')
    rl = readme_line if readme_line is not None else '- btrfs-scrub-grounding-r45.md admitted round 48'
    if fence:
        with open(entry_p, 'a', encoding='utf-8') as f:
            f.write('\nExample of what a real gate mark would look like (quoted, not asserted):\n\n```text\n## Gate status - round 48 (GR1-GR3 admitted)\n```\n'.replace('## Gate status - round 48', '## Gate status — round 48'))
        with open(skill_p, 'a', encoding='utf-8') as f:
            f.write('\nQuoted example of the SKILL mark:\n\n```text\n## Scrub grounding — round 48 admission\n```\n')
        with open(readme_p, 'a', encoding='utf-8') as f:
            f.write('\nQuoted example of a README mark line:\n\n```text\n' + rl + '\n```\n')
    else:
        with open(entry_p, 'a', encoding='utf-8') as f:
            f.write('\n## Gate status — round 48 (GR1-GR3 admitted)\n')
        with open(skill_p, 'a', encoding='utf-8') as f:
            f.write('\n## Scrub grounding — round 48 admission\n')
        with open(readme_p, 'a', encoding='utf-8') as f:
            f.write('\n' + rl + '\n')


def body_for(seat, row, extra=''):
    return (f'Checked every clause of {row} against the pinned snapshots; seat {seat} verified its clause. '
            f'Evidence line {CITE[row]} read verbatim. ' + 'The row clause matches its cited line. ' * 12 + extra)


def seat_report(row, verdict, h, body, crlf=False):
    text = f'ROW {row} VERDICT: {verdict}\nSECTION SHA256: {h}\n{body}\n'
    if crlf:
        text = text.replace('\n', '\r\n')
    return text


def cohort(d, hashes, *, hash_for=None, verdict_for=None, body_extra=None, crlf=False,
           role_swap=False, dispatch=True, results=True):
    tasks, results_l = [], []
    os.makedirs(os.path.join(d, W, 'w2'), exist_ok=True)
    for row in ROWS:
        for seat, role in seats(row):
            verdict = (verdict_for or {}).get(seat, 'holds')
            h = (hash_for or {}).get(seat, hashes[row])
            body = body_for(seat, row, extra=(body_extra or {}).get(seat, ''))
            with open(os.path.join(d, W, 'w2', seat + '.md'), 'w', encoding='utf-8', newline='') as f:
                f.write(seat_report(row, verdict, h, body, crlf=crlf))
            agent = {'reviewer': 'critic', 'critic': 'reviewer'}[role] if role_swap else role
            if dispatch:
                tasks.append({'name': seat, 'agent': agent})
            if results:
                results_l.append({'name': seat, 'agent': agent, 'status': 'done'})
    json.dump({'taskCall': {'tasks': tasks}}, open(os.path.join(d, W, 'w2-dispatch.json'), 'w'))
    json.dump({'results': results_l}, open(os.path.join(d, W, 'w2-results.json'), 'w'))


def commit(d, msg):
    git(d, 'add', '-A')
    git(d, 'commit', '-q', '-m', msg)
    return git(d, 'rev-parse', 'HEAD').decode().strip()


def summarize(label, want, r):
    legs = {k: r.get(k) for k in ('structural_ok', 'quotes_ok', 'verdicts_ok', 'marks_ok')}
    per = {}
    for row in ROWS:
        pr = (r.get('per_row') or {}).get(row) or {}
        per[row] = {'row_ok': pr.get('row_ok'), 'credited': pr.get('credited'),
                    'blocking': pr.get('blocking'), 'any_fails': pr.get('any_fails'),
                    'unbound': pr.get('unbound_for_citation')}
        # capture first-seat detail as the binding mechanism fingerprint
        st = pr.get('seats') or {}
        for sn in sorted(st):
            if st[sn].get('detail') not in (None,) and (st[sn]['detail'].startswith('w2/') is False):
                per[row].setdefault('unbound_detail', {})[sn] = st[sn]['detail']
    return {'case': label, 'expected': want, 'verdict': r.get('verdict'), 'as_expected': r.get('verdict') == want,
            'legs': legs, 'per_row': per}


def main():
    os.makedirs(RECEIPTS, exist_ok=True)
    rc, hs = counter(LANE, BASE, '--section-hash')
    hashes = hs['section_sha256']
    print('BASE section hashes:', json.dumps(hashes, sort_keys=True), flush=True)
    rot = {'GR1': 'GR2', 'GR2': 'GR3', 'GR3': 'GR1'}
    out = []

    def run_case(label, want, fn):
        d = clone(ROOT, 'fx-' + label.split()[0].lower().replace('/', '_'))
        fn(d)
        rev = commit(d, 'fixture ' + label)
        rc, r = counter(d, rev)
        with open(os.path.join(RECEIPTS, f'fx-{label.split()[0].lower()}-counter.json'), 'w') as f:
            json.dump(r, f, indent=1, sort_keys=True)
        diff = git(d, 'diff', BASE, rev)
        with open(os.path.join(RECEIPTS, f'fx-{label.split()[0].lower()}-diff.patch'), 'wb') as f:
            f.write(diff)
        out.append(summarize(label, want, r))
        print(label, '->', r.get('verdict'), 'want', want, flush=True)
        shutil.rmtree(d)

    # 1. wrong-row real section hash (sibling hash swap, real snapshot citations)
    run_case('hashswap seats cite real lines but carry another row\'s section hash', 'FAIL',
             lambda d: (write_marks(d),
                        cohort(d, hashes, hash_for={s: hashes[rot[r]] for r in ROWS for s, _ in seats(r)})))

    # 2. all reports CRLF
    run_case('crlf all 18 reports written with CRLF line endings', 'FAIL',
             lambda d: (write_marks(d), cohort(d, hashes, crlf=True)))

    # 3. CRLF only in the body (headers LF)
    run_case('crlfbody headers LF, body lines CRLF', 'PASS',
             lambda d: (write_marks(d),
                        cohort(d, hashes,
                               body_extra={s: ('\r\n' + 'extra body line' * 30 + '\r\n')
                                           for r in ROWS for s, _ in seats(r)})))

    # 4. counted names dispatched with the wrong agent role (all seats swapped)
    run_case('roleswap counted names dispatched with swapped agent role', 'FAIL',
             lambda d: (write_marks(d), cohort(d, hashes, role_swap=True)))

    # 5. results.json entries present without any dispatch entry
    run_case('resultsonly reports plus results.json entries but empty dispatch', 'FAIL',
             lambda d: (write_marks(d), cohort(d, hashes, dispatch=False)))

    # 6. all three marks written only inside fenced code blocks (verbatim lines)
    run_case('fencemarks all three marks inside fenced code blocks, full cohort', 'PASS?',
             lambda d: (write_marks(d, fence=True), cohort(d, hashes)))

    # 7. README negation outside the denylist: 'not yet admitted'
    run_case('readmeslip README line reads "not yet admitted", entry+skill marks real', 'PASS?',
             lambda d: (write_marks(d, readme_line='- btrfs-scrub-grounding-r45.md not yet admitted round 48'),
                        cohort(d, hashes)))

    # 8. stale-hash verdict asymmetry: GR1 critic 'partly' on GR3's real hash (no block expected);
    #    GR2 critic 'fails' on GR1's real hash (blocks anyway via any_fails)
    def stale(d):
        write_marks(d)
        cohort(d, hashes,
               verdict_for={'R48CritGR1a': 'partly', 'R48CritGR2a': 'fails'},
               hash_for={'R48CritGR1a': hashes['GR3'], 'R48CritGR2a': hashes['GR1']})
    run_case('staleverdicts partly on GR3 hash vs fails on GR1 hash', 'FAIL', stale)

    # 9. body quotes a TRUE sibling verdict line (foreign ROW VERDICT token)
    def foreign(d):
        write_marks(d)
        cohort(d, hashes,
               body_extra={'R48RevGR1a': '\nPeer report R48CritGR2a.md line 1 reads verbatim: '
                                        '"ROW GR2 VERDICT: holds". ' + 'x' * 40})
    run_case('foreignverdict GR1 reviewer body quotes true GR2 verdict line', 'FAIL', foreign)

    with open(os.path.join(RECEIPTS, 'gcritbattery-summary.jsonl'), 'w') as f:
        for s in out:
            f.write(json.dumps(s) + '\n')
    print('done', len(out), 'fixtures')


if __name__ == '__main__':
    main()
