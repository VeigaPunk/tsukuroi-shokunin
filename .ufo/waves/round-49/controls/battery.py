#!/usr/bin/env python3
"""Round-49 pre-data control battery (frozen counters; run BEFORE wave w1 is dispatched).

Scores each frozen counter against fixtures that skip the claimed work, and against a full
K-pass fixture set. Every receipt line is the counter's own JSON plus the control name.

Usage: python3 .ufo/waves/round-49/controls/battery.py <FREEZE-sha> [c1|c2|c3 ...]
Writes .ufo/waves/round-49/controls/battery-summary-r49-<claim>.jsonl
Scratch: $HYAKU_SCRATCH/tsukuroi-r49/controls/<claim>/ (removed at the end).
"""
import json
import os
import re
import shutil
import subprocess
import sys

FREEZE = sys.argv[1]
REV = os.environ.get('BATTERY_REV', FREEZE)
WANT = sys.argv[2:] or ['c1', 'c2', 'c3']
L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
W = f'{L}/.ufo/waves/round-49'
CTL = f'{W}/controls'
BASE = '6256760d1382ce4ce20fcba830d4b2912cfbf12b'
ENTER = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
PROV = 'PROVINCE.md'
CEN = 'tools/tsukuroi-census.sh'
C1C = f'{L}/tools/check-scrub-admission-r49.py'
C2C = f'{L}/tools/check-adjacency-table-r49.py'
C3C = f'{L}/tools/check-fd-band-r49.py'
SC = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'tsukuroi-r49', 'controls')
CITE = {'GR1': 'cmdline.c:147', 'GR2': 'dev-replace.c:700', 'GR3': 'scrub.c:3094'}
MARK_ENTRY = '## Gate status — round 49 (GR1-GR3 admitted)'
MARK_SKILL = '## Scrub grounding — round 49 admission'
README_SENT = ('The btrfs scrub grounding entry `corpus/knowledge/btrfs-scrub-grounding-r45.md` is '
               'admitted round 49 for GR1-GR3 by the counted cohort.')
PAD = (' The reading was checked against the pinned snapshot lines named above and against the errno '
       'ordering the row states; nothing in the row contradicts the bytes that were read, and the host '
       'reading remains marked where the capture does not decide it. This paragraph is padding so the '
       'body clears the counter floor without adding a second citation.')
FORBID = ['leading `0x` followed by a hex digit', 'which by SR7',
          'dev-replace.c:1171-1199', 'only sets the state to SUSPENDED',
          'which it is for a previous replace in state']


def git(*args, rev=None):
    cmd = ['git', '-C', L] + list(args)
    return subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL)


def blob(rev, path):
    p = git('show', f'{rev}:{path}')
    assert p.returncode == 0, f'show {rev}:{path} rc={p.returncode}'
    return p.stdout.decode('utf-8')


def jrun(cmd, timeout=1800):
    p = subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL, text=True, timeout=timeout)
    line = (p.stdout or '').strip().split('\n')[-1] if p.stdout.strip() else '{}'
    try:
        obj = json.loads(line)
    except Exception:
        obj = {'parse_error': True, 'raw': line[:400], 'stderr': (p.stderr or '')[:400]}
    obj['_rc'] = p.returncode
    return obj


def hashes(entry_path):
    o = jrun(['python3', C1C, '--revision', REV, '--entry-file', entry_path, '--no-base-check',
              '--section-hash'])
    return o['section_sha256'], o


def report(seat, row, verdict, entry_hash, body=None):
    cite = CITE[row]
    if body is None:
        body = (f'{seat} read row {row} at the frozen bytes. The clause chain at {cite} agrees with the '
                f'row, the quoted lines sit where the row cites them, and the host reading keeps its '
                f'inference mark where the capture does not decide it.' + PAD)
    return f'ROW {row} VERDICT: {verdict}\nSECTION SHA256: {entry_hash}\n{body}\n'


def cohort_reports(dirpath, row_hashes, verdicts=None, bodies=None):
    os.makedirs(dirpath, exist_ok=True)
    for row in ('GR1', 'GR2', 'GR3'):
        n = row[2:]
        for prefix in ('Rev', 'Crit'):
            for letter in 'abc':
                seat = f'R49{prefix}{row}{letter}'
                v = 'holds'
                if verdicts and seat in verdicts:
                    v = verdicts[seat]
                body = None
                if bodies and seat in bodies:
                    body = bodies[seat]
                with open(os.path.join(dirpath, f'{seat}.md'), 'w') as fh:
                    fh.write(report(seat, row, v, row_hashes[row], body))


def results_file(path, names, agent_of, skip=(), empty=()):
    res = {'lane': 'tsukuroi', 'round': 49, 'wave': 'w1', 'seats': len(names), 'results': []}
    for n in names:
        if n in skip:
            continue
        res['results'].append({'name': n, 'agent': agent_of(n), 'output': '' if n in empty else 'ok',
                               'note': None})
    with open(path, 'w') as fh:
        json.dump(res, fh)
    return path


def agent_of(seat):
    return 'reviewer' if 'Rev' in seat else 'critic'


def c1(batt):
    d = os.path.join(batt, 'c1')
    os.makedirs(d, exist_ok=True)
    entry = blob(FREEZE, ENTER)
    skill = blob(FREEZE, 'SKILL.md')
    readme = blob(FREEZE, 'corpus/README.md')
    fy = os.path.join(d, 'entry.md')
    fs = os.path.join(d, 'skill.md')
    fr = os.path.join(d, 'readme.md')
    open(fy, 'w').write(entry + '\n' + MARK_ENTRY + '\n\nadmitted round 49 by the counted cohort.\n')
    open(fs, 'w').write(skill + '\n' + MARK_SKILL + '\n')
    open(fr, 'w').write(readme + '\n' + README_SENT + '\n')
    row_hashes, hinfo = hashes(fy)
    names = [f'R49{p}GR{r}{x}' for r in '123' for p in ('Rev', 'Crit') for x in 'abc']
    out = []

    def run(name, entry_file, skill_file, readme_file, wave_dir, results, note):
        o = jrun(['python3', C1C, '--revision', REV, '--no-base-check',
                  '--entry-file', entry_file, '--skill-file', skill_file,
                  '--readme-file', readme_file, '--wave-dir', wave_dir, '--results-file', results])
        o['control'] = name
        o['note'] = note
        out.append(o)
        print(name, o.get('verdict'), {k: o.get(k) for k in
              ('structural_ok', 'corr_ok', 'quotes_ok', 'verdicts_ok', 'seats_ok', 'marks_ok')})

    empty_dir = os.path.join(d, 'empty')
    os.makedirs(empty_dir, exist_ok=True)
    res_missing = results_file(os.path.join(d, 'res-empty.json'), [], agent_of)
    # K0: base bytes, no cohort, no marks
    base_entry = os.path.join(d, 'entry-base.md')
    base_skill = os.path.join(d, 'skill-base.md')
    base_readme = os.path.join(d, 'readme-base.md')
    open(base_entry, 'w').write(blob(BASE, ENTER))
    open(base_skill, 'w').write(blob(BASE, 'SKILL.md'))
    open(base_readme, 'w').write(blob(BASE, 'corpus/README.md'))
    run('K0', base_entry, base_skill, base_readme, empty_dir, res_missing,
        'base bytes, no cohort, no marks -> FAIL')
    # K1: corrected entry + marks, no cohort
    run('K1', fy, fs, fr, empty_dir, res_missing, 'corrected entry + marks, no cohort -> FAIL')
    # K2: defect strings restored, full clean cohort
    k2 = os.path.join(d, 'entry-k2.md')
    open(k2, 'w').write(entry + '\n' + MARK_ENTRY + '\n\n' +
                        '\n'.join(FORBID) + '\n')
    k2h, _ = hashes(k2)
    k2dir = os.path.join(d, 'cohort-k2')
    cohort_reports(k2dir, k2h)
    k2res = results_file(os.path.join(d, 'res-k2.json'), names, agent_of)
    run('K2', k2, fs, fr, k2dir, k2res, 'clean cohort on bytes carrying the r48 defect strings -> FAIL (corr_ok 0)')
    # K3: one bound partly
    k3dir = os.path.join(d, 'cohort-k3')
    cohort_reports(k3dir, row_hashes, verdicts={'R49CritGR2b': 'partly'})
    k3res = results_file(os.path.join(d, 'res-k3.json'), names, agent_of)
    run('K3', fy, fs, fr, k3dir, k3res, 'one bound partly -> FAIL (blocks GR2)')
    # K4: two identical bodies
    body = report('dup', 'GR1', 'holds', row_hashes['GR1'])
    k4dir = os.path.join(d, 'cohort-k4')
    cohort_reports(k4dir, row_hashes, bodies={'R49RevGR1a': body.split('\n', 2)[2],
                                             'R49RevGR1b': body.split('\n', 2)[2]})
    k4res = results_file(os.path.join(d, 'res-k4.json'), names, agent_of)
    run('K4', fy, fs, fr, k4dir, k4res, 'two byte-identical bodies -> FAIL (distinct_bodies)')
    # K5: reviewers only (critics' files absent)
    k5dir = os.path.join(d, 'cohort-k5')
    cohort_reports(k5dir, row_hashes)
    for n in names:
        if n.startswith('R49Crit'):
            os.remove(os.path.join(k5dir, f'{n}.md'))
    k5res = results_file(os.path.join(d, 'res-k5.json'), names, agent_of)
    run('K5', fy, fs, fr, k5dir, k5res, 'reviewers only, critics unbound -> FAIL')
    # K6: reports present, results entries missing
    full = os.path.join(d, 'cohort-full')
    cohort_reports(full, row_hashes)
    k6res = results_file(os.path.join(d, 'res-k6.json'), names, agent_of, skip=set(names[:6]))
    run('K6', fy, fs, fr, full, k6res, 'six results entries absent -> FAIL (seats_ok < 18)')
    # K-pass
    kpres = results_file(os.path.join(d, 'res-pass.json'), names, agent_of)
    run('K-pass', fy, fs, fr, full, kpres, 'corrected entry + marks + 18 reports/results -> PASS')
    return out


def c2(batt):
    d = os.path.join(batt, 'c2')
    os.makedirs(d, exist_ok=True)
    base_prov = blob(BASE, PROV)
    freeze_prov = blob(FREEZE, PROV)
    out = []

    def write(name, text):
        p = os.path.join(d, f'{name}.md')
        open(p, 'w').write(text)
        return p

    def run(name, prov, skip_check, note):
        cmd = ['python3', C2C, '--revision', REV, '--no-base-check', '--province-file', prov]
        if skip_check:
            cmd.append('--skip-anchors-check')
        o = jrun(cmd)
        o['control'] = name
        o['note'] = note
        out.append(o)
        print(name, o.get('verdict'), {k: o.get(k) for k in
              ('adj_rows', 'linked_rows', 'bare_ranges', 'anchors_ok', 'registry_ok', 'anchors_checker_rc')})

    run('K0', write('prov-base', base_prov), True, 'base province (9 bare ranges) -> FAIL')
    # K1: links added, ranges kept
    k1 = base_prov
    for rid, outs in (('ADJ-01', 'OUT-002'), ('ADJ-02', 'OUT-003'), ('ADJ-03', 'OUT-004'),
                      ('ADJ-04', 'OUT-005'), ('ADJ-05', 'OUT-006, OUT-007'),
                      ('ADJ-06', 'OUT-008, OUT-009'), ('ADJ-07', 'OUT-010')):
        k1 = re.sub(r'(\| ' + rid + r' \|.*?)\| (`\.\./[^|]+?`) \|', r'\1| \2, `' + outs + r'` |', k1)
    run('K1', write('prov-k1', k1), True, 'anchors added, bare ranges kept -> FAIL')
    # K2: one nonexistent OUT id
    run('K2', write('prov-k2', freeze_prov.replace('`OUT-003`', '`OUT-099`')), True,
        'ADJ-02 points at OUT-099 (absent) -> FAIL')
    # K3: every row pointed at OUT-001 (wrong class)
    k3 = freeze_prov
    for rid in ('ADJ-02', 'ADJ-03', 'ADJ-04', 'ADJ-05', 'ADJ-06', 'ADJ-07'):
        k3 = re.sub(r'(\| ' + rid + r' \|.*)\| `OUT-0\d\d`(, `OUT-0\d\d`)? \|', r'\1| `OUT-001` |', k3)
    run('K3', write('prov-k3', k3), True, 'every row linked to OUT-001 (Core pointer) -> FAIL (class)')
    run('K-pass', write('prov-pass', freeze_prov), False,
        'the freeze province with the live anchor checker -> PASS')
    return out


def c3(batt):
    d = os.path.join(batt, 'c3')
    os.makedirs(d, exist_ok=True)
    base_cen = blob(BASE, CEN)
    freeze_cen = blob(FREEZE, CEN)
    out = []

    def run(name, text, note):
        p = os.path.join(d, f'{name}.sh')
        open(p, 'w').write(text)
        o = jrun(['python3', C3C, '--revision', REV, '--census-file', p,
                  '--work', os.path.join(batt, 'c3work')])
        o['control'] = name
        o['note'] = note
        out.append(o)
        print(name, o.get('verdict'), {k: o.get(k) for k in
              ('stale_ok', 'diag_ok', 'band_ok', 'cases', 'selftest_rc')})

    run('K0', base_cen, 'base census: stale comment, no diagnostic, 166 cases -> FAIL')
    lines = freeze_cen.split('\n')
    if any('(R49-C3)' in ln for ln in lines):
        i = next(k for k, ln in enumerate(lines) if ln.lstrip().startswith('# (R49-C3)'))
        j = next(k for k, ln in enumerate(lines) if ln.startswith('  unset r49_dir r49_held'))
        k1 = '\n'.join(lines[:i] + lines[j + 1:])
    else:
        k1 = freeze_cen
    run('K1', k1, 'diagnostic present, the R49-C3 case removed -> FAIL (band_ok 0)')
    run('K2', freeze_cen.replace(
        '  # Hermetic selftest: `--selftest` builds a fixture tree under the resolved base',
        '  # Hermetic selftest: `--selftest` builds a /tmp fixture tree with a dispatcher stub for'),
        'stale comment restored -> FAIL (stale_ok 0)')
    run('K-pass', freeze_cen, 'the freeze census -> PASS (167 cases)')
    return out


def main():
    os.makedirs(SC, exist_ok=True)
    batt = SC
    try:
        for claim in WANT:
            out = {'c1': c1, 'c2': c2, 'c3': c3}[claim](batt)
            with open(f'{CTL}/battery-summary-r49-{claim}.jsonl', 'w') as fh:
                for o in out:
                    fh.write(json.dumps(o, sort_keys=True) + '\n')
    finally:
        shutil.rmtree(batt, ignore_errors=True)


if __name__ == '__main__':
    main()
