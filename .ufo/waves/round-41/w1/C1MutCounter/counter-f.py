#!/usr/bin/env python3
"""Round-41 C1 counter (operability): does the census `--selftest` at <REV> kill the held-out mount-table
mutants of the STORAGE arm that the round-40 selftest let through, by behaviour and not by reading itself?

Frozen before any seat scored (SCORECARD.md "Round 41 — declaration"). Closes the round-40 closure's routed
defects (corpus/lessons/round-40-verifier-spotcheck.md §6.1, §6.2; QUALITY 88):
  * R40-ANSWER-KEY (C1): a one-line `declare -f probe_storage_arm | grep -qF <markers>` prologue, or the
    same through `${0}` / `${BASH_ARGV0}`, passed the round-40 predicate with no fixture
    (.ufo/waves/round-40/w1/C1CritControl.md). Here one DECOY variant is the unmutated arm plus a dead
    here-document (`: <<'R41DECOY'`) inside probe_storage_arm that carries every mutant's replacement text
    verbatim. The decoy behaves exactly like the base arm, so a behavioural selftest PASSes it; a selftest
    that greps its own text (declare -f, $0, ${0}, BASH_ARGV0, /proc) for any mutant's text fails it. The
    decoy must PASS. A self-reader that skips here-documents is not refused (recorded limit).
  * held-out H5, H6, H9 (.ufo/waves/round-40/w1/C1HeldOutMutants.md) and H10 (count direction, new) are
    frozen mutants beside the round-40 M1-M9.
  * `first_fails` read stderr (the selftest's bad() writes FAIL lines there); scratch removed on SIGINT and
    SIGTERM as well as on normal exit.
  * kill attribution: a mutant counts as KILLED only when its run exits nonzero, prints the FAIL summary
    line with the baseline's case count, and at least one stderr `FAIL <label>` names a label the baseline
    printed as `PASS <label>` — a selftest that aborts early or prints a summary without running its
    cases does not kill — and a second run of the same mutant fails at least one of the same labels.
  * load flakiness: a failed baseline, capture, neutral or decoy run is re-run once, serially, and the
    second verdict is kept; the first is recorded under `retried`.
  * parameters (QUALITY 88): the counter captures, in its private copy only, every fixture mount table the
    selftest hands the census (one `cp` line injected at the top of `check()`), and requires a PASSing
    baseline case for each of the four declared table properties whose wanted patterns include
    `detail=mounts:btrfs-without-sysfs`: P1 a btrfs line whose mountpoint is not absolute, P2 a btrfs line
    whose source does not start with `/dev/`, P3 a btrfs line with no `subvol=` option, P4 a table with
    two or more btrfs lines.

Method: `tools/tsukuroi-census.sh` is read from <REV> (git show) into a private directory under --scratch.
A mutant, neutral or decoy is APPLIED only when its `old` text occurs exactly once (the arm is not this
claim's surface; a changed arm makes it unappliable and the run FAIL). Each variant runs
`bash <copy> --selftest` with PATH=/usr/bin:/bin, LC_ALL=C, HOME and TMPDIR inside the scratch, cwd `/`.
Neutral rewrites (NEUTRAL) are the round-40 three, unchanged. The one known equivalent mutant (`$fsn` ->
`$devn` in the guard) stays excluded. A PASS run is: exit 0 and last stdout line
`TSUKUROI_CENSUS_SELFTEST: PASS (<n> cases, <n> passed, 0 failed)`.

Predicate (same sentence in the declaration, here and in the receipt):

    baseline_pass == 1 and neutral_pass == 3 and decoy_pass == 1 and mutants_applied == 13
    and survivors == 0 and params == 4                                               -> PASS, exit 0

Usage: score-selftest-mounts-r41.py --revision <REV> --scratch <DIR> [--repo <lane>] [--branch master]
       [--jobs N] [--timeout S]
Exit: 0 PASS; 1 FAIL; 2 could-not-evaluate (binding, git, scratch). Read-only on the lane.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _revision  # noqa: E402

COUNTER_ID = 'score-selftest-mounts-r41'
CENSUS = 'tools/tsukuroi-census.sh'
TOOL_ROOT = Path(__file__).resolve().parent.parent
PASS_RE = re.compile(r'^TSUKUROI_CENSUS_SELFTEST: PASS \((\d+) cases, (\d+) passed, 0 failed\)$')
SUMMARY_RE = re.compile(r'^TSUKUROI_CENSUS_SELFTEST: (PASS|FAIL) \((\d+) cases, (\d+) passed, (\d+) failed\)$')
WANT_BLOCK = 'detail=mounts:btrfs-without-sysfs'
LABEL_TAIL = re.compile(r' \(exit \d+(?:, [A-Z]+)?\)$')  # ok() appends "(exit N[, VERDICT])" to the label

LOOP = ('''      while read -r _src _mp fst _rest; do
        if [ "${fst:-}" = btrfs ]; then mt=$((mt + 1)); fi
      done <<< "$mtab"
      if [ "$mt" -gt 0 ]; then blocked=1; detail+='mounts:btrfs-without-sysfs,'; fi
''')
COUNT_LINE = '        if [ "${fst:-}" = btrfs ]; then mt=$((mt + 1)); fi\n'


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
    ('H5-mountpoint-absolute', COUNT_LINE,
     '        if [ "${fst:-}" = btrfs ] && [[ ${_mp:-} == /* ]]; then mt=$((mt + 1)); fi\n'),
    ('H6-source-devonly', COUNT_LINE,
     '        if [ "${fst:-}" = btrfs ] && [[ ${_src:-} == /dev/* ]]; then mt=$((mt + 1)); fi\n'),
    ('H9-subvolkey-option', LOOP, keyed("*'subvol='*")),
    ('H10-count-exactly-one', '      if [ "$mt" -gt 0 ]; then blocked=1;', '      if [ "$mt" -eq 1 ]; then blocked=1;'),
]
NEUTRAL = [
    ('N1-rename-counter', LOOP, LOOP.replace('mt=$((mt + 1))', 'mt=$((1 + mt))').replace('"$mt" -gt 0', '0 -lt "$mt"')),
    ('N2-double-bracket', 'if [ "${fst:-}" = btrfs ]; then', 'if [[ ${fst:-} == "btrfs" ]]; then'),
    ('N3-awk-field', LOOP,
     '''      mt=$(awk '$3 == "btrfs" { n++ } END { print n + 0 }' <<< "$mtab")
      if [ "$mt" -gt 0 ]; then blocked=1; detail+='mounts:btrfs-without-sysfs,'; fi
'''),
]
# decoy: dead here-document carrying the mutant's replacement text, inserted in front of LOOP
DECOY_DELIM = 'R41DECOY'
CAPTURE_ANCHOR = '    local label=$1 wrc=$2 wverdict=$3\n'
CAPTURE_LINE = ('    { printf "%s\\n" "$label" "$*" > "$R41_CAP/$((PASS + FAIL)).args"; '
                '[ -f "$FX/mounts" ] && cp -- "$FX/mounts" "$R41_CAP/$((PASS + FAIL)).mounts"; } 2>/dev/null || true\n')


def decoy(texts) -> str:
    body = '\n'.join(t.rstrip('\n') for t in texts)
    return f": <<'{DECOY_DELIM}'\n{body}\n{DECOY_DELIM}\n" + LOOP


_WORK: list[Path] = []


def _cleanup(*_a):
    for w in _WORK:
        shutil.rmtree(w, ignore_errors=True)
    if _a:
        sys.exit(130)


def run_selftest(text: str, d: Path, timeout: int, cap: Path | None = None):
    d.mkdir(parents=True, exist_ok=True)
    f = d / 'tsukuroi-census.sh'
    f.write_text(text)
    tmp = d / 'tmp'
    tmp.mkdir(exist_ok=True)
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': str(d), 'TMPDIR': str(tmp)}
    if cap is not None:
        cap.mkdir(exist_ok=True)
        env['R41_CAP'] = str(cap)
    try:
        p = subprocess.run(['bash', str(f), '--selftest'], cwd='/', env=env, capture_output=True,
                           timeout=timeout)
    except subprocess.TimeoutExpired:
        return {'exit': 124, 'last': 'timeout', 'pass': False, 'labels': [], 'fail_labels': [],
                'first_fails': [], 'cases': None}
    out = p.stdout.decode('utf-8', 'replace').strip().splitlines()
    err = p.stderr.decode('utf-8', 'replace').splitlines()
    last = out[-1] if out else ''
    sm = SUMMARY_RE.match(last)
    labels = [LABEL_TAIL.sub('', l[5:]) for l in out if l.startswith('PASS ')]
    fails = [l for l in err if l.startswith('FAIL ')]
    return {'exit': p.returncode, 'last': last, 'pass': p.returncode == 0 and bool(PASS_RE.match(last)),
            'cases': int(sm.group(2)) if sm else None, 'labels': labels,
            'fail_labels': [l[5:] for l in fails], 'first_fails': fails[:3]}


def mount_props(table: str):
    lines = [l.split() for l in table.splitlines() if l.strip()]
    bt = [f for f in lines if len(f) >= 3 and f[2] == 'btrfs']
    return {
        'P1-mountpoint-not-absolute': any(not f[1].startswith('/') for f in bt),
        'P2-source-not-dev': any(not f[0].startswith('/dev/') for f in bt),
        'P3-no-subvol-option': any(len(f) < 4 or 'subvol=' not in f[3] for f in bt),
        'P4-two-btrfs-lines': len(bt) >= 2,
    }


def params_from_capture(cap: Path, passed_labels: set):
    found = {k: [] for k in ('P1-mountpoint-not-absolute', 'P2-source-not-dev', 'P3-no-subvol-option',
                             'P4-two-btrfs-lines')}
    for a in sorted(cap.glob('*.args')):
        m = a.with_suffix('.mounts')
        if not m.is_file():
            continue
        args = a.read_text(errors='replace').splitlines()
        label = args[0] if args else ''
        if label not in passed_labels or not any(WANT_BLOCK in x for x in args[1:]):
            continue
        for k, v in mount_props(m.read_text(errors='replace')).items():
            if v:
                found[k].append(label)
    return found


def failed_base_labels(res: dict, base: dict) -> set:
    """Baseline PASS labels that this run reports as FAIL (a FAIL line is `<label>: <reason>`)."""
    return {lb for fl in res['fail_labels'] for lb in base['labels'] if fl == lb or fl.startswith(lb + ':')}


def killed(res: dict, base: dict) -> bool:
    if res['pass'] or res['exit'] == 0 or res['cases'] != base['cases']:
        return False
    return bool(failed_base_labels(res, base))


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
            raise _revision.RevisionError('E-GIT-FAILED', CENSUS, f'not readable at {b.sha}')
        text = p.stdout.decode('utf-8')
        os.makedirs(a.scratch, exist_ok=True)
        work = Path(tempfile.mkdtemp(prefix='r41c1.', dir=a.scratch))
    except (_revision.RevisionError, OSError, UnicodeDecodeError) as e:
        print(json.dumps({'counter': COUNTER_ID, 'error': str(e), 'exit': 2}))
        return 2
    _WORK.append(work)
    signal.signal(signal.SIGINT, _cleanup)
    signal.signal(signal.SIGTERM, _cleanup)
    try:
        jobs, applied = {}, {}
        cap_text = text.replace(CAPTURE_ANCHOR, CAPTURE_ANCHOR + CAPTURE_LINE, 1) \
            if text.count(CAPTURE_ANCHOR) == 1 else None
        for kind, table in (('mutant', MUTANTS), ('neutral', NEUTRAL)):
            for name, old, new in table:
                n = text.count(old)
                applied[name] = {'kind': kind, 'occurrences': n}
                if n == 1:
                    jobs[name] = text.replace(old, new)
        n = text.count(LOOP)
        applied['D-all-mutant-texts'] = {'kind': 'decoy', 'occurrences': n}
        if n == 1:
            jobs['D-all-mutant-texts'] = text.replace(LOOP, decoy([new for _n, _o, new in MUTANTS]))
        res = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            futs = {ex.submit(run_selftest, text, work / 'baseline', a.timeout): 'baseline'}
            if cap_text is not None:
                futs[ex.submit(run_selftest, cap_text, work / 'capture', a.timeout, work / 'cap')] = 'capture'
            for n, t in jobs.items():
                futs[ex.submit(run_selftest, t, work / n, a.timeout)] = n
            for f in concurrent.futures.as_completed(futs):
                res[futs[f]] = f.result()
        # one serial retry: a failed non-mutant run is re-run and the second verdict kept (load flakiness,
        # round-40 C1CritControl §6); a kill is confirmed only when a re-run fails a common baseline label
        texts = dict(jobs, baseline=text)
        if cap_text is not None:
            texts['capture'] = cap_text
        for name in sorted(res):
            kind = applied.get(name, {}).get('kind', 'control')
            if not res[name]['pass']:
                first = res[name]
                res[name] = run_selftest(texts[name], work / (name + '.retry'), a.timeout,
                                         (work / 'cap2') if name == 'capture' else None)
                res[name]['retried'] = {'first_last': first['last'], 'first_fails': first['first_fails']}
                if name == 'capture':
                    shutil.rmtree(work / 'cap', ignore_errors=True)
                    (work / 'cap2').rename(work / 'cap')
        base = res['baseline']
        todo = [n for n, info in applied.items() if info['kind'] == 'mutant' and n in res and killed(res[n], base)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            futs = {ex.submit(run_selftest, texts[n], work / (n + '.confirm'), a.timeout): n for n in todo}
            for f in concurrent.futures.as_completed(futs):
                name, again = futs[f], f.result()
                common = failed_base_labels(res[name], base) & failed_base_labels(again, base)
                res[name]['confirm_labels'] = sorted(common)
                res[name]['confirm_last'] = again['last']
                res[name]['confirmed'] = killed(again, base) and bool(common)
        params = {}
        if cap_text is not None and res['capture']['pass']:
            params = params_from_capture(work / 'cap', set(base['labels']))
    finally:
        _cleanup()
    baseline_pass = int(base['pass'])
    rows = {'mutant': {}, 'neutral': {}, 'decoy': {}}
    for name, info in applied.items():
        row = dict(info)
        if name in res:
            r = {k: v for k, v in res[name].items() if k not in ('labels', 'fail_labels')}
            r['fail_count'] = len(res[name]['fail_labels'])
            row.update(r)
            if info['kind'] == 'mutant':
                row['killed'] = killed(res[name], base) and bool(res[name].get('confirmed'))
        rows[info['kind']][name] = row
    mutants, neutrals, decoys = rows['mutant'], rows['neutral'], rows['decoy']
    m_applied = sum(1 for r in mutants.values() if r['occurrences'] == 1)
    survivors = sorted(n for n, r in mutants.items() if r['occurrences'] == 1 and not r['killed'])
    neutral_pass = sum(1 for r in neutrals.values() if r['occurrences'] == 1 and r['pass'])
    decoy_pass = sum(1 for r in decoys.values() if r['occurrences'] == 1 and r['pass'])
    n_params = sum(1 for v in params.values() if v)
    ok = (baseline_pass == 1 and neutral_pass == len(NEUTRAL) and decoy_pass == 1
          and m_applied == len(MUTANTS) and not survivors and n_params == 4)
    rec = {'counter': COUNTER_ID, 'revision': b.sha, 'branch_tip': b.branch_tip,
           'predicate': 'baseline_pass == 1 and neutral_pass == 3 and decoy_pass == 1 and mutants_applied == 13 '
                        'and survivors == 0 and params == 4',
           'baseline': {k: v for k, v in base.items() if k not in ('labels', 'fail_labels')},
           'baseline_labels': len(base['labels']), 'baseline_pass': baseline_pass,
           'capture_pass': int(bool(cap_text is not None and res.get('capture', {}).get('pass'))),
           'neutral_pass': neutral_pass, 'decoy_pass': decoy_pass, 'mutants_applied': m_applied,
           'survivors': len(survivors), 'survivor_names': survivors,
           'params': n_params, 'param_cases': params,
           'mutants': mutants, 'neutrals': neutrals, 'decoys': decoys,
           'result': 'PASS' if ok else 'FAIL', 'exit': 0 if ok else 1}
    print(json.dumps(rec, indent=1))
    return rec['exit']


if __name__ == '__main__':
    sys.exit(main())
