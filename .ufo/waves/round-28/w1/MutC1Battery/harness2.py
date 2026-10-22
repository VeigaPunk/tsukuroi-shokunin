#!/usr/bin/env python3
"""Round 2: more mutants of the C1 battery, focused on the export step and control fields."""
import hashlib, json, os, subprocess

ORIG = '/fast/scratch/hyaku/tsuku28/MutC1Battery/tree/tools/mutants-adjacency-overlap.py'
WORK = '/fast/scratch/hyaku/tsuku28/MutC1Battery/work2'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '3b9e0430b88d01415c241dd5a18b8939b8a520ac'
OLD = 'dd94cb1f'
NEW = 'f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0'

MUTANTS = [
    # --- export step ---
    ('M11-export-archive-head-not-base', [
        ("tar = subprocess.run(['git', '-C', lane, 'archive', rev], capture_output=True, check=True).stdout",
         "tar = subprocess.run(['git', '-C', lane, 'archive', 'HEAD'], capture_output=True, check=True).stdout"),
    ]),
    ('M12-export-counter-from-lane-worktree', [
        ("blob = subprocess.run(['git', '-C', lane, 'show', ARGS.counter_rev + ':tools/check-adjacency-overlap.py'],\n                              capture_output=True, check=True).stdout",
         "blob = open(os.path.join(lane, 'tools/check-adjacency-overlap.py'), 'rb').read()"),
    ]),
    ('M13-export-counter-file-ignored', [
        ("    if ARGS.counter_file:\n        with open(ARGS.counter_file, 'rb') as fh:\n            blob = fh.read()\n    else:\n",
         "    if False:\n        with open(ARGS.counter_file, 'rb') as fh:\n            blob = fh.read()\n    else:\n"),
    ]),
    ('M14-export-base-rev-not-verified', [
        ("rev = subprocess.run(['git', '-C', lane, 'rev-parse', '--verify', ARGS.base + '^{commit}'],\n                         capture_output=True, text=True, check=True).stdout.strip()",
         "rev = ARGS.base"),
    ]),
    ('M15-export-extractall-without-data-filter', [
        ("t.extractall(TREE, filter='data')", "t.extractall(TREE)"),
    ]),
    # --- accepted predicate ---
    ('M16-accepted-anchored-rows-ge-6', [
        ("o.get('anchored_rows') == 6", "o.get('anchored_rows') >= 6"),
    ]),
    ('M17-accepted-anchored-rows-ge-5', [
        ("o.get('anchored_rows') == 6", "o.get('anchored_rows') >= 5"),
    ]),
    ('M18-accepted-truthy-rows', [
        ("accepted = any(o.get('exit') == 0 and o.get('anchored_rows') == 6 for o in out.values())",
         "accepted = any(o.get('exit') == 0 and o.get('anchored_rows') for o in out.values())"),
    ]),
    # --- summary counting / control fields ---
    ('M19-control-count-from-no-sibling', [
        ("'control_live_anchored_rows': ctl['live-mori'].get('anchored_rows'),",
         "'control_live_anchored_rows': ctl['no-sibling'].get('anchored_rows'),"),
    ]),
    ('M20-control-count-from-any-accepted-mutant', [
        ("'control_live_anchored_rows': ctl['live-mori'].get('anchored_rows'),",
         "'control_live_anchored_rows': next((r['live-mori'].get('anchored_rows') for r in sf if r['accepted']), 0),"),
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
        print('PRISTINE', rev, 'exit', rc, json.dumps({k: summ.get(k) for k in
              ('should_fail_total', 'should_fail_accepted', 'control_live_anchored_rows', 'control_live_exit',
               'counter_sha256', 'should_pass_accepted')}) if summ else 'NO-SUMMARY')
    results = []
    for name, reps in MUTANTS:
        data = orig_bytes.decode()
        ok = True
        for old, new in reps:
            if data.count(old) != 1:
                ok = False
                print('MUTANT', name, 'SKIP count=%d' % data.count(old))
                break
            data = data.replace(old, new)
        if not ok:
            continue
        path = os.path.join(WORK, name + '.py')
        with open(path, 'w') as fh:
            fh.write(data)
        row = {'mutant': name, 'mut_sha256': sha(data.encode()), 'runs': {}}
        for rev in (OLD, NEW):
            rc, summ, err, n = run(path, rev)
            b_rc, b_summ = base_runs[rev]
            changed = []
            if (summ is None) != (b_summ is None):
                changed.append('summary-present-differs')
            elif summ is not None:
                for k in ('should_fail_total', 'should_fail_accepted', 'control_live_anchored_rows',
                          'control_live_exit', 'should_pass_accepted', 'counter_sha256', 'counter_rev'):
                    if summ.get(k) != b_summ.get(k):
                        changed.append('%s:%s->%s' % (k, b_summ.get(k), summ.get(k)))
                if summ.get('accepted_mutants') != b_summ.get('accepted_mutants'):
                    changed.append('accepted_mutants-list-differs')
            row['runs'][rev] = {'exit': rc, 'stderr_tail': err, 'lines': n, 'summary': summ,
                                'changed_vs_pristine': changed}
        results.append(row)
        for rev in (OLD, NEW):
            r = row['runs'][rev]
            s = r['summary'] or {}
            print('MUTANT', name, rev[:8], 'exit', r['exit'], 'changed', r['changed_vs_pristine'],
                  '| acc', s.get('should_fail_accepted'), 'total', s.get('should_fail_total'),
                  'ctl', s.get('control_live_anchored_rows'), 'ctl_exit', s.get('control_live_exit'),
                  'stderr', r['stderr_tail'])
        print('MUTANT-SHA', name, row['mut_sha256'])
    after = open(ORIG, 'rb').read()
    print('RESTORE sha256', sha(after), 'identical', sha(after) == orig_sha)
    for rev in (OLD, NEW):
        rc, summ, err, n = run(ORIG, rev)
        print('RESTORE-RERUN', rev, 'exit', rc, 'same_summary', summ == base_runs[rev][1])
    with open('/fast/scratch/hyaku/tsuku28/MutC1Battery/mutation-results-2.json', 'w') as fh:
        json.dump({'pristine_sha256': orig_sha, 'base': BASE, 'mutants': results}, fh, indent=1)


if __name__ == '__main__':
    main()
