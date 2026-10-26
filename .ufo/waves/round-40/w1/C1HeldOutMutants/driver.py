#!/usr/bin/env python3
"""Seat C1HeldOutMutants (round 40, item C1-3): held-out mutants of the STORAGE arm's
mount-table read in probe_storage_arm, census at f951f288483c1af0cef4afd458488b84cf7a2165.

Method mirrors tools/score-selftest-literals-r40.py: census text from `git show <REV>:...`
(read-only), each mutant an exact substring replacement applied only when its old text occurs
exactly once, each variant run as `bash <copy> --selftest` with TMPDIR inside this scratch,
cwd /, PATH /usr/bin:/bin. KILLED = nonzero exit or last stdout line is not the PASS summary.
Survivors get a separating-table proof: the storage-mounts-varied-home fixture table is replaced
by a separating table; pristine+sep must PASS (case valid) and mutant+sep must FAIL (case kills).
"""
import difflib
import hashlib
import json
import re
import subprocess
import time
from pathlib import Path

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = 'f951f288483c1af0cef4afd458488b84cf7a2165'
S = Path('/fast/scratch/hyaku/tsukuroi-r40/C1HeldOutMutants')
CENSUS_PATH = 'tools/tsukuroi-census.sh'
PASS_RE = re.compile(r'^TSUKUROI_CENSUS_SELFTEST: PASS \((\d+) cases, (\d+) passed, 0 failed\)$')

# Byte-exact mount-table read block inside probe_storage_arm (same constant as the frozen
# counter's LOOP; asserted to occur exactly once in the pinned text below).
LOOP = (
    '      while read -r _src _mp fst _rest; do\n'
    '        if [ "${fst:-}" = btrfs ]; then mt=$((mt + 1)); fi\n'
    '      done <<< "$mtab"\n'
    '      if [ "$mt" -gt 0 ]; then blocked=1; detail+=\'mounts:btrfs-without-sysfs,\'; fi\n'
)

TAIL = '      if [ "$mt" -gt 0 ]; then blocked=1; detail+=\'mounts:btrfs-without-sysfs,\'; fi\n'
CASE = '      case $mtab in {pat}) blocked=1; detail+=\'mounts:btrfs-without-sysfs,\' ;; esac\n'

MUTANTS = [
    ('H1-btrfstrw-adjacency', CASE.format(pat="*' btrfs rw'*")),
    ('H2-relatime-option', CASE.format(pat='*relatime*')),
    ('H3-dumppass-fields', CASE.format(pat="*' 0 0'*")),
    ('H4-first-line-only',
     '      IFS=\' \' read -r _src _mp fst _rest <<< "$mtab"\n'
     '      if [ "${fst:-}" = btrfs ]; then mt=1; fi\n' + TAIL),
    ('H5-mountpoint-absolute',
     '      while read -r _src _mp fst _rest; do\n'
     '        if [ "${fst:-}" = btrfs ] && [[ ${_mp:-} == /* ]]; then mt=$((mt + 1)); fi\n'
     '      done <<< "$mtab"\n' + TAIL),
    ('H6-source-devonly',
     '      while read -r _src _mp fst _rest; do\n'
     '        if [ "${fst:-}" = btrfs ] && [[ ${_src:-} == /dev/* ]]; then mt=$((mt + 1)); fi\n'
     '      done <<< "$mtab"\n' + TAIL),
    ('H7-threshold-two',
     '      while read -r _src _mp fst _rest; do\n'
     '        if [ "${fst:-}" = btrfs ]; then mt=$((mt + 1)); fi\n'
     '      done <<< "$mtab"\n'
     '      if [ "$mt" -gt 1 ]; then blocked=1; detail+=\'mounts:btrfs-without-sysfs,\'; fi\n'),
    ('H8-options-ro-only',
     '      while read -r _src _mp fst _rest; do\n'
     '        if [ "${fst:-}" = btrfs ] && [[ ${_rest:-} == ro,* ]]; then mt=$((mt + 1)); fi\n'
     '      done <<< "$mtab"\n' + TAIL),
    ('H9-subvolkey-option', CASE.format(pat="*'subvol='*")),
]

# Separating-table proof: replace the storage-mounts-varied-home fixture table (unique via the
# nvme line) with a table that separates pristine from the surviving mutant.
SEPFIX_OLD = (
    "  printf '%s\\n' 'proc /proc proc rw 0 0' \\\n"
    "    '/dev/nvme0n1p3 /home btrfs rw,relatime,ssd,discard=async,space_cache=v2,subvolid=5,subvol=/ 0 0' \\\n"
    "    'tmpfs /tmp tmpfs rw,nosuid,nodev 0 0' > \"$FX/mounts\"\n"
)
SEPARATING = {
    'H5-mountpoint-absolute': 'devtmpfs btrfs btrfs rw 0 0',
    'H6-source-devonly': 'UUID=0b1c2d3e-4d5e-6f70-8192-a3b4c5d6e7f8 /data btrfs rw 0 0',
    'H9-subvolkey-option': '/dev/sdc1 /mnt/plain btrfs rw,commit=60 0 0',
}


def sepfix_new(table: str) -> str:
    return ("  printf '%s\\n' 'proc /proc proc rw 0 0' \\\n"
            "    '" + table + "' > \"$FX/mounts\"\n")


def run_selftest(body: str, tag: str, name: str):
    d = S / 'runs' / f'{tag}-{name}'
    (d / 'tmp').mkdir(parents=True, exist_ok=True)
    f = d / 'tsukuroi-census.sh'
    f.write_text(body)
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': str(d), 'TMPDIR': str(d / 'tmp')}
    t0 = time.time()
    try:
        p = subprocess.run(['bash', str(f), '--selftest'], cwd='/', env=env,
                           capture_output=True, timeout=600)
        rc, out, err = p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')
    except subprocess.TimeoutExpired as e:
        rc, out, err = 124, (e.stdout or b'').decode('utf-8', 'replace'), (e.stderr or b'').decode('utf-8', 'replace')
    dt = round(time.time() - t0, 1)
    (d / 'transcript.stdout').write_text(out)
    (d / 'transcript.stderr').write_text(err)
    merged = [l for l in (out.splitlines() + err.splitlines()) if l.strip()]
    fails = [l for l in merged if l.startswith('FAIL ')][:5]
    last_out = [l for l in out.splitlines() if l.strip()]
    last = last_out[-1] if last_out else ''
    m = PASS_RE.match(last)
    passed = rc == 0 and bool(m)
    return {'tag': tag, 'name': name, 'exit': rc, 'seconds': dt, 'last': last,
            'pass': passed, 'cases': m.groups() if m else None,
            'first_fails': fails,
            'sha256': hashlib.sha256(body.encode()).hexdigest()}


def udiff(old_text, new_text, a_name, b_name):
    return '\n'.join(difflib.unified_diff(old_text.splitlines(), new_text.splitlines(),
                                          fromfile=a_name, tofile=b_name, lineterm='', n=2)) + '\n'


def main():
    S.mkdir(parents=True, exist_ok=True)
    (S / 'diffs').mkdir(exist_ok=True)
    p = subprocess.run(['git', '-C', LANE, 'show', f'{REV}:{CENSUS_PATH}'],
                       capture_output=True, timeout=60)
    assert p.returncode == 0, p.stderr.decode()
    text = p.stdout.decode('utf-8')
    n = text.count(LOOP)
    print(f'census bytes={len(text)} sha256={hashlib.sha256(text.encode()).hexdigest()}')
    print(f'LOOP occurrences={n}')
    assert n == 1, 'mount-table block not byte-unique at pinned rev'
    start = text.index(LOOP)
    line_no = text.count('\n', 0, start) + 1
    print(f'LOOP starts at line {line_no} of {CENSUS_PATH} @ {REV}')

    results = []
    r = run_selftest(text, 'base', 'pristine')
    results.append(r)
    print(f"BASELINE pass={r['pass']} exit={r['exit']} {r['last']} fails={r['first_fails']}")

    for name, new in MUTANTS:
        assert text.count(new) == 0 or True
        body = text.replace(LOOP, new, 1)
        assert body != text
        r = run_selftest(body, 'mut', name)
        r['verdict'] = 'SURVIVED' if r['pass'] else 'KILLED'
        results.append(r)
        print(f"{name}: {r['verdict']} exit={r['exit']} {r['last']} fails={r['first_fails']}")
        (S / 'diffs' / f'{name}.diff').write_text(
            udiff(text, body, f'{CENSUS_PATH}@{REV[:9]}', f'{CENSUS_PATH}@{name}'))

    for name, table in SEPARATING.items():
        mut_body = text.replace(LOOP, dict(MUTANTS)[name], 1)
        assert text.count(SEPFIX_OLD) == 1, 'varied-home fixture block not byte-unique'
        sep_pristine = text.replace(SEPFIX_OLD, sepfix_new(table), 1)
        sep_mutant = mut_body.replace(SEPFIX_OLD, sepfix_new(table), 1)
        (S / 'diffs' / f'{name}.separating.diff').write_text(
            udiff(text, sep_pristine, f'{CENSUS_PATH}@{REV[:9]}',
                  f'{CENSUS_PATH}@varied-home-separating-{name}'))
        rp = run_selftest(sep_pristine, 'seppristine', name)
        results.append(rp)
        print(f"{name} + separating table, PRISTINE: pass={rp['pass']} exit={rp['exit']} "
              f"{rp['last']} fails={rp['first_fails']}")
        rm_ = run_selftest(sep_mutant, 'sepmutant', name)
        results.append(rm_)
        print(f"{name} + separating table, MUTANT: pass={rm_['pass']} exit={rm_['exit']} "
              f"{rm_['last']} fails={rm_['first_fails']}")

    (S / 'results.json').write_text(json.dumps(
        {'rev': REV, 'census_sha256': hashlib.sha256(text.encode()).hexdigest(),
         'loop_line': line_no, 'runs': results}, indent=2))
    print('WROTE results.json')


if __name__ == '__main__':
    main()
