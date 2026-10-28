#!/usr/bin/env python3
"""Round-51 pre-data control batteries (L1 TsukuroiR51). Run BEFORE any seat scores.

Usage: battery.py --freeze <REV> [--scratch <dir>] [--only c1|c2|c3] [--tag <label>]
Writes controls/battery-summary-r51-<tag>-c{1,2,3}.jsonl (one JSON line per control) and exits 1 if
any control does not score as declared. Fixtures live under --scratch and are removed at the end.
"""
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
W = f'{L}/.ufo/waves/round-51'
C1 = f'{L}/tools/check-scrub-admission-r51.py'
C2S = f'{L}/tools/score-counter-cheats-r51.py'
C3 = f'{L}/tools/check-adjacency-table-r51.py'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
BASE = 'c0ad548a93425a3bf8813d28d92f26fe2f64b9d4'
CITE = {'GR1': ('cmdline.c:147', 'kstrtox.c:1'),
        'GR2': ('dev-replace.c:1111', 'scrub.c:3094'),
        'GR3': ('systemd.kill.xml:1', 'btrfs-scrub@.service:1')}
ROLES = {n: tuple(f'R51{k}GR{n[2]}{x}' for k in ('Rev', 'Crit') for x in 'abc') for n in ('GR1', 'GR2', 'GR3')}


def git_show(rev, path):
    p = subprocess.run(['git', '-C', L, 'show', f'{rev}:{path}'], capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f'cannot read {path} at {rev}')
    return p.stdout.decode('utf-8', errors='replace')


def section_hashes(rev, entry_file=None):
    cmd = [sys.executable, C1, '--revision', rev, '--section-hash', '--no-base-check']
    if entry_file:
        cmd += ['--entry-file', entry_file]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(p.stdout)['section_sha256']


def build_cohort(d, hashes, verdicts=None, bodies=None, roles=None, cohort=True):
    wave = os.path.join(d, 'wave')
    os.makedirs(wave, exist_ok=True)
    if not cohort:
        for name, obj in (('results.json', {'results': []}),
                          ('dispatch.json', {'taskCall': {'context': 'fixture', 'tasks': []}})):
            with open(os.path.join(d, name), 'w', encoding='utf-8') as fh:
                json.dump(obj, fh)
        return wave
    verdicts = verdicts or {}
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
    entry = entry_text + '\n## Gate status — round 51 (GR1-GR3 admitted)\n\nfixture.\n'
    skill = ('# fixture skill\n\n## Scrub grounding — round 51 admission\n\nfixture.\n' if skill_line
             else '# fixture skill\n')
    sentence = ('The btrfs scrub grounding entry `btrfs-scrub-grounding-r45.md` is admitted round 51 on '
                'its re-read bytes.')
    if negate:
        sentence = f'The entry `btrfs-scrub-grounding-r45.md` {negate}.'
    readme_text = ('# fixture readme\n\n## Round 51\n\n' + sentence + '\n') if readme else '# fixture readme\n'
    paths = {}
    for name, text in (('entry.md', entry), ('skill.md', skill), ('readme.md', readme_text)):
        p = os.path.join(d, name)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(text)
        paths[name] = p
    return paths


def run_json(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    try:
        return p.returncode, json.loads(p.stdout.strip().split('\n')[-1])
    except Exception:
        return p.returncode, {'error': (p.stdout + p.stderr)[-400:], 'verdict': 'ERROR'}


def c1_battery(freeze, scratch):
    entry = git_show(freeze, ENTRY)
    base_entry = git_show(BASE, ENTRY)
    hashes = section_hashes(freeze)
    out = []

    def score(name, expect, tag, entry_text, hashes_used=None, verdicts=None, bodies=None, roles=None,
              cohort=True, results_empty=False, **kw):
        d = os.path.join(scratch, f'c1-{tag}')
        os.makedirs(d, exist_ok=True)
        wave = build_cohort(d, hashes_used or hashes, verdicts=verdicts, bodies=bodies, roles=roles,
                            cohort=cohort)
        if results_empty:
            with open(os.path.join(d, 'results.json'), 'w', encoding='utf-8') as fh:
                json.dump({'results': []}, fh)
        paths = marks(d, entry_text, **kw)
        cmd = [sys.executable, C1, '--revision', freeze, '--no-base-check',
               '--entry-file', paths['entry.md'], '--skill-file', paths['skill.md'],
               '--readme-file', paths['readme.md'], '--dispatch-file', os.path.join(d, 'dispatch.json'),
               '--results-file', os.path.join(d, 'results.json'), '--wave-dir', wave]
        rc, obj = run_json(cmd)
        got = obj.get('verdict')
        out.append({'control': name, 'expected': expect, 'got': got, 'rc': rc, 'as_expected': got == expect,
                    'legs': {k: obj.get(k) for k in ('structural_ok', 'lint_ok', 'quotes_ok', 'verdicts_ok',
                                                     'seats_ok', 'marks_ok')},
                    'why': (obj.get('seat_notes') or [])[:2]})

    score('K0 base entry, no cohort', 'FAIL', 'k0', base_entry, cohort=False)
    score('K1 corrected entry + marks, no cohort', 'FAIL', 'k1', entry, cohort=False)
    # K2: all-holds cohort on bytes whose cmdline.c:147 quote drops its comment leader (the round-50 defect)
    bad = entry.replace('"* potentially suffixed with K, M, G, T, P, E."', '"potentially suffixed with K, M, G, T, P, E."')
    assert bad != entry
    score('K2 all-holds cohort, dropped comment leader', 'FAIL', 'k2', bad, hashes_used=section_hashes(freeze, _w(scratch, 'k2h', bad)))
    # K3: all-holds cohort on bytes citing a line outside the declared ranges that the gap block omits
    anchor = 'scrub.c:3094-3153'
    bad3 = entry.replace(anchor, anchor + ' and :3200', 1)
    assert bad3 != entry
    score('K3 all-holds cohort, undeclared range gap', 'FAIL', 'k3', bad3, hashes_used=section_hashes(freeze, _w(scratch, 'k3h', bad3)))
    # K3b: a quote that is a fragment of its line, not the whole line
    bad3b = entry.replace('"if (btrfs_fs_closing(fs_info))"', '"btrfs_fs_closing(fs_info)"', 1)
    assert bad3b != entry
    score('K3b all-holds cohort, fragment quote', 'FAIL', 'k3b', bad3b, hashes_used=section_hashes(freeze, _w(scratch, 'k3bh', bad3b)))
    score('K4 one bound partly', 'FAIL', 'k4', entry, verdicts={'R51CritGR2b': 'partly'})
    c1, c2 = CITE['GR2']
    same = f'The cited lines {c1} and {c2} decide the statement of this row. ' + 'Evidence. ' * 40
    score('K5 whitespace-padded identical bodies', 'FAIL', 'k5', entry,
          bodies={'R51RevGR2a': same, 'R51CritGR2a': same + '   \n\n  '})
    only = {s for seats in ROLES.values() for s in seats} - {'R51CritGR1a', 'R51CritGR1b', 'R51CritGR1c'}
    score('K6 GR1 reviewers only', 'FAIL', 'k6', entry, roles=only)
    score('K7 reports but no results entries', 'FAIL', 'k7', entry, results_empty=True)
    lane_only = {s: 'Only lane artifacts are cited here: entry.md:5 and SHA256SUMS:2 decide it. '
                    + 'Padding sentence. ' * 20 for s in ROLES['GR2']}
    score('K8 lane-artifact citations only', 'FAIL', 'k8', entry, bodies=lane_only)
    score('K-pass corrected entry + marks + 18 valid reports', 'PASS', 'pass', entry)
    return out


def _w(scratch, name, text):
    p = os.path.join(scratch, f'{name}.md')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(text)
    return p


def c2_battery(freeze, scratch):
    out = []
    # the scorer IS the measurement; here it runs once at the freeze as the pre-data control record
    rc, obj = run_json([sys.executable, C2S, '--revision', freeze, '--scratch', os.path.join(scratch, 'c2')])
    out.append({'control': 'K-pass real census passes, 4 cheats rejected, round-50 counter rejects none',
                'expected': 'PASS', 'got': obj.get('verdict'), 'rc': rc,
                'as_expected': obj.get('verdict') == 'PASS',
                'legs': {k: obj.get(k) for k in ('real_pass', 'cheats', 'cheats_rejected',
                                                 'r50_cheats_rejected')},
                'detail': obj.get('detail')})
    # K0 (do-nothing): scoring the round-50 counter as if it were the claim's counter
    rc, obj = run_json([sys.executable, C2S, '--revision', freeze, '--scratch', os.path.join(scratch, 'c2k0'),
                        '--counter', 'tools/check-selftest-matcher-r50.py', '--skip-r50'])
    out.append({'control': 'K0 do-nothing: the round-50 counter in the claim slot', 'expected': 'FAIL',
                'got': obj.get('verdict'), 'rc': rc, 'as_expected': obj.get('verdict') == 'FAIL',
                'legs': {k: obj.get(k) for k in ('real_pass', 'cheats', 'cheats_rejected')}})
    return out


def c3_battery(freeze, scratch):
    out = []
    spec = importlib.util.spec_from_file_location('adj51', C3)
    adj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adj)
    prov = git_show(freeze, 'PROVINCE.md')
    reg = git_show(freeze, 'corpus/knowledge/adjacency-anchors-r19.json')
    d = os.path.join(scratch, 'c3')
    os.makedirs(d, exist_ok=True)

    def score(name, expect, extra, want_rc=None):
        rc, obj = run_json([sys.executable, C3, '--revision', freeze, '--no-base-check'] + extra)
        got = obj.get('verdict')
        ok = got == expect and (want_rc is None or rc == want_rc)
        out.append({'control': name, 'expected': expect, 'got': got, 'rc': rc, 'as_expected': ok,
                    'legs': {k: obj.get(k) for k in ('display_bound_ok', 'quote_specific_ok', 'digests_bound_ok',
                                                     'display_forge_fails', 'override_blocked', 'r50_blind',
                                                     'quote_at_pin_ok', 'stub_fails')}})

    forged, hit = adj.forged_province(prov)
    assert hit == 1
    p = _w(d, 'forged-province', forged)
    score('K0 false displayed OUT-009 commit', 'CONTROL-FAIL', ['--control', '--province-file', p])
    score('K1 an override without --control is not a measurement', 'OVERRIDE-NOT-MEASURED',
          ['--province-file', p], want_rc=3)
    spec50 = importlib.util.spec_from_file_location('adj50', f'{L}/tools/check-adjacency-table-r50.py')
    m50 = importlib.util.module_from_spec(spec50)
    spec50.loader.exec_module(m50)
    stub_text, stub_reg = m50.stub_province()
    sp = _w(d, 'stub-province', stub_text)
    sr = _w(d, 'stub-registry', json.dumps(stub_reg))
    score('K2 shape-valid stub', 'CONTROL-FAIL', ['--control', '--province-file', sp, '--registry-file', sr])
    regj = json.loads(reg)
    for row in regj['outbound']:
        if row['id'] == 'OUT-004':
            row['sibling_blob_sha256'] = '0' * 64
    r = _w(d, 'mutated-registry', json.dumps(regj))
    score('K3 one registry digest mutated', 'CONTROL-FAIL', ['--control', '--registry-file', r])
    regq = json.loads(reg)
    for row in regq['outbound']:
        if row['id'] == 'OUT-010':
            row['quote_line'] = 1
    rq = _w(d, 'mutated-quote-line', json.dumps(regq))
    score('K4 registry quote_line moved off the quote', 'CONTROL-FAIL', ['--control', '--registry-file', rq])
    badd = prov.replace('sha256 8006da5db27d2188ff2f3fc20ae402d0d30c7b5c5fcf9ca26c6793d2ff7e080f',
                        'sha256 ' + '0' * 64, 1)
    assert badd != prov
    pd = _w(d, 'mutated-digest-list', badd)
    score('K5 displayed OUT-010 digest altered', 'CONTROL-FAIL', ['--control', '--province-file', pd])
    score('K-pass real province and registry, measurement mode', 'PASS', [])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--freeze', required=True)
    ap.add_argument('--scratch', default='/fast/scratch/hyaku/tsukuroi-r51/controls')
    ap.add_argument('--only', choices=['c1', 'c2', 'c3'])
    ap.add_argument('--tag', default='freeze')
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    work = tempfile.mkdtemp(dir=a.scratch, prefix='battery.')
    bad = 0
    try:
        for name, fn in (('c1', c1_battery), ('c2', c2_battery), ('c3', c3_battery)):
            if a.only and a.only != name:
                continue
            rows = fn(a.freeze, work)
            path = f'{W}/controls/battery-summary-r51-{a.tag}-{name}.jsonl'
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
