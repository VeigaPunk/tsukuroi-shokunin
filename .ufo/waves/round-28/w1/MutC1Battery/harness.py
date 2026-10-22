#!/usr/bin/env python3
"""Mutation harness for the round-28 C1 battery (tools/mutants-adjacency-overlap.py).

Each mutant is a set of literal string replacements applied to a COPY of the battery bytes.
Every copy is run twice (--counter-rev dd94cb1f and --counter-rev f8e3a8f) and the summary
line is compared with the pristine run of the same counter rev.
"""
import hashlib, json, os, shutil, subprocess, sys

ORIG = '/fast/scratch/hyaku/tsuku28/MutC1Battery/tree/tools/mutants-adjacency-overlap.py'
WORK = '/fast/scratch/hyaku/tsuku28/MutC1Battery/work'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '3b9e0430b88d01415c241dd5a18b8939b8a520ac'
OLD = 'dd94cb1f'
NEW = 'f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0'

MUTANTS = [
    ('M1-accepted-any-to-all', [
        ("accepted = any(o.get('exit') == 0 and o.get('anchored_rows') == 6 for o in out.values())",
         "accepted = all(o.get('exit') == 0 and o.get('anchored_rows') == 6 for o in out.values())"),
    ]),
    ('M2-accepted-drop-exit-check', [
        ("accepted = any(o.get('exit') == 0 and o.get('anchored_rows') == 6 for o in out.values())",
         "accepted = any(o.get('anchored_rows') == 6 for o in out.values())"),
    ]),
    ('M3-shouldfail-filter-any-not-control', [
        ("sf = [r for r in RESULTS if r['kind'] == 'should-fail']",
         "sf = [r for r in RESULTS if r['kind'] != 'control']"),
    ]),
    ('M4-shouldfail-filter-include-divergence', [
        ("sf = [r for r in RESULTS if r['kind'] == 'should-fail']",
         "sf = [r for r in RESULTS if r['kind'] in ('should-fail', 'divergence')]"),
    ]),
    ('M5-sibling-mode-drop-no-sibling', [
        ("for label, sib in (('live-mori', REALSIB), ('no-sibling', NOSIB)):",
         "for label, sib in (('live-mori', REALSIB),):"),
    ]),
    ('M6-sibling-mode-swap-roots', [
        ("for label, sib in (('live-mori', REALSIB), ('no-sibling', NOSIB)):",
         "for label, sib in (('live-mori', NOSIB), ('no-sibling', REALSIB)):"),
    ]),
    ('M7-summary-accepted-count-over-all-results', [
        ("'should_fail_accepted': sum(r['accepted'] for r in sf),",
         "'should_fail_accepted': sum(r['accepted'] for r in RESULTS),"),
    ]),
    ('M8-summary-total-counts-all-results', [
        ("'should_fail_total': len(sf),",
         "'should_fail_total': len(RESULTS),"),
    ]),
    ('M9-export-counter-blob-from-base-rev', [
        ("blob = subprocess.run(['git', '-C', lane, 'show', ARGS.counter_rev + ':tools/check-adjacency-overlap.py'],",
         "blob = subprocess.run(['git', '-C', lane, 'show', rev + ':tools/check-adjacency-overlap.py'],"),
    ]),
    ('M10-sandbox-drop-git-clean', [
        ("    g('clean', '-fdqx')\n", ""),
    ]),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(path, counter_rev):
    p = subprocess.run(['python3', path, '--base', BASE, '--counter-rev', counter_rev, '--lane', LANE],
                       capture_output=True, text=True)
    lines = [l for l in p.stdout.strip().splitlines() if l.strip()]
    summ = None
    if lines:
        try:
            summ = json.loads(lines[-1])
        except Exception:
            summ = None
    return p.returncode, summ, p.stderr.strip().splitlines()[-3:], len(lines)


def main():
    os.makedirs(WORK, exist_ok=True)
    orig_bytes = open(ORIG, 'rb').read()
    orig_sha = sha(orig_bytes)
    print('PRISTINE sha256', orig_sha)
    base_runs = {}
    for rev in (OLD, NEW):
        rc, summ, err, n = run(ORIG, rev)
        base_runs[rev] = (rc, summ)
        print('PRISTINE', rev, 'exit', rc, 'lines', n, json.dumps({k: summ.get(k) for k in
              ('should_fail_total', 'should_fail_accepted', 'control_live_anchored_rows', 'control_live_exit',
               'counter_sha256', 'should_pass_accepted')}) if summ else 'NO-SUMMARY', 'stderr', err)

    results = []
    for name, reps in MUTANTS:
        data = orig_bytes.decode()
        applied = []
        ok = True
        for old, new in reps:
            if data.count(old) != 1:
                ok = False
                applied.append('MISS(%d)' % data.count(old))
                break
            data = data.replace(old, new)
            applied.append('ok')
        if not ok:
            print('MUTANT', name, 'SKIP', applied)
            continue
        path = os.path.join(WORK, name + '.py')
        with open(path, 'w') as fh:
            fh.write(data)
        mut_sha = sha(data.encode())
        row = {'mutant': name, 'mut_sha256': mut_sha, 'replacements': applied, 'runs': {}}
        for rev in (OLD, NEW):
            rc, summ, err, n = run(path, rev)
            b_rc, b_summ = base_runs[rev]
            changed = []
            if (summ is None) != (b_summ is None):
                changed.append('summary-present-differs')
            elif summ is not None:
                for k in ('should_fail_total', 'should_fail_accepted', 'control_live_anchored_rows',
                          'control_live_exit', 'should_pass_accepted'):
                    if summ.get(k) != b_summ.get(k):
                        changed.append('%s:%s->%s' % (k, b_summ.get(k), summ.get(k)))
                if summ.get('accepted_mutants') != b_summ.get('accepted_mutants'):
                    changed.append('accepted_mutants-list-differs')
            row['runs'][rev] = {'exit': rc, 'stderr_tail': err, 'lines': n,
                                'summary': summ, 'changed_vs_pristine': changed,
                                'pristine_exit': b_rc}
        results.append(row)
        for rev in (OLD, NEW):
            r = row['runs'][rev]
            print('MUTANT', name, rev, 'exit', r['exit'], 'changed', r['changed_vs_pristine'],
                  'accepted', (r['summary'] or {}).get('should_fail_accepted'),
                  'total', (r['summary'] or {}).get('should_fail_total'),
                  'ctl', (r['summary'] or {}).get('control_live_anchored_rows'),
                  'ctl_exit', (r['summary'] or {}).get('control_live_exit'),
                  'stderr', r['stderr_tail'])
        print('MUTANT-SHA', name, mut_sha)

    # restoration check: original bytes untouched, pristine rerun identical
    after = open(ORIG, 'rb').read()
    print('RESTORE sha256', sha(after), 'identical', sha(after) == orig_sha)
    for rev in (OLD, NEW):
        rc, summ, err, n = run(ORIG, rev)
        b_rc, b_summ = base_runs[rev]
        print('RESTORE-RERUN', rev, 'exit', rc, 'same_summary', summ == b_summ)
    with open('/fast/scratch/hyaku/tsuku28/MutC1Battery/mutation-results.json', 'w') as fh:
        json.dump({'pristine_sha256': orig_sha, 'base': BASE, 'mutants': results}, fh, indent=1)


if __name__ == '__main__':
    main()
