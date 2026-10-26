#!/usr/bin/env python3
"""Round-40 C1 counter (operability): does the census `--selftest` at <REV> kill the literal-keyed and
guard mutants of the STORAGE arm's mount-table cross-check that the round-39 selftest let through?

Frozen before any seat scored (SCORECARD.md "Round 40 — declaration"). Closes round-39 routed defect §6.2
(R39-FIXTURE-MONOCULTURE): every round-39 "btrfs mounted" fixture was the one string
`/dev/mapper/root / btrfs rw,noatime,subvolid=256,subvol=/@ 0 0`, so arms keyed on a literal of that string
passed the selftest 117/117 (`.ufo/waves/round-39/w1/C1CritControl.md` VA, VB, VC, VG; `C1MutParse.md` (a),
(b); `C1MutCrossCheck.md` (e)).

Method: `tools/tsukuroi-census.sh` is read from <REV> (git show) and written into a private scratch
directory (never the lane). Each frozen mutant (MUTANTS) is an exact substring replacement of the round-40
base text of `probe_storage_arm`; it is APPLIED only when its `old` text occurs exactly once in the census
at <REV> (the arm is not this claim's surface; a changed arm makes the mutant unappliable and the run FAIL).
Each variant runs `bash <copy> --selftest` with TMPDIR inside the scratch and cwd `/`; a variant is KILLED
when the selftest's last line is not `TSUKUROI_CENSUS_SELFTEST: PASS ...` or its exit code is nonzero.
Controls inside the same run:
  * baseline: the unmutated census must print the PASS line and exit 0;
  * neutral rewrites (NEUTRAL): three semantics-preserving rewrites of the same arm must each PASS — a
    selftest keyed on the arm's exact text (reading its own source) fails them;
  * selfref: the number of census lines matching SELFREF_RE must equal the base count 5 — a selftest that
    adds a read of its own file (`$SELF`, `$0`, `BASH_SOURCE`, /proc/self) is refused.
The arm's mount-table cross-check is the one known equivalent mutant (`$fsn` -> `$devn` in the guard:
devn > 0 implies fsn > 0, and fsn > 0 with devn == 0 sets blocked=1 first); it is excluded and named here.

Predicate (same sentence in the declaration, here and in the receipt):

    baseline_pass == 1 and neutral_pass == 3 and mutants_applied == 9 and survivors == 0
    and selfref == 5                                                                -> PASS, exit 0

Usage: score-selftest-literals-r40.py --revision <REV> --scratch <DIR> [--repo <lane>] [--branch master]
Exit: 0 PASS; 1 FAIL; 2 could-not-evaluate (binding, git, scratch). Read-only on the lane.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _revision  # noqa: E402

COUNTER_ID = 'score-selftest-literals-r40'
CENSUS = 'tools/tsukuroi-census.sh'
TOOL_ROOT = Path(__file__).resolve().parent.parent
SELFREF_RE = re.compile(r'\$\{?SELF|BASH_SOURCE|\$0\b|/proc/self/(exe|fd)|/proc/\$\$')
SELFREF_BASE = 5
PASS_RE = re.compile(r'^TSUKUROI_CENSUS_SELFTEST: PASS \((\d+) cases, (\d+) passed, 0 failed\)$')

LOOP = ('''      while read -r _src _mp fst _rest; do
        if [ "${fst:-}" = btrfs ]; then mt=$((mt + 1)); fi
      done <<< "$mtab"
      if [ "$mt" -gt 0 ]; then blocked=1; detail+='mounts:btrfs-without-sysfs,'; fi
''')


def keyed(pattern: str) -> str:
    return f"      case $mtab in {pattern}) blocked=1; detail+='mounts:btrfs-without-sysfs,' ;; esac\n"


MUTANTS = [
    ('M1-VA-device-literal', LOOP, keyed("*'/dev/mapper/root'*")),
    ('M2-VB-root-mountpoint', LOOP, keyed("*' / btrfs '*")),
    ('M3-VC-substring-btrfs', LOOP, keyed('*btrfs*')),
    ('M4-VG-subvolid-256', LOOP, keyed("*'subvolid=256'*")),
    ('M5-a-grep-count', LOOP,
     '''      mt=$(printf '%s\\n' "$mtab" | grep -c btrfs || true)
      if [ "$mt" -gt 0 ]; then blocked=1; detail+='mounts:btrfs-without-sysfs,'; fi
'''),
    ('M6-b-fstype-casefold', 'if [ "${fst:-}" = btrfs ]; then', 'if [ "${fst,,}" = btrfs ]; then'),
    ('M7-e-guard-drops-blocked', 'if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]; then', 'if [ "$fsn" -eq 0 ]; then'),
    ('M8-subvol-at-literal', LOOP, keyed("*'subvol=/@'*")),
    ('M9-last-line-only', 'mtab=$(cat -- "$PROC_MOUNTS" 2>/dev/null)', 'mtab=$(tail -n 1 -- "$PROC_MOUNTS" 2>/dev/null)'),
]
NEUTRAL = [
    ('N1-rename-counter', LOOP, LOOP.replace('mt=$((mt + 1))', 'mt=$((1 + mt))').replace('"$mt" -gt 0', '0 -lt "$mt"')),
    ('N2-double-bracket', 'if [ "${fst:-}" = btrfs ]; then', 'if [[ ${fst:-} == "btrfs" ]]; then'),
    ('N3-awk-field', LOOP,
     '''      mt=$(awk '$3 == "btrfs" { n++ } END { print n + 0 }' <<< "$mtab")
      if [ "$mt" -gt 0 ]; then blocked=1; detail+='mounts:btrfs-without-sysfs,'; fi
'''),
]


def run_selftest(text: str, d: Path, timeout: int):
    d.mkdir(parents=True, exist_ok=True)
    f = d / 'tsukuroi-census.sh'
    f.write_text(text)
    tmp = d / 'tmp'
    tmp.mkdir(exist_ok=True)
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': str(d), 'TMPDIR': str(tmp)}
    try:
        p = subprocess.run(['bash', str(f), '--selftest'], cwd='/', env=env, capture_output=True,
                           timeout=timeout)
    except subprocess.TimeoutExpired:
        return {'exit': 124, 'last': 'timeout', 'pass': False}
    lines = p.stdout.decode('utf-8', 'replace').strip().splitlines()
    last = lines[-1] if lines else ''
    fails = [l for l in lines if l.startswith('FAIL')][:3]
    return {'exit': p.returncode, 'last': last, 'pass': p.returncode == 0 and bool(PASS_RE.match(last)),
            'first_fails': fails}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--repo', default=str(TOOL_ROOT))
    ap.add_argument('--revision', required=True)
    ap.add_argument('--branch', default='master')
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--timeout', type=int, default=900)
    a = ap.parse_args(argv)
    try:
        b = _revision.bind(a.repo, a.revision, a.branch)
        p = subprocess.run(['git', '-C', a.repo, 'show', f'{b.sha}:{CENSUS}'], env=_revision.clean_env(),
                           capture_output=True, timeout=60)
        if p.returncode != 0:
            raise _revision.RevisionError(f'{CENSUS} not readable at {b.sha}')
        text = p.stdout.decode('utf-8')
        os.makedirs(a.scratch, exist_ok=True)
        work = Path(tempfile.mkdtemp(prefix='r40c1.', dir=a.scratch))
    except (_revision.RevisionError, OSError, UnicodeDecodeError) as e:
        print(json.dumps({'counter': COUNTER_ID, 'error': str(e), 'exit': 2}))
        return 2
    try:
        selfref = sum(1 for l in text.splitlines() if SELFREF_RE.search(l))
        jobs = {'baseline': text}
        applied = {}
        for kind, table in (('mutant', MUTANTS), ('neutral', NEUTRAL)):
            for name, old, new in table:
                n = text.count(old)
                applied[name] = {'kind': kind, 'occurrences': n}
                if n == 1:
                    jobs[name] = text.replace(old, new)
        res = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            futs = {ex.submit(run_selftest, t, work / n, a.timeout): n for n, t in jobs.items()}
            for f in concurrent.futures.as_completed(futs):
                res[futs[f]] = f.result()
    finally:
        shutil.rmtree(work, ignore_errors=True)
    baseline_pass = int(res['baseline']['pass'])
    mutants, neutrals = {}, {}
    for name, info in applied.items():
        row = dict(info)
        if name in res:
            row.update(res[name])
            if info['kind'] == 'mutant':
                row['killed'] = not res[name]['pass']
        (mutants if info['kind'] == 'mutant' else neutrals)[name] = row
    m_applied = sum(1 for r in mutants.values() if r['occurrences'] == 1)
    survivors = sum(1 for r in mutants.values() if r['occurrences'] == 1 and not r['killed'])
    neutral_pass = sum(1 for r in neutrals.values() if r['occurrences'] == 1 and r['pass'])
    ok = (baseline_pass == 1 and neutral_pass == len(NEUTRAL) and m_applied == len(MUTANTS)
          and survivors == 0 and selfref == SELFREF_BASE)
    rec = {'counter': COUNTER_ID, 'revision': b.sha, 'branch_tip': b.branch_tip,
           'predicate': 'baseline_pass == 1 and neutral_pass == 3 and mutants_applied == 9 and survivors == 0 '
                        'and selfref == 5',
           'baseline': res['baseline'], 'baseline_pass': baseline_pass, 'neutral_pass': neutral_pass,
           'mutants_applied': m_applied, 'survivors': survivors,
           'survivor_names': sorted(n for n, r in mutants.items() if r['occurrences'] == 1 and not r['killed']),
           'selfref': selfref, 'mutants': mutants, 'neutrals': neutrals,
           'result': 'PASS' if ok else 'FAIL', 'exit': 0 if ok else 1}
    print(json.dumps(rec, indent=1))
    return rec['exit']


if __name__ == '__main__':
    sys.exit(main())
