#!/usr/bin/env python3
"""Round-48 pre-data control battery for C2 (GR1-GR3 admission), scored with the frozen counter
tools/check-scrub-admission-r48.py. Every fixture lives in a sandbox clone under $HYAKU_SCRATCH
(git -C <sandbox> only, sandbox identity), never in the lane. Usage:
  python3 battery-c2.py <out.jsonl>   (HYAKU_SCRATCH defaults to /fast/scratch/hyaku)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '5fdf062f969292736e36513e39f98b1b8de43635'
COUNTER = LANE + '/tools/check-scrub-admission-r48.py'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
W = '.ufo/waves/round-48'
ROWS = ('GR1', 'GR2', 'GR3')
CITE = {'GR1': 'cmdline.c:100', 'GR2': 'scrub.c:3094', 'GR3': 'scrub.c:3094'}


def git(d, *a, inp=None):
    return subprocess.run(['git', '-C', d, '-c', 'user.name=ctl', '-c', 'user.email=ctl@sandbox.invalid', *a],
                          capture_output=True, input=inp, check=True).stdout


def counter(d, rev, *extra):
    p = subprocess.run(['python3', COUNTER, '--revision', rev, '--lane', d, *extra], capture_output=True)
    return p.returncode, json.loads(p.stdout.decode() or '{}')


def seats(row, roles=('rev', 'crit')):
    n = row[2:]
    out = []
    for r in roles:
        for x in 'abc':
            out.append((f'R48{"Rev" if r == "rev" else "Crit"}GR{n}{x}', 'reviewer' if r == 'rev' else 'critic'))
    return out


def build(root, name, hashes, *, marks=True, cohort=True, wrong_hash=False, partly=None, identical=False,
          roles_by_row=None, cite_override=None, neg_readme=False, no_dispatch=False, keep=None, inner=False, partly_clean=None, contradict=None, tiny=None):
    d = os.path.join(root, name)
    subprocess.run(['git', 'clone', '-q', '--shared', LANE, d], check=True)
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, check=True).stdout.decode().strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    git(d, 'checkout', '-q', '--detach', BASE)
    entry = open(os.path.join(d, ENTRY), encoding='utf-8').read()
    if inner:
        # the stray header lands INSIDE GR1's extent (before the GR2 header)
        entry = entry.replace('\n## GR2\n', '\n## stray inner header\nx\n\n## GR2\n', 1)
    if marks:
        entry += '\n## Gate status — round 48 (GR1-GR3 admitted)\n'
        with open(os.path.join(d, 'SKILL.md'), 'a', encoding='utf-8') as f:
            f.write('\n## Scrub grounding — round 48 admission\n')
        with open(os.path.join(d, 'corpus/README.md'), 'a', encoding='utf-8') as f:
            if neg_readme:
                f.write('\n- btrfs-scrub-grounding-r45.md remains unadmitted round 48 (admitted round 48 is withheld)\n')
            else:
                f.write('\n- btrfs-scrub-grounding-r45.md admitted round 48\n')
    with open(os.path.join(d, ENTRY), 'w', encoding='utf-8') as f:
        f.write(entry)
    tasks, results = [], []
    os.makedirs(os.path.join(d, W, 'w2'), exist_ok=True)
    if cohort:
        for row in ROWS:
            roles = (roles_by_row or {}).get(row, ('rev', 'crit'))
            for seat, role in seats(row, roles):
                verdict = 'holds'
                h = '0' * 64 if wrong_hash else hashes[row]
                cite = (cite_override or {}).get(row, CITE[row])
                if partly == seat:
                    verdict = 'partly'
                    cite = 'bogus.c:1'
                uniq = 'IDENTICAL BODY' if identical else f'seat {seat} checked clause {seat[-1]} of {row}'
                body = (f'Checked every clause of {row} against the pinned snapshots; {uniq}. '
                        f'Evidence line {cite} read verbatim. ' + 'The row clause matches its cited line. ' * 12)
                if partly_clean == seat:
                    verdict = 'partly'
                if contradict == seat:
                    body += f'\nROW {row} VERDICT: partly\n'
                if tiny == seat:
                    verdict, body = 'fails', 'no'
                with open(os.path.join(d, W, 'w2', seat + '.md'), 'w', encoding='utf-8') as f:
                    f.write(f'ROW {row} VERDICT: {verdict}\nSECTION SHA256: {h}\n{body}\n')
                if not no_dispatch:
                    tasks.append({'name': seat, 'agent': role})
                    results.append({'name': seat, 'agent': role, 'status': 'done'})
    if keep is not None:  # drop seats not in keep
        pass
    json.dump({'taskCall': {'tasks': tasks}}, open(os.path.join(d, W, 'w2-dispatch.json'), 'w'))
    json.dump({'results': results}, open(os.path.join(d, W, 'w2-results.json'), 'w'))
    git(d, 'add', '-A')
    git(d, 'commit', '-q', '-m', f'fixture {name}')
    return d, git(d, 'rev-parse', 'HEAD').decode().strip()


def main():
    out = sys.argv[1]
    root = tempfile.mkdtemp(dir=os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'tsukuroi-r48'))
    try:
        rc, hs = counter(LANE, BASE, '--section-hash')
        hashes = hs['section_sha256']
        cases = []
        # K0: do-nothing control — base bytes, no seats, no marks
        rc, r = counter(LANE, BASE)
        cases.append(('K0 do-nothing base', r, 'FAIL'))
        specs = [
            ('K1 marks-only (marks written, no counted seats)', dict(cohort=False), 'FAIL'),
            ('K2 forged cohort on a stale section hash', dict(wrong_hash=True), 'FAIL'),
            ('K3 one bound GR2 critic reads partly with a bad citation (citation slip never launders a negative)',
             dict(partly='R48CritGR2b'), 'FAIL'),
            ('K3b one bound GR1 reviewer reads partly with clean citations', dict(partly_clean='R48RevGR1c'), 'FAIL'),
            ('K3c one GR3 critic report contradicts its own first line', dict(contradict='R48CritGR3a'), 'FAIL'),
            ('K3d one GR2 reviewer reads fails with a two-byte body (format-thin negative still blocks)', dict(tiny='R48RevGR2a'), 'FAIL'),
            ('K4 byte-identical bodies (K23)', dict(identical=True), 'FAIL'),
            ('K5 GR1 has reviewers only, no critic', dict(roles_by_row={'GR1': ('rev',)}), 'FAIL'),
            ('K6 GR3 seats cite an unpinned file (unbound for credit)', dict(cite_override={'GR3': 'README.md:5'}), 'FAIL'),
            ('K7 reports present but no dispatch/results entries', dict(no_dispatch=True), 'FAIL'),
            ('K8 negating README mark', dict(neg_readme=True), 'FAIL'),
            ('F1a stray `## ` header inside GR1 (structural_ok 0)', dict(inner=True), 'FAIL'),
            ('K9 full valid synthetic cohort + marks (counter can pass; fixture, not the live integration)', dict(), 'PASS'),
        ]
        for label, kw, want in specs:
            d, rev = build(root, f'c{len(cases)}', hashes, **kw)
            rc, r = counter(d, rev)
            cases.append((label, r, want))
        with open(out, 'w') as f:
            for label, r, want in cases:
                legs = {k: r.get(k) for k in ('structural_ok', 'quotes_ok', 'verdicts_ok', 'marks_ok')}
                f.write(json.dumps({'case': label, 'expected': want, 'verdict': r.get('verdict'), 'legs': legs,
                                    'as_expected': r.get('verdict') == want}) + '\n')
        bad = [c[0] for c in cases if c[1].get('verdict') != c[2]]
        print('as_expected', len(cases) - len(bad), 'of', len(cases), 'unexpected:', bad)
        return 1 if bad else 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
