#!/usr/bin/env python3
"""Round-50 pre-data control batteries (L1 TsukuroiR50). Run BEFORE any seat scores.

Usage: battery.py --freeze <REV> [--scratch <dir>] [--only c1|c2|c3]
Writes controls/battery-summary-r50-c{1,2,3}.jsonl (one JSON line per control) and exits 1 if any
control does not score as declared. Fixtures live under --scratch and are removed at the end.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
W = f'{L}/.ufo/waves/round-50'
C1 = f'{L}/tools/check-scrub-admission-r50.py'
C2 = f'{L}/tools/check-selftest-matcher-r50.py'
C3 = f'{L}/tools/check-adjacency-table-r50.py'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
BASE = 'b866a1d3d26616119a089f1a69b080136becc17b'
CITE = {'GR1': ('cmdline.c:147', 'kstrtox.c:1'),
        'GR2': ('dev-replace.c:1111', 'scrub.c:3094'),
        'GR3': ('systemd.kill.xml:1', 'btrfs-scrub@.service:1')}
ROLES = {'GR1': ('R50RevGR1a', 'R50RevGR1b', 'R50RevGR1c', 'R50CritGR1a', 'R50CritGR1b', 'R50CritGR1c'),
         'GR2': ('R50RevGR2a', 'R50RevGR2b', 'R50RevGR2c', 'R50CritGR2a', 'R50CritGR2b', 'R50CritGR2c'),
         'GR3': ('R50RevGR3a', 'R50RevGR3b', 'R50RevGR3c', 'R50CritGR3a', 'R50CritGR3b', 'R50CritGR3c')}


def git_show(rev, path):
    p = subprocess.run(['git', '-C', L, 'show', f'{rev}:{path}'], capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f'cannot read {path} at {rev}')
    return p.stdout.decode('utf-8', errors='replace')


def section_hashes(rev):
    p = subprocess.run([sys.executable, C1, '--revision', rev, '--section-hash'], capture_output=True, text=True)
    return json.loads(p.stdout)['section_sha256']


def build_cohort(d, hashes, verdicts=None, bodies=None, roles=None):
    """Write 18 reports + a results file + a dispatch file under d."""
    verdicts = verdicts or {}
    wave = os.path.join(d, 'wave')
    os.makedirs(wave, exist_ok=True)
    tasks, results = [], []
    for row, seats in ROLES.items():
        for seat in seats:
            role = 'reviewer' if 'Rev' in seat else 'critic'
            body = (bodies or {}).get(seat)
            if body is None:
                c1, c2 = CITE[row]
                body = (f'Clause check for {row} by {seat}: the cited lines {c1} and {c2} decide the '
                        f'statement, and the row reads the pinned bytes at the cited numbers. '
                        f'This body is distinct for {seat}. ' + 'Evidence sentence. ' * 12)
            v = verdicts.get(seat, 'holds')
            with open(os.path.join(wave, f'{seat}.md'), 'w', encoding='utf-8') as fh:
                fh.write(f'ROW {row} VERDICT: {v}\nSECTION SHA256: {hashes[row]}\n{body}\n')
            tasks.append({'name': seat, 'agent': role})
            results.append({'name': seat, 'agent': role, 'output': 'done'})
    if roles:
        tasks = [t for t in tasks if t['name'] in roles]
        results = [r for r in results if r['name'] in roles]
    with open(os.path.join(d, 'results.json'), 'w', encoding='utf-8') as fh:
        json.dump({'results': results}, fh)
    with open(os.path.join(d, 'dispatch.json'), 'w', encoding='utf-8') as fh:
        json.dump({'taskCall': {'context': 'fixture', 'tasks': tasks}}, fh)
    return wave


def marks(d, entry_text, skill_line=True, readme=True, negate=None):
    entry = entry_text + '\n## Gate status — round 50 (GR1-GR3 admitted)\n\nfixture.\n'
    if not skill_line:
        skill = '# fixture skill\n'
    else:
        skill = '# fixture skill\n\n## Scrub grounding — round 50 admission\n\nfixture.\n'
    sentence = ('The btrfs scrub grounding entry `btrfs-scrub-grounding-r45.md` is admitted round 50 on '
                'its re-read bytes.')
    if negate:
        sentence = f'The entry `btrfs-scrub-grounding-r45.md` {negate}.'
    readme_text = ('# fixture readme\n\n## Round 50\n\n' + sentence + '\n') if readme else '# fixture readme\n'
    paths = {}
    for name, text in (('entry.md', entry), ('skill.md', skill), ('readme.md', readme_text)):
        p = os.path.join(d, name)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(text)
        paths[name] = p
    return paths


def run_json(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return p.returncode, json.loads(p.stdout.strip().split('\n')[-1])
    except Exception:
        return p.returncode, {'error': (p.stdout + p.stderr)[-400:], 'verdict': 'ERROR'}


def c1_battery(freeze, scratch):
    hashes = section_hashes(freeze)
    entry = git_show(freeze, ENTRY)
    base_entry = git_show(BASE, ENTRY)
    out = []

    def score(name, expect, d, entry_text, **kw):
        paths = marks(d, entry_text, **{k: v for k, v in kw.items() if k in ('skill_line', 'readme', 'negate')})
        wave = kw.get('wave')
        cmd = [sys.executable, C1, '--revision', freeze, '--no-base-check',
               '--entry-file', paths['entry.md'], '--skill-file', paths['skill.md'],
               '--readme-file', paths['readme.md'], '--dispatch-file', kw['dispatch'],
               '--results-file', kw['results'], '--wave-dir', wave]
        rc, obj = run_json(cmd)
        got = obj.get('verdict')
        out.append({'control': name, 'expected': expect, 'got': got, 'rc': rc,
                    'as_expected': got == expect,
                    'legs': {k: obj.get(k) for k in ('structural_ok', 'corr_ok', 'quotes_ok',
                                                     'verdicts_ok', 'seats_ok', 'marks_ok')},
                    'why': (obj.get('seat_notes') or [])[:2]})
        return obj

    # K0: base bytes, no cohort
    d = os.path.join(scratch, 'c1-k0')
    os.makedirs(d, exist_ok=True)
    wave = build_cohort(d, hashes)
    score('K0 base entry, no cohort', 'FAIL', d, base_entry, wave=wave,
          dispatch=os.path.join(d, 'dispatch.json'), results=os.path.join(d, 'results.json'))
    # K1: corrected entry + marks, no cohort
    d = os.path.join(scratch, 'c1-k1')
    os.makedirs(d, exist_ok=True)
    wave = build_cohort(d, hashes)
    score('K1 corrected entry + marks, no cohort', 'FAIL', d, entry, wave=wave,
          dispatch=os.path.join(d, 'dispatch.json'), results=os.path.join(d, 'results.json'))
    # K2: all-holds cohort on bytes with a round-49 defect string restored
    d = os.path.join(scratch, 'c1-k2')
    os.makedirs(d, exist_ok=True)
    wave = build_cohort(d, hashes)
    bad = entry.replace('* Scrub doing the replace isn\'t running so we need to do the',
                        'Scrub doing the replace isn\'t running so we need to do the')
    score('K2 all-holds cohort on defective bytes', 'FAIL', d, bad, wave=wave,
          dispatch=os.path.join(d, 'dispatch.json'), results=os.path.join(d, 'results.json'))
    # K3: one bound partly
    d = os.path.join(scratch, 'c1-k3')
    os.makedirs(d, exist_ok=True)
    wave = build_cohort(d, hashes, verdicts={'R50CritGR2b': 'partly'})
    score('K3 one bound partly', 'FAIL', d, entry, wave=wave,
          dispatch=os.path.join(d, 'dispatch.json'), results=os.path.join(d, 'results.json'))
    # K4: two whitespace-padded identical bodies
    d = os.path.join(scratch, 'c1-k4')
    os.makedirs(d, exist_ok=True)
    c1, c2 = CITE['GR2']
    same = f'The cited lines {c1} and {c2} decide the statement of this row. ' + 'Evidence. ' * 40
    wave = build_cohort(d, hashes, bodies={'R50RevGR2a': same, 'R50CritGR2a': same + '   \n\n  '})
    score('K4 whitespace-padded identical bodies', 'FAIL', d, entry, wave=wave,
          dispatch=os.path.join(d, 'dispatch.json'), results=os.path.join(d, 'results.json'))
    # K5: reviewers only for GR1
    d = os.path.join(scratch, 'c1-k5')
    os.makedirs(d, exist_ok=True)
    only = {'R50RevGR1a', 'R50RevGR1b', 'R50RevGR1c', 'R50CritGR2a', 'R50CritGR2b', 'R50CritGR2c',
            'R50RevGR2a', 'R50RevGR2b', 'R50RevGR2c', 'R50CritGR3a', 'R50CritGR3b', 'R50CritGR3c',
            'R50RevGR3a', 'R50RevGR3b', 'R50RevGR3c'}
    wave = build_cohort(d, hashes, roles=only)
    score('K5 GR1 reviewers only', 'FAIL', d, entry, wave=wave,
          dispatch=os.path.join(d, 'dispatch.json'), results=os.path.join(d, 'results.json'))
    # K6: reports present, results entries absent
    d = os.path.join(scratch, 'c1-k6')
    os.makedirs(d, exist_ok=True)
    wave = build_cohort(d, hashes)
    with open(os.path.join(d, 'results.json'), 'w', encoding='utf-8') as fh:
        json.dump({'results': []}, fh)
    score('K6 reports but no results entries', 'FAIL', d, entry, wave=wave,
          dispatch=os.path.join(d, 'dispatch.json'), results=os.path.join(d, 'results.json'))
    # K7: citations only of lane artifacts, no row source
    d = os.path.join(scratch, 'c1-k7')
    os.makedirs(d, exist_ok=True)
    lane_only = {s: 'Only lane artifacts are cited here: entry.md:5 and SHA256SUMS:2 decide it. '
                    + 'Padding sentence. ' * 20 for s in ROLES['GR2']}
    wave = build_cohort(d, hashes, bodies=lane_only)
    score('K7 lane-artifact citations only', 'FAIL', d, entry, wave=wave,
          dispatch=os.path.join(d, 'dispatch.json'), results=os.path.join(d, 'results.json'))
    # K-pass: corrected entry + marks + valid cohort
    d = os.path.join(scratch, 'c1-pass')
    os.makedirs(d, exist_ok=True)
    wave = build_cohort(d, hashes)
    score('K-pass corrected entry + marks + 18 valid reports', 'PASS', d, entry, wave=wave,
          dispatch=os.path.join(d, 'dispatch.json'), results=os.path.join(d, 'results.json'))
    return out


def c2_battery(freeze, scratch):
    out = []
    census = git_show(freeze, 'tools/tsukuroi-census.sh')
    base_census = git_show(BASE, 'tools/tsukuroi-census.sh')

    def score(name, expect, path):
        rc, obj = run_json([sys.executable, C2, '--revision', freeze, '--census-file', path,
                            '--scratch', os.path.join(scratch, 'c2work'), '--runs', '1'])
        got = obj.get('verdict')
        out.append({'control': name, 'expected': expect, 'got': got, 'rc': rc,
                    'as_expected': got == expect,
                    'legs': {k: obj.get(k) for k in ('idiom_sites', 'base_misses', 'full_misses',
                                                     'cases', 'pass_runs', 'case_ok')}})

    d = os.path.join(scratch, 'c2')
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'base.sh')
    open(p, 'w', encoding='utf-8').write(base_census)
    score('K0 base census', 'FAIL', p)
    # K1: fix with the new case removed
    start = census.index('  # (R50-C2) The must-match arm')
    end = census.index('  unset r50_big r50_probe r50_miss r50_t\n') + len('  unset r50_big r50_probe r50_miss r50_t\n')
    p = os.path.join(d, 'nocase.sh')
    open(p, 'w', encoding='utf-8').write(census[:start] + census[end:])
    score('K1 new case removed', 'FAIL', p)
    # K2: fix with one pipe idiom restored
    p = os.path.join(d, 'oneidiom.sh')
    open(p, 'w', encoding='utf-8').write(
        census.replace("    elif ! out_has 'host=fixture-host'; then",
                       "    elif ! printf '%s\\n' \"$out\" | grep -q 'host=fixture-host'; then", 1))
    score('K2 one pipe idiom restored', 'FAIL', p)
    # K-pass: the freeze census
    p = os.path.join(d, 'pass.sh')
    open(p, 'w', encoding='utf-8').write(census)
    score('K-pass freeze census', 'PASS', p)
    return out


def c3_battery(freeze, scratch):
    out = []

    def score(name, expect, extra):
        rc, obj = run_json([sys.executable, C3, '--revision', freeze] + extra)
        got = obj.get('verdict')
        out.append({'control': name, 'expected': expect, 'got': got, 'rc': rc,
                    'as_expected': got == expect,
                    'legs': {k: obj.get(k) for k in ('adj_rows', 'linked_rows', 'bare_ranges', 'anchors_ok',
                                                     'registry_ok', 'quote_at_pin_ok', 'live_quote_ok',
                                                     'stub_fails')}})

    d = os.path.join(scratch, 'c3')
    os.makedirs(d, exist_ok=True)
    prov = git_show(freeze, 'PROVINCE.md')
    reg = git_show(freeze, 'corpus/knowledge/adjacency-anchors-r19.json')
    # the shape-valid stub the round-49 counter passed
    sys.path.insert(0, f'{L}/tools')
    import importlib.util
    spec = importlib.util.spec_from_file_location('adj50', C3)
    adj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adj)
    stub_text, stub_reg = adj.stub_province()
    p = os.path.join(d, 'stub-province.md')
    open(p, 'w', encoding='utf-8').write(stub_text)
    r = os.path.join(d, 'stub-registry.json')
    open(r, 'w', encoding='utf-8').write(json.dumps(stub_reg))
    score('K1 shape-valid stub', 'FAIL', ['--province-file', p, '--registry-file', r])
    # K2: one ADJ row pointed at the wrong class
    wrong = prov.replace('| ADJ-02 | A credential-bearing helper', '| ADJ-02 | A credential-bearing helper')
    wrong = wrong.replace('`OUT-003`', '`OUT-002`', 1)
    p = os.path.join(d, 'wrongclass.md')
    open(p, 'w', encoding='utf-8').write(wrong)
    score('K2 ADJ-02 pointed at OUT-002', 'FAIL', ['--province-file', p])
    # K3: one registry digest mutated
    regj = json.loads(reg)
    for row in regj['outbound']:
        if row['id'] == 'OUT-004':
            row['sibling_blob_sha256'] = '0' * 64
    r = os.path.join(d, 'mutated-registry.json')
    open(r, 'w', encoding='utf-8').write(json.dumps(regj))
    score('K3 one registry digest mutated', 'FAIL', ['--registry-file', r])
    # K-pass: the freeze province and registry
    score('K-pass freeze province + registry', 'PASS', [])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--freeze', required=True)
    ap.add_argument('--scratch', default='/fast/scratch/hyaku/tsukuroi-r50/controls')
    ap.add_argument('--only', choices=['c1', 'c2', 'c3'])
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    work = tempfile.mkdtemp(dir=a.scratch, prefix='battery.')
    bad = 0
    try:
        for name, fn in (('c1', c1_battery), ('c2', c2_battery), ('c3', c3_battery)):
            if a.only and a.only != name:
                continue
            rows = fn(a.freeze, work)
            path = f'{W}/controls/battery-summary-r50-{name}.jsonl'
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as fh:
                for row in rows:
                    fh.write(json.dumps(row, sort_keys=True) + '\n')
            miss = [r for r in rows if not r['as_expected']]
            bad += len(miss)
            print(f'{name}: {len(rows)} controls, {len(rows) - len(miss)} as expected, {len(miss)} not')
            for r in miss:
                print('  MISS', r['control'], 'expected', r['expected'], 'got', r['got'], r['legs'])
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
